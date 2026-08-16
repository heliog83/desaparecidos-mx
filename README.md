# Desaparecidos MX

**What Mexico's public registry of disappeared people does not let you see — and what
can still be measured through it.**

More than 133,000 people are registered as disappeared or not-located in Mexico. For
**36.8% of them the public record contains a single fact: the state where they
vanished.** Every other field — date, age, sex, municipality, case status — is replaced
by the word `CONFIDENCIAL`.

This project quantifies that redaction, establishes what causes it, and shows that it is
an administrative artifact rather than a record of families choosing privacy.

📄 **Read the article:** *The Redacted Crisis* — [published version](https://claude.ai/code/artifact/5f7022ae-4357-4fb8-a16e-a8e40ac988e7)
· [markdown source](reports/article_draft.md)

---

## Findings

**1. The redaction flag is not about protecting people at risk.**
Redaction correlates *negatively* with violence (r = −0.42 against homicide rate, 28
states). The three most violent states — Colima, Guerrero, Chihuahua — each redact 9%.
Yucatán, which has both the lowest homicide rate and the lowest disappearance rate in
the country, redacts 62%.

**2. It is an administrative artifact, and the government's own paperwork says so.**
In 2020 the National Search Commission told the transparency institute that for **77.4%
of records no consent information existed at all** (Oficio SEGOB/CNBP/1349/2020). The
Fiscalía of Jalisco declared its *entire* federal submission non-publishable. Journalists
later found 4,765 cases marked confidential while the same authorities circulated public
search posters for them.

**3. The flag moves in batches, not in individual decisions.**
Rebuilding ten monthly snapshots from a mirror's git history: confidential records grew
44,035 → 49,136 in eight months — **77% of the registry's entire net growth**. Tamaulipas
reclassified ~2,500 existing records in two months while its total barely moved (share
20% → 39%). Mexico City added 1,217 records through 2025, then shed 1,327 by August 2026.

**4. Opacity has two modes, and a state can look clean on the wrong axis.**
Jalisco redacts 67% of its registry. Guerrero redacts 9% — but registers ~3,800 people
while three collectives document 623 cases in the city of Iguala alone. One registry
hides what it holds; the other is missing what it never took in.

**5. Resolution has been flat for eighteen years.**
Since 2008, close to two-thirds of each year's reported disappearances end with the
person located, while annual volume more than tripled. But of those who disappeared
before 2016 and are still missing, only ~2.5% are found per year.

Full reasoning and caveats: [docs/methodology.md](docs/methodology.md) ·
[docs/opacity-mechanism.md](docs/opacity-mechanism.md)

---

## Reproducing it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then, in order. Every figure in the article is produced by one of these:

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
python src/build_page.py                           # -> reports/article.html
```

`MPLBACKEND=Agg` matters: several scripts inherit `plt.show()` from the notebooks they
were extracted from and will block without it.

Interactive dashboard:

```bash
streamlit run dashboard/app.py
```

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
