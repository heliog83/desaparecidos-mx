# Publication checklist — *The Redacted Crisis*

Gate date 2026-10-12. **Nothing has been published, deployed or pushed.** The branch
holds uncommitted audit changes for your review.

## Recommendation: **CONDITIONAL GO**

The evidence base is sound and reproducible. Every headline number reproduces
exactly from hash-verified raw sources, and the two-vintage architecture holds. The
audit found one conclusion that was wrong (the §2/Fig J substitution test), several
overstated attributions, and some chart bugs. All are fixed and validated. Publication
should wait on three conditions that only you can clear: G-1 to G-3 below. Nothing
else is blocking.

## Gate — must be done before publication

- [x] **G-1 Author sign-off on the substantive corrections** (given 2026-10-12), especially C-01/C-12
      (the §2 conclusion now says a partial shift of deaths into "still missing"
      *cannot be excluded*), C-05 (§9) and the new §6b paragraph on the March 2026
      reclassification. Read `audit/article_draft_corrections.diff`.
- [x] **G-2 Reader-facing reproducibility links work.** (2026-10-12: repository made public at the author's choice; full history scanned first: no raw data, PDFs or secrets) The repository is private, so the
      methods-note links to GitHub are dead for readers. Make it public (the `.gitignore`
      already excludes the oficio and scratch packets; check `git ls-files` once more),
      publish a public mirror of `src/`, `docs/` and the freeze, or archive them (e.g.
      Zenodo DOI) and relink.
- [x] **G-3 Licence.** (2026-10-12: `LICENSE` MIT for code; `LICENSE-CONTENT.md` CC BY 4.0 for text, figures and derived tables, plus third-party data terms) Add `LICENSE` (suggested: CC BY 4.0 for text and figures, MIT for
      code) and a data-terms note for the RNPDNO, the lapanquecita mirror, SESNSP and INEGI.

## Strongly recommended before publication

- [x] **R-1** Language: English (decided 2026-10-12). Nothing in the article needed changing.
- [x] **R-2** (done 2026-10-12: dropped, A-08) Resolve the June-2026 points (CDMX 6,086; Jalisco 12,776): restore the raw
      pull into a freeze amendment, or drop them from §6b, Fig F and its caption.
- [x] **R-3** (done 2026-10-14: all 5 external sources re-fetched and verified verbatim) Re-fetch the external figures not re-verified here: 72,172 bodies;
      Tlachinollan 3,800 / 260 / 69 / 2–6%; HRW >160; Proceso Holy Week; Data Cívica's
      2023 10,953.
- [ ] **R-4** Screen-reader pass (VoiceOver + NVDA) and Safari/Firefox, iOS and Android
      checks (BLOCKED here).
- [x] **R-5a** E-3 applied (§6 + Fig K), validated.
- [x] **R-5b** E-1 applied (standfirst), validated.
- [x] **R-5c** (done 2026-10-15: E-2 kept §2 intact for claim/chart continuity; E-4 split §6b into §6b and §6c; E-5 locked in *The Redacted Crisis: What Mexico's public registry leaves unseen*) Decide on E-2 (compress §2), E-4 (split §6b), E-5 (headline).
- [x] **R-6** (done: https://heliog83.github.io/desaparecidos-mx/) Set the canonical URL once the host is chosen: add
      `<link rel="canonical">` and `og:url` in `src/build_page.py`'s template. No URL
      was guessed.
- [x] **R-7** (done 2026-10-15) Commit the complete unit: draft, build, JS/CSS, figure scripts, 3 PNGs +
      2 numbered PNGs, manifest amendment, generated HTML, `check_claims.py`,
      `audit_sensitivity.py`, reports, `.gitignore`, `pages.yml`, docs notes.

## Can follow publication

- Roving tabindex or data tables to cut ~340 tab stops (visual audit, 2.4.3).
- Serve the PNGs as separate WebP files (2.8 MB → ~0.25 MB of HTML).
- Fig G's "size unknown" gradient; Fig H's non-zero-baseline note; Fig D's label overlap.
- Trim Fig D's selector to the three variables the text discusses.

## Platform and deployment

**Recommendation: GitHub Pages, through the existing `pages.yml`.** It's already in the
repository, deploys the reviewed committed bytes without rebuilding, and costs nothing.
This audit added a validation step to it: it now runs `check_article.py` and
`check_claims.py` on the committed page before deploying, using stdlib only, which works
on a clean checkout (tested, V-7). The workflow is still **manual-trigger only**.

Staging strategy:

1. **Local staging, done.** The `pages.yml` assembly steps were reproduced locally.
   The staged `index.html` is byte-identical to the tested `reports/article.html` (V-23).
2. **Remote staging, not done; needs your approval.** Pages gives one site per repo, so
   for an unlisted remote preview either (a) push the branch to a separate staging repo
   with Pages enabled, or (b) use a host with preview deployments (Cloudflare Pages or
   Netlify) pointed at a `_site` built by the same steps. Add
   `<meta name="robots" content="noindex">` to the staging copy only.
3. **Production:** after G-1…G-3, merge to `main`, then run "Publish article to Pages" by
   hand. Optional custom domain.

Per `AGENTS.md`, never publish through Claude Artifacts.

## Final handoff summary

| | |
|---|---|
| Already correct | All 15 freeze checks; headline totals; Fig A; redaction shares and rankings; rates; panel/version audit; consent accounting; ZonaDocs counts; drift by state |
| Incorrect or unsupported (now fixed) | Substitution inference (B-1); "only the state" (H-1); "records gained"; §9 overreach; 0.1% drift; Fig C JS national average; Yucatán highlight; §1 cohort descriptions; 8 overstated attributions; uncited killings |
| Added | §6 filing-authority finding + Fig K (E-3); Data Cívica 2026 (dated, not blended); March 2026 federal reclassification; sources [10]–[12]; `check_claims.py` (53 checks); `audit_sensitivity.py` |
| Still uncertain | The denominator of Data Cívica's 38.5%; the 2026 government report cited via a secondary source; filing-authority finding (case-mix confound) |
| Tests | 24 executed and passing; R-3 external figures re-fetched and verified (2026-10-14); 3 browser/screen-reader checks pending (see validation report) |
| Blockers | Cleared (G-1 author sign-off · G-2 public repository links · G-3 licence all completed) |
| Decision | **CONDITIONAL GO** |
