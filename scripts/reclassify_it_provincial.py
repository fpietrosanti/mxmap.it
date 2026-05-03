#!/usr/bin/env python3
"""Reclassify Italian entries whose MX is on a 2-letter province SLD (XX.it).

The XX.it naming pattern is widely used in Italian PA for provincial-shared
mail infrastructure (e.g., comune.alessandria.al.it has MX on something.al.it,
where al.it is a Provincia di Alessandria shared mail server).

This is a *naming convention*, not a provider — the actual backend behind the
provincial mail server may still be Microsoft 365, Google Workspace, Aruba, or
self-hosted. So for each entry whose MX matches XX.it (with XX in the valid
Italian province code set), we re-run a focused look-through against the
*comune's own* DKIM / SPF / autodiscover / MS365-tenant to find the true backend.

If a hyperscaler tenant is found → reclassify as that provider, reason notes
the provincial gateway. Otherwise → label as `provincial-shared` with the
province code in the reason.

Pipeline position: runs AFTER preprocess + recover_it_unknowns.

Usage: uv run python3 scripts/reclassify_it_provincial.py
"""

from __future__ import annotations

import asyncio
import json
import re
from collections import Counter
from pathlib import Path

from mail_sovereignty.classify import classify_from_dkim, classify_from_autodiscover
from mail_sovereignty.dns import (
    lookup_autodiscover,
    lookup_dkim,
    lookup_spf,
    lookup_tenant,
    lookup_txt,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

CONCURRENCY = 20

# Italian province license-plate / ISTAT 2-letter codes used as second-level
# domains by provincial-shared mail infrastructure. Includes currently active
# province as well as historical codes still seen in legacy domains.
ITALIAN_PROVINCE_CODES = frozenset({
    "ag", "al", "an", "ao", "ap", "aq", "ar", "at", "av",
    "ba", "bg", "bi", "bl", "bn", "bo", "br", "bs", "bt", "bz",
    "ca", "cb", "ce", "ch", "ci", "cl", "cn", "co", "cr", "cs", "ct", "cz",
    "en", "fc", "fe", "fg", "fi", "fm", "fr",
    "ge", "go", "gr",
    "im", "is",
    "kr",
    "lc", "le", "li", "lo", "lt", "lu",
    "mb", "mc", "me", "mi", "mn", "mo", "ms", "mt",
    "na", "no", "nu",
    "og", "or", "ot",
    "pa", "pc", "pd", "pe", "pg", "pi", "pn", "po", "pr", "pt", "pu", "pv", "pz",
    "ra", "rc", "re", "rg", "ri", "rm", "rn", "ro",
    "sa", "si", "so", "sp", "sr", "ss", "su", "sv",
    "ta", "te", "tn", "to", "tp", "tr", "ts", "tv",
    "ud",
    "va", "vb", "vc", "ve", "vi", "vr", "vs", "vt", "vv",
})

# Match "<host>.<XX>.it" where XX is exactly two letters. We further check
# that XX is in ITALIAN_PROVINCE_CODES to avoid false positives.
PROVINCE_MX_RE = re.compile(r"^.+\.([a-z]{2})\.it\.?$", re.IGNORECASE)


def first_mx_host(entry: dict) -> str | None:
    mxes = entry.get("mx") or []
    if not mxes:
        return None
    h = mxes[0]
    if isinstance(h, dict):
        h = h.get("exchange") or h.get("host") or ""
    if not isinstance(h, str):
        return None
    h = h.strip().lower().rstrip(".")
    tokens = h.split()
    if len(tokens) == 2 and tokens[0].isdigit():
        h = tokens[1]
    return h or None


def detect_province(entry: dict) -> str | None:
    """Return the 2-letter province code if any of the entry's MX hosts
    match the XX.it pattern (with XX in the valid set). None otherwise."""
    for mx in entry.get("mx") or []:
        if isinstance(mx, dict):
            mx = mx.get("exchange") or mx.get("host") or ""
        if not isinstance(mx, str):
            continue
        h = mx.strip().lower().rstrip(".")
        tokens = h.split()
        if len(tokens) == 2 and tokens[0].isdigit():
            h = tokens[1]
        m = PROVINCE_MX_RE.match(h)
        if not m:
            continue
        code = m.group(1).lower()
        if code in ITALIAN_PROVINCE_CODES:
            return code
    return None


async def look_through(domain: str) -> tuple[str | None, str]:
    """Look-through pattern: query the comune's OWN DKIM / autodiscover /
    tenant / SPF. Return (provider, evidence_string) where provider may be
    None if nothing definitive is found."""
    dkim_task = asyncio.create_task(lookup_dkim(domain))
    autodiscover_task = asyncio.create_task(lookup_autodiscover(domain))
    tenant_task = asyncio.create_task(lookup_tenant(domain))
    spf_task = asyncio.create_task(lookup_spf(domain))
    txt_task = asyncio.create_task(lookup_txt(domain))

    dkim = await dkim_task
    autodiscover = await autodiscover_task
    tenant = await tenant_task
    spf = await spf_task
    _spf, txt_verifications = await txt_task

    # 1) DKIM CNAME — strongest signal
    p = classify_from_dkim(dkim)
    if p:
        return p, f"DKIM signs via {p}"

    # 2) Autodiscover SRV/CNAME pointing to a hyperscaler
    p = classify_from_autodiscover(autodiscover)
    if p:
        return p, f"autodiscover -> {p}"

    # 3) MS365 tenant lookup (getuserrealm.srf)
    if tenant:
        return "microsoft", f"MS365 tenant ({tenant})"

    # 4) TXT verification tokens (MS=, google-site-verification=)
    if "microsoft" in (txt_verifications or {}):
        return "microsoft", "MS= verification token"
    if "google" in (txt_verifications or {}):
        return "google", "google-site-verification token"

    return None, "no DKIM/autodiscover/tenant/TXT signal"


async def reclassify_one(
    key: str,
    entry: dict,
    province_code: str,
    sem: asyncio.Semaphore,
) -> tuple[str, str | None, str, str]:
    """Try the look-through. Return (key, new_provider_or_None_for_provincial,
    evidence, province_code)."""
    domain = entry.get("domain")
    if not domain:
        return key, None, "no primary domain", province_code
    async with sem:
        try:
            provider, evidence = await look_through(domain)
        except Exception as e:
            return key, None, f"error: {e!r}", province_code
    return key, provider, evidence, province_code


async def main_async() -> int:
    data_path = ROOT / "data.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    muns = data["municipalities"]

    candidates: list[tuple[str, dict, str]] = []
    for key, entry in muns.items():
        if entry.get("country") != "IT":
            continue
        # Skip hyperscalers (already correctly classified)
        if entry.get("provider") in {"microsoft", "google", "aws", "zoho", "yandex"}:
            continue
        # Skip if already reclassified by this script
        if entry.get("provincial_gateway"):
            continue
        province_code = detect_province(entry)
        if not province_code:
            continue
        candidates.append((key, entry, province_code))

    print(f"Found {len(candidates)} IT entries with MX on XX.it (provincial-shared pattern)")
    if not candidates:
        return 0

    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [reclassify_one(k, e, p, sem) for k, e, p in candidates]

    province_distribution: Counter[str] = Counter()
    backend_found: Counter[str] = Counter()
    no_backend = 0
    n_done = 0

    for coro in asyncio.as_completed(tasks):
        key, provider, evidence, province_code = await coro
        n_done += 1
        entry = muns[key]
        province_distribution[province_code] += 1
        entry["provincial_gateway"] = province_code
        if provider:
            entry["provider"] = provider
            entry["reason"] = (
                f"via provincial gateway {province_code}.it; {evidence}"
            )
            backend_found[provider] += 1
        else:
            entry["provider"] = "provincial-shared"
            entry["reason"] = (
                f"shared mail on provincia {province_code}; "
                f"no hyperscaler backend detected ({evidence})"
            )
            no_backend += 1
        if n_done % 50 == 0:
            print(
                f"  [{n_done}/{len(candidates)}] backend_found="
                f"{sum(backend_found.values())}  provincial_only={no_backend}"
            )

    # Recompute counts
    counts: Counter[str] = Counter(v.get("provider", "unknown") for v in muns.values())
    data["counts"] = dict(counts)

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print()
    print("=== Reclassification summary ===")
    print(f"  Total candidates                  : {len(candidates)}")
    print(f"  Reclassified to actual backend    : {sum(backend_found.values())}")
    print(f"  Stayed as 'provincial-shared'     : {no_backend}")
    print()
    print("=== Backends detected behind provincial gateways ===")
    for prov, n in backend_found.most_common():
        print(f"  {prov:<25} {n:>4}")
    print()
    print("=== Top provinces (by entry count using provincial mail) ===")
    for code, n in province_distribution.most_common(20):
        print(f"  {code:<3} {n:>4}")
    print()
    print(f"Wrote {data_path}")
    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
