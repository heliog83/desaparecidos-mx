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
missing. That live registry publishes only totals, so field-level detail comes from the
last record-level snapshot, dated 2 December 2025. In it, 63.2% of unresolved records
carried the ordinary public fields — date, age, sex, municipality, case status. The
other 36.8% revealed only the state. This is the story of how publication decisions
shape what the public can see.*

---

## 1. The crisis is real, and it is growing

**[FIG A — `figures/article/A_outcomes_by_year.png`]**
*Caption: Recorded year-of-disappearance cohorts in Mexico, 2000–2025, decomposed by
current registry outcome. Use the controls to compare all outcomes, view still-missing
counts from a zero baseline, or compare cohort shares. These are current statuses, not
dates on which anybody was found. Source: RNPDNO dashboard
API, consulted 2026-08-15 [1]; 214,643 found alive, 20,551 found dead and 117,100 still
missing across the period.*

Start with the honest version of the number. On 15 August 2026 Mexico's National
Registry of Disappeared and Missing Persons (RNPDNO) contained 407,253 records:
249,502 people recorded as found alive, 23,483 found dead and 134,268 still missing
[1]. Those are current registry statuses, not dates on which anybody was found.

Figure A looks at the subset assigned a year of disappearance between 2000 and 2025.
Across those cohorts the registry currently records roughly 214,600 found alive,
20,600 found dead and 117,100 still missing. The gap between those figures and the
headline totals consists mainly of records without a usable year and records outside
the chart's period.

Three things stand out.

- **The registry has grown more than tenfold in eighteen years.** It holds about
  3,000 records for 2007, the year the militarised drug war began, and 37,124 for
  2025 [1]. That is growth in *the registry*, which is not the same thing as growth
  in disappearances — see the next figure.
- **A third of the people in it are still missing.** 134,268 of 407,253 — and the
  still-missing share of each year's cohort has barely shifted since 2008, while the
  cohorts themselves kept growing.
- **The registry's red band never really empties.** Roughly two-thirds of every
  post-2008 cohort now sits in a "located" category — 65% of 2008, 75% of 2014, 68%
  of 2025 — and the remaining third stays where it is, year after year.

Now the limits, because they change what those numbers mean.

Each bar counts **records the state holds**, not disappearances that happened. Over
25 years, reporting rates, prosecutorial practice and registry coverage all changed
enormously, and cases still arrive late: three new 2014 records appeared inside a
single eight-week window in 2026. The cohorts have also had wildly unequal time to
resolve — 2008 has been observed for eighteen years, 2025 for months — so the
two-thirds figure describes where the register stands today, not how effectively
anyone searched.

And "located" is a **registry category, not a verified outcome**. It mixes people
found alive, people found dead, and records reclassified in administrative batches,
including the contested 2023 *censo*. The public data cannot tell you when a status
changed or why: someone recorded in the 2014 cohort may have been found that year or
a decade later. Nothing here credits any institution with finding anyone.

(The 2000–2005 bars look dramatic in percentage form but cover only a few hundred
records each, so the piece draws no trend from them.)

## 2. But is the country more violent, or better at recording?

**[FIG I — `figures/article/I_incidence_vs_homicide.png`]**
*Caption: Recorded disappearances and homicide victims, 2015–2025, both indexed to
2015. Complete years are drawn solid; 2025 is provisional in both series and drawn
detached. Sources: RNPDNO aggregate flow, publication freeze 2026-08-15 [1]; SESNSP
victim time series, which begins in January 2015 and sets the start year [2].*

A tenfold rise invites one obvious reading — that the country simply became more
violent — and for a decade the data support it. Between 2015 and 2018 recorded
disappearances and homicide victims climb together.

Then they part. From 2019 to 2024, homicide victims fall 13.4%, from 34,721 to
30,060, while recorded disappearances rise 43.4%, from 25,151 to 36,056. Across
2015–2025 the two series correlate at only r = 0.28. Whatever drove the registry's
recent growth, worsening lethal violence does not account for it.

