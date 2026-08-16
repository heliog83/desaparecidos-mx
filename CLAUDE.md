# CLAUDE.md — Project context for Desaparecidos MX

## Current agent and delivery rules (supersedes older status notes below)

- Read and follow [`AGENTS.md`](AGENTS.md). It applies equally to Claude Code, Codex
  and other coding agents.
- **Never publish this project through Claude Artifacts and never use an Artifact URL
  as the canonical article.** Artifacts are agent-specific and previously allowed a
  stale file from a different checkout to be published.
- The canonical article is the repository-generated `reports/article.html`.
- Before every handoff or publication, run `python src/build_page.py` followed by
  `python src/check_article.py`. A failed check blocks delivery.
- Preview locally at `http://127.0.0.1:8794/article.html` after running
  `python -m http.server 8794 --directory reports`.
- Current validated aggregate vintage: **2026-08-15 — 407,253 total records;
  249,502 found alive; 23,483 found dead; 134,268 still missing.** Figure A contains
  352,294 records assigned to 2000–2025. The 36.8% confidentiality figure belongs to
  the separate **2025-12-02 record-level snapshot**.
- Historical status entries below document how the project developed. Their older
  headline numbers, figure layouts and framing are not reusable publication facts.

## What this is
Data project to (1) **quantify** disappeared/missing persons in Mexico and (2) research the
**impact of the madres buscadoras** (citizen search collectives). Two-stage scope: build the
quantified official baseline first, then layer in the harder, proxy-based collectives analysis.

## Deliverables
- **Interactive dashboard** (Streamlit, in `dashboard/`).
- **Research report** with narrative + polished charts (in `reports/`).

## Stack decision (settled)
Python backbone. `pandas` for wrangling; `altair`/`plotnine` for charts (plotnine = ggplot
parity for the report); `streamlit` for the dashboard; `geopandas` for state/municipio maps.
R was considered (ggplot2/Shiny) but Python won on one-language simplicity + easier dashboard
deployment. A single signature chart could still be done in R later if wanted.

## Data — the central challenge
- **RNPDNO** (official registry) has **no clean download** and revises numbers retroactively.
- **Best entry point: Data Cívica** cleaned CSVs — https://volveradesaparecer.datacivica.org/datos-abiertos
  (also reconstructs *erased* names between versions → enables revision analysis).
- Community tooling: `lapanquecita/personas-desaparecidas` (Python), `irvingfisica/reqrnpdno` (Rust).
- **Stage-2 buscadoras data does not exist cleanly** — must be built from journalism datasets
  ("A dónde van los desaparecidos" / Quinto Elemento) + structured news collection. Proxy, not census.
- Full catalog: [docs/data-sources.md](docs/data-sources.md).

## Snapshot figures
Do not copy figures from this historical section. Use the validated current values in
the rules above and recompute them from the processed CSVs before citing.

## Conventions
- Data flow: `data/raw` → `data/interim` → `data/processed` (parquet). `data/external` = third-party.
- Raw/large data is gitignored; only `data/processed` artifacts can be committed if small.
- Every cited figure carries a source + consultation date. Never present a proxy as an exact count.

## Status (2026-06-19)
Stage-1 pipeline working end to end:
- `data/external/data.csv` — 133,566-record RNPDNO microdata (pulled from the lapanquecita mirror).
- `src/clean.py` → `data/processed/rnpdno_clean.parquet` (date parsing, age/age-group, redaction flag).
- `src/explore.py` → 4 figures (by year, by state, age-sex pyramid, redaction by state).
- `src/rates.py` → `data/processed/state_rates.csv` + 2 figures (rate ranking, choropleth map).
  Joins everything on 2-digit zero-padded state code (`CVE_ENT`); map drawn straight from
  `mexico.json` GeoJSON with matplotlib patches (no geopandas dependency).
- `src/interrogate.py` → data-forensics diagnostics behind [docs/methodology.md](docs/methodology.md).
- `src/category_compare.py` → fig 07; `DESAPARECIDA` vs `+NO LOCALIZADA` sensitivity (national +6.1%,
  but Zacatecas +42%/Chiapas +29%; methodology open-q 2 RESOLVED).
