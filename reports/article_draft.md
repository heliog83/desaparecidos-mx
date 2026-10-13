# DRAFT — The Redacted Crisis: How Mexico's Registry of the Disappeared Hides What It Counts

Draft v1.1, 2026-08-15 (data refreshed; see `docs/data-refresh-2026-08-15.md`).
Visual-led web article. ~2,900 words + 8 figures.
Language: English (author decision, 2026-10-12). A Spanish edition remains a possible
follow-up.
Every figure is reproducible from `src/`; every number carries a consultation date in
`docs/`. Figure production notes at the end.

Delivery note: this markdown is the narrative source and `reports/article.html` is its
generated local output. Do not publish or update this article through Claude Artifacts.
Build with `python3 src/build_page.py`, validate with `python3 src/check_article.py`, and
preview at `http://127.0.0.1:8794/article.html` using the repository's local server.

Working titles (pick one):
1. *The Redacted Crisis: what Mexico's registry of the disappeared won't let you see*
2. *134,000 people, one third behind a wall*
3. *Two ways to disappear twice: redacted in Jalisco, uncounted in Guerrero*

Standfirst: *On 15 August 2026 Mexico's official registry counted **134,268 people still
missing**. Its live dashboard publishes only totals. In the last record-level snapshot,
dated 2 December 2025, **36.8% of unresolved records revealed only two things: the
state, and which office filed the report.** Ten snapshots taken between April and
December 2025 show that this blackout does not move one family at a time. It moves in
batches — about 2,500 records in one state in two months — and in several states the
share hidden differs by 30 to 60 points depending on which office filed the case.*

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

- **The yearly cohorts have grown more than tenfold in eighteen years.** The
  registry holds about 3,000 records for 2007, the year the militarised drug war
  began, and 37,124 for 2025 [1]. That is growth in *the registry*, which is not the
  same thing as growth in disappearances — see the next figure.
- **A third of the people in it are still missing.** 134,268 of 407,253. Since
  2015 the still-missing share of each year's cohort has stayed between 29% and 38%,
  while the cohorts themselves kept growing.
- **The registry's red band never really empties.** Most cohorts since 2012 now sit
  roughly two-thirds in a "located" category — 75% of 2014, 68% of 2025 — though not
  all: the 2010 and 2011 cohorts are only 45% and 54% located. In every cohort a
  large unresolved remainder stays where it is.

Now the limits, because they change what those numbers mean.

Each bar counts **records the state holds**, not disappearances that happened. Over
25 years, reporting rates, prosecutorial practice and registry coverage all changed
enormously, and cases still arrive late: Data Cívica found that the registry's count
of disappearances up to July 2024 grew by 14,952 records between its July 2024
consultation and a July 2026 re-extraction [10]. The cohorts have also had wildly unequal time to
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
30,060, while recorded disappearances rise 43.4%, from 25,151 to 36,056. With only
ten complete years, a correlation coefficient adds little here: the two series
correlate at about r = 0.53 over 2015–2024, a value that ten trending points cannot
distinguish from no relationship, and their year-to-year changes are essentially
uncorrelated. The plain comparison is the evidence: after 2019 the lines move in
opposite directions. Two further cautions apply. The disappearance series counts
people by the year they went missing, as registered by August 2026, while homicide
victims are counted when an investigation is opened; and 2025 is provisional in both.
On national totals, worsening lethal violence does not account for the registry's
recent growth.

Part of the answer is that the country built the machinery to record more. The 2017
General Law created local search commissions. Among unresolved records with public
fields in the 2025-12-02 mirror, 5.0% of cases for 2017 came through a search
commission, against 47.7% for 2025, while the prosecutors' share fell from 94% to
45%; the CNB's online reporting portal, launched in late 2019, accounts for 8% to
21% of each cohort since 2020 [3].
A family that once had to persuade a prosecutor now has somewhere else to go.
Crucially, this breakdown applies only to unresolved records whose fields are public
(63.2% of the mirror snapshot); neither the confidential records nor resolved cases
can be assumed to follow the same intake pattern. That exclusion bites hardest
exactly where the shift happens: Data Cívica's analysis of a February 2026 extract
found more confidential than public records for the 2021–2023 cohorts [10].

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
registry's outcome split weighs against that as the whole explanation, but it cannot
rule it out.

