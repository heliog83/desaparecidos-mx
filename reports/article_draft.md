# DRAFT — The Redacted Crisis: How Mexico's Registry of the Disappeared Hides What It Counts

Draft v1, 2026-07-06. Visual-led web article. ~2,800 words + 7 figures.
Language: drafted in English; decide EN/ES (or both) before publication — the natural
home for this piece (and its sources) is Spanish-language.
Every figure is reproducible from `src/`; every number carries a consultation date in
`docs/`. Figure production notes at the end.

Working titles (pick one):
1. *The Redacted Crisis: what Mexico's registry of the disappeared won't let you see*
2. *132,000 people, one third behind a wall*
3. *Two ways to disappear twice: redacted in Jalisco, uncounted in Guerrero*

Standfirst: *Mexico's official registry counts more than 132,000 disappeared people.
For one in three of them, the public record contains a single fact: the state where
they vanished. This is the story of who decides that — and of the two very different
ways a person can go missing from the data itself.*

---

## 1. The crisis is real, and it is growing

**[FIG A — `figures/article/A_outcomes_by_year.png`]**
*Caption: Every year of reported disappearances in Mexico, 2000–2025, decomposed into
people found alive, found dead, and still missing. Two panels: absolute counts and
shares. Source: RNPDNO dashboard API, consulted 2026-06-19; ~212,900 found alive, ~19,900
found dead, ~118,600 still missing across the period.*

Start with the honest version of the number, because almost nobody publishes it.
Mexico's National Registry of Disappeared and Missing Persons (RNPDNO) is usually
quoted as a single figure — 132,000+ disappeared. But the registry is a *stock*, not a
history: it counts people missing *right now*. The fuller accounting, pulled from the
registry's own API, is that since 2000 roughly 350,000 disappearances have been
reported; most people were found alive, about 20,000 were found dead, and nearly
120,000 have never been found.

Two things in this chart survive every methodological caveat we could throw at them
(and we threw several — see methods note):

- **The growth is real incidence, not an artifact of accumulation.** Reported
  disappearances rose from ~100/year in 2000 to ~3,000 at the drug-war onset in
  2007 to ~37,000 in 2025.
- **The unresolved share behaves the opposite of intuition:** older cohorts are *less*
  resolved (~16–27%) than recent ones (~65–70%). Time does not find people; it
  buries the cases.

## 2. Where people disappear — once you divide by population

**[FIG B — `figures/article/B_rate_map.png`]**
*Caption: Unresolved disappearances per 100,000 residents by state. Tamaulipas
(359), Zacatecas (226) and Sinaloa (211) lead by rate; Estado de México and CDMX,
the leaders in absolute counts, fall to ~80.*

One paragraph of geography, because it sets up the puzzle: the map of disappearance
is not the map of population. Per-capita, the northeastern corridor and the
Pacific trafficking routes dominate. Keep this section short — its job is to
establish that we *can* compare states… which is exactly what the next chart breaks.

## 3. The wall: one in three records is blank

**[FIG C — `figures/article/C_confidential_share.png`]**
*Caption: Share of each state's unresolved records marked CONFIDENCIAL in the public
registry. National: 36.8%. Jalisco: 67%. Nayarit: 66%. Guerrero and Colima: 9%. A
confidential record retains exactly one public fact — the state.*

Here is what "consulting the public registry" actually gets you: for 36.8% of
unresolved records, every field is redacted — no date, no age, no sex, no
municipality, no case status. One fact survives: the state. This is why national
trend charts and state comparisons are built on different denominators, and why
every chart in this piece says so.

The redaction is not evenly spread. Jalisco redacts two of every three records.
Guerrero, one of the most violent states in the country, redacts one in eleven.

## 4. Redaction does not follow violence

**[FIG D — `figures/article/D_redaction_vs_rate.png`]**
*Caption: Confidential share vs disappearance rate, by state. If redaction were a
by-product of crisis intensity, states would line up. They don't: Guerrero has ~2.4×
Jalisco's homicide rate and one-seventh of its redaction share.*

If confidentiality were protecting families in the most dangerous places, the most
violent states would redact the most. The scatter says otherwise. Whatever drives
redaction, it is not violence. So what is it?

## 5. Who decides a record goes dark

**[FIG E — `figures/article/E_consent_accounting.png`]**
*Caption: The CNB's own accounting of publication consent, Aug 2020 (73,388
records): for 77.4%, no consent information exists at all. Among the minority of
family reporters actually asked, 52% declined publication, 47% agreed. Source:
Oficio SEGOB/CNBP/1349/2020, pp. 5, 11.*

On paper, the rule is humane and simple. Article 108 of the General Law on
Disappearances gives families the right to keep their loved one's information out
of the public registry, and requires that they be told of this right before giving
information. Redaction, officially, means "the family asked."

