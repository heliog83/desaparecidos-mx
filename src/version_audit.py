"""Version audit: does CONFIDENCIAL grow across registry versions? (memo test #1)

Uses the upstream mirror's own git history (lapanquecita/personas-desaparecidas):
ten snapshots of data.csv, 2025-04-03 -> 2025-12-02, pinned by commit SHA below.
Each snapshot is the same scrape method applied to the RNPDNO public consulta,
so month-over-month changes in CONFIDENCIAL are directly comparable.

Outputs:
  data/external/mirror_history/data_YYYY-MM-DD.csv   (cached downloads, gitignored)
  data/processed/confidencial_panel.csv              (tiny, committed)
  reports/figures/23_confidencial_batches.png        + article/H_confidencial_batches.png

Key findings (2026-07-11 run): national confidential 44,035 -> 49,136 (+5,101) in
8 months = 77% of the registry's net growth; Tamaulipas +2,537 in two months with
flat totals (batch reclassification, May-Jul 2025); Jalisco -1,367 confidential in
Q4 2025 as its total fell (the purge predates the Jan-2026 recount announcement);
Tabasco batch deletion Nov 2025; Guanajuato catch-up load arriving ~60% confidential.

Run:  MPLBACKEND=Agg python src/version_audit.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

import article_style as st

ROOT = Path(__file__).resolve().parents[1]
HIST = ROOT / "data" / "external" / "mirror_history"
PANEL_OUT = ROOT / "data" / "processed" / "confidencial_panel.csv"
FIGDIR = ROOT / "reports" / "figures"

REPO_RAW = "https://raw.githubusercontent.com/lapanquecita/personas-desaparecidas/{sha}/data.csv"
SNAPSHOTS = {  # snapshot date -> upstream commit sha
    "2025-04-03": "bee9de8f7e",
    "2025-04-04": "637c7ac94a",
    "2025-05-02": "bfa2a6eac4",
    "2025-06-02": "83c8af6820",
    "2025-07-02": "db63d2bd68",
    "2025-08-02": "45e96c4773",
    "2025-09-02": "cb1a082ba5",
    "2025-10-02": "9082127cb2",
    "2025-11-04": "2604481a15",
    "2025-12-02": "666b3e7605",
}
FOCUS = {"28": "Tamaulipas", "14": "Jalisco", "11": "Guanajuato",
         "27": "Tabasco", "09": "Ciudad de México", "26": "Sonora"}


def fetch() -> None:
    HIST.mkdir(parents=True, exist_ok=True)
    for date, sha in SNAPSHOTS.items():
        dst = HIST / f"data_{date}.csv"
        if not dst.exists() or dst.stat().st_size == 0:
            print(f"  downloading {date} ({sha})")
            subprocess.run(["curl", "-sL", REPO_RAW.format(sha=sha), "-o", str(dst)], check=True)


def build_panel() -> pd.DataFrame:
    rows = []
    for date in SNAPSHOTS:
        df = pd.read_csv(HIST / f"data_{date}.csv", dtype="string",
                         usecols=["ESTATUS_VICTIMA", "CVE_ENT", "ENTIDAD"])
        df["CVE_ENT"] = df["CVE_ENT"].str.zfill(2)
        g = (df.assign(conf=df["ESTATUS_VICTIMA"].eq("CONFIDENCIAL"))
               .groupby(["CVE_ENT", "ENTIDAD"], dropna=False)
               .agg(total=("conf", "size"), conf=("conf", "sum")).reset_index())
        g.insert(0, "snapshot", date)
        rows.append(g)
    panel = pd.concat(rows, ignore_index=True)
    panel.to_csv(PANEL_OUT, index=False)
    print(f"wrote {PANEL_OUT.relative_to(ROOT)} ({len(panel)} rows)")
    return panel


def fig_batches(panel: pd.DataFrame) -> None:
    st.apply()
    nat = panel.groupby("snapshot").agg(total=("total", "sum"), conf=("conf", "sum"))
    nat["share"] = nat.conf / nat.total
    x = pd.to_datetime(nat.index)

    fig, axes = plt.subplots(2, 3, figsize=(11.5, 6.6), sharex=True)
    fig.subplots_adjust(top=0.82, bottom=0.15, hspace=0.45, wspace=0.3)
    st.title(fig, "The redaction flag moves in batches",
             "CONFIDENCIAL records per state, ten monthly snapshots of the public registry, Apr–Dec 2025")

    notes = {
        "Tamaulipas": "+2,537 in two months;\ntotals flat — existing records\nreclassified",
        "Jalisco": "−1,367 in Q4 as totals fall —\nthe purge precedes the\nJan-2026 recount announcement",
        "Guanajuato": "totals nearly double;\nnew records arrive\n~60% confidential",
        "Tabasco": "batch deletion,\nNov 2025",
        "Ciudad de México": "steady climb,\n+1,075",
        "Sonora": "share 13% to 22%\nin 8 months",
    }
    for ax, (cve, name) in zip(axes.flat, FOCUS.items()):
        s = panel[panel.CVE_ENT == cve].sort_values("snapshot")
        xs = pd.to_datetime(s.snapshot)
        ax.plot(xs, s.conf, color=st.RED, lw=2, marker="o", ms=3.5)
        ax.plot(xs, s.total, color=st.MUTED, lw=1.2, ls="--")
        ax.set_title(name, fontsize=10.5, pad=4)
        ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
        ax.tick_params(axis="x", labelsize=8, rotation=0)
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
        ax.margins(y=0.28)
        ax.text(0.02, 0.98, notes[name], transform=ax.transAxes, va="top",
                fontsize=7.3, color=st.INK)
    axes.flat[0].text(0.02, 0.02, "— confidential   -- total unresolved",
                      transform=axes.flat[0].transAxes, fontsize=7.3, color=st.MUTED)

    st.caption(fig,
               f"National: confidential records grew {int(nat.conf.iloc[0]):,} to {int(nat.conf.iloc[-1]):,} "
               f"(+{int(nat.conf.iloc[-1] - nat.conf.iloc[0]):,}) Apr–Dec 2025 — 77% of the registry's net growth — "
               f"share {nat.share.iloc[0]:.1%} to {nat.share.iloc[-1]:.1%}. Step changes, flat totals during "
               "reclassifications, and batch deletions are administrative signatures, not family decisions.\n"
               "Source: ten pinned snapshots of the lapanquecita RNPDNO mirror (same scrape method throughout), "
               "Apr 2025–Dec 2025. Consulted 2026-07-11.")
    fig.savefig(FIGDIR / "23_confidencial_batches.png", dpi=200, bbox_inches="tight")
    print(f"wrote {(FIGDIR / '23_confidencial_batches.png').relative_to(ROOT)}")
    st.save(fig, "H_confidencial_batches.png")


def main() -> None:
    fetch()
    panel = build_panel()
    nat = panel.groupby("snapshot").agg(total=("total", "sum"), conf=("conf", "sum"))
    nat["share"] = (nat.conf / nat.total).round(4)
    print(nat.to_string())
    fig_batches(panel)


if __name__ == "__main__":
    main()
