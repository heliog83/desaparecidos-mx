# Data Sources Catalog

Last reviewed: 2026-06-19. Figures below are snapshots — always re-check the source date.

## Headline figures (context, not for hardcoding)

- **~132,500** people registered as disappeared/not-located (RNPDNO, as of March 2026).
- **~262,000** registered as *located* (~66% of all records) — most located alive; a minority found dead.
- Numbers **shift between consultations**; treat any single figure as a snapshot with a date.

Sources: [SinEmbargo](https://www.sinembargo.mx/4787261/registro-de-personas-desaparecidas-2026-notas-criticas-y-contexto/),
[CNN en Español](https://cnnespanol.cnn.com/2026/03/27/mexico/gobierno-nuevo-informe-personas-desaparecidas-ong-cuestionan-orix),
[POPLab](https://poplab.mx/posts/registro-de-personas-desaparecidas-2026-notas-criticas-y-contextos/).

---

## Stage 1 — Official / reconstructed registry data

### 1. RNPDNO — Registro Nacional de Personas Desaparecidas y No Localizadas (PRIMARY)
- Official registry, run by the Comisión Nacional de Búsqueda (CNB).
- Public dashboard: https://versionpublicarnpdno.segob.gob.mx/
- **No clean download.** Data is served to the dashboard via internal JSON endpoints; you must
  scrape those. Variables include state, municipality, sex, age range, nationality, date.

### 2. Data Cívica — "Volver a Desaparecer" open data (RECOMMENDED ENTRY POINT)
- https://volveradesaparecer.datacivica.org/datos-abiertos
- Cleaned CSVs reconstructed from the RNPDNO, **plus** a reconstruction of names *erased*
  between public versions (2017–2024) — directly enables the retroactive-revision analysis.
- NGO-maintained, documented, the least painful way to get analysis-ready data.
- (403s a plain fetch — download in a browser, or use their GitHub.)

### 3. Community tooling (scrapers / ready datasets)
- **`lapanquecita/personas-desaparecidas`** (Python) — scripts + dataset to analyze the RNPDNO.
  https://github.com/lapanquecita/personas-desaparecidas
- **`irvingfisica/reqrnpdno`** (Rust crate) — consumes the RNPDNO public dashboard endpoints.
  https://github.com/irvingfisica/reqrnpdno — reference for replicating the API calls in Python.
- **Data Cívica GitHub:** https://github.com/datacivica

### 3b. Aggregate FLOW data — with located outcomes (the de-biasing source)
Our record-level mirror is the still-missing *stock* only. But aggregate flow data **with located
people is obtainable**: the official RNPDNO dashboard publishes counts by status — including
**`LOCALIZADA CON VIDA`** and **`LOCALIZADA SIN VIDA`** — broken down by year/state/sex. Those are
reachable through its JSON endpoints (the **`reqrnpdno`** tool automates exactly this), and Data
Cívica's whole *"Volver a desaparecer"* project is built on tracking which names fell off the list
between versions (located vs. "disappeared again"). This is what lets us compute true incidence and
resolution rates and de-bias the year trend. (Interpret "located" carefully — see methodology.md §3 note.)

### 4. RNPED (predecessor registry, historical)
- Older registry (fuero común/federal), now superseded by RNPDNO but useful for long history.
- https://www.gob.mx/sesnsp/acciones-y-programas/registro-nacional-de-datos-de-personas-extraviadas-o-desaparecidas-rnped
- datos.gob.mx mirrors: https://datos.gob.mx/dataset/?tags=desaparecidos

---

## Stage 2 — Madres buscadoras / clandestine graves (proxy data)

No single clean dataset exists. Build a structured table from these:

- **"A dónde van los desaparecidos"** (Quinto Elemento Lab / journalism) — the leading
  investigative dataset on *fosas clandestinas* (clandestine graves) by state and year.
- **FUNDENL** (Fuerzas Unidas por Nuestros Desaparecidos en Nuevo León) — collective with
  documented search records. https://en.wikipedia.org/wiki/FUNDENL
- **News-event collection** — structured extraction from outlets (Infobae, Milenio, Cultura
  Colectiva) reporting collective finds: date, state/municipality, collective, # graves,
  # bodies/remains, who led the search. Build a coding schema; treat as a sample, not a census.
- **CIDH/OAS report (2026)** on disappearances in Mexico — context + some aggregate figures.
  https://www.oas.org/es/cidh/informes/pdfs/2026/informe_desapariciones_mx_spa.pdf

### Measurement caveats for Stage 2
- News coverage is **biased** toward large/dramatic finds and better-covered states — undercounts.
- "Bodies" vs. "remains" vs. "bone fragments" are not interchangeable; keep them as separate fields.
- Attribution (collective-led vs. state-led) is often ambiguous in reporting — code an explicit
  confidence level.

## Added 2026-08-29 (used in the article, not in any pipeline)

Neither of these is a dataset this repo derives from. Both are cited journalism whose
figures are quoted, not recomputed, and neither is merged with the registry numbers.

- **Unidentified bodies in state custody, 2006–2023.** Efraín Tzuc and Mayela Sánchez,
  "Cierra sexenio de AMLO con más de 72,100 cuerpos sin identificar", Quinto Elemento
  Lab / A dónde van los desaparecidos, 2024-09-24.
  <https://quintoelab.org/project/sexenio-amlo-72-mil-cuerpos-crisis-forense> — data and
  methodology at <https://quintoelab.org/project/crisis-forense-2024>.
  72,172 bodies entered Semefos and were never identified; 48,108 (67%) went to common
  graves; 13,272 have been unidentified over a decade; 34,699 entered 2019–2023.
  Compiled from transparency requests to all 32 state forensic services plus the FGR.
  **Treat as a floor:** Morelos refused to respond, and it counts whole cadavers, not
  unindividuated remains. The overlap with the RNPDNO's 134,268 is unknown and cannot
  be derived from public data — never subtract or add these figures.

- **Registry field completeness, snapshot 2023-08-23.** Data Cívica, "Volver a
  desaparecer", <https://volveradesaparecer.datacivica.org/> — reported by Sandra
  Rojas, La Cadera de Eva, 2024-03-20,
  <https://lacaderadeeva.com/actualidad/amlo-borra-11-mil-nombres-de-registro-de-desapariciones-en-mexico/9593>.
  Audit of the 110,964-record public RNPDNO version: reporter contact left blank in 7
  of 10 records. Also the source for the 10,953 erased names (not yet used in the
  article — see §6b, which currently has to leave the deletion question open).
