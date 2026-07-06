"""
Option 2 — Category sensitivity: DESAPARECIDA-only vs. DESAPARECIDA + NO LOCALIZADA.

The two statuses mean different things (crime-presumed vs. no-crime-evidence). This quantifies
how much the choice of denominator moves results, so any headline can state its sensitivity and
pre-empt the "you lumped voluntary cases in" critique.

Scope note: this can only speak to NON-CONFIDENTIAL records (the 49k confidential rows hide their
status entirely, so we don't know their split — itself a limit worth stating).

Outputs:
  reports/figures/07_category_sensitivity_by_state.png
Run:  python src/category_compare.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PARQUET = ROOT / "data" / "processed" / "rnpdno_clean.parquet"
FIGDIR = ROOT / "reports" / "figures"

ACCENT = "#7a1f1f"
INK = "#2b2b2b"
MUTED = "#9a9a9a"
plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 11,
    "axes.edgecolor": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": INK,
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
})


def main():
    df = pd.read_parquet(PARQUET)
    known = df[df["ESTATUS_VICTIMA"].notna()].copy()   # non-confidential
    n_known = len(known)
    n_nl = (known["ESTATUS_VICTIMA"] == "NO LOCALIZADA").sum()

    print(f"Non-confidential records: {n_known:,} "
          f"({len(df) - n_known:,} confidential excluded — status unknown)")
    print(f"NO LOCALIZADA: {n_nl:,}  =>  including it inflates the count by "
          f"{n_nl / (n_known - n_nl):.1%} nationally (among non-confidential).")

    # By state: how much does adding NO LOCALIZADA change each state's count?
    g = known.groupby("ENTIDAD")["ESTATUS_VICTIMA"].value_counts().unstack(fill_value=0)
    g["desap"] = g.get("DESAPARECIDA", 0)
    g["nl"] = g.get("NO LOCALIZADA", 0)
    g["pct_uplift"] = (g["nl"] / g["desap"].replace(0, pd.NA) * 100)
    g["total_known"] = g["desap"] + g["nl"]
    g = g[g["total_known"] >= 500].sort_values("pct_uplift", ascending=False)

    print("\nStates where the category choice matters MOST (NO LOCALIZADA as % of DESAPARECIDA):")
    print(g.head(8)[["desap", "nl", "pct_uplift"]].round(1).to_string())
    print("\nStates where it barely matters:")
    print(g.tail(5)[["desap", "nl", "pct_uplift"]].round(1).to_string())

    # Figure: uplift by state.
    s = g.sort_values("pct_uplift").tail(15)
    nat = n_nl / (n_known - n_nl) * 100
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(s.index, s["pct_uplift"], color=ACCENT)
    ax.axvline(nat, color=INK, lw=1, ls="--")
    ax.text(nat, -0.6, f" national {nat:.1f}%", fontsize=8, color=INK)
    ax.set_title("Sensitivity to category choice, by state\n"
                 "(how much adding NO LOCALIZADA to DESAPARECIDA inflates the count)")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    for y, v in enumerate(s["pct_uplift"]):
        ax.text(v, y, f" {v:.1f}%", va="center", fontsize=8, color=INK)
    ax.text(0, -0.14, "Non-confidential records only (states with >=500). A high value means that "
            "state's total depends heavily on a category that does NOT presume a crime.",
            transform=ax.transAxes, fontsize=8, color=MUTED)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    out = FIGDIR / "07_category_sensitivity_by_state.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"\nwrote {out.relative_to(ROOT)}")

    # Verdict for the methodology record.
    print("\nVERDICT: nationally the choice moves the count only ~{:.0f}%, so combined-vs-DESAPARECIDA"
          .format(nat))
    print("is a minor headline risk — BUT it is concentrated in specific states, and the 37%")
    print("confidential bucket is a far larger unknown than the NO LOCALIZADA question.")


if __name__ == "__main__":
    main()
