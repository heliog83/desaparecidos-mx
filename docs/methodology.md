# What Are We Counting? — Methodology & Data Caveats

This file is the project's conscience. Every chart and claim inherits these caveats. Read it
before interpreting any number.

**Two vintages, and they do not merge.** Record-level findings (redaction shares, field
completeness, per-state rates) come from the pinned RNPDNO mirror snapshot of
**2025-12-02**, 133,566 records, interrogated 2026-06-19 — re-run `src/interrogate.py`
to refresh. Aggregate outcome totals come from the live dashboard API captured for the
**2026-08-15** publication freeze. Every figure in the article is labelled with the one
it uses. Reading a number from one against a number from the other gives a wrong
answer.

## TL;DR — the one thing to never forget
**This dataset is the *stock of people still missing*, not the *flow of all disappearances*.**
People who were located (alive or dead) are removed from it. So counts measure *unresolved
cases as of the snapshot*, not how many disappeared.

---

## 1. Unit of analysis — solid
`ID_VICTIMA` is 100% unique: **one row = one person**, no duplicates. Counts are people.

## 2. Stock, not flow — the defining caveat (now RESOLVED with flow data)
The record-level mirror has only `DESAPARECIDA` (79,612), `NO LOCALIZADA` (4,818), and
`CONFIDENCIAL` (49,136). **There is no "located" status** — the located people are absent, so the
mirror is a *still-missing stock*, not a flow. We feared this made time trends survivorship-biased.

**`src/fetch_flow.py` pulled the aggregate flow (incl. located) from the live dashboard and TESTED
that fear — and largely refuted it:**
- The rise is **real incidence growth, not survivorship.** True incidence (everyone who disappeared
  that year, any current status) went ~100 (2000) → ~3,000 (2007, drug-war onset) → ~37,000 (2025).
  Old years are small because few people disappeared *and were registered* then, not because they
  were resolved — 2000-cohort cases are only ~19% resolved.
- **Resolution runs opposite to the naive guess:** OLDER cohorts are LESS resolved (~16–27% pre-2006)
  than recent ones (~65–70%). Likely because pre-2006 the registry held disproportionately genuine
  long-term disappearances, while the post-2007 surge sweeps in many quickly-located people (and the
  contested 2023 *censo* may inflate recent "locations" — see §3 note).
- We now **can** compute resolution/recovery rates — at the aggregate (year/state) level — via the
  flow endpoints. National, at the 2026-08-15 freeze: **134,268 still missing, 272,985 located
  (249,502 alive and 23,483 found dead), of 407,253 records**. (An earlier draft of this file
  quoted 135,092 / 268,171 / 22,621 from the 2026-06-19 pull; those are superseded.)
- Lesson recorded honestly: our first "recent acceleration overstates incidence" caveat was itself
  overstated. Better data corrected it. See figs `08_incidence_vs_stock` and `09_resolution_by_year`.
- **But "not survivorship" is not the same as "more violence" (added 2026-08-29).** Refuting the
  stock artifact says the cohorts really did grow; it says nothing about *why*. Tested against
  SESNSP homicide victims (`src/incidence_vs_homicide.py`, article fig I), the two series rise
  together 2015–2018 and then part: 2019→2024 homicides −13.4% while recorded disappearances
  +43.4%, r = 0.28 across 2015–2025. Part of the growth is intake capacity — the búsqueda
  commissions created by the 2017 Ley General took 5.0% of records for disappearance-year 2017 and
  47.7% for 2025 (non-confidential records only, so 63.2% of the registry). **Treat registry growth
  as growth in the registry, never as a measured change in how many people disappear.**
- The substitution hypothesis — that deaths are relabelled as disappearances to flatter the homicide
  count — is **not supported** (`src/outcome_vs_homicide.py`, article fig J). Of the +10,905 records
  gained for 2019–2024, 61.7% are found alive, 36.8% still missing, 1.4% found dead; and homicides
  plus registry found-dead fell together, 36,638 → 32,133. What this cannot rule out: a body never
  found enters neither statistic, and nothing here sizes that gap.
  > **Audit correction (2026-10-12, `reports/corrections_log.md` C-01/C-04/C-12):** the test
  > above used the wrong sum. Deaths recorded as disappearances would sit in *still missing*, and
  > homicides + still missing is nearly flat (42,970 → 42,326). The 10,905 is also a difference
  > between cohort sizes, not records gained. Revised reading: most of the growth is people now
  > recorded found alive, which weighs against substitution as the main story, but a partial shift
  > cannot be excluded; found dead is right-censored for recent cohorts.

## 3. Two categories lumped together
- **Desaparecida** = absence presumed linked to a *crime* (e.g. forced disappearance).
- **No localizada** = whereabouts unknown, *no evidence of a crime* (may be voluntary, accident).
These mean different things. For a violence-focused analysis, `DESAPARECIDA` is the more
appropriate denominator. `CONFIDENCIAL` records hide which category they belong to.

