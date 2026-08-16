"""Verify that the generated article still matches its source CSVs.

Run after ``python src/build_page.py`` and before publishing the HTML artifact.
"""
from __future__ import annotations

import json
import re

from build_page import OUT, chart_data, flow_totals


def main() -> None:
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
        raise SystemExit("FAIL: embedded chart data do not match the processed CSVs")

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

    print(
        "PASS: article HTML matches source data — "
        f"{totals['TotalGlobal']:,} total, "
        f"{totals['TotalDesaparecidos']:,} still missing; "
        f"Figure A {sum(outcome_sums.values()):,} records."
    )


if __name__ == "__main__":
    main()
