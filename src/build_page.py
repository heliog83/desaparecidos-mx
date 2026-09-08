"""Build the self-contained HTML article from reports/article_draft.md.

Single source of truth is the markdown draft: this converts it, inlines every
figure in reports/figures/article/ as a base64 data URI, and writes one file that
depends on nothing external (required — the Artifact CSP blocks all remote hosts).

The draft's internal scaffolding (working titles, figure production notes) is
dropped; the standfirst and methods note are lifted into their own treatments.

Data comes from one immutable, dated publication freeze (PUBLICATION_FREEZE below),
never from the mutable data/processed/ working directory. That matters: re-running
src/fetch_flow.py refreshes data/processed/ with live figures, which would silently
change what the article is validated against. The freeze is the pin; refreshing the
article's numbers means cutting a new freeze with src/publication_freeze.py and
bumping PUBLICATION_FREEZE deliberately.

Output: reports/article.html  (~2 MB, mostly embedded PNGs)
Run:    python3 src/build_page.py
"""
from __future__ import annotations

import base64
import csv
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "reports" / "article_draft.md"
FIGDIR = ROOT / "reports" / "figures" / "article"
OUT = ROOT / "reports" / "article.html"
INTERACTIVE_CSS = ROOT / "src" / "article_interactive.css"
INTERACTIVE_JS = ROOT / "src" / "article_interactive.js"
# The pinned publication vintage. Every number in the article resolves through it.
PUBLICATION_FREEZE = "2026-08-15"
FREEZE = ROOT / "data" / "publication_freezes" / PUBLICATION_FREEZE
FREEZE_DERIVED = FREEZE / "derived"
FREEZE_MANIFEST = FREEZE / "manifest.json"

FLOW_YEAR = FREEZE_DERIVED / "flow_by_year.csv"
FLOW_TOTALS = FREEZE_DERIVED / "flow_totales.csv"
STATE_DATA = FREEZE_DERIVED / "state_opacity_enriched.csv"
STATE_RATES = FREEZE_DERIVED / "state_rates.csv"
SNAPSHOT_DATA = FREEZE_DERIVED / "confidencial_panel.csv"
COMPARE_DATA = FREEZE_DERIVED / "incidence_vs_homicide.csv"

# Cached SVG state outlines. The 4.8 MB source GeoJSON is gitignored, so the build
# reads this 64 KB derived cache and a clean checkout needs no external assets.
# Delete it (with mexico.json present) to regenerate from source.
MAP_PATHS_CACHE = FREEZE_DERIVED / "map_paths.json"
MEXICO_GEO = ROOT / "data" / "external" / "assets" / "mexico.json"

TITLE = "The Redacted Crisis"
SUBTITLE = "What Mexico's public registry leaves unseen"

# Field readout for the hero: exactly what the public registry returns for a
# confidential record. Structure only — no person, no invented identifiers.
# (registry field name, plain-language gloss, value, redacted). The raw names are
# the point — this is literally what the registry returns — but FECHA_DESAPARICION
# and ESTATUS_VICTIMA mean nothing to a reader who has never opened the file, so
# each carries a gloss underneath.
HERO_FIELDS = [
    ("ENTIDAD", "State", "JALISCO", False),
    ("FECHA_DESAPARICION", "Date of disappearance", "CONFIDENCIAL", True),
    ("SEXO", "Sex", "CONFIDENCIAL", True),
    ("EDAD", "Age", "CONFIDENCIAL", True),
    ("MUNICIPIO", "Municipality", "CONFIDENCIAL", True),
    ("ESTATUS_VICTIMA", "Case status", "CONFIDENCIAL", True),
]

# Text alternatives state each figure's finding rather than merely repeating its
# label. They are used for both static plates and interactive-chart fallbacks.
FIGURE_ALT_TEXT = {
    "A": "Stacked annual bars show Mexico's 2000 to 2025 disappearance cohorts by current registry status: found alive, found dead, or still missing.",
    "B": "Map of Mexico shows unresolved registry records per 100,000 residents, highest in Tamaulipas, Zacatecas, and Sinaloa.",
    "C": "Ranked bars show confidential shares of unresolved records by state, from about 67 percent in Jalisco to about 9 percent in Guerrero and Colima.",
    "D": "Scatter plot shows no positive relationship between a state's homicide-victim rate and the confidential share of its unresolved records.",
    "E": "Consent accounting for 73,388 records shows no consent information for 77.4 percent; among records with information, family refusals and agreements are similar in number.",
    "F": "Timeline shows Jalisco's state and federal disappearance registries diverging while confidentiality, omitted records, and later recounts are documented.",
    "G": "Paired bars compare Guerrero's statewide registry count with 623 cases documented by three Iguala collectives; the bars overlap by an unknown amount and are not additive.",
    "H": "Lines across ten 2025 snapshots show confidential registry records changing in state-level batches rather than smoothly over time.",
    "I": "Indexed annual series show recorded disappearances rising from 2019 to 2024 while homicide victims decline; 2025 is provisional.",
    "J": "Annual disappearance cohorts are split by current outcome beside homicide victims, showing 2019 to 2024 growth is mostly cases now recorded found alive rather than found dead.",
}


def figure_asset_names(md: str | None = None) -> tuple[str, ...]:
    """Return the PNG names referenced by the article's figure markers."""
    source = md if md is not None else DRAFT.read_text(encoding="utf-8")
    matches = re.findall(
        r"^\*\*\[FIG\s+([A-Z])\s*[—-]\s*`figures/article/([^`/]+\.png)`\]\*\*",
        source,
        flags=re.M,
    )
    letters = [letter for letter, _ in matches]
    if len(letters) != len(set(letters)):
        raise ValueError("article draft contains duplicate figure letters")
    missing_alt = sorted(set(letters) - set(FIGURE_ALT_TEXT))
    if missing_alt:
        raise ValueError(f"article figures lack alt text: {missing_alt}")
    return tuple(name for _, name in matches)


