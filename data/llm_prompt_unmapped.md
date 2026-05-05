# mxmap.it — manual LLM enrichment prompt

_Generated: 2026-05-05 13:37 UTC_

## Task

Each row below is an Italian Public Administration entity (PA) that is registered in IndicePA but has NO `Sito_istituzionale` and ONLY a PEC email (no normal email). Wikidata and DuckDuckGo automated lookup did not find a working website.

**Goal**: For each entity, return its **real institutional website domain** (without the `www.` prefix), if discoverable from public knowledge. The domain should be the one whose MX records are used for the entity's office email — NOT the PEC provider's domain (skip Aruba PEC, legalmail, postecert, asmepec, etc.).

**If unsure or no domain is publicly known**: omit the entry entirely (do NOT guess).

## Output format

Return ONLY a JSON object (no prose, no markdown), keyed by `codice_ipa` (lowercase), with values:
```json
{
  "<codice_ipa_lowercase>": {
    "domain": "example.it",
    "confidence": "high|medium|low",
    "rationale": "1-line citation or note (e.g., 'Wikipedia article', 'Reperito su sito provincia')"
  },
  ...
}
```

Save the JSON to `data/manual_llm_enrichment.json`. The pipeline will pick it up on the next `fetch_indicepa` run.

## Entities (603)