### Note — are these categories used to "cover for" the state? (the politics of the count)
A reasonable suspicion, and one that is **documented, not just folklore** — but aim it precisely.
- **The labels are real, not invented dodges.** "Persona desaparecida" and "persona no localizada"
  are both defined in the 2017 *Ley General en Materia de Desaparición Forzada*. So `NO LOCALIZADA`
  is a lawful category, not by itself a cover-up. In our snapshot it's also *small* (4,818), which
  argues against it being the main minimization lever.
- **The real lever is the "located" purge — and it's exactly what creates our stock-vs-flow gap.**
  The AMLO government's 2023 door-to-door *censo* (Estrategia Nacional de Búsqueda Generalizada)
  reclassified large numbers of people as **located** and removed them from the active count,
  driving the "active disappearances" figure down to ~43,128. Critics — including **Karla Quintana,
  who resigned as head of the CNB over it** — warned that cases were marked located on administrative
  criteria (name matches, signs of activity) *without confirming whereabouts*. Quinto Elemento Lab
  found people listed as "located" whose families say they are **still missing**.
- **Data implication for us:** the ~262k "located" people absent from our file are **not all truly
  found.** An unknown share were administratively removed. So our still-missing stock may *under*count
  the genuinely-missing, and the depletion of older years is part real resolution, part contested
  reclassification. Treat "located" as "removed from the registry," **not** "confirmed found."
- **How to stay honest:** never present the government's "active" figure as the size of the crisis
  without the families'/collectives' contested-count framing alongside it (the dispute itself is data).

