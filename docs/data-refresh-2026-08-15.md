# Data refresh audit — 2026-08-15

Pre-publication re-pull of every input behind `reports/article_draft.md`, with a
number-by-number diff against the figures the draft currently cites (pulled
2026-06-19, microdata snapshot 2025-12-02).

**Verdict: the draft's argument survives intact. Three numeric edits are required,
one caption is now wrong, and the refresh produced one genuinely new finding
(Ciudad de México) that strengthens §5b.**

---

## 1. What could and could not be refreshed

| Source | Status | Freshest available |
|---|---|---|
| RNPDNO live dashboard API | ✅ refreshed | **2026-08-15** (this pull) |
| lapanquecita mirror (record-level microdata) | ❌ **frozen** | 2025-12-02 (unchanged) |
| CNB oficio 1349/2020, ZonaDocs, Tlachinollan, HRW | n/a (documentary) | unchanged |

### The mirror is dead
`lapanquecita/personas-desaparecidas` last pushed **2025-12-02**. It had updated on
the 1st–4th of every month from April 2025; that cadence stopped after December and
has not resumed in eight months. Our local `data.csv` is **byte-identical** (md5
`69b60ff303e36c244f492097228825de`) to the pinned upstream commit `666b3e7605`, so
the snapshot we hold is the freshest record-level data that exists from this source.

Consequence: **the stock/redaction figures (C, D, and the 36.8% headline) cannot be
made fresher.** They are now an 8.5-month-old cross-section carried inside an
article whose flow figures are current. The methods note must say so explicitly —
see §5.

---

## 2. National totals — live API, 2026-06-19 → 2026-08-15

| Metric | Jun 2026 | Aug 2026 | Change |
|---|---:|---:|---:|
| Total reported (all outcomes) | 403,263 | 407,253 | +3,990 |
| Still missing | 135,092 | **134,268** | −824 (−0.6%) |
| Located (all) | 268,171 | 272,985 | +4,814 |
| Located alive | 245,550 | 249,502 | +3,952 |
| **Found dead** | 22,621 | **23,483** | **+862 (+3.8%)** |

The still-missing count *fell* while total reports rose — resolution outpaced new
registrations over the eight weeks.

## 3. Figure A window (2000–2025) — **caption edit required**

| Band | Draft says | Now | Δ |
|---|---:|---:|---:|
| Found alive | ~212,900 | **214,643** | +1,767 |
| Found dead | ~19,900 | **20,551** | +631 |
| Still missing | ~118,600 | **117,100** | −1,484 |
| Total reported | "roughly 350,000" | 352,294 | still "roughly 350,000" ✅ |

Structural claims all hold:

- Growth anchors: 2000 = 102 (draft "~100" ✅), 2007 = 3,034 ("~3,000" ✅),
  2025 = 37,124 ("~37,000" ✅).
- Resolution inversion holds and **strengthened**: 2000 cohort 18.6% resolved,
  2005 27.4%, vs 2015 70.5% / 2024 66.0% / 2025 68.1%. The draft's "~16–27% vs
  ~65–70%" is still accurate.

## 4. Stock figures — **all unchanged** (same microdata)

Every one of these reproduced exactly:

| Claim | Draft | Verified |
|---|---:|---:|
| Records | 133,566 | 133,566 ✅ |
| National redaction | 36.8% | 36.8% ✅ |
| Jalisco redaction | 67% | 66.9% ✅ |
| Nayarit redaction | 66% | 66.2% ✅ |
| Guerrero / Colima | 9% | 9.1% / 9.0% ✅ |
| Tamaulipas rate | 359 | 359.1 ✅ |
| Zacatecas / Sinaloa rate | 226 / 211 | 225.8 / 211.3 ✅ |
| Jalisco n | 13,766 | 13,766 ✅ |
| Guerrero n | 4,453 | 4,453 ✅ |
| §4 "one-seventh of its redaction share" | — | 66.9/9.1 = 7.35× ✅ |

Version audit (fig H) also reproduced exactly: confidential 44,035 → 49,136
(+5,101), share 34.69% → 36.79%, and +5,101 / +6,624 net growth = **77.0%** ✅.

## 5. Snapshot mismatch — the one real vulnerability