The government's own paperwork says otherwise. In August 2020 the National Search
Commission (CNB) wrote to the transparency institute (INAI) asking how to build the
public registry — and admitted, in its own tables, that **for 77.4% of records
nobody knew whether the family had consented or not**, largely because the records
predate the law. Where no paperwork exists, the default is silence. And in a
footnote, the CNB recorded something remarkable: the Fiscalía of Jalisco had
declared that *everything* it sends to the national registry is non-publishable,
invoking family refusals it has never had to evidence.

When INAI later ordered the CNB to release a public database (resolution RRA
09082/20), the commission resisted — citing family consent it could not produce —
and eventually delivered 50,204 records out of 175,371.

Journalists then closed the loop. In 2024, ZonaDocs found 4,765 cases across six
states that are marked confidential in the registry *while having active public
search notices* — posters with names and photographs, issued by the same
authorities. Officials admitted no risk assessment underlies the classification.
María de Jesús Solís, whose son disappeared in Zapopan in 2020, said she never
signed anything and wants maximum visibility. Her son's record is confidential.

**The redaction flag is an administrative artifact — a mixture of genuine family
requests, missing paperwork defaulting to silence, and at least one blanket state
policy — and no public field distinguishes them.**


### 5b. And the flag moves in batches

**[FIG H — `figures/article/H_confidencial_batches.png`]**
*Caption: CONFIDENCIAL records per state across ten monthly snapshots of the public
registry, April–December 2025, recovered from the mirror's version history.
Nationally, confidential records grew 44,035 → 49,136 (+5,101) — 77% of the
registry's entire net growth in those eight months.*

If confidentiality reflected family choices, it would drift — a few records at a
time, in every state. Instead it jumps. Tamaulipas reclassified ~2,500 existing
records to confidential in two months (May–July 2025) while its total barely moved;
its redaction share went from 20% to 39%, and every chart in this piece would have
looked different had we pulled the data in April. Jalisco's confidential count was
flat all year, then fell by ~1,400 in the last quarter as records left the federal
registry entirely — months before the new recount was announced. Tabasco deleted a
third of its records in a single month.

Step changes, flat totals during reclassifications, batch deletions: these are the
signatures of administrative operations, not of thousands of families changing
their minds in the same week. This is the version-history evidence for the claim in
section 5 — and it means the registry's most basic public property, *how much of it
you can see*, is being rewritten in bulk, state by state, with no public log of who
decided or why.

## 6. Jalisco: opacity by redaction

**[FIG F — `figures/article/F_jalisco_divergence.png`]**
*Caption: Jalisco's registry conflict, 2020–2025: blanket confidentiality declared
(2020), the state stops feeding the national registry in favor of its own (2022),
"erased" names controversy (2023), official denial (2024), Teuchitlán (2025).
Federal vs state registry totals diverge by hundreds of cases.*

Jalisco has the largest number of unresolved cases among large states and redacts
67% of them. It also, since 2022, effectively seceded from the national registry:
disappearances were logged in the state's own registry (REPD) and stopped flowing
to the RNPDNO — a gap critics put at up to ~3,000 people, and which the state
government answered with a communiqué titled "Jalisco does not manipulate its
registry, nor erase figures." Today the federal and state registries disagree with
each other by hundreds of cases at any given cut-off date.

What the registry would not document, families did. In March 2025 the collective
Guerreros Buscadores de Jalisco entered Rancho Izaguirre in Teuchitlán and found a
cartel recruitment-and-extermination site: clothing, shoes, backpacks, notebooks
with names, bone fragments. That year two searchers from Jalisco collectives were
killed. The state with the most redacted registry in Mexico is also the state
where civil society keeps producing the evidence the registry lacks.

## 7. Guerrero: opacity by omission

**[FIG G — `figures/article/G_two_modes.png`]**
*Caption: Guerrero registers ~3,800–4,500 disappeared. In Iguala alone, three
family collectives jointly document 623 cases. Collectives — not the state — have
located 260+ bodies in Iguala and ~70 in Acapulco. Sources: Tlachinollan, HRW,
consulted 2026-07-06.*

Guerrero looks, on the redaction chart, like the transparent one: 9% confidential.
The same federal consent rules apply there — its search commission's privacy notice
mirrors the national architecture almost word for word. The difference is what
happens *before* a record can be redacted: in Guerrero, cases often never enter the
registry at all.

Human-rights monitors and the collectives born after Ayotzinapa — Los Otros
Desaparecidos de Iguala, who have exhumed more than 160 bodies from the hills
around the city — document systematically more disappeared than the state
registers. Prosecutors stall or discourage reports. During Holy Week searches in
2026, three families approached the searching mothers to report disappearances
they had never reported to any authority.

A low confidential share is not good news. It can mean the missing were never
counted.

## 8. What this means — and what we cannot claim

No chart in this piece supports the sentence "the state deliberately hides its
disappeared." What the evidence supports is narrower and, for data users, more
important:

- The public registry's confidentiality flag is **unexplained, unaudited, and in
  thousands of documented cases contradicted by the authorities' own public search
  notices**.
