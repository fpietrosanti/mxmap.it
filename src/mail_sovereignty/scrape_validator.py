"""Validator: is a scraped email domain legitimately associated with an
IndicePA entity?

Used by postprocess.process_unknown() and scripts/finalize_it_unknowns.py
to prevent the cross-tenant misattribution bug where scraping the website
of entity A finds an email referenced for entity B (event partner,
footer, hosted municipality, etc.) and the recovery code blindly
assigns B's MX to A.

Default verdict: REJECT. Only accept on positive signal that the
scraped domain genuinely belongs to / is operated for the entity.

Acceptance order:
  1. Exact match (scraped == ente_domain)
  2. Hand-verified manual override (codice_ipa -> domain mapping)
  3. PA-shared infrastructure whitelist (Lepida, ARIA, RUPAR, ASMEL, ...)
  4. Meaningful-label intersection (after stripping TLDs / Italian
     2-letter province codes / generic prefixes like "comune", "mail")
  5. PEC-host hard reject

Returns (is_legit: bool, reason: str). The reason is logged for audit
so that false negatives (e.g. hyphenation typos) can be promoted to
the manual override layer.
"""
from __future__ import annotations

# 2-letter Italian province codes used as 3rd-level subdomains
# (e.g. comune.roccagorga.lt.it). Source: ISTAT, all 110.
_ITALIAN_PROVINCE_CODES = {
    "ag", "al", "an", "ao", "ap", "aq", "ar", "at", "av", "ba",
    "bg", "bi", "bl", "bn", "bo", "br", "bs", "bt", "bz", "ca",
    "cb", "ce", "ch", "cl", "cn", "co", "cr", "cs", "ct", "cz",
    "en", "fc", "fe", "fg", "fi", "fm", "fr", "ge", "go", "gr",
    "im", "is", "kr", "lc", "le", "li", "lo", "lt", "lu", "mb",
    "mc", "me", "mi", "mn", "mo", "ms", "mt", "na", "no", "nu",
    "og", "or", "ot", "pa", "pc", "pd", "pe", "pg", "pi", "pn",
    "po", "pr", "pt", "pu", "pv", "pz", "ra", "rc", "re", "rg",
    "ri", "rm", "rn", "ro", "sa", "si", "so", "sp", "sr", "ss",
    "su", "sv", "ta", "te", "tn", "to", "tp", "tr", "ts", "tv",
    "ud", "va", "vb", "vc", "ve", "vi", "vr", "vs", "vt", "vv",
}

# Top-level / public-suffix labels we strip when comparing domain
# "core identity". Anything in this set is noise.
_NOISE_TLDS = {
    "it", "eu", "com", "org", "net", "gov", "edu", "co", "ac", "or",
    "info", "biz", "name",
}

# Generic structural prefixes that don't carry organizational identity.
_NOISE_PREFIXES = {
    "comune", "comuni", "comunedi", "comune-di",
    "provincia", "provincie", "regione",
    "asl", "ats", "azienda", "ausl", "aoo", "aos", "ato",
    "consorzio", "unione",
    "mail", "webmail", "posta", "cert", "pec", "smtp", "mx", "imap",
    "pop3", "in", "out", "spf", "dkim",
    "www", "wwww", "official", "sito", "site",
    "m", "m1", "m2", "m3", "ns", "ns1", "ns2",
    "protocollo", "ufficio", "uffici", "servizi", "servizio",
    "amministrazione", "transparenz", "rest", "api", "online",
}

NOISE_LABELS = _NOISE_TLDS | _ITALIAN_PROVINCE_CODES | _NOISE_PREFIXES

# PA-shared infrastructure — split into two scopes to prevent the
# "regione.vda.it accepted for Min Interno" class of bug.
#
# NATIONAL: cross-PA platforms with no jurisdictional restriction
# (research network, national consortia of comuni). Accepted for any
# Italian PA regardless of geography or category.
PA_SHARED_PLATFORMS_NATIONAL = {
    "garr.it",                                      # research network
    "sogei.it",                                     # state IT (MEF/AdE et al.)
    "asmel.it", "asmenet.it", "asmecal.it", "asmecam.it",  # comune consortia
}

