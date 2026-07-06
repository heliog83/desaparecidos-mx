# What Are We Counting? — Methodology & Data Caveats

This file is the project's conscience. Every chart and claim inherits these caveats. Read it
before interpreting any number. Findings here come from interrogating `data/external/data.csv`
(133,566 records, RNPDNO mirror) on 2026-06-19; re-run `src/interrogate.py` to refresh.

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
  flow endpoints. National: 135,092 still missing, 268,171 located, **22,621 found dead**.
- Lesson recorded honestly: our first "recent acceleration overstates incidence" caveat was itself
  overstated. Better data corrected it. See figs `08_incidence_vs_stock` and `09_resolution_by_year`.

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
- **Cross-state comparison is confounded by redaction practice.** A state can rank "high" partly
  because its prosecutor redacts more (Jalisco 67%, Nayarit 66% vs national 37%), not only because
  more people vanish there. Redaction share is itself a transparency variable, not noise.

## 5. The two date fields are effectively one
`FECHA_REGISTRO` ≈ `FECHA_DESAPARICION` (registration lag: median 0 days, 99.5% same year), so
`FECHA_REGISTRO` carries no independent signal about reporting delay. Don't analyze "lag".

## 6. Structural blind spots (true of the registry itself, not just our copy)
- **Only reported cases.** Underreporting (fear, distrust of authorities, mixed-status families)
  is large and **uneven across states** — so even true incidence is undercounted unevenly.
- **No cause and no outcome** recorded (no perpetrator, no found-alive/found-dead field).
- **Geography = place of the disappearance event** (assumed; not place of residence). State of
  the *body's discovery* is a different thing entirely — relevant for the Stage-2 buscadoras work.
- **Single snapshot.** This is one community mirror at one date; RNPDNO revises retroactively, so
  totals here will not exactly match the live dashboard. Treat every figure as "as of <date>".

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
   reading against the §3 minimization note. The 37% confidential bucket remains the larger unknown.
3. ✅ **RESOLVED (`src/crosscheck.py`).** National drift vs the official RNPDNO figure (134,481 on
   2026-05-27) is **−0.7%** — our mirror is a slightly earlier but recent snapshot, trustworthy as a
   cross-section. Per-state drift is 0–7%, mostly negative (mirror just behind latest). **Jalisco is
   the outlier** (ours +7.7% vs the May figure, yet below the June ">15,000" claim): sources disagree
   by thousands, so treat Jalisco's number with explicit care in any output.