- `src/crosscheck.py` → mirror vs official figures: national drift −0.7%, Jalisco the volatile outlier
  (methodology open-q 3 RESOLVED).
- `src/fetch_flow.py` → **LIVE RNPDNO dashboard API scraper WORKS** (no captcha on the JSON endpoints;
  exact POST params reverse-engineered from `reqrnpdno` — empty-string defaults matter, not "0").
  Pulls aggregate flow incl. located outcomes → `data/processed/flow_{totales,by_year,by_state}.csv`
  + raw JSON in `data/external/rnpdno_api/`. National: 135,092 missing / 268,171 located / 22,621 found dead.
- `src/flow_consolidated.py` → fig `19_outcomes_by_year_consolidated` — the SIGNATURE chart: two stacked
  panels (absolute + 100%) decomposing each year into found-alive / found-dead / still-missing.
  2000–2025: 212,876 alive / 19,920 dead / 118,584 missing. (Retired the earlier debias.py scale/rate
  figs it superseded.)
- `.venv/` has pandas/numpy/matplotlib/pyarrow/requests installed.

**KEY CORRECTION (intellectual-honesty note):** the flow data REFUTED our earlier survivorship worry.
The rise is REAL incidence growth (~100 in 2000 → ~3,000 in 2007 drug-war onset → ~37,000 in 2025),
not a stock artifact. Resolution runs opposite to intuition: older cohorts LESS resolved (~16–27%) than
recent (~65–70%). methodology.md §2 updated to reflect this.

**FIGURE SET (clean, no dup numbers, ALL reproducible from src/):** explore.py(01–04), rates.py(05–06),
category_compare.py(07), opacity_confidentiality.py(08–10), opacity_models.py(11–13),
opacity_typology.py(14–15), opacity_interactive_and_stats.py(16–18), flow_consolidated.py(19).
The opacity 08–15 scripts were extracted from notebooks 03/04/05 (faithful nbconvert + cleanup).
NOTE: opacity scripts inherit the notebooks' `plt.show()` — run with `MPLBACKEND=Agg` for headless/batch.

**DASHBOARD (Stage-1 deliverable, DONE):** `dashboard/app.py` — Streamlit, boots clean. Sections:
national metrics, scale&outcomes (year slider + abs/share toggle), geography (count-vs-rate toggle +
choropleth), opacity scatter (confidential-share × rate, sized by homicide rate). `streamlit run dashboard/app.py`.

