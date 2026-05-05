#!/usr/bin/env python3
"""Enrichment pipeline for PEC-only IndicePA enti.

~620 entities in IndicePA have NO Sito_istituzionale and ONLY PEC emails
(no non-PEC). The standard fetch_indicepa drops them at seed-time because
PEC providers (Aruba PEC, legalmail, postecert, asmepec) are dominated by
~5 entities and don't represent the ente's real email infrastructure.

This script tries to discover the real website / non-PEC email domain via:

  Tier 1: Wikidata SPARQL — query P6832 (IndicePA code) -> P856 (website)
  Tier 2: DuckDuckGo HTML search (no API key required) for "<ente_name>"
          + heuristic filter (.it/.gov.it/.eu, valid hostname, has MX)
  Tier 3: TODO — Claude API LLM prompt (skipped if ANTHROPIC_API_KEY absent)

Output:  data/enrichment_pec_only.json
  {
    "codice_ipa": {
      "domain": "comune-x.it",
      "source": "wikidata|duckduckgo|llm",
      "name": "Comune di X",
      "verified_mx": true
    },
    ...
  }

`fetch_indicepa.py` loads this file via load_pec_enrichment() and applies
each entry as a second-priority override (after IT_MANUAL_DOMAIN_OVERRIDES).
The seed marks domain_source='pec_enrichment_<source>' for audit.

Usage:
  uv run python3 scripts/enrich_pec_only.py [--limit N] [--rebuild]
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_FILE = DATA / "enrichment_pec_only.json"

CKAN_BASE = "https://indicepa.gov.it/ipa-dati/api/3/action"
RESOURCE_ID = "d09adf99-dc10-4349-8c53-27b1e5aa97b6"
PAGE_SIZE = 5000
USER_AGENT = "mxmap.it-pec-enrichment/0.1 (+https://github.com/fpietrosanti/mxmap.it)"

WD_SPARQL = "https://query.wikidata.org/sparql"

HOSTNAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+$")

# Skip these "fake" PEC-derived results — popular Italian PEC providers.
SKIP_PEC_PROVIDER_HOSTS = {
    "pec.it", "legalmail.it", "postecert.it", "arubapec.it", "aruba.it",
    "asmepec.it", "conafpec.it", "notariato.it", "fnofi.it",
    "sicurezzapostale.it", "pec.aruba.it", "kpec.it", "namirial.it",
}

# Acceptable Italian/EU TLDs for results
GOOD_TLD_RE = re.compile(r"\.(it|gov\.it|edu\.it|eu|com|org|net)$", re.IGNORECASE)


def http_get(url: str, *, headers: dict[str, str] | None = None,
             retries: int = 3, sleep_s: float = 2.0,
             data: bytes | None = None) -> str:
    """GET (or POST when data set) with simple retry on transient failures."""
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, data=data,
                                         headers={"User-Agent": USER_AGENT, **(headers or {})})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(sleep_s); sleep_s *= 1.7
    raise RuntimeError(f"GET {url} failed after {retries} attempts: {last_err}")


# ---------- IndicePA loader ----------

def fetch_pec_only_candidates() -> list[dict[str, Any]]:
    """Return all IndicePA rows that have NO Sito_istituzionale (or syntactically
    invalid) AND only PEC emails (no non-PEC Mail{1..5} entry)."""
    print("Fetching all IndicePA rows (paginated)…")
    rows: list[dict[str, Any]] = []
    offset = 0
    while True:
        params = {"resource_id": RESOURCE_ID, "limit": PAGE_SIZE, "offset": offset}
        url = f"{CKAN_BASE}/datastore_search?{urllib.parse.urlencode(params)}"
        body = http_get(url)
        data = json.loads(body)
        recs = data["result"]["records"]
        rows.extend(recs)
        if len(recs) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(0.4)
    print(f"  total IndicePA rows: {len(rows)}")

    candidates: list[dict[str, Any]] = []
    for r in rows:
        if (r.get("Ente_in_liquidazione") or "").strip().upper() == "S":
            continue
        sito = (r.get("Sito_istituzionale") or "").strip()
        # accept candidate if no sito OR sito is syntactically broken
        if sito:
            s = sito if "://" in sito else "//" + sito
            try:
                from urllib.parse import urlparse
                host = (urlparse(s).hostname or "").lower().lstrip("www.")
            except Exception:
                host = ""
            if host and HOSTNAME_RE.match(host):
                continue  # has a usable website — skip
        # Now check that NO non-PEC email exists
        has_non_pec = False
        has_pec = False
        for n in range(1, 6):
            addr = (r.get(f"Mail{n}") or "").strip()
            kind = (r.get(f"Tipo_Mail{n}") or "").strip().lower()
            if not addr or "@" not in addr:
                continue
            if kind == "pec":
                has_pec = True
            else:
                has_non_pec = True
        if has_non_pec or not has_pec:
            continue
        candidates.append(r)
    print(f"  PEC-only candidates: {len(candidates)}")
    return candidates


# ---------- Tier 1: Wikidata ----------

def wikidata_lookup_by_ipa(codice_ipa: str) -> str | None:
    """Query Wikidata for an entity with P6832=codice_ipa, return its P856
    (official website) host if present."""
    q = (
        "SELECT ?ente ?website WHERE { "
        f'?ente wdt:P6832 "{codice_ipa}". '
        "OPTIONAL { ?ente wdt:P856 ?website. } "
        "} LIMIT 5"
    )
    url = f"{WD_SPARQL}?query={urllib.parse.quote(q)}&format=json"
    try:
        body = http_get(url, headers={"Accept": "application/sparql-results+json"})
    except RuntimeError:
        return None
    try:
        d = json.loads(body)
    except Exception:
        return None
    for b in d.get("results", {}).get("bindings", []):
        site = b.get("website", {}).get("value")
        if site:
            return _extract_host(site)
    return None


def _extract_host(url: str) -> str | None:
    s = url.strip()
    if not s:
        return None
    if "://" not in s:
        s = "//" + s
    try:
        from urllib.parse import urlparse
        host = (urlparse(s).hostname or "").lower().lstrip(".")
    except Exception:
        return None
    if host.startswith("www."):
        host = host[4:]
    if not host or not HOSTNAME_RE.match(host):
        return None
    return host


# ---------- Tier 2: DuckDuckGo HTML ----------

DDG_RESULT_RE = re.compile(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', re.IGNORECASE)


def duckduckgo_lookup(query: str) -> str | None:
    """Scrape DuckDuckGo HTML SERP and return the first plausible Italian PA
    domain (prefer .gov.it / .it that isn't a known PEC provider)."""
    url = "https://html.duckduckgo.com/html/"
    body = (f"q={urllib.parse.quote(query)}").encode("ascii")
    try:
        resp = http_get(url, headers={"Content-Type": "application/x-www-form-urlencoded"},
                        data=body)
    except RuntimeError:
        return None
    candidates: list[str] = []
    for m in DDG_RESULT_RE.finditer(resp):
        target = unescape(m.group(1))
        # DDG wraps results: //duckduckgo.com/l/?uddg=<url>
        if "uddg=" in target:
            target = urllib.parse.unquote(target.split("uddg=", 1)[1].split("&", 1)[0])
        host = _extract_host(target)
        if not host:
            continue
        if host in SKIP_PEC_PROVIDER_HOSTS:
            continue
        if any(host.endswith(s) or host == s.lstrip(".") for s in
               (".facebook.com", ".instagram.com", ".linkedin.com", ".wikipedia.org",
                ".indicepa.gov.it", "indicepa.gov.it")):
            continue
        if not GOOD_TLD_RE.search(host):
            continue
        candidates.append(host)
        if len(candidates) >= 3:
            break
    return candidates[0] if candidates else None


# ---------- Verification: MX lookup ----------

def has_mx_records(host: str) -> bool:
    """Light MX check via system resolver (fallback: skip on import failure)."""
    try:
        import dns.resolver
    except ImportError:
        return True  # don't reject if dnspython missing
    try:
        answers = dns.resolver.resolve(host, "MX", lifetime=5)
        return len(list(answers)) > 0
    except Exception:
        return False


# ---------- Main loop ----------

def enrich_one(row: dict[str, Any]) -> dict[str, Any] | None:
    codice_ipa = (row.get("Codice_IPA") or "").strip()
    name = (row.get("Denominazione_ente") or "").strip()
    if not codice_ipa or not name:
        return None

    # Tier 1
    host = wikidata_lookup_by_ipa(codice_ipa)
    src = "wikidata" if host else None

    # Tier 2
    if not host:
        host = duckduckgo_lookup(f'"{name}" sito ufficiale')
        src = "duckduckgo" if host else None
        if host:
            time.sleep(random.uniform(2.0, 4.0))  # be polite to DDG

    if not host:
        return None

    return {
        "codice_ipa": codice_ipa,
        "name": name,
        "domain": host,
        "source": src,
        "verified_mx": has_mx_records(host),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None,
                    help="enrich only first N candidates (for testing)")
    ap.add_argument("--rebuild", action="store_true",
                    help="discard existing enrichment file and start over")
    ap.add_argument("--skip-existing", action="store_true",
                    help="(default) only enrich entries not yet in the output file")
    args = ap.parse_args()

    DATA.mkdir(parents=True, exist_ok=True)
    existing: dict[str, dict[str, Any]] = {}
    if OUT_FILE.exists() and not args.rebuild:
        existing = json.loads(OUT_FILE.read_text(encoding="utf-8"))
        print(f"Loaded {len(existing)} existing enrichments from {OUT_FILE}")

    candidates = fetch_pec_only_candidates()
    if args.limit:
        candidates = candidates[: args.limit]

    enriched = dict(existing)
    n_wd, n_ddg, n_fail = 0, 0, 0
    for i, row in enumerate(candidates, 1):
        codice_ipa = (row.get("Codice_IPA") or "").strip()
        if not codice_ipa:
            continue
        if codice_ipa in enriched and not args.rebuild:
            continue
        try:
            res = enrich_one(row)
        except Exception as e:
            print(f"  [{i}/{len(candidates)}] {codice_ipa}: ERROR {e!r}")
            res = None
        if res:
            enriched[codice_ipa] = res
            if res["source"] == "wikidata":  n_wd += 1
            else:                            n_ddg += 1
            print(f"  [{i}/{len(candidates)}] {codice_ipa}  {res['name'][:40]:<40} "
                  f"-> {res['domain']:<35}  [{res['source']}]"
                  f"{' MX✓' if res['verified_mx'] else ' MX✗'}")
        else:
            n_fail += 1
            if i % 25 == 0:
                print(f"  [{i}/{len(candidates)}] (still searching… {n_fail} failures so far)")
        # Periodic checkpoint every 50 candidates
        if i % 50 == 0:
            OUT_FILE.write_text(json.dumps(enriched, ensure_ascii=False, indent=2),
                                encoding="utf-8")
        time.sleep(random.uniform(0.5, 1.5))

    OUT_FILE.write_text(json.dumps(enriched, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print()
    print(f"Wrote {OUT_FILE}")
    print(f"Total enrichments: {len(enriched)}  (Wikidata: {n_wd}  DDG: {n_ddg}  failed: {n_fail})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
