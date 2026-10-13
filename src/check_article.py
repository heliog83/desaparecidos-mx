"""Verify that the generated article still matches its pinned source data.

Two independent gates:

1. Freeze integrity — every publication input present on disk hashes to the value
   recorded in the freeze manifest, and every input the build actually reads is
   covered by that manifest. This is what makes the vintage auditable rather than
   merely asserted.
2. Article fidelity — the embedded chart dataset and the headline numbers in the
   HTML match what the build derives from those same inputs.

Run after ``python3 src/build_page.py`` and before publishing.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from build_page import (
    DRAFT,
    FIGDIR,
    FREEZE,
    FREEZE_MANIFEST,
    OUT,
    PUBLICATION_FREEZE,
    chart_data,
    figure_asset_names,
    flow_totals,
    map_paths,
)

# Everything build_page.py reads to produce the article's numbers and geometry.
BUILD_INPUTS = (
    "derived/flow_by_year.csv",
    "derived/flow_totales.csv",
    "derived/state_opacity_enriched.csv",
    "derived/state_rates.csv",
    "derived/confidencial_panel.csv",
    "derived/incidence_vs_homicide.csv",
    "derived/map_paths.json",
    "derived/confidential_by_filing_authority.csv",
)

ARTICLE_ASSET_HASHES = "article_asset_hashes_sha256"


def verify_freeze() -> tuple[int, int]:
    """Hash-check the freeze. Returns (verified, not-present-locally) counts."""
    if not FREEZE_MANIFEST.exists():
        raise SystemExit(f"FAIL: no manifest for freeze {PUBLICATION_FREEZE}")
    hashes = json.loads(FREEZE_MANIFEST.read_text(encoding="utf-8"))
    hashes = hashes["source_hashes_sha256"]

    # An input the build reads but nobody hashed is an unaudited number.
    unhashed = [rel for rel in BUILD_INPUTS if rel not in hashes]
    if unhashed:
        raise SystemExit(
            f"FAIL: build inputs missing from the freeze manifest: {unhashed}"
        )

    missing = [rel for rel in BUILD_INPUTS if not (FREEZE / rel).exists()]
    if missing:
        raise SystemExit(f"FAIL: build inputs absent from the freeze: {missing}")

    verified, unchecked = 0, 0
    for rel, expected in sorted(hashes.items()):
        path = FREEZE / rel
        if not path.exists():
            # Raw sources (microdata, API JSON, the oficio PDF) stay gitignored;
            # they are only checkable where they were captured.
            unchecked += 1
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(
                f"FAIL: {rel} does not match the freeze manifest\n"
                f"  expected {expected}\n  actual   {actual}"
            )
        verified += 1
    return verified, unchecked


def verify_article_assets() -> int:
    """Hash-check every PNG that the article build embeds from reports/figures."""
    manifest = json.loads(FREEZE_MANIFEST.read_text(encoding="utf-8"))
    hashes = manifest.get(ARTICLE_ASSET_HASHES, {})
    assets = [f"reports/figures/article/{name}" for name in figure_asset_names(
        DRAFT.read_text(encoding="utf-8")
    )]
    unhashed = [rel for rel in assets if rel not in hashes]
    if unhashed:
        raise SystemExit(f"FAIL: article assets missing from freeze manifest: {unhashed}")

    for rel in assets:
        path = FIGDIR / Path(rel).name
        if not path.exists():
            raise SystemExit(f"FAIL: article asset is absent: {rel}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != hashes[rel]:
            raise SystemExit(
                f"FAIL: {rel} does not match the freeze manifest\n"
                f"  expected {hashes[rel]}\n  actual   {actual}"
            )
    return len(assets)


def main() -> None:
    verified, unchecked = verify_freeze()
    article_assets = verify_article_assets()

    page = OUT.read_text(encoding="utf-8")
    match = re.search(
        r'<script type="application/json" id="article-chart-data">(.*?)</script>',
        page,
        flags=re.S,
    )
    if not match:
        raise SystemExit("FAIL: article.html has no embedded chart dataset")

    embedded = json.loads(match.group(1))
    expected = chart_data()
    if embedded != expected:
        raise SystemExit("FAIL: embedded chart data do not match the pinned freeze")

    totals = flow_totals()
    keys = (
        "TotalGlobal",
        "TotalLocalizadosCV",
        "TotalLocalizadosSV",
        "TotalDesaparecidos",
    )
    absent = [f"{totals[key]:,}" for key in keys if f"{totals[key]:,}" not in page]
    if absent:
        raise SystemExit(f"FAIL: source-derived headline values absent from HTML: {absent}")

    outcome_sums = {
        key: sum(row[key] for row in expected["outcomes"])
        for key in ("alive", "dead", "missing")
    }
    absent_outcomes = [
        f"{value:,}" for value in outcome_sums.values() if f"{value:,}" not in page
    ]
    if absent_outcomes:
        raise SystemExit(
            f"FAIL: Figure A summary values absent from HTML: {absent_outcomes}"
        )

    if "Two panels: absolute counts and shares" in page:
        raise SystemExit("FAIL: obsolete Figure A two-panel caption remains")
    if "2 December 2025" not in page or "36.8%" not in page:
        raise SystemExit("FAIL: confidentiality figure lacks its record-level vintage")

    if len(map_paths()) != 32:
        raise SystemExit("FAIL: map geometry does not cover all 32 states")

    print(
        f"PASS: freeze {PUBLICATION_FREEZE} intact — {verified} files hash-verified, "
        f"{unchecked} gitignored raw sources not checkable here; "
        f"{article_assets} embedded article figures hash-verified."
    )
    print(
        "PASS: article HTML matches source data — "
        f"{totals['TotalGlobal']:,} total, "
        f"{totals['TotalDesaparecidos']:,} still missing; "
        f"Figure A {sum(outcome_sums.values()):,} records."
    )


if __name__ == "__main__":
    main()
