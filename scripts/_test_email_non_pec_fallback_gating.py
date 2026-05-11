#!/usr/bin/env python3
"""Cosa succederebbe se applicassimo is_legit_email_domain ANCHE al path
seed-time `email_non_pec_fallback` di fetch_indicepa.transform()?

Per ogni ente nel seed con domain_source == "email_non_pec_fallback":
  - il candidato è il dominio non-PEC del record IndicePA
  - non c'è un seed.domain alternativo (è perché abbiamo usato il fallback)
  - confrontiamo il candidato contro l'IDENTITÀ DEL NOME dell'ente,
    tokenizzando il nome (rimozione di noise: "comune", "di", articoli,
    apostrofi, ecc.) e cercando intersezione con i meaningful_labels
    del dominio.

Stampa la distribuzione di accept/reject, e i 30 più sospetti.
"""
from __future__ import annotations
import json, re, sys, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str((ROOT / "src").as_posix()))
from mail_sovereignty.scrape_validator import (
    meaningful_labels, NOISE_LABELS, PEC_PROVIDERS, _ITALIAN_PROVINCE_CODES,
)

# Parole/stop-tokens da rimuovere quando tokenizziamo il NOME dell'ente.
NAME_NOISE = {
    # articoli/preposizioni italiane
    "di","del","della","dello","dei","delle","degli","da","dal","dalla",
    "in","con","su","per","tra","fra","ed","e","a","al","alla","i","la",
    "il","lo","gli","le","l","d","-","de",
    # marcatori istituzionali (NON portatori di identità)
    "comune","comuni","provincia","provincie","regione","municipio",
    "citta","metropolitana",
    "ministero","ministerio","ministeri",
    "istituto","istituzione","istituzioni","istituti",
    "scuola","scuole","liceo","licei","circolo","didattico",
    "ordine","ordini","collegio","federazione","federazioni",
    "azienda","aziende","agenzia","agenzie","ente","enti",
    "consorzio","consorzi","unione","unioni",
    "consiglio","commissione","autorita","autorità","direzione",
    "centro","centri","ufficio","uffici","servizio","servizi",
    "stato","statale","statali","nazionale","nazionali",
    "italiana","italiano","italiani","italiane",
    "iss","ic","cd","iiss","iis","cpia","aoo",
    "polo","istituzionale","amministrazione",
    "professione","professionisti","professione","professionale",
    "comprensivo","superiore","secondaria","primaria",
    "general","generale","direzione",
}


def slug(s: str) -> str:
    """lowercase, no diacritics, alfa only, no spaces."""
    n = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", n.lower())


def name_tokens(name: str) -> set[str]:
    """Token significativi del nome ente."""
    if not name:
        return set()
    n = unicodedata.normalize("NFKD", name).encode("ascii","ignore").decode().lower()
    parts = re.split(r"[\s\.,;:'\"\-\(\)\/\d]+", n)
    return {p for p in parts
            if p and p not in NAME_NOISE
            and p not in NOISE_LABELS
            and p not in _ITALIAN_PROVINCE_CODES
            and len(p) > 3}


def simulate_gate(name: str, candidate_dom: str) -> tuple[bool, str]:
    """True se il candidato è 'legittimo' rispetto al nome."""
    if not candidate_dom:
        return False, "empty_input"
    s = candidate_dom.lower().strip().rstrip(".")
    for pec in PEC_PROVIDERS:
        if s == pec or s.endswith("." + pec):
            return False, f"pec_provider:{pec}"
    nt = name_tokens(name)
    if not nt:
        return False, "name_has_no_meaningful_tokens"
    dl = meaningful_labels(s)
    if not dl:
        return False, "domain_has_no_meaningful_labels"
    # Match a) intersezione diretta dei token significativi
    if nt & dl:
        return True, f"shared_token:{','.join(sorted(nt & dl))}"
    # Match b) un label del dominio contiene un token nome (es. comuneacquario ↔ acquario)
    name_slug_tokens = {slug(t) for t in nt if len(t) > 4}
    for lbl in dl:
        for nts in name_slug_tokens:
            if nts in lbl or lbl in nts:
                return True, f"substring_token:{nts}~{lbl}"
    return False, "unrelated"


def main() -> int:
    seed = json.loads((ROOT / "data/municipalities_it.json").read_text(encoding="utf-8"))
    rows = [e for e in seed
            if (e.get("domain_source") or "") == "email_non_pec_fallback"]
    print(f"Total enti con domain_source=email_non_pec_fallback: {len(rows)}")
    if not rows:
        return 0

    by_cat = Counter(e.get("ipa_codice_categoria") or "?" for e in rows)
    print("\nDistribuzione per categoria IndicePA:")
    for c, n in by_cat.most_common():
        print(f"  {c:<6} {n}")

    n_accept = 0
    n_reject = 0
    reject_reasons: Counter[str] = Counter()
    accept_reasons: Counter[str] = Counter()
    rejected_samples: list[tuple] = []
    accepted_samples: list[tuple] = []
    for e in rows:
        ok, reason = simulate_gate(e.get("name") or "", e.get("domain") or "")
        rkey = reason.split(":", 1)[0]
        if ok:
            n_accept += 1
            accept_reasons[rkey] += 1
            if len(accepted_samples) < 20:
                accepted_samples.append((e.get("ipa_codice_ipa"), e.get("name"), e.get("domain"), reason))
        else:
            n_reject += 1
            reject_reasons[rkey] += 1
            if len(rejected_samples) < 30:
                rejected_samples.append((e.get("ipa_codice_ipa"), e.get("name"), e.get("domain"), reason))

    print()
    print(f"=== Risultato simulazione gating ===")
    print(f"  ACCEPT (manterrebbe il dominio): {n_accept}  ({100*n_accept/len(rows):.1f}%)")
    print(f"  REJECT (diventerebbe unknown):   {n_reject}  ({100*n_reject/len(rows):.1f}%)")
    print()
    print("Accept reasons (top 5):")
    for r, n in accept_reasons.most_common(5):
        print(f"  {r:<35} {n}")
    print()
    print("Reject reasons (top 5):")
    for r, n in reject_reasons.most_common(5):
        print(f"  {r:<35} {n}")
    print()
    print(f"--- 30 ESEMPI DI REJECT (candidati a diventare unknown) ---")
    for ipa, name, dom, reason in rejected_samples:
        print(f"  {(ipa or '')[:14]:<15} {(name or '')[:55]:<55}  dom={dom!r}  why={reason}")
    print()
    print(f"--- 20 ESEMPI DI ACCEPT (validati dalla simulazione) ---")
    for ipa, name, dom, reason in accepted_samples:
        print(f"  {(ipa or '')[:14]:<15} {(name or '')[:55]:<55}  dom={dom!r}  why={reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
