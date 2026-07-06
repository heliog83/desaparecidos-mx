"""
Consolidated flow figure: every year's disappearances decomposed into the three outcomes
that matter — found alive, found dead, still missing — in one picture.

Two panels share the year axis:
  - TOP  (absolute): true scale + how much of each year remains unresolved.
  - BOTTOM (100%):   composition — how the outcome mix shifted over time.

This is the signature flow visual: a single coherent read of scale + composition that retired the
earlier split scale/rate charts, and surfaces the found-DEAD band that a generic "located" band hid.

Inputs:  data/processed/flow_by_year.csv  (from src/fetch_flow.py)
Output:  reports/figures/19_outcomes_by_year_consolidated.png
Run:     python src/flow_consolidated.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FLOW = ROOT / "data" / "processed" / "flow_by_year.csv"
FIGDIR = ROOT / "reports" / "figures"

# Sober, meaningful palette: alive = calm slate-blue, dead = charcoal, missing = deep red.
ALIVE = "#7d9bb5"
DEAD = "#2b2b2b"
MISSING = "#7a1f1f"
INK = "#2b2b2b"
MUTED = "#9a9a9a"
plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 11,
    "axes.edgecolor": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": INK,
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
})

START, END = 2000, 2025


def load() -> pd.DataFrame:
    df = pd.read_csv(FLOW, index_col=0)
    df.index = pd.to_numeric(df.index, errors="coerce")
    df = df[df.index.notna()]
    df.index = df.index.astype(int)
    df = df[(df.index >= START) & (df.index <= END)].sort_index()
    out = pd.DataFrame({
        "Found alive": df["loc_con_vida"],
        "Found dead": df["loc_sin_vida"],
        "Still missing": df["desap_y_nollocal"],
    })
    # sanity: the three outcomes should sum to true incidence (todos)
    resid = (out.sum(axis=1) - df["todos"]).abs().max()
    if resid > 1:
        print(f"  NOTE: outcomes vs incidence mismatch up to {resid:.0f} (rounding/in-flux rows)")
    return out


def main():
    if not FLOW.exists():
        raise FileNotFoundError("Run src/fetch_flow.py first.")
    d = load()
    yrs = d.index
    cols = ["Found alive", "Found dead", "Still missing"]
    colors = [ALIVE, DEAD, MISSING]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True,
                                   gridspec_kw={"height_ratios": [2.1, 1]})
    fig.subplots_adjust(left=0.10, right=0.97, top=0.90, bottom=0.20, hspace=0.12)

    # --- TOP: absolute, stacked alive -> dead -> missing ---
    bottom = pd.Series(0, index=yrs, dtype=float)
    for c, col in zip(cols, colors):
        ax1.bar(yrs, d[c], bottom=bottom, color=col, width=0.85, label=c)
        bottom += d[c]
    tot = int(d["Still missing"].sum())
    fig.suptitle("Mexico's disappeared, by year and outcome", x=0.10, ha="left",
                 fontsize=15, fontweight="bold", y=0.965)
    ax1.set_title(f"RNPDNO flow, all statuses · {tot:,} of these people are still missing today",
                  loc="left", fontsize=10, fontweight="normal", color=MISSING, pad=8)
    ax1.set_ylabel("People who disappeared")
    ax1.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax1.legend(frameon=False, fontsize=9, loc="upper left", ncol=1)
    # drug-war onset marker (point into the empty left region)
    ax1.annotate("2006–07: militarized\n'war on drugs' begins", xy=(2007, d.loc[2007].sum()),
                 xytext=(2002.5, 19000), fontsize=8, color=INK,
                 arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))

    # --- BOTTOM: 100% composition ---
    share = d.div(d.sum(axis=1), axis=0)
    bottom = pd.Series(0, index=yrs, dtype=float)
    for c, col in zip(cols, colors):
        ax2.bar(yrs, share[c], bottom=bottom, color=col, width=0.85)
        bottom += share[c]
    ax2.set_ylabel("Share of outcomes")
    ax2.set_ylim(0, 1)
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    ax2.set_xlabel("Year of disappearance")
    ax2.margins(x=0.01)

    caption = (
        "Top = absolute scale; bottom = the same data as composition. Read together: the RISE is real\n"
        "(incidence grew ~360x since 2000), yet the OUTCOME MIX also shifted — the still-missing share (red)\n"
        "was largest for pre-2007 cohorts (the hard, genuine disappearances), while later years show more\n"
        "locations. The charcoal band is people found DEAD — the registry's closest proxy for the recovery\n"
        "work and the bridge to the madres buscadoras (Stage 2). Source: RNPDNO dashboard flow via\n"
        "src/fetch_flow.py. 'Located' includes contested 2023 censo reclassifications (see methodology §3)."
    )
    fig.text(0.10, 0.015, caption, fontsize=8, color=MUTED, va="bottom", ha="left")

    FIGDIR.mkdir(parents=True, exist_ok=True)
    out = FIGDIR / "19_outcomes_by_year_consolidated.png"
    fig.savefig(out)
    plt.close(fig)

    # console summary
    last = d.loc[END]
    print(f"{START}-{END}: found alive {int(d['Found alive'].sum()):,} | "
          f"found dead {int(d['Found dead'].sum()):,} | still missing {int(d['Still missing'].sum()):,}")
    print(f"  {END}: alive {int(last['Found alive']):,} / dead {int(last['Found dead']):,} / "
          f"missing {int(last['Still missing']):,}")
    print(f"  still-missing share: 2000={d.loc[2000,'Still missing']/d.loc[2000].sum():.0%}  "
          f"2024={d.loc[2024,'Still missing']/d.loc[2024].sum():.0%}")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
