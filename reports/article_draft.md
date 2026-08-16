# DRAFT — The Redacted Crisis: How Mexico's Registry of the Disappeared Hides What It Counts

Draft v1.1, 2026-08-15 (data refreshed; see `docs/data-refresh-2026-08-15.md`).
Visual-led web article. ~2,900 words + 8 figures.
Language: drafted in English; decide EN/ES (or both) before publication — the natural
home for this piece (and its sources) is Spanish-language.
Every figure is reproducible from `src/`; every number carries a consultation date in
`docs/`. Figure production notes at the end.

Working titles (pick one):
1. *The Redacted Crisis: what Mexico's registry of the disappeared won't let you see*
2. *134,000 people, one third behind a wall*
3. *Two ways to disappear twice: redacted in Jalisco, uncounted in Guerrero*

Standfirst: *Mexico's official registry recorded 134,268 people as disappeared or not
located on 15 August 2026. For one in three of them, the public record contains a
single fact: the state where they vanished. This is the story of who decides that —
and of the two very different ways a person can go missing from the data itself.*

---

## 1. The crisis is real, and it is growing

**[FIG A — `figures/article/A_outcomes_by_year.png`]**
*Caption: Top — the current recorded status of all 407,253 people in the registry:
249,502 found alive, 23,483 found dead, 134,268 still missing. Bottom — the same
records arranged by the year the person disappeared. Both panels show status as
recorded on one day, 15 August 2026; neither shows when a case changed status.
Aggregate figures: RNPDNO dashboard API, consulted 2026-08-15 [1].*

Start with the honest version of the number, because almost nobody publishes it.
Mexico's National Registry of Disappeared and Missing Persons (RNPDNO) is usually
quoted as a single figure — more than 134,000 disappeared. That figure is real: on
15 August 2026 the registry recorded **134,268** people as disappeared or not located.
But it is a *stock*, not a history. It counts people recorded as missing at that
moment, out of **407,253** records in total: 249,502 of them recorded as found alive,
23,483 as found dead.

Read the chart as a photograph, not a film. Every number in it is a status **as
recorded on 15 August 2026**. The registry publishes what a case looks like now; it
does not publish when a case changed, or who changed it. So the top panel is a census
of the present, and the bottom panel sorts that same census by the year each person
went missing.

Three things in this chart hold up, stated as narrowly as the data allows:

- **Recorded disappearances per year rose steeply.** The registry holds ~100 records
  for 2000, ~3,000 for 2007 as the militarised drug war began, and ~37,000 for 2025.
  This is the count of *records the state holds*, not a measurement of how many
  disappearances occurred. Reporting rates, prosecutorial practice and registry
  coverage all changed enormously over the same 25 years, and cases can still be
  registered years late — three new 2014 records appeared in an eight-week window in
  2026. Treat the shape as a floor under a growing crisis, not a census of it.
- **About two-thirds of post-2008 cohorts are currently recorded as located.** 65% of
  the 2008 cohort, 75% of 2014, 68% of 2025 [1]. But these cohorts have had wildly
  unequal time to reach that state — the 2008 group has been observed for eighteen
  years, the 2025 group for months — so this is not a like-for-like comparison, and
  it is not evidence that outcomes have held steady. It is a description of where the
  register happens to stand today.
- **Older records move very little between snapshots.** Comparing our two
  consultations, eight weeks apart, 123 records from pre-2016 cohorts moved into a
  located category, against 32,102 still recorded as missing. Annualising a single
  eight-week window gives roughly 2.5% a year — a rough snapshot estimate, not a
  measured rate, and one short window can be unrepresentative. What it does suggest
  is that the register's older strata are close to static.

Two cautions carry through the whole piece. "Located" is a **registry category, not a
verified outcome**: it includes people found alive, people found dead, and records
reclassified in administrative batches — including the contested 2023 *censo*. It is
not a measure of successful searching, and nothing here should be read as crediting
any institution with finding people. And the bars for 2000–2005 look dramatic in the
lower panel but cover only a few hundred records each, so we do not lean on them.