Sources: [Fundar — "el juego de las cifras"](https://fundar.org.mx/la-cndh-al-servicio-del-juego-de-las-cifras-sobre-personas-desaparecidas/),
[Quinto Elemento — "localizadas que siguen desaparecidas"](https://quintoelab.org/project/decenas-personas-localizadas-censo-siguen-desaparecidas),
[A dónde van los desaparecidos](https://adondevanlosdesaparecidos.org/2026/01/08/abandonan-censo-de-amlo-anuncian-nuevo-computo-de-desapariciones/),
[Animal — "una cifra en disputa"](https://grupoanimal.mx/sociedad/desaparecidos-cifra-en-disputa-familias-colectivos-crisis).

## 4. Redaction (`CONFIDENCIAL`) is all-or-nothing → shifting denominators
100% of confidential records have **no date, sex, age, or status** — only a state + ID.
Consequences:
- Charts use **different denominators**: state counts/rates use all 133k; year/age/sex charts
  use only the ~84k non-confidential (and ~90% of those with a usable date). Always state the base.
- **Cross-state comparison of anything finer than the count is confounded by redaction practice.**
  Confidential records keep their state, so state counts and rates include them; but every
  date-, age-, sex- or status-based comparison by state uses only the published records, and
  states publish very different shares (Jalisco 66.9%, Nayarit 66.2% confidential vs national
  36.8%). Counts themselves are separately affected by how completely each state feeds the
  registry (see `docs/cases/`). Redaction share is itself a transparency variable, not noise.
  (Corrected 2026-10-19: an earlier version said redaction could raise a state's rank; it
  cannot, since redacted records are still counted.)

## 5. The two date fields are effectively one
`FECHA_REGISTRO` ≈ `FECHA_DESAPARICION` (registration lag: median 0 days, 99.5% same year), so
`FECHA_REGISTRO` carries no independent signal about reporting delay. Don't analyze "lag".

**Why (established 2026-08-29).** The two fields differ in only 32% of non-confidential
records, and where they differ the gap is hours or days, not months. `FECHA_REGISTRO` is
therefore the moment the *originating authority took the report*, not the moment the
record entered the federal registry. Records for disappearance years long before RNPDNO
existed carry pre-2017 registration dates, which a genuine registry-entry field could not.
Consequence: **the mirror cannot measure retrospective registration at all.** Any attempt
to estimate how much of a year's cohort was added later — the natural test for whether
registry growth reflects reporting expansion — is not answerable from this field.

## 6. Structural blind spots (true of the registry itself, not just our copy)
- **Only reported cases.** Underreporting (fear, distrust of authorities, mixed-status families)
  is large and **uneven across states** — so even true incidence is undercounted unevenly.
- **No cause and no outcome** recorded (no perpetrator, no found-alive/found-dead field).
- **Geography = place of the disappearance event** (assumed; not place of residence). State of
  the *body's discovery* is a different thing entirely — relevant for the Stage-2 buscadoras work.
- **Single snapshot.** This is one community mirror at one date; RNPDNO revises retroactively, so
  totals here will not exactly match the live dashboard. Treat every figure as "as of <date>".

## 7. Opacity vs. State Capacity/Corruption (Negative Control)

To investigate whether the high rates of redaction (`CONFIDENCIAL`) are simply a byproduct of low state capacity or general administrative corruption, we ran a negative control test. We merged the state-level redaction rates with the INEGI ENCIG 2025 (Corruption Prevalence) and PIBE 2024 (Economic Capacity/GDP per capita) datasets.

The correlations show **no detectable association between redaction rates and economic output per capita or citizens' experience with general corruption** (with n = 32, only strong associations were detectable, and GDP per capita is a rough proxy for capacity, not a measure of it):
- **Corruption Prevalence:** Very weak negative correlation (Pearson *r* = -0.1917, p-value = 0.2933; Spearman ρ = -0.2416, p-value = 0.1829). The relationship is not statistically significant.
- **Economic Capacity:** Very weak positive correlation with Pearson (*r* = 0.2237, p-value = 0.2184) and essentially zero rank correlation (Spearman ρ = 0.0517, p-value = 0.7788). Both are statistically insignificant.

**Conclusion:** Neither general corruption experience nor economic output per capita shows a
detectable association with how much of a state's registry is published. Together with the homicide-rate result (Pearson *r* = −0.38
across all 32 states), this finds no support at state level for the three most obvious structural explanations —
violence, corruption, and state wealth — for why publication practice varies so widely between
states. Redaction does not rise with violence; the other two are nulls of limited power.

Two limits on what that licenses:

- **These are null results, and a null result does not identify a cause.** Ruling out three
  explanations does not establish that redaction is deliberate, or that any particular record was
  redacted for any particular reason. The evidence for administrative rather than family-driven
  redaction comes from the documentary record (CNB oficio 1349/2020; the Jalisco blanket
  declaration; active search notices on confidential cases) and from the batch movement visible
  across snapshots — not from these correlations.
- **The variation is concentrated at the state level**, which is consistent with publication
  practice being set per *fiscalía*. The clearest contrast is Jalisco at 66.9% against Guerrero
  at 9.1% and Chihuahua at 8.8% — note that the extremes run in both directions, and that the
  least-redacted states include some of the most violent. Guerrero's low share is not
  transparency; see [cases/guerrero.md](cases/guerrero.md) on under-registration.

All correlations reproduce from `src/stat_correlations.py` against
`data/processed/state_correlations.csv` (n = 32).

---

## What each existing figure is safe to claim
| Figure | Safe reading | Do NOT say |
|---|---|---|
| `01_disappearances_by_year` | Stock of people who went missing in year Y **and are still missing** | "Disappearances rose 150×" |
| `02_by_state` | Where the most *unresolved* cases are registered | "Where most people disappear" (ignores redaction + reporting bias) |
| `03_age_sex` | Demographics **among non-confidential, dated** records (~38% of file) | That it represents all victims |
| `04_redaction_by_state` | How opaque each state's data is | That redaction = more disappearances |
| `05_rate_by_state` / `06_choropleth` | Unresolved cases per 100k residents | "Disappearance rate" without the stock/reporting caveats |

## Open questions worth resolving next
1. **De-bias the trend with the flow (incidence + resolution).** Record-level data *with* located
   people is NOT cleanly public (the mirror we have is still-missing only). BUT the official RNPDNO
   dashboard publishes **aggregate** counts by status — including `LOCALIZADA CON VIDA` / `SIN VIDA`
   — by year/state/sex, reachable via its JSON endpoints (automated by `irvingfisica/reqrnpdno`) and
   via Data Cívica's reconstructions (their "Volver a desaparecer" project tracks names that fall off
   the list = located-or-re-disappeared). So the flow IS obtainable at the aggregate level — enough to
   compute resolution rates and reweight the year chart. (Treat "located" per the §3 note.)
2. ✅ **RESOLVED (`src/category_compare.py`).** Adding `NO LOCALIZADA` to `DESAPARECIDA` moves the
   national count only **+6.1%** (among non-confidential) — a minor headline risk. BUT it is highly
   state-dependent: **Zacatecas +42%, Chiapas +29%, Chihuahua +27%** vs. ~0% in Tamaulipas/Veracruz/
   Sonora. So state comparisons must fix the category choice, and heavy `NO LOCALIZADA` use is worth
   reading against the §3 minimization note. The 36.8% confidential bucket remains the larger unknown.
3. ✅ **RESOLVED (`src/crosscheck.py`).** National drift between the mirror and the live registry is
   **−0.11%** as measured at the 2026-08-15 refresh (see `data-refresh-2026-08-15.md`); an earlier
   check against the 2026-05-27 official figure of 134,481 put it at −0.7%. Either way the mirror is
   a slightly earlier but recent snapshot, trustworthy as a cross-section. *(Audit correction 2026-10-12: the −0.11% compared the mirror's 133,566 rows — including 2,964 with no state — with the live 133,416 state-assigned records. Like for like: −0.5% overall (133,566 vs 134,268) and −2.1% state-assigned (130,602 vs 133,416).)* Per-state drift is 0–7%, mostly negative (mirror just behind latest). **Jalisco is
   the outlier** (ours +7.7% vs the May figure, yet below the June ">15,000" claim): sources disagree
   by thousands, so treat Jalisco's number with explicit care in any output.
