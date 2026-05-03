#!/usr/bin/env python3
"""Recover Italian Unknown-MX entries by retrying classification against
domain_fallbacks (non-PEC email-derived hostnames from IndicePA).

Pipeline position: runs AFTER `uv run preprocess IT` and re-classifies any
IT entry where mxmap returned `provider=unknown` with reason
"No MX records found". The primary website domain has already been tried
and failed; we now try the IndicePA email-derived fallbacks (PEC excluded
at fetch time, see scripts/fetch_indicepa.py).

The original `domain` field is preserved (so the website is still recorded);
a new `domain_used` field is added when recovery succeeds, indicating which
fallback provided the working MX.

Usage: uv run python3 scripts/recover_it_unknowns.py
"""

from __future__ import annotations

import asyncio
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

CONCURRENCY = 20


async def classify_domain(domain: str) -> dict | None:
    """Run the full classification pipeline against `domain`. Returns None
    when no MX is found; otherwise a dict with the classification fields."""
    mx_records = await lookup_mx(domain)
    if not mx_records:
        return None
    # Run the rest of the lookups in parallel
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
        "mx": mx_records,
        "spf": spf_record,
        "spf_resolved": resolved_spf,
        "provider": provider,
        "reason": reason,
        "mx_cnames": mx_cnames,
        "mx_asns": sorted(mx_asns) if isinstance(mx_asns, set) else list(mx_asns or []),
        "mx_countries": sorted(mx_countries) if isinstance(mx_countries, set) else list(mx_countries or []),
        "autodiscover": autodiscover,
        "dkim": dkim,
        "txt_verifications": txt_verifications,
        "tenant": tenant,
    }


async def recover_one(seed_entry: dict, sem: asyncio.Semaphore) -> tuple[str, dict | None, str | None]:
    """Try each domain_fallback in order; return (entry_id, classification, domain_used).
    Returns (id, None, None) if no fallback yields MX."""
    eid = seed_entry["id"]
    fallbacks = seed_entry.get("domain_fallbacks") or []
    if not fallbacks:
        return eid, None, None
    async with sem:
        for fb in fallbacks:
            try:
                result = await classify_domain(fb)
            except Exception as e:
                print(f"  {eid}: error on fallback {fb}: {e!r}")
                continue
            if result is not None:
                return eid, result, fb
    return eid, None, None


async def main_async() -> int:
    seed_path = DATA / "municipalities_it.json"
    data_path = ROOT / "data.json"

    with open(seed_path, encoding="utf-8") as f:
        seed = json.load(f)
    seed_by_id = {e["id"]: e for e in seed}

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    muns = data["municipalities"]

    # Find IT unknowns to recover. Skip entries already recovered (have
    # `domain_used`) so re-runs are idempotent.
    candidates = []
    for k, v in muns.items():
        if v.get("country") != "IT":
            continue
        if v.get("provider") != "unknown":
            continue
        if v.get("domain_used"):
            continue
        seed_entry = seed_by_id.get(v.get("id") or k)
        if not seed_entry or not seed_entry.get("domain_fallbacks"):
            continue
        candidates.append((k, seed_entry))

    print(f"Found {len(candidates)} IT unknowns with at least one non-PEC domain_fallback")
    if not candidates:
        return 0

    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [recover_one(seed_entry, sem) for _, seed_entry in candidates]

    n_done = 0
    n_recovered = 0
    provider_counts: Counter[str] = Counter()

    for coro in asyncio.as_completed(tasks):
        eid, result, used = await coro
        n_done += 1
        if result is None:
            continue
        # Find which key in muns this id belongs to (should be eid itself)
        key = eid if eid in muns else next((k for k, v in muns.items() if v.get("id") == eid), None)
        if key is None:
            continue
        entry = muns[key]
        # Preserve original domain; add domain_used and overlay classification
        entry["domain_used"] = used
        for k, v in result.items():
            entry[k] = v
        n_recovered += 1
        provider_counts[result["provider"]] += 1
        if n_done % 20 == 0:
            print(f"  [{n_done}/{len(candidates)}] recovered={n_recovered}")

    # Recompute counts at the data.json top level
    counts: Counter[str] = Counter(v.get("provider", "unknown") for v in muns.values())
    data["counts"] = dict(counts)

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print()
    print(f"=== Recovery summary ===")
    print(f"  Candidates with fallbacks  : {len(candidates)}")
    print(f"  Recovered (MX found)       : {n_recovered}")
    print(f"  Still unknown after retry  : {len(candidates) - n_recovered}")
    print()
    print(f"=== New provider distribution among recovered ===")
    for k, v in sorted(provider_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<25} {v:>4}")
    print()
    print(f"Wrote {data_path}")
    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
