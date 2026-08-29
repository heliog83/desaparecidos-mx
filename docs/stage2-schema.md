# Stage 2 — Madres Buscadoras / Clandestine Finds: coding schema

There is **no official dataset** of what search collectives find. We build one by structured
coding of journalism + collective reports. This is a **sample, not a census** — coverage is biased
toward large, dramatic, well-reported finds in well-covered states. Treat every aggregate as a lower
bound, and never present it as the true total.

## The anchor it connects to
Stage 1's flow gives **23,483 people found dead** nationally (`localizadas sin vida`,
2026-08-15 freeze). Stage 2 asks:
*of recovery work, how much is done by collectives vs. the state, and where?* The registry can't
answer attribution; coded journalism is the only route.

## Unit of analysis
**One row = one reported find event** (a search action that located grave(s) and/or remains at a
place/time). Not one body, not one collective. A single event may yield many graves/bodies.

## Columns (data/stage2/clandestine_finds.csv)
| column | type | notes |
|---|---|---|
| `event_id` | str | stable id, e.g. `2025-12-silao-gto-01` |
| `date` | date | `YYYY-MM-DD`; use first of month/year if imprecise |
| `date_precision` | enum | `day` / `month` / `year` / `approx` |
| `state` | str | match RNPDNO `ENTIDAD` spelling (uppercase) for joinability |
| `municipality` | str | as reported |
| `collective` | str | collective name, or `unknown` |
| `led_by` | enum | `collective` / `state` / `joint` / `unknown` — the key attribution field |
| `graves_found` | int? | number of *fosas*; null if not stated |
| `bodies_found` | int? | whole bodies/cuerpos |
| `remains_bags` | int? | *bolsas* with remains (NOT interchangeable with bodies) |
| `persons_identified` | int? | confirmed identifications, if reported |
| `source_outlet` | str | e.g. `Milenio`, `Infobae` |
| `source_url` | str | direct link |
| `consulted` | date | when you read the source |
| `source_type` | enum | `journalism` / `registry` — see "Two provenances" below |
| `confidence` | enum | `high` / `med` / `low` — your confidence in the coded figures |
| `notes` | str | ambiguities, double-report risk, body-vs-remains caveats |

Registry-imported rows carry two extra columns:

| column | type | notes |
|---|---|---|
| `municipality_lat` | float? | **municipal seat (town centre), not a grave location** |
| `municipality_lon` | float? | same — every grave in a municipality shares this point |

`state` must be one of the 32 canonical `entidad` values used by the Stage-1 tables
(uppercase, accented: `CIUDAD DE MÉXICO`, `ESTADO DE MÉXICO`, `MICHOACÁN`, `NUEVO
LEÓN`, `COAHUILA`, `VERACRUZ`, …), plus the registry's own `SE DESCONOCE`.
`src/stage2_validate.py` fails on anything else, because a non-canonical spelling
silently breaks the join to Stage 1 that this column exists to support.

## Two provenances, one schema

`source_type` separates two things that must never be pooled or captioned alike.

**`journalism`** — `data/stage2/clandestine_finds.csv`. Hand-coded find events. One
row = one find event. Carries real attribution, so `led_by` is meaningful. Currently
5 illustrative seed rows.

**`registry`** — `data/stage2/clandestine_finds_imported.csv`, built by
`src/stage2_import.py` from the CNB / Quinto Elemento Lab clandestine-grave registry
(4,483 rows, 5,698 graves, consulted 2023-10-06).

The registry import comes with hard limits:

- **No attribution exists in the source.** Every row is `led_by='state'` and
  `collective='unknown'`. That is a *missing column*, not evidence that the state
  located these graves. Never chart, caption, or summarise these rows as madres
  buscadoras work, and never compute an attribution share over them.
- **Bodies and remains are not recorded**, so no body count derives from it.
- **One row is one registry grave record, not one find event.** 1,499 rows sit in
  exact-duplicate groups (same municipality, date and count) — those are genuinely
  separate graves, not duplicates to clean.
- **Coordinates are municipal seats**, repeated for every grave in the municipality.
  They support municipality-level counts and nothing finer.
- **`confidence` records temporal resolution**, not doubt about a grave's existence:
  `high` = day-precision date, `med` = year only, `low` = no date at all (92 rows).
- **`event_id` is a content hash** plus an occurrence index, so it is stable under
  re-sorting. An earlier version numbered rows sequentially, which silently
  relabelled every event whenever the source order changed.

Raw source (gitignored, 361 KB):
`data/external/20231006-registro-fosas-cnb-quintoelab.csv`,
sha256 `7b973c49cdb1212431d44ee29a1e55cd8ec84e8c06329351d9f89fe55e935fe9`.
Municipal-seat coordinates are cached in `data/stage2/municipality_coords.csv` so
the import is reproducible offline; `--refresh-coords` rebuilds it from the network.

## Coding rules (so the dataset stays honest)
1. **Bodies ≠ remains ≠ bone fragments.** Keep them in separate columns; never sum into "victims."
2. **Attribution is often fuzzy.** If a report says "collectives located, authorities exhumed," code
   `led_by = joint`. Only use `collective` when the collective clearly drove discovery. When unclear,
   `unknown` + low confidence — do not guess in the state's or the collectives' favor.
3. **Deduplicate.** The same find is re-reported across outlets and updated over days. One event = one
   row; pick the most complete source, note others in `notes`.
4. **Counts get revised.** Initial reports under/overstate. Prefer later, official-confirmed figures;
   flag volatility in `notes`.
5. **Geography here = where remains were FOUND**, which is *not* the same as where people disappeared
   (Stage 1's geography). Keep that distinction explicit in any cross-analysis.

## Sources to mine (see docs/data-sources.md §Stage 2)
"A dónde van los desaparecidos" / Quinto Elemento (the leading fosas dataset), FUNDENL, and outlet
reporting (Infobae, Milenio, Cultura Colectiva). The seed rows in the CSV are **illustrative, coded
from news at low confidence** — verify and expand before any analysis.
