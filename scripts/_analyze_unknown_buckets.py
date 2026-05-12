#!/usr/bin/env python3
"""Bucketizzazione dei 627 unknown rimasti per identificare cluster
ricorrenti tipo-ACI/tipo-MIM dove un override mirato sblocca molti enti.

Per ogni cluster identifico:
  - Pattern del dominio seed (es. ordine{città}.conaf.it)
  - Pattern del dominio fallback più comune
  - Pattern del nome (es. inizia con "Ordine Dottori Agronomi")
  - Cardinalità
  - Sample di 5 enti

Output:
  - stdout: top buckets in tabella
  - data/reports/unknown_buckets.csv: ogni unknown con campi diagnostici
"""
from __future__ import annotations
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str((ROOT / "src").as_posix()))

DATA = ROOT / "data"
data = json.load(open(ROOT / "data.json", encoding="utf-8"))
muns = data.get("municipalities") or data
seed = json.load(open(DATA / "municipalities_it.json", encoding="utf-8"))
seed_by_id = {e["id"]: e for e in seed}

unknowns = []
for k, m in muns.items():
    if (m.get("country") or "").upper() != "IT":
        continue
    if m.get("provider") != "unknown":
        continue
    se = seed_by_id.get(k) or {}
    unknowns.append({
        "id": k,
        "codice_ipa": se.get("ipa_codice_ipa", ""),
        "categoria": se.get("ipa_codice_categoria", ""),
        "name": se.get("name", "") or m.get("name", ""),
        "seed_domain": (se.get("domain") or "").lower(),
        "fallbacks": se.get("domain_fallbacks") or [],
        "domain_source": se.get("domain_source") or "",
    })

print(f"Totale enti UNKNOWN: {len(unknowns)}\n")
print("=== Distribuzione per categoria IndicePA ===")
for c, n in Counter(u["categoria"] for u in unknowns).most_common(20):
    print(f"  {c:<6} {n}")
print()


# --- BUCKETIZER: estrae il SUFFISSO del dominio dopo il primo label ---
# Es. "ordineprato.conaf.it" -> ".conaf.it"
# Es. "comune.foo.it" -> ".foo.it"
def suffix_pattern(d: str) -> str:
    if not d or "." not in d:
        return ""
    parts = d.split(".")
    if len(parts) < 2:
        return ""
    # ritorna gli ultimi 2-3 segmenti come pattern
    if len(parts) >= 3 and parts[-2] in {"gov", "ac", "co", "or", "edu"}:
        return "." + ".".join(parts[-3:])
    return "." + ".".join(parts[-2:])


print("=== TOP 20 SEED-DOMAIN SUFFIX PATTERNS (≥3 enti) ===")
suffix_counts = Counter(suffix_pattern(u["seed_domain"]) for u in unknowns)
for s, n in suffix_counts.most_common(30):
    if n < 3:
        break
    print(f"  {s:<28} {n}")
print()


# --- BUCKETIZER: parola-chiave del NOME ente ---
NAME_NOISE = {
    "di","del","della","dello","dei","delle","degli","da","in","con","per",
    "e","la","il","lo","gli","le","l","d","a","al",
    "comune","provincia","regione","ordine","collegio","federazione",
    "azienda","agenzia","ente","consorzio","unione","commissione",
    "istituto","istituzione","scuola","liceo","albo","ministero",
    "professione","provinciale","interprovinciale","statale","nazionale",
    "dottori","laureati","sanitari","della","dei","del",
}
def name_lead_token(name: str) -> str:
    """Prima parola significativa del nome — utile a clusterizzare."""
    import unicodedata
    n = unicodedata.normalize("NFKD", name).encode("ascii","ignore").decode().lower()
    for w in re.split(r"[\s\.,;:'\"\-\(\)\/]+", n):
        if w and w not in NAME_NOISE and len(w) >= 5:
            return w
    return "?"

print("=== TOP 20 NAME-LEAD-TOKEN ===")
for t, n in Counter(name_lead_token(u["name"]) for u in unknowns).most_common(20):
    if n < 3: break
    print(f"  {t:<22} {n}")
print()


