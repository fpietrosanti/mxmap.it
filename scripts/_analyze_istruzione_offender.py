#!/usr/bin/env python3
"""Diagnostic: explain the istruzione.it cross-tenant offender pattern."""
import csv, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rej = list(csv.DictReader(open(ROOT / "data/reports/manual_review_rejections_full.csv")))
istr = [r for r in rej if r["claimed_domain"] == "istruzione.it"]
seed = {e["id"]: e for e in json.load(open(ROOT / "data/municipalities_it.json"))}

print(f"=== istruzione.it cross-tenant offender: {len(istr)} entries ===\n")

print("ipa_codice_categoria of the victims (what kind of ente got the wrong MX):")
cats = Counter(seed.get(r["id"], {}).get("ipa_codice_categoria", "?") for r in istr)
for c, n in cats.most_common():
    print(f"  {c!r:<8} {n}")
print()

print("ipa_codice_ipa prefix breakdown (first 4 chars of codice_ipa):")
by_ipa = Counter((r["codice_ipa"] or "")[:4] for r in istr)
for c, n in by_ipa.most_common(12):
    print(f"  {c!r:<10} {n}")
print()

print("Sample entries (id, ente, seed_domain):")
for r in istr[:20]:
    print(f"  {r['id']:<22} {r['name'][:42]:<44} {r['seed_domain']}")
print()

print("old_reason buckets (what was the wrong classification before cleanup):")
old = Counter((r["old_reason"] or "")[:100] for r in istr)
for c, n in old.most_common(5):
    print(f"  {n:>4}x  {c}")
print()

print("old_provider distribution:")
op = Counter(r["old_provider"] for r in istr)
for c, n in op.most_common():
    print(f"  {c!r:<14} {n}")
print()

# Most common seed_domain TLDs/patterns
print("Seed domain patterns of victims:")
patterns = Counter()
for r in istr:
    sd = r["seed_domain"] or ""
    if ".edu.it" in sd:
        patterns["*.edu.it (school directly)"] += 1
    elif ".gov.it" in sd:
        patterns["*.gov.it (national PA)"] += 1
    elif sd.startswith("comune."):
        patterns["comune.* (town hall)"] += 1
    elif "scuol" in sd or "istit" in sd or "liceo" in sd:
        patterns["other school-related"] += 1
    else:
        patterns["other"] += 1
for c, n in patterns.most_common():
    print(f"  {c:<32} {n}")