Part of the answer is that the country built the machinery to record more. The 2017
General Law created local search commissions, and they now take nearly half of all
reports: 5.0% of records for 2017 came through a search commission, against 47.7%
for 2025, with the remainder shifting away from prosecutors and toward a public
online portal that did not meaningfully exist before 2020 [3]. A family that once
had to persuade a prosecutor now has somewhere else to go. That breakdown can only
be computed for records whose fields are public, so it describes 63.2% of the
registry and assumes the redacted remainder behaves no differently — which is
exactly the assumption the rest of this piece is about.

This does not make the rise an illusion. Two official series moving apart is a fact
about the two series; falling homicides say nothing about how honestly
disappearances are recorded, and a disappearance is not a homicide. But it does
mean the tenfold figure cannot be read as a measure of how much worse the violence
became. It measures a registry — one whose reach, rules and staffing all changed
inside the period it covers.

**[FIG J — `figures/article/J_outcome_vs_homicide.png`]**
*Caption: Each bar is one year of disappearance, split by where the case stands in
the registry now, with that year's homicide victims overlaid. Sources: RNPDNO
aggregate flow, publication freeze 2026-08-15 [1]; SESNSP [2].*

There is a darker reading of the same divergence: that deaths are being recorded as
disappearances, so the homicide statistic improves without anything improving. The
registry's own outcome split does not support it.

Of the 10,905 records the registry gained for 2019–2024, **61.7% are people it now
records as found alive.** Another 36.8% are still missing. Just 1.4% — 156 people —
are found dead. Relabelled homicide victims would have to land in the dead or
still-missing columns; instead the growth is dominated by people who turned up
alive. Homicides plus the registry's own found-dead count fell together over those
years, from 36,638 to 32,133, where a shuffle between the two categories would have
held that total roughly flat.

What this cannot rule out is quieter and more troubling, and it has two forms. A body
that is never found enters neither statistic — not the homicide count, because no
victim is ever named, and not the registry's found-dead column, because nobody is
ever found. That channel is real, and Teuchitlán is what it looks like when one
instance of it surfaces.

The second form is not unmeasured at all. Between 2006 and 2023, **72,172 bodies
entered Mexico's forensic services and were never given a name back** [6]. Two thirds
of them, 48,108, were sent to cemetery common graves. Nearly a fifth — 13,272 — have
been unidentified for more than a decade. These people were found. They are in the
state's own custody. And because nobody knows who they are, they cannot be matched to
anyone in the registry, so they sit in neither the found-dead column nor, in most
cases, anywhere a searching family can reach. The count is a floor, not a total: the
Fiscalía of Morelos declined to answer the transparency requests, and the figure
counts whole bodies, not the bone fragments that clandestine graves mostly yield.

So the gap between the two series on this chart is not simply unknown. Part of it has
already been counted, by journalists rather than by the state. The claim this section
can defend stays narrow — the registry's growth is not the homicide count in disguise
— but the reason the two counts fail to meet is partly a forensic backlog with a
number attached to it.

---

## 3. Where unresolved stock is greatest per resident

**[FIG B — `figures/article/B_rate_map.png`]**
*Caption: Unresolved disappearances per 100,000 residents by state, from the
record-level registry snapshot of 2025-12-02. Tamaulipas (359), Zacatecas (226)
and Sinaloa (211) lead by rate; Estado de México (82) and CDMX (79), the leaders
in absolute counts, fall to around 80. Note: on the live registry consulted
2026-08-15, CDMX's unresolved count has since fallen by ~1,300 (a rate of ~64) —
see §6b. Microdata vintage 2025-12-02 [3]; live comparison [1].*

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

## 4. The wall: one in three records is blank

**[FIG C — `figures/article/C_confidential_share.png`]**
*Caption: Share of each state's unresolved records marked CONFIDENCIAL in the public
registry. National: 36.8%. Jalisco: 66.9%. Nayarit: 66.2%. Guerrero 9.1%, Colima 9.0%.
A confidential record retains exactly one public fact — the state. Read the bottom of
this ranking with care: it measures redaction among records that reached the registry,
so a short bar means little was hidden, not that little was missed — see §8. Vintage
2025-12-02 [3].*

Here is what "consulting the public registry" actually gets you: for 36.8% of
unresolved records, every field is redacted — no date, no age, no sex, no
municipality, no case status. One fact survives: the state. This is why national
trend charts and state comparisons are built on different denominators, and why
every chart in this piece says so.

