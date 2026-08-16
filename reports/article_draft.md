# DRAFT — The Redacted Crisis: How Mexico's Registry of the Disappeared Hides What It Counts

Draft v1.1, 2026-08-15 (data refreshed; see `docs/data-refresh-2026-08-15.md`).
Visual-led web article. ~2,900 words + 8 figures.
Language: drafted in English; decide EN/ES (or both) before publication — the natural
home for this piece (and its sources) is Spanish-language.
Every figure is reproducible from `src/`; every number carries a consultation date in
`docs/`. Figure production notes at the end.

Delivery note: this markdown is the narrative source and `reports/article.html` is its
generated local output. Do not publish or update this article through Claude Artifacts.
Build with `python src/build_page.py`, validate with `python src/check_article.py`, and
preview at `http://127.0.0.1:8794/article.html` using the repository's local server.

Working titles (pick one):
1. *The Redacted Crisis: what Mexico's registry of the disappeared won't let you see*
2. *134,000 people, one third behind a wall*
3. *Two ways to disappear twice: redacted in Jalisco, uncounted in Guerrero*

Standfirst: *On 15 August 2026 Mexico's official registry counted 134,268 people still
missing. In the latest comparable record-level snapshot, dated 2 December 2025, 36.8%
of unresolved records revealed only the state; every other public field was redacted.
This is the story of how publication decisions shape what the public can see.*

---

## 1. The crisis is real, and it is growing

**[FIG A — `figures/article/A_outcomes_by_year.png`]**
*Caption: Recorded year-of-disappearance cohorts in Mexico, 2000–2025, decomposed by
current registry outcome. Use the control to switch between counts and shares. These
are current statuses, not dates on which anybody was found. Source: RNPDNO dashboard
API, consulted 2026-08-15; 214,643 found alive, 20,551 found dead and 117,100 still
missing across the period.*

Start with the honest version of the number. On August 15th 2026 Mexico's National
Registry of Disappeared and Missing Persons (RNPDNO) contained 407,253 records:
249,502 people recorded as found alive, 23,483 found dead and 134,268 still missing.
Those are current registry statuses, not dates on which anybody was found.

Figure A looks at the subset assigned a year of disappearance between 2000 and 2025.
Across those cohorts the registry currently records roughly 214,600 found alive,
20,600 found dead and 117,100 still missing. The gap between those figures and the
headline totals consists mainly of records without a usable year and records outside
the chart's period.

Three things can be read from the chart, provided its limits stay visible:

- **Recent recorded cohorts are much larger.** The registry assigns roughly 3,000
  reports to 2007 and 37,124 to 2025. Unlike a cumulative line, each bar represents
  one recorded year-of-disappearance cohort. Delayed reporting and later registry
  revisions still mean that the bars are not a perfect measure of annual incidence.
- **Most post-2008 cohorts are currently recorded as roughly two-thirds located.**
  The shares include 65% of the 2008 cohort, 75% of 2014 and 68% of 2025. Because
  those cohorts have had radically different follow-up periods, this is a descriptive
  registry pattern — not a measure of search effectiveness.
- **The chart cannot show when a status changed.** A person assigned to the 2014
  cohort may have been located in 2014 or years later. Nor can the public aggregate
  data distinguish a confirmed recovery from every administrative correction or
  reclassification captured by the category "located".

(The bars for 2000–2005 look dramatic in percentage form, but each covers only a few
hundred people. The article does not use those small cohorts to infer a trend.)

## 2. Where unresolved stock is greatest per resident

**[FIG B — `figures/article/B_rate_map.png`]**
*Caption: Unresolved disappearances per 100,000 residents by state, from the
record-level registry snapshot of 2025-12-02. Tamaulipas (359), Zacatecas (226)
and Sinaloa (211) lead by rate; Estado de México (82) and CDMX (79), the leaders
in absolute counts, fall to around 80. Note: on the live registry consulted
2026-08-15, CDMX's unresolved count has since fallen by ~1,300 (a rate of ~64) —
see §5b.*

Mexico's disappeared are not distributed the way Mexicans are. Estado de México and
Mexico City register the most cases in absolute terms, which is unsurprising: they
are where the most people live. Divide by population and the map rearranges itself.

The national rate is 98 unresolved records per 100,000 residents. Tamaulipas, on the
northeastern border, runs at 359 — more than four times Estado de México's 82. Behind
it come Zacatecas (226) and Sinaloa (211). This is a map of the unresolved registry
stock, not of underlying risk: differences in reporting, resolution and publication
practice all affect where a state appears.

