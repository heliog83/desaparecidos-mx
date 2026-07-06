# Desaparecidos MX — Quantifying Mexico's Disappearance Crisis & the Madres Buscadoras

A data project to (1) quantify the scale and dynamics of disappeared/missing persons in
Mexico using official and reconstructed registries, and (2) research the role and impact of
the **madres buscadoras** — the citizen search collectives (mostly mothers) who locate
clandestine graves and recover remains where the state has not.

> **Stack:** Python (pandas / Altair / plotnine for analysis & report charts) +
> Streamlit (interactive dashboard). See [docs/research-design.md](docs/research-design.md)
> for the project frame and [docs/data-sources.md](docs/data-sources.md) for the data catalog.

## Why this is hard (and worth doing)

- The official registry (**RNPDNO**) is **locked behind an interactive dashboard** with no
  clean download. Figures also *change retroactively* between consultations — names appear
  and disappear. So even the baseline "how many" is a data problem, not a lookup.
- The **madres buscadoras impact is not in any official dataset.** There is no national table
  of "graves found by collectives." It has to be measured through **proxies** (clandestine
  graves / *fosas* discovered, remains recovered, who found them — state vs. collective) built
  from investigative-journalism datasets and structured news collection.

## Research questions (staged)

**Stage 1 — Quantify the crisis (official, solid data)**
- How many people are registered as disappeared/not-located, and how has it grown over time?
- Geographic concentration (by state/municipality), demographics (sex, age), found vs. still missing.
- Retroactive-revision analysis: how much do the official numbers shift between versions?

**Stage 2 — Madres buscadoras impact (proxy, patchy data)**
- How many clandestine graves / remains have collectives located, and where?
- Collective-led vs. state-led recoveries — share and trend.
- Relationship between collective activity and official case resolution.

## Project structure

```
data/
  raw/         # untouched downloads (gitignored)
  interim/     # cleaned, not yet analysis-ready
  processed/   # analysis-ready tables
  external/    # third-party datasets (Data Cívica, journalism datasets)
src/           # reusable pipeline code (fetch, clean, build)
notebooks/     # exploratory analysis
reports/       # written report + figures/
dashboard/     # Streamlit app
docs/          # data catalog, methodology, notes
```

## Getting started

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/fetch_rnpdno.py        # pull the registry data (see script header)
jupyter lab                       # start exploring in notebooks/
```

## Ethics & framing

This concerns real victims and grieving families. Treat every record as a person. Cite
sources, state uncertainty explicitly, never present a proxy as a precise count, and prefer
language that centers victims and searchers over sensationalism.