The top of this ranking is the easier half to read. The bottom is the trap. A state
sits low here when it redacts little of what it holds — which says nothing at all
about how much it holds. Guerrero's 9.1% is the lowest bar on the chart and the
weakest evidence of openness in this piece; §8 is about why.

The redaction is not evenly spread. Jalisco redacts two of every three records.
Guerrero, one of the most violent states in the country, redacts one in eleven.

## 5. State violence does not explain confidentiality

**[FIG D — `figures/article/D_redaction_vs_rate.png`]**
*Caption: Confidential share vs cumulative homicide-victim rate, 2015–2025, by
state. Higher state-level violence is not associated with more confidentiality; the
relationship is moderately negative (Pearson r = −0.38, all 32 states). This
ecological comparison is descriptive, not a test of risk in individual cases.
Redaction 2025-12-02 [3]; homicide victims 2015–2025 cumulative [2].*

There is an innocent explanation for all this redaction, and it deserves a fair test.

If statewide danger were the principal explanation for interstate variation in
confidentiality, states with higher homicide rates should generally redact more.

The data do not show that pattern. Across all 32 states, the correlation between the
confidential share and the cumulative homicide-victim rate for 2015–2025 is
*negative* — Pearson r = −0.38 [2]. Several of the most violent states are among
those publishing the largest share of registry detail. Colima has recorded roughly
950 homicides per 100,000 residents since 2015, the highest rate in the country; it
redacts 9% of its disappearance records. Guerrero, at 550, redacts 9%. Chihuahua, at
548, redacts 9%.

At the other end of the scale, Jalisco's homicide rate is less than half Guerrero's
and it redacts 67%. Yucatán has both the lowest homicide rate and the lowest
unresolved-record rate in Mexico — 18 and 12.5 per 100,000 respectively — yet redacts
62% of its records.

The narrow conclusion, and the only one this supports: **state-level homicide rates
do not explain state-level differences in confidentiality.** This is an ecological
comparison between states; it does not measure risk in any individual case, and it
cannot rule out case-by-case risk assessments, which no public field records. What it
does rule out is the simplest version of the official rationale — that redaction
tracks danger — as the explanation for why Jalisco sits at 67% and Guerrero at 9%.

So what does account for the difference?

## 6. Who decides a record goes dark

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
and eventually delivered 50,204 records out of 175,371, withholding 71%.

There is a simpler reason the consent paperwork is missing, and it is visible in the
registry's own fields. When Data Cívica audited the public version the CNB published
in August 2023 — 110,964 records — it found that the contact details of the person
who reported the disappearance had been left blank in **seven of every ten cases**
[7]. That is the field an authority would need in order to ask a family anything at
all. Lawyers at Centro Prodh report families who gave their details to authorities in
2017 and 2020 and were never entered into the system, and put the consequence
plainly: it ends up looking as though the families are the ones who withheld the
information. A registry that did not record how to reach seven families in ten cannot
then explain its silence by saying the families did not speak.

Journalists then closed the loop. In 2024, ZonaDocs found 4,765 cases across six
states that are marked confidential in the registry *while having active public
search notices* — posters with names and photographs, issued by the same
authorities. Officials admitted no risk assessment underlies the classification.
María de Jesús Solís, whose son disappeared in Zapopan in 2020, said she never
signed anything and wants maximum visibility. Her son's record is confidential.

**The redaction flag mixes genuine family requests, missing consent paperwork and at
least one blanket state policy — and no public field distinguishes them.**


### 6b. The totals move in batches — and once, somebody checked

**[FIG H — `figures/article/H_confidencial_batches.png`]**
*Caption: CONFIDENCIAL records per state across ten monthly snapshots of the public
registry, April–December 2025, recovered from the mirror's version history.
Nationally, confidential records grew 44,035 → 49,136 (+5,101) — 77% of the
registry's entire net growth in those eight months. Ten pinned mirror snapshots [5].*

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

For one episode, that question has been answered — and not by the registry.

In August 2023 the National Search Commission published a person-level version of
the register containing 110,964 names. In December, after the federal government's
*Estrategia Nacional de Búsqueda Generalizada* — the *censo* — the equivalent public
version held 94,283. Data Cívica compared the two and found **10,953 names present in
the first and absent from the second** [8]. The official explanation was that most had
been located. Data Cívica is careful about what its own method can establish: it can
show that a name left the register, and it cannot show whether the person was found,
is alive, or is safe, because the removals came with no case-by-case verification and
no notification to families.