This is the ordinary way to read registry data, and for one paragraph it works.
Hold onto it. The next chart takes it apart.

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

## 4. State violence does not explain confidentiality

**[FIG D — `figures/article/D_redaction_vs_rate.png`]**
*Caption: Confidential share vs cumulative homicide-victim rate, 2015–2025, by
state. Higher state-level violence is not associated with more confidentiality; the
relationship is moderately negative (Pearson r = −0.38, 32 states). This ecological
comparison is descriptive, not a test of risk in individual cases.*

There is an innocent explanation for all this redaction, and it deserves a fair test.

If statewide danger were the principal explanation for interstate variation in
confidentiality, states with higher homicide rates should generally redact more.

The data do not show that pattern. Across all 32 states, the correlation between the
confidential share and the cumulative homicide-victim rate for 2015–2025 is
*negative* — −0.38. Several of the most violent states are among those publishing the
largest share of registry details.
Colima has recorded roughly 950 homicides per 100,000 residents since 2015, the worst
rate in the country; it redacts 9% of its disappearance records. Guerrero, at 550,
redacts 9%. Chihuahua, at 548, redacts 9%.

Now look at the other end of the scale. Jalisco's homicide rate is less than half
Guerrero's, and it redacts 67%. Yucatán has both the lowest homicide rate and the
lowest unresolved-record rate in Mexico — 18 and 12.5 per 100,000 respectively — yet
redacts 62% of its records.

State-level homicide rates therefore do not explain the publication pattern. That
does not rule out genuine danger in individual cases; it tells us to investigate the
administrative process as well.

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

**The redaction flag mixes genuine family requests, missing consent paperwork and at
least one blanket state policy — and no public field distinguishes them.**


### 5b. The public totals sometimes move in batches

**[FIG H — `figures/article/H_confidencial_batches.png`]**
*Caption: CONFIDENCIAL records per state across ten monthly snapshots of the public
registry, April–December 2025, recovered from the mirror's version history.
Nationally, confidential records grew 44,035 → 49,136 (+5,101) — 77% of the
registry's entire net growth in those eight months.*

If confidentiality were updated one family decision at a time, we might expect it to
move gradually. Instead the published count sometimes jumps. Tamaulipas added ~2,500
confidential records in two months (May–July 2025) while its total barely moved;
its redaction share went from 20% to 39%, and every chart in this piece would have
looked different had we pulled the data in April. Jalisco's confidential count was
flat all year, then fell by ~1,400 in the last quarter as the state's overall federal
count also fell — months before the new recount was announced. Tabasco's published
total fell by a third in a single month.

The reversals do not stop at the edge of the panel. Mexico City's unresolved count
climbed steadily all through 2025, from 6,025 in April to 7,242 in December — and
then gave the entire increase back. By June 2026 the live registry showed 6,086;
by August, 5,915. A capital that had been adding cases for a year shed 1,327 of
them in eight months, roughly one in five. We can see the direction and the size of
that reversal but not its mechanism: the registry does not say whether those
records were deleted, reclassified, resolved, or moved.

Step changes and flat totals while confidentiality changes are consistent with bulk
administrative processing. The snapshots cannot reveal whether the
underlying records reflect consent, correction, resolution, deletion or another
operation. They do show that the registry's most basic public property — *how much of
it you can see* — can be rewritten in bulk with no public change log explaining why.

## 6. Jalisco: opacity by redaction

**[FIG F — `figures/article/F_jalisco_divergence.png`]**
*Caption: Jalisco's registry conflict, 2020–2026: blanket confidentiality declared
(2020), the state stops feeding the national registry in favour of its own (2022),
"erased" names controversy (2023), official denial (2024), Teuchitlán (2025), new
federal recount (2026). The two registries move independently and now differ by
roughly 3,000 people — the federal count fell to 12,776 by June 2026 and has since
edged back to 12,964, while the state's stands near 16,000. Markers are documented
snapshots, not a continuous series, and the two registries define their counts
differently.*

Jalisco redacts more of its registry than any other state in Mexico: 9,216 of its
13,766 unresolved records, two out of every three. It is also the state that stopped
fully participating in the national count.

From 2022, under then-governor Enrique Alfaro, Jalisco largely stopped reporting
disappearances to the RNPDNO and logged them in its own state registry instead. The
country now has two official counts of Jalisco's disappeared, kept by two governments,
and they do not agree with each other. Animal Político put the resulting gap at up to
2,986 people. The state government's answer, in January 2024, was a communiqué titled
"Jalisco does not manipulate its registry, nor erase figures."

