# Visualization, UX and accessibility audit

Tested 2026-10-12 against the rebuilt `reports/article.html`, served at
`http://localhost:8794/article.html`, in the Claude desktop app's built-in
(Chromium) browser. Method: scripted DOM and geometry probes plus a full control
cycle. 90 interactions per run: every `data-mode` button and every `<select>` option
in every chart. After each interaction the probe checked SVG overflow, text clipping,
text-on-text overlap, control-row overflow and page-level horizontal scroll.
Screenshots weren't usable as evidence because the pane was hidden, so the results are
geometric measurements, not visual impressions.

## Results matrix (after fixes)

| width | theme | page h-scroll | chart issues (90 interactions) | console errors |
|---|---|---|---|---|
| 320 | dark | 0 px | none | none |
| 375 | dark | 0 px | none | none |
| 390 | dark | 0 px | none (default modes probed) | none |
| 768 | light | 0 px | Fig D, kidnapping view: 1 label overlap | none |
| 1440 | light | 0 px | Fig D, kidnapping view: 1 label overlap | none |

**Before the fixes**, at 320 px: 8 px horizontal page scroll (Fig D `<select>`, 307 px
wide); 4 tick-label collisions on Fig C; the Fig A legend clipped in three single-series
views; 3 label collisions on the Fig J "Change 2019–2024" view.

## Per chart

| fig | one clear point? | correctness | fixed | open |
|---|---|---|---|---|
| Status bar | yes | Percentages derived at build time | — | — |
| Hero record | yes | Claimed one surviving field; there are two | `ORIGEN_REPORTE` row added; gloss contrast 2.67 → 5.05:1 | — |
| A outcomes | yes | Correct; the share view shows 2000–05 small-n cohorts (caveated in text) | Legend clipping; white separators between stacked segments (dead vs missing was 1.38:1) | ~78 focusable bars |
| I (static) | yes | Correct; provisional 2025 detached | — | — |
| J compare | yes, after correction | **Summary text was logically wrong** (dark bar vs still-missing); "gained" | Text, PNG and labels | — |
| B map + state explorer | yes | Rates verified; legend bins fixed thresholds | — | Legend colour-only (values in tooltip and ARIA); lightest bin vs white stroke 1.19:1 |
| C ranking | yes | **"National average" was a mean of state shares**; heading mentioned violence; Yucatán never highlighted (accent bug) | National 36.8% from records; "Median state" label; round ticks; accent-insensitive keys | Grey bars 2.06:1 vs white (each bar labelled with text) |
| D scatter | yes | r recomputed live; "modest" wording; Yucatán highlight bug | Strength wording aligned to prose; highlight fix; `select` max-width | Highlighted labels can overlap in the kidnapping view |
| E–G (static) | yes | Fig G said "only the state" | G re-rendered | **G**: the gradient "not in the registry at all, size unknown" has a drawn length (~5,000 on the axis), which a reader may read as an estimate. Consider a fixed-width hatched stub with no axis extent. |
| K filing authority (new) | yes | One table, two derivations (PNG + HTML) checked against each other | Rendered as HTML/CSS so labels stay at 11–13 px on a 320 px screen (the PNG shrank to ~4 px text); per-row `role="img"` with full values; values printed as text (non-colour encoding); hollow vs filled dots | Portal tick is grey-on-white 3.3:1 (non-text, passes 1.4.11) |
| H snapshots | yes | Totals view uses a non-zero baseline (acceptable for a line; not flagged on screen) | — | Add "axis does not start at zero" when metric ≠ share |

**Simplification candidates.** The "Explore the states" bar list duplicates the map's
detail panel and Fig C. It adds 32 tab stops and has no static fallback. Consider
dropping it, or folding its select into the map. Fig D's variable selector offers six
variables, though the article discusses only homicide (plus corruption and GDP in
§9). Kidnapping, femicide and resolution share are exploration without an editorial
point. Consider limiting it to the three the text discusses.

## WCAG 2.2 AA

| criterion | finding | status |
|---|---|---|
| 1.1.1 Non-text content | Every `<img>` has finding-level alt text; every chart SVG has `role="img"` + `aria-label`; each mark has an `aria-label` with its value | PASS |
| 1.3.1 Info and relationships | Logical heading order (h1 → h2 → h3 for charts); `<dl>` for the hero; source list linked both ways | PASS |
| 1.4.3 Contrast (text) | Computed: muted on ground 5.50 (light) / 5.77 (dark); chart labels 4.70–12.19; hero gloss **fixed** 2.67 → 5.05 | PASS after fix |
| 1.4.10 Reflow | No horizontal scroll at 320 px after the `select` fix | PASS after fix |
| 1.4.11 Non-text contrast | Adjacent stacked segments fixed with separators; Fig C grey bars 2.06:1 and map lightest bin 1.19:1, both carrying text equivalents | PARTIAL |
| 1.4.1 Use of colour | Map bins colour-only, but values are available via focus and tooltip; Fig D highlights labelled at ≥420 px only | PARTIAL |
| 2.1.1 Keyboard | All marks focusable; map Enter/Space selects a state and syncs the explorer (tested); focus shows the tooltip (tested via focus event; the pane lacked window focus) | PASS |
| 2.4.1 Bypass blocks | Skip link added (first focusable element) | PASS after fix |
| 2.4.3 Focus order / efficiency | ~340 tab stops: every bar is a stop | **OPEN**: use a roving tabindex per chart (one stop, arrow keys inside), or a `<details>` data table per chart and `tabindex="-1"` on marks |
| 2.4.7 / 2.4.11 Focus visible | Buttons and state rows had styles; SVG bars relied on the browser default | PASS after fix |
| 2.3.3 Motion | `prefers-reduced-motion` respected; no animation | PASS |
| 4.1.2 Name, role, value | Toggle buttons use `aria-pressed`, verified to stay consistent across 90 interactions | PASS |
| 3.1.1 Language | `lang="en"`; Spanish proper nouns not marked `lang="es"` | LOW |

Screen readers weren't tested with real assistive technology (VoiceOver/NVDA). That
testing is **BLOCKED** in this environment and listed in the checklist.

## Robustness

| scenario | before | after (tested) |
|---|---|---|
| JavaScript disabled | Empty chart frames with live-looking buttons; static image hidden in a collapsed `<details>` | `no-js` class hides the frames; fallback `<details>` rendered open; all six fallback images load |
| Corrupt or missing chart JSON | Whole script threw; every chart blank | Every interactive figure falls back to its static image |
| One chart throws | All later charts would fail too | Per-chart try/catch; only that chart falls back |
| Dark mode | Charts on white plates (intentional) | Unchanged; verified body #151817, plates #fff, ink #22201E on plates |

## Performance

Single file, 2.82 MB, of which 2.58 MB is ten base64 PNGs. Six of those are collapsed
fallbacks that most JS readers never open. Intrinsic `width`/`height` were added to
prevent layout shift. For production on a real host, serve the PNGs as separate files
(WebP, `loading="lazy"`). That cuts the initial HTML to ~250 KB. It's a deployment
change, deliberately not made here, because the freeze manifest pins the embedded
assets and the single-file artifact is the reviewed unit.