def img_uri(name: str) -> str:
    data = base64.b64encode((FIGDIR / name).read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def _number(value: str | None, *, integer: bool = False) -> float | int:
    if value is None or value == "":
        return 0 if integer else 0.0
    parsed = float(str(value).replace(",", "").replace("%", "").strip())
    return int(round(parsed)) if integer else parsed


def _state_label(name: str) -> str:
    label = name.strip().title()
    for token in (" De ", " Del ", " La ", " Las ", " Los "):
        label = label.replace(token, token.lower())
    return label


def _rdp(points: list[list[float]], epsilon: float) -> list[list[float]]:
    """Simplify one geographic ring with the Ramer-Douglas-Peucker algorithm."""
    if len(points) <= 3:
        return points
    x1, y1 = points[0]
    x2, y2 = points[-1]
    dx, dy = x2 - x1, y2 - y1
    denom = dx * dx + dy * dy
    best_i, best_d = 0, -1.0
    for i, (x, y) in enumerate(points[1:-1], 1):
        if denom == 0:
            dist = (x - x1) ** 2 + (y - y1) ** 2
        else:
            t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / denom))
            px, py = x1 + t * dx, y1 + t * dy
            dist = (x - px) ** 2 + (y - py) ** 2
        if dist > best_d:
            best_i, best_d = i, dist
    if best_d > epsilon * epsilon:
        left = _rdp(points[:best_i + 1], epsilon)
        right = _rdp(points[best_i:], epsilon)
        return left[:-1] + right
    return [points[0], points[-1]]