Jalisco is also where the contradiction from section 5 concentrates. Of the 4,765
confidential-yet-publicly-searched-for cases ZonaDocs identified, 1,026 are Jalisco's —
more than any other state. The same investigation found a further 2,137 disappearances
between 2019 and mid-2024 that were never registered anywhere at all: not redacted,
simply absent.

What the registry would not record, families recorded themselves. On 5 March 2025 the
collective Guerreros Buscadores de Jalisco entered Rancho Izaguirre, a property outside
Teuchitlán, and found a cartel recruitment and extermination site: clothing, shoes,
backpacks, notebooks, bone fragments. It became a national scandal — not only for what
was on the ranch, but because a group of searching families, rather than the state, was
what finally established it.

Searching in Jalisco is lethal work. In 2025 Teresa González Murillo was attacked and
died. María del Carmen Morales, of Guerreros Buscadores, was murdered alongside one son
while searching for another.

The state with the most redacted registry in Mexico is also the state where civil
society keeps producing the evidence its registry lacks. Those are not two facts about
Jalisco. They are one fact, seen from two sides.

## 7. Guerrero: the limits of official counts

**[FIG G — `figures/article/G_two_modes.png`]**
*Caption: Guerrero's December 2025 federal stock contains 4,453 unresolved records.
In Iguala, three family collectives jointly document 623 cases. The person-level
overlap is unknown, so the figures cannot be added or subtracted. Collectives are
credited with locating 260+ bodies in Iguala and ~70 in Acapulco. Sources:
Tlachinollan, HRW, consulted 2026-07-06.*

On the redaction chart, Guerrero appears unusually open: 9% confidential, against
Jalisco's 67%. But a low confidential share describes only records that have entered
the federal stock. It cannot tell us how completely the registry covers disappearances
known to families and collectives.

The state registers roughly 3,800–4,500 disappeared people. In Iguala alone — one city
— three family collectives jointly document 623 cases. These figures may overlap:
without person-level linkage, the 623 cannot be added to the state total or treated as
623 proven omissions. They do establish a parallel record maintained by families.
The human-rights centre
Tlachinollan, which has tracked the state for decades, describes prosecutors who stall
investigations unless families force them open, and a forensic service that has
effectively collapsed. Nationally, between 2% and 6% of disappearance cases are ever
prosecuted; there have been 36 sentences in the entire country.

The modern searching-mothers movement was, in an important sense, born here. When the
43 students from Ayotzinapa disappeared in September 2014, families searching the hills
around Iguala for them began instead to find other people: graves of the dead nobody
was officially looking for. The collective that formed out of that search, Los Otros
Desaparecidos de Iguala, has since exhumed more than 160 bodies. Tlachinollan credits
women-led collectives — not state institutions — with locating over 260 bodies in
Iguala and around 70 in Acapulco.

The under-registration is not history. During Holy Week searches in 2026, in Iguala and
Buenavista de Cuéllar, three families approached the searching mothers to report
disappearances they had never reported to any authority. That is the gap happening in
real time: people becoming known to a collective before they are known to the state.

A low confidential share, then, is not a clean bill of health. Jalisco documents how
fields can disappear after a record enters the registry. Guerrero's family records
show why coverage before that point must be investigated separately. The project
cannot measure Guerrero's under-registration from these sources because the official
and collective lists have not been linked person by person.

## 8. What this means — and what we cannot claim

No chart in this piece supports the sentence "the state deliberately hides its
disappeared." What the evidence supports is narrower and, for data users, more
important:

- The public registry's confidentiality flag is **unexplained, unaudited, and in
  thousands of documented cases contradicted by the authorities' own public search
  notices**.
- Cross-state comparisons of registry data measure *institutional publication
  practice* as much as they measure disappearance.
- There are two distinct visibility problems: **fields redacted inside the registry,
  and disappearances documented by families outside it**. Their overlap must be
  measured before the second can be called an undercount.
- Families and collectives provide an essential parallel record, but the registry does
  not provide the identifiers needed to reconcile the two systems publicly.

That is the subject of the next piece.

---

## Methods note (publish as expandable box or footer)