## 2. Where people disappear — once you divide by population

**[FIG B — `figures/article/B_rate_map.png`]**
*Caption: Unresolved disappearances per 100,000 residents by state, from the
record-level registry snapshot of 2025-12-02. Tamaulipas (359), Zacatecas (226)
and Sinaloa (211) lead by rate; Estado de México (82) and CDMX (79), the leaders
in absolute counts, fall to around 80. Note: on the live registry consulted
2026-08-15, CDMX's unresolved count has since fallen by ~1,300 (a rate of ~64) —
see §5b. Microdata vintage 2025-12-02 [3]; live comparison [1].*

Mexico's disappeared are not distributed the way Mexicans are. Estado de México and
Mexico City register the most cases in absolute terms, which is unsurprising: they
are where the most people live. Divide by population and the map rearranges itself.

The national rate is 98 unresolved disappearances per 100,000 residents. Tamaulipas,
on the northeastern border, runs at 359 — more than four times Estado de México's 82.
Behind it come Zacatecas (226) and Sinaloa (211): one state straddling the highway
corridors that run north toward the border, the other the home of the country's
oldest trafficking organisation. The states that lead by rate are the states the drug
economy moves through.

This is the ordinary way to read registry data, and for one paragraph it works.
Hold onto it. The next chart takes it apart.

## 3. The wall: one in three records is blank

**[FIG C — `figures/article/C_confidential_share.png`]**
*Caption: Share of each state's unresolved records marked CONFIDENCIAL in the public
registry. National: 36.8%. Jalisco: 66.9%. Nayarit: 66.2%. Guerrero 9.1%, Colima 9.0%.
A confidential record retains exactly one public fact — the state. Vintage 2025-12-02 [3].*

Here is what "consulting the public registry" actually gets you: for 36.8% of
unresolved records, every field is redacted — no date, no age, no sex, no
municipality, no case status. One fact survives: the state. This is why national
trend charts and state comparisons are built on different denominators, and why
every chart in this piece says so.

The redaction is not evenly spread. Jalisco redacts two of every three records.
Guerrero, one of the most violent states in the country, redacts one in eleven.

## 4. The most violent states redact the least

**[FIG D — `figures/article/D_redaction_vs_rate.png`]**
*Caption: Confidential share vs disappearance rate, by state. If redaction were a
by-product of crisis intensity, states would line up. They don't — the relationship
with violence is actually negative (r = −0.42 against homicide rate, 28 states).
Guerrero has ~2.4× Jalisco's homicide rate and one-seventh of its redaction share.
Redaction 2025-12-02 [3]; homicide rates 2015–2025 cumulative [2].*

There is an innocent explanation for all this redaction, and it deserves a fair test.

If confidentiality exists to protect families, it should be most common where
families are in the most danger. A mother in a state where the cartels read the
newspapers has an obvious reason to keep her son's name out of a public database. On
that theory, redaction should rise with violence.

The data does not support it. Across the 28 states where both measures can be
matched, redaction and homicide rate are *negatively* correlated — Pearson r = −0.42
[2]. The states carrying the heaviest violence are among the least redacted. Colima
has recorded roughly 950 homicides per 100,000 residents since 2015, the highest rate
in the country; it redacts 9% of its disappearance records. Guerrero, at 550, redacts
9%. Chihuahua, at 548, redacts 9%.

At the other end of the scale, Jalisco's homicide rate is less than half Guerrero's
and it redacts 67%. Yucatán has both the lowest homicide rate and the lowest
disappearance rate in the country — 18 and 12.5 per 100,000 — and redacts 62% of its
records.