def map_paths() -> list[dict[str, str]]:
    """Compact, dependency-free SVG state paths, from cache or from the GeoJSON."""
    if MAP_PATHS_CACHE.exists():
        return json.loads(MAP_PATHS_CACHE.read_text(encoding="utf-8"))
    if not MEXICO_GEO.exists():
        raise SystemExit(
            f"FAIL: neither {MAP_PATHS_CACHE.relative_to(ROOT)} nor "
            f"{MEXICO_GEO.relative_to(ROOT)} is present — cannot draw the map"
        )
    geo = json.loads(MEXICO_GEO.read_text(encoding="utf-8"))
    all_points: list[list[float]] = []
    for feature in geo["features"]:
        coords = feature["geometry"]["coordinates"]
        polygons = coords if feature["geometry"]["type"] == "MultiPolygon" else [coords]
        for polygon in polygons:
            for ring in polygon:
                all_points.extend(ring)
    min_x = min(p[0] for p in all_points)
    max_x = max(p[0] for p in all_points)
    min_y = min(p[1] for p in all_points)
    max_y = max(p[1] for p in all_points)
    width, height, pad = 900.0, 520.0, 12.0
    scale = min((width - 2 * pad) / (max_x - min_x), (height - 2 * pad) / (max_y - min_y))

    paths = []
    for feature in geo["features"]:
        coords = feature["geometry"]["coordinates"]
        polygons = coords if feature["geometry"]["type"] == "MultiPolygon" else [coords]
        commands = []
        for polygon in polygons:
            for ring in polygon:
                simplified = _rdp(ring, 0.018)
                projected = [
                    (pad + (x - min_x) * scale, pad + (max_y - y) * scale)
                    for x, y in simplified
                ]
                if len(projected) < 3:
                    continue
                commands.append(
                    "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in projected) + "Z"
                )
        paths.append({
            "cve": feature["properties"]["CVE_ENT"].zfill(2),
            "d": "".join(commands),
        })
    # Persist so the next build — and every clean checkout — needs no GeoJSON.
    MAP_PATHS_CACHE.write_text(
        json.dumps(paths, ensure_ascii=False, indent=0, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return paths


def chart_data() -> dict:
    outcomes = []
    with FLOW_YEAR.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                year = int(row.get("") or "")
            except ValueError:
                continue
            if 2000 <= year <= 2025:
                outcomes.append({
                    "year": year,
                    "alive": _number(row.get("loc_con_vida"), integer=True),
                    "dead": _number(row.get("loc_sin_vida"), integer=True),
                    "missing": _number(row.get("desap_y_nollocal"), integer=True),
                })

    state_codes = {}
    with STATE_RATES.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            state_codes[(row.get("entidad") or "").strip().upper()] = row["cve_ent"].zfill(2)

    states = []
    with STATE_DATA.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = (row.get("entidad") or row.get("state_key") or "").strip()
            if not name:
                continue
            states.append({
                "cve": state_codes.get(name.upper(), ""),
                "name": name,
                "label": _state_label(name),
                "count": _number(row.get("total_records"), integer=True),
                "confidential_count": _number(row.get("confidential_records"), integer=True),
                "rate": round(float(row.get("tasa_100k") or 0), 1),
                "confidential_share": round(float(row.get("confidential_share") or 0), 6),
                # alive / dead / resolution for the new outcome views
                "alive": _number(row.get("loc_con_vida"), integer=True),
                "dead": _number(row.get("loc_sin_vida"), integer=True),
                "resolution_share": round(float(row.get("resolution_share") or 0), 6),
                # correlation variables for Fig D
                "homicide_rate": round(float(row.get("homicide_victims_2015_2025_per100k") or 0), 2),
                "pibe_per_capita": round(float(row.get("pibe_per_capita_2024_2018_mxn") or 0), 0),
                "corruption_per100k": round(float(row.get("corruption_prevalence_2025_per100k") or 0), 0),
                "kidnapping_per100k": round(float(row.get("kidnapping_victims_2015_2025_per100k") or 0), 4),
                "femicide_per100k": round(float(row.get("femicide_victims_2015_2025_per100k") or 0), 4),
            })

    snapshots = []
    with SNAPSHOT_DATA.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            snapshots.append({
                "snapshot": row["snapshot"],
                "name": _state_label(row["ENTIDAD"]),
                "total": _number(row["total"], integer=True),
                "conf": _number(row["conf"], integer=True),
            })
    # Fig J: registry outcomes beside homicide victims, 2015 onward. Two separate
    # populations that overlap by an unknown amount, never a sum — the chart says so.
    outcome_by_year = {row["year"]: row for row in outcomes}
    compare = []
    with COMPARE_DATA.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            year = int(row["year"])
            base = outcome_by_year.get(year)
            if not base:
                continue
            compare.append({
                "year": year,
                "alive": base["alive"],
                "dead": base["dead"],
                "missing": base["missing"],
                "homicides": _number(row["homicide_victims_annualised"], integer=True),
                "provisional": row["provisional"] == "1",
            })

    return {"outcomes": outcomes, "states": states, "snapshots": snapshots,
            "compare": compare, "map_paths": map_paths()}


def flow_totals() -> dict[str, int]:
    totals: dict[str, int] = {}
    with FLOW_TOTALS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row[""]] = _number(row["0"], integer=True)
    return totals


def validate_article_inputs(md: str, data: dict, totals: dict[str, int]) -> None:
    """Fail the build when prose, headline totals and embedded data drift apart."""
    alive = totals["TotalLocalizadosCV"]
    dead = totals["TotalLocalizadosSV"]
    missing = totals["TotalDesaparecidos"]
    total = totals["TotalGlobal"]
    if alive + dead + missing != total:
        raise ValueError("flow_totales.csv categories do not sum to TotalGlobal")

    years = [row["year"] for row in data["outcomes"]]
    if years != list(range(2000, 2026)):
        raise ValueError("Figure A must contain exactly one row for every year 2000–2025")

    outcome_sums = {
        key: sum(row[key] for row in data["outcomes"])
        for key in ("alive", "dead", "missing")
    }
    required = [total, alive, dead, missing, *outcome_sums.values()]
    absent = [f"{value:,}" for value in required if f"{value:,}" not in md]
    if absent:
        raise ValueError(f"article draft is stale; missing source-derived figures: {absent}")
    if "Two panels:" in md:
        raise ValueError("Figure A is now one interactive chart; remove the old two-panel caption")
    missing_figures = [name for name in figure_asset_names(md) if not (FIGDIR / name).is_file()]
    if missing_figures:
        raise ValueError(f"article figure assets are missing: {missing_figures}")

    latest = max(row["snapshot"] for row in data["snapshots"])
    latest_rows = [row for row in data["snapshots"] if row["snapshot"] == latest]
    latest_total = sum(row["total"] for row in latest_rows)
    latest_conf = sum(row["conf"] for row in latest_rows)
    latest_share = latest_conf / latest_total
    if latest != "2025-12-02" or round(latest_share * 100, 1) != 36.8:
        raise ValueError("the record-level confidentiality vintage or share changed; revise the standfirst")


def national_status(totals: dict[str, int]) -> str:
    alive = totals["TotalLocalizadosCV"]
    dead = totals["TotalLocalizadosSV"]
    missing = totals["TotalDesaparecidos"]
    total = totals["TotalGlobal"]
    # Percentages and segment widths are derived, never written by hand: a hard-coded
    # 61/6/33 silently stops matching the moment the capture changes.
    pct = {k: v / total * 100 for k, v in (("alive", alive), ("dead", dead), ("missing", missing))}
    # The found-dead band is ~6% wide, too narrow to hold a label. Rather than hide the
    # label (which left "6%" on the page with nothing saying what it counted), it is
    # called out above the bar, centred on the band.
    dead_centre = pct["alive"] + pct["dead"] / 2
    return f"""
    <section class="status-snapshot" aria-labelledby="status-title">
      <h2 id="status-title">One in three remains missing</h2>
      <p class="asof">Current RNPDNO registry status, 15 August 2026</p>
      <div class="status-callout-row">
        <div class="status-callout" style="left:{dead_centre:.2f}%">
          <span class="callout-text">{pct['dead']:.1f}% found dead &middot; {dead:,}</span>
          <span class="callout-stem"></span>
        </div>
      </div>
      <div class="status-track" role="img" aria-label="Of {total:,} registry records, {alive:,} are recorded found alive, {dead:,} found dead and {missing:,} still missing">
        <div class="status-segment status-alive" style="width:{pct['alive']:.2f}%" title="Found alive — {alive:,} records ({pct['alive']:.1f}%)"><strong>{pct['alive']:.0f}%</strong><span>found alive</span></div>
        <div class="status-segment status-dead" style="width:{pct['dead']:.2f}%" title="Found dead — {dead:,} records ({pct['dead']:.1f}%)"></div>
        <div class="status-segment status-missing" style="width:{pct['missing']:.2f}%" title="Still missing — {missing:,} records ({pct['missing']:.1f}%)"><strong>{pct['missing']:.0f}%</strong><span>still missing</span></div>
      </div>
      <div class="status-key">
        <span><b>{alive:,}</b> found alive</span>
        <span><b>{dead:,}</b> found dead</span>
        <span><b>{missing:,}</b> still missing</span>
        <span><b>{total:,}</b> total records</span>
      </div>
      <p class="status-note">These are people's current registry statuses. They do not show when somebody was located or why a record changed category.</p>
    </section>"""


def standfirst(totals: dict[str, int]) -> str:
    missing = totals["TotalDesaparecidos"]
    return (
        f"On 15 August 2026 Mexico's official registry counted <strong>{missing:,} people "
        "still missing</strong>. That live registry publishes only totals, so field-level "
        "detail comes from the last record-level snapshot, dated 2 December 2025. In it, "
        "63.2% of unresolved records carried the ordinary public fields \u2014 date, age, "
        "sex, municipality, case status. The other <strong>36.8% revealed only the "
        "state</strong>. This is the story of how publication decisions shape what the "
        "public can see."
    )


def interactive_figure(letter: str, caption: str, image_name: str) -> str | None:
    fallback = (
        f'<details class="static-fallback"><summary>Show static version</summary>'
        f'<img src="{img_uri(image_name)}" alt="{FIGURE_ALT_TEXT[letter]}" loading="lazy"></details>'
    )
    if letter == "A":
        return f"""<figure class="interactive-figure" data-chart="outcomes">
<div class="chart-shell">
  <h3 class="chart-heading">Recorded disappearances, by year and current outcome</h3>
  <p class="chart-subtitle">Grouped by the year a person disappeared, 2000–2025, and coloured by where their case stands <em>now</em>. Use “Still missing” for a zero-based comparison; hover or focus for exact values.</p>
  <div class="chart-controls" aria-label="Outcome chart display">
    <span class="chart-control-label">View</span>
    <button type="button" data-mode="absolute" aria-pressed="true">All outcomes</button>
    <button type="button" data-mode="missing" aria-pressed="false">Still missing</button>
    <button type="button" data-mode="alive" aria-pressed="false">Found alive</button>
    <button type="button" data-mode="dead" aria-pressed="false">Found dead</button>
    <button type="button" data-mode="share" aria-pressed="false">Share of cohort</button>
  </div>
  <div class="chart-canvas"><div class="chart-tooltip" role="tooltip"></div></div>
  <div class="chart-summary" aria-live="polite"></div>
</div>
{fallback}
<figcaption><span class="figlabel">Fig. A</span> {inline(caption)}</figcaption>
</figure>"""
    if letter == "J":
        return f"""<figure class="interactive-figure" data-chart="compare">
<div class="chart-shell">
  <h3 class="chart-heading">Did the missing deaths become disappearances?</h3>
  <p class="chart-subtitle">Each bar is one year of disappearance, split by where the case stands <em>now</em>. Homicide victims for the same year are a separate count, shown for comparison.</p>
  <p class="chart-note"><strong>These two counts are not added, and neither contains the other.</strong> The bars count people reported disappeared. The homicide line counts victims named in homicide investigation files. A person can be in both only if they were reported missing <em>and</em> later found dead <em>and</em> investigated as a homicide — at most the dark band, and the true overlap is not published.</p>
  <div class="chart-controls" aria-label="Comparison chart display">
    <span class="chart-control-label">View</span>
    <button type="button" data-mode="growth" aria-pressed="true">Where the growth went</button>
    <button type="button" data-mode="homicides" aria-pressed="false">Against homicides</button>
    <button type="button" data-mode="change" aria-pressed="false">Change 2019&#8211;2024</button>
  </div>
  <div class="chart-canvas"><div class="chart-tooltip" role="tooltip"></div></div>
  <div class="chart-summary" aria-live="polite"></div>
</div>
{fallback}
<figcaption><span class="figlabel">Fig. J</span> {inline(caption)}</figcaption>
</figure>"""
    if letter == "B":
        return f"""<figure class="interactive-figure" data-chart="map">
<div class="chart-shell">
  <h3 class="chart-heading">Where unresolved cases are highest per resident</h3>
  <p class="chart-subtitle">Point to, tap or focus a state for its count, population-adjusted rate and confidential share.</p>
  <div class="chart-controls" aria-label="Map display">
    <span class="chart-control-label">Colour by</span>
    <button type="button" data-mode="rate" aria-pressed="true">Rate</button>
    <button type="button" data-mode="count" aria-pressed="false">Count</button>
    <button type="button" data-mode="confidential" aria-pressed="false">Confidential share</button>
  </div>
  <div class="map-canvas"><div class="chart-tooltip" role="tooltip"></div></div>
  <div class="map-legend" aria-hidden="true"></div>
  <div class="map-detail" aria-live="polite"></div>
</div>
{fallback}
<figcaption><span class="figlabel">Fig. B</span> {inline(caption)}</figcaption>
</figure>
<figure class="interactive-figure" data-chart="states">
<div class="chart-shell">
  <h3 class="chart-heading">Explore the states</h3>
  <p class="chart-subtitle">The ranked view uses the December 2025 record-level snapshot throughout.</p>
  <div class="chart-controls">
    <label for="state-select">Highlight state</label><select id="state-select"></select>
    <button type="button" data-mode="rate" aria-pressed="true">Rate</button>
    <button type="button" data-mode="count" aria-pressed="false">Count</button>
    <button type="button" data-mode="confidential" aria-pressed="false">Confidential share</button>
  </div>
  <div class="state-bars" aria-live="polite"></div>
  <div class="state-detail" aria-live="polite"></div>
</div>
</figure>"""
    if letter == "C":
        return f"""<figure class="interactive-figure" data-chart="confidential">
<div class="chart-shell">
  <h3 class="chart-heading">Confidential share by state — violence does not explain it</h3>
  <p class="chart-subtitle">Share of each state&#8217;s unresolved records marked CONFIDENCIAL. National median shown as dashed line. Hover or focus for detail.</p>
  <div class="chart-controls" aria-label="Sort order">
    <button type="button" data-mode="confidential_share" aria-pressed="true">By redaction share</button>
    <button type="button" data-mode="rate" aria-pressed="false">By missing-persons rate</button>
  </div>
  <div class="chart-canvas"><div class="chart-tooltip" role="tooltip"></div></div>
  <div class="chart-summary" aria-live="polite"></div>
</div>
{fallback}
<figcaption><span class="figlabel">Fig. C</span> {inline(caption)}</figcaption>
</figure>"""
    if letter == "D":
        return f"""<figure class="interactive-figure" data-chart="scatter">
<div class="chart-shell">
  <h3 class="chart-heading">State violence does not explain confidentiality</h3>
  <p class="chart-subtitle">Confidential share vs selected state variable. Hover or focus a dot for detail. Pearson <em>r</em> is recomputed for the active variable.</p>
  <div class="chart-controls" aria-label="X-axis variable">
    <label for="scatter-var">Compare against</label>
    <select id="scatter-var">
      <option value="homicide_rate" selected>Homicide rate per 100k (2015&#8211;2025)</option>
      <option value="pibe_per_capita">GDP per capita (PIBE 2024, MXN 2018)</option>
      <option value="corruption_per100k">Corruption prevalence per 100k (ENCIG 2025)</option>
      <option value="kidnapping_per100k">Kidnapping rate per 100k (2015&#8211;2025)</option>
      <option value="femicide_per100k">Femicide rate per 100k (2015&#8211;2025)</option>
      <option value="resolution_share">Resolution share (% of records located)</option>
    </select>
  </div>
  <div class="chart-canvas"><div class="chart-tooltip" role="tooltip"></div></div>
  <div class="chart-summary" aria-live="polite"></div>
</div>
{fallback}
<figcaption><span class="figlabel">Fig. D</span> {inline(caption)}</figcaption>
</figure>"""
    if letter == "H":
        return f"""<figure class="interactive-figure" data-chart="snapshots">
<div class="chart-shell">
  <h3 class="chart-heading">How the public registry changes between snapshots</h3>
  <p class="chart-subtitle">Ten comparable snapshots, April–December 2025. A change is a registry movement, not a known real-world event.</p>
  <div class="chart-controls">
    <label for="snapshot-state">State</label><select id="snapshot-state"></select>
    <button type="button" data-mode="share" aria-pressed="true">Confidential share</button>
    <button type="button" data-mode="conf" aria-pressed="false">Confidential count</button>
    <button type="button" data-mode="total" aria-pressed="false">Total unresolved</button>
  </div>
  <div class="chart-canvas"><div class="chart-tooltip" role="tooltip"></div></div>
  <div class="chart-summary" aria-live="polite"></div>
</div>
{fallback}
<figcaption><span class="figlabel">Fig. H</span> {inline(caption)}</figcaption>
</figure>"""
    return None


def inline(t: str) -> str:
    """Escape, then re-apply the small markdown subset the draft actually uses."""
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    # [label](url) first, then any bare URL left over
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"(?<!\")(?<!>)\((https?://[^)\s]+)\)",
               r'(<a href="\1" target="_blank" rel="noopener">\1</a>)', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t, flags=re.S)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", t, flags=re.S)
    return t


