#!/usr/bin/env python3
"""Analytical report on IndicePA entries dropped at seed-build time.

`scripts/fetch_indicepa.py` drops a row when:
  (a) Ente_in_liquidazione = 'S'
  (b) Sito_istituzionale missing or syntactically invalid (any TLD accepted)
  (c) For territorial categories L4/L5/L45/L6: name matches consorzio /
      associazione / unione / comunità montana

This script audits ALL ~23,683 IndicePA entries against those rules and
produces a report broken down by drop reason and by IPA category. For
each "no website" entry it also reports the Mail{1..5} fields so we can
see how many have a non-PEC email we could use as fallback.

Output:
  data/reports/it_seed_dropouts.txt
  data/reports/it_seed_dropouts.json (machine-readable by drop reason)

Usage: uv run python3 scripts/report_it_seed_dropouts.py
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = DATA / "reports"

CKAN_BASE = "https://indicepa.gov.it/ipa-dati/api/3/action"
RESOURCE_ID = "d09adf99-dc10-4349-8c53-27b1e5aa97b6"
USER_AGENT = "mxmap.it-seed-dropouts/0.1"
PAGE_SIZE = 5000

HOSTNAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+$")

NON_TERRITORIAL_NAME_RE = re.compile(
    r"\b(consorzio|associazione|unione\s+(?:dei|di|del)\s+comuni|"
    r"unione\s+montana|unione\s+territoriale|"
    r"comunit[aà]\s+montana|comunit[aà]\s+collinare|comunit[aà]\s+isolana)\b",
    re.IGNORECASE,
)
TERRITORIAL_CODES = {"L4", "L5", "L45", "L6"}


def fetch_all() -> list[dict]:
    """Pull every IndicePA row by paginating across all categories."""
    rows: list[dict] = []
    offset = 0
    while True:
        params = {"resource_id": RESOURCE_ID, "limit": PAGE_SIZE, "offset": offset}
        url = f"{CKAN_BASE}/datastore_search?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if not data.get("success"):
            raise RuntimeError(f"CKAN error at offset {offset}")
        records = data["result"]["records"]
        rows.extend(records)
        if len(records) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(0.4)
    return rows


def extract_domain(sito: str | None) -> str | None:
    if not sito:
        return None
    s = sito.strip()
    if not s:
        return None
    if "://" not in s:
        s = "//" + s
    parsed = urlparse(s)
    host = (parsed.hostname or "").lower().strip()
    if not host:
        return None
    if host.startswith("www."):
        host = host[4:]
    if not HOSTNAME_RE.match(host):
        return None
    return host


def is_territorial_kept(name: str, codice_categoria: str) -> bool:
    """Mirror of fetch_indicepa.is_territorial — returns True when kept."""
    if codice_categoria not in TERRITORIAL_CODES:
        return True  # only territorial categories trigger the consorzi filter
    if not name:
        return False
    return NON_TERRITORIAL_NAME_RE.search(name) is None


def classify_row(row: dict) -> tuple[str, dict]:
    """Return (drop_reason | 'KEPT', {emails, has_non_pec_email, has_pec, ...})"""
    extras: dict = {}
    name = (row.get("Denominazione_ente") or "").strip()
    cat = (row.get("Codice_Categoria") or "").strip()
    extras["name"] = name
    extras["cat"] = cat
    extras["codice_ipa"] = (row.get("Codice_IPA") or "").strip()
    extras["sito_istituzionale"] = (row.get("Sito_istituzionale") or "").strip()

    # Collect mail fields
    mails_pec: list[str] = []
    mails_non_pec: list[str] = []
    for n in range(1, 6):
        addr = (row.get(f"Mail{n}") or "").strip()
        kind = (row.get(f"Tipo_Mail{n}") or "").strip().lower()
        if not addr or "@" not in addr:
            continue
        if kind == "pec":
            mails_pec.append(addr)
        else:
            mails_non_pec.append(addr)
    extras["mails_pec"] = mails_pec
    extras["mails_non_pec"] = mails_non_pec
    extras["has_non_pec_email"] = bool(mails_non_pec)
    extras["has_pec"] = bool(mails_pec)

    # Drop reasons
    if (row.get("Ente_in_liquidazione") or "").strip().upper() == "S":
        return "in_liquidazione", extras

    domain = extract_domain(row.get("Sito_istituzionale"))
    if not domain:
        # Sub-classify based on whether email is salvageable
        if mails_non_pec:
            return "no_website_has_non_pec_email", extras
        if mails_pec:
            return "no_website_pec_only", extras
        return "no_website_no_email", extras

    if cat in TERRITORIAL_CODES and not is_territorial_kept(name, cat):
        return "consorzio_associazione_filtered", extras

    return "KEPT", extras


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    print("Fetching all IndicePA records (paginated)...")
    rows = fetch_all()
    print(f"  Total IndicePA rows: {len(rows)}")

    by_reason: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        reason, extras = classify_row(row)
        by_reason[reason].append(extras)

    lines: list[str] = []
    lines.append("=" * 100)
    lines.append(f"Seed-dropout report — IndicePA total {len(rows)}")
    lines.append("=" * 100)
    lines.append("")
    for reason, items in sorted(by_reason.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"  {reason:<40} {len(items):>5}")
    lines.append("")

    # Detail: no_website_has_non_pec_email — recoverable via email-domain fallback
    recov = by_reason.get("no_website_has_non_pec_email", [])
    if recov:
        lines.append("=" * 100)
        lines.append(f"## RECOVERABLE: {len(recov)} enti senza Sito_istituzionale ma con email non-PEC")
        lines.append("=" * 100)
        lines.append("")
        # Aggregate by email-domain to see what infrastructure they use
        host_counter: Counter[str] = Counter()
        cat_counter: Counter[str] = Counter()
        for e in recov:
            cat_counter[e["cat"]] += 1
            for addr in e["mails_non_pec"]:
                host = addr.rsplit("@", 1)[1].lower().strip().rstrip(".")
                if host.startswith("www."):
                    host = host[4:]
                # Use registrable domain (last 2 labels)
                parts = host.split(".")
                reg = ".".join(parts[-2:]) if len(parts) >= 2 else host
                host_counter[reg] += 1
        lines.append("Per categoria IPA:")
        for c, n in cat_counter.most_common():
            lines.append(f"  {c:<5} {n}")
        lines.append("")
        lines.append("Top 25 registrable email-domains tra i recuperabili:")
        for d, n in host_counter.most_common(25):
            lines.append(f"  {n:>5}  {d}")
        lines.append("")
        # Sample 30 rows for human inspection
        lines.append("--- Sample 30 entries ---")
        for e in recov[:30]:
            lines.append(f"  [{e['cat']:<5}] {e['name'][:50]:<50}  "
                         f"non-pec: {(e['mails_non_pec'][0] if e['mails_non_pec'] else '?')[:55]}")

    # Detail: no_website_pec_only — only PEC available
    peconly = by_reason.get("no_website_pec_only", [])
    if peconly:
        lines.append("")
        lines.append("=" * 100)
        lines.append(f"## PEC-ONLY: {len(peconly)} enti senza Sito_istituzionale, solo PEC")
        lines.append("=" * 100)
        cat_counter = Counter()
        pec_host_counter: Counter[str] = Counter()
        for e in peconly:
            cat_counter[e["cat"]] += 1
            for addr in e["mails_pec"]:
                host = addr.rsplit("@", 1)[1].lower().strip().rstrip(".")
                parts = host.split(".")
                reg = ".".join(parts[-2:]) if len(parts) >= 2 else host
                pec_host_counter[reg] += 1
        lines.append("Per categoria IPA:")
        for c, n in cat_counter.most_common():
            lines.append(f"  {c:<5} {n}")
        lines.append("")
        lines.append("Top 15 PEC providers di questi:")
        for d, n in pec_host_counter.most_common(15):
            lines.append(f"  {n:>5}  {d}")

    # Detail: no_website_no_email — completely unreachable
    nothing = by_reason.get("no_website_no_email", [])
    if nothing:
        lines.append("")
        lines.append("=" * 100)
        lines.append(f"## TRULY NOTHING: {len(nothing)} enti senza website e senza email")
        lines.append("=" * 100)
        cat_counter = Counter(e["cat"] for e in nothing)
        for c, n in cat_counter.most_common():
            lines.append(f"  {c:<5} {n}")

    # Detail: in_liquidazione
    liq = by_reason.get("in_liquidazione", [])
    if liq:
        lines.append("")
        lines.append("=" * 100)
        lines.append(f"## IN LIQUIDAZIONE: {len(liq)} enti")
        lines.append("=" * 100)
        cat_counter = Counter(e["cat"] for e in liq)
        for c, n in cat_counter.most_common(15):
            lines.append(f"  {c:<5} {n}")

    out_txt = REPORTS / "it_seed_dropouts.txt"
    out_txt.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_txt}")

    # JSON for downstream consumption
    payload = {
        "total": len(rows),
        "by_reason_counts": {k: len(v) for k, v in by_reason.items()},
        "recoverable_with_non_pec_email": [
            {
                "codice_ipa": e["codice_ipa"], "name": e["name"], "cat": e["cat"],
                "non_pec_email": e["mails_non_pec"][0] if e["mails_non_pec"] else None,
                "all_non_pec_emails": e["mails_non_pec"],
            }
            for e in recov
        ],
        "pec_only": [
            {
                "codice_ipa": e["codice_ipa"], "name": e["name"], "cat": e["cat"],
                "pec_email": e["mails_pec"][0] if e["mails_pec"] else None,
            }
            for e in peconly
        ],
    }
    out_json = REPORTS / "it_seed_dropouts.json"
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_json}")
    print()
    print("Summary:")
    for reason, items in sorted(by_reason.items(), key=lambda kv: -len(kv[1])):
        print(f"  {reason:<40} {len(items):>5}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