The 2024 cohort is 10,905 records larger than the 2019 cohort. **61.7% of that
difference is people the registry now records as found alive** — 6,732 more than in
2019 — which a relabelling of homicides could not produce. But 36.8% of the
difference, 4,017 records, is people still missing, and that is exactly where an
uncounted killing would sit. Over the same years homicide victims fell by 4,661. Add
homicide victims to the registry's still-missing count and the total barely moves —
42,970 in 2019, 42,326 in 2024. That proves no substitution, but it leaves room for
some. The found-dead difference, 156, cannot settle it either way: the 2024 cohort has
had two years to be identified, the 2019 cohort seven.

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
can defend stays narrow — most of the registry's recent growth is not the homicide
count in disguise, though a partial shift cannot be excluded — and the reason the two
counts fail to meet is partly a forensic backlog with a number attached to it.

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

The national rate is 98 unresolved records per 100,000 residents, counting the
130,602 records assigned to a state; another 2,964 name no state. Tamaulipas, on the
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
A confidential record retains only the state and the authority that filed it. Read the bottom of
this ranking with care: it measures redaction among records that reached the registry,
so a short bar means little was hidden, not that little was missed — see §8. Vintage
2025-12-02 [3]. A February 2026 extract analysed by Data Cívica gives 38.5% nationally
and a near-identical ranking [10].*

Here is what "consulting the public registry" actually gets you: for 36.8% of
unresolved records, every descriptive field is redacted — no date, no age, no sex, no
municipality, no case status. Two facts survive: the state, and the name of the
authority that filed the report. This is why national
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
relationship is weakly negative (Pearson r = −0.38, all 32 states; −0.28 without
Colima; rank correlation −0.25). This ecological comparison is descriptive, not a
test of risk in individual cases.
Redaction 2025-12-02 [3]; homicide victims 2015–2025 cumulative [2].*

There is an innocent explanation for all this redaction, and it deserves a fair test.
The law itself supplies it: Article 108 lets families ask that a record not be made
public "for reasons of security" [4].

If statewide danger were the principal explanation for interstate variation in
confidentiality, states with higher homicide rates should generally redact more.

The data do not show that pattern. Across all 32 states, the correlation between the
confidential share and the cumulative homicide-victim rate for 2015–2025 is
*negative* — Pearson r = −0.38 [2]. That value leans on Colima and weakens to −0.28
without it, so the robust finding is the absence of any positive relationship, not
the negative one. Several of the most violent states are among
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
records): for 77.4%, no consent information exists at all. Among the 14,295 family
reporters with a recorded preference, 52% declined publication, 47% agreed. Source:
Oficio SEGOB/CNBP/1349/2020, pp. 5, 11 [4]; universe dated 2020-08-07.*

On paper, the rule is humane and simple. Article 108 of the General Law on
Disappearances lets families ask, for security reasons, that their loved one's
information be kept out of the public registry, and requires that families be told
of their data rights before giving information. Redaction, officially, means "the
family asked."

The government's own paperwork says otherwise. In August 2020 the National Search
Commission (CNB) wrote to the transparency institute (INAI) asking how to build the
public registry — and admitted, in its own tables, that **for 77.4% of records
nobody knew whether the family had consented or not** — which the CNB attributed,
"probably and among other factors," to many records predating the law. In the
proceedings that followed, the CNB argued that without families' express consent it
could not release the data — and when a journalist asked for the consent declarations
it was relying on, it answered that they did not exist [4]. And in a footnote, the CNB recorded that the Fiscalía of Jalisco had
declared that *everything* it sends to the national registry is non-publishable,
invoking family refusals without producing any supporting documentation in the
public proceeding.

When INAI ordered the CNB to release a public database (resolution RRA 09082/20, and
at least two later resolutions), the commission resisted on those grounds and
eventually delivered 50,204 records against the 175,371 then registered — about 29%
[4].

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