Quinto Elemento Lab tested the other side of the same operation. Of the 16,681 people
the censo declared located, it reconstructed 11,026 names — the remaining 4,607 were
published redacted — and crossed them against missing-persons lists held by collectives,
the FGR's own *¿Has visto a...?* search notices, the UN Committee on Enforced
Disappearances' urgent actions, and dirty-war case files. That produced 85 candidates.
Ten journalists then contacted families and accompanying collectives one by one, and
confirmed **30 people who were listed as located and had not come home** [9]. Nine more
had recent search reports the team could not confirm directly. Two had been erased from
the register altogether.

The individual cases show how a location gets recorded. Miguel Ángel Hernández Guzmán
disappeared in Orizaba, Veracruz, in May 2019, at 27. The men who took him are serving
sentences for forced disappearance and have never said where he is; the FGR still
circulates a notice asking whether anyone has seen him; the censo lists him as located.
His mother, Lorena Guzmán, searches clandestine graves. *"It is not true that my son has
been located,"* she told the reporters. *"That is a lie."* José Marco Antonio Márquez
Sandoval was recorded as located on the strength of a DNA match to a single arm bone,
which his family disputes, and then removed from the register entirely. *"I do not accept
my son as found because of a piece of arm bone they found,"* said his mother, Leticia
Sandoval Zúñiga.

The reporters also obtained the call log behind the census visits: more than 18,000 calls
placed from a federal call centre in October 2023, of which over 86% went unanswered. In
four documented cases officials recorded either that nobody answered or that the family
said their relative had not come back — and all four folios appear on the located list.

Thirty confirmed cases out of 16,681 is not proof that the census was fabricated, and
this piece does not claim it was. What those thirty establish is narrower and harder to
argue with: **"located" is a status the register asserts, not a fact it verifies.** The
Interior Secretary, Luisa María Alcalde, said of the 16,681 that the government had
"certainty of their whereabouts", and that no record had been or would be erased. Both
statements are contradicted by documented cases. Karla Quintana, who resigned as
National Search Commissioner during the exercise, has said publicly that its purpose was
to reduce the numbers.

Step changes, flat totals during reclassification, batch deletions: these patterns are
**consistent with administrative processing** — records handled in bulk, by an office,
on an office's schedule. They are not proof that the underlying consent decisions are
fabricated. Families do decide, and some of those decisions are surely real; a backlog
of genuine consent forms entered in one batch would look much like this from the
outside. But the census shows what bulk processing can produce when nobody checks it
afterwards, and it is the only episode in this period where anyone did check. What the shape of the data does show is that the *timing* of publication is
governed by administrative operations rather than by when families decide, and that
the two cannot be separated from the public record.

That is the version-history counterpart to section 6. Together they support a claim
that is narrower than "the state is hiding people" and harder to dismiss: the
registry's most basic public property — *how much of it you can read* — is rewritten
in bulk, state by state, with no published log of who authorised a change or why, and
no field that distinguishes a redaction a family asked for from one that a missing form
produced.

## 7. Jalisco: opacity by redaction

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

Jalisco is also where the contradiction from section 6 concentrates. Of the 4,765
confidential-yet-publicly-searched-for cases ZonaDocs identified, 1,026 are Jalisco's —
second only to Estado de México's 2,691, and a ninth of everything Jalisco redacts. The same investigation found a further 2,137 disappearances
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

## 8. Guerrero: the limits of official counts

**[FIG G — `figures/article/G_two_modes.png`]**
*Caption: Guerrero's registry holds ~3,800–4,500 records. In Iguala alone, three
family collectives jointly document 623 cases. The two bars count different things
and may overlap: some of the 623 are certainly also in the state's register, and we
cannot say how many. Tlachinollan credits collective searches with 260 bodies
recovered in Iguala, of which 69 were identified and returned to families. Sources:
Tlachinollan, HRW [4]; registry figures 2025-12-02 microdata [3].*

