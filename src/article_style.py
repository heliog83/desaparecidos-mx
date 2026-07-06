"""Shared style for the 7 publication figures (reports/figures/article/).

One palette, one typography, one caption format across figs A–G. Semantic colors:
red = missing/redacted, blue = found alive/collectives, charcoal = found dead/ink.
Import and call apply() before building a figure; use save() to emit into article/.
"""
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
ARTDIR = ROOT / "reports" / "figures" / "article"

# palette
RED = "#7a1f1f"       # still missing / CONFIDENCIAL
BLUE = "#3c6e91"      # found alive / collectives
INK = "#2b2b2b"       # found dead / text
SAND = "#cfc8bd"      # neutral fill (records with public details)
MUTED = "#9a9a9a"     # de-emphasized states, gridlines, captions
PAPER = "#ffffff"

FONT_STACK = ["Helvetica Neue", "Arial", "DejaVu Sans"]


def apply():
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 200, "savefig.facecolor": PAPER,
        "figure.facecolor": PAPER, "axes.facecolor": PAPER,
        "font.family": "sans-serif", "font.sans-serif": FONT_STACK, "font.size": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": MUTED, "axes.linewidth": 0.8,
        "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlecolor": INK,
        "axes.titlelocation": "left",
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": INK, "ytick.color": INK,
        "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
        "legend.frameon": False,
    })


def title(fig_or_ax, main: str, sub: str = "", x: float = 0.0):
    """Left-aligned bold title with a plain-language subtitle underneath."""
    if hasattr(fig_or_ax, "suptitle"):  # a Figure
        fig_or_ax.suptitle(main, x=x if x else 0.06, ha="left", fontsize=15,
                           fontweight="bold", color=INK)
        if sub:
            fig_or_ax.text(x if x else 0.06, 0.925, sub, ha="left", fontsize=10,
                           color=MUTED)
    else:  # an Axes
        fig_or_ax.set_title(main, loc="left", pad=16 if sub else 8)
        if sub:
            fig_or_ax.text(0, 1.02, sub, transform=fig_or_ax.transAxes,
                           fontsize=9.5, color=MUTED)


def caption(fig, text: str, x: float = 0.06, y: float = 0.012):
    fig.text(x, y, text, fontsize=8, color=MUTED, va="bottom", ha="left")


def save(fig, name: str):
    ARTDIR.mkdir(parents=True, exist_ok=True)
    out = ARTDIR / name
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")
    return out
