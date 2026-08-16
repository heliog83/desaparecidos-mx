"""Publication versions of the four reused article figures (A–D).

Rebuilds fig 19 / 06 / 09 / 10 in the shared article style (article_style.py)
without touching the pipeline scripts or their numbered outputs.

  A_outcomes_by_year.png       <- frozen RNPDNO totals + flow_by_year.csv
  B_rate_map.png               <- data/processed/state_rates.csv + mexico.json
  C_confidential_share.png     <- data/processed/rnpdno_clean.parquet
  D_redaction_vs_rate.png      <- parquet + state_rates.csv (join on cve_ent)

Run:  MPLBACKEND=Agg python src/article_figs.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Patch, Polygon as MplPolygon

import article_style as st

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data" / "publication_freezes" / "2026-08-15"
FLOW = FREEZE / "derived" / "flow_by_year.csv"
TOTALS = FREEZE / "sources" / "rnpdno_api" / "totales.json"
PARQUET = ROOT / "data" / "processed" / "rnpdno_clean.parquet"
RATES = ROOT / "data" / "processed" / "state_rates.csv"
GEO = ROOT / "data" / "external" / "assets" / "mexico.json"

ALIVE = "#8fadc4"  # light tint of article blue for the large found-alive band
CASE_RED = {"14": "Jalisco", "18": "Nayarit"}      # redaction-mode case states
CASE_BLUE = {"12": "Guerrero", "06": "Colima"}     # omission-mode case states


def fig_a():
    totals = json.loads(TOTALS.read_text(encoding="utf-8"))

    def as_int(key: str) -> int:
        return int(totals[key].replace(",", ""))

    all_status = pd.Series(
        {
            "Found alive": as_int("TotalLocalizadosCV"),
            "Found dead": as_int("TotalLocalizadosSV"),
            "Still missing": as_int("TotalDesaparecidos"),
        }
    )
    all_records = as_int("TotalGlobal")
    if int(all_status.sum()) != all_records:
        raise ValueError("RNPDNO outcome totals do not reconcile to TotalGlobal")

    df = pd.read_csv(FLOW, index_col=0)
    df.index = pd.to_numeric(df.index, errors="coerce")
    df = df[df.index.notna()]
    df.index = df.index.astype(int)
    df = df[(df.index >= 2000) & (df.index <= 2025)].sort_index()
    d = pd.DataFrame({"Found alive": df["loc_con_vida"], "Found dead": df["loc_sin_vida"],
                      "Still missing": df["desap_y_nollocal"]})
    yrs, cols = d.index, ["Found alive", "Found dead", "Still missing"]
    colors = [ALIVE, st.INK, st.RED]

    fig, (ax0, ax1) = plt.subplots(
        2,
        1,
        figsize=(10, 7.5),
        gridspec_kw={"height_ratios": [0.9, 3.2]},
    )
    fig.subplots_adjust(left=0.09, right=0.97, top=0.87, bottom=0.16, hspace=0.44)
    st.title(fig, "One in three remains missing",
             f"Mexico, current outcome of all {all_records:,} people in the national disappearance registry, August 15th 2026",
             x=0.09)

    # Complete all-period accounting: one compact bar that reconciles every
    # registry record, including records without a usable disappearance year.
    ax0.set_title("All records, current status", loc="left", pad=8, fontsize=11,
                  weight="bold")
    left = 0
    for label, color in zip(cols, colors):
        value = int(all_status[label])
        ax0.barh(0, value, left=left, height=0.48, color=color)
        centre = left + value / 2
        pct = value / all_records
        if label == "Found dead":
            ax0.annotate(
                f"FOUND DEAD  {value:,} · {pct:.0%}",
                xy=(centre, 0.24),
                xytext=(centre, 0.55),
                ha="center",
                va="bottom",
                fontsize=8.5,
                weight="bold",
                color=st.INK,
                arrowprops=dict(arrowstyle="-", color=st.MUTED, lw=0.8),
            )
        else:
            ax0.text(
                centre,
                0,
                f"{label.upper()}\n{value:,} · {pct:.0%}",
                ha="center",
                va="center",
                fontsize=9,
                weight="bold",
                color="white",
            )
        left += value
    ax0.set_xlim(0, all_records)
    ax0.set_ylim(-0.38, 0.82)
    ax0.axis("off")

    bottom = pd.Series(0.0, index=yrs)
    for c, col in zip(cols, colors):
        ax1.bar(yrs, d[c], bottom=bottom, color=col, width=0.85)
        bottom += d[c]
    ax1.set_title("By year of disappearance, current outcome", loc="left", pad=10,
                  fontsize=11, weight="bold")
    # Direct band labels at the right edge instead of a legend.
    y_cum = d.loc[2025].cumsum()
    for c, col in zip(cols, [st.BLUE, st.INK, st.RED]):
        ymid = y_cum[c] - d.loc[2025, c] / 2
        ax1.annotate(c.upper(), xy=(2025.6, ymid), fontsize=9, weight="bold",
                     color=col, va="center", annotation_clip=False)
    ax1.set_ylabel("People recorded")
    ax1.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax1.set_xlim(1999.2, 2028.6)
    ax1.set_xlabel("Year of disappearance")
    ax1.set_xticks([2000, 2005, 2010, 2015, 2020, 2025])

    for year in (2015, 2025):
        total = int(d.loc[year].sum())
        ax1.text(year, total + 650, f"{total:,}", ha="center", va="bottom",
                 fontsize=8.5, weight="bold", color=st.INK)

    st.caption(
        fig,
        "Top includes all registry records. Annual bars include 352,294 records with a known disappearance year in 2000–25;\n"
        "historical reporting is incomplete. Outcomes are current at August 15th 2026. Source: RNPDNO dashboard API.",
        x=0.09,
    )
    st.save(fig, "A_outcomes_by_year.png")


def fig_b():
    rates = pd.read_csv(RATES, dtype={"cve_ent": "string"}).set_index("cve_ent")
    geo = json.loads(GEO.read_text())
    bins = [0, 50, 100, 150, 225, 400]
    bin_colors = ["#f5e4dc", "#e5bfae", "#cf8d78", "#b25545", "#7a1f1f"]

    def color_for(v):
        for hi, c in zip(bins[1:], bin_colors):
            if v <= hi:
                return c
        return bin_colors[-1]

    patches, colors, centroids = [], [], {}
    for f in geo["features"]:
        cve = f["properties"]["CVE_ENT"].zfill(2)
        val = rates["tasa_100k"].get(cve, np.nan)
        geom = f["geometry"]
        rings = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        biggest, biggest_n = None, 0
        for poly in rings:
            arr = np.array(poly[0])
            patches.append(MplPolygon(arr, closed=True))
            colors.append(color_for(val) if not np.isnan(val) else "#eeeeee")
            if len(arr) > biggest_n:
                biggest, biggest_n = arr, len(arr)
        centroids[cve] = biggest.mean(axis=0)

    fig, ax = plt.subplots(figsize=(10, 6.4))
    fig.subplots_adjust(top=0.86)
    st.title(fig, "Where the crisis is most intense, per person",
             "Registered disappeared per 100,000 residents (cumulative stock ÷ 2025 population)", x=0.06)
    pc = PatchCollection(patches, facecolor=colors, edgecolor="white", linewidths=0.5)
    ax.add_collection(pc)
    ax.autoscale_view()
    ax.set_aspect("equal")
    ax.axis("off")

    for cve in ["28", "32", "25"]:  # Tamaulipas, Zacatecas, Sinaloa
        cx, cy = centroids[cve]
        name, rate = rates.loc[cve, "entidad"], rates.loc[cve, "tasa_100k"]
        ax.annotate(f"{name}\n{rate:.0f}", (cx, cy), xytext=(cx, cy + 2.6),
                    ha="center", fontsize=8.5, weight="bold", color=st.INK,
                    arrowprops=dict(arrowstyle="-", color=st.INK, lw=0.7))

    handles = [Patch(facecolor=c, label=f"{lo}–{hi}")
               for lo, hi, c in zip(bins[:-1], bins[1:], bin_colors)]
    ax.legend(handles=handles, title="per 100,000", loc="lower left",
              fontsize=8.5, title_fontsize=8.5)
    st.caption(fig, "Discrete bins avoid one outlier flattening the scale. National rate: "
                    f"{rates['desaparecidos'].sum() / rates['poblacion'].sum() * 1e5:.0f} per 100,000. "
                    "Source: RNPDNO mirror microdata + CONAPO population.")
    st.save(fig, "B_rate_map.png")


def load_opacity():
    df = pd.read_parquet(PARQUET)
    df["cve_ent"] = df["CVE_ENT"].astype("string").str.zfill(2)
    g = df.groupby("cve_ent").agg(total=("ID_VICTIMA", "size"),
                                  conf=("confidencial", "sum"))
    g["share"] = g["conf"] / g["total"]
    rates = pd.read_csv(RATES, dtype={"cve_ent": "string"}).set_index("cve_ent")
    g = g.join(rates[["entidad", "tasa_100k"]], how="inner")
    return g, df["confidencial"].mean()


def fig_c():
    g, national = load_opacity()
    g = g.sort_values("share")

    fig, ax = plt.subplots(figsize=(8.5, 9.2))
    fig.subplots_adjust(top=0.90, left=0.22)
    st.title(fig, "One crisis, 32 publication practices",
             "Share of each state's unresolved records fully redacted (CONFIDENCIAL) in the public registry", x=0.06)
    colors, weights = [], []
    for cve in g.index:
        if cve in CASE_RED:
            colors.append(st.RED)
        elif cve in CASE_BLUE:
            colors.append(st.BLUE)
        else:
            colors.append(st.SAND)
    ax.barh(g["entidad"], g["share"], color=colors)
    ax.axvline(national, color=st.INK, lw=1, ls="--")
    ax.text(national + 0.004, 0.2, f"national {national:.0%}", fontsize=8.5, color=st.INK)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    for cve, hl in [*CASE_RED.items(), *CASE_BLUE.items()]:
        row = g.loc[cve]
        y = list(g.index).index(cve)
        ax.text(row["share"] + 0.004, y, f"{row['share']:.0%}", va="center",
                fontsize=9, weight="bold",
                color=st.RED if cve in CASE_RED else st.BLUE)
    for label in ax.get_yticklabels():
        if label.get_text() in ("Jalisco", "Nayarit"):
            label.set_color(st.RED); label.set_weight("bold")
        elif label.get_text() in ("Guerrero", "Colima"):
            label.set_color(st.BLUE); label.set_weight("bold")
    st.caption(fig, "A confidential record keeps one public fact: the state. Red: case states with high redaction;\n"
                    "blue: high-violence case states with low redaction. Source: RNPDNO mirror microdata.")
    st.save(fig, "C_confidential_share.png")


def fig_d():
    g, _ = load_opacity()

    fig, ax = plt.subplots(figsize=(9, 6.4))
    fig.subplots_adjust(top=0.87, bottom=0.18)
    st.title(fig, "Redaction does not follow the crisis",
             "If confidentiality tracked danger, states would line up. They don't.", x=0.06)
    others = g[~g.index.isin(list(CASE_RED) + list(CASE_BLUE))]
    ax.scatter(others["tasa_100k"], others["share"], s=48, color=st.SAND,
               edgecolor="white", linewidth=0.6, zorder=2)
    offsets = {"Jalisco": (10, 4, "left"), "Nayarit": (-10, -4, "right"),
               "Guerrero": (10, 4, "left"), "Colima": (10, 4, "left")}
    for cve, name in {**CASE_RED, **CASE_BLUE}.items():
        row = g.loc[cve]
        color = st.RED if cve in CASE_RED else st.BLUE
        dx, dy, ha = offsets[name]
        ax.scatter(row["tasa_100k"], row["share"], s=110, color=color, zorder=3)
        ax.annotate(name, (row["tasa_100k"], row["share"]),
                    xytext=(dx, dy), textcoords="offset points", ha=ha,
                    fontsize=10, weight="bold", color=color)
    tam = g.loc["28"]
    ax.annotate("Tamaulipas", (tam["tasa_100k"], tam["share"]), xytext=(-8, 8),
                textcoords="offset points", ha="right", fontsize=8.5, color=st.MUTED)

    ax.set_xlabel("Unresolved disappearances per 100,000 residents   (right = more disappearances)")
    ax.set_ylabel("Share of records redacted   (up = more hidden)")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    ax.set_ylim(0, 0.75)
    st.caption(fig, "Each dot is a state. Guerrero has roughly 2.4× Jalisco's homicide rate and one-seventh of its\n"
                    "redaction share. Source: RNPDNO mirror microdata + CONAPO population.")
    st.save(fig, "D_redaction_vs_rate.png")


if __name__ == "__main__":
    st.apply()
    fig_a()
    fig_b()
    fig_c()
    fig_d()