# A citation marker is [1]..[9]. The negative lookahead keeps it from eating the
# "[label](url)" markdown links inline() has not rewritten yet, and figure markers
# are letters, not digits, so they are never matched.
CITATION_RE = re.compile(r"\[([1-9])\](?!\()")

# Editorial scaffolding that must never reach a reader. "Ethics line (keep):" once
# shipped in the published page; this turns that class of leak into a build failure.
EDITORIAL_MARKERS = ("(keep)", "(pick one)", "DRAFT —", "publish as expandable box")


def new_citation_state() -> dict:
    """Shared counter so body and methods citations get unique, stable ids."""
    return {"counts": {}, "first": {}}


def linkify_citations(fragment: str, state: dict) -> str:
    """Turn in-text [n] markers into links into the source list.

    Records the id of each source's first citation in ``state["first"]`` so the
    source entry can offer a link back to where the reader broke off.
    """
    def repl(m: re.Match) -> str:
        n = m.group(1)
        state["counts"][n] = state["counts"].get(n, 0) + 1
        ref_id = f"cite-{n}-{state['counts'][n]}"
        state["first"].setdefault(n, ref_id)
        return (
            f'<a class="fnref" id="{ref_id}" href="#source-{n}">'
            f'<span class="sr-only">Source </span>[{n}]</a>'
        )

    return CITATION_RE.sub(repl, fragment)