# --- CLUSTER ESPLICITI: combinazione di suffisso + parole chiave ---
def cluster_key(u):
    sd = u["seed_domain"]
    name = u["name"].lower()
    # CONAF agronomi
    if ".conaf.it" in sd or ".conaf.eu" in sd:
        return "C14:ordine_agronomi_CONAF"
    if ".cnpi.eu" in sd:
        return "C14:ordine_periti_industriali_CNPI"
    if ".archiworld.it" in sd:
        return "C14:ordine_architetti_archiworld"
    if ".odec.com" in sd or ".commercialisti.it" in sd:
        return "C14:ordine_commercialisti"
    if "peritiagrari" in sd:
        return "C14:periti_agrari"
    if "agrotecnici" in sd:
        return "C14:agrotecnici"
    if "ostetric" in sd:
        return "C14:ostetriche"
    if "geometri" in sd:
        return "C14:geometri"
    if "consulentidellavoro" in sd:
        return "C14:consulenti_lavoro"
    if "tsrm" in sd or "tsrmpstrp" in sd:
        return "C14:tecnici_radiologia_tsrm"
    if "consiglionotarile" in sd or "notarile" in sd:
        return "C14:consiglio_notarile"
    if "ordinearchitetti" in sd or "ordine.architetti" in sd:
        return "C14:ordine_architetti_altro"
    if "ordineavvocati" in sd or "avvocati" in sd:
        return "C14:ordine_avvocati"
    if "ordineingegneri" in sd or "ordine.ingegneri" in sd:
        return "C14:ordine_ingegneri"
    if "ordinedeimedici" in sd or "ordinedeimedici" in sd or "ordinemedici" in sd:
        return "C14:ordine_medici"
    if "ordineveterinari" in sd or "ordinevet" in sd:
        return "C14:ordine_veterinari"
    if "ordinechimici" in sd:
        return "C14:ordine_chimici"
    if "ordinefarmacist" in sd:
        return "C14:ordine_farmacisti"
    # Comuni (L6)
    if sd.startswith("comune.") or sd.startswith("comuni."):
        return "L6:comune.X.Y"
    # Università / scuole AFAM / istituti
    if u["categoria"] == "L1":
        return "L1:scuole_provinciali_BZ_TN"
    if u["categoria"] == "L33":
        return "L33:scuole_statali"
    if u["categoria"] in ("L12",):
        return "L12:unioni_comuni"
    if u["categoria"] == "L34":
        return "L34:comunita_montane"
    if u["categoria"] == "L37":
        return "L37:aziende_speciali_comunali"
    if u["categoria"] == "L36":
        return "L36:enti_parco_consorzi"
    if u["categoria"] == "L38":
        return "L38:aziende_sanitarie_speciali"
    if u["categoria"] == "L47":
        return "L47:commissari_straordinari"
    if u["categoria"] == "C3":
        return "C3:agenzie_nazionali"
    if u["categoria"] == "C1":
        return "C1:ministeri"
    return f"{u['categoria']}:altro"


cluster = defaultdict(list)
for u in unknowns:
    cluster[cluster_key(u)].append(u)

print("=" * 80)
print("CLUSTER PIÙ NUMEROSI (≥5 enti)")
print("=" * 80)
for ck, items in sorted(cluster.items(), key=lambda x: -len(x[1])):
    if len(items) < 5:
        continue
    print(f"\n--- {ck} ({len(items)} enti) ---")
    for u in items[:5]:
        fbs = ",".join(u["fallbacks"][:2]) if u["fallbacks"] else "(no fallback)"
        print(f"   {u['codice_ipa']:<14}{u['name'][:46]:<48}  seed={u['seed_domain'][:30]:<32}  fb={fbs[:40]}")
    if len(items) > 5:
        print(f"   ... +{len(items)-5} altri")

# Write full CSV
out = DATA / "reports" / "unknown_buckets.csv"
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id","codice_ipa","categoria","name","seed_domain","fallbacks","cluster"])
    for u in unknowns:
        w.writerow([u["id"], u["codice_ipa"], u["categoria"], u["name"],
                    u["seed_domain"], ";".join(u["fallbacks"]), cluster_key(u)])
print(f"\nCSV completo: {out.relative_to(ROOT)} ({len(unknowns)} righe)")