| codice_ipa | Categoria | Denominazione | PEC (hint) | Indirizzo |
|---|---|---|---|---|
| `00yw4x9b` | SA | MONTALTO MULTISERVIZI SRL | `montaltomultiservizi@pec.it` | VIA DEL PALOMBARO 11, 01014 |
| `0ithr9pn` | L47 | Commissario  Delegato OCDPC 1156-2025 zona Emilia Romagna | `OCDPC1156@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `0kqqxtdd` | L37 | Organizzazione Progetti e Servizi SpA | `opschieti@pec.aruba.it` | Via Padre Ugolino Frasca, 66100 |
| `0mq3upqs` | L47 | SOGGETTO RESPONSABILE OCDPC 1178-26 OCDPC 1120-24 OCDPC 1087-24 OCDPC 1070-24 ZONA EMILIA ROMAGNA | `OCDPC1070@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `0ope3620` | L10 | AZIENDA DI PROMOZIONE TURISTICA PROVINCIA DI LECCE IN LIQUIDAZIONE | `aptlecceinliquidazione@pec.it` | Piazza aldo moro 33/a, 70100 |
| `0uqcyvcu` | SA | F.A. S.R.L. | `AEROPORTO.FO@LEGALMAIL.IT` | Via CARLO SEGANTI N. 103, 47121 |
| `17uw94zl` | L6 | Comune di Castegnero Nanto | `comune.castegneronanto.vi@pecveneto.it` | Via Mercato 43, 36024 |
| `1ha36spj` | L37 | A.S.P. AZIENDA SERVIZI PUBBLICI | `asp-pistoia@pec.it` | Via CILIEGIOLE N. 43, 51100 |
| `1i4r6hfh` | L1 | Consorzio strade vicinali Montenero | `consorziostradamontenero@pec.it` | Via Marconi 9, 58033 |
| `1snwqqo5` | SA | MO.RE S.r.l. | `appalti.more@legalmail.it` | Viale della Stazione n. 5, 39100 |
| `1y69dayi` | SA | AQUILANA SOCIETA MULTISERVIZI | `ACQUISTI@PEC.ASMAQ.IT` | Via DELL'INDUSTRIA, 67100 |
| `1zlo0oib` | L5 | PROVINCIA DELL'OGLIASTRA | `protocollo@pec.provincia.ogliastra.it` | Via MAMELI, 22, 08048 |
| `21u98xl1` | L34 | AZIENDA CONSORTILE WELFARE VESUVIANO | `welfarevesuviano@pec.it` | Piazza ELENA D'AOSTA, 1, 80047 |
| `254g7qf2` | L37 | SIVA SERVICE S.R.L. | `siva.service.srl@pec.it` | C.SO IVREA 118, 14100 |
| `2j7iqvpz` | SA | Ecomisile S.r.l. | `ecomisilesrl@legalmail.it` | Via Petrarca n. 4, 20123 |
| `2o8e0na9` | L36 | Consorzio tra comuni per la gestione delle attivita' e servizi relativi alla realizzazione di strutture e servizi avanzati per l'impresa | `consorzioserviziavanzati@pec.it` | Piazza Del Popolo, n. 8, 56029 |
| `2sh4yo8c` | L2 | Agenzia Metropolitana per la Formazione, l'Orientamento e il lavoro | `segreteriagenerale@pec.afolmet.it` | Via Soderini 24, 20146 |
| `2tujr47o` | L47 | OCDPC 1151 2025 | `ocdpc1151_2025@pec.protezionecivilesicilia.it` | Via ABELA 5, 90141 |
| `2x9nv8rm` | SA | Consorzio Irriguo Naviglio-Pertusata di Cervere | `naviglio.pertusata@pec.it` | Piazza Umberto n. 1, 12040 |
| `321viygl` | SA | FONDAZIONE ITS CAMPANIA MODA | `itscampaniamoda@pec.it` | Via Giuseppe Pica n. 62, 80142 |
| `38hu6hct` | C14 | Ordine dei Medici Veterinari Isernia | `ordinevetis@pec.aruba.it` | Contrada isernia, 86170 |
| `39b07q7b` | SA | Società Immobiliare Belvedere s.r.l. | `socimmbelvedere@pec.it` | Via Mario De Ciccio, 18, 80127 |
| `3jgcanob` | SA | Infratel Italia S.p.A. | `posta@pec.infratelitalia.it` | Via Calabria 46, 00187 |
| `3lm92qzx` | SA | TRENTINO LUNCH S.R.L. | `info@pec.trentinolunch.it` | Via ZENI 8, 38068 |
| `3oyeqcrk` | L37 | GLOBAL POWER S.P.A. | `info@pec.globalpower.it` | Corso PORTA NUOVA 127, 37122 |
| `3tq5qdvm` | L37 | Fondazione ITS Tech&Food - Area Tecnologica Nuove Tecnologie per il Made in Italy - Ambito Settoriale Regionale Agroalimentare | `itstechandfood@pec.itstechandfood.it` | Via Via Martiri di Cefalonia, 14, 43017 |
| `3twjaxop` | L1 | SOGGETTO ATTUATORE REGIONE LAZIO EMERGENZA SANITARIA COVID- 19 | `emergenzacovid19@pec.regione.lazio.it` | Via CRISTOFORO COLOMBO 212, 00145 |
| `3vq38pae` | SA | GRUPPO DI AZIONE LOCALE BASSO TIRRENO REGGINO A R.L. | `galbatir@pec.it` | Via Nazionale 16, 89011 |
| `3xx8bive` | L47 | Commissario Straordinario del Governo per l'adozione di interventi urgenti connessi al fenomeno della diffusione e proliferazione della specie granchio blu | `commissario.gb@pec.masaf.gov.it` | Via XX Settembre 20, 00187 |
| `3xzuh7zy` | SA | Fondazione Taormina | `fondazione.taormina@pec.comune.taormina.me.it` | Corso Umberto I 217, 98039 |
| `437mry30` | L18 | UNIONE DEI COMUNI BASSA VALLE DEL TORTO | `unionedeicomunibassavalledeltorto@pec.it` | VIA ROMA N. 2, 90020 |
| `446w9j1y` | L37 | AUSINO S.P.A.  SERVIZI IDRICI INTEGRATI | `protocollo@pec.ausino.it` | Via ALFONSO  BALZICO, 46, 84013 |
| `470kp2vf` | L37 | AZIENDA SPECIALE SOLARO MULTISERVIZI | `solaromultiservizi@pec.it` | Via Mazzini 76, 20020 |
| `478evj7x` | L37 | GESENU ENTRATE S.R.L. | `GESENUENTRATE@LEGALMAIL.IT` | STRADA DELLA MOLINELLA 7, 06125 |
| `480gndlf` | S01G | VICENZA E' - CONVENTION AND VISITORS BUREAU | `consorziovicenzae@legalmail.it` | via Montale 25, 36100 |
| `48452xfy` | C7 | IPAB Orfanotrofio Parisi Zuppelli Santangelo | `saverinorichiusa@pec.it` | Via Orfanotrofio 22, 96011 |
| `4leto36n` | L47 | COMMISSARIO DELEGATO OCDPC 721/2020 | `emergenza.alluvione2020@pec.regione.sardegna.it` | Via Vittorio Veneto, 28, 09123 |
| `4oiixpzc` | SA | AURORA SRL | `aurorasrl.garetelematiche@pec.it` | Viale Vincenzo Randi 45, 48121 |
| `4yt8gxjt` | L37 | FUTURE SERVICE SRL | `NOTIFICAATTI.FUTURESERVICE@PEC.IT` | Via ERNESTO SIMINI 32/36, 73100 |
| `4yvskh3v` | SA | Naviglio della città di Cremona | `navigliocremona@raccomandata-ar.com` | Via via Cesare Battisti 21, 26100 |
| `53029qd1` | L1 | CONSORZIO STRADA VICINALE ZIA ANEDDA BINGIA DE PIRA | `Consziaanedda@pec.agritel.it` | Via Municipio, 08030 |
| `54mh8wx1` | SA | ATER FONDAZIONE | `ater@pec.ater.emr.it` | Via P. GIARDINI 466/G, 41124 |
| `56sb9f6e` | L18 | Unione dei Comuni "Valle del Fasanella" | `unione@pec.unionedelfasanella.it` | Via Giuseppe Garibaldi n. 5, 84020 |
| `57q4nkxn` | L37 | AMBITO TERRITORIALE DI CACCIA DI MANTOVA N. 4 | `atc4mn@pecimprese.it` | Via Pilona 3, 46031 |
| `5qgp8huo` | L37 | F.P. APPALTI SRL | `fpappalti@pec.it` | Via DEL CONVENTINO 18, 00013 |
| `5xfga83c` | SAG | SAGAT SPA | `pec.sagat@legalmail.it` | STRADA SAN MAURIZIO 12, 10072 |
| `6006vsss` | L37 | SISTEMA AMBIENTE SPA | `sistemaambientelucca@legalmail.it` | Via DELLE TAGLIATE III TRAVERSA IV 136, 55100 |
| `61h4iij0` | L47 | OCDPC 1034_2023 | `ocdpc1034_2023@pec.protezionecivilesicilia.it` | Via G. Abela n. 5, 90141 |
| `69e2hguv` | SA | Courmayeur Mont Blanc Funivie S.p.A. | `cmbf@pec.it` | Strada Dolonne  La Villette 1b, 11013 |
| `6bwzk0sg` | SA | FONDAZIONE COSIMO ED ENNIO DE GIORGI ETS | `ispefondazionedegiorgi@pec.it` | Via San Lazzaro n. 15, 73100 |
| `6pin2f5x` | SA | PATRIMIO TAORMINA | `patrimonio.taormina@pec.comune.taormina.me.it` | Corso UMBERTO N. 217, 98039 |
| `6pm6n6si` | L47 | SUB-COMMISSARIO DL 61-23 ART 20 QUINQUIES COMMA 4 BIS ZONA EMILIA-ROMAGNA | `SUBCOMDL6123@postacert.regione.emilia-romagna.it` | Via, Aldo Moro 52, 40127 |
| `6v91bkhk` | L37 | COOPERATIVA SOCIALE LA QUERCIA | `COOPQUERCIA@LEGALMAIL.IT` | Via LUIGI PIRANDELLO, 95016 |
| `6w0ztant` | L47 | COMMISSARIO DELEGATO OCDPC 1120-24 OCDPC 1087-24 OCDPC 1022-23 ZONA EMILIA ROMAGNA | `OCDPC1022@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `735id71u` | L37 | ASTEM SPA | `astemspa@legalmail.it` | Viale Dante 2, 26900 |
| `7c6v5b2r` | L33 | ISTITUTO COMPRENSIVO SIANI-ALIGHIERI | `NAIC8G7002@PEC.ISTRUZIONE.IT` | Via ROBERTO DE VITO,1, 80034 |
| `7d4px82j` | L37 | ENEL GREEN POWER SPA | `enelgreenpower@pec.enel.it` | VIALE REGINA MARGHERITA 125, 00198 |
| `7dfyyiwa` | L37 | NERULUM SERVICE SRL | `nerulumservice@pec.it` | Via ROMA 56, 85048 |
| `7h7m2pq0` | L37 | SO.SVI.MA. SPA | `sosvima.agenzia@pec.it` | Via VIALE RISOSRGIMENTO N. 13/B, 90020 |
| `7hc22r9i` | L1 | ASUC CASTELFONDO | `asuccastelfondo@pec.it` | Piazza G. Cantore, 38013 |
| `7txuc0uj` | L37 | Società Farmaceutica Foiano s.r.l. | `societafarmaceuticafoiano@pec.it` | Piazza Cavour n. 1, 52045 |
| `7tyix3xj` | SA | Coutenza Canali Lanza Mellana e Roggia Fuga | `canalilanza@pec.it` | Via Guala 9, 15033 |
| `7wc83bca` | L1 | CONSORZIO OBBLIGATORIO STRADE VICINALI PALESTRINA | `stradevicinalipalestrina@legalmail.it` | Piazza PIAZZA DEL CARMINE SNC, 00036 |
| `7zj0jtpq` | L47 | OCDPC 1084_2024 | `ocdpc1084_2024@pec.protezionecivilesicilia.it` | Via G. Abela n. 5, 90141 |
| `81r3mh1h` | SA | Fondazione Morra Greco ETS | `fondazionemorragreco@altapec.it` | Via Toledo 106, 80138 |
| `8kwi35em` | SA | PROVINCIA SAN FRANCESCO DI PAOLA DELL'ORDINE DEI MINIMI | `provincia@pec.it` | Largo San Francesco 1, 87027 |
| `8oh2q4wu` | SA | A.RI.C.A. AZIENDE RIUNITE COLLETTORE ACQUE | `protocollo@pec.consorzioarica.it` | Via Ferraretta, 10, 36071 |
| `8yjgw8qh` | SA | ENVAL S.R.L. | `enval@greenholdingpec.it` | Regione Borgnalle 10L, 11100 |
| `91licpep` | L37 | ITS Tecnologie Innovative per il Made in Italy | `info@pec.itsmitimoda.it` | Contrada Pergolo, 74015 |
| `93g8tw4t` | L18 | Unione di Comuni Lombarda Terra di Cascine | `unione.terradicascine@pec.regione.lombardia.it` | Piazza Municipio 23, 26022 |
| `98vyk3p0` | C14 | Ordine Interprovinciale dei Dottori Agronomi e dei Dottori Forestali del Piemonte | `protocollo.odaf.piemonte@conafpec.it` | Via Amedeo Peyron 13, 10143 |
| `9c4kqewc` | SA | RIVIERA AIRPORT S.P.A. | `ava@legalmail.it` | Viale Viale Generale Disegna snc, 17038 |
| `9hnsg4nn` | L37 | LINEA GESTIONI S.R.L. | `lineagestioni@pec.a2a.eu` | Via DEL COMMERCIO N.29, 26013 |
| `9k62wynv` | L47 | COMMISSARIO STRAORDINARIO DI GOVERNO PER LA ZES ABRUZZO | `commissariozes.abruzzo@pec.agenziacoesione.gov.it` | SICILIA 162/C, 00187 |
| `9pbyaa8i` | C3 | Poliambulatorio Montezemolo | `poliambulatorio.montezemolo@corteconticert.it` | Via Fratelli Rosselli s.n.c., 00195 |
| `9xbsz46i` | SA | PSG Servizi & Salute s.r.l. | `psgserviziesalute@legalmail.it` | Contrada Savorgnan 11/A, 33057 |
| `9z0lbtjc` | SA | A.S.TER. Azienda servizi territoriali Genova S.p.A. | `direzioneastergenova@sicurezzapostale.it` | Via XX SETTEMBRE 15, 16121 |
| `a2qozbnl` | L37 | casteldaccia ambiente e altri servizi srl | `casteldacciaambiente@pec.it` | Piazza matrice 11, 90014 |
| `a2v9oory` | L6 | fondazione asiago 7 comuni | `fondazioneasiago7comuni@legalmail.it` | stazione, 36012 |
| `a7oq3otd` | L18 | UNIONE DEI COMUNI TERRE DEL LINO | `unione.terredellino@pec.regione.lombardia.it` | Piazza GARIBALDI,16, 26033 |
| `abigs` | L1 | Amministrazione Separata  Beni Usi Civici Cengles | `ebnr.tschengls@pec.rolmail.net` | Cengles 15, 39023 |
| `abucsi` | L1 | Amministrazione Beni Uso Civico St.Sigmund | `fraktion.st.sigmund@pec.it` | Via Peuren 2 A, 39030 |
| `acpspa` | S01 | Autostrade Centro Padane Spa | `centropadane@legalmail.it` | Via Colletta, 1, 26100 |
| `adb` | L1 | Asuc di Brez | `asucbrez@pec.it` | Piazza Municipio, 38028 |
| `afrnet` | S01 | Afragolanet S.R.L. Unipersonale | `afragolanetsrl@pec.it` | Piazza Municipio, 1, 80021 |
| `afsl` | S01 | Aeroporto di Frosinone Spa - in Liquidazione | `aeroportofrosinone@pec.it` | Via Dei Volsci, 29, 03100 |
| `aftn` | L1 | Asuc Faedo | `asucfaedo@pec.it` | Via S. Agata 5, 38098 |
| `agtpa` | L37 | Agenzia Gioia Tauro Port Agency | `alpgt@pec.it` | Contrada Lamia, 89013 |
| `aicb` | L34 | Asilo Infantile Castelletto Busca | `ASILOCASTELLETTO@PEC.IT` | Via Monastero, 180, 12022 |
| `aig` | L34 | Asilo Infantile G. Destefanis | `asilodestefanis@arubapec.it` | Via G. Destefanis 68, 10070 |
| `aim` | L34 | Fondazione Asilo Infantile Salvatore Ruggiero Ex Ipab | `fondazionesalvatoreruggiero@pec.it` | Piazza Vittorio Veneto 10, 80062 |
| `aimar` | L34 | Asilo Infantile Maria | `s.mainardi@pec.it` | Via Garibaldi N.2, 13893 |
| `aimcr` | L34 | Asilo D'Infanzia Maria Ceccarini Riccione | `ipabceccarini@pec.it` | Corso Flli Cervi, 50, 47838 |
| `aisdd` | L34 | Asilo Infantile San Damiano D'Asti | `asiloinfantilesd@pcert.postecert.it` | Via C. Beccaria 6, 14015 |
| `amspame` | L44 | Ato Me 2 S.P.A. in Liquidazione | `atome2spa@pec-mail.it` | Via Strada Statale S.antonino, 461, 98051 |
| `apser` | L37 | Appia Servizi Srl | `appiaservizisrl@pec.it` | Vico Isonzo, 4, 81040 |
| `apspmp` | L34 | Azienda Pubblica di Servizi alla Persona Maria De Peppo Serena e Tito Pellegrino | `asplucera.ragioneria@pec.it` | Piazza S. Leonardo, 33, 71036 |
| `apsppg` | L34 | Apsp Fusconi Lombrici Renzi | `apspnorcia@pec.it` | Viale Lombrici, 27, 06046 |
| `apspt` | L34 | Azienda Pubblica di Servizi alla Persona di Terra Jonica C.Mondelli A. De Carlo S. Benedetto - Opere Pie Riunite S. Zuccaretti e V. De Cesare | `aspditerrajonica@pec.it` | Via Lombardia, 61, 74121 |
| `arb8nuny` | L1 | AMMINISTRAZIONE SEPARATA USI CIVICI DI STUMIAGA | `asuc.stumiaga@pec.it` | Via STUMIAGA 37, 38075 |
| `arisme` | C3 | A.Ris.Me | `arisme@pec.it` | Piazza Unione Europea, 98122 |
| `asbco` | L1 | Amministrazione Separata Buc Corvara | `fraziun.corvara@pec.rolmail.net` | Str. Col Alt, 36, 39033 |
| `asbsold` | L1 | Amministrazione Separata Beni Usi Civici di Solda | `eigenverwaltung.sulden@pec.rolmail.net` | Stelvio Paese 24, 39029 |
| `asbucca` | L1 | Amministrazione Separata Beni Usi Civici Casteldarne | `eigenverwaltungfraktionehrenburg@legalmail.it` | Via Chienes, 4C, 39030 |
| `asbucd` | L1 | Amministrazione Sep. B.U.C. Braies di Dentro | `fraktion.innerprags@pec.sbb.it` | Braies Di Dentro, 40, 39030 |
| `asbuce` | L1 | Amministrazione Seprarata Beni Usi Civici Ega | `e.b.n.r.eggen@pec.rolmail.net` | Via Castello Thurn, 1, 39050 |
| `asbuceo` | L1 | Amministrazione Separata Beni Usi Civici Eores | `evbnr.afers@pec.sbb.it` | Via Aussergasse 24, 39042 |
| `asbucf` | L1 | Amministrazione Sep. B.U.C. Braies di Fuori | `fraktion.ausserprags@pec.sbb.it` | Braies Di Dentro, 40, 39030 |
| `asbucfp` | L1 | Amministrazione Separata Beni di Uso Civico Frazione di Pergine | `asuc@pec.comune.pergine.tn.it` | Piazza Garibaldi, 7, 38057 |
| `asbucfr` | L1 | Amministrazione Separata Beni Usi Civici Frassene | `asbucfrassene@pec.net` | Viale Della Vittoria, 43a, 32020 |
| `asbucfsa` | L1 | Amministrazione Separata Beni Uso Civico Frazione Salorno | `SalornoBUC_SalurnBNR@pec.it` | Piazza Municipio, 1, 39040 |
| `asbucg` | L1 | Amministrazione Separata Dei Beni di Uso Civico della Frazione di Gais | `fraktiongais@pec.it` | Ulrich von Taufers Strasse 5, 39030 |
| `asbuclac` | L1 | Amministrazione Separata Beni Usi Civici Lasa Centro | `ebnr.laas@pec.rolmail.net` | Via Venosta N. 52, 39023 |
| `asbucmsp` | L1 | Amministrazione Seprarata Beni Usi Civici Monte San Pietro | `e.b.n.r.petersberg@pec.rolmail.net` | Via Castello Thurn, 1, 39050 |
| `asbucmu` | L1 | Amministrazione Separata Beni Usi Civici Mules Con Cave | `yasmin.sparber@pec.it` | Mules, 84, 39040 |
| `asbucmz` | L1 | Amministrazione Separata Beni Usi Civici della Frazione di Maranza | `fraktion@pec.it` | Maranza, Via Waldeler 5, 39037 |
| `asbucnp` | L1 | Amministrazione Seprarata Beni Usi Civici Nova Ponente | `e.b.n.r.deutschnofen@pec.rolmail.net` | Via Castello Thurn, 1, 39050 |
| `asbucpe` | L1 | Amministrazione Separata B.U.C. Pescosta | `cm@pec.rolmail.net` | Str. Col Alt, 36, 39033 |
| `asbucrv` | L1 | Amministrazione Separata B.U.C. Frazione di Riva | `manfred.knapp@odcecbz.legalmail.it` | Via Municipio, 8, 39032 |
| `asbucs` | L1 | Amministrazione Separata Beni Usi Civici di Slingia | `fraktion.schlinig@pec.sbb.it` | Slingia, 46, 39024 |
| `asbucsb` | L1 | Amministrazione Separata B.U.C. Frazione San Benedetto | `fraktion.nauders@pec.it` | Frazione San Benedetto 65a, 39037 |
| `asbucsf` | L1 | Amministrazione Separata Beni Ad Uso Civico San Felice | `ebnrstfelix@pec.rolmail.net` | Via Palade, 12, 39010 |
| `asbucsv` | L1 | Amministrazione Separata Beni Usi Civici San Vito | `fraktionstveit@legalmail.it` | Via Della Chiesa, 7, 39030 |
| `asbuctc` | L1 | Amministrazione Separata Beni Usi Civici di Tarces | `fraktion.tartsch@pec.it` | Tarces 84, 39024 |
| `asbucti` | L1 | Amministrazione Separata Beni Usi Civici di Taio | `asuctaio@legalmail.it` | Via Simone Barbacovi, 4, 38012 |
| `asbuctu` | L1 | Amministrazione Separata Beni Usi Civici Caminata | `fraktion.kematen@pec.it` | Municipio, 39032 |
| `asbucvl` | L1 | Amministrazione Separata Beni Uso Civico Vallarga | `bnr-fraktionweitental@pec.rolmail.net` | Hinterdrittel 12, 39030 |
| `asbucvre` | L1 | Amministrazione Separata Beni di Uso Civico Comunita' Vigo Rendena | `asucdivigorendena@pec.cgn.it` | Via Iv Novembre, 10 Vigo Rendena, 38094 |
| `asbuface` | L1 | Amministrazione Separata B.U.C. Frazione Acereto | `fraktion.ahornach@pec.it` | Acereto, 114, 39032 |
| `asbufal` | L1 | Amministrazione Separata Beni di Uso Civico Frazione di Falesina | `asucfalesina@pec.it` | Frazione Vignola, 12, 38057 |
| `asbufc` | L1 | Amministrazione Separata Beni Usi Civici Frazione Campo Tures | `fraktion.sandintaufers@pec.it` | Via Municipio 8, 39032 |
| `ascs` | L37 | Azienda Speciale Pluriservizi Comune di Saracena | `asp.saracena@open.legalmail.it` | Via Carlo Pisacane, 87010 |
| `asdbuca` | L1 | Amministrazione Separata Dei Beni di Uso Civico di Castelbello Ciardes | `fraktion.kastelbell@pec.sbb.it` | Piazza Centro, 1, 39020 |
| `asdbucc` | L1 | Amministrazione Separata Dei Beni di Uso Civico Colsano | `fraktion.galsaun@pec.sbb.it` | Piazza Centro, 1, 39020 |
| `asdbucci` | L1 | Amministrazione Separata Dei Beni di Uso Civico Ciardes | `FRAKTION.TSCHARS@PEC.SBB.IT` | Piazza Centro, 1, 39020 |
| `asdgoss` | L1 | Ammistrazione Separata Beni Civici di Druogno Gagnone Orcesco Sagrogno Sasseglio | `benicivicidruogno@pec.it` | Piazza Municipio, 3, 28853 |
| `asmfc` | L37 | A.S.M. Farmacie Comunali Garbagnate Milanese S.R.L. | `asmfarmacie@pec.it` | Piazza De Gasperi, 1, 20024 |
| `aspt` | L1 | Amministrazione Separata Promisquita di Tesido | `exgemeinde.taisten@pec.rolmail.net` | Via Riva Di Sotto, 39035 |
| `asucd` | L1 | Amministrazione Separata Usi Civici di Dardine | `asucdardine@legalmail.it` | Via Simone Barbacovi, 4, 38012 |
| `asucdar` | L1 | Amministrazione Separata Usi Civici di Dare | `asucdare@pec.it` | Via Dare, 38, 38094 |
| `asucdeg` | L1 | Amministrazione Separata Usi Civici di Deggiano | `asuc.deggiano@legalmail.it` | Via Del Comun, 38020 |
| `asucf` | L1 | Amministrazione Separata Usi Civici di Favrio | `asucfavrio@pec.it` | Favrio, 38075 |
| `asucffi` | L1 | Amministrazione Separata Usi Civici Fisto | `asuc.fisto@pec.it` | Frazione Fisto 58, 38088 |
| `asucfia` | L1 | Amministrazione Separata Usi Civici Fiave' | `asuc.fiave@pec.it` | Via San Zeno, 18a, 38075 |
| `asucl` | L1 | Amministrazione Separata  Beni Usi Civici di Clusio | `fraktion-schleis@pec.rolmail.net` | Clusio Schleis, 39024 |
| `asuclov` | L1 | Amministrazione Separata Usi Civici Lover | `asuclover@pec.it` | Frazione Lover Piazza San Giorgio, 4, 38010 |
| `asucpi` | L1 | Amministrazione Separata Usi Civici di Piano | `asuc.piano@legalmail.it` | Via Del Comun 10, 38020 |
| `asucq` | L1 | Amministrazione Separata Usi Civici di Quetta | `asucquetta@pec.it` | Via Ciasal, 1, 38010 |
| `asucs` | L1 | Amministrazione Separata Usi Civici di Segno | `asucsegno@legalmail.it` | Via Simone Barbacovi, 4, 38012 |
| `asucsa` | L1 | Amministrazione Separata Usi Civici di S.Agnese | `asucsagnese@pec.it` | Via Degasperi, 33a, 38045 |
| `asucse` | L1 | Amministrazione Separata Usi Civici di Seregnano | `asucseregnano@pec.it` | Via Degasperi, 33a, 38045 |
| `asucsm` | L1 | Amministrazione Separata Usi Civici di S.Mauro | `ASUC.SMAURO@PEC.IT` | Via Di S. Mauro, 57, 38042 |
| `asucsma` | L1 | Amministrazione Separata Usi Civici di Smarano | `asucsmarano@legalmail.it` | Piazza Don L. Dal Ponte, 1, 38010 |
| `asucsop` | L1 | Asuc Sopramonte | `asuc.sopramonte@pec.it` | Via Di Revolta 4 - Fraz. Sopramonte, 38123 |
| `asucsot` | L1 | Amministrazione Separata Usi Civici Sant'Orsola | `asucsantorsola@legalmail.it` | Localita Pintarei 55, 38050 |
| `asucve` | L1 | Asuc Verdesina | `asucverdesina@pec.it` | Via Verdesina, 9, 38080 |
| `asucvifa` | L1 | Amministrazione Separata Usi Civici di Vigo di Fassa del Comune di Sen Jan | `asucvich@pec.comune.senjandifassa.tn.it` | Strada Rezia, 12, 38039 |
| `asucvr` | L1 | Asuc Villa Rendena | `asucvillarendena@pec.it` | Via Verdesina, 9, 38080 |
| `asucvt` | L1 | Amministrazione Separata Usi Civici Vigo di Ton | `asucvigoditon@pec.it` | Vigo Di Ton Piazza Guardi, 7, 38010 |
| `asupor` | L1 | Asuc di Por | `asucpor@pec.it` | Frazione Por, 38085 |
| `asus` | L1 | Asuc di Strada | `asuc.strada@pec.it` | Fraz. Strada, 38085 |
| `atca_101` | C3 | Ambito Territoriale di Caccia Atckr2 | `atckr2@pcert.postecert.it` | Via Antonio Panella, 178, 88900 |
| `atie` | L44 | Assemblea Territoriale Idrica Enna | `atienna@pec.it` | Via Trieste 13, 94100 |
| `atome1` | L44 | Ato Me 1 Spa in Liquidazione | `PROTOCOLLO@PEC.ATOME1SPA.COM` | Via Medici 259, 98076 |
| `atsmag` | L6 | Associazione Temporanea di Scopo Maguli | `ats.maguli@legalmail.it` | Piazza Municipio, 5, 95041 |
| `au042wp3` | SA | Progroup Board S.r.l. | `progroupboardsrl@legalmail.it` | Via Via Lodovico Settala, n. 3, 20124 |
| `avssm` | L37 | Associazione di Volontariato e Solidarieta Sociale Millevoci | `millevoci@pec.it` | Via San Lazzaro, 8 A, 61032 |
| `ay3zmtp0` | L37 | ISTITUTO TECNICO SUPERIORE TECHNOLOGIES TALENT FACTORY | `i.t.s.techtalentfactory@legalmail.it` | Via  SAN VITTORE N. 21, 20123 |
| `b2fo2wn3` | L34 | Casa della Fanciulla del Carmelo-Cantello | `casadellafanciullaediriposoipab@pec.it` | Piazza Gramsci, 20, 93011 |
| `b4lub3pe` | SA | SEA AMBIENTE S.P.A. | `seambiente@postecert.it` | Via Dei Comparini 186, 55049 |
| `b69wa07f` | L37 | GRS SRL | `postapec@pec.grssrl.com` | Corso GARIBALDI, 183, 84122 |
| `bbnif4bn` | L37 | Fondazione ITS per l'Efficienza Energetica di Reggio Calabria | `itsenergeticarc@pec.it` | Via Emilio Cuzzocrea, 89128 |
| `bgk42ke5` | SA | RAI - RADIOTELEVISIONE ITALIANA S.P.A. | `raispa@postacertificata.rai.it` | Via Alessandro Severo 246, 00145 |
| `bmy560ix` | SA | Infratrasporti.To S.r.l. | `INFRATRASPORTITOSRL@LEGALMAIL.IT` | Corso Novara 96, 10152 |
| `bprtp` | L34 | Ipab Boccone del Povero Riggirello | `ipabriggirello@pec.it` | Via Messina N. 4, 91028 |
| `bqsqko3n` | L37 | FARMACIA COMUNALE DI SPIRANO S.R.L. | `farmaciacomunalespiranosrl@pec.it` | Largo EUROPA, 24050 |
| `bteyi4sx` | L37 | Ciclat Trasporti Ambiente Società Cooperativa | `ciclatambiente@ciclatpec.ra.it` | Via Luciano Romagnoli 13, 48123 |
| `c0m169gn` | L37 | COGESER S.P.A. | `cogeserspa@legalmail.it` | Via MARTIRI DELLA LIBERTA' N. 18, 20066 |
| `c526abvo` | L6 | Consorzio Volontario per la Valorizzazione Turistica del Litorale Tarantino Occidentale | `costaverde.castellaneta@pec.it` | Piazza John Fitzgerald Kennedy, 74011 |
| `c5p9vi43` | C14 | Ordine provinciale della professione sanitaria di fisioterapista di Reggio Calabria | `reggiocalabria.ofi@pec.fnofi.it` | Via Francesco Baracca 10, 89123 |
| `c7roxf19` | L47 | commissario straordinario per la realizzazione dei giochi del mediterraneo 2026 | `commissario.giochimediterraneo26@pec.governo.it` | Viale Virgilio n. 152, 74121 |
| `cabmar` | L6 | Consorzio Acquedotto Benevello - Montelupo Albese - Rodello | `acquedotto.bmr@legalmail.it` | Piazza Comunale, 6, 12050 |
| `cabonif` | L37 | Consorzio Aurunco di Bonifica | `consorzioauruncodibonificainliquidazione@pec.net` | Via Delle Terme, 8, 81037 |
| `cadf` | L1 | Comunanza Agraria di Foce | `comunanzafoce@legalmail.it` | Fraz. Foce, 63088 |
| `caisb` | L1 | Comunanza Agraria di Isola San Biagio | `comunanzaisolasanbiagio@pec.it` | Fraz. Isola San Biagio, 63088 |
| `cale2sc` | L36 | Consorzio Ato Le 2 Salento Centrale | `CONSORZIOATOLE2@LEGALMAIL.IT` | Piazza Indipendenza, 73020 |
| `capls` | L36 | Consorzio Agrigentino per La Legalita e Lo Sviluppo | `consorzioagrigentinolegalita@pec.it` | P.za Don Giustino, 92026 |
| `carbba` | L6 | Consorzio Ato Rifiuti Bacino Ba1 | `unionearo2bt@pec.it` | Piazza Umberto I, 76123 |
| `caroc` | L1 | Comunanza Agraria di Rocca | `comunanzarocca@legalmail.it` | Fraz. Rocca, 63088 |
| `carsc` | L37 | Consorzio Autonoleggiatori Riuniti Soc Coop | `carat@indirizzopec.com` | Via Elio Vittotini, 29, 06012 |
| `cav` | L36 | Consorzio Ambiente Versilia | `consorzioambienteversilia@pec.it` | Via Papa Giovanni XXIII, 86, 55054 |
| `caval` | L1 | Comunanza Agraria di Vallegrascia | `comunanzavallegrascia@legalmail.it` | Fraz. Vallegrascia, 63088 |
| `cbbosrl` | L37 | C.B.B.O. Srl | `fatturazione@pec.cbbo.it` | Via Industriale, 33, 25016 |
| `cbiba` | SAG | Consorzio di Bonifica Interno 'Bacino Aterno e Sagittario' | `areatecnicacbaternosagittario@pec.it` | Via Trieste 63, 67035 |
| `cbimbat` | L24 | Consorzio Bacino Imbrifero Montano del Bormida Asti | `bimbormidaat@pec.it` | Via Cortemilia, 1, 14051 |
| `cbimds` | L24 | Consorzio del Bacino Imbrifero Montano dello Scrivia | `consorziobimscrivia@legalmail.it` | Piazza Santo Bertelli, 15061 |
| `cbims` | L24 | Consorzio B.I.M. dello Spol | `bimspol@pec.it` | plaza dal comun 93, 23041 |
| `cbimsm` | L24 | Consorzio Bacino Imbrifero Montano del Sarca Mincio Garda | `bim.smg.vr@pec.it` | Via XX Settembre, 8, 37010 |
| `cbpsm` | L37 | Consorzio di Bonifica della Piana di Sibari e Media Valle in Liquidazione | `consorziobonificasc@pec.it` | Via G.Russo, 6, 87100 |
| `ccf` | L36 | Consorzio di Campocatino in Liquidazione | `consorziodicampocatino@pec.it` | Piazza Gramsci 13, 03100 |
| `ccil` | L18 | Comunita' Collinare Intorno al Lago | `protocollo.intornoallago@cert.ruparpiemonte.it` | Via Torino, 4, 10031 |
| `ccpavn` | L6 | Consorzio Casa Protetta Alta Val Nure | `casaprotetta.altavalnure@legalmail.it` | Localita Borcaglie, 29023 |
| `ccsrl` | L37 | Casa Civita Srl | `CASACIVITASRL@PEC.IT` | Via Roma, 28, 01022 |
| `cctc` | L36 | Ctc Consorzio Trasporti Comunali | `ctcroccadarce@pec.it` | Via IV Novembre,1, 03030 |
| `cdbat` | L37 | Centro di Diagnostica Bio-Chimica di Angela Tucci e C. S.N.C. | `aldo.corrado@biologo.onb.it` | Viale Italia 269-271, 83100 |
| `cdcmuaf` | L6 | Consorzio Dei Comuni per Il Museo Territoriale dell'Agro Foronovano | `consorziomuseo@pec.it` | Piazza Roma, 6, 02049 |
| `cdeamag` | L1 | Commissario Delegato Eventi Atmosferici Maggio | `commissariodelegatomaggio@regione.lazio.legalmail.it` | Via Rosa Raimondi Garibaldi, 7, 00145 |
| `cdear` | L1 | Commissario Delegato Emergenza Ambientale nella Regione Puglia Opcm 2450 Del1996 | `emergenzaambientale@pec.rupar.puglia.it` | Via Lattanzio, 29, 70126 |
| `cdears` | L1 | Commissario Delegato Emergenza Arsenico nel Lazio | `commissariodelegatoarsenico@regione.lazio.legalmail.it` | Via Rosa Raimondi Garibaldi, 7, 00145 |
| `cded` | L1 | Commissario Delegato  Emergenza Dissesto Idrogeologico Bonorva | `emergenzabonorva@pec.comune.bonorva.ss.it` | Piazza Santa Maria 27, 07012 |
| `cdesea` | L1 | Commissario Delegato all'Emergenza Socio Economico-ambientale Regione Puglia | `gabinetto.prefba@pec.interno.it` | Piazza Liberta, 1, 70122 |
| `cdodi` | L47 | Commissario Delegato Ocdpc 472 2017 | `ocdpc472_2017@pec.protezionecivilesicilia.it` | Via Gaetano Abela, 90100 |
| `cdodpc` | L47 | Commissario Delegato Ocdpc 458 2017 | `ocdpc458_2017@pec.protezionecivilesicilia.it` | Via Gaetano Abela, 90100 |
| `cdssub` | L1 | Commissario Delegato Subsidenza | `commissariodelegatosubsidenza@regione.lazio.legalmail.it` | Via Rosa Raimondi Garibaldi, 7, 00145 |
| `cgadm` | C14 | Collegio Guide Alpine Delle Marche | `collegioguidealpinemarche@pec.it` | Contrada Fonte Balzana, 1, 63823 |
| `cibimpr` | L24 | Consorzio Intercomunale del Bacino Imbrifero Montano di Parma | `bimtorrenteparma@pec.it` | Largo Castello, 1, 43021 |
| `cidaeaci` | C14 | Collegio Interprovinciale Degli Agrotecnici e Degli Agrotecnici Laureati di Campobasso e Isernia | `molise@pecagrotecnici.it` | Via San Lorenzo, 68, 86100 |
| `cif` | L36 | Consorzio Idrico Fontanazzo | `consorzioidricofontanazzo@pcert.postecert.it` | Corso Italia, 45, 17014 |
| `cifsp` | L6 | Consorzio Intercomunale Fognatura Sinistra Piave | `cons.fognatura.sxpiave@pec.it` | Via Vittorio Veneto, 2, 31016 |
| `cigat` | L6 | Consorzio Intercomunale Gasdotto Val Trebbia | `consorzio.gasdottovaltrebbia@legalmail.it` | Piazza Trento, 21, 29020 |
| `cimepop` | L6 | Consorzio Intercomunale Milanese per L'Edilizia Popolare | `cimep@pecmailbox.com` | Via Giovanni Battista Pirelli, 30, 20124 |
| `cimtaro` | L24 | Consorzio Imbrifero Montano del Taro | `consorziobimdeltaro@pec.it` | Piazza Manara 6, 43043 |
| `cipabtv` | C14 | Collegio Interprovinciale Dei Periti Agrari e Dei Periti Agrari Laureati di Belluno, Treviso e Venezia | `collegio.btv@pec.peritiagrari.it` | Viale Veneto, 40, 31015 |
| `cipls` | L6 | Consorzio Intercomunale di Polizia Locale Segrino in Liquidazione | `consorzio.segrino@pec.regione.lombardia.it` | P.zza Remo Sordo, 3, 22035 |
| `cipmpc` | L36 | Consorzio Intercomunale di Polizia Municipale e Protezione Civile Delle Valli Joniche | `comunepagliara@pec.it` | Via R. Margherita, 92, 98020 |
| `cipsal` | L36 | Consorzio Intercomunale per Un Piano di Sviluppo Alta Lomellina | `cipal@pec.it` | Corso Cavour, 85, 27036 |
| `cipsc` | L36 | Consorzio Intercomunale di Promozione e Sviluppo della Costa Tirrenica in Liquidazione | `consorziointercomunalecostatirrenica@pec.it` | Largo Municipio Presso Sede Comunale, 89861 |
| `cittss` | L6 | Consorzio per L'Amministrazione del Complesso Idrotermale di Telese Terme e di San Salvatore Telesino | `segreteria.consorzioidrotermale@pec.cstsannio.it` | Viale Minieri, 146, 82037 |
| `ciuse` | L36 | Consorzio Intercomunale Ufficio Sviluppo Economico Valli Joniche | `comunepagliara@pec.it` | Via R. Margherita, 92, 98020 |
| `ciust` | L36 | Consorzio Intercomunale Ufficio Sviluppo Turistico Delle Valli Joniche | `comunepagliara@pec.it` | Via R. Margherita, 92, 98020 |
| `ciutfvj` | L36 | Consorzio Intercomunale Uffici Tecnici e Finanziari Delle Valli Joniche | `comunepagliara@pec.it` | Via R. Margherita, 92, 98020 |
| `civdc` | L6 | Consorzio per La Industrializzazione della Vallata del Cismon | `consorzio.vallata.cismon@legalmail.it` | Piazza I Novembre, 14, 32030 |
| `ck3ostzd` | C14 | Ordine Interprovinciale della Professione Sanitaria di Fisioterapista di Bari, Barletta Andria Trani e Taranto | `pugliacentrale.ofi@pec.fnofi.it` | Via Magliano, 62, 70010 |
| `ckh4k9xj` | L1 | Amministrazione Separata Beni Civici di Buttogno | `benicivicibuttogno@pec.it` | Via Piave, 2, 28857 |
| `clpe` | C14 | Ordine Dei Consulenti del Lavoro di Pescara | `ordine.pescara@consulentidellavoropec.it` | Via Chieti, 5, 65121 |
| `cm_giovo` | L12 | Comunita' Montana del Giovo | `cmi@legalmail.it` | c. Italia, 3, 17100 |
| `cm_mrtm` | L12 | COMUNITA MONTANA DEI MONTI REVENTINO TIRIOLO MANCUSO | `commissariounicocmliquidazione@pec.it` | Via Miguel Cervantes, 10, 88049 |
| `cmdavtb` | L12 | Comunita' Montana Delle Alte Valli Trebbia e Bisagno | `vallitrebbiaebisagno@pec.it` | P.zza Matteotti, 1, 16018 |
| `cmea` | L1 | Centro Meridionale di Educazione Ambientale | `cmeapec@pec.cmea.it` | Piazza S. Antonino, 80067 |
| `cmls` | L6 | Consorzio Madonita per La Legalita' e Lo Sviluppo | `consorziomadonitalegalita@pec.it` | Via Garibaldi, 13, 90028 |
| `cmoea` | L12 | Comunita' Montana dell'Olivo Ed Alta Valle Arroscia in Liquidazione | `cmi@legalmail.it` | Loc. Roccanegra, 18027 |
| `cmvfpfn` | L12 | Comunita Montana del Vomano Fino Piomba | `cmvomano@pec.it` | Via Nazionale, 69, 64037 |
| `cmvge` | L12 | Comunita Montana Valli Stura Orba Leira in Liquidazione | `vallisturaorba@pec.it` | Via Convento 8, 16013 |
| `cnao` | C14 | Consiglio Notarile di Aosta | `cnd.aosta@postacertificata.notariato.it` | Via De Tillier, 3, 11100 |
| `cnbiel` | C14 | Consiglio Notarile di Biella ed Ivrea | `cnd.biella@postacertificata.notariato.it` | Via Duomo 3, 13900 |
| `cnc` | C14 | Consiglio Notarile di Cagliari | `cnd.cagliari@postacertificata.notariato.it` | Via Logudoro, 40, 09127 |
| `cndag` | C14 | Consiglio Notarile Dei Distretti Riuniti di Agrigento | `cnd.agrigento@postacertificata.notariato.it` | Viale Della Vittoria N.319, 92100 |
| `cngr` | C14 | Consiglio Notarile di Grosseto | `cnd.grosseto@postacertificata.notariato.it` | Via Abruzzi 11, 58100 |
| `cnla` | C14 | Consiglio Notarile L'Aquila | `cnd.laquila@postacertificata.notariato.it` | Via Savini, 25, 67100 |
| `cnrg` | C14 | Consiglio Notarile Dei Distretti Riuniti di Ragusa e Modica | `cnd.ragusa@postacertificata.notariato.it` | Via Ecce Homo N.183, 97100 |
| `cns` | C14 | Consiglio Notarile di Sondrio | `cnd.sondrio@postacertificata.notariato.it` | Via Piazzi, 29, 23100 |
| `cntepe` | C14 | Consiglio Notarile di Teramo e Pescara | `cnd.teramo@postacertificata.notariato.it` | Via Vincenzo Cerulli Irelli, 5, 64100 |
| `cocb` | L36 | Consorzio Occhito | `consorzio.occhito@pec.it` | Via Fratelli Bandiera, 86040 |
| `cofic` | L24 | Consorzio Obbligatorio Fra I Comuni della Provincia di Treviso Facenti Parte del Bacino Imbrifero del Brenta | `bimbrentatreviso@pecit.it` | Via Iv Novembre, 31 Crespano, 31017 |
| `consborm` | L24 | Consorzio Bim Alta Val Bormida | `protocollo@pec.bimbormidasavona.it` | Piazza Italia, 17017 |
| `coredipa` | C3 | Co.Re.Di. Commissione Amministrativa Regionale di Disciplina Sicilia | `coredi.sicilia@pec.it` | Via Bandiera, 11, 90133 |
| `covi` | L37 | Covigas S.R.L. | `covigas@pec.it` | Piazza A. Massalongo, 2, 37039 |
| `coyur7ez` | L37 | Fondazione I.T.S. per l'Informazione e la Comunicazione | `cert@pec.itsincom.it` | Viale Stelvio 173, 21052 |
| `cpaalvi` | C14 | Collegio Provinciale Agrotecnici e Agrotecnici Laureati di Vicenza | `vicenza@pecagrotecnici.it` | Casella Postale N. 7 - Cesuna, 36010 |
| `cpdadc` | C14 | Collegio Provinciale Degli Agrotecnici e Degli Agrotecnici Laureati di Chieti | `chieti@pecagrotecnici.it` | Via Valle D'oro, 31, 66010 |
| `cpdae_1` | C14 | Collegio Provinciale Degli Agrotecnici e E Degli Agrotecnici Laureati di Catania | `catania@pecagrotecnici.it` | Piazza Regina Elena N, 24, 95047 |
| `cpdpabr` | C14 | Collegio Provinciale Dei Periti Agrari e Periti Agrari Laureati di Brindisi | `collegio.brindisi@pec.peritiagrari.it` | Via Custoza, 82, 72017 |
| `cpes` | L6 | Consorzio Casa Protetta Dottor Ellenio Silva | `casaprotetta.elleniosilva@legalmail.it` | Via Sant'antonio Maria Gianelli, 2, 29022 |
| `crdaq` | C14 | Comminissione Regionale Disciplina | `coredi.abruzzo@postacertificata.notariato.it` | Via Savini, 25, 67100 |
| `crdba` | C14 | Commissione Regionale di Disciplina Puglia | `coredi.puglia@postacertificata.notariato.it` | Via Calefati, 89, 70122 |
| `crdca` | C14 | Co.Re.Di. Commissione Amministrativa Regionale di Disciplina per La Circoscrizione Territoriale della Toscana | `coredi.toscana@postacertificata.notariato.it` | Via Dei Renai, 23, 50125 |
| `crdsvc` | L1 | Consorzio Riunito Delle Strade Vicinali del Comune di Civitella Paganico | `strade.civitellapaganico@pec.it` | Via I Maggio, 4, 58045 |
| `crga` | L34 | Casa di Riposo Giuseppe Altobelli | `cdr.altobelli@pec.it` | Viale Di Montecastello, 2, 01030 |
| `crmsa` | C14 | Collegio Regionale Maestri di Sci Abruzzo | `mdsabruzzo@legalmail.it` | Via Montenero, 43, 67039 |
| `crs` | L37 | Cooperazione e Rinascita Srl | `cooperazionerinascita@pec.it` | Via Manin, 23, 84092 |
| `crsge` | L34 | Casa di Riposo San Giuseppe Ex Ipab | `casariposos.giuseppe@pec.it` | Via Del Seminario, 58, 01021 |
| `csdg` | L36 | Consorzio Sentieri del Grano | `SENTIERIDELGRANO@LEGALMAIL.IT` | Piazza Del Ducato, 1, 09040 |
| `csgir` | L1 | Commissario Straordinario del Governo per Il Recupero Delle Balle di Rifiuti Plastici Pressati Perse dalla Motonave Ivy Nelle Acque del Golfo di Follonica | `commissario.caligiore@pec.minambiente.it` | Via Cristoforo Colombo,44, 00147 |
| `csim` | L47 | Commissario Straordinario per Il Mose | `commissario.mose@pec.it` | Via Piacenza , 3, 00184 |
| `cslmd` | L1 | Consorzio Stradale per La Manutenzione Delle Strade Vicinali del Comune di Capranica | `consorzio.capranica@pec.it` | C.so Francesco Petrarca, 40, 01012 |
| `cslrams` | L1 | Commissario Straordinario per La Realizzazione dell'Acquedotto Molisano Centrale | `SEGRETERIA.C.ACQUEDOTTOMOLISANO@PEC.IT` | Via Marchese Campodisola, 21, 80133 |
| `csmp` | L34 | Conservatorio Santa Maria della Pieta | `conservatoriosantamariadellapieta@pec.it` | Via Santa Maria Della Pieta, 24, 80067 |
| `cspaa` | L34 | Centro Servizi alla Persona Antonietta Aldisio | `cssap.aldisio@pec.buffetti.it` | Via Europa, 50, 93012 |
| `csr` | L1 | Consorzio Strada Rebaude | `consorziorebaude@pec.it` | Piazza Vittorio Emanuele II, 2, 10024 |
| `csrad` | L6 | Consorzio Smaltimento Rifiuti Av2 | `consorzio.av2@pec.it` | Via Cannaviello, 57, 83100 |
| `csrav1` | L6 | Consorzio Smaltimento Rifiuti Avellino 1 | `consorzio.av1@pec.it` | Via Cannaviello, 57, 83100 |
| `csrtsp` | L37 | Consorzio Smaltimento Rifiuti | `consorziosmaltimentorifiuti@cgn.legalmail.it` | P.za Umberto I N. 1, 63814 |
| `cssasil` | L34 | Centro Servizi Socio Assistenziali Sanitari Ipab Lercaro | `l1279.2025alessandria@pecliquidazioni.it` | Strada Lercaro, 3, 15076 |
| `cstib` | L36 | Consorzio Sviluppo Tecnologie Internet Banda Larga Delle Valli Joniche | `comunepagliara@pec.it` | Via R. Margherita, 92, 98020 |
| `csvcpf` | L1 | Consorzio Strade Vicinali del Comune di Pavullo nel Frignano | `stradevicinalipavullo@pec.it` | Piazza Monteccucoli, 1, 41026 |
| `csvdr` | L1 | Consorzio Strada Vicinale Dei Rimorti | `RIMORTI@PEC.CETTI.IT` | Via Del Rio Morto Di Sopra 16, 50051 |
| `csvlc` | L1 | Consorzio Strada Vicinale Li Curuneddi Tronco B e Sue Diramazioni | `consorziolicurunedditroncob@pec.it` | Largo Budapest, 7/a, 07100 |
| `csvms` | L1 | Consorzio Strada Vicinale Monticello Selga | `consorziostradamonticelloselga@arubapec.it` | Piazza Garibaldi, 1, 43036 |
| `csvspa` | L37 | Cosev Servizi Spa | `cosevservizi@pcert.postecert.it` | Via F. Petrarca, 64015 |
| `csvssdl` | L1 | Consorzio Strada Vicinale Serra Secca Don Lorenzo | `consorzioserraseccadonlorenzoss@pec.it` | Largo Budapest, 7 A, 07100 |
| `ctsd` | C14 | Consiglio Territoriale degli Spedizionieri Doganali della Sicilia | `ccsdpa@pec.cnsd.it` | Via Francesco Crispi, 286, 90133 |
| `cusvill` | L1 | Consorzio Utenti Strade Vicinali Villata | `cusvvillata@pec.it` | Piazza A. Gastaldi, 14, 13010 |
| `cvcnvb` | L1 | Consorzio Via Case Nuove e Via Buonasera | `consorziocasenuovebuonasera@legalmail.it` | Via Mazzini N.4, 40026 |
| `cw4ffwqz` | SA | consorzio stradale conce ripolo sodi | `concesodiripolo@pec.libero.it` | Via marconi, 9, 58033 |
| `d3zdp3w4` | SA | Società Trasporti Provinciale Bari | `SEGRETERIA.BARI@PEC.STPSPA.IT` | Via Barletta 156, 76125 |
| `dfno` | C14 | Ordine Dei Dottori Agronomi e Dei Dottori Forestali Delle Province di Novara e Vco | `protocollo.odaf.novara-verbaniacusioossola@conafpec.it` | Corso Vercelli, 120, 28100 |
| `dgmqg724` | C14 | Ordine Provinciale dei Medici Veterinari di Vibo Valentia | `ordinevet.vv@pec.fnovi.it` | San Domenico Savio n. 12, 89900 |
| `dhuz5yc6` | SAG | EGEA ACQUE S.p.A. | `egeacque@pec.egea.it` | Via Vivaro, 2, 12051 |
| `dirl388` | L1 | Dir. Infr. R.L. Soggetto Delegato Ocdpc 388 2016 Sisma 2016 | `soggettoattuatoresisma2016@pec.regione.lazio.it` | Via Cristoforo Colombo, 212, 00147 |
| `dlxebn8b` | L1 | Azienda Speciale A.S. Paistom | `aspaistom@pec.it` | Via Vittorio Emanuel 1, 84047 |
| `dqxs37mh` | L18 | UNIONE DEI COMUNI LOMBARDI ALTO PAVESE - TERRE DEI VISCONTI E DEGLI SFORZA | `unione.comunialtopavese@pec.it` | Via PALMIRO TOGLIATTI, 12, 27012 |
| `dsh36rfv` | L37 | Fondazione ITS Agroalimentare | `itsagroalimentare@pec.it` | Via Saffi, 49, 01100 |
| `dta2bfh2` | SA | CEMADIS SRL | `orinvest@pec.it` | Via DEL CAMPO, 12/1, 16124 |
| `dtemi` | L10 | Destinazione Turistica Emilia | `dtemilia@pec.it` | Via Martiri Della Liberta, 15, 43123 |
| `dtvipc8d` | L37 | I.T.S. Angelo Rizzoli per le Tecnologie dell' Informazione e della Comunicazione | `itsangelorizzoli@legalmail.it` | Piazza Castello, 28, 20121 |
| `dxcphh6z` | L37 | Fraternita Sistemi IS SCS | `protocollo@pec.coopsistemi.it` | Via Nisida, 7, 25125 |
| `ea_076` | L36 | Ex Apofil | `giuseppe.romaniello@pec.basilicatanet.it` | Potenza, 85100 |
| `eah5y8x8` | SA | ASD ACADEMY LUCCHESE | `asdacademylucchese@pec.it` | Via Via dello Stadio snc, 55100 |
| `ebfa` | L34 | Ente di Beneficenza Fondazione Agosti | `fondazione.agosti@pec.it` | Piazza L. Cristofori, 16, 01022 |
| `ecsrl` | L37 | E'-comune S.R.L. | `ecomune@pec.it` | Via Dante, 44, 08100 |
| `ek7jbb69` | L37 | Acea Ato 2 s.p.a. | `acea.ato2@pec.aceaspa.it` | Piazzale Ostiense 2, 00154 |
| `enlcl` | C3 | Ente Nazionale per La Cellulosa e La Carta in Liquidazione | `encc@legalmail.it` | Via Alessandria 220, 00198 |
| `eq30lf00` | L47 | Commissario Straordinario D.P.C.M. 13 maggio 2025 | `CommissarioStraordinarioSIN@pec.stoppanicogoleto.it` | Via Rati 66, 16016 |
| `erdu2byw` | SA | Casa dei Musicisti | `casamusicisti@pec.it` | Piazza Buonarroti 29, 20149 |
| `esbla` | L34 | Elisabetta e Sara Bottai Lekie Azienda Pubblica di Servizi alla Persona | `aspbottailekie@pec.it` | Via F. Campana, 18, 53034 |
| `escbc` | L37 | E.S.Co Bim e Comuni del Chiese S.P.A. | `escocom@pec.it` | Via Oreste Baratieri, 11, 38083 |
| `f133wgip` | L18 | AREA URBANA FUNZIONALE DI AGRIGENTO | `fua.agrigento@pec.it` | Piazza Pirandello 35, 92100 |
| `f1epyeng` | L37 | DAMIANI COSTRUZIONI SRL | `DAMIANICOSTRUZIONILT@PEC.IT` | Piazzale PRAMPOLINI 49, 04100 |
| `f2o7ptm8` | SA | CONSORZIO INTERUNIVERSITARIO ALMALAUREA | `consorzio@pec.almalaurea.it` | VIALE MASINI 36, 40126 |
| `f526panq` | L47 | COMMISSARIO STRAORDINARIO DEL GOVERNO PER LA BONIFICA AMBIENTALE E RIGENERAZIONE URBANA AREA RIN "ARSENALE MILITARE E AREA MILITARE CONTIGUA MOLO CARBONE" NELL'ISOLA DI LA MADDALENA | `commissario.areainteressenazionale.lamaddalena@pec.regione.sardegna.it` | Viale Trento n. 69, 09123 |
| `f75zqk7d` | SA | Associazione Milano & Partners | `milanosmartcity@legalmail.it` | Piazza della Scala 2, 20121 |
| `f7dfhc25` | L6 | Consorzio "Il Cammino della Pace" | `camminodellapace@pec.it` | Piazza Mazzini 5, 66036 |
| `f9bhu0at` | L18 | Unione dei comuni Paternò-Ragalna | `unionepaternoragalna@pec.it` | Piazza DELLA REGIONE N.4, 95047 |
| `fccrm` | L37 | Fondazione per La Cultura Castelli Romani | `FONDAZIONE@PEC.CULTURACASTELLI.IT` | Viale G. Mazzini, 12, 00045 |
| `fcsrl` | SA | Futuro & Conoscenza S.R.L. | `fatturepassive@pec.futuroeconoscenza.it` | Via Salaria, 691, 00138 |
| `fdeaq2vp` | L15 | CONSORZIO PER GLI STUDI UNIVERSITARI IN VERONA IN LIQUIDAZIONE | `consorzioperglistudiuniversitariinverona@legalmail.it` | Via VIA DELL'ARTIGLIERE 8, 37129 |
| `fdoddaba` | C14 | Federazione Degli Ordini Dei Dottori Agronomi e Dei Dottori Forestali della Basilicata | `protocollo.odaf.basilicata@conafpec.it` | Via Ascanio Branca, snc, 85100 |
| `fdq0363d` | L37 | CONSORZIO FORESTALE DEI COMUNI DELLE VALLI CHISONE E GERMANASCA | `consorziochisonegermanasca@legalmail.it` | VIA ROMA 22, 10063 |
| `fipcm` | L34 | Fondazione Istituzione Povera Costante Maria | `costante.maria@pcert.postecert.it` | Via Beata Lavinia Sernardi, 9, 63066 |
| `fmcjo4qq` | L18 | Unione dei Comuni di Roverè, Velo e San Mauro | `unionervs@pec.it` | Piazza San Vitale 41/b, 37028 |
| `fmgc1alf` | C14 | Ordine Regionale della Professione Sanitaria di Fisioterapista dell'Abruzzo | `abruzzo.ofi@pec.fnofi.it` | Via Cavalieri di Vittorio Veneto 66, 67051 |
| `fojwcqb8` | L1 | ASUC TUENNO | `asuctuenno@pec.it` | Piazza Liberazione, 38019 |
| `fpacc` | L37 | Fondazione di Partecipazione Arte e Cultura Citta' di Velletri | `fondarc@pec.it` | Piazza Cesare Ottaviano Augusto, 00049 |
| `frdo` | C14 | Federazione Regionale Degli Ordini Dei Dottori Agronomi e Dei Dottori Forestali della Sardegna | `protocollo.odaf.sardegna@conafpec.it` | Via Delle Miniere, 39, 09030 |
| `frodadfl` | C14 | Federazione Regionale Degli Ordini di Dottori Agronomi e Dottori Forestali del Lazio | `protocollo.odaf.lazio@conafpec.it` | Via Livenza, 6, 00198 |
| `ft0sumsk` | L37 | ISTITUTO TECNICO SUPERIORE ITS PER L'AREA NUOVE TECNOLOGIE PER IL MADE IN ITALY - SISTEMA AGROALIMENTARE | `fondazioneiridea@pec.it` | Piazza XV MARZO, 87100 |
| `fw96ao8l` | L37 | G.LM. RISTORAZIONE SRL | `GLMRISTORAZIONE@PEC.IT` | Traversa SCHITO,33, 80053 |
| `g3qm24yk` | SA | FONDAZIONE CASA DEI BAMBINI SANGIORGIO GUALTIERI | `fondazionegualtieri@pec.it` | Via SAN PIETRO 37, 95031 |
| `galml` | L37 | Gruppo di Azione Locale Monti Lepini | `galmontilepini@pec.it` | Via Umberto I, 04018 |
| `galsc` | L37 | G.A.L. Serre Calabresi | `galserrecalabresi@pec.it` | Contrada Foresta, 88064 |
| `ggi49ko7` | L47 | COMMISSARIO DELEGATO OCDPC 1120-24 OCDPC 1100 E 1109-2024 ZONA EMILIA ROMAGNA | `OCDPC1100@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `gmb` | L37 | Gmb Srl Societa' di Servizi del Collegio Geometri della Provincia di Monza e della Brianza | `gmb.srl@pec.it` | Via G. Ferrari 39, 20900 |
| `go2b9cdp` | SA | CONSTRUCTA SRL | `constructasrl@arubapec.it` | Via Francesco de Bartolo, 76125 |
| `gsic_107` | SA | Gal Sulcis Iglesiente, Capoterra e Campidano di Cagliari | `galsulcisiglesiente@pec.it` | Via Aldo Moro S.n.c., 09010 |
| `gtlocr` | L37 | Gal Terre Locridee Soc. Coop. Cons. a R.L. | `galterrelocride@pec.it` | Piazza V. Veneto, 89048 |
| `gtn9o8pu` | L47 | OCDPC 1078_2024 | `ocdpc1078_2024@pec.protezionecivilesicilia.it` | Via G. ABELA N. 5, 90141 |
| `h3y12wpo` | L47 | COMMISSARIO STRAORDINARIO DEL GOVERNO PER LA ZES CAMPANIA | `commissariozescampania@pec.agenziacoesione.gov.it` | Via Sicilia n. 162, 00187 |
| `heyuh7rf` | L37 | Seminario Vescovile di Verona | `seminariovr@pcert.postecert.it` | Via Seminario, 8, 37129 |
| `hg2pmavy` | L37 | SOGEA S.R.L. | `SOGEASRL@PEC.IT` | Via SQUILLACI,2, 95131 |
| `hk16u1as` | L1 | COMMISSARIO DELEGATO ORDINANZA CAPO DIPARTIMENTO PROTEZIONE CIVILE N. 749/2021 | `commissario_delegato@pec.regione.vda.it` | Via Promis, 2/A, 11100 |
| `hl4mklqt` | SA | Coutenza del Canale Ex Demaniale Pertusata | `coutenza.pertusata@pec.it` | Piazza Caduti per la Libertà 14, 12042 |
| `hvb8za1t` | SA | UDINE MERCATI S.R.L. | `UDINEMERCATI@PEC.IT` | PIAZZALE DELL'AGRICOLTURA 16, 33100 |
| `i3qqcnaf` | L37 | Energy Green City S.P.A | `romagas@legalmail.it` | clitunno, 00198 |
| `i50eoozn` | L47 | COMMISSARIO STRAORDINARIO PER LA REALIZZAZIONE DELL'INTERVENTO "LINEA 2 DELLA METROPOLITANA DELLA CITTA' DI TORINO" | `commissario.metro2.torino@pec.governo.it` | Corso INGHILTERRA N. 7, 10138 |
| `i9puifzg` | SA | Associazione Istituto di Culture Mediterranee | `icmlecce@pec.it` | Viale Gallipoli, 30, 73100 |
| `iafg` | L34 | Istituto dell'Addolorata | `ASPADDOLORATA@LEGALMAIL.IT` | Via Barra, 35, 71121 |
| `iaima` | L34 | Ipab Asilo Infantile Monumento Ai Caduti | `scuolamaternamotta@pec.cgn.it` | Borgo Girolamo Aleandro 25, 31045 |
| `iazhib7o` | L34 | AZIENDA PUBBLICA DI SERVIZI ALLA PERSONA REGIONALE ISTITUTI RIUNITI DEL LAZIO | `asp@pec.istitutiriunitilazio.it` | Via Annunziata, 21, 04024 |
| `ieaa` | C7 | Istituto Educativo Assistenziale Aletta | `istitutoaletta@pec.it` | Piazza Degli Studi, 2, 96016 |
| `ieb` | L34 | Istituto E. Baratta | `ipabebaratta@pec.it` | Piazza Santa Chiara, 7, 04015 |
| `iigst` | L34 | Ipab Ignazio e Giovanni Sillitti | `ipabsillitti@pec.it` | Via Progresso N.5, 92023 |
| `ijep822y` | SAG | Gespa S.p.A. | `gespa.spa@legalmail.it` | Via Gidino, 6, 37066 |
| `ilvpszoy` | L37 | FONDAZIONE RETE PROFESSIONI TECNICHE PROVINCIA DI RIMINI | `fondazionerpt.rimini@pec.it` | Corso D'AUGUSTO 231, 47921 |
| `ioi0n13j` | L37 | Mood & Progress | `associazionemoodeprogress@pec.it` | Via Alcide De Gasperi 57 a, 90010 |
| `ipabsmai` | L34 | I.P.A.B. Scuola Materna Asilo Infantile | `asilorecoaro@pec.it` | Via Asilo, 6, 36076 |
| `iren` | L37 | Iren Acqua S.P.A. | `irenacqua@pec.gruppoiren.it` | Via Dei Santi Giacomo E Filippo, 7, 16122 |
| `iscmss` | C7 | Istituzione Scuola Civica di Musica di San Sperate | `scuolacivicadisansperate@pec.it` | Via Sassari, 3 Presso Comune, 09026 |
| `isrra` | L37 | Impianti S.R.R Ato 4 Caltanissetta Provincia Sud | `IMPIANTISRR@PECODP.IT` | Piazzetta Don Pedro Altariva 1, 93016 |
| `istsc_vcis016008` | L33 | ISTRUZIONE SECONDARIA SUPERIORE - VINCENZO LANCIA | `vcis016008@pec.istruzione.it` | Via G Marconi 8, 13011 |
| `jb7t7jpz` | L18 | DISTRETTO REGIO DI CASERTA C01 | `distrettoregiocaserta@pec.it` | Piazza vanvitelli, 81100 |
| `jh6oojq4` | SA | CONSORZIO EDILIZIO SANT'ANNA 2 | `consorzio.santanna2@pec.it` | Via LORENZO VITALE 8, 70126 |
| `ji85t6mi` | L47 | COMMISSARIO DELEGATO OCDPC 1120-24 OCDPC 1095-24 ZONA EMILIA ROMAGNA | `OCDPC1095@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `jkqjkagq` | SA | Fondazione Museo della Shoah | `museodellashoah@legalmail.it` | Via Via Nomentana 70, 00162 |
| `jn7thmb2` | L47 | OCDPC 789_2021 | `ocdpc789_2021@pec.protezionecivilesicilia.it` | Via Gaetano Abela 5, 90141 |
| `jpzrx8nt` | L37 | CAMPAGNATICO SERVIZI SRL | `campagnaticoservizi@pec.it` | Piazza GARIBALDI 12, 58042 |
| `jtdwhrat` | L34 | ASP Tuscia | `asptuscia@pec.it` | Piazza LUIGI CRISTOFORI 16, 01022 |
| `jur0h58k` | L18 | UNIONE DEI COMUNI DELL'AREA URBANA FUNZIONALE DELLA SICILIA CENTRALE | `protocollo@pec.fuasiciliacentrale.it` | Corso CORSO UMBERTO I, 134, 93100 |
| `jwuqlh5u` | L6 | CONSORZIO FORESTALE ALTA VALLE TROMPIA | `consorzioaltavt@legalmail.it` | via Giacomo Matteotti 327, 25063 |
| `k1jycpmr` | L37 | ASM TERNI S.p.A. | `asmternispa@legalmail.it` | Via Bruno Capponi, 100, 05100 |
| `k2p1cfs2` | SA | CONSORZIO IRRIGUO BEALERA MAESTRA | `bealera.maestra@pec.it` | Via Roma 101, 12041 |
| `k30du9fs` | L47 | SOGGETTO RESPONSABILE OCDPC 1123-24 OCDPC 1120-24 OCDPC 1087-24 OCDPC 872-22 ZONA EMILIA ROMAGNA | `OCDPC872@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `k8e3zoah` | L37 | STITUTO TECNICO SUPERIORE LOMBARDO PER LE NUOVE TECNOLOGIE MECCA NICHE E MECCATRONICHE | `itslombardiameccatronica@pec.it` | Viale Matteotti n. 425, 20099 |
| `kaspa` | L37 | Kalat Ambiente S.P.A. in Liquidazione | `kalatambiente@pec.it` | Via Giuseppe Liverani,13 -15, 95042 |
| `kelkmkc1` | SA | TAORMINA SOCIAL CITY | `taorminasocialcity@pec.comune.taormina.me.it` | Corso CORSO UMBERTO I, 98039 |
| `kh36a2ap` | L37 | Fondazione Its Efficienza Energetica Sardegna | `FONDAZIONEITSMACOMER@DIGITALPEC.COM` | Via Milano snc, 08015 |
| `kjf8jbij` | L47 | COMMISSARIO STRAORDINARIO DEL GOVERNO PER LA FIERA DEL LIBRO DI FRANCOFORTE | `commissario.italyfrankfurt2024@pec.cultura.gov.it` | Via SALARIA 280, 00199 |
| `kml594ng` | L47 | OCDPC872_2022 | `ocdpc872_2022@pec.protezionecivilesicilia.it` | Via Gaetano Abela n. 5, 90141 |
| `kpbraqw7` | L37 | ENEL GRIDS S.R.L. | `enelgin@pec.enel.it` | Via Ombrone 2, 00198 |
| `kptoxfrb` | L33 | ISTITUTO COMPRENSIVO PESSINA VITALE BARNABA | `bric84300q@pec.istruzione.it` | Piazza Italia 11, 72017 |
| `kqrqf6qa` | L18 | UNIONE DEI COMUNI COLLINA MATERANA | `info@pec.unionecollinamaterana.it` | VIA ALCIDE DE GASPERI, 39, 75018 |
| `kttxepsd` | L37 | COGESER ENERGIA S.R.L. | `cgvendite@legalmail.it` | Via MARTIRI DELLA LIBERTA' N. 18, 20066 |
| `kuhe68jm` | L47 | SOGGETTO RESPONSABILE OCDPC 1120-24 OCDPC 1087-24 OCDPC 1053-24 OCDPC 906-22 ZONA EMILIA ROMAGNA | `OCDPC906@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `kvvypq6g` | L37 | Posta Trade srl | `postaltradesrl@legalmail.it` | Calata San Marco,13, 80133 |
| `l71ljsar` | L37 | Valle Camonica Servizi srl | `appalti@pec.vallecamonicaservizi.it` | Via Rigamonti, 25047 |
| `lhp700i2` | SA | STUDIO TECNICO CASTELLI S.R.L. | `info@pec.studiotecnicocastelli.eu` | via Monteggia , 38, 21014 |
| `lj17o4ix` | L36 | Consorzio ATO Rifiuti Catanzaro | `atorifiuticatanzaro@legalmail.it` | Via Alberghi n.3, 88100 |
| `lkojwn3h` | SA | ALI IMMOBILIARE S.R.L. | `aliimmobiliare@legalmail.it` | Via OLANDA 2, 35127 |
| `llhztm6r` | L37 | FONDAZIONE ITS MA.DE ACADEMY | `itsmadeacademy@pec.it` | Via BOSCO DI CAPODIMONTE, 80131 |
| `lliyqz36` | L47 | "SOGGETTO RESPONSABILE OCDPC 1160- 24 OCDPC 1120-24 OCDPC 1087-24  OCDPC 992-23 ZONA EMILIA ROMAGNA" | `OCDPC992@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `llkgrrqc` | SA | SEVEN ESTATE s.r.l. | `sevenestatesrl@legalmail.it` | Via Venezia 18, 31046 |
| `lln0mqsr` | SA | CONSORZIO IRRIGUO DI SECONDO GRADO VALLE GESSO | `consorziovallegesso@pec.it` | Via Roma 101, 12041 |
| `lo3xfuch` | L47 | Commissario di Governo per il dissesto idrogeologico DL 133-14 77-21 | `CommissarioDL133@postacert.regione.emilia-romagna.it` | Viale della Fiera, 8, 40127 |
| `lqw8xtif` | L37 | CONSORZIO CFA SOCIETA' COOPERATIVA SOCIALE | `formulambiente@pec.it` | Via FOSSALTA 344, 47522 |
| `lqwghoat` | L37 | PROSERVICE SOCIETA' PER AZIONI | `proservicespa@pec.fofi.it` | Via Palestro n. 75, 00185 |
| `lqztow81` | L37 | FONDAZIONE ITS MOBILITA' SOSTENIBILE TRASPORTI CATANIA | `fondazione@pec.itscatania.it` | Viale ARTALE ALAGONA 99, 95126 |
| `lr32ek9o` | SA | I.S.P.E SALENTO S.R.L. | `ispesalentosrl@pec.it` | Via SAN LAZZARO N. 15, 73100 |
| `lyo1b6g5` | L37 | Enel Italia SPA | `enelitalia@pec.enel.it` | Via Boccherini 15, 00198 |
| `m0yjkclh` | L37 | AZIENDA SPECIALE ISOLA DI PONZA | `asisoladiponza@pecimprese.it` | Corso CARLO PISACANE, 04027 |
| `maj6tnpq` | L37 | R.T. GAS & POWER S.R.L. | `rtgasepowersrl@pec.it` | Via FRANCESCO MOROSINI 34, 80125 |
| `mcs4xzb0` | L37 | CITY GREEN LIGHT SRL | `citygreenlight@legalmail.it` | VIA G. ZAMPIERI 15, 36100 |
| `mcsrl` | L37 | Marciana Civitas S.R.L. | `marcianacivitas@pec.sag-srl.it` | Via Santa Croce, 34, 57030 |
| `mgv2xfb1` | SA | INTERPORTO PADOVA S.P.A. | `interportopadova@cert.legalmail.it` | Galleria Spagna n.35, 35127 |
| `mi8mmmju` | L18 | UNIONE DEI COMUNI MONTAGNA AQUILANA | `unionecomunimontagnaaquilana@pec.it` | Via CAVOUR 43/A, 67021 |
| `mmms` | L37 | Massa Marittima Multiservizi Srl | `FARMACIA.COMUNALE@LEGALMAIL.IT` | Piazza Garibaldi, 10, 58024 |
| `mmyg19fo` | L37 | Assist spa | `assist.spa@pec.it` | Strada Strada Torino 34/36, 10092 |
| `mzjz0sfz` | SA | FONDAZIONE ANDORA BORGO CASTELLO | `borgocastelloandora@cert.comunediandora.it` | Via CAVOUR, 17051 |
| `n953rpqa` | SA | MERIDIANA S.R.L. | `meridianasrlbo@pec.it` | Via ISONZO 69, 40033 |
| `n9zfk66n` | SA | COUTENZA CANALI EX DEMANIALI DELLA PIANURA CUNEESE CONS IRR | `coutenzacanaliexdem@pec.it` | Via Circonvallazione n. 44, 12045 |
| `nbcjj9jk` | L37 | Fondazione Cadmo ITS ICT | `segreteria@pec.itscadmo.it` | Via Largo Cardillo, snc, 88100 |
| `ne8urc5k` | L47 | SOGGETTO RESPONSABILE OCDPC 1120-24 OCDPC 1087-24 OCDPC 940-22 ZONA EMILIA ROMAGNA | `OCDPC940@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `nfhtle7i` | L34 | CENTRO EGIZIANO GIGLIOLI - A.P.S.P. | `centrogiglioli@arubapec.it` | Via DELLO SPEDALE N. 3, 50052 |
| `njhfhque` | SAG | CALORE VERDE SRL | `caloreverde@legalmail.it` | Via TECO 1, 12078 |
| `nxt1a67p` | L47 | SOGGETTO RESPONSABILE OCDPC 1149-25 OCDPC 1120-24 OCDPC 1087-24 OCDPC 966-23 ZONA EMILIA-ROMAGNA | `OCDPC966@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `nyiomchl` | L18 | UNIONE MUSSOMELI VALLE DEI SICANI | `PROTOCOLLO@PEC.MUSSOMELIVALLEDEISICANI.IT` | Piazza DELLA REPUBBLICA 1, 93014 |
| `o1bm07pc` | L33 | ISTITUTO D'ISTRUZIONE SUPERIORE "M.PANTALEONI-M.BUONARROTI" | `rmis13100l@pec.istruzione.it` | Via BRIGIDA POSTORINO 27, 00044 |
| `o81l5afy` | L37 | GLOBAL POWER PLUS S.R.L. | `info@pec.globalpowerplus.it` | Corso PORTA NUOVA 127, 37122 |
| `oaddoeaj` | SA | GRUPPO RITMO SRL | `grupporitmo.garetelematiche@pec.it` | Viale Vincenzo Randi 45, 48121 |
| `ocb` | L34 | Ospedale Civile di Busca | `contabilitaospedalebusca@pec.it` | Piazza Regina Margherita, 10, 12022 |
| `ocdpa` | L47 | Ocdpc 558 2018 Co Drpc | `ocdpc558_2018@pec.protezionecivilesicilia.it` | Via Gaetano Abela, 90141 |
| `ocdpc37` | L4 | Ocdpc 37-2013 | `ocdpc37.2013@certmail.regione.sicilia.it` | Via Gaetano Abela, 5, 90141 |
| `ocdpc71` | L4 | Ocdpc 71-2013 | `ocdpc71.2013@certmail.regione.sicilia.it` | Via Gaetano Abela, 5, 90141 |
| `odafar` | C14 | Ordine Dottori Agronomi e Dottori Forestali della Provincia di Arezzo | `protocollo.odaf.arezzo@conafpec.it` | Viale Santa Margherita 80, 52100 |
| `odclcch` | C14 | Ordine Dei Consulenti del Lavoro Consiglio Provinciale di Chieti | `ordine.chieti@consulentidellavoropec.it` | Via Spezioli, 16, 66100 |
| `odcpm` | C14 | Ordine Dei Chimici della Provincia di Mantova | `ordine.mantova@pec.chimici.org` | Via F. Da Paola, 6, 46100 |
| `oddadfci` | C14 | Ordine Dei Dottori Agronomi e Dei Dottori Forestali della Provincia di Campobasso Ed Isernia | `ordineagronomiforestalicbis@pec.it` | C-o Dipartimento A.a.a. - Via De Sanctis, Snc, 86100 |
| `oddadkr` | C14 | Ordine Dei Dottori Agronomi e Dottori Forestali della Provincia di Crotone | `protocollo.odaf.crotone@conafpec.it` | Via A. Cefaly, 1bis, 88900 |
| `oddafr` | C14 | Ordine Dei Dottori Agronomi e Forestali di Rieti | `protocollo.odaf.rieti@conafpec.it` | Piazza Vittorio Emanuele II, 17, 02100 |
| `odpca` | C14 | Ordine Dei Dottori Agronomi e Dei Dottori Forestali della Provincia di Cagliari | `protocollo.odaf.cagliari@conafpec.it` | Via Delle Miniere, 39, 09030 |
| `oihklt5m` | SA | A.F.V.G. SECURITY S.R.L. | `afvgsecurity@legalmail.it` | Via Aquileia 46, 34077 |
| `om2gh77a` | L37 | ISTITUTO TECNICO SUPERIORE PER LE TECNOLOGIE INNOVATIVE PER I BENI E LE ATTIVITA' CULTURALI - TURISMO - MARCHE | `itsturismomarche@pec.it` | Via Nolfi, 37, 61032 |
| `om75c900` | L37 | CATERING SRL | `catering@pec.impresecatania.it` | Viale CATANIA 60, 95034 |
| `omvt` | C14 | Ordine Medici Veterinari Trieste | `ordinevet.ts@pec.fnovi.it` | Casella Postale, 3012, 34143 |
| `on5yoih6` | L38 | Comitato di Gestione Provvisoria Parco Nazionale del Matese | `parcomatese.comitato@pec.matesepark.it` | Via Figulantina, 81016 |
| `ont6uh2n` | L18 | UNIONE DEI COMUNI DEL CORLEONESE E DEL TORTO | `protocollo@pec.unionecomunicorleonesetorto.it` | Piazza GARIBALDI, 90034 |
| `oo0o6edm` | L37 | Civitavecchia Servizi Pubblici S.r.l. | `civitavecchiaservizipubblicisrl@legalmail.it` | Via Terme di Traiano 42, 00053 |
| `ooh4ihc9` | L37 | Sistema Cilento Scpa | `sistemacilento@pec.it` | Via Filippo Palumbo, 84078 |
| `oorf355i` | L37 | Fondazione ITS Moda Campania | `itsmodacampania@pec.it` | Piazzetta Mondragone 18, 80132 |
| `op8adqa2` | L37 | AZIENDA SPECIALE CONSORTILE FIERA DI MORCONE E DELL'ALTO TAMMARO | `AZIENDASPECIALEFIERA@ASMEPEC.IT` | Via PIANA 131, 82026 |
| `opcd` | L34 | Opera Pia Casa Diodorea | `amministrazione@pec.casadiodorea.it` | Via Orfanotrofio, 6, 94011 |
| `opiaomg` | L34 | Opera Pia Istituto Agricolo Operaio Michele Grimaldi | `assap.grimaldi@pcert.postecert.it` | Via Cannizzaro, 7, 97015 |
| `orwzkgwm` | L18 | UNIONE BASSA OVEST PARMENSE | `unionebassaovestparmense@pec.it` | Piazza Mazzini n. 10, 43017 |
| `p5xj4csf` | L37 | Ambito territoriale di caccia n. 5 mantova | `ambito5@pcert.postecert.it` | Vicolo II ospedale,1, 46046 |
| `page` | L38 | Parco Archeologico di Gela | `parco.archeo.gela@pec.it` | Corso Vittorio Emanuele, 2, 93012 |
| `pakcd` | L38 | Parco Archeologico di Kamarina e Cava D'Ispica | `parco.archeo.kamarina@legalmail.it` | Via Via Cristoforo Colombo,2, 97100 |
| `pasevt` | L38 | Parco Archeologico e Paesaggistico di Siracusa, Eloro, Villa del Tellaro e Akrai | `parcoarcheologico.siracusa@legalmail.it` | Viale Teocrito, 66, 96100 |
| `pc738m3y` | SAG | ALTA LANGA SERVIZI S.p.A. | `alsespa@legalmail.it` | Via Umberto I, 1, 12060 |
| `pd0ajk0l` | SAG | Azienda Mobilità e Trasporti S.p.A. | `amt.spa@pec.amt.genova.it` | Via Leonardo Montaldo 2, 16137 |
| `pegaso` | L37 | Pegaso Soa Spa | `pegasosoa@postecert.it` | Via Santa Maria Alla Porta, 9, 20123 |
| `pimjc` | L34 | Pio Istituto Maria Jolanda Canzoneri | `istitutocanzoneri@pec.it` | Via San Martino, 5, 90034 |
| `pjpfhwk6` | L47 | Commissario Straordinario Collegamento Stradale Cisterna Valmontone e Relative Opere Connesse | `commissario@pec.commissariocisternavalmontone.it` | Via Gino Capponi 76, 00179 |
| `pnsxfsn2` | L47 | COMMISSARIO PER L'EDILIZIA SANITARIA DELLA REGIONE CALABRIA | `commissario.ediliziasanitaria@pec.regione.calabria.it` | Viale Europa, 88100 |
| `pohg3kr4` | SAG | Viveracqua S.c.ar.l. | `segreteria@pec.viveracqua.it` | Via Monsignor Giacomo Gentilin 71, 37132 |
| `pps7fe2r` | L47 | Commissario Delegato ex OCDPC 1180/26 Zona Sicilia | `commOCDPC1180_26@legalmail.it` | Via Munter 21, 90145 |
| `pssbg` | L37 | Palosco Servizi Srl | `paloscoservizisrl@pec.it` | P.zza Castello 8, 24050 |
| `pu35rkjt` | L13 | Agenzia per lo sviluppo e la valorizzazione ippica -  ASVI Sardegna | `direzione@pec.asvisardegna.it` | Piazza Duchessa Borgia, n. 4, 07014 |
| `q0txu19m` | L37 | ATC Mobilità e Parcheggi SpA | `atcmp@pec.it` | Via Saffi n. 3, 19126 |
| `q13prxlp` | L37 | COMITATO DI GESTIONE AMBITO TERRITORIALE DI CACCIA N.2 POTENZA | `atc2potenza@pcert.postecert.it` | VIA MESSINA 192, 85100 |
| `q4mv5lc1` | C14 | FEDERAZIONE REGIONALE ORDINI DOTTORI AGRONOMI E DOTTORI FORESTALI DELLA CALABRIA | `protocollo.odaf.calabria@conafpec.it` | VIA GABRIELE BARRIO, 14, 88100 |
| `q8ivcy52` | C14 | ORDINE DEI BIOLOGI DELLA LOMBARDIA | `presidente.ordinebiologilombardia@pec.it` | Strada 1 MILANOFIORI 290, 20090 |
| `q9zru4aw` | SA | AMIR ONORANZE FUNEBRI SRL | `amirof@legal-pec.it` | Via DARIO CAMPANA 59, 47922 |
| `qf4082un` | SA | FUNIVIE MOLISE SPA | `funiviemolise@pec.it` | Piazza PEPE N.13, 86100 |
| `qfiyte9u` | L37 | Fondazione La Locomotiva ETS | `fondazionelalocomotiva@pec.it` | Via Stradella n 38, 41043 |
| `qh4mz3x6` | SA | Chilemi s.r.l. | `chilemisrl@lamiapec.it` | Piazzale Carducci, 20, 48022 |
| `qm9yi6nu` | L37 | AMAIE ENERGIA E SERVIZI S.R.L. | `amaieenergia@pec.it` | Via Quinto Mansuino, 18038 |
| `qq0nbr5f` | SA | INSULA SPA | `appalti.insula@pec.it` | Santa Croce 482, 30135 |
| `qwvqku78` | SA | FONDAZIONE TORRECCHIA VECCHIA | `fondazionetorrecchiavecchia@legalmail.it` | Via Torrecchia Vecchia snc, 04012 |
| `qzv117nl` | SA | IMMOBILIARE DI RHO SRL | `immobiliaredirhosrl@legalmail.it` | Via Montefeltro n. 4, 20156 |
| `r7f28gke` | L37 | BONIFICA MARCHE SERVICE S.R.L | `bonificamarcheservice@certificata.org` | Via DEGLI ABETI N.160, 61122 |
| `ramx7eys` | SA | Diocesi di Carpi | `diocesicarpi@pec.chiesacattolica.it` | Corso Manfredo Fanti 7, 41012 |
| `rar` | L37 | R.A.R. Ravanusa Ambiente e Risorse Srl | `rar.ravanusa@legalmail.it` | Via Montebello, 11, 92029 |
| `rcrpscb` | L47 | Regionemolise Commissario Ricostruzione Post Sisma 2018 | `ricostruzionepostsisma2018@cert.regione.molise.it` | Via Genova, 11, 86100 |
| `rdodv` | L34 | Reclusorio Delle Orfane Delle Vergini | `reclusorioverginimonreale@pec.it` | Via Palermo, 65, 90046 |
| `re5hcpgc` | SA | AZIENDA TRASPORTI AUTOMOBILISTICI FOGGIA | `ataf@cert.comune.foggia.it` | VIA DI MOTTA DELLA REGINA, 71122 |
| `rf7gqbh4` | SA | SOGAER SECURITY SPA SOCIO UNICO | `info@pec.sogaersecurity.it` | Via DEI TRASVOLATORI SN, 09030 |
| `rfskhtxx` | L1 | SOGGETTO RESPONSABILE COMPLETAMENTO INTERVENTI URGENTI OCDPC 700/2020 | `emergenzanovembre2019@pec.regione.lazio.it` | Via CRISTOFORO COLOMBO 212, 00145 |
| `rhlox0l2` | L28 | CONSORZIO INTERUNIVERSITARIO PER L'INGEGNERIA E LA MEDICINA | `coiim@legalmail.it` | Via ROMA 64, 86100 |
| `rjun8vv8` | L37 | FONDAZIONE MAESTRE PIE DELL'ADDOLORATA E.T.S | `amministrazione@pec.fondazionempda.org` | Via TEBALDI 20, 00168 |
| `rm30374g` | S01 | Puglia Valore Immobiliare società di cartolarizzazione SRL | `pugliavaloresrl@pec.it` | Via Via Giovanni Gentile  n. 52, 70126 |
| `rmok3mx8` | C14 | ORDINE DELLA PROFESSIONE SANITARIA DI FISIOTERAPISTA DI MODENA E REGGIO EMILIA | `MODENAREGGIO.OFI@PEC.FNOFI.IT` | Via Enrico Sartori, 6/A, 43126 |
| `rmsac` | L1 | Regione Molise - Soggetto Attuatore Coordin. Attivita' Emergenza Sanitaria Covid-19 | `EMERGENZACOVID19@CERT.REGIONE.MOLISE.IT` | Via Genova 11, 86100 |
| `rozevu2w` | L37 | AZIENDA SPECIALE SARNO SERVIZI INTEGRATI | `aziendaspecialesarnoserviziintegrati@legalmail.it` | Piazza IV NOVEMBRE SNC, 84087 |
| `rp8eqlpe` | L33 | ISTITUTO COMPRENSIVO LUZZI | `csic8a200c@pec.istruzione.it` | Via Chiusa 1, 87040 |
| `rpeohn5s` | L37 | VALLI VARANENSI SRL | `valli.varanensi@arubapec.it` | Via VENANZIO VARANO 3, 62032 |
| `rs3swwdz` | L6 | ASSOCIAZIONE SIBILLINI MOUNTAIN EXPERIENCE | `sibilliniitalyexperience@pec.it` | Via CIRCONVALLAZIONE 43/F, 63858 |
| `rspa` | L37 | Retiambiente S.P.A. | `retiambiente@pec.it` | Piazza Vittorio Emanuele Ii, 2, 56125 |
| `s9ypfbnx` | L18 | UNIONE DEI COMUNI DEL BAIANESE - ALTO CLANIS | `unionedeicomunidelbaianesealtoclanis@pec.it` | Via MUNICIPIO,10, 83020 |
| `sass` | L37 | Sant'Agata Servizi Srl | `segreteriamministrativa@pec.santagataservizi.it` | Piazza Xx Settembre 7, 71028 |
| `scpns` | S01 | Soc. Cons. per La Programmazione Negoziata e Lo Sviluppo dell'Anglona a R.L. | `agenziasviluppoanglona@arubapec.it` | Via E. Toti, 20, 07034 |
| `sh58q9p2` | L37 | Domodossola parking srl | `domodossolaparking@legalmail.it` | via G. Zampieri 15, 36100 |
| `shh785hi` | L47 | OCDPC 976/2023 | `ocdpc976_2023@pec.protezionecivilesicilia.it` | Via Gaetano Abela n. 5, 90141 |
| `sjq24ae4` | SA | Fondazione Enea Tech e Biomedical | `fondazioneeneatech@pec.it` | Via Po 12, 00198 |
| `sjr0ngx6` | L44 | ENTE DI GOVERNO DELL'AMBITO DEL MOLISE | `egammolise@pec.it` | Via VIALE ELENA 1, 86100 |
| `sjrp4qs0` | L33 | ISTITUTO COMPRENSIVO STATALE DE CURTIS - RAGAZZI D'EUROPA | `NAIC8HJ00N@PEC.ISTRUZIONE.IT` | VIA EDUARDO DE FILIPPO, 80013 |
| `slrsg` | S01 | Societa' per La Regolamentazione del Servizio di Gestione Rifiuti S.R.R. A.T.O. Siracusa Provincia | `srrsiracusa@legalpec.me` | Piazza Duomo, 4, 96100 |
| `smc` | L37 | Scuola Materna di Cembra | `cembra@pec.fpsm.tn.it` | Zanotelli, 1, 38034 |
| `spledbf` | L1 | Scuola Professionale per L'Economia Domestica e Agroalimentare Corces e Scuola Professionale per L'Agricoltura Fuerstenburg Con Sede a Burgusio | `fs.fuerstenburg-kortsch@pec.prov.bz.it` | Burgusio, 7, 39024 |
| `splfvo` | L1 | Scuola Professionale per La Frutti- Viti- e Orticoltura Laimburg Con Sede a Vadena | `fs.laimburg@pec.prov.bz.it` | Laimburg, 42, 39051 |
| `sppic` | L1 | Scuola Professionale Provinciale per Il Commercio Turismo e I Servizi Luigi Einaudi | `fp.cts@pec.prov.bz.it` | Via S. Geltrude, 3, 39100 |
| `spplpsh` | L1 | Scuola Professionale Provinciale per Le Professioni Sociali Hannah | `lfs.bz-sozialberufe@pec.prov.bz.it` | Via Wolkenstein, 1, 39100 |
| `sqq0f9zq` | SA | V-reti Gas S.r.l. | `v-retigas@legalmail.it` | Via PALOMABRO,13, 06034 |
| `sscsr` | L37 | Servizi Sociali del Cassinate S.R.L. | `servizisocialisrl@pec.it` | Piazza Luigi Sturzo, 10, 03030 |
| `ssms` | L37 | Santo Stefano Multiservizi S.R.L. | `santostefanomultiservizisrl@pec.it` | Via Domenico Morabito 25, 89057 |
| `suzakx3q` | L37 | 12.12.12 RIPARTENZE PERSONE IN MOVIMENTO S.R.L | `ripartenze@pec.it` | Via LEONE PANCALDO, 37138 |
| `t6hdp5k4` | SA | RISORSE IDRICHE S.p.A. | `risorseidricheto@postecert.it` | Corso XI FEBBRAIO 14, 10152 |
| `t77umgpm` | SA | COMITATO ORGANIZZATORE DEI GIOCHI MONDIALI INVERNALI SPECIAL OLYMPICS TORINO 2025 | `torino2025@pec.it` | Piazza Piemonte 1, 10127 |
| `tbso` | L37 | Trasporti Bergamo Sud Ovest S.P.A. | `tbso@propec.it` | Via Milano, 23, 24046 |
| `ternal` | L37 | Terre Naldi S.R.L. | `terrenaldi@pec.confagricoltura.com` | Via Tebano, 54, 48018 |
| `th8f7atc` | SA | Cervino S.p.A. | `amministrazione.cervinospa@legalmail.it` | Strada bardoney, 11028 |
| `thwu5257` | L37 | Azienda Speciale Multiservizi Pontecagnano Faiano | `ASFARMACIAPONTECAGNANOFAIANO@PEC.IT` | Via M. Alfani, 84098 |
| `tj7e0okq` | SA | SPIAGGIA E MARE SRL | `spiaggiaemaresrl@pec.it` | Via DEI MILLE 62, 44022 |
| `tmyvezwp` | L37 | AMBITO TERRITORIALE DI CACCIA MN3 | `ATC3MN@PEC.IT` | VIA DON MAZZI 109, 46019 |
| `tpg06ene` | C14 | ORDINE DEI BIOLOGI DELLA PUGLIA E DELLA BASILICATA | `protocollo@pec.biologipugliabasilicata.it` | Via SCIPIONE CRISANZIO N. 6, 70122 |
| `tsrmbr` | C14 | Ordine Dei Tsrm e Delle Professioni Sanitarie Tecniche della Riabilitazione e della Prevenzione della Provincia di Brindisi | `brindisi@pec.tsrm.org` | Via Eugenia 87, C.da Rosamarina, 72017 |
| `u5a2qpw9` | C14 | ORDINE REGIONALE PROFESSIONE SANITARIA FISIOTERAPISTA DEL LAZIO | `LAZIO.OFI@PEC.FNOFI.IT` | Viale Luca Gaurico, 91/93 c/o Spaces Centre di Roma Eur Laurentina, 00143 |
| `u9g2qw50` | L37 | Telenergia s.r.l. | `telenergiasrl@pec.it` | Via damiano chiesa 18, 15121 |
| `ucas` | L18 | Unione di Comuni Alto Serio | `unione.altoserio@pec.regione.lombardia.it` | Piazza Dante, 8, 24020 |
| `ucbm` | L18 | Unione Comuni Basso Monferrato | `unionecomunibassomonferrato@pec.it` | Piazza Alla Vittoria 1, 15020 |
| `uclto` | L18 | Unione di Comuni Lombarda Terre dell'Oglio | `unione.terredelloglio@pec.regione.lombardia.it` | Piazza Marconi, 5, 26032 |
| `uclvt` | L18 | Unione di Comuni La Valle del Tempo | `info@pec.unionecomunivalledeltempo.it` | Passo Marinai Italia, 1, 16030 |
| `udcco` | L18 | Unione Dei Comuni del Corleonese | `comunidelcorleonese@pec.intradata.it` | Piazza Santo Agostino, 90034 |
| `udci` | L18 | Unione Dei Comuni dell'Irno | `protocollogenerale.unioneirno@pec.it` | Piazza Della Repubblica, 1, 84081 |
| `udcmea` | L18 | Unione Dei Comuni Medio Agri | `unionemedioagri@pec.it` | Via Leonardo Da Vinci, 85037 |
| `udcmvgs` | L18 | Unione Dei Comuni Montani della Valli Graveglia e Sturla - Le Valli dell'Entella | `info@pec.unionevallientella.ge.it` | Via Cap. F. Gandolfo, 115, 16046 |
| `udcmvl` | L18 | Unione Dei Comuni Montani Val Lemme | `cuc@pec.unionevallemme.al.it` | Piazza Giuseppe Garibaldi, 2, 15060 |
| `udcos` | L18 | Unione Dei Comuni Oltre Sesia | `unioneoltresesia@cert.ruparpiemonte.it` | Piazza Gastaldi, 14, 13010 |
| `udcpl` | L18 | Unione Dei Comuni Pandosia in Liquidazione | `unionedeicomuni.pandosia@asmepec.it` | Via Kennedy, 87040 |
| `udctm` | L18 | Unione Dei Comuni Terra di Mezzo | `ut.terradimezzo@pec.it` | Via Municipio, 83036 |
| `udcvaago` | L18 | Unione Dei Comuni Valle dell'Agogna | `segreteria@pec.unionevalleagogna.it` | Piazza Vittorio Veneto, 2, 28045 |
| `udcvf` | L18 | Unione Dei Comuni della Vallata del Foro | `unionecomunivallataforo@pec.it` | Via N. Marcone, 42, 66010 |
| `udcvnr` | L18 | Unione Dei Comuni Delle Valli Nervia e Roja | `pec.unionevallinerviaroia@cesisrl.legalmail.it` | Via Roma, 50, 18035 |
| `udcvu` | L18 | Unione Dei Comuni della Vite e dell'Ulivo | `unioneviteulivo@pec.it` | Via Roma, 249, 17037 |
| `udnsc` | L1 | Universiadi di Napoli 2019 - Struttura Commissariale | `commissariouniversiade.na2019@pec.it` | Molo Angioino - Stazione Marittima, 80133 |
| `ufh3ssbu` | SA | FEDERAZIONE ITALIANA TENNISTAVOLO | `acquisti@pec.fitet.org` | STADIO OLIMPICO FORO ITALICO CURVA NORD, 00135 |
| `uhsucnqe` | L24 | BACINO IMBRIFERO MONTANO DELL'ADIGE CONSORZIO DEI COMUNI DELLA PROVINCIA DI BELLUNO | `tributi.cortina@pec-legal.it` | Corso ITALIA 33, 32043 |
| `uncem` | L18 | Unione Nazionale Comuni Comunita' Enti Montani | `uncem-marche@pec.it` | Corso Garibaldi, 78, 60121 |
| `uncemve` | L18 | U.N.C.E.M. Delegazione Regionale Veneto | `uncemveneto@pec.it` | Piazza 4 Novembre, 15, 36020 |
| `uo360uaa` | SA | Consorzio Strade Vicinali di Montegiovi | `consorziostrademontegiovi@pec.it` | Via Marconi 9, 58033 |
| `ur48y785` | SA | CONSORZIO DI IRRIGAZIONE COMPRENSORIALE DI II GRADO FOSSANESE BRAIDESE | `secondogrado.fossanese.braidese@pec.it` | Via Circonvallazione n. 44, 12045 |
| `uwgsrjq2` | L37 | Gruppo di Azione Locale Trentino Orientale | `galtrentinorientale@pec.it` | Corso Ausugum, 82, 38051 |
| `v0zsau5v` | SAG | Gestione Funivie Savona - S. Giuseppe di Cairo | `gestione@pec.funiviesavonacairo.com` | Corso Stalingrado, 17014 |
| `v2as9ntw` | C14 | ORDINE DEI BIOLOGI DELLA CAMPANIA E DEL MOLISE | `protocollo.obcampaniamolise@pec.it` | Via PONTE DI TAPPIA N. 82, 80133 |
| `vd5vqfwz` | L37 | Fondazione Alghero Musei Eventi Turismo Arte | `fondazionealghero@informapec.it` | Largo Lo Quarter, 07041 |
| `vdtteh48` | L1 | ASUC CLOZ | `asuc.cloz@pec.it` | Via S. Stefano, 38028 |
| `vicrin` | C3 | Vicinia Rina | `viciniarina@pec.it` | Strada Catarina Lanz, 27, 39030 |
| `viechvrl` | L33 | ISTITUTO D'ISTRUZIONE SUPERIORE "F.DE PINEDO - M.COLONNA" | `rmis127001@pec.istruzione.it` | Via FRANCESCO MORANDINI 30, 00142 |
| `vmyjaxi1` | L37 | ISTITUTO DELLE FIGLIE DI NOSTRA SIGNORA AL MONTE CALVARIO | `istitutofigliemontecalvario@legalmail.it` | Via EMANUELE FILIBERTO 104, 00185 |
| `vpvkoz4n` | SA | sistema informativo nazionale per lo sviluppo dell'agricoltura | `protocollo.sin@pec.it` | Via curtatone 4/D, 00185 |
| `vr6xzrb2` | SA | CONSORZIO PUA SARNELLA | `consorziopuasarnella@legalmail.it` | Via Giordano Bruno 50, 80035 |
| `vsrl` | L37 | Vereinshaus Soc.R.L. | `vereinshaus@pec.it` | Piazza Hans Gamper, 3, 39022 |
| `vv38txt0` | L36 | consorzio tutela lago monate | `consorzio.lago.monate@pec.it` | Via vittorio veneto 29, 21062 |
| `vx261skn` | L37 | ITS ACADEMY LEADING GENERATION | `fondazioneitsacademy@pec.it` | Via Varese 25/d, 21047 |
| `vxds52jm` | L1 | A.S.U.C. Terlago | `asucterlago@pec.it` | Via De Gasperi. 2, 38070 |
| `vy6e7tce` | S01 | MERCATO AGRICOLO ALIMENTARE BARI SCRL | `maab.bari@legalmail.it` | Corso Cavour 2, 70121 |
| `w13fizab` | L44 | Autorità Rifiuti Piemonte | `protocollo@cert.autoritarifiutipiemonte.it` | Via PIO VII 9, 10135 |
| `w18ouc8b` | L36 | CONSORZIO DEI SERVIZI SOCIALI DEL MEDIO VOLTURNO C09 | `consorziodelmediovolturnoc09@pec.it` | Piazza DEI GIUDICI, 81043 |
| `wcg9m66f` | SA | consorzio il borgo | `consorzio.ilborgo@legalmail.it` | Piazza XX Settembre 3, 40024 |
| `wcoal29s` | SA | CASA DI RIPOSO PER MUSICISTI FONDAZIONE GIUSEPPE VERDI - ETS | `casaverdi@pec.it` | Piazza Buonarroti 29, 20149 |
| `whp0qvas` | SA | CONSORZIO URBANISTICO COMPARTO 11 | `marissrl@pec.it` | Via MODUGNO 73, 30016 |
| `wmao35t5` | L33 | ISTITUTO COMPRENSIVO PESCARA 1 | `peic84000p@pec.istruzione.it` | Via LUIGI EINAUDI, 1, 65129 |
| `wr9o8393` | L47 | Commissario Straordinario del Governo per la ZES Sardegna | `commissariozes.sardegna@pec.agenziacoesione.gov.it` | Via Via Siracusa 1/B, 09126 |
| `wyou7u1o` | L37 | LOGUDORO SERVIZI UNIPERSONALE SRL | `logudoroambiente@pec.it` | Via De Gasperi 98, 07014 |
| `x788gj0p` | L37 | ISTITUTO TECNICO SUPERIORE PER I BENI E LE ATTIVITA' CULTURALI ELAIA CALABRIA | `fondazioneelaiacalabria@pec.it` | Via zona industriale, 89900 |
| `x9g11750` | L37 | ALTA SOCIETA' COOPERATIVA | `alta_soccoop@pec.it` | Via EDMONDO DE AMICIS 3, 90143 |
| `xdy27f5a` | L37 | SILVE S.R.L. | `silvespa@pcert.it` | Via BOLOGNESE 82R, 50139 |
| `xmyjgzuu` | SA | Azienda Speciale Servizi alla Persona | `assp@pec.it` | Via San Carlo 23/c, 20081 |
| `xn8s2hnm` | SA | Fondazione Rome Technopole | `rometechnopole@pec.it` | Piazza Piazzale Aldo Moro 5, 00185 |
| `xq370ayk` | L37 | Proservice S.p.A. | `proservicespa@pec.it` | Via Ciusa 17, 09131 |
| `xsbvci2x` | L37 | DAP ORGANISMO DI ATTESTAZIONE S.P.A. | `protocollo@pec.dapsoa.it` | Via KENNEDY 88/96, 86170 |
| `xsuig654` | SA | AZIENDA CONSORTILE MERCATO ORTOFRUTTICOLO DEL ROERO | `mercato.roero@pec.it` | Piazza ITALIA 18, 12043 |
| `xu9nlswo` | L18 | UNIONE DEI COMUNI "AREA INTERNA ETNA-NEBRODI ALCANTARA | `protocollo@pec.unioneetnanebrodialcantara.it` | Corso Giorgio Maniace, 1, 95034 |
| `xurjpvzn` | L6 | Comune di Uggiate con Ronago | `protocollo@pec.comune.uggiateconronago.co.it` | Piazza Della Pieve 1, 22029 |
| `xv5xyaud` | SA | B.E.L. COREDO SPA | `belcoredospa@pec.belcoredo.it` | Via VIA DON LORENZO GUETTI, 14, 38012 |
| `y4o9fovf` | L37 | Intesi Group S.p.A. | `intesigroup@ig-trustmail.com` | Via Torino 48, 20123 |
| `y59z8qwy` | L18 | UNIONE MONTANA PREALPI VICENTINE VALCHIAMPO | `protocollo.unione.montanavalchiampo.vi@pecveneto.it` | Piazza GIACOMO ZANELLA, 42, 36072 |
| `y8i79rbd` | C14 | Ordine provinciale della professione sanitaria di Fisioterapista di Bolzano | `bolzano.ofi@pec.fnofi.it` | Via Capri 36, 39100 |
| `ya4oq7fq` | C8 | Centro italiano per il design dei circuiti integrati a semiconduttore | `segreteria@pec.fondazione-chipsit.it` | Via Sant' Ennodio 26, 27100 |
| `ycrq920k` | L33 | ISTITUTO COMPRENSIVO "DE AMICIS-D.ALIGHIERI" | `BAIC8AN00D@PEC.ISTRUZIONE.IT` | Piazza DE AMICIS 4, 70026 |
| `yd1lbf3r` | SA | FONDAZIONE ONFOODS | `fondazioneonfoods@pec.it` | STRADA UNIVERSITA' 12, 43123 |
| `yf6520sd` | L33 | I.T.T. ELENA DI SAVOIA-CARACCIOLO | `bate02000t@pec.istruzione.it` | Via CALDAROLA, 70126 |
| `ykzgi1kf` | SA | Parrocchia Madonna del Riposo | `SACROCUORE.ALCAMO@PEC.IT` | Via Madonna del Riposo, 91011 |
| `yleon1x4` | SA | Parrocchia SS. Annunziata | `parrocchiamariasantissimaannunziata@pec.it` | Piazza Annunziata, 71010 |
| `yoq3ftyl` | L37 | Istituto Tecnico Superiore per le Nuove Tecnologie peri l Made in Italy nel Settore dei Servizi alle Imprese | `itssi1@pec.it` | via del paradiso 4, 01100 |
| `yw2nw6bc` | L44 | ATA (Assemblea Territoriale d'Ambito) rifiuti 4 - FERMO | `ata4fermo@emarche.it` | Largo Don Gaspare Morello 2/4, 63900 |
| `z6fj8ssg` | L37 | COGESER SERVIZI S.R.L. | `cogeserservizi@legalmail.it` | Via MARTIRI DELLA LIBERTA' N. 18, 20066 |
| `za71ibir` | L2 | Agenzia Regionale Ligure per i Rifiuti | `agenzia_arlir@cert.arlir.liguria.it` | Via d'annunzio, 16121 |
| `zbmzj1zk` | SA | CISTERNA AMBIENTE | `cisternaambiente@pec.it` | VIA I MAGGIO, 04012 |
| `zdo3vsxe` | L37 | CONSORZIO ATENA | `atenasocietacooperativa@legalmail.it` | Via NAPOLI, 44, 81055 |
| `zf2h1nzk` | L47 | COMMISSARIO DELEGATO OCDPC 1120-24 OCDPC 1087-24 OCDPC 1042-23 ZONA EMILIA ROMAGNA | `OCDPC1042@postacert.regione.emilia-romagna.it` | Viale Antonio Silvani, 6, 40122 |
| `zjnh5wgy` | SA | MUSA S.C.A.R.L. | `musa-scarl@legalmail.it` | Piazza dell'Ateneo Nuovo, 20126 |
| `zp13zm78` | L37 | INIZIATIVE PER LA PROMOZIONE DELLO SVILUPPO ECONOMICO DELLA PROVINCIA DI REGGIO CALABRIA | `postacertificata@pec.sviprore.it` | Piazza ITALIA SNC, 89127 |
| `zpppxm62` | SA | CONSORZIO PTU CASAL MONASTERO | `consorzioptucasalmonastero@legalmail.it` | Corso del Rinascimento 49, 00186 |
| `zsilssnt` | L37 | Società Aree Produttive Industriali Basilicata - API Bas S.p.A. | `apibas@pec.it` | Largo Azzarà n. 1, 85100 |
| `zz71solp` | L37 | Ge.s.a.p. Srl | `gesapsrl@pec.it` | Via Via Bascule n. 9, 76016 |

---

## After you finish

1. Save the JSON to `data/manual_llm_enrichment.json`
2. Run `uv run python3 scripts/fetch_indicepa.py --include-others` (it will load the file automatically)
3. Run preprocess + chain to classify the new domains
4. Commit `data/manual_llm_enrichment.json` for reproducibility