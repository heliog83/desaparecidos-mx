# Research Design

Last updated: 2026-06-19.

## Working thesis

This project studies how official disappearance records, clandestine grave discoveries, and
citizen search efforts reveal different parts of Mexico's disappearance crisis, with special
attention to what madres buscadoras make visible that institutions fail to count, find, or
identify.

## First broad question

How has the geography of disappearances and clandestine graves changed since 2006, and how
do those patterns overlap with federal administrations, legal reforms, and major collective
search discoveries?

This question starts wide on purpose. The first pass should map the crisis nationally; later
passes can zoom into states, municipalities, periods, or collectives.

## Legal categories vs. project categories

Mexican law distinguishes two registry categories:

- `Persona Desaparecida`: the person's whereabouts are unknown and there is some indication
  that the absence is related to a crime.
- `Persona No Localizada`: the person's location is unknown, but the information reported to
  the authority does not indicate probable connection to a crime.

Source: Ley General en Materia de Desaparicion Forzada de Personas, Desaparicion Cometida
por Particulares y del Sistema Nacional de Busqueda de Personas, Article 4, sections XVI and
XVII. Latest reform in the official Congressional PDF: 2025-07-16.

For this project, the human-centered umbrella category is:

> A person whose people cannot find them and do not know where they are.

For measurement, we do not use a fixed "XX days missing" threshold to decide whether someone
counts. Instead, we include people reported, registered, or documented as disappeared / not
located, and use time unresolved as a metric: 24 hours, 72 hours, 7 days, 30 days, 1 year, and
multi-year unresolved.

## What the current local RNPDNO mirror can measure

The local file `data/external/data.csv` contains 133,566 rows. One row appears to represent
one person (`ID_VICTIMA` is unique; see `docs/methodology.md`).

Status mix in the current file:

| Status | Rows | Share |
|---|---:|---:|
| `DESAPARECIDA` | 79,612 | 59.6% |
| `NO LOCALIZADA` | 4,818 | 3.6% |
| `CONFIDENCIAL` | 49,136 | 36.8% |

Important: this mirror is a stock of people still missing / unresolved at the snapshot date,
not the flow of all disappearance reports. People already located are not present in this
file, so year charts must be described as "people who disappeared in year Y and remain
unresolved in this snapshot."

## What we will count

Keep units separate. Do not combine them into one headline number.

- People: disappeared, not located, confidential / redacted, located alive, located dead, still
  unresolved when available.
- Time: year of disappearance, year of report, unresolved duration, pre/post legal or
  administrative changes.
- Place: state first, municipality second, with caution around redaction and underreporting.
- Fosas: clandestine graves, bodies recovered, remains, fragments, identifications. These are
  different units.
- Search collectives: collective-reported findings, official confirmations, searches that
  reveal gaps, and institutional responses after major discoveries.
- Government context: federal administrations, major reforms, protocols, commissions,
  registries, and identification systems.

## Time frame

- 2006-present: broad historical frame, useful for the geography of disappearances, violence,
  and clandestine graves.
- 2017/2019-present: stronger registry frame, because the national system and RNPDNO era make
  comparisons more defensible.
- 2025-present: policy-break frame, because the Ley General was reformed on 2025-07-16,
  including changes such as the Alerta Nacional de Busqueda and the Base Nacional de Carpetas
  de Investigacion.

## Legal and institutional timeline question

Major collective discoveries and family pressure appear alongside legal and institutional
responses. We will build a timeline and compare what changed on paper versus what changed in
outcomes.

Do not claim that madres buscadoras "caused" a law, budget change, or institutional response
unless the evidence supports that causal claim. Safer categories:

- preceded
- coincided with
- was cited by officials or legislators
- was demanded by families / collectives
- was followed by
- appears in the same policy cycle as

## Ethics rules

Do not publish:

- exact active search locations or GPS points
- private names unless already public and necessary
- children's identifying details
- family phone numbers or personal social accounts
- unverified accusations
- cartel labels unless sourced
- graphic images
- "voluntary disappearance" claims without context
- exact locations that could endanger searchers, families, witnesses, or evidence

Always separate:

- confirmed
- reported
- alleged
- official
- collective-reported
- media-reported

This distinction is not cosmetic. It protects both people and the credibility of the analysis.

