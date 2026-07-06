"""
Stage-1 exploratory analysis of the RNPDNO microdata.

Loads data/processed/rnpdno_clean.parquet and writes figures to reports/figures/.
Each chart annotates its coverage, because large shares of records are redacted or
undated — honesty about the denominator matters with this data.

Run:  python src/explore.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PARQUET = ROOT / "data" / "processed" / "rnpdno_clean.parquet"
FIGDIR = ROOT / "reports" / "figures"

# Sober palette for a sober subject.
INK = "#2b2b2b"
ACCENT = "#7a1f1f"   # deep red
MUTED = "#9a9a9a"
MALE = "#3b5b7a"
FEMALE = "#9c4f6c"

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 11,
    "axes.edgecolor": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": INK,
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
})


def _save(fig, name: str):
    FIGDIR.mkdir(parents=True, exist_ok=True)
    path = FIGDIR / name
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")


def fig_by_year(df):
    s = df.loc[df["anio_desaparicion"].between(1990, 2025), "anio_desaparicion"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(s.index, s.values, color=ACCENT, width=0.8)
    ax.set_title("People who went missing each year and REMAIN missing (RNPDNO stock)")
    ax.set_ylabel("Still-missing people, by year of disappearance")
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    cov = df["FECHA_DESAPARICION"].notna().mean()
    ax.text(0, -0.22, f"Among records with a known disappearance date ({cov:.0%} of all). This is the STILL-MISSING "
            "stock, not all disappearances. Flow data (fig 08) shows the recent rise is REAL incidence growth,\nnot a "
            "survivorship artifact — but this view still undercounts each year's true total. See docs/methodology.md.",
            transform=ax.transAxes, fontsize=8, color=MUTED)
    _save(fig, "01_disappearances_by_year.png")


def fig_by_state(df):
    s = df["ENTIDAD"].value_counts().head(15).sort_values()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(s.index, s.values, color=INK)
    ax.set_title("Top 15 states by registered disappeared persons")
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    for y, v in enumerate(s.values):
        ax.text(v, y, f" {v:,}", va="center", fontsize=8, color=INK)
    _save(fig, "02_by_state.png")


def fig_age_sex(df):
    d = df.dropna(subset=["grupo_edad", "SEXO"])
    d = d[d["SEXO"].isin(["Hombre", "Mujer"])]
    order = ["0-12", "13-17", "18-29", "30-44", "45-59", "60+"]
    piv = d.pivot_table(index="grupo_edad", columns="SEXO", values="ID_VICTIMA",
                        aggfunc="count", observed=True).reindex(order).fillna(0)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(piv.index, -piv["Hombre"], color=MALE, label="Hombre")
    ax.barh(piv.index, piv["Mujer"], color=FEMALE, label="Mujer")
    ax.set_title("Age at disappearance, by sex")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{abs(x):,.0f}"))
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.legend(frameon=False, loc="lower right")
    cov = df["edad_desaparicion"].notna().mean()
    ax.text(0, -0.18, f"Among records with known age and sex ({cov:.0%} of all records). "
            "Young adults (18-29) dominate; the female share peaks in adolescence.",
            transform=ax.transAxes, fontsize=8, color=MUTED)
    _save(fig, "03_age_sex.png")


def fig_redaction(df):
    # Redacted records keep their STATE but lose dates/status/sex, so we break the
    # redaction share down by state (not by year, which the redaction itself removes).
    g = df.groupby("ENTIDAD").agg(n=("ID_VICTIMA", "size"), share=("confidencial", "mean"))
    g = g[g["n"] >= 1000].sort_values("share").tail(15)
    overall = df["confidencial"].mean()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(g.index, g["share"], color=ACCENT)
    ax.axvline(overall, color=INK, lw=1, ls="--")
    ax.text(overall, -0.6, f" national avg {overall:.0%}", fontsize=8, color=INK)
    ax.set_title("Share of records with redacted (CONFIDENCIAL) details, by state")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    for y, v in enumerate(g["share"]):
        ax.text(v, y, f" {v:.0%}", va="center", fontsize=8, color=INK)
    ax.text(0, -0.13, "States with >=1,000 records. Redacted records withhold status/sex/dates, "
            "so a high share means that state's data is largely unusable for analysis.",
            transform=ax.transAxes, fontsize=8, color=MUTED)
    _save(fig, "04_redaction_by_state.png")


def main():
    if not PARQUET.exists():
        raise FileNotFoundError(f"Missing {PARQUET}. Run: python src/clean.py")
    df = pd.read_parquet(PARQUET)

    print(f"Loaded {len(df):,} records. Headline numbers:")
    print(f"  status: {df['ESTATUS_VICTIMA'].value_counts(dropna=False).to_dict()}")
    last = df.loc[df['anio_desaparicion'].between(2018, 2025)]
    print(f"  2018->2025 yearly counts: "
          f"{last['anio_desaparicion'].value_counts().sort_index().to_dict()}")

    print("Figures:")
    fig_by_year(df)
    fig_by_state(df)
    fig_age_sex(df)
    fig_redaction(df)
    print(f"Done. See {FIGDIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
