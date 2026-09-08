# Desaparecidos MX

**What Mexico's public registry of disappeared people does not let you see — and what
can still be measured through it.**

More than 134,000 people are currently registered as disappeared or not-located in
Mexico. In the frozen record-level mirror dated 2 December 2025, **36.8% of unresolved
records contained a single public fact: the state.** Every other field — date, age,
sex, municipality and case status — was replaced by the word `CONFIDENCIAL`.

This project quantifies that redaction, tests several explanations for it and documents
how administrative decisions shape what the public can see. The available data do not
identify a single cause for every confidential record.

📄 **Read the article:** *The Redacted Crisis* — [generated local HTML](reports/article.html)
· [markdown source](reports/article_draft.md) · [agent workflow](docs/working-with-agents.md)

---

## Findings

**1. State violence does not explain interstate differences in confidentiality.**
Across all 32 states, confidential share correlates *negatively* with the cumulative
homicide-victim rate for 2015–2025 (Pearson r = −0.38). That state-level association is
descriptive: it neither measures danger in individual cases nor establishes why a
particular record was marked confidential.

**2. The government's own paperwork reveals an administrative and consent-accounting gap.**
In 2020 the National Search Commission told the transparency institute that for **77.4%
of records no consent information existed at all** (Oficio SEGOB/CNBP/1349/2020). The
Fiscalía of Jalisco declared its *entire* federal submission non-publishable. Journalists
later found 4,765 cases marked confidential while the same authorities circulated public
search posters for them.

**3. The public totals sometimes move in batches.**
Rebuilding ten monthly snapshots from a mirror's git history: confidential records grew
44,035 → 49,136 in eight months — **77% of the registry's entire net growth**. Tamaulipas
reclassified ~2,500 existing records in two months while its total barely moved (share
20% → 39%). These changes are consistent with bulk administrative processing, but the
snapshots do not reveal whether the cause was consent, correction, resolution, deletion
or another operation.

**4. Official and family records provide different views.**
Jalisco redacts 67% of its registry. Guerrero redacts 9%, while three collectives
document 623 cases in the city of Iguala. The person-level overlap is unknown, so these
figures cannot be added or subtracted; they establish parallel systems of evidence, not
a measured undercount.

**5. Recent recorded cohorts are much larger.**
For most cohorts since 2008, roughly two-thirds are currently classified as located,
even as annual recorded volume more than tripled. Because the aggregate data contain a
year of disappearance but no date of location, this pattern cannot measure search speed
or show how many people were found in any particular year.

Full reasoning and caveats: [docs/methodology.md](docs/methodology.md) ·
[docs/opacity-mechanism.md](docs/opacity-mechanism.md)

---

## Reproducing it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**Building and validating the article needs none of this** — not even the venv.
`build_page.py` and `check_article.py` are standard-library only, and the publication
data is committed under `data/publication_freezes/2026-08-15/`, so a clean checkout
can run:

```bash
python3 src/build_page.py     # -> reports/article.html
python3 src/check_article.py  # hash-verifies the freeze, then the HTML against it
```

That reproduces the committed `reports/article.html` byte for byte.

The scripts below regenerate the *underlying* data and figures. They need the
gitignored raw sources, and `fetch_flow.py` pulls **live** numbers that will differ
from the pinned freeze — it writes to the mutable `data/processed/`, which the article
build deliberately does not read. To move the article to fresher data, cut a new
freeze with `src/publication_freeze.py --date YYYY-MM-DD` and bump the
`PUBLICATION_FREEZE` constant in `src/build_page.py`.

```bash
MPLBACKEND=Agg python src/fetch_flow.py        # live RNPDNO dashboard API -> flow_*.csv
MPLBACKEND=Agg python src/clean.py             # microdata -> rnpdno_clean.parquet
MPLBACKEND=Agg python src/rates.py             # per-capita rates + choropleth
MPLBACKEND=Agg python src/category_compare.py  # DESAPARECIDA vs +NO LOCALIZADA
MPLBACKEND=Agg python src/crosscheck.py        # mirror vs live registry drift
MPLBACKEND=Agg python src/flow_consolidated.py # signature outcomes-by-year figure
MPLBACKEND=Agg python src/article_figs.py      # article figures A-D
MPLBACKEND=Agg python src/consent_accounting.py    # figure E
MPLBACKEND=Agg python src/jalisco_divergence.py    # figure F
MPLBACKEND=Agg python src/two_modes.py             # figure G
MPLBACKEND=Agg python src/version_audit.py         # figure H
MPLBACKEND=Agg python src/international_comparison.py  # figure 28
python src/stage2_import.py                        # CNB grave registry -> Stage 2
python src/stage2_validate.py                      # schema gate for Stage-2 files
python src/check_figures.py                        # figure numbers unique + contiguous
```

