#!/usr/bin/env python3
"""Probe each Italian provincial-shared mail domain (XX.it where XX is a
2-letter province code) to discover its actual mail backend.

Output: data/it_provincial_backends.json — a dict mapping 2-letter province
code -> {provider, reason, mx, mx_asns, dkim, tenant, ...}.

Used by scripts/reclassify_it_provincial.py: when a comune's MX is on
provincial-shared XX.it, we now assign the comune the SAME provider as
the provincial server itself — because the comune's email is effectively
hosted via the province's infrastructure.

Sovereignty interpretation (per user direction):
  * If provincial server is on Microsoft 365 / Google Workspace / AWS:
    the comune is on that hyperscaler (USA jurisdiction).
  * If provincial server is on Aruba / Register.it / Seeweb / etc.:
    the comune is on Italian commercial provider (Provider Italiano).
  * If provincial server is self-hosted by the province (no hyperscaler
    signal): the comune is on Italian publicly-owned regional ICT
    (Cloud Italiano) — because the provincia IS a public administration,
    so its mail infrastructure is sovereign-by-construction.
  * If provincial server has no MX or is otherwise broken: keep as
    `provincial-shared` (couldn't determine).

Pipeline position: runs AFTER preprocess and BEFORE
scripts/reclassify_it_provincial.py. Idempotent — output cached on disk.

Usage: uv run python3 scripts/probe_it_provincial_backends.py
"""

from __future__ import annotations

import asyncio
import datetime as _dt
import json
from collections import Counter
from pathlib import Path

from mail_sovereignty.classify import classify
from mail_sovereignty.dns import (
    lookup_autodiscover,
    lookup_dkim,
    lookup_mx,
    lookup_spf,
    lookup_tenant,
    lookup_txt,
    resolve_mx_asns,
    resolve_mx_cnames,
    resolve_mx_countries,
    resolve_spf_includes,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_PATH = DATA / "it_provincial_backends.json"

# Italian 2-letter province codes (license-plate / ISTAT). Includes active
# province plus historical codes still seen in legacy XX.it provincial mail
# infrastructure. Mirror of the set in reclassify_it_provincial.py.
ITALIAN_PROVINCE_CODES = sorted({
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

CONCURRENCY = 10


async def probe_domain(domain: str) -> dict | None:
    """Run full mxmap classify() against a single domain. Returns None if no MX."""
    mx_records = await lookup_mx(domain)
    if not mx_records:
        return None
    spf_task = asyncio.create_task(lookup_spf(domain))
    txt_task = asyncio.create_task(lookup_txt(domain))
    cname_task = asyncio.create_task(resolve_mx_cnames(mx_records))
    asn_task = asyncio.create_task(resolve_mx_asns(mx_records))
    country_task = asyncio.create_task(resolve_mx_countries(mx_records))
    autodiscover_task = asyncio.create_task(lookup_autodiscover(domain))
    dkim_task = asyncio.create_task(lookup_dkim(domain))
    tenant_task = asyncio.create_task(lookup_tenant(domain))

    spf_record = await spf_task
    _spf_raw, txt_verifications = await txt_task
    mx_cnames = await cname_task
    mx_asns = await asn_task
    mx_countries = await country_task
    autodiscover = await autodiscover_task
    dkim = await dkim_task
    tenant = await tenant_task
    resolved_spf = await resolve_spf_includes(spf_record) if spf_record else None

    provider, reason = classify(
        mx_records=mx_records,
        spf_record=spf_record,
        mx_cnames=mx_cnames,
        mx_asns=mx_asns,
        resolved_spf=resolved_spf,
        autodiscover=autodiscover,
        dkim=dkim,
        txt_verifications=txt_verifications,
        tenant=tenant,
    )
    return {
        "provider": provider,
        "reason": reason,
        "mx": mx_records,
        "mx_asns": sorted(mx_asns) if isinstance(mx_asns, set) else list(mx_asns or []),
        "mx_countries": sorted(mx_countries) if isinstance(mx_countries, set) else list(mx_countries or []),
        "spf": spf_record,
        "spf_resolved": resolved_spf,
        "autodiscover": autodiscover,
        "dkim": dkim,
        "txt_verifications": txt_verifications,
        "tenant": tenant,
        "mx_cnames": mx_cnames,
    }


async def probe_one_province(code: str, sem: asyncio.Semaphore) -> tuple[str, dict | None]:
    """Probe a single 2-letter province code's XX.it domain."""
    domain = f"{code}.it"
    async with sem:
        try:
            result = await probe_domain(domain)
        except Exception as e:
            return code, {"provider": "error", "reason": f"{type(e).__name__}: {e}"}
    return code, result


async def main_async() -> int:
    sem = asyncio.Semaphore(CONCURRENCY)
    print(f"Probing {len(ITALIAN_PROVINCE_CODES)} Italian province domains "
          f"(XX.it, X = 2-letter province code)...")

    results: dict[str, dict | None] = {}
    tasks = [probe_one_province(code, sem) for code in ITALIAN_PROVINCE_CODES]
    n_done = 0
    for coro in asyncio.as_completed(tasks):
        code, result = await coro
        results[code] = result
        n_done += 1
        if n_done % 20 == 0:
            print(f"  [{n_done}/{len(ITALIAN_PROVINCE_CODES)}]")

    out = {
        "metadata": {
            "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "source": "mxmap classify() against XX.it for each Italian province code",
            "n_codes": len(ITALIAN_PROVINCE_CODES),
        },
        "by_province_code": dict(sorted(results.items())),
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # Stats
    print()
    counts: Counter[str] = Counter()
    for code, r in results.items():
        if r is None:
            counts["(no MX)"] += 1
        else:
            counts[r.get("provider", "?")] += 1
    print("=== Backend distribution across XX.it provincial domains ===")
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<25} {v:>4}")
    print(f"\nWritten {OUT_PATH}")
    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
