#!/usr/bin/env python3
"""Generate a manual-LLM-enrichment prompt for the residual unmapped enti.

After scripts/enrich_pec_only.py runs (Wikidata + DuckDuckGo), some
IndicePA enti remain without a discoverable website. This script:

  1. Loads all IndicePA rows (CKAN paginated).
  2. Filters to candidates: rows where standard fetch_indicepa would
     drop them (no usable Sito_istituzionale, no non-PEC email).
  3. Subtracts entries already enriched with verified_mx=True in
     data/enrichment_pec_only.json.
  4. Writes data/llm_prompt_unmapped.md — a structured prompt the user
     can paste into a Claude Code session (no API key required).

The prompt asks for a strict JSON response. The user pastes the
response back into data/manual_llm_enrichment.json, which fetch_indicepa
loads as a third-tier override (priority: HARDCODED > MANUAL_LLM > PEC_AUTO).

Why manual LLM:
  - Preserves reproducibility for the deterministic part (Wikidata + DDG)
  - Keeps the fragile / unstable LLM step OUT of the automated pipeline
  - Allows human verification of LLM-discovered domains before commit

Usage:
  uv run python3 scripts/generate_llm_enrichment_prompt.py
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ENRICH_FILE = DATA / "enrichment_pec_only.json"
PROMPT_FILE = DATA / "llm_prompt_unmapped.md"
MANUAL_FILE = DATA / "manual_llm_enrichment.json"

CKAN_BASE = "https://indicepa.gov.it/ipa-dati/api/3/action"
RESOURCE_ID = "d09adf99-dc10-4349-8c53-27b1e5aa97b6"
PAGE_SIZE = 5000
USER_AGENT = "mxmap.it-llm-prompt-generator/0.1"

HOSTNAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+$")


def fetch_all_indicepa() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0
    while True:
        params = {"resource_id": RESOURCE_ID, "limit": PAGE_SIZE, "offset": offset}
        url = f"{CKAN_BASE}/datastore_search?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode("utf-8"))
        recs = d["result"]["records"]
        rows.extend(recs)
        if len(recs) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(0.4)
    return rows


def is_unmapped(row: dict[str, Any]) -> bool:
    if (row.get("Ente_in_liquidazione") or "").strip().upper() == "S":
        return False
    sito = (row.get("Sito_istituzionale") or "").strip()
    if sito:
        s = sito if "://" in sito else "//" + sito
        try:
            from urllib.parse import urlparse
            host = (urlparse(s).hostname or "").lower().lstrip("www.")
            if host and HOSTNAME_RE.match(host):
                return False
        except Exception:
            pass
    has_non_pec, has_pec = False, False
    for n in range(1, 6):
        addr = (row.get(f"Mail{n}") or "").strip()
        kind = (row.get(f"Tipo_Mail{n}") or "").strip().lower()
        if not addr or "@" not in addr:
            continue
        if kind == "pec":
            has_pec = True
        else:
            has_non_pec = True
    if has_non_pec:
        return False
    return has_pec  # PEC-only is the unmapped target


def main() -> int:
    auto: dict[str, Any] = {}
    if ENRICH_FILE.exists():
        auto = json.loads(ENRICH_FILE.read_text(encoding="utf-8"))
    enriched_ipas = {k.lower() for k, v in auto.items()
                     if isinstance(v, dict) and v.get("verified_mx")}
    print(f"Auto-enriched (verified_mx=True): {len(enriched_ipas)}")

    print("Fetching all IndicePA…")
    rows = fetch_all_indicepa()
    print(f"  {len(rows)} total")

    unmapped: list[dict[str, Any]] = []
    for r in rows:
        if not is_unmapped(r):
            continue
        codice = (r.get("Codice_IPA") or "").strip()
        if not codice or codice.lower() in enriched_ipas:
            continue
        unmapped.append(r)
    print(f"Residual unmapped (PEC-only, no auto-enrichment): {len(unmapped)}")

    # Compose prompt
    lines: list[str] = []
    lines.append("# mxmap.it — manual LLM enrichment prompt")
    lines.append("")
    lines.append(f"_Generated: {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}_")
    lines.append("")
    lines.append("## Task")
    lines.append("")
    lines.append("Each row below is an Italian Public Administration entity (PA) "
                 "that is registered in IndicePA but has NO `Sito_istituzionale` "
                 "and ONLY a PEC email (no normal email). Wikidata and DuckDuckGo "
                 "automated lookup did not find a working website.")
    lines.append("")
    lines.append("**Goal**: For each entity, return its **real institutional website "
                 "domain** (without the `www.` prefix), if discoverable from public "
                 "knowledge. The domain should be the one whose MX records are used "
                 "for the entity's office email — NOT the PEC provider's domain "
                 "(skip Aruba PEC, legalmail, postecert, asmepec, etc.).")
    lines.append("")
    lines.append("**If unsure or no domain is publicly known**: omit the entry "
                 "entirely (do NOT guess).")
    lines.append("")
    lines.append("## Output format")
    lines.append("")
    lines.append("Return ONLY a JSON object (no prose, no markdown), keyed by "
                 "`codice_ipa` (lowercase), with values:")
    lines.append("```json")
    lines.append("{")
    lines.append('  "<codice_ipa_lowercase>": {')
    lines.append('    "domain": "example.it",')
    lines.append('    "confidence": "high|medium|low",')
    lines.append('    "rationale": "1-line citation or note (e.g., \'Wikipedia article\', \'Reperito su sito provincia\')"')
    lines.append("  },")
    lines.append("  ...")
    lines.append("}")
    lines.append("```")
    lines.append("")
    lines.append("Save the JSON to `data/manual_llm_enrichment.json`. The pipeline "
                 "will pick it up on the next `fetch_indicepa` run.")
    lines.append("")
    lines.append(f"## Entities ({len(unmapped)})")
    lines.append("")
    lines.append("| codice_ipa | Categoria | Denominazione | PEC (hint) | Indirizzo |")
    lines.append("|---|---|---|---|---|")
    for r in unmapped:
        codice = (r.get("Codice_IPA") or "").strip()
        cat = (r.get("Codice_Categoria") or "").strip()
        name = (r.get("Denominazione_ente") or "").strip().replace("|", "/")
        # First PEC for context
        pec_hint = ""
        for n in range(1, 6):
            a = (r.get(f"Mail{n}") or "").strip()
            k = (r.get(f"Tipo_Mail{n}") or "").strip().lower()
            if k == "pec" and "@" in a:
                pec_hint = a
                break
        addr_parts = [
            (r.get("Indirizzo") or "").strip(),
            (r.get("CAP") or "").strip(),
            (r.get("Comune") or "").strip(),
            (r.get("Provincia") or "").strip(),
        ]
        addr = ", ".join(p for p in addr_parts if p).replace("|", "/")
        lines.append(f"| `{codice.lower()}` | {cat} | {name} | `{pec_hint}` | {addr} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## After you finish")
    lines.append("")
    lines.append("1. Save the JSON to `data/manual_llm_enrichment.json`")
    lines.append("2. Run `uv run python3 scripts/fetch_indicepa.py --include-others` "
                 "(it will load the file automatically)")
    lines.append("3. Run preprocess + chain to classify the new domains")
    lines.append("4. Commit `data/manual_llm_enrichment.json` for reproducibility")

    PROMPT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {PROMPT_FILE}  ({len(unmapped)} entities listed)")
    print(f"\nNext steps:")
    print(f"  1. Open  {PROMPT_FILE}")
    print(f"  2. Paste its contents into a Claude Code session")
    print(f"  3. Save Claude's JSON response to  {MANUAL_FILE}")
    print(f"  4. Re-run scripts/fetch_indicepa.py --include-others")
    return 0


if __name__ == "__main__":
    sys.exit(main())