On the redaction chart, Guerrero appears unusually open: 9% confidential, against
Jalisco's 67%. But a low confidential share describes only records that have entered
the federal stock. It cannot tell us how completely the registry covers disappearances
known to families and collectives.

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
forensic service that has effectively collapsed. In Guerrero it documents that between
2% and 6% of disappearance cases are ever prosecuted; nationally there have been 36
sentences in the entire country [4].

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

A low confidential share, then, is not a clean bill of health. Jalisco documents how
fields can disappear after a record enters the registry. Guerrero's family records
show why coverage before that point must be investigated separately. The project
cannot measure Guerrero's under-registration from these sources because the official
and collective lists have not been linked person by person.

## 9. What this means — and what we cannot claim

No chart in this piece supports the sentence "the state deliberately hides its
disappeared." I looked for it and could not find it, and the honest reason is that
the public data are not built to answer questions about intent. Every explanation
that could be tested from outside — that redaction protects families in danger, that
it tracks corruption, that it tracks state poverty — failed. What is left is not
proof of a motive. It is the absence of an account.

That absence is the finding, and it is specific. The confidentiality flag is
**unexplained, unaudited, and contradicted in thousands of documented cases by the
authorities' own search posters**. It moves in batches, on administrative schedules,
with no published log of who authorised a change or why. And no public field
distinguishes a redaction a family requested from one produced by a missing form —
which means the state cannot demonstrate that the humane version of its own rule is
what is happening, even where it is.

The practical consequence for anyone using this data: **a cross-state comparison of
the RNPDNO measures institutional publication practice at least as much as it
measures disappearance.** Jalisco redacts seven times as much of its register as
Guerrero while recording less than half Guerrero's homicide rate — the publication gap
runs opposite to the violence gap, not alongside it. Any map, ranking or model built on
those numbers without saying so is describing bureaucracies while appearing to describe
victims.

And there are two different ways to vanish from the record, which the same chart
cannot show at once: **fields redacted inside the registry, and people never entered
into it.** The first is measurable — we measured it. The second is visible only
where families have done the counting themselves, and the registry publishes no
identifiers that would let anyone reconcile the two. Guerrero's 623 documented Iguala
cases and its ~3,800 official records cannot be added, subtracted, or matched. That
is not a gap in our method. It is a gap the state maintains.

Which leaves the part no dataset in this piece can reach. Behind 134,268 records is a
number of families who learned that the search would be theirs to run — and who, in
Iguala and Teuchitlán and dozens of places with no reporters in them, went out with
rods and shovels and found what the registry does not contain. Counting what they
have found, and at what cost, is the subject of the next piece.

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

**[2] Homicide and state-capacity variables — vintage 2015–2025.**
SESNSP homicide victims: aggregated 2015–2025 per 100,000 and matched to all 32
states for the correlations in §5 and the negative controls in
`docs/methodology.md` §7; and as a national annual series for fig I, where the
file's January 2015 start sets that chart's start year and its October 2025 end
makes the final year provisional. Also INEGI ENCIG 2025 (corruption prevalence) and
PIBE 2024 (GDP per capita).

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

**[6] Unidentified bodies — vintage 2006–2023.** Efraín Tzuc and Mayela Sánchez,
"Cierra sexenio de AMLO con más de 72,100 cuerpos sin identificar", Quinto Elemento
Lab / A dónde van los desaparecidos, 2024-09-24
(`quintoelab.org/project/sexenio-amlo-72-mil-cuerpos-crisis-forense`; data and
methodology at `quintoelab.org/project/crisis-forense-2024`). Compiled from
transparency requests to all 32 state forensic services and the FGR. **A floor, not a
total:** Morelos refused to respond, and the count covers whole cadavers entering
Semefos, excluding unindividuated remains. Not derived from any dataset in this
repository and not merged with the registry figures — the overlap between the 72,172
and the 134,268 is unknown and, by construction, unknowable from public data.

**[7] Registry field completeness — vintage 2023-08-23.** Data Cívica, "Volver a
desaparecer" (`volveradesaparecer.datacivica.org`), reported by Sandra Rojas, La
Cadera de Eva, 2024-03-20. Audit of the 110,964-record public RNPDNO version of
2023-08-23: reporter contact left blank in 7 of 10 records. Centro Prodh (César
Contreras) on families whose details were given and never entered.

