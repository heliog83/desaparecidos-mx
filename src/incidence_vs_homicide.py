"""Fig 26 / article fig I: recorded disappearances against homicide victims.

Answers a question the article previously left open. Section 1 said the registry
"has grown more than tenfold in eighteen years" without saying whether that growth
tracks worsening violence or a widening capacity to record. Plotted against
homicides, the two explanations separate cleanly at 2019:

* 2015-2018 the series rise together — consistent with the violence account.
* 2019-2024 homicide victims fall 13.4% while recorded disappearances rise 43.4%.

So lethal violence does not account for the recent growth. This chart states that
divergence and nothing more: it is two official series side by side, not a causal
claim, and a fall in homicides is not evidence that disappearances are being
mis-recorded. The reporting-channel shift documented in docs/methodology.md is the
complementary evidence.

Data
----
Disappearances: RNPDNO aggregate flow, by year OF DISAPPEARANCE, from the pinned
publication freeze. Homicides: SESNSP victim time series (2015-01 onward, which is
why the chart starts at 2015 rather than 2000).

2025 is provisional in BOTH series and is drawn detached: the SESNSP file ends in
October (annualised here), and recent disappearance cohorts are still filling in.
The headline comparison uses complete years only.

Run:
    python src/incidence_vs_homicide.py              # uses the committed series
    python src/incidence_vs_homicide.py --refresh    # rebuild from the raw SESNSP file
"""
from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt

import article_style as st

ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_FREEZE = "2026-08-15"
FREEZE_DERIVED = ROOT / "data" / "publication_freezes" / PUBLICATION_FREEZE / "derived"
SERIES = FREEZE_DERIVED / "incidence_vs_homicide.csv"
FLOW_YEAR = FREEZE_DERIVED / "flow_by_year.csv"
SESNSP = ROOT / "data" / "external" / "assets" / "timeseries_victimas.csv"

FIRST, LAST_COMPLETE, PROVISIONAL = 2015, 2024, 2025


def refresh_series() -> None:
    """Rebuild the two-column annual series from the raw sources."""
    import pandas as pd

    if not SESNSP.exists():
        raise SystemExit(f"FAIL: {SESNSP.relative_to(ROOT)} is missing (gitignored raw source)")
    v = pd.read_csv(SESNSP, low_memory=False)
    v["yr"] = pd.to_datetime(v["PERIODO"]).dt.year
    hom = v[v["DELITO"].str.contains("Homicidio doloso", case=False, na=False)]
    total = hom.groupby("yr")["TOTAL"].sum()
    months = hom.groupby("yr")["PERIODO"].nunique()

    flow = pd.read_csv(FLOW_YEAR, index_col=0)
    flow.index = pd.to_numeric(flow.index, errors="coerce")
    flow = flow[flow.index.notna()]
    flow.index = flow.index.astype(int)

    rows = []
    for year in range(FIRST, PROVISIONAL + 1):
        rows.append({
            "year": year,
            "homicide_victims": int(total.get(year, 0)),
            "months_reported": int(months.get(year, 0)),
            # Annualise only the incomplete year, and record that it was done.
            "homicide_victims_annualised": round(
                total.get(year, 0) / months.get(year, 12) * 12
            ),
            "disappearances_recorded": int(flow.loc[year, "todos"]),
            "provisional": int(months.get(year, 12) < 12 or year == PROVISIONAL),
        })
    SERIES.parent.mkdir(parents=True, exist_ok=True)
    with SERIES.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {SERIES.relative_to(ROOT)} ({len(rows)} years)")


def load_series() -> list[dict]:
    if not SERIES.exists():
        raise SystemExit(
            f"FAIL: {SERIES.relative_to(ROOT)} is missing. Run with --refresh to "
            f"rebuild it from the raw SESNSP file."
        )
    with SERIES.open(newline="", encoding="utf-8") as f:
        return [
            {k: (int(v) if k != "year" or True else v) for k, v in row.items()}
            for row in csv.DictReader(f)
        ]


