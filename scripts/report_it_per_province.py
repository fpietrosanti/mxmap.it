#!/usr/bin/env python3
"""Per-provincia provider-distribution report for Italian comuni.

Groups all classified IT comuni by the 3-digit ISTAT province code (extracted
from `Codice_comune_ISTAT[:3]` in the seed) and reports the provider mix per
province. Also emits an aggregate region-level table.

Output: data/reports/it_per_province.txt and data/reports/it_per_province.json

Run after the full pipeline (preprocess + recover + reclassify_provincial).
Usage: uv run python3 scripts/report_it_per_province.py
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = DATA / "reports"

# ISTAT region code → name (Italian).
ISTAT_REGION_NAME: dict[str, str] = {
    "01": "Piemonte",
    "02": "Valle d'Aosta",
    "03": "Lombardia",
    "04": "Trentino-Alto Adige",
    "05": "Veneto",
    "06": "Friuli-Venezia Giulia",
    "07": "Liguria",
    "08": "Emilia-Romagna",
    "09": "Toscana",
    "10": "Umbria",
    "11": "Marche",
    "12": "Lazio",
    "13": "Abruzzo",
    "14": "Molise",
    "15": "Campania",
    "16": "Puglia",
    "17": "Basilicata",
    "18": "Calabria",
    "19": "Sicilia",
    "20": "Sardegna",
}

# ISTAT province code (3-digit) → name. Italian provinces don't follow a clean
# region prefix (province codes are sequential ~001..111 with reform-induced
# gaps). For the report we derive the region per-comune from the seed.
# We only use this for display in the per-province table; the source of truth
# is the seed's region field once populated.


def shorten(provider: str) -> str:
    """Map mxmap provider tag to a compact column header."""
    return {
        "microsoft": "MS",
        "google": "Goog",
        "aws": "AWS",
        "aruba": "Aruba",
        "register-it": "Reg.it",
        "seeweb": "Seeweb",
        "infocert": "InfoC",
        "namirial": "Nam",
        "regional-public": "Pub",
        "pa-contractor-private": "Priv",
        "provincial-shared": "Prov",
        "local-isp": "ISP",
        "independent": "Indep",
        "unknown": "?",
    }.get(provider, provider[:6])


PROVIDER_ORDER = [
    "microsoft", "google", "aruba", "register-it", "seeweb",
    "infocert", "namirial", "regional-public", "pa-contractor-private",
    "provincial-shared", "local-isp", "independent", "aws",
    "unknown",
]


def main() -> int:
    seed_path = DATA / "municipalities_it.json"
    data_path = ROOT / "data.json"
    REPORTS.mkdir(parents=True, exist_ok=True)

    with open(seed_path, encoding="utf-8") as f:
        seed = json.load(f)
    seed_by_id = {e["id"]: e for e in seed}

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    muns = data["municipalities"]

    # Group comuni by 3-digit province ISTAT, plus collect all relevant data.
    by_prov: dict[str, list[dict]] = defaultdict(list)
    by_region: dict[str, list[dict]] = defaultdict(list)

    for key, entry in muns.items():
        if entry.get("country") != "IT":
            continue
        # Only comuni for this report (id starts with IT-COM).
        eid = entry.get("id") or key
        if not eid.startswith("IT-COM-"):
            continue
        seed_entry = seed_by_id.get(eid)
        if not seed_entry:
            continue
        com_istat = seed_entry.get("ipa_codice_comune_istat") or ""
        if not com_istat or len(com_istat) < 3:
            continue
        prov_istat = com_istat[:3].zfill(3)
        # Region extraction: keep first 2 digits of comune ISTAT only when
        # it falls in the standard 01..20 range. ISTAT's province numbering
        # doesn't always encode region, but the comune's region is in the
        # seed_entry["region"] when populated.
        region = seed_entry.get("region")
        merged = dict(entry)
        merged["_prov_istat"] = prov_istat
        merged["_region"] = region
        merged["_seed_name"] = seed_entry.get("name", "")
        by_prov[prov_istat].append(merged)
        if region:
            by_region[region].append(merged)

    # --- Build TEXT report ---
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("Italian per-provincia email-provider distribution")
    lines.append("=" * 100)
    lines.append(f"Source: {data_path}  ({len(muns)} total entries)")
    lines.append(f"Comuni analyzed: {sum(len(v) for v in by_prov.values())}")
    lines.append("")

    header_cols = ["Prov", "N"] + [shorten(p) for p in PROVIDER_ORDER]
    lines.append("  ".join(f"{c:>5}" for c in header_cols))
    lines.append("-" * 100)

    rows = []
    for prov in sorted(by_prov):
        entries = by_prov[prov]
        provider_counts = Counter(e.get("provider", "unknown") for e in entries)
        row = [prov, str(len(entries))]
        for p in PROVIDER_ORDER:
            row.append(str(provider_counts.get(p, "")))
        rows.append(row)
    for row in rows:
        lines.append("  ".join(f"{c:>5}" for c in row))
    lines.append("-" * 100)
    # Totals
    grand = Counter()
    for entries in by_prov.values():
        grand.update(e.get("provider", "unknown") for e in entries)
    total_n = sum(grand.values())
    total_row = ["TOT", str(total_n)] + [str(grand.get(p, 0)) for p in PROVIDER_ORDER]
    lines.append("  ".join(f"{c:>5}" for c in total_row))
    lines.append("")

    lines.append("=" * 100)
    lines.append("Aggregate provider distribution (Italian comuni)")
    lines.append("=" * 100)
    for p in PROVIDER_ORDER + sorted(set(grand) - set(PROVIDER_ORDER)):
        n = grand.get(p, 0)
        if n == 0:
            continue
        pct = (n / total_n * 100) if total_n else 0.0
        lines.append(f"  {p:<25} {n:>5}  ({pct:>5.1f}%)")
    lines.append("")

    text_path = REPORTS / "it_per_province.txt"
    text_path.write_text("\n".join(lines), encoding="utf-8")
    print(text_path)

    # --- Build JSON report (machine-readable for the web UI later) ---
    json_report = {
        "source": str(data_path.name),
        "comuni_analyzed": sum(len(v) for v in by_prov.values()),
        "aggregate": {p: grand.get(p, 0) for p in PROVIDER_ORDER + sorted(set(grand) - set(PROVIDER_ORDER))},
        "per_province": {
            prov: {
                "n": len(entries),
                "providers": dict(Counter(e.get("provider", "unknown") for e in entries)),
            }
            for prov, entries in sorted(by_prov.items())
        },
        "per_region": {
            region: {
                "n": len(entries),
                "providers": dict(Counter(e.get("provider", "unknown") for e in entries)),
            }
            for region, entries in sorted(by_region.items())
        },
    }
    json_path = REPORTS / "it_per_province.json"
    json_path.write_text(json.dumps(json_report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