**[8] Erased names — comparison of two 2023 public versions.** Data Cívica, "Volver a
desaparecer" (`volveradesaparecer.datacivica.org`; open data at
`volveradesaparecer.datacivica.org/datos-abiertos`), scraped 2024-03-01; reported by
Sandra Rojas, La Cadera de Eva, 2024-03-20. 10,953 names in the 110,964-record version
of 2023-08-23 and absent from the 94,283-record post-census version. **Data Cívica's own
limit, quoted rather than softened:** the comparison establishes that a record left the
register, not that the person was found, alive or safe.

**[9] "Located" people still missing.** Efraín Tzuc, "Decenas de personas 'localizadas'
por el Gobierno siguen desaparecidas", Quinto Elemento Lab / A dónde van los
desaparecidos, 2024-03-06
(`quintoelab.org/project/decenas-personas-localizadas-censo-siguen-desaparecidas`).
16,681 declared located; 11,026 names reconstructed, 4,607 redacted; crossed against
collective lists, FGR "¿Has visto a...?" notices, UN CED urgent actions and dirty-war
files to 85 candidates; 30 confirmed still missing by ten journalists contacting
families and collectives. Also the source for the October 2023 call-centre log. Named
individuals and quotations are published in that investigation with their families'
participation.

Cross-checks: category sensitivity tested (DESAPARECIDA vs +NO LOCALIZADA moves the
national count +6.1%, but Zacatecas +42%); confidential records are counted as people
but excluded from every field-level analysis; 15 headline numbers are recomputed
automatically against the freeze on each build
(`data/publication_freezes/2026-08-15/derived/automated_claim_checks.csv`). All figures
reproduce from `src/` in the project repository
(https://github.com/heliog83/desaparecidos-mx). Full methodology:
[methodology](https://github.com/heliog83/desaparecidos-mx/blob/main/docs/methodology.md); refresh audit and number-by-number diff:
[data refresh audit](https://github.com/heliog83/desaparecidos-mx/blob/main/docs/data-refresh-2026-08-15.md); source audit:
[source audit](https://github.com/heliog83/desaparecidos-mx/blob/main/reports/publication_data_audit_2026-08-15.md).

Ethics line (keep): behind every record is a person and a searching family. This
piece reports uncertainty as uncertainty and does not present proxies as counts.

---

## DECISION — the article stays whole (settled 2026-08-16)

A split of §7 and §8 into a separate piece was proposed and **declined**. The article
ships as one piece, §1 through §9. Recorded here so it is not reopened.

The argument for splitting was that the piece does two jobs: §1–§6b are registry
forensics built on national data, while §7 and §8 switch to reported case studies with
named people and sources the quantitative sections never use. They are also the two
longest sections.

The argument that won: §8 carries fig G and the two-modes idea, and §9 resolves on it.
Splitting would leave the first article closing on a claim the reader had never been
shown, and would strip out the most original framing in the piece to leave a more
conventional data story behind. The case material is what makes the national analysis
land as something other than an audit.

Consequence for the follow-up: the madres buscadoras piece (Stage 2) is a genuine
sequel built on new data — find-events, collective attribution — not a spin-off of
material removed from this one. §9's closing line already sets that up.

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

- **fig 20 — consent accounting (for §6).** BUILT: `src/consent_accounting.py` →
  `figures/20_consent_accounting.png`. Stacked bar of the 73,388 Aug-2020 records:
  77.4% "no consent info" / family-asked split 52/47 refuse/agree. Data hardcoded
  from the oficio (pp. 5, 11) — cited, not derived. Known issue: labels cramped on
  the two narrow segments.
- **fig 21 — Jalisco divergence timeline (for §7).** BUILT: `src/jalisco_divergence.py`
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
- **fig 22 — parallel evidence systems (for §8).** BUILT:
  `src/two_modes.py` → `figures/22_two_modes_of_opacity.png`. Left: Jalisco's
  documented denominator and redaction path. Right: Guerrero's official statewide
  stock and the Iguala collective record shown as separate evidence boxes, with
  overlap explicitly unknown. They are not placed on a shared quantitative scale.

The standalone article now embeds three dependency-free responsive interactives:
Figure A switches counts/shares; Figure B ranks and inspects every state by rate,
count or confidential share; Figure H explores every stored national or state
snapshot. Static figures remain in `<noscript>` fallbacks.