The narrow conclusion, and the only one this supports: **state-level homicide rates
do not explain state-level differences in confidentiality.** A state's violence tells
you almost nothing about how much of its registry is readable. That does not
establish what redaction *is* tracking, and it cannot rule out risk assessments made
case by case, which no public field records. It does rule out the simplest version of
the official rationale — that redaction maps onto danger — as an explanation for why
Jalisco is at 67% and Guerrero at 9%.

So what does account for the difference?

## 5. Who decides a record goes dark

**[FIG E — `figures/article/E_consent_accounting.png`]**
*Caption: The CNB's own accounting of publication consent, Aug 2020 (73,388
records): for 77.4%, no consent information exists at all. Among the minority of
family reporters actually asked, 52% declined publication, 47% agreed. Source:
Oficio SEGOB/CNBP/1349/2020, pp. 5, 11 [4]; universe dated 2020-08-07.*

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
registry's entire net growth in those eight months. Ten pinned mirror snapshots [5].*

If confidentiality reflected family choices, it would drift — a few records at a
time, in every state. Instead it jumps. Tamaulipas reclassified ~2,500 existing
records to confidential in two months (May–July 2025) while its total barely moved;
its redaction share went from 20% to 39%, and every chart in this piece would have
looked different had we pulled the data in April. Jalisco's confidential count was
flat all year, then fell by ~1,400 in the last quarter as records left the federal
registry entirely — months before the new recount was announced. Tabasco deleted a
third of its records in a single month.

The reversals do not stop at the edge of the panel. Mexico City's unresolved count
climbed steadily all through 2025, from 6,025 in April to 7,242 in December — and
then gave the entire increase back. By June 2026 the live registry showed 6,086;
by August, 5,915. A capital that had been adding cases for a year shed 1,327 of
them in eight months, roughly one in five. We can see the direction and the size of
that reversal but not its mechanism: the registry does not say whether those
records were deleted, reclassified, resolved, or moved.

Step changes, flat totals during reclassification, batch deletions: these patterns are
**consistent with administrative processing** — records handled in bulk, by an office,
on an office's schedule. They are not proof that the underlying consent decisions are
fabricated. Families do decide, and some of those decisions are surely real; a backlog
of genuine consent forms entered in one batch would look much like this from the
outside. What the shape of the data does show is that the *timing* of publication is
governed by administrative operations rather than by when families decide, and that
the two cannot be separated from the public record.

That is the version-history counterpart to section 5. Together they support a claim
that is narrower than "the state is hiding people" and harder to dismiss: the
registry's most basic public property — *how much of it you can read* — is rewritten
in bulk, state by state, with no published log of who authorised a change or why, and
no field that distinguishes a redaction a family asked for from one that a missing form
produced.

## 6. Jalisco: opacity by redaction

**[FIG F — `figures/article/F_jalisco_divergence.png`]**
*Caption: Jalisco's registry conflict, 2020–2026: blanket confidentiality declared
(2020), the state stops feeding the national registry in favour of its own (2022),
"erased" names controversy (2023), official denial (2024), Teuchitlán (2025), new
federal recount (2026) [4]. The two registries move independently and now differ by
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

## 7. Guerrero: opacity by omission

**[FIG G — `figures/article/G_two_modes.png`]**
*Caption: Guerrero's registry holds ~3,800–4,500 records. In Iguala alone, three
family collectives jointly document 623 cases. The two bars count different things
and may overlap: some of the 623 are certainly also in the state's register, and we
cannot say how many. Tlachinollan credits collective searches with 260 bodies
recovered in Iguala, of which 69 were identified and returned to families. Sources:
Tlachinollan, HRW [4]; registry figures 2025-12-02 microdata [3].*

On the redaction chart, Guerrero is one of the clean ones: 9% confidential, against
Jalisco's 67%. The same federal consent rules apply there; its search commission's
privacy notice mirrors the national architecture almost word for word. Guerrero is not
redacting less because it has better privacy law. It is redacting less because of what
happens *before* a record can be redacted. In Guerrero, cases often never enter the
registry at all.

