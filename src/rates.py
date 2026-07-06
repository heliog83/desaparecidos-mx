"""
Stage-1 deepening: per-capita disappearance rates by state + a choropleth map.

Absolute counts mostly track population (big states top the list). Normalizing by
population reveals where the crisis is most *intense* relative to who lives there.

Inputs:
  data/processed/rnpdno_clean.parquet      (cleaned microdata)
  data/external/assets/poblacion.csv       (municipal population by year, CONAPO)
  data/external/assets/mexico.json         (state polygons, GeoJSON, keyed by CVE_ENT)
Outputs:
  data/processed/state_rates.csv
  reports/figures/05_rate_by_state.png
  reports/figures/06_choropleth_rate.png

Note: counts are the CUMULATIVE stock of people ever registered as disappeared/not-located
(not an annual flow), so the rate is "registered disappeared per 100k residents".

Run:  python src/rates.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as MplPolygon

ROOT = Path(__file__).resolve().parents[1]
PARQUET = ROOT / "data" / "processed" / "rnpdno_clean.parquet"
POB = ROOT / "data" / "external" / "assets" / "poblacion.csv"
GEO = ROOT / "data" / "external" / "assets" / "mexico.json"
OUT_CSV = ROOT / "data" / "processed" / "state_rates.csv"
FIGDIR = ROOT / "reports" / "figures"
POP_YEAR = "2025"

ACCENT = "#7a1f1f"
INK = "#2b2b2b"
MUTED = "#9a9a9a"
plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 11,
    "axes.edgecolor": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": INK,
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
})


def build_rates() -> pd.DataFrame:
    df = pd.read_parquet(PARQUET)
    # 2-digit zero-padded state code is the universal join key.
    df["cve_ent"] = df["CVE_ENT"].astype("string").str.zfill(2)
    counts = df.groupby("cve_ent").size().rename("desaparecidos")

    pob = pd.read_csv(POB, dtype={"CVE": "string"})
    pob["cve_ent"] = pob["CVE"].str.zfill(5).str[:2]
    pop = pob.groupby("cve_ent")[POP_YEAR].sum().rename("poblacion")

    # State names from the GeoJSON (authoritative CVE_ENT -> name).
    geo = json.loads(GEO.read_text())
    names = {f["properties"]["CVE_ENT"].zfill(2): f["properties"]["NOMGEO"]
             for f in geo["features"]}

    out = pd.concat([counts, pop], axis=1).dropna()
    out["entidad"] = out.index.map(names)
    out["tasa_100k"] = (out["desaparecidos"] / out["poblacion"] * 100_000).round(1)
    out = out.sort_values("tasa_100k", ascending=False)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV)
    return out


def fig_rate_ranking(rates: pd.DataFrame):
    s = rates.sort_values("tasa_100k").tail(15)
    nat = rates["desaparecidos"].sum() / rates["poblacion"].sum() * 100_000
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(s["entidad"], s["tasa_100k"], color=ACCENT)
    ax.axvline(nat, color=INK, lw=1, ls="--")
    ax.text(nat, -0.6, f" national {nat:.0f}", fontsize=8, color=INK)
    ax.set_title("Registered disappeared per 100,000 residents, by state")
    for y, v in enumerate(s["tasa_100k"]):
        ax.text(v, y, f" {v:.0f}", va="center", fontsize=8, color=INK)
    ax.text(0, -0.13, f"Cumulative registered (all years) ÷ {POP_YEAR} population. "
            "Normalizing reveals intensity small states hide in raw counts.",
            transform=ax.transAxes, fontsize=8, color=MUTED)
    _save(fig, "05_rate_by_state.png")


def fig_choropleth(rates: pd.DataFrame):
    geo = json.loads(GEO.read_text())
    rate_by = rates["tasa_100k"].to_dict()
    vmax = float(rates["tasa_100k"].quantile(0.97))
    cmap = plt.get_cmap("OrRd")

    patches, values = [], []
    for f in geo["features"]:
        cve = f["properties"]["CVE_ENT"].zfill(2)
        val = rate_by.get(cve, np.nan)
        geom = f["geometry"]
        rings = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        for poly in rings:
            patches.append(MplPolygon(np.array(poly[0]), closed=True))  # exterior ring
            values.append(val)

    fig, ax = plt.subplots(figsize=(9, 6))
    pc = PatchCollection(patches, edgecolor="white", linewidths=0.4)
    pc.set_array(np.array(values))
    pc.set_clim(0, vmax)
    pc.set_cmap(cmap)
    ax.add_collection(pc)
    ax.autoscale_view()
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Disappearance intensity by state (registered per 100,000)")
    cb = fig.colorbar(pc, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label(f"per 100,000 ({POP_YEAR} pop.)")
    ax.text(0.5, 0.02, "Color capped at the 97th percentile so one outlier doesn't flatten the scale.",
            transform=ax.transAxes, ha="center", fontsize=8, color=MUTED)
    _save(fig, "06_choropleth_rate.png")


def _save(fig, name):
    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIGDIR / name, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {(FIGDIR / name).relative_to(ROOT)}")


def main():
    rates = build_rates()
    print(f"State rates -> {OUT_CSV.relative_to(ROOT)}")
    print("\nTop 6 by RATE (per 100k):")
    print(rates.head(6)[["entidad", "desaparecidos", "tasa_100k"]].to_string(index=False))
    print("\nFor contrast, top 6 by ABSOLUTE count:")
    print(rates.sort_values("desaparecidos", ascending=False)
          .head(6)[["entidad", "desaparecidos", "tasa_100k"]].to_string(index=False))
    print("\nFigures:")
    fig_rate_ranking(rates)
    fig_choropleth(rates)


if __name__ == "__main__":
    main()