# LOCAL-ONLY: platforms operated BY a regional/provincial entity FOR
# the local PAs in its jurisdiction. Accepted only when the ente looks
# like a local PA (comune / provincia / regione / asl / etc.), and
# only when the ente is in (or could plausibly belong to) the same
# region as the platform — enforced via meaningful-label intersection.
# Reject for national centrali / .gov.it ministries.
PA_SHARED_PLATFORMS_LOCAL_ONLY = {
    # Regional in-house IT
    "lepida.it", "lepida.net",                      # Emilia-Romagna
    "ariaspa.it", "aria.lombardia.it",              # Lombardia
    "ruparpiemonte.it", "csi.it",                   # Piemonte
    "insiel.it", "insiel.net",                      # FVG
    "regione.emilia-romagna.it",
    "regione.lombardia.it",
    "regione.toscana.it",
    "regione.liguria.it",
    "regione.veneto.it",
    "regione.lazio.it",
    "regione.campania.it",
    "regione.sardegna.it",
    "regione.fvg.it",
    "regione.marche.it",
    "regione.umbria.it",
    "regione.abruzzo.it",
    "regione.molise.it",
    "regione.basilicata.it",
    "regione.calabria.it",
    "regione.sicilia.it",
    "regione.puglia.it",
    "regione.vda.it",
    # South Tyrol Gemeindenverband + schools
    "gvcc.net",
    "schule.suedtirol.it", "scuola.alto-adige.it",
    # Trentino IT Exchange
    "tix.it",
}

# Back-compat alias
PA_SHARED_PLATFORMS = PA_SHARED_PLATFORMS_NATIONAL | PA_SHARED_PLATFORMS_LOCAL_ONLY

# Markers that indicate "this domain belongs to a local Italian PA"
# (comune / provincia / regione / health authority / consortium / etc.)
LOCAL_PA_DOMAIN_MARKERS = {
    "comune", "comuni", "comunedi", "comune-di",
    "citta-metropolitana", "cittametropolitana",
    "provincia", "provincie",
    "regione",
    "asl", "ausl", "asp", "ats", "ato", "aoo",
    "consorzio", "unione",
    "gemeindenverband", "gvcc",
}

# PEC providers — by mxmap policy, never the basis for classification.
PEC_PROVIDERS = {
    "pec.it", "legalmail.it", "postecert.it", "arubapec.it", "aruba.it",
    "asmepec.it", "notariato.it", "pec.aruba.it", "kpec.it",
    "namirial.it", "namirialtsp.it", "sicurezzapostale.it",
    "fnofi.it", "conafpec.it", "ingpec.eu", "epap.sicurezzapostale.it",
    "pa.postecert.it",
}


def _domain_endswith(host: str, base: str) -> bool:
    """True if host == base or host has base as a strict suffix component."""
    return host == base or host.endswith("." + base)


def is_local_pa_domain(d: str) -> bool:
    """True iff `d` looks like a local Italian PA (comune / provincia /
    regione / ASL / etc.). FALSE for national centrali / .gov.it
    ministries / reserved-namespace national bodies.

    This gates whether a regional PA-shared platform (e.g. lepida.it,
    regione.vda.it) may be accepted as legitimate infrastructure for
    the parent ente — preventing the bug where AOO records of a
    ministry exposed a regional sub-unit's email and the regional
    platform ended up whitelisted for the central ministry.
    """
    if not d:
        return False
    d = d.lower().strip().rstrip(".")
    # gov.it is reserved by AGID for national PA / ministries — never local.
    if d == "gov.it" or d.endswith(".gov.it"):
        return False
    parts = d.split(".")
    if any(p in LOCAL_PA_DOMAIN_MARKERS for p in parts):
        return True
    if any(p in _ITALIAN_PROVINCE_CODES for p in parts):
        return True
    return False