The one field the registry leaves on a confidential record makes a test possible: it
names the office that filed the report. If redaction reflected what families chose, it
should not depend much on which office happened to take the case. In several states it
depends on it enormously. In Estado de México, 3% of the unresolved records
filed by state prosecutors are confidential, against 36% of those filed by the state's
search commission. In Nuevo León the figures are 32% and 93%; in Jalisco, 64% and 90%.
The gap does not even run the same way everywhere — in Puebla and Baja California Sur
it is the prosecutors who redact more — which is itself the finding: no single rule is
being applied. In six of the 17 states where both offices filed enough cases to compare,
the two differ by 30 points or more; in eight, by fewer than 10. Families who report directly through the national commission's online
portal, meanwhile, end up confidential at a similar rate almost everywhere, between
about 35% and 41% across the middle half of the states with enough cases to measure
[3]. This is a description, not a proof: the channels do not receive identical cases,
and the portal leans toward family self-reports and recent years. But family
preferences do not obviously change at an office door. Office practice plainly does.

**[FIG K — `figures/article/K_filing_authority.png`]**
*Caption: Share of each office's unresolved records marked CONFIDENCIAL, in the 17
states where both the state prosecutor and the state search commission filed at least
300 records. Grey tick: reports filed by families through the national commission's
portal. Records filed by the national commission itself or by federal prosecutors are
excluded. Descriptive, not causal: case mix differs by channel. Vintage 2025-12-02 [3].*

Journalists then closed the loop. In 2024, ZonaDocs found 4,765 cases across six
states that are marked confidential in the registry *while having active public
search notices* — posters with names and photographs, issued by the same
authorities. In transparency responses, authorities said they produce no context or
risk analysis for these publication decisions, arguing the law does not require one.
María de Jesús Solís, whose son disappeared in Zapopan in 2020, said she never
signed for his record to be confidential and wants maximum visibility. Her son's
record is confidential [4].

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
looked different had we pulled the data in April. Jalisco's confidential count
drifted down for most of the year, then fell by about 1,200 in the last quarter as the
state's overall federal count also fell — before the new recount was announced in
January 2026. Tabasco's published total fell by a third in a single month. Data
Cívica, comparing re-extractions a year apart, found that falls of this kind in
Jalisco and Tabasco were roughly matched by rises in records marked located — while
noting it cannot confirm they are the same records [10].

The reversals do not stop at the edge of the panel. Mexico City's unresolved count
climbed steadily all through 2025, from 6,025 in April to 7,242 in December — and
then gave the entire increase back. By August 2026 the live registry showed 5,915:
a capital that had been adding cases for a year shed 1,327 of them in eight months,
roughly one in five. We can see the direction and the size of
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
the censo declared located, it reconstructed 11,026 names — at least 4,607 more were
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
"certainty of their whereabouts". The documented cases contradict that. Karla Quintana,
who left the National Search Commission months after the census was announced, has
said publicly that its purpose was to reduce the numbers [9].

The exercise has a successor. On 27 March 2026 the federal government presented the
132,534 people then recorded as missing in three operational groups: 46,742 records it
said lacked the data needed to search, 40,308 showing administrative activity after
the disappearance — among which it said it had confirmed 5,338 locations — and 43,128
with no activity at all [11]. Data Cívica, working from a February 2026 extract, found
that fewer than 2% of records lack the combination of name, dates and other fields
needed to identify a person [10]. The same pattern holds: a status is asserted for
tens of thousands of records at once, and the public cannot check it record by record.

Step changes, flat totals during reclassification, batch removals: these patterns are
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
roughly 3,000 people — the federal count stood at 12,964 in August 2026, down from
15,015 in March 2025, while the state's stood near 16,000 at the end of 2025. Markers are documented
snapshots, not a continuous series, and the two registries define their counts
differently.*

Jalisco redacts more of its registry than any other state in Mexico: 9,216 of its
13,766 unresolved records, two out of every three. It is also the state that stopped
fully participating in the national count.