The state's registry holds roughly 3,800 records. In Iguala alone — one city — three
family collectives jointly document 623 cases.

Those two numbers are not a subtraction, and it matters that we say so. **They may
overlap, and we cannot measure by how much.** Some of the 623 Iguala cases are
certainly also registered with the state; others, by the collectives' account, are
not. Without case-level identifiers on both sides — which no public source provides —
there is no way to net one against the other. The comparison is worth making because
of the ratio it implies: three collectives in one city hold a caseload equal to a
sixth of the entire state register. It is not worth making as an estimate of how many
people are missing from that register.

The human-rights centre Tlachinollan, which has tracked the state for decades,
describes prosecutors who stall investigations unless families force them open, and a
forensic service that has effectively collapsed. Nationally, between 2% and 6% of
disappearance cases are ever prosecuted; there have been 36 sentences in the entire
country [4].

The modern searching-mothers movement was, in an important sense, born here. When the
43 students from Ayotzinapa disappeared in September 2014, families searching the hills
around Iguala for them began instead to find other people: graves of the dead nobody
was officially looking for. The collective that formed out of that search, Los Otros
Desaparecidos de Iguala, has since exhumed more than 160 bodies. Tlachinollan credits
women-led collectives — not state institutions — with the recovery of 260 bodies in
Iguala, of which 69 were identified and returned to their families. In Acapulco it
records a different outcome: 70 people found alive, and 55 identified bodies returned
[4].

The under-registration is not history. During Holy Week searches in 2026, in Iguala and
Buenavista de Cuéllar, three families approached the searching mothers to report
disappearances they had never reported to any authority. That is the gap happening in
real time: people becoming known to a collective before they are known to the state.

A low confidential share, then, is not a clean bill of health. Jalisco's registry hides
what it holds; Guerrero's is missing what it never took in. A state can look
transparent on the redaction chart precisely because it failed at the earlier step.

The two modes are not opposites, and no state is purely one or the other — Jalisco's
2,137 unregistered cases are omission, sitting alongside its redaction. They are two
different points at which a person can vanish from the public record: before the state
writes anything down, and after. Guerrero shows you the first clearly. Jalisco shows
you the second. Most states are doing some of both, and the registry gives you no way
to tell how much.

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

**This piece draws on two data vintages that cannot be merged, and every figure is
labelled with the one it uses.** They answer different questions and carry different
cutoff dates. Reading a number from one against a number from the other will give a
wrong answer.

**[1] Aggregate outcomes — vintage 2026-08-15 (live).** All-record totals and the
by-year outcome breakdown in fig A. Source: RNPDNO public dashboard API, captured
2026-08-15 23:49 America/Mexico_City. Covers every record including confidential ones,
because the dashboard counts records it will not display. Totals: 407,253 records —
249,502 recorded found alive, 23,483 found dead, 134,268 disappeared or not located.
Frozen with source hashes at `data/publication_freezes/2026-08-15/`.

**[2] Homicide and state-capacity variables — vintage 2015–2025 cumulative.**
SESNSP homicide victims aggregated 2015–2025 per 100,000; INEGI ENCIG 2025
(corruption prevalence) and PIBE 2024 (GDP per capita). Matched to 28 of 32 states.
Used only for the correlations in §4 and the negative controls in
`docs/methodology.md` §7.

