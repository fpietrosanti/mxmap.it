#!/usr/bin/env python3
"""Inspect the IT preprocess output — provider counts, top Local-ISP MX hosts,
top ASNs, and Unknown-entry samples — to drive the ISP discovery iteration.

Run on the server (where data.json lives) or locally after pulling data.json.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def reg_domain(host: str) -> str:
    """Crude registrable-domain extractor (last 2 labels). Good enough for
    grouping Italian PA MX hosts whose suffix is .it/.eu/.com/.org/.net."""
    if not host:
        return "?"
    parts = host.lower().rstrip(".").split(".")
    if len(parts) < 2:
        return host
    return ".".join(parts[-2:])


def first_mx_host(entry: dict) -> str | None:
    """Extract the primary MX hostname regardless of mxmap's mx field shape."""
    mxes = entry.get("mx") or []
    if not mxes:
        return None
    first = mxes[0]
    if isinstance(first, dict):
        host = first.get("exchange") or first.get("host") or ""
    elif isinstance(first, str):
        host = first
    else:
        host = ""
    host = host.strip().lower().rstrip(".")
    tokens = host.split()
    if len(tokens) == 2 and tokens[0].isdigit():
        host = tokens[1]
    return host or None


def main() -> int:
    data_path = ROOT / "data.json"
    with open(data_path, encoding="utf-8") as f:
        d = json.load(f)
    muns = d["municipalities"]  # dict keyed by id
    it = [e for e in muns.values() if e.get("country") == "IT"]
    print(f"IT entries: {len(it)}")
    print()

    # Provider distribution
    prov = Counter(e.get("provider", "?") for e in it)
    print("=== Provider distribution ===")
    total = sum(prov.values())
    for k, v in sorted(prov.items(), key=lambda kv: -kv[1]):
        pct = (v / total * 100) if total else 0
        print(f"  {k:<15} {v:>6}  ({pct:>5.1f}%)")

    # Local-ISP breakdown
    local_isps = [e for e in it if e.get("provider") == "local-isp"]
    print()
    print(f"=== Local ISP — top MX registrable domains ({len(local_isps)} total) ===")
    mx_doms = Counter()
    for e in local_isps:
        host = first_mx_host(e)
        if host:
            mx_doms[reg_domain(host)] += 1
    for dom, cnt in mx_doms.most_common(30):
        print(f"  {cnt:>5}  {dom}")

    # ASN breakdown
    print()
    print("=== Local ISP — top MX ASNs ===")
    asn_counter = Counter()
    for e in local_isps:
        asns = e.get("mx_asns") or []
        if not isinstance(asns, list):
            asns = [asns]
        for a in asns:
            asn_counter[str(a)] += 1
    if asn_counter:
        for asn, cnt in asn_counter.most_common(30):
            print(f"  {cnt:>5}  AS{asn}")
    else:
        print("  (no mx_asns field present)")

    # Independent breakdown
    independent = [e for e in it if e.get("provider") == "independent"]
    print()
    print(f"=== Independent — top MX registrable domains ({len(independent)} total) ===")
    indep_doms = Counter()
    for e in independent:
        host = first_mx_host(e)
        if host:
            indep_doms[reg_domain(host)] += 1
    for dom, cnt in indep_doms.most_common(30):
        print(f"  {cnt:>5}  {dom}")

    # Unknown sample
    unknowns = [e for e in it if e.get("provider") == "unknown"]
    print()
    print(f"=== Unknown — sample of 30 (of {len(unknowns)} total) ===")
    for e in unknowns[:30]:
        reason = (e.get("reason") or "")[:60]
        name = (e.get("name") or "?")[:32]
        domain = (e.get("domain") or "?")[:35]
        print(f"  {e.get('id', '?'):<14} {name:<32} domain={domain:<35} reason={reason}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
