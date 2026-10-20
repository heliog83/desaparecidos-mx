# Corrections log — publication audit, 2026-10-12

Every change made to the article's claims during the audit, with the evidence that
forced it. Nothing was corrected silently: each entry names the original wording,
the replacement, the evidence and where to reproduce it. Claim ids refer to
`reports/claim_registry.csv`. The full word-level prose diff is
`reports/audit/article_draft_corrections.diff`; code changes are in
`reports/audit/code_changes.diff`.

Data were not changed. The publication freeze `2026-08-15` keeps every data hash. The
only manifest change is a recorded amendment replacing the hashes of three re-rendered
PNGs (C-03, C-04, C-12).

Severity: **B** blocker · **H** high · **M** medium · **L** low.

| id | sev | where | was | now | evidence |
|---|---|---|---|---|---|
| C-01 | H | §2 ¶ on Fig J; Fig J chart summary; Fig J PNG title | "The registry's own outcome split does not support it." / "Deaths moving into the disappeared column would have to show up in the dark bar; it barely moves." / PNG: "The extra records are not dead people" | The split "weighs against that as the whole explanation, but it cannot rule it out"; a killing recorded as a disappearance sits in **still missing**; homicides + still missing is nearly flat (42,970 → 42,326). PNG: "Most of the extra records are people found alive" | The substitution hypothesis predicts a flat *homicides + still-missing* total, not a flat *homicides + found-dead* total. The test in the draft used the wrong pair. `audit_sensitivity.py` §2. Claim SUB-01..07 |
| C-12 | H | §2 | "Homicides plus the registry's own found-dead count fell together … where a shuffle … would have held that total roughly flat." | Removed; replaced by the correct sum and a right-censoring caveat (2024 cohort has had two years to be identified, 2019 seven) | Same as C-01 |
| C-04 | H | §2, Fig J JS summary, Fig J PNG caption | "Of the 10,905 records the registry gained for 2019–2024 … 156 people … found dead" | "The 2024 cohort is 10,905 records larger than the 2019 cohort … The found-dead difference, 156" | The 10,905 is a difference between two cohort sizes, not a set of records or people. SUB-01 |
| C-03 | H | standfirst, hero record, record note, §4 text, Fig C caption, Fig C PNG, Fig G PNG | "revealed only the state" / "exactly one public fact — the state" / "One fact survives: the state" | "only the state and the authority that filed the report"; hero gains an `ORIGEN_REPORTE` row | All 49,136 confidential rows keep `ORIGEN_REPORTE` (73 distinct authorities) and an opaque `ID_VICTIMA`. `audit_sensitivity.py` §3. STAND-02 |
| C-05 | H | §9 | "Every explanation that could be tested from outside — that redaction protects families in danger … — failed." | "…tested from outside, state by state — that redaction tracks how dangerous a state is … — found no support. None of those tests can see inside an individual case." | §5 itself says an ecological test cannot rule out case-by-case risk. The conclusion overreached its own method. CONC-01 |
| C-06 | H | Methods note | "the mirror sits within 0.5% of the live registry, 0.1% across state-attributable records" | −0.5% overall (133,566 vs 134,268); −2.1% for records with a known state (130,602 vs 133,416), because the mirror files 2,964 records under an unknown state against 852 live | The 0.1% compared the mirror's *all* rows with the live *state-assigned* rows. METH-01 |
| C-07 | M | §1 bullet | "the still-missing share of each year's cohort has barely shifted since 2008" | "Since 2015 … between 29% and 38%" | 2008 35%, 2010 55%, 2013–14 25%. FLOW-09. (The audit's first rewrite said 30%; `check_claims.py` caught 2015 = 29.5%.) |
| C-08 | M | §1 bullet | "Roughly two-thirds of every post-2008 cohort now sits in a 'located' category" | "Most cohorts since 2012 … though not all: the 2010 and 2011 cohorts are only 45% and 54% located" | FLOW-LOC |
| C-09 | M | §1 | "three new 2014 records appeared inside a single eight-week window in 2026" | Data Cívica: cases up to July 2024 grew by 14,952 records between the July 2024 and July 2026 consultations [10] | The June 2026 pull is not in the freeze or in git history, so the claim can't be checked. Three records is also too few to show late registration. FLOW-LATE |
| C-10 | M | §2 | "correlate at approximately r = 0.53 … the completed-year series is the primary comparison" | The r is reported as uninformative for ten trending points; the argument rests on the post-2019 divergence; time bases are stated | r = 0.53, p = 0.12; first-difference r = −0.08. HOM-03 |
| C-11 | M | §5 text, Fig D caption, Fig D JS summary | "moderately negative" | "weakly negative … −0.28 without Colima; rank correlation −0.25"; "the robust finding is the absence of any positive relationship" | `audit_sensitivity.py` §1. CORR-01 |
| C-13 | M | §5, §6 | Article 108 "gives families the right to keep their loved one's information out of the public registry, and requires that they be told of this right" | Non-publication is a request made "for security reasons"; the duty to inform attaches to families' data rights generally | Text of Art. 108 as quoted in the CNB oficio. LAW-01 |
| C-14 | M | §6 | "largely because the records predate the law" | The CNB attributed it "probably and among other factors" to many records predating the law | Oficio, PDF p. 11. CONS-02 |
| C-15 | M | §6 | "In the proceeding, the CNB described a withholding practice under which records without affirmative consent paperwork were kept out of public versions" | The CNB argued it could not release data without express consent, and said the consent declarations it relied on did not exist | A dónde van, 2021-04-08. CONS-04 |
| C-16 | M | §6 | "withholding 71%" | "about 29%" delivered; methods note gives the composition of the 50,204 | CONS-05 |
| C-17 | M | §6 | "Officials admitted no risk assessment underlies the classification." | Authorities said they produce no context or risk analysis for these publication decisions, arguing the law does not require one | ZonaDocs 2024-11-21. ZD-02 |
| C-18 | M | §6 | Solís "said she never signed anything" | "said she never signed for his record to be confidential" | ZonaDocs quote "Nunca firmé para que fuera confidencial". ZD-03 |
| C-19 | M | §6b | "the remaining 4,607 were published redacted" | "at least 4,607 more were published redacted" | 11,026 + 4,607 = 15,633 ≠ 16,681; the source does not explain the 1,048 gap. QE-01 |
| C-20 | M | §6b | Alcalde said "no record had been or would be erased. Both statements are contradicted" | Clause removed; the "certainty of their whereabouts" quote is kept | Absent from the cited investigation [9]. Restore only with a source. QE-03 |
| C-21 | L | §6b | Quintana "resigned … during the exercise" | "left the National Search Commission months after the census was announced" | QE-04 |
| C-22 | M | §6b | "Jalisco's confidential count was flat all year, then fell by ~1,400 in the last quarter" | "drifted down for most of the year, then fell by about 1,200 in the last quarter" | Sep→Dec −1,224; Apr→Dec −1,367. PANEL-JAL |
| C-23 | M | §6b | "batch deletions" | "batch removals" | The mechanism isn't known. Data Cívica finds that comparable falls in Jalisco and Tabasco were matched by rises in "located". PANEL-TAB |
| C-24 | M | §7 | "Searching in Jalisco is lethal work. … murdered alongside one son while searching for another." (uncited) | Dated account with citation [12]: shot in Tlajomulco with one son, had been searching for another; prosecutors list search work among lines of investigation; no motive established in court | ADN40, El Financiero, 2025. JAL-02 |
| C-25 | L | §7 | "a ninth of everything Jalisco redacts" | The ratio is kept, with both vintages named (ZonaDocs 2024 vs 9,216 in Dec 2025) | ZD-04 |
| C-26 | M | §8 | "nationally there have been 36 sentences in the entire country" | "the CNB counted 36 sentences for forced disappearance by the end of 2021", sourced in the methods note | GRO-02 |
| C-27 | M | standfirst | "63.2% … carried the ordinary public fields — date, age, sex, municipality, case status" | "were open to inspection, with fields such as … — not always complete" | Among non-confidential rows, birth date is present in 67.3% and disappearance date in 90.4%. STAND-01 |
| C-28 | L | §1 | "The registry has grown more than tenfold" | "The yearly cohorts have grown more than tenfold" | Cohort size, not registry size |
| C-29 | L | §2 | portal "did not meaningfully exist before 2020"; remainder shifting "toward" it | Prosecutors' share fell from 94% to 45%; the portal (launched late 2019) accounts for 8–21% of cohorts since 2020 | INTAKE-02 |
| C-30 | L | §3 | "The national rate is 98" | Denominator stated: 130,602 state-assigned records; 2,964 name no state | RATE-01 |
| C-31 | L | Fig E caption | "family reporters actually asked" | "family reporters with a recorded preference" | CONS-01 |
| C-32 | H | Fig C interactive | Summary "National average" = unweighted mean of 32 state shares; dashed line labelled as a national median | Summary uses the national share (36.8%, all records incl. unknown state); line labelled "Median state"; heading no longer claims "violence does not explain it" | The JS averaged state shares |
| C-33 | M | Fig C & D interactive | Yucatán never highlighted (`"YUCATAN"` key vs data `"YUCATÁN"`) | Accent-insensitive key comparison | JS bug |

## Additions (new, dated evidence; not corrections)

| id | where | what | source |
|---|---|---|---|
| A-01 | §2 caveat | Data Cívica: more confidential than public records in the 2021–2023 cohorts | [10] |
| A-02 | Fig C caption | Data Cívica's 38.5% (Feb-2026 extract) and similar ranking, as corroboration, not blended | [10] |
| A-03 | §6b | Data Cívica: falls in Jalisco and Tabasco roughly matched by rises in "located" | [10] |
| A-04 | §6b | 27 March 2026 federal reclassification (132,534; 46,742; 40,308; 43,128) and Data Cívica's < 2% unidentifiable finding. This event predates the freeze and was missing | [11], [10] |
| A-05 | Methods | Sources [10], [11], [12] | — |
| A-06 | §6 + Fig K | **E-3 adopted (author request, 2026-10-12):** confidentiality by filing authority. Estado de México 3% vs 36%, Nuevo León 32% vs 93%, Jalisco 64% vs 90% (state prosecutor vs state search commission); 6 of 17 states differ by ≥30 points, 8 by <10; Puebla and Baja California Sur run the other way; portal reports 35–41% in the middle half of states. New derived table pinned in the freeze; Fig K drawn as an HTML/CSS dot plot (readable at 320 px, no JS needed) with the PNG as static version | [3]; `src/filing_authority.py` |

| A-07 | Standfirst | **E-1 adopted (author request, 2026-10-12):** the standfirst now leads with the record-level blackout, the batch movement (≈2,500 records in one state in two months) and the filing-office gap (30–60 points in six states). Two phrases from the proposal were dropped as unsupported: "for more than a third of the unresolved records it publishes" (blended the Aug-2026 and Dec-2025 vintages) and "which office files a case matters more than where the family lives" (never tested). `build_page.py` now reads the standfirst from the draft instead of a second hard-coded copy | `check_claims.py` STAND-* |

| A-08 | §6b, Fig F caption and PNG | **Unverifiable June-2026 values dropped (author decision, 2026-10-12).** CDMX 6,086 and Jalisco 12,776 came from a 2026-06-19 pull that was overwritten and never archived (searched: main checkout, all worktrees, git history). §6b now goes straight from December 2025 to August 2026 (5,915), and Fig F from March 2025 (15,015) to August 2026 (12,964). Neither the reversal claim nor the ~3,000 gap depended on the June point | freeze `flow_by_state.csv` |

### Changes to E-3 while applying it (the proposal was wrong in three places)

- The proposal's grouping put the **national** search commission (CNB, 4,950 records) in with the state commissions, and **federal** prosecutors (FGR and legacy PGR offices, 2,384 records) in with the state prosecutors. The article's wording ("state prosecutors", "the state's search commission") needed state offices only. With them separated, Nuevo León is 32% vs **93%** (was 91%) and Jalisco 64% vs **90%** (was 84%). Estado de México is unchanged.
- "Within the same state, it depends on it enormously" overgeneralised. The gap is 30+ points in 6 of the 17 comparable states and under 10 in 8. The prose now says "in several states" and gives the distribution.
- Counting by eye, I wrote "nine" states under 10 points; `check_claims.py` failed the build and the correct count is eight.

## Left as is, and why

- **June-2026 values:** resolved by A-08 (dropped).
- **72,172 unidentified bodies; Tlachinollan, HRW and Proceso figures; Data Cívica 2023
  erased names:** all five external sources were re-fetched and verified verbatim on
  2026-10-14 (R-3 cleared; see `claim_registry.csv` rows `FOR-01`, `CENSO-01`, `GRO-01`,
  `GRO-03`).

## Post-publication corrections — 2026-10-19

Published 2026-10-12. These were found by a readiness re-audit on 2026-10-19
(`reports/publication_readiness_2026-10-19.md` in the main checkout, findings 1–5) and
re-checked against the 2026-08-15 freeze. A dated note in the Methods box lists them for
readers. No data changed.

| id | sev | where | was | now | evidence |
|---|---|---|---|---|---|
| C-25 | H | §3 Fig B caption and body | Estado de México and CDMX "the leaders in absolute counts" / "register the most cases" | Estado de México first, CDMX fourth | Freeze `derived/state_rates.csv`: Edomex 14,579; Jalisco 13,766; Tamaulipas 13,460; CDMX 7,242 |
| C-26 | H | §4 | Guerrero's 9.1% "is the lowest bar on the chart" | "among the lowest bars … only Chihuahua and Colima sit below it" | Freeze `derived/state_opacity_enriched.csv`: Chihuahua 8.78%, Colima 8.96%, Guerrero 9.05% |
| C-27 | H | §6c | 132,534 presented "in three operational groups" | The three groups add up to 130,178, 2,356 short; the presentation separately counted 2,356 pre-2006 records but does not say whether they are the difference | 46,742 + 40,308 + 43,128 = 130,178. ZonaDocs [11] Nota 4 lists the pre-2006 cases separately and does not reconcile them (consulted 2026-10-19) |
| C-28 | H | §9; methodology §4 | Cross-state comparison "measures institutional publication practice at least as much as it measures disappearance"; methodology: a state "can rank high partly because its prosecutor redacts more" | Cross-state comparison is also a comparison of registration and publication practice, which the public data cannot separate; redaction removes fields, not people, from a state's count | Confidential records keep `ENTIDAD` and are included in Fig B counts. "At least as much" was never measured |
| C-29 | M | §5, §6, §9; methodology §7 | "rules out the simplest version"; "no single rule is being applied"; three explanations "found no support"; methodology "rules out the three most obvious structural explanations" | "counts against"; "the same rule does not produce the same result from one office to the next"; homicide: redaction does not rise with violence; corruption and GDP: nulls of limited power at n = 32, GDP a rough proxy | Homicide vs confidential share: r = −0.38, n = 32. Corruption and GDP: p > 0.18. A null at n = 32 cannot exclude moderate associations |
| C-30 | M | §2 | A body never found misses the homicide count "because no victim is ever named"; the gap between the series "is partly a forensic backlog with a number attached" | Probably misses the homicide count because no death is established; the 72,172 unidentified bodies are not linked to either series, so their share of the gap cannot be stated | No person-level link between the forensic count [6] and either series |
| C-31 | M | Fig J chart note (`src/build_page.py`) | Overlap of homicides and disappearances is "at most the dark band" | "which should place them in the dark band, though registry statuses are not always updated" | The article itself documents status lag (§6c); a hard upper bound does not hold under lag |
| C-32 | M | §6 | "There is a simpler reason the consent paperwork is missing"; "A registry that did not record how to reach seven families in ten cannot then explain its silence" | "There may be a simpler reason some of the consent paperwork is missing"; a blank in a published version does not show what is held internally, and it postdates the 2020 accounting; the conclusion is limited to cases like those Centro Prodh documents | Data Cívica's 70% figure is for the Aug-2023 published version [7]; the consent accounting is Aug 2020 [4] |