**[3] Record-level microdata — vintage 2025-12-02 (frozen).** Every field-level figure:
redaction shares, per-capita rates, and the state rankings in figs B, C and D. Source:
the public RNPDNO record-level extract via the
[lapanquecita mirror](https://github.com/lapanquecita/personas-desaparecidas) —
133,566 records, upstream commit 666b3e7605, max FECHA_REGISTRO 2025-12-01. **This
mirror stopped publishing after 2025-12-02**, having released monthly since April 2025,
and no comparable record-level extract has appeared since. Our copy is byte-identical
to the last upstream commit.

Drift between [1] and [3] is small nationally — the mirror sits within 0.5% of the live
registry, 0.1% across state-attributable records — but **it is not uniform by state**.
Ciudad de México has since fallen 18% and Jalisco 6% against the frozen microdata;
both carry their live figures in the caption. `src/crosscheck.py` reports the full
per-state drift table.

**[4] Documentary and journalistic sources**, each with its own date: Oficio
SEGOB/CNBP/1349/2020 (consent accounting, universe dated 2020-08-07); ZonaDocs,
"El engaño estadístico", 2024-11-21 (active notices marked confidential; Jalisco
under-registration); El Informador, 2023-05-09 (Jalisco federal/state divergence);
Animal Político (the 2022 reporting gap); Tlachinollan, "Guerrero: territorio de
personas desaparecidas" (Iguala and Acapulco recoveries, prosecution rates); Human
Rights Watch, 2019-01-14 (Los Otros Desaparecidos de Iguala); Proceso, 2026-04-03
(Holy Week searches). Web sources consulted 2026-07-06 unless stated.

**[5] Redaction over time — vintage Apr–Dec 2025.** Ten pinned monthly snapshots of
the mirror, upstream commit SHAs in `src/version_audit.py`.

Cross-checks: category sensitivity tested (DESAPARECIDA vs +NO LOCALIZADA moves the
national count +6.1%, but Zacatecas +42%); confidential records are counted as people
but excluded from every field-level analysis; 15 headline numbers are recomputed
automatically against the freeze on each build
(`data/publication_freezes/2026-08-15/derived/automated_claim_checks.csv`). All figures
reproduce from `src/` in the project repository
(https://github.com/heliog83/desaparecidos-mx). Full methodology:
[docs/methodology.md](docs/methodology.md); refresh audit and number-by-number diff:
[docs/data-refresh-2026-08-15.md](docs/data-refresh-2026-08-15.md); source audit:
[reports/publication_data_audit_2026-08-15.md](reports/publication_data_audit_2026-08-15.md).

Ethics line (keep): behind every record is a person and a searching family. This
piece reports uncertainty as uncertainty and does not present proxies as counts.

---

## PROPOSAL — split §6 and §7 into a second article (NOT EXECUTED, needs sign-off)

Proposed, not done. Nothing below has been actioned; §6 and §7 remain in place.

**The case for splitting.** The piece currently does two jobs. §1–§5b build one
argument from national data: the confidentiality flag is an administrative artifact,
not a record of family choice. §6 and §7 then switch mode entirely — from registry
forensics to reported case studies, carrying named people, a killing, an
extermination site, and sources the national analysis never uses. They are the
longest sections (300 and 400 words after the rewrite) and the least like the rest.

Splitting would give:

- **Article 1 — "The Redacted Crisis."** §1–§5b plus §8, ~1,500 words, figs A–E and H.
  A self-contained argument about how the registry is written and rewritten. Its
  evidence is entirely quantitative and documentary, and every claim survives on
  national data alone.
- **Article 2 — "Two ways to disappear twice."** §6 and §7 expanded, figs F and G plus
  the Iguala and Teuchitlán material. This is the natural bridge to Stage 2 and the
  madres buscadoras, which is already the stated follow-up.

**The case against.** §7 carries the thesis chart (fig G) and the "two modes" idea
that §8 depends on; removing it would require §8 to be rewritten around a claim the
reader has not yet seen demonstrated. The two-modes framing is arguably the most
original thing in the whole piece, and article 1 without it is a more conventional
data story.

**If split, §8 must be rewritten**, and article 1 needs a new closing that lands on
the administrative-artifact claim rather than on the two modes.

Decision required before any restructuring.

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
  (Mar 2025) → 12,776 (our API pull, 2026-06-19, after the new federal recount)
  → 12,964 (second API pull, 2026-08-15: the count is edging back up, +188 in ~8
  weeks, while the state registry stays ~3,000 higher);
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
