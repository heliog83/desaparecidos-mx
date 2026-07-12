# What Does Opacity Mean Here? — 1-Page Memo

Date: 2026-07-06. Basis: `docs/opacity-mechanism.md`, `docs/cases/jalisco.md`,
`docs/cases/guerrero.md`. All figures carry consultation dates in those files.

## The claim

**CONFIDENCIAL in the RNPDNO public version is an administrative redaction artifact —
shaped by consent-documentation gaps, fiscalía capture practice, and at least one
documented blanket state policy — not a measure of family privacy preference. And
redaction is only one of two modes of registry opacity: states can hide the recorded
(Jalisco) or fail to record at all (Guerrero).**

## What the data shows

36.8% of unresolved records in our mirror are fully redacted (all fields lost except
state). The share varies from 67% (Jalisco) and 66% (Nayarit) down to ~9% (Guerrero,
Colima), and the variation does not track violence: Guerrero has ~2.4× Jalisco's
homicide rate and one-seventh its redaction share.

## What the mechanism says

Federal law (Art. 108, Ley General en Materia de Desaparición) makes publication
consent-based, collected by whoever captures the report — ~79% state fiscalías. The
CNB's own 2020 consulta to INAI admits 77.4% of records then had *no consent
information at all* (defaulting to confidential), that families split ~half/half when
actually asked, and — footnote 3 — that **Jalisco's Fiscalía declares its entire
federal submission non-publishable**. Journalists later found 4,765 cases in six
states with active public search notices yet marked confidential, and authorities
admitted no risk assessment underlies the classification (ZonaDocs, 2024-11-21).

## Why the Jalisco–Guerrero contrast matters

Same federal rules, opposite outcomes, both bad:

- **Jalisco (redaction opacity):** blanket fiscalía non-consent policy (documented
  2020), stopped feeding the federal registry from 2022 in favor of its own REPD,
  federal-vs-state totals diverge by hundreds, 1,026 confidential records with active
  search notices, and a mother on record who never requested confidentiality.
- **Guerrero (omission opacity):** low redaction — partly because historic
  grave-violation cases (Guerra Sucia, Ayotzinapa) legally disfavor confidentiality —
  but collectives document substantially more disappeared than the state registers
  (623 in Iguala alone vs ~3,800 statewide official), prosecutors stall or discourage
  reports, and new cases surface at collective searches rather than at the ministerio
  público.

Consequence for analysis: cross-state comparisons of the confidential share measure
*institutional publication practice*, and a low share must never be read as better
data — it may mean the missing were never counted.

## What we still cannot prove

- Per-record cause of any CONFIDENCIAL flag (no microdata field distinguishes family
  request / missing paperwork / blanket policy).
- Whether the consent declarations Jalisco invokes exist (the CNB could not produce
  them when INAI ordered release, RRA 09082/20).
- Whether the confidential share grew across registry versions.
- Intent. "The state hides records deliberately" remains an unsafe claim; "redaction
  is unexplained, unaudited, and contradicted by public search notices" is safe.

## What would test it next

1. **Version audit — EXECUTED 2026-07-11, claim CONFIRMED** (`src/version_audit.py`,
   fig 23/H): across ten monthly mirror snapshots (Apr–Dec 2025), confidential
   records grew +5,101 nationally — 77% of the registry's net growth — and the
   movement is batched, not gradual: Tamaulipas reclassified ~2,500 existing records
   in two months (share 20%→39%, totals flat); Jalisco removed ~1,400 confidential
   records in Q4 2025 (before the recount announcement); Tabasco batch-deleted a
   third of its records in November. Batch signatures are administrative, not
   family decisions. Data Cívica's Aug/Dec-2023 person-level bases (downloaded, in
   scratch) remain available for a longer-horizon person-level version of this test.
2. **Targeted transparency requests** replicating ZonaDocs' method for our six case
   states: ask each fiscalía how many consent declarations it holds vs records
   submitted (tests the paperwork-default hypothesis directly).
3. **Stage 2 find-events** — if collective-led finds cluster in *both* opacity modes,
   that supports the framing that buscadoras reveal what the state fails to document,
   whichever way it fails.