Data: this piece draws on **two vintages, and says so deliberately.** Aggregate
outcome flows (fig A) come from the live RNPDNO dashboard API, consulted
**2026-08-15**. Everything field-level — redaction shares, per-capita rates, the
state rankings in figs B, C, D — comes from the registry's public *record-level*
microdata via the [lapanquecita mirror](https://github.com/lapanquecita/personas-desaparecidas)
(133,566 records, snapshot **2025-12-02**,
upstream commit 666b3e7; max FECHA_REGISTRO 2025-12-01). The two cannot be
aligned: the mirror stopped updating after 2025-12-02, having published monthly
since April 2025, and no comparable record-level extract has been released since.
The gap is measurable and small — the mirror's national total sits within 0.5% of
the live registry (0.1% across state-attributable records) — but it is not uniform
by state, and §5b is in part about exactly that. Where a state's live figure has
since moved materially (Ciudad de México, Jalisco), we say so in the caption.

Cross-checks: category-sensitivity tested (DESAPARECIDA vs +NO LOCALIZADA:
national +6.1%, but Zacatecas +42%); Jalisco remains the volatile outlier across
sources. Redaction-over-time: ten pinned monthly snapshots of the mirror
(Apr–Dec 2025, upstream commit SHAs in `src/version_audit.py`). All figures
reproducible from `src/` in the project repository
(https://github.com/heliog83/desaparecidos-mx). Confidential records are counted as
unresolved people but excluded from any
field-level analysis. Full methodology:
[methodology](https://github.com/heliog83/desaparecidos-mx/blob/main/docs/methodology.md);
refresh audit and full number-by-number diff:
[data refresh audit](https://github.com/heliog83/desaparecidos-mx/blob/main/docs/data-refresh-2026-08-15.md).
Key primary
sources: Oficio SEGOB/CNBP/1349/2020; ZonaDocs (2024-11-21); A dónde van los
desaparecidos (2021-04-08); Data Cívica, Volver a desaparecer; Tlachinollan; HRW
(2019-01-14). All web sources consulted 2026-07-06 unless noted.

Ethics line (keep): behind every record is a person and a searching family. This
piece reports uncertainty as uncertainty and does not present proxies as counts.

---

## FIGURE PRODUCTION NOTES (the data-viz workplan)

STYLE PASS DONE (updated 2026-08-16): all 8 publication figures live in
`reports/figures/article/` (A–H), built by `src/article_figs.py` (A–D) and
`src/consent_accounting.py` / `src/jalisco_divergence.py` / `src/two_modes.py`
(E–G; these also still emit the numbered pipeline versions), plus
`src/version_audit.py` (H). Shared palette,
typography and caption format in `src/article_style.py` — edit there to restyle
the whole set.

- **FIG A.** One-panel stacked cohorts with direct outcome labels and a careful
  current-status caveat. The page adds a counts/share toggle and exact tooltips.
- **FIG B = fig 06 + 05.** Choropleth needs a discrete legend (rates bin better
  than continuous), and top-3 state labels on the map itself.
- **FIG C = fig 09 or 04.** Horizontal ranking, national reference line at 36.8%,
  Jalisco/Nayarit/Guerrero/Colima emphasized.
- **FIG D.** Confidential share against the cumulative homicide-victim rate,
  2015–2025; all 32 states, highlighted outliers, Pearson r = −0.38. This is an
  ecological description, not a causal or individual-risk model.

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
  (Mar 2025) → 12,776 (our API pull, 2026-06-19, after the new federal recount)
  → 12,964 (second API pull, 2026-08-15: the count is edging back up, +188 in ~8
  weeks, while the state registry stays ~3,000 higher);
  state 13,976 (SISOVID Mar 2023) → 15,426 (REPD Feb 2025) → 16,064 (end 2025).
  Six event markers 2020–2026. CAVEAT kept in footer: registry definitions differ;
  the 2026 federal drop coincides with the announced recount (A dónde van los
  desaparecidos, 2026-01-08) — say "coincides", do not assert cause.
- **fig 22 — parallel evidence systems (for §7).** BUILT:
  `src/two_modes.py` → `figures/22_two_modes_of_opacity.png`. Left: Jalisco's
  documented denominator and redaction path. Right: Guerrero's official statewide
  stock and the Iguala collective record shown as separate evidence boxes, with
  overlap explicitly unknown. They are not placed on a shared quantitative scale.

The standalone article now embeds three dependency-free responsive interactives:
Figure A switches counts/shares; Figure B ranks and inspects every state by rate,
count or confidential share; Figure H explores every stored national or state
snapshot. Static figures remain in `<noscript>` fallbacks.