def parse_body(md: str, state: dict | None = None) -> str:
    """Convert the article body (§1..§9) into HTML."""
    state = new_citation_state() if state is None else state
    body = md.split("## 1.", 1)[1]
    body = "## 1." + body.split("## Methods note", 1)[0]

    out: list[str] = []
    # split into blocks on blank lines, keeping order
    for block in re.split(r"\n\s*\n", body.strip()):
        b = block.strip()
        if not b:
            continue

        m = re.match(r"^#{2,3}\s+(\d+b?)\.\s+(.+)$", b, flags=re.S)
        if m:
            num, title = m.group(1), " ".join(m.group(2).split())
            out.append(
                f'<section class="sec">\n'
                f'<p class="eyebrow"><span class="idx">{num}</span></p>\n'
                f"<h2>{inline(title)}</h2>"
            )
            continue

        # A figure marker and its caption share one block (no blank line between them).
        m = re.match(r"^\*\*\[FIG\s+([A-Z])\s*[—-]\s*`([^`]+)`\]\*\*\s*(.*)$", b, flags=re.S)
        if b.lstrip().startswith("**[FIG") and not m:
            # Silent fallthrough would render the marker as body prose and drop the
            # figure. A too-narrow letter class did exactly that, twice.
            raise SystemExit(f"FAIL: malformed figure marker: {b.splitlines()[0]!r}")
        if m:
            letter, path, rest = m.group(1), m.group(2), m.group(3).strip()
            cap = ""
            if rest.startswith("*Caption:"):
                cap = " ".join(rest.strip().strip("*").replace("Caption:", "", 1).split())
            enhanced = interactive_figure(letter, cap, Path(path).name)
            if enhanced:
                out.append(enhanced)
            else:
                out.append(
                    f'<figure class="plate">\n'
                    f'<img src="{img_uri(Path(path).name)}" alt="{FIGURE_ALT_TEXT[letter]}" loading="lazy">\n'
                    f'<figcaption><span class="figlabel">Fig. {letter}</span> '
                    f"{inline(cap)}</figcaption>\n</figure>"
                )
            continue

        # bullet list: items start with "- " and may wrap over several lines
        if b.startswith("- "):
            items, cur = [], []
            for line in b.split("\n"):
                if line.lstrip().startswith("- "):
                    if cur:
                        items.append(" ".join(cur))
                    cur = [line.lstrip()[2:].strip()]
                else:
                    cur.append(line.strip())
            if cur:
                items.append(" ".join(cur))
            lis = "\n".join(f"<li>{inline(' '.join(i.split()))}</li>" for i in items)
            out.append(f"<ul>\n{lis}\n</ul>")
            continue

        out.append(f"<p>{inline(' '.join(b.split()))}</p>")

    hchunks = "\n".join(out)
    # close each section before the next opens, and at the end
    hchunks = hchunks.replace('<section class="sec">', "</section>\n<section class=\"sec\">")
    hchunks = hchunks.replace("</section>\n<section class=\"sec\">", '<section class="sec">', 1)
    return linkify_citations(hchunks + "\n</section>", state)


