#!/usr/bin/env python3
"""Analisi specifica del cluster ACI (Automobile Club Italia + sezioni
provinciali). Quantifica:
  1. Cosa la fuzzy DL<=1 ha effettivamente recuperato in tutto il dataset
  2. Lo stato attuale degli enti ACI (categoria C13)
  3. Quanti ACI sarebbero recuperabili da una regola 6.6 di tipo
     'label concatenation' (es. aciarezzo ↔ {aci, arezzo})
"""
from __future__ import annotations
import csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str((ROOT / "src").as_posix()))
from mail_sovereignty.scrape_validator import meaningful_labels

# =============== 1. Recuperi fuzzy in pipeline ===============
print("=" * 80)
print("1. RECUPERI FUZZY ATTUALI IN data.json")
print("=" * 80)
data = json.load(open(ROOT / "data.json", encoding="utf-8"))
muns = data.get("municipalities") or data
fuzzy_hits = []
for k, m in muns.items():
    if (m.get("country") or "").upper() != "IT":
        continue
    for fld in ("reason", "recovery_legit_reason", "mx_discovery_evidence"):
        v = m.get(fld) or ""
        if "fuzzy_match" in v:
            fuzzy_hits.append((k, m.get("name", ""), m.get("domain", ""),
                               m.get("domain_used", ""), fld, v))
            break
print(f"Enti con tag fuzzy_match in qualche audit field: {len(fuzzy_hits)}")
for k, name, dom, used, fld, v in fuzzy_hits[:20]:
    print(f"  {k:<24} {name[:36]:<38} {dom} -> {used}  ({fld}={v[:60]})")

# =============== 2. Stato attuale enti ACI ===============
print()
print("=" * 80)
print("2. STATO ATTUALE ENTI ACI (categoria C13)")
print("=" * 80)
seed = json.load(open(ROOT / "data/municipalities_it.json", encoding="utf-8"))
seed_by_id = {e["id"]: e for e in seed}
aci_enti = [(k, m) for k, m in muns.items()
            if (seed_by_id.get(k, {}).get("ipa_codice_categoria") == "C13")
               or k.startswith("IT-C13-")]
print(f"Totale enti ACI: {len(aci_enti)}")
by_provider = Counter(m.get("provider") for _, m in aci_enti)
print("Provider distribution:")
for p, n in by_provider.most_common():
    print(f"  {p:<25} {n}")
print()
unknown_aci = [(k, m) for k, m in aci_enti if m.get("provider") == "unknown"]
print(f"ACI unknown da risolvere: {len(unknown_aci)}")
print()
print("--- primi 30 ACI unknown ---")
for k, m in unknown_aci[:30]:
    sd = (seed_by_id.get(k) or {}).get("domain", "(no seed dom)")
    print(f"  {k:<24} {(m.get('name') or '')[:34]:<36}  seed_dom={sd}")

# =============== 3. Simulazione rule 6.6 "label concatenation" ===============
print()
print("=" * 80)
print("3. SIMULAZIONE rule 6.6: 'label_concatenation_match'")
print("=" * 80)
print("Regola proposta: il dominio candidato è un singolo label che")
print("CONTIENE (come substring) 2+ label significativi del dominio ente,")
print("ciascuno >= 3 caratteri, e la unione delle substring copre almeno")
print("l'80% della lunghezza del label candidato.")
print()

# Carichiamo il rejection report per i candidati ACI già purgati
rej_path = ROOT / "data/reports/manual_review_rejections_full.csv"
if rej_path.exists():
    rej = list(csv.DictReader(open(rej_path, encoding="utf-8")))
    aci_rej = [r for r in rej if (r["id"] or "").startswith("IT-C13-")
                              or (r["id"] or "").startswith("IT-C14-")]   # anche ordini
    print(f"  Candidati nel report rejection per categoria C13/C14: {len(aci_rej)}")

    def label_concat_match(cand_dom: str, ente_dom: str) -> tuple[bool, str]:
        """Vero se un label del candidato contiene 2+ label dell'ente come
        substring (copertura >= 80% del label candidato)."""
        cand_labels = [l for l in meaningful_labels(cand_dom) if len(l) >= 5]
        ente_labels = [l for l in meaningful_labels(ente_dom) if len(l) >= 3]
        if not cand_labels or len(ente_labels) < 2:
            return False, ""
        for c in cand_labels:
            covers = sorted([e for e in ente_labels if e in c],
                            key=len, reverse=True)
            if len(covers) < 2:
                continue
            # check non-overlapping coverage
            covered = [False] * len(c)
            for e in covers:
                idx = c.find(e)
                if idx < 0: continue
                for i in range(idx, idx + len(e)):
                    if i < len(covered): covered[i] = True
            cov_pct = sum(covered) / len(c)
            if cov_pct >= 0.8 and len(covers) >= 2:
                return True, f"{c}={'+'.join(covers)} ({cov_pct*100:.0f}%)"
        return False, ""

    recoverable = []
    for r in aci_rej:
        ok, why = label_concat_match(r["claimed_domain"], r["seed_domain"])
        if ok:
            recoverable.append((r, why))
    print(f"  Recuperabili da rule 6.6: {len(recoverable)} / {len(aci_rej)}")
    print()
    print("--- esempi (primi 30) ---")
    for r, why in recoverable[:30]:
        print(f"  {r['id']:<24} {r['name'][:32]:<34}")
        print(f"     seed={r['seed_domain']}    claimed={r['claimed_domain']}")
        print(f"     match: {why}")
