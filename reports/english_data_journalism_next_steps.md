# English Data-Journalism Version — Next Steps

## Target

Publish an English-language, data-journalism article centered on the RNPDNO public registry's
opacity problem: Mexico's disappearance registry counts the missing, but it also hides key
public information through redaction, batch reclassification, and omission.

## Working headline

**The Redacted Crisis: What Mexico's Missing-Person Registry Won't Let You See**

Alternative:

**132,000 People, One Third Behind a Wall**

## Audience

International readers who may know Mexico has a disappearance crisis, but do not know how the
official data works. Assume curiosity, not prior expertise. Explain each institution and acronym
once, then keep the story moving through charts and concrete state contrasts.

## Core claim

The public registry's `CONFIDENCIAL` label should not be read simply as family-requested privacy.
The evidence supports a narrower but powerful claim: public registry opacity is shaped by
administrative practice, missing consent documentation, blanket state policies, batch changes,
and under-recording. Cross-state comparisons therefore measure institutional publication behavior
as well as disappearance.

## Structure

1. Open with the scale of the crisis and the honest denominator: reported disappearances since
   2000 include people found alive, found dead, and still missing.
2. Show the geographic pattern by rate, then immediately complicate it with the redaction wall.
3. Establish that redaction does not simply track violence or crisis intensity.
4. Explain the consent mechanism and why the official privacy explanation fails.
5. Use version-history evidence to show that confidentiality changes in batches.
6. Use Jalisco as opacity by redaction.
7. Use Guerrero as opacity by omission.
8. Close with what can and cannot be claimed, then bridge to the madres buscadoras piece.

## Recommended figure set

- `reports/figures/article/A_outcomes_by_year.png`
- `reports/figures/article/C_confidential_share.png`
- `reports/figures/article/D_redaction_vs_rate.png`
- `reports/figures/article/E_consent_accounting.png`
- `reports/figures/article/H_confidencial_batches.png`
- `reports/figures/article/G_two_modes.png`

Hold `B_rate_map.png` and `F_jalisco_divergence.png` as optional supporting figures if the piece
needs more geographic or Jalisco-specific context.

## Editorial pass

- Replace internal research language with reader-facing explanations.
- Define RNPDNO, CNB, INAI, and `CONFIDENCIAL` in plain English.
- Keep caveats visible but brief; move detailed methods to a boxed note or appendix.
- Avoid intent claims such as "the state deliberately hides people."
- Prefer precise claims: "unexplained," "unaudited," "contradicted by public search notices,"
  "changed in batches," and "not comparable across states without opacity caveats."
- Keep the madres buscadoras material as the bridge to the next article, not the main quantitative
  claim of this one.

## Fact-check checklist

- National reported-flow totals and consultation date.
- Current unresolved registry total and consultation date.
- National confidential share.
- Jalisco and Guerrero confidential shares.
- Consent-accounting numbers from the 2020 CNB oficio.
- ZonaDocs active-search-notice contradiction count.
- Version-audit batch-change numbers.
- Jalisco federal/state registry divergence numbers.
- Guerrero collective-documented counts and source wording.

## Publication package

- Final article Markdown.
- Six publication figures.
- One compact methods note.
- One source list with consultation dates.
- Link to reproducible code and data caveats.

## Next dataset phase

After publishing this article, expand `data/stage2/clandestine_finds.csv` before making a
quantitative claim about madres buscadoras' recovery work. The current Stage 2 file is a seed
dataset, not yet enough for a full analysis.