def parse_methods(md: str, state: dict | None = None) -> str:
    state = new_citation_state() if state is None else state
    chunk = md.split("## Methods note", 1)[1]
    chunk = chunk.split("---", 1)[0]
    chunk = chunk.split("\n", 1)[1]  # drop the rest of the heading line
    paras = [" ".join(p.split()) for p in re.split(r"\n\s*\n", chunk.strip()) if p.strip()]

    rendered: list[str] = []
    for para in paras:
        block = f"<p>{inline(para)}</p>"
        m = re.match(r"^<p><strong>\[([1-9])\]", block)
        if not m:
            rendered.append(linkify_citations(block, state))
            continue

        # A source entry. Its own leading [n] is the label, not a citation of
        # itself, so it is held back while the rest of the entry is linked.
        n = m.group(1)
        head, rest = block.split(f"[{n}]", 1)
        rest = linkify_citations(rest, state)
        target = state["first"].get(n)
        back = (
            f' <a class="fnback" href="#{target}" '
            f'aria-label="Back to the first citation of source {n}">&#8617;</a>'
            if target else ""
        )
        opened = head.replace("<p>", '<p id="source-%s">' % n, 1)
        block = f"{opened}[{n}]{rest}"
        rendered.append(block[: -len("</p>")] + back + "</p>")

    return "\n".join(rendered)


def hero_record() -> str:
    rows = []
    for field, gloss, value, redacted in HERO_FIELDS:
        cls = "val redacted" if redacted else "val"
        rows.append(
            f'<div class="frow">'
            f'<dt><span class="fname">{field}</span>'
            f'<span class="fgloss">{gloss}</span></dt>'
            f'<dd class="{cls}">{value}</dd>'
            f'</div>'
        )
    return "\n".join(rows)


def _assert_ascii(path: Path) -> str:
    """Refuse to inline a non-ASCII asset into the page.

    ascii_safe() escapes the finished page to numeric entities so encoding cannot
    break it. That is right for markup, but entities are NOT decoded inside <script>
    or <style>: a literal accented character in the JS renders on the chart as
    "Calder&#243;n". Assets must therefore be ASCII at source, using \\u escapes for
    accented strings. This turns a silent rendering bug into a build failure.
    """
    text = path.read_text(encoding="utf-8")
    bad = sorted({c for c in text if ord(c) > 127})
    if bad:
        lines = [f"{i}: {ln.strip()[:80]}" for i, ln in enumerate(text.splitlines(), 1)
                 if any(ord(c) > 127 for c in ln)]
        raise ValueError(
            f"{path.name} contains non-ASCII {bad}; entities do not decode inside "
            f"<script>/<style>. Use \\uXXXX escapes instead.\n  " + "\n  ".join(lines)
        )
    return text


def ascii_safe(s: str) -> str:
    """Escape every non-ASCII char to a numeric entity.

    The page carries em-dashes and Spanish names (Michoacán, Teuchitlán, María),
    and is viewed both from a local static server and from the Artifact host. Rather
    than depend on either declaring UTF-8, make the bytes ASCII so the encoding
    cannot matter.
    """
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)