From 2022, under then-governor Enrique Alfaro, Jalisco largely stopped reporting
disappearances to the RNPDNO and logged them in its own state registry instead. The
country now has two official counts of Jalisco's disappeared, kept by two governments,
and they do not agree with each other. By the article's own comparison of public
snapshots, the resulting gap now reaches roughly 3,000 people — following earlier
divergence documented by El Informador [4]. The state government's answer, in January
2024, was a communiqué titled "Jalisco does not manipulate its registry, nor erase
figures."

Jalisco is also where the contradiction from section 6 concentrates. Of the 4,765
confidential-yet-publicly-searched-for cases ZonaDocs identified, 1,026 are Jalisco's —
second only to Estado de México's 2,691 — equal to about a ninth of the 9,216 Jalisco
records marked confidential in December 2025, though ZonaDocs counted at an earlier
date. The
same investigation found a further 2,137 disappearances between 2019 and mid-2024 that
state authorities registered locally with official search notices but omitted from the
federal registry: not redacted inside the national count, but withheld from it entirely.

What the registry would not record, families recorded themselves. On 5 March 2025 the
collective Guerreros Buscadores de Jalisco entered Rancho Izaguirre, a property outside
Teuchitlán, and found a cartel recruitment and extermination site: clothing, shoes,
backpacks, notebooks, bone fragments. It became a national scandal — not only for what
was on the ranch, but because a group of searching families, rather than the state, was
what finally established it.

Searching in Jalisco carries mortal risk. In March 2025 Teresa González Murillo, who
was searching for her brother, was shot at her home in Guadalajara; she died days
later. In April 2025 María del Carmen Morales, of Guerreros Buscadores, was shot dead
in Tlajomulco with one of her sons; she had been searching for another. In both cases
prosecutors listed the victims' search work among their lines of investigation; no
motive has been established in court [12].

The state with the most redacted registry in Mexico is also the state where civil
society keeps producing the evidence its registry lacks. Those are not two facts about
Jalisco. They are one fact, seen from two sides.

## 8. Guerrero: the limits of official counts

**[FIG G — `figures/article/G_two_modes.png`]**
*Caption: Guerrero's state register held roughly 3,800 records per Tlachinollan's
2022 report ("Guerrero: territorio de personas desaparecidas"), while the
federal RNPDNO mirror snapshot (2025-12-02) documents 4,453 unresolved records.
In Iguala alone, three family collectives jointly document 623 cases. The two
bars count different things and may overlap: some of the 623 are certainly also
in the state or federal register, and we cannot say how many. Tlachinollan
credits collective searches with 260 bodies recovered in Iguala, of which 69
were identified and returned to families. Sources: Tlachinollan, HRW [4];
registry figures 2025-12-02 microdata [3].*

On the redaction chart, Guerrero appears unusually open: 9% confidential, against
Jalisco's 67%. But a low confidential share describes only records that have entered
the federal stock. It cannot tell us how completely the registry covers disappearances
known to families and collectives.

In 2022 reporting, the human-rights centre Tlachinollan documented roughly 3,800
records in Guerrero's state registry; in the federal 2025-12-02 mirror snapshot,
unresolved records for the state reached 4,453. In Iguala alone — one city — three
family collectives jointly document 623 cases.

Those numbers are not a subtraction, and it matters that we say so. **They may
overlap, and we cannot measure by how much.** Some of the 623 Iguala cases are
certainly also registered with the state; others, by the collectives' account, are
not. Without case-level identifiers on both sides — which no public source provides —
there is no way to net one against the other. The comparison is worth making because
of the ratio it implies: three collectives in one city hold a caseload equal to a
seventh of the federal register (and a sixth of the 2022 state count). It is not
worth making as an estimate of how many people are missing from that register.

The human-rights centre Tlachinollan, which has tracked the state for decades,
describes prosecutors who stall investigations unless families force them open, and a
forensic service that has effectively collapsed. In Guerrero it documents that between
2% and 6% of disappearance cases are ever prosecuted. Nationally, the CNB counted 36
sentences for forced disappearance by the end of 2021 [4].