**OPACITY MECHANISM ANSWERED (2026-07-06):** `docs/opacity-mechanism.md` — CONFIDENCIAL is a
federal consent rule (Art. 108 Ley General) operationalized by capturing fiscalías, with missing
consent paperwork defaulting to confidential (77.4% of records had no consent info in Aug 2020 per
CNB's own oficio to INAI, copy in `data/external/legal_docs/`) and Jalisco's Fiscalía
blanket-declaring its submissions non-publishable (oficio p.11 n.3). Never frame CONFIDENCIAL as
"families chose privacy." `docs/cases/jalisco.md` evidence sections FILLED: blanket policy (2020)
+ Jalisco stopped feeding RNPDNO from 2022 (parallel REPD registry) + 1,026
confidential-with-active-search-notice cases (ZonaDocs "engaño estadístico", 2024-11-21);
Teuchitlán/Rancho Izaguirre (2025-03-05, Guerreros Buscadores) is the candidate Stage-2 anchor
event. `docs/cases/guerrero.md` also FILLED (2026-07-06): same consent rules, 9% share — opacity by
OMISSION (collectives count more than the state registers; Iguala 623 vs ~3,800 statewide) vs
Jalisco's opacity by REDACTION. Thesis memo written: `reports/opacity_memo.md` ("one defensible
claim": CONFIDENCIAL is administrative artifact; two modes of opacity). **ARTICLE DRAFT v1:**
`reports/article_draft.md` — visual-led web piece (8 sections, each anchored on one figure; user's
strength is data viz so charts carry the argument). Figs A–D reuse 19/06/09/10-14 (style-pass
notes in draft); fig 20 BUILT (`src/consent_accounting.py` → consent-accounting stacked bar,
hardcoded from oficio pp.5,11); fig 21 BUILT (`src/jalisco_divergence.py` — documented snapshot
pairs: federal froze +68 in 13 months from Apr 2022 while state issued 1,260 bulletins; federal
15,015 Mar-2025 → 12,776 our API pull Jun-2026 after recount announcement — "coincides", don't
assert cause); fig 22 BUILT (`src/two_modes.py` — thesis chart, Jalisco redaction vs Guerrero
omission, different-denominators caveat in footer). **STYLE PASS DONE (2026-07-06):** all 7
publication figures in `reports/figures/article/` (A–G): A–D rebuilt by `src/article_figs.py`
(A=fig19 redesign w/ direct band labels, B=binned choropleth w/ top-3 labels, C=all-32 redaction
ranking w/ case states colored, D=redaction-vs-rate scatter w/ case states highlighted); E–G from
the consent/divergence/two-modes scripts which now dual-save numbered + article versions. Shared
palette/typography/captions in `src/article_style.py` — restyle the whole set from there. Draft
figure refs updated. Decide EN/ES before publishing. Stage-2 (10 find-events, one state) is the
follow-up article.

**VERSION AUDIT (2026-07-11) — memo test #1 EXECUTED, claim CONFIRMED:** `src/version_audit.py`
rebuilds a 10-snapshot monthly panel (Apr–Dec 2025) from the lapanquecita mirror's git history
(SHAs pinned in script; snapshots cached in `data/external/mirror_history/`, panel committed at
`data/processed/confidencial_panel.csv`). National: confidential 44,035→49,136 (+5,101 = 77% of
net registry growth; share 34.7%→36.8%). Movement is BATCHED: Tamaulipas +2,537 in 2 months w/
flat totals (share 20%→39% — fig C/D would've looked different in April!); Jalisco −1,367 conf in
Q4-2025 as totals fell (purge PRECEDES Jan-2026 recount announcement); Tabasco deleted ⅓ of records
in Nov; Guanajuato catch-up load ~60% confidential. Fig 23 / article fig H ("The redaction flag
moves in batches"), draft §5b added. **Mirror snapshot date PINNED: data.csv = 2025-12-02 upstream
commit (max FECHA_REGISTRO 2025-12-01)** — draft placeholders closed. Also downloaded (scratchpad,
not yet analyzed): Data Cívica Sep-2023 named CSV (116,945 named vs mirror's 84,430 — context in
opacity-mechanism.md), 2017-2024 person panel, borrados list — person-level long-horizon test is
the natural deepening.

**STAGE 2 STARTED:** `docs/stage2-schema.md` (coding schema, one-row-per-find-event, body≠remains,
led_by attribution), `data/stage2/clandestine_finds.csv` (5 LOW-confidence illustrative seeds from
journalism — NOT a census), `src/stage2_validate.py` (schema/enum validator). Anchor: 22,621 found dead.
Next: expand from Quinto Elemento / FUNDENL / news; never present seeds as totals.

**CRITICAL framing (see docs/methodology.md):** the dataset is the STOCK of people *still missing*,
not a flow of all disappearances (no "located" status exists). Time trends are survivorship-biased
— don't read the year chart as incidence. `DESAPARECIDA` (crime-presumed) and `NO LOCALIZADA`
(no crime evidence) are lumped; `CONFIDENCIAL` (37%) is all-or-nothing (state only), so charts use
different denominators and cross-state rank is confounded by prosecutorial redaction practice.

Key Stage-1 findings: 36.8% of records redacted (CONFIDENCIAL); redaction varies wildly by
state (Jalisco 67%, Nayarit 66% vs national 37%) and redacted rows lose ALL dates — so redaction
can only be analyzed by state, not over time. Disappearances/yr rose sharply 2023->2025 (~5.1k->7.9k).
Per-capita reframes the geography: Tamaulipas (359/100k), Zacatecas (226), Sinaloa (211) lead by
RATE, while Edo. de México / CDMX (top by absolute count) fall to ~80/100k.

**Next options:** (B) Streamlit dashboard, (D) Stage-2 buscadoras dataset, or more Stage-1
(monthly trends, age-rate by state, found-vs-missing over time).

## Ethics
Real victims and grieving families. Center victims/searchers, state uncertainty, avoid sensationalism.