National drift between the Dec-2025 microdata and the Aug-2026 live registry is
**−0.11%** (133,566 vs 133,416 excluding "se desconoce"), which is reassuring.
*(Audit correction 2026-10-12: this compares unlike populations — the 133,566 includes the
mirror's 2,964 no-state records. Like for like the drift is −0.5% overall and −2.1% for
state-assigned records, 130,602 vs 133,416. See `reports/corrections_log.md` C-06.)* But
per-state drift is not uniform:

| State | Mirror (Dec 2025) | Live (Aug 2026) | Drift |
|---|---:|---:|---:|
| **Ciudad de México** | 7,242 | 5,915 | **−18.3%** |
| Yucatán | 313 | 378 | +20.8% |
| Campeche | 148 | 172 | +16.2% |
| Tabasco | 2,058 | 2,347 | +14.0% |
| Chiapas | 1,776 | 1,989 | +12.0% |
| Baja California | 4,660 | 5,167 | +10.9% |
| Michoacán | 7,234 | 7,992 | +10.5% |
| Nayarit | 1,990 | 2,190 | +10.1% |
| **Jalisco** | 13,766 | 12,964 | **−5.8%** |
| Guerrero | 4,453 | 4,681 | +5.1% |

**§2 needs a numeric edit.** The draft says Estado de México and CDMX "fall to ~80"
per 100k. EdoMex holds (82.3), but CDMX on live data is now ~64 per 100k, not 79.
Either re-state as "EdoMex ~82, CDMX ~64" or keep the stock-vintage number and label
the vintage.

## 6. New finding — Ciudad de México is a second Jalisco

The refresh surfaced a purge the June pull only hinted at:

| Date | CDMX still missing | Source |
|---|---:|---|
| 2025-04-03 | 6,025 | mirror panel |
| 2025-12-02 | **7,242** | mirror panel (+1,217 over 8 months) |
| 2026-06-19 | 6,086 | live API |
| 2026-08-15 | **5,915** | live API (−1,327 from peak) |

CDMX climbed steadily all through 2025 — the version audit already flagged it as a
"steady climb, +1,075" of *confidential* records — and then gave the entire increase
back and more during the first half of 2026. Raw API labels are unambiguous
(`CIUDAD DE MEXICO` vs `ESTADO DE MEXICO`), so this is not a matching artifact.

This is the same signature the article documents for Jalisco: a bulk reversal with no
public log. It is a strong addition to §5b, and it means the batch-rewriting claim is
not a Jalisco/Tamaulipas peculiarity. **Framing caution:** we have three points
(Dec/Jun/Aug), not a monthly series, so describe the direction and magnitude, not a
mechanism — we do not know whether these are deletions, reclassifications, or
resolutions.

## 7. Jalisco — post-recount rebound

Federal Jalisco went 15,015 (Mar 2025) → 12,776 (Jun 2026) → **12,964** (Aug 2026):
the count is edging back up after the recount trough while the state registry sits
~3,000 higher. `src/jalisco_divergence.py` now carries both API points (fig 21 / F
rebuilt).

---

## Edits required before publishing

1. **§1 fig-A caption** — 212,900/19,900/118,600 → **214,600/20,600/117,100**;
   change consultation date to 2026-08-15.
2. **§2** — CDMX "~80" is wrong on live data (~64). Fix the number or label the vintage.
3. **Methods note** — state the two vintages explicitly: flow/API data 2026-08-15,
   record-level stock 2025-12-02, and say the mirror stopped updating.
4. **§5b** — add the CDMX reversal (optional but recommended; it generalizes the claim).
5. Everything else stands as written.

## Reproduction

```bash
MPLBACKEND=Agg python src/fetch_flow.py       # live API (this pull: 2026-08-15)
MPLBACKEND=Agg python src/clean.py            # microdata -> parquet
MPLBACKEND=Agg python src/rates.py
MPLBACKEND=Agg python src/category_compare.py
MPLBACKEND=Agg python src/crosscheck.py
MPLBACKEND=Agg python src/flow_consolidated.py
MPLBACKEND=Agg python src/article_figs.py     # A-D
MPLBACKEND=Agg python src/consent_accounting.py    # E
MPLBACKEND=Agg python src/jalisco_divergence.py    # F
MPLBACKEND=Agg python src/two_modes.py             # G
MPLBACKEND=Agg python src/version_audit.py         # H
```

Note `src/crosscheck.py` still compares against hand-collected press figures from
2026-05-27 (national 134,481). Our own API pull is now a better reference
(134,268 at 2026-08-15, drift −0.5% vs the mirror); worth rewiring before publication.