The modern searching-mothers movement was, in an important sense, born here. When the
43 students from Ayotzinapa disappeared in September 2014, families searching the hills
around Iguala for them began instead to find other people: graves of the dead nobody
was officially looking for. The collective that formed out of that search, Los Otros
Desaparecidos de Iguala, has since exhumed more than 160 bodies. Tlachinollan credits
women-led collectives — not state institutions — with the recovery of 260 bodies in
Iguala, of which 69 were identified and returned to their families. In Acapulco it
records a different outcome: 70 people found alive, and 55 identified bodies returned
[4].

The under-registration is not history. During Holy Week searches in 2026, in Buenavista
de Cuéllar and Iguala, eight families approached searching mothers from the collective
Familiares en Búsqueda María Herrera — five in Buenavista and three in Iguala — to report
disappearances after official channels had stalled. One woman in Iguala whose father had
been missing six months recounted that authorities had made no progress and told her to
stop inquiring. That is the gap happening in real time: families turning to search
collectives because the state has ceased to look.

A low confidential share, then, is not a clean bill of health. Jalisco documents how
fields can disappear after a record enters the registry. Guerrero's family records
show why coverage before that point must be investigated separately. The project
cannot measure Guerrero's under-registration from these sources because the official
and collective lists have not been linked person by person.

## 9. What this means — and what we cannot claim

