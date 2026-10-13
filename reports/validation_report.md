# Validation report — 2026-10-12

Every result below was produced by actually running the command, in this audit, on
branch `claude/desaparecidos-mx-audit-0cb93d` (base `c4838cc`) with uncommitted audit
changes. Nothing is reported as passing that wasn't executed. Tests that couldn't run
are marked **BLOCKED**.

## Reproduce

```bash
python3 src/build_page.py        # build (stdlib)
python3 src/check_article.py     # freeze hashes + embedded data + PNG hashes (stdlib)
python3 src/check_claims.py      # 53 prose claims recomputed from the freeze (stdlib, new)
python3 src/check_figures.py     # figure numbering (stdlib)
python3 src/stage2_validate.py   # Stage-2 schema
python src/audit_sensitivity.py <path/to/rnpdno_mirror_2025-12-02.csv>   # pandas/scipy; needs raw mirror
```

## Results

| # | test | command / method | result |
|---|---|---|---|
| V-1 | Raw-source integrity | sha256 of all 29 manifest entries in the main checkout, where the gitignored raw sources live | **PASS**: 29/29 match |
| V-2 | Build | `python3 src/build_page.py` | **PASS**: 2.82 MB |
| V-3 | Deterministic build | build twice, `cmp` | **PASS**: byte-identical |
| V-4 | Freeze and article fidelity | `python3 src/check_article.py` | **PASS**: 13 files hash-verified (12 on a clean checkout); 10 article PNGs hash-verified; 407,253 / 134,268 / 352,294 |
| V-5 | Prose claims | `python3 src/check_claims.py` | **PASS**: 53/53 |
| V-6 | Prose-claim checker detects errors | mutated copy of the draft (61.7 → 61.8; −0.38 → −0.40) | **PASS**: both mutations reported, exit 1 |
| V-7 | Clean checkout | tracked + new files copied to an empty dir (no raw data, no parquet); system Python 3.9.6 | **PASS**: check_article, check_claims, rebuild byte-identical to the worktree build |
| V-8 | Figure numbering | `python3 src/check_figures.py` | **PASS**: 28 figures, contiguous |
| V-9 | Stage-2 schema | `python3 src/stage2_validate.py` | **PASS** (5 seeds; illustrative only) |
| V-10 | Python syntax | `python3 -m py_compile src/*.py dashboard/*.py` | **PASS** |
| V-11 | JS syntax | `node --check src/article_interactive.js` | **PASS** |
| V-12 | Independent recomputation | scratch scripts reading raw API JSON and mirror CSV (not project derived tables) | **PASS** for all registry rows marked SUPPORTED; see `claim_registry.csv` |
| V-13 | Sensitivity analyses | `src/audit_sensitivity.py` | **RAN**: results in `audit/sensitivity_results.md` |
| V-14 | Primary document | `pdftotext` of CNB oficio; figures checked on PDF p. 11 | **PASS** (73,388 / 77.40% / 52.31% / 46.98%) |
| V-15 | Responsive layout | built-in Chromium; 320/375/390/768/1440 px; geometry probe | **PASS** after fixes (one known Fig D label overlap at ≥768 px, kidnapping view) |
| V-16 | Every control, every chart | 90 scripted interactions per run, at 320 (dark), 375 (dark), 768 (light), 1440 (light) | **PASS**; `aria-pressed` consistent; no NaN/undefined text |
| V-17 | Console errors | `read_console_messages` after each run | **PASS**: none |
| V-18 | No-JavaScript | temporary copy with scripts stripped (deleted after) | **PASS**: shells hidden, six fallbacks open, all images load |
| V-19 | Corrupt data payload | temporary copy with broken JSON (deleted after) | **PASS**: all interactive figures fall back to static images |
| V-20 | Keyboard | skip link first; map Enter selects state and syncs explorer; focus shows tooltip | **PASS**; focus events had to be dispatched because the hidden pane lacked window focus |
| V-21 | Theme | Light / Dark / Auto toggle; computed colours | **PASS** |
| V-22 | Text contrast | WCAG formula on 24 colour pairs | **PASS** for all text after the hero-gloss fix; 2 non-text pairs below 3:1 (documented) |
| V-23 | Staging assembly | `pages.yml` steps reproduced locally (`_site/index.html` + token grep) | **PASS**: the staged file is byte-identical to the tested `reports/article.html` |
| V-24 | External resources | grep for external `src=` in the page | **PASS**: none (only outbound citation links) |
| V-30 | Fig K (added after the audit) | build + `check_article.py` (new table and PNG hash-pinned, table in `BUILD_INPUTS`) + `check_claims.py` (60 claims, 7 new) + `check_figures.py` (29 contiguous) | **PASS** |
| V-31 | Fig K deterministic redraw | `filing_authority.py` from the pinned table, twice; sha256 compared | **PASS**: byte-identical |
| V-32 | Fig K layout | 320/375/390/768/1440 px: axis-to-track offset 0 px, no tick overlap, no row overflow, no page overflow; dark and light | **PASS** after 3 fixes (column-header overflow, prose list styles leaking into rows, em-based columns misaligning the axis) |
| V-33 | Fig K without JS; other charts regression | no-JS copy: K shows all 17 rows; 90 interactions on the other charts at 320 px | **PASS** |
| V-34 | E-1 standfirst | build reads it from the draft (single copy) and fails if the frozen still-missing total is absent; 4 new STAND-* checks | **PASS**: 64/64 |
| V-25 | Screen reader (VoiceOver/NVDA) | — | **BLOCKED**: not available in this environment |
| V-26 | Real mobile devices / Safari / Firefox | — | **BLOCKED**: only built-in Chromium available |
| V-27 | Remote staging deploy | — | **BLOCKED by design**: needs your approval and a host decision |
| V-28 | External sources not re-fetched (72,172 bodies; Tlachinollan; HRW; Proceso; Data Cívica 2023 names) | — | **NOT RE-VERIFIED**: attribution consistent with project notes |
| V-29 | `dashboard/app.py` | — | **NOT RUN**: out of scope for the article; compiles (V-10) |

## Consistency: article ↔ captions ↔ chart data ↔ methods

- Headline totals and Fig A sums: enforced by `check_article.py`.
- 53 prose numbers: enforced by `check_claims.py` against the same freeze tables the
  charts embed.
- PNG captions for C, G and J were corrected to match the prose, re-rendered, and their
  hashes amended in the manifest. The other seven PNGs are unchanged and their text was
  read for conflicts: none with the corrected prose, except the Fig J annotation "Found
  dead barely moves", which is accurate.
- `docs/methodology.md` (§2 substitution paragraph, open question 3) and
  `docs/data-refresh-2026-08-15.md` (§5 drift) carried the two corrected inferences.
  Dated audit-correction notes were added in place; the history was not rewritten.