`MPLBACKEND=Agg` matters: several scripts inherit `plt.show()` from the notebooks they
were extracted from and will block without it.

Interactive dashboard:

```bash
streamlit run dashboard/app.py
```

### Local-first delivery rule

`reports/article.html` is generated output, not a second source document. Do not edit
it independently. Make prose or data changes in the repository, run `build_page.py`,
require `check_article.py` to pass, and commit the source and generated HTML together.

**Claude Artifacts are not part of this project.** Agents must not invoke an Artifact
tool or link to `claude.ai/code/artifact/...`. Preview locally with:

```bash
python3 -m http.server 8794 --directory reports
```

Then open `http://127.0.0.1:8794/article.html`. If public hosting is requested later,
use an agent-neutral destination chosen explicitly by the user and deploy the exact
validated HTML. See [docs/working-with-agents.md](docs/working-with-agents.md).

## Data sources, and one important caveat

| Source | Role | Vintage |
|---|---|---|
| RNPDNO dashboard API | Aggregate flows incl. located-alive / located-dead | live (last pull 2026-08-15) |
| [lapanquecita mirror](https://github.com/lapanquecita/personas-desaparecidas) | Record-level microdata (133,566 rows) | **frozen at 2025-12-02** |
| CNB oficio to INAI | Consent accounting (primary document) | 2020 |
| ZonaDocs, Tlachinollan, Animal Político, HRW | Case evidence | 2019–2026 |

**The mirror is no longer updated.** It published monthly from April 2025 and stopped
after 2025-12-02; our copy is byte-identical to the last upstream commit. So the project
carries two vintages on purpose: flow figures are current, field-level figures are a
December 2025 cross-section. National drift between them is 0.11%, but it is not uniform
by state — `src/crosscheck.py` reports it, and per-state claims are labelled accordingly.
Full audit: [docs/data-refresh-2026-08-15.md](docs/data-refresh-2026-08-15.md).

## What this data cannot tell you

- The registry is a **stock of people still missing**, not a history of all
  disappearances. Record-level data carries no "located" status.
- `DESAPARECIDA` (crime presumed) and `NO LOCALIZADA` (no evidence of crime) are lumped
  together. Nationally the choice moves counts ~6%; in Zacatecas, 42%.
- **Confidential records have no date**, so redaction can be analysed by state but never
  over time by year of disappearance. This is why the version-history analysis exists.
- Under-registration is invisible. People who were never reported do not appear, and
  Guerrero's section is about exactly that gap.
- None of this supports the claim that the state deliberately hides its disappeared. It
  supports a narrower one: the flag is unexplained, unaudited, and contradicted in
  thousands of documented cases by the authorities' own search notices.

## Layout

```
data/
  external/    third-party + registry pulls (gitignored; mirror_history/ cached snapshots)
  processed/   analysis-ready tables (parquet/csv)
  stage2/      hand-coded clandestine-find events — ILLUSTRATIVE SEEDS, not a census
src/           pipeline: fetch -> clean -> analyse -> figures -> page
notebooks/     exploratory work (03-06 were extracted into src/opacity_*.py)
reports/       article draft, article.html, figures/ (numbered) + figures/article/ (A-H)
dashboard/     Streamlit app
docs/          methodology, data sources, opacity mechanism, per-state case files
```

## Status

Stage 1 is complete: pipeline, dashboard, eight publication figures, and the article.

Stage 2 — measuring what the search collectives themselves find — is **scoped but not
built**. `data/stage2/clandestine_finds.csv` holds five low-confidence illustrative
records and a validator. It is not a dataset yet, and it must never be presented as a
count.

## Ethics

This concerns real victims and grieving families. Every record is a person. Sources are
cited with consultation dates, uncertainty is stated rather than smoothed, proxies are
never presented as precise counts, and the framing centres victims and searchers over
sensationalism. `CONFIDENCIAL` is never described as "families chose privacy" — the
evidence does not support it.