No chart in this piece supports the sentence "the state deliberately hides its
disappeared." I looked for it and could not find it, and the honest reason is that
the public data are not built to answer questions about intent. Every explanation
that could be tested from outside, state by state — that redaction tracks how
dangerous a state is, that it tracks corruption, that it tracks state poverty — found
no support. None of those tests can see inside an individual case. What is left is
not proof of a motive. It is the absence of an account.

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
by-year outcome breakdown in fig A. Source: [RNPDNO public dashboard](https://versionpublicarnpdno.segob.gob.mx/), captured
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

Drift between [1] and [3] is small nationally — the mirror's 133,566 records sit 0.5%
below the live 134,268 — but larger once records with no state are set aside: 130,602
state-assigned records in the mirror against 133,416 live (−2.1%), because the mirror
files 2,964 records under an unknown state against 852 live. **It is not uniform by
state.**
Ciudad de México has since fallen 18% and Jalisco 6% against the frozen microdata;
both carry their live figures in the caption. `src/crosscheck.py` reports the full
per-state drift table.

**[4] Documentary and journalistic sources**, each with its own date: Oficio
SEGOB/CNBP/1349/2020 (consent accounting, universe dated 2020-08-07); A dónde van
los desaparecidos, 2021-04-08, on INAI resolution RRA 09082/20 (December 2020) and the
two that followed it — the order to publish a public-version database, the CNB's
answer that the consent declarations it cited did not exist, and the eventual delivery
of 50,204 records (older RNPED files plus 11,197 newer records) against 175,371
registered; ZonaDocs,
"El engaño estadístico", 2024-11-21 (active notices marked confidential; Jalisco
under-registration); El Informador, 2023-05-09 (Jalisco federal/state divergence);
Animal Político, 2026-02-09 (Jalisco's halt in federal reporting since 2022 and state registry divergence); Tlachinollan, "Guerrero: territorio de
personas desaparecidas" (Iguala and Acapulco recoveries, prosecution rates); Human
Rights Watch, 2019-01-14 (Los Otros Desaparecidos de Iguala); Proceso, 2026-04-03
(Holy Week searches); the figure of 36 sentences for forced disappearance is the CNB's
count to the end of 2021, as reported in the UN Committee on Enforced Disappearances'
2022 report on Mexico. Web sources consulted 2026-07-06 unless stated.

**[5] Redaction over time — vintage Apr–Dec 2025.** Ten pinned monthly snapshots of
the mirror, upstream commit SHAs in `src/version_audit.py`.

**[6] Unidentified bodies — vintage 2006–2023.** Efraín Tzuc and Mayela Sánchez,
"Cierra sexenio de AMLO con más de 72,100 cuerpos sin identificar", Quinto Elemento
Lab / A dónde van los desaparecidos, 2024-09-24
([investigation](https://quintoelab.org/project/sexenio-amlo-72-mil-cuerpos-crisis-forense); data and
[methodology](https://quintoelab.org/project/crisis-forense-2024)). Compiled from
transparency requests to all 32 state forensic services and the FGR. **A floor, not a
total:** Morelos refused to respond, and the count covers whole cadavers entering
Semefos, excluding unindividuated remains. Not derived from any dataset in this
repository and not merged with the registry figures — the overlap between the 72,172
and the 134,268 is unknown and, by construction, unknowable from public data.

**[7] Registry field completeness — vintage 2023-08-23.** Data Cívica, "Volver a
desaparecer" ([project](https://volveradesaparecer.datacivica.org/)), reported by Sandra Rojas, La
Cadera de Eva, 2024-03-20. Audit of the 110,964-record public RNPDNO version of
2023-08-23: reporter contact left blank in 7 of 10 records. Centro Prodh (César
Contreras) on families whose details were given and never entered.

**[8] Erased names — comparison of two 2023 public versions.** Data Cívica, "Volver a
desaparecer" ([project](https://volveradesaparecer.datacivica.org/); [open data](https://volveradesaparecer.datacivica.org/datos-abiertos)), scraped 2024-03-01; reported by
Sandra Rojas, La Cadera de Eva, 2024-03-20. 10,953 names in the 110,964-record version
of 2023-08-23 and absent from the 94,283-record post-census version. **Data Cívica's own
limit, quoted rather than softened:** the comparison establishes that a record left the
register, not that the person was found, alive or safe.

**[9] "Located" people still missing.** Efraín Tzuc, "Decenas de personas 'localizadas'
por el Gobierno siguen desaparecidas", Quinto Elemento Lab / A dónde van los
desaparecidos, 2024-03-06
([investigation](https://quintoelab.org/project/decenas-personas-localizadas-censo-siguen-desaparecidas)).
16,681 declared located; 11,026 names reconstructed, 4,607 redacted; crossed against
collective lists, FGR "¿Has visto a...?" notices, UN CED urgent actions and dirty-war
files to 85 candidates; 30 confirmed still missing by ten journalists contacting
families and collectives. Also the source for the October 2023 call-centre log. Named
individuals and quotations are published in that investigation with their families'
participation.

**[10] Data Cívica, "A quienes nos faltan: sin datos para encontrarles"** (fifth
edition, published September 2026, after this piece's data freeze;
[compendium](https://datacivica.org/a-quienes-nos-faltan-2026/)). Analyses an RNPDNO
record-level extract taken in February 2026 and received in April 2026, plus
statistical-version consultations of July 2024, July 2025 and July 2026. Its 38.5%
confidential share is a different vintage, and possibly a different denominator, from
this piece's 36.8% (133,566 unresolved records, 2 December 2025); the two are not
combined. Consulted 2026-10-12.

**[11] Federal registry report, 27 March 2026.** Presented by the SESNSP and the
Interior Ministry (SEGOB) at the presidential press conference; categories and counts
as reported by Fabrizio Lorusso, ZonaDocs, 2026-04-13
([analysis](https://www.zonadocs.mx/2026/04/13/registro-de-personas-desaparecidas-2026-notas-criticas-y-contextos/)).
Consulted 2026-10-12.

**[12] Killings of searchers, 2025.** Teresa González Murillo: attacked 2025-03-27,
died 2025-04-02 (ADN40, 2025-04-02). María del Carmen Morales and her son Jaime Daniel
Ramírez Morales: killed 2025-04-24 in Tlajomulco (El Financiero, 2025-04-24). Consulted
2026-10-12.

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

Behind every record is a person and a searching family. This piece reports
uncertainty as uncertainty and does not present proxies as counts.

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
  (Mar 2025) → [2026-06-19 point, 12,776, dropped 2026-10-12: pull not archived]
  → 12,964 (API pull, 2026-08-15, publication freeze; the state registry stays
  ~3,000 higher);
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