def build() -> str:
    md = DRAFT.read_text(encoding="utf-8")
    data = chart_data()
    totals = flow_totals()
    validate_article_inputs(md, data, totals)
    citations = new_citation_state()
    body_html = parse_body(md, citations)
    methods_html = parse_methods(md, citations)
    for marker in EDITORIAL_MARKERS:
        for where, frag in (("body", body_html), ("methods", methods_html)):
            if marker in frag:
                raise SystemExit(
                    f"FAIL: editorial marker {marker!r} would publish in the {where}"
                )
    cited = set(citations["first"])
    defined = set(re.findall(r'<p id="source-([1-9])">', methods_html))
    if cited - defined:
        raise SystemExit(f"FAIL: cited but undefined sources: {sorted(cited - defined)}")
    if defined - cited:
        raise SystemExit(f"FAIL: sources defined but never cited: {sorted(defined - cited)}")
    data_json = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    data_json = data_json.replace("<", "\\u003c").replace("&", "\\u0026")
    return ascii_safe(TEMPLATE.format(
        title=TITLE,
        subtitle=SUBTITLE,
        hero=hero_record(),
        standfirst=standfirst(totals),
        status=national_status(totals),
        body=body_html,
        methods=methods_html,
        interactive_css=_assert_ascii(INTERACTIVE_CSS),
        chart_data=data_json,
        interactive_js=_assert_ascii(INTERACTIVE_JS),
    ))


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  /* ---- tokens: light is the base, dark redefines tokens only ---- */
  :root {{
    /* --muted is darker than it looks like it needs to be: captions and the
       methods note run at 13.5-14px, so they need >=4.5:1 on --ground, not 3:1. */
    --ground:#E7E9E6; --plate:#FFFFFF; --ink:#22201E; --muted:#585D59;
    --redact:#7A1F1F; --collective:#3C6E91; --rule:#CBCFC9; --plate-edge:#D5D8D2;
    --serif:'Iowan Old Style',Palatino,'Palatino Linotype',Charter,Georgia,serif;
    --mono:ui-monospace,'SF Mono',Menlo,Consolas,monospace;
    --sans:-apple-system,'Helvetica Neue',Helvetica,Arial,sans-serif;
  }}
  @media (prefers-color-scheme:dark) {{
    :root:not([data-theme="light"]) {{
      --ground:#151817; --ink:#E3E6E2; --muted:#8E948F;
      --redact:#C4706A; --collective:#84ABC6; --rule:#2E3331; --plate-edge:#343937;
    }}
  }}
  :root[data-theme="dark"] {{
    --ground:#151817; --ink:#E3E6E2; --muted:#8E948F;
    --redact:#C4706A; --collective:#84ABC6; --rule:#2E3331; --plate-edge:#343937;
  }}

  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--ground); color:var(--ink);
    font-family:var(--serif); font-size:19px; line-height:1.62;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap {{ max-width:1120px; margin:0 auto; padding:0 28px 96px; }}
  .col {{ max-width:34em; }}

  /* ---- masthead ---- */
  header.mast {{ padding:64px 0 8px; }}
  .kicker {{
    font-family:var(--mono); font-size:11px; letter-spacing:.16em; text-transform:uppercase;
    color:var(--muted); margin:0 0 22px; display:flex; flex-wrap:wrap; gap:10px 16px; align-items:center;
  }}
  .chip {{ border:1px solid var(--rule); padding:3px 8px; }}
  a {{ color:inherit; text-decoration:underline; text-underline-offset:2px;
       text-decoration-color:var(--muted); }}
  a:hover {{ text-decoration-color:var(--redact); }}
  a:focus-visible {{ outline:2px solid var(--redact); outline-offset:2px; }}
  h1 {{
    font-size:clamp(2.4rem,6vw,4.1rem); line-height:1.03; margin:0 0 18px;
    font-weight:600; letter-spacing:-.015em; text-wrap:balance; max-width:15ch;
  }}
  .subtitle {{
    font-size:clamp(1.15rem,2.4vw,1.5rem); color:var(--muted); margin:0 0 40px;
    max-width:26ch; line-height:1.3; text-wrap:balance; font-weight:400;
  }}
  .standfirst {{ font-size:1.16rem; line-height:1.6; max-width:33em; margin:0 0 44px; }}
  .standfirst strong {{ font-weight:600; }}

  /* ---- hero: one registry record as the public sees it ---- */
  .record {{
    background:var(--plate); border:1px solid var(--plate-edge);
    padding:26px 28px 24px; max-width:36em; margin:0 0 14px; color:var(--ink);
  }}
  .record .rlabel {{
    font-family:var(--mono); font-size:10.5px; letter-spacing:.15em; text-transform:uppercase;
    color:#6B706C; margin:0 0 18px; padding-bottom:12px; border-bottom:1px solid #E2E5E0;
  }}
  dl.fields {{ margin:0; display:flex; flex-direction:column; gap:11px; }}
  .frow {{ display:grid; grid-template-columns:minmax(0,15em) 1fr; gap:14px; align-items:baseline; }}
  dl.fields dt {{ display:flex; flex-direction:column; gap:2px; }}
  dl.fields .fname {{
    font-family:var(--mono); font-size:11.5px; letter-spacing:.06em; color:#6B706C;
    text-transform:uppercase; overflow-wrap:anywhere;
  }}
  dl.fields .fgloss {{
    font-family:var(--sans); font-size:12px; color:#9AA09A; letter-spacing:0;
    text-transform:none;
  }}
  dl.fields dd {{ margin:0; font-family:var(--mono); font-size:13px; letter-spacing:.04em; color:var(--ink); }}
  dl.fields dd.redacted {{ color:#7A1F1F; }}
  .record-note {{
    font-family:var(--sans); font-size:13.5px; color:var(--muted); max-width:36em;
    margin:0 0 60px; line-height:1.5;
  }}

  /* ---- sections ---- */
  .sec {{ padding-top:52px; }}
  .eyebrow {{ margin:0 0 14px; display:flex; align-items:center; gap:12px; }}
  .idx {{
    font-family:var(--mono); font-size:11px; letter-spacing:.18em; color:var(--muted);
    border:1px solid var(--rule); padding:4px 9px; text-transform:uppercase;
  }}
  .eyebrow::after {{ content:""; flex:1; height:1px; background:var(--rule); }}
  h2 {{
    font-size:clamp(1.55rem,3.2vw,2.15rem); line-height:1.15; margin:0 0 26px;
    font-weight:600; letter-spacing:-.01em; max-width:20ch; text-wrap:balance;
  }}
  .sec p {{ max-width:34em; margin:0 0 21px; }}
  .sec ul {{
    max-width:34em; margin:0 0 24px; padding:0; list-style:none;
    display:flex; flex-direction:column; gap:15px;
  }}
  .sec li {{ position:relative; padding-left:22px; }}
  .sec li::before {{
    content:""; position:absolute; left:0; top:.62em;
    width:9px; height:1.5px; background:var(--redact);
  }}
  em {{ font-style:italic; }}
  strong {{ font-weight:600; }}
  code {{ font-family:var(--mono); font-size:.86em; letter-spacing:.02em; }}

  /* ---- figure plates ---- */
  figure.plate {{ margin:38px 0 40px; }}
  figure.plate img {{
    display:block; width:100%; height:auto; background:var(--plate);
    border:1px solid var(--plate-edge); padding:14px;
  }}
  figcaption {{
    font-family:var(--sans); font-size:13.5px; line-height:1.5; color:var(--muted);
    margin-top:13px; max-width:44em;
  }}
  .figlabel {{
    font-family:var(--mono); font-size:11px; letter-spacing:.13em; text-transform:uppercase;
    color:var(--redact); margin-right:9px;
  }}

  /* ---- citations ---- */
  /* The marker is a jump target as well as a label, so it gets a real hit area
     without opening a gap in the line it sits in. */
  a.fnref {{
    font-family:var(--sans); font-size:.72em; font-weight:600; vertical-align:.42em;
    text-decoration:none; color:var(--redact); padding:0 .12em; white-space:nowrap;
  }}
  a.fnref:hover {{ text-decoration:underline; }}
  a.fnback {{ text-decoration:none; color:var(--redact); font-size:15px; padding-left:.2em; }}
  a.fnback:hover {{ text-decoration:underline; }}
  :target {{ scroll-margin-top:24px; }}
  .methods p:target {{
    background:var(--plate); outline:2px solid var(--redact); outline-offset:6px;
  }}
  .sr-only {{
    position:absolute; width:1px; height:1px; padding:0; margin:-1px;
    overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0;
  }}
  @media (prefers-reduced-motion:no-preference) {{ html {{ scroll-behavior:smooth; }} }}

  /* ---- methods ---- */
  .methods {{ margin-top:76px; border-top:2px solid var(--ink); padding-top:26px; }}
  .methods h2 {{ font-size:1.2rem; margin-bottom:18px; max-width:none; }}
  .methods p {{
    font-family:var(--sans); font-size:14px; line-height:1.62; color:var(--muted);
    max-width:44em; margin:0 0 15px;
  }}
  .methods strong {{ color:var(--ink); font-weight:600; }}
  footer {{
    margin-top:56px; padding-top:22px; border-top:1px solid var(--rule);
    font-family:var(--mono); font-size:11px; letter-spacing:.1em; text-transform:uppercase;
    color:var(--muted); display:flex; flex-wrap:wrap; gap:8px 20px;
  }}

  @media (max-width:640px) {{
    body {{ font-size:17.5px; }}
    .wrap {{ padding:0 20px 72px; }}
    header.mast {{ padding-top:40px; }}
    .frow {{ grid-template-columns:1fr; gap:3px; }}
    figure.plate img {{ padding:9px; }}
  }}
  @media (prefers-reduced-motion:reduce) {{ * {{ animation:none !important; transition:none !important; }} }}
{interactive_css}
</style>
</head>
<body>

<div class="wrap">
  <header class="mast">
    <p class="kicker">
      <span>Data investigation</span>
      <span class="chip">RNPDNO</span>
      <span class="chip">Mexico</span>
      <span class="theme-toggle" aria-label="Theme selection">
        <button type="button" data-theme-set="light" aria-pressed="false">Light</button>
        <button type="button" data-theme-set="dark" aria-pressed="false">Dark</button>
        <button type="button" data-theme-set="auto" aria-pressed="true">Auto</button>
      </span>
    </p>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <p class="standfirst">{standfirst}</p>

{status}

    <div class="record">
      <p class="rlabel">What a confidential record contains</p>
      <dl class="fields">
{hero}
      </dl>
    </div>
    <p class="record-note">The field structure above is illustrative, not one person's
      file. It represents the 36.8% of unresolved records marked confidential in the
      2 December 2025 record-level snapshot. One public field survives.</p>
  </header>

  <main>
{body}

    <section class="methods">
      <h2>Methods and limits</h2>
{methods}
    </section>
  </main>

  <footer>
    <span>Stage 1 of 2</span>
    <span>Figures reproducible from source</span>
    <span>Data consulted 2026-08-15</span>
  </footer>
</div>
<script type="application/json" id="article-chart-data">{chart_data}</script>
<script>{interactive_js}</script>
</body>
</html>
"""


def main() -> None:
    out = build()
    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(out.encode()) / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
