"""Fig 28: Mexico's registry against other countries' missing-persons universes.

Two panels, identical row order, so the reader watches Mexico move:

  left  — absolute totals. Mexico sits among countries that fought wars.
  right — per 100,000 residents. Mexico falls to the bottom of the same list.

That reordering IS the finding. The honest claim is not "Mexico is worse than war
countries" — per capita it plainly is not — but that Mexico has accumulated a
registry the size of Colombia's sixty-year armed-conflict universe, in peacetime,
mostly since 2006.

Every figure counts something different and the chart says so on its face: each row
carries its own definition, and the footer states the category mismatch outright.
Iraq is drawn as a range because its own authorities' estimate spans a factor of four.

Figures, definitions and sourcing: docs/international-comparison.md.
Populations are approximate, at the period each figure refers to, and are the
weakest input here — the rate panel is labelled accordingly.

Run:  MPLBACKEND=Agg python src/international_comparison.py
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import article_style as st

# name, low, high (None = point estimate), population, context, definition shown on the row
ROWS = [
    ("Iraq", 250_000, 1_000_000, 45_000_000, "conflict",
     "decades of war, Ba'ath-era atrocity, Da'esh"),
    ("Syria", 300_000, None, 23_000_000, "conflict",
     "estimates run 'as high as'"),
    ("Colombia", 136_010, None, 52_000_000, "conflict",
     "60-year armed conflict, state search unit"),
    ("Mexico", 134_268, None, 130_000_000, "peace",
     "national registry, no armed conflict"),
    ("Western Balkans", 40_000, None, 8_000_000, "conflict",
     "1990s conflicts; >70% since accounted for"),
    ("Argentina", 30_000, None, 28_000_000, "dictatorship",
     "1976-83 dictatorship; symbolic figure"),
]

COLOR = {"peace": st.RED, "conflict": st.INK, "dictatorship": st.MUTED}
LABEL = {"peace": "No armed conflict", "conflict": "Armed conflict",
         "dictatorship": "Military dictatorship"}


def main() -> None:
    st.apply()
    rows = list(ROWS)
    ys = list(range(len(rows)))[::-1]  # first row at the top

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 6.2))
    fig.subplots_adjust(left=0.155, right=0.985, top=0.80, bottom=0.20, wspace=0.30)
    st.title(
        fig,
        "Mexico's registry is the size of a war's, without the war",
        "Missing-persons universes by country. Left: totals. Right: the same figures per 100,000 residents.",
        x=0.012,
    )

    for ax, mode in ((ax1, "abs"), (ax2, "rate")):
        for y, (name, low, high, pop, ctx, _note) in zip(ys, rows):
            c = COLOR[ctx]
            big = name == "Mexico"
            lo = low if mode == "abs" else low / pop * 1e5
            hi = (high if mode == "abs" else high / pop * 1e5) if high else None
            if hi:
                ax.plot([lo, hi], [y, y], color=c, lw=2.4, solid_capstyle="round", zorder=2)
                ax.scatter([lo, hi], [y, y], s=52, color=c, zorder=3)
            else:
                ax.scatter([lo], [y], s=150 if big else 78, color=c, zorder=3,
                           edgecolor="white", linewidth=1.1 if big else 0)
            txt = (f"{lo:,.0f}–{hi:,.0f}" if hi else f"{lo:,.0f}")
            ax.annotate(txt, (hi or lo, y), xytext=(9, 0), textcoords="offset points",
                        va="center", fontsize=8.8, color=c,
                        weight="bold" if big else "normal")
        ax.set_yticks(ys)
        ax.set_ylim(-0.75, len(rows) - 0.25)
        ax.grid(axis="x", color="#e6e6e6", lw=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))

    ax1.set_yticklabels([r[0] for r in rows][::-1], fontsize=10.5)
    for tick, (name, *_rest) in zip(ax1.get_yticklabels()[::-1], rows):
        if name == "Mexico":
            tick.set_color(st.RED)
            tick.set_fontweight("bold")
    ax2.set_yticklabels([])

    ax1.set_title("People recorded missing", loc="left", fontsize=10.5,
                  weight="bold", pad=8)
    ax2.set_title("Per 100,000 residents", loc="left", fontsize=10.5,
                  weight="bold", pad=8)
    ax1.set_xlim(0, 1_180_000)
    ax2.set_xlim(0, 2_600)

    # The one comparison the piece rests on.
    y_col = ys[rows.index(("Colombia",) + ROWS[2][1:])] if False else ys[2]
    y_mex = ys[3]
    ax1.annotate(
        "", xy=(136_010, y_col), xytext=(134_268, y_mex),
        arrowprops=dict(arrowstyle="-", color=st.RED, lw=1.0, ls=":"))
    ax1.annotate(
        "1.3% apart —\nbut Colombia's universe is a\n60-year armed conflict",
        xy=(136_010, (y_col + y_mex) / 2), xytext=(300_000, (y_col + y_mex) / 2),
        fontsize=8.6, color=st.RED, va="center",
        arrowprops=dict(arrowstyle="-", color=st.RED, lw=0.8))

    ax2.annotate("per head, Mexico is the\nlowest on this list",
                 xy=(103, ys[3]), xytext=(560, ys[3] - 0.85),
                 fontsize=8.6, color=st.RED, va="center",
                 arrowprops=dict(arrowstyle="->", color=st.RED, lw=0.9))

    handles = [plt.Line2D([], [], marker="o", ls="", markersize=8,
                          color=COLOR[k], label=LABEL[k])
               for k in ("conflict", "dictatorship", "peace")]
    ax1.legend(handles=handles, loc="lower right", frameon=False, fontsize=8.8,
               handletextpad=0.5)

    st.caption(
        fig,
        "THESE FIGURES DO NOT COUNT THE SAME THING and cannot be read as a ranking. Mexico's registry includes NO LOCALIZADA cases, "
        "where no crime need be evidenced; Colombia's universe is armed-conflict related; the Western Balkans figure is wartime missing, "
        "of which more than 70% have since been accounted for; Argentina's 30,000 is a symbolic and contested figure, not a register. "
        "Iraq is shown as a range because its authorities' own estimate spans 250,000 to 1,000,000.\nPopulations are approximate, taken at "
        "the period each figure refers to, so the right-hand panel is indicative only. Sources and full definitions: "
        "docs/international-comparison.md. Mexico: RNPDNO API, 2026-08-15. Colombia: UBPD, March 2026. Others: ICMP. Consulted 2026-08-16.",
        x=0.012, y=0.012,
    )

    fig.savefig("reports/figures/28_international_comparison.png", dpi=200,
                bbox_inches="tight")
    print("wrote reports/figures/28_international_comparison.png")


if __name__ == "__main__":
    main()