def build(rows: list[dict]) -> None:
    st.apply()
    years = [r["year"] for r in rows]
    dis = [r["disappearances_recorded"] for r in rows]
    hom = [r["homicide_victims_annualised"] for r in rows]
    base_d, base_h = dis[0], hom[0]
    dis_i = [v / base_d * 100 for v in dis]
    hom_i = [v / base_h * 100 for v in hom]

    # Complete years carry the argument; the provisional year is drawn detached so
    # it cannot be read as part of the measured trend.
    n = years.index(LAST_COMPLETE) + 1
    fig, ax = plt.subplots(figsize=(11, 5.8))

    ax.axvspan(2019, LAST_COMPLETE, color=st.MUTED, alpha=0.10, zorder=0)
    ax.text(2019.1, 272, "Homicides falling,\nrecorded disappearances rising",
            fontsize=9.5, color=st.INK, va="top")

    ax.plot(years[:n], dis_i[:n], color=st.RED, lw=2.6, zorder=3)
    ax.plot(years[:n], hom_i[:n], color=st.INK, lw=2.6, zorder=3)
    # Provisional tail: dotted, hollow marker.
    ax.plot(years[n - 1:], dis_i[n - 1:], color=st.RED, lw=1.6, ls=":", zorder=3)
    ax.plot(years[n - 1:], hom_i[n - 1:], color=st.INK, lw=1.6, ls=":", zorder=3)
    for series, colour in ((dis_i, st.RED), (hom_i, st.INK)):
        ax.plot([PROVISIONAL], [series[-1]], marker="o", ms=6, mfc=st.PAPER,
                mec=colour, mew=1.6, zorder=4)

    ax.annotate(f"Recorded disappearances\n{dis[n-1]:,} in {LAST_COMPLETE}",
                xy=(LAST_COMPLETE, dis_i[n - 1]), xytext=(-6, 16),
                textcoords="offset points", ha="right", fontsize=10,
                color=st.RED, weight="bold")
    ax.annotate(f"Homicide victims\n{hom[n-1]:,} in {LAST_COMPLETE}",
                xy=(LAST_COMPLETE, hom_i[n - 1]), xytext=(-6, -30),
                textcoords="offset points", ha="right", fontsize=10,
                color=st.INK, weight="bold")
    ax.text(PROVISIONAL, dis_i[-1] + 9, "2025\nprovisional",
            ha="center", va="bottom", fontsize=8.5, color=st.MUTED)

    ax.axhline(100, color=st.MUTED, lw=0.8, ls="--", zorder=1)

    ax.set_xlim(FIRST - 0.9, PROVISIONAL + 0.7)
    ax.set_ylim(70, 292)
    ax.set_xticks(range(FIRST, PROVISIONAL + 1))
    ax.set_ylabel(f"Indexed to {FIRST} = 100")
    ax.grid(axis="y", color=st.MUTED, alpha=0.22, lw=0.7)
    ax.set_axisbelow(True)

    st.title(
        ax,
        "Violence stopped explaining the registry's growth in 2019",
        "Recorded disappearances and homicide victims, both indexed to 2015. "
        "Shaded years: the two official series move in opposite directions.",
    )
    st.caption(fig, textwrap.fill(
        "Disappearances by year of disappearance (RNPDNO aggregate flow, publication freeze "
        f"{PUBLICATION_FREEZE}); homicide victims from SESNSP (data begin 2015-01, which sets "
        "the start year). 2025 is provisional in both series \u2014 SESNSP runs to October and "
        "is annualised here, and recent disappearance cohorts are still filling in \u2014 so it "
        "is drawn detached and excluded from the comparison. Two series side by side, not a "
        "causal claim: falling homicides are not evidence about how disappearances are recorded.",
        width=118))

    fig.tight_layout(rect=(0, 0.10, 1, 1))

    numbered = ROOT / "reports" / "figures" / "26_incidence_vs_homicide.png"
    fig.savefig(numbered, dpi=200, bbox_inches="tight")
    print(f"wrote {numbered.relative_to(ROOT)}")
    st.save(fig, "I_incidence_vs_homicide.png")

    d0, d1 = dis[years.index(2019)], dis[n - 1]
    h0, h1 = hom[years.index(2019)], hom[n - 1]
    print(f"  2019->{LAST_COMPLETE} homicides      {h0:,} -> {h1:,} ({(h1/h0-1)*100:+.1f}%)")
    print(f"  2019->{LAST_COMPLETE} disappearances {d0:,} -> {d1:,} ({(d1/d0-1)*100:+.1f}%)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true",
                        help="rebuild the annual series from the raw SESNSP file")
    args = parser.parse_args()
    if args.refresh:
        refresh_series()
    build(load_series())


if __name__ == "__main__":
    main()