- Cross-state comparisons of registry data measure *institutional publication
  practice* as much as they measure disappearance.
- Opacity has two modes — **redacting what is recorded, and never recording** — and
  a state can look clean on one axis while failing badly on the other.
- In both modes, the gap is being filled by the same people: the families and
  collectives searching, counting, and digging where the record ends.

That is the subject of the next piece.

---

## Methods note (publish as expandable box or footer)

Data: RNPDNO public microdata via the [lapanquecita mirror] (133,566 records,
snapshot 2025-12-02, upstream mirror commit 666b3e7; max FECHA_REGISTRO 2025-12-01), cross-checked against the live RNPDNO dashboard API
(national drift −0.7%; Jalisco the volatile outlier) and category-sensitivity
tested (DESAPARECIDA vs +NO LOCALIZADA: national +6.1%). Outcome flows pulled
directly from the registry API. Redaction-over-time: ten pinned monthly snapshots
of the mirror (Apr–Dec 2025, upstream commit SHAs in `src/version_audit.py`). All figures reproducible from `src/` in [repo
link]. Confidential records are counted as unresolved people but excluded from any
field-level analysis. Full methodology: [link docs/methodology.md]. Key primary
sources: Oficio SEGOB/CNBP/1349/2020; ZonaDocs (2024-11-21); A dónde van los
desaparecidos (2021-04-08); Data Cívica, Volver a desaparecer; Tlachinollan; HRW
(2019-01-14). All web sources consulted 2026-07-06 unless noted.

Ethics line (keep): behind every record is a person and a searching family. This
piece reports uncertainty as uncertainty and does not present proxies as counts.

---

## FIGURE PRODUCTION NOTES (the data-viz workplan)

STYLE PASS DONE (2026-07-06): all 7 publication figures live in
`reports/figures/article/` (A–G), built by `src/article_figs.py` (A–D) and
`src/consent_accounting.py` / `src/jalisco_divergence.py` / `src/two_modes.py`
(E–G; these also still emit the numbered pipeline versions). Shared palette,
typography and caption format in `src/article_style.py` — edit there to restyle
the whole set. Remaining viz decisions, if any, are ES caption pairs and any
personal design touches. Original per-figure notes kept below for reference:

- **FIG A = fig 19** (signature). Already the strongest asset. Add direct labels on
  the three bands; consider annotating 2007 (drug-war onset) and the resolution
  gradient.
- **FIG B = fig 06 + 05.** Choropleth needs a discrete legend (rates bin better
  than continuous), and top-3 state labels on the map itself.
- **FIG C = fig 09 or 04.** Horizontal ranking, national reference line at 36.8%,
  Jalisco/Nayarit/Guerrero/Colima emphasized.
- **FIG D = fig 10 or 14.** Grey all states except the four case states; annotate
  the two axes in plain language ("more redacted →", "more disappearances →").

New figures — ALL BUILT (baseline styling; restyle pass pending):

- **fig 20 — consent accounting (for §5).** BUILT: `src/consent_accounting.py` →
  `figures/20_consent_accounting.png`. Stacked bar of the 73,388 Aug-2020 records:
  77.4% "no consent info" / family-asked split 52/47 refuse/agree. Data hardcoded
  from the oficio (pp. 5, 11) — cited, not derived. Known issue: labels cramped on
  the two narrow segments.
- **fig 21 — Jalisco divergence timeline (for §6).** BUILT: `src/jalisco_divergence.py`
  → `figures/21_jalisco_registry_divergence.png`. Documented snapshots (markers, not
  a series): federal 14,944 (Apr 2022) → 15,012 (May 2023, i.e. +68 in 13 months
  while the state issued 1,260 bulletins — annotated as "the freeze") → 15,015
  (Mar 2025) → 12,776 (our API pull, 2026-06-19, after the new federal recount);
  state 13,976 (SISOVID Mar 2023) → 15,426 (REPD Feb 2025) → 16,064 (end 2025).
  Six event markers 2020–2026. CAVEAT kept in footer: registry definitions differ;
  the 2026 federal drop coincides with the announced recount (A dónde van los
  desaparecidos, 2026-01-08) — say "coincides", do not assert cause.
- **fig 22 — the two modes (for §7, the thesis chart).** BUILT (safer option 2):
  `src/two_modes.py` → `figures/22_two_modes_of_opacity.png`. Left: Jalisco 13,766
  split 67% CONFIDENCIAL / 33% public, annotated with the 1,026
  active-notice-yet-confidential cases. Right: Guerrero 4,453 statewide (9%
  confidential) beside the 623 Iguala collective-documented bar, shared y-scale,
  footer states explicitly that denominators differ and the Iguala figure is a
  documented example, not a comparable measurement.

Interactive (optional, dashboard cross-link): fig 16's interactive typology is the
natural embed; update its language per the memo ("administrative redaction
artifact", omission caveat) before linking.
