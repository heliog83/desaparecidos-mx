# Stage 2 — Madres Buscadoras / Clandestine Finds: coding schema

There is **no official dataset** of what search collectives find. We build one by structured
coding of journalism + collective reports. This is a **sample, not a census** — coverage is biased
toward large, dramatic, well-reported finds in well-covered states. Treat every aggregate as a lower
bound, and never present it as the true total.

## The anchor it connects to
Stage 1's flow gives **22,621 people found dead** nationally (`localizadas sin vida`). Stage 2 asks:
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
| `confidence` | enum | `high` / `med` / `low` — your confidence in the coded figures |
| `notes` | str | ambiguities, double-report risk, body-vs-remains caveats |

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