def meaningful_labels(domain: str) -> set[str]:
    """Extract the identity-bearing labels of a domain.

    interno.gov.it           -> {'interno'}
    comune.roccagorga.lt.it  -> {'roccagorga'}
    mail.comune.padova.it    -> {'padova'}
    aslroma1.it              -> {'aslroma1'}
    interno.it               -> {'interno'}

    Length filter (>2) prevents 'tn' / 'mi' shorthand from being identity
    when they're really region/province codes that slipped through.
    """
    if not domain:
        return set()
    parts = domain.lower().split(".")
    return {p for p in parts if p not in NOISE_LABELS and len(p) > 2}


def is_legit_email_domain(
    scraped: str,
    ente_domain: str,
    *,
    codice_ipa: str | None = None,
    manual_overrides: dict | None = None,
) -> tuple[bool, str]:
    """Return (is_legit, reason).

    Conservative: returns False unless one of the positive signals fires.
    """
    if not scraped or not ente_domain:
        return False, "empty_input"
    s = scraped.lower().strip().rstrip(".")
    e = ente_domain.lower().strip().rstrip(".")

    # 1. Exact match
    if s == e:
        return True, "exact_match"

    # 2. PEC reject (hard)
    for pec in PEC_PROVIDERS:
        if _domain_endswith(s, pec):
            return False, f"pec_provider:{pec}"

    # 3. Hand-verified override match
    if codice_ipa and manual_overrides:
        ipa_l = codice_ipa.strip().lower()
        if manual_overrides.get(ipa_l) == s:
            return True, "manual_override"

    # 4a. PA-shared infrastructure (NATIONAL scope — accepted for any PA)
    for plat in PA_SHARED_PLATFORMS_NATIONAL:
        if _domain_endswith(s, plat):
            return True, f"pa_shared_national:{plat}"

    # 4b. PA-shared infrastructure (LOCAL-ONLY scope — only accepted
    #     when the ente is itself a local PA; reject for national
    #     centrali / ministries / .gov.it bodies). Falls through to
    #     subdomain / shared-label rules so the platform domain is
    #     still subject to identity matching when it doesn't apply.
    matched_local_plat = None
    for plat in PA_SHARED_PLATFORMS_LOCAL_ONLY:
        if _domain_endswith(s, plat):
            matched_local_plat = plat
            break
    if matched_local_plat:
        if is_local_pa_domain(e):
            # Local PA — the platform is legitimately offered to it.
            # Region-pair check: also require the platform's
            # meaningful-label set to intersect the ente's, so we
            # don't accept regione.lombardia.it for a Sicily comune.
            plat_labels = meaningful_labels(matched_local_plat)
            ente_labels_q = meaningful_labels(e)
            if not plat_labels or (plat_labels & ente_labels_q):
                return True, f"pa_shared_local:{matched_local_plat}"
            # else: fall through — the platform region doesn't match
            # the ente region, so try the remaining rules (none of
            # which will fire for cross-region cases) → unrelated.
        # else (national ente): fall through to remaining rules; if
        # none accept, this becomes "unrelated" and the regional
        # platform is rejected — which is the desired Min-Interno fix.

    # 5. Subdomain relationship (one is descendant of the other)
    if _domain_endswith(s, e) or _domain_endswith(e, s):
        return True, "subdomain_or_parent"

    # 6. Meaningful-label intersection
    s_labels = meaningful_labels(s)
    e_labels = meaningful_labels(e)
    common = s_labels & e_labels
    if common:
        return True, "shared_label:" + ",".join(sorted(common))

    if matched_local_plat:
        return False, f"pa_shared_platform_out_of_scope:{matched_local_plat}"
    return False, "unrelated"


# Convenience for testing
__all__ = [
    "is_legit_email_domain", "meaningful_labels", "is_local_pa_domain",
    "NOISE_LABELS", "PA_SHARED_PLATFORMS",
    "PA_SHARED_PLATFORMS_NATIONAL", "PA_SHARED_PLATFORMS_LOCAL_ONLY",
    "PEC_PROVIDERS",
]
