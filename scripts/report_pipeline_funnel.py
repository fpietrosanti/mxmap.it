#!/usr/bin/env python3
"""Generate the IndicePA pipeline funnel report — what fraction of entities
were validated at first attempt vs needed which fix vs remain unmapped.

Output: data/it_pipeline_funnel.json
{
  "generated": "...",
  "indicepa_total": 23684,
  "in_seed": 22967,
  "coverage_pct": 96.97,
  "stages": [
    {"label": "...", "count": ..., "pct": ...},
    ...
  ],
  "summary_sentence": "Su 23.684 enti IndicePA, 22.967 (96.97%) sono ..."
}

This is consumed by the frontend "Informazioni" link to display a
transparency report on the dataset coverage. Auto-updates on every
pipeline run (new step in server_autorun_full_pipeline.sh).

Run AFTER fetch_indicepa.py:
  uv run python3 scripts/report_pipeline_funnel.py
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_FILE = DATA / "it_pipeline_funnel.json"

CKAN_BASE = "https://indicepa.gov.it/ipa-dati/api/3/action"
RESOURCE_ID = "d09adf99-dc10-4349-8c53-27b1e5aa97b6"
PAGE_SIZE = 5000
USER_AGENT = "mxmap.it-pipeline-funnel/0.1"
HOSTNAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+$")


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8")


def fetch_indicepa_all() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0
    while True:
        params = {"resource_id": RESOURCE_ID, "limit": PAGE_SIZE, "offset": offset}
        url = f"{CKAN_BASE}/datastore_search?{urllib.parse.urlencode(params)}"
        d = json.loads(http_get(url))
        recs = d["result"]["records"]
        rows.extend(recs)
        if len(recs) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(0.4)
    return rows


def has_valid_sito(row: dict) -> bool:
    sito = (row.get("Sito_istituzionale") or "").strip()
    if not sito:
        return False
    s = sito if "://" in sito else "//" + sito
    try:
        from urllib.parse import urlparse
        host = (urlparse(s).hostname or "").lower().lstrip("www.")
    except Exception:
        return False
    return bool(host and HOSTNAME_RE.match(host))


def main() -> int:
    seed_path = DATA / "municipalities_it.json"
    if not seed_path.exists():
        print(f"FATAL: {seed_path} missing — run fetch_indicepa first")
        return 1
    seed = json.loads(seed_path.read_text(encoding="utf-8"))

    # Index seed by codice IPA -> domain_source
    seed_by_ipa = {}
    for e in seed:
        ipa = (e.get("ipa_codice_ipa") or "").lower()
        if ipa:
            seed_by_ipa[ipa] = e

    print("Fetching IndicePA…")
    rows = fetch_indicepa_all()
    total = len(rows)
    print(f"  total IndicePA rows: {total}")

    # Walk every IndicePA row, classify by what fix path placed it (if any)
    bucket = Counter()
    for r in rows:
        if (r.get("Ente_in_liquidazione") or "").strip().upper() == "S":
            bucket["in_liquidazione"] += 1
            continue
        ipa = (r.get("Codice_IPA") or "").strip().lower()
        if not ipa:
            bucket["no_codice_ipa"] += 1
            continue
        seeded = seed_by_ipa.get(ipa)
        if not seeded:
            # Not in seed at all — counted under residual unmapped (PEC-only or empty contact)
            bucket["unmapped_residual"] += 1
            continue
        src = seeded.get("domain_source") or "sito_istituzionale"
        # Distinguish IT-CONS-* (V1.1 un-filter) regardless of domain_source
        if (seeded.get("id") or "").startswith("IT-CONS-"):
            bucket[f"v1.1_consorzi_unfiltered/{src}"] += 1
        else:
            bucket[src] += 1

    # Roll up to citizen-friendly buckets
    funnel = []
    sito_first  = bucket.get("sito_istituzionale", 0)
    manual_hard = bucket.get("manual_override", 0)
    manual_llm  = bucket.get("manual_llm_enrichment", 0)
    pec_auto    = bucket.get("pec_enrichment", 0)
    email_fb    = bucket.get("email_non_pec_fallback", 0)
    cons        = sum(v for k, v in bucket.items() if k.startswith("v1.1_consorzi_unfiltered"))
    in_liq      = bucket.get("in_liquidazione", 0)
    unmapped    = bucket.get("unmapped_residual", 0) + bucket.get("no_codice_ipa", 0)

    def stage(label, n):
        return {"label": label, "count": n, "pct": round(n / total * 100, 2)}

    funnel.append(stage("validati al primo tentativo (Sito_istituzionale + MX)", sito_first))
    funnel.append(stage("recuperati via override hardcoded", manual_hard))
    funnel.append(stage("recuperati via enrichment LLM manuale (Tier-3 Claude Code)", manual_llm))
    funnel.append(stage("recuperati via enrichment automatico (Wikidata + Wikipedia)", pec_auto))
    funnel.append(stage("recuperati via fallback email non-PEC", email_fb))
    funnel.append(stage("recuperati come consorzi/unioni miscategorizzati (V1.1)", cons))
    funnel.append(stage("esclusi: enti in liquidazione", in_liq))
    funnel.append(stage("non mappati (solo PEC, nessun sito né email non-PEC)", unmapped))

    in_seed = sito_first + manual_hard + manual_llm + pec_auto + email_fb + cons
    coverage_pct = round(in_seed / total * 100, 2)

    sentence = (
        f"Su {total} enti IndicePA, {in_seed} ({coverage_pct}%) sono mappati nel "
        f"seed e classificati via DNS; {in_liq} sono esclusi perché in liquidazione; "
        f"{unmapped} restano non mappati (solo PEC, senza sito né email non-PEC)."
    )

    out = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "indicepa_total": total,
        "in_seed": in_seed,
        "coverage_pct": coverage_pct,
        "in_liquidazione": in_liq,
        "unmapped_residual": unmapped,
        "stages": funnel,
        "summary_sentence": sentence,
    }
    OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_FILE}")
    print()
    print(sentence)
    print()
    print("Funnel:")
    for s in funnel:
        print(f"  {s['count']:>6}  ({s['pct']:>5.2f}%)  {s['label']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
