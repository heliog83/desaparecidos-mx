"""Publication versions of the four reused article figures (A–D).

Rebuilds fig 19 / 06 / 09 / 10 in the shared article style (article_style.py)
without touching the pipeline scripts or their numbered outputs.

  A_outcomes_by_year.png       <- data/processed/flow_by_year.csv
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
FLOW = ROOT / "data" / "processed" / "flow_by_year.csv"
PARQUET = ROOT / "data" / "processed" / "rnpdno_clean.parquet"
RATES = ROOT / "data" / "processed" / "state_rates.csv"
GEO = ROOT / "data" / "external" / "assets" / "mexico.json"

ALIVE = "#8fadc4"  # light tint of article blue for the large found-alive band
CASE_RED = {"14": "Jalisco", "18": "Nayarit"}      # redaction-mode case states
CASE_BLUE = {"12": "Guerrero", "06": "Colima"}     # omission-mode case states


def fig_a():
    df = pd.read_csv(FLOW, index_col=0)
    df.index = pd.to_numeric(df.index, errors="coerce")
    df = df[df.index.notna()]
    df.index = df.index.astype(int)
    df = df[(df.index >= 2000) & (df.index <= 2025)].sort_index()
    d = pd.DataFrame({"Found alive": df["loc_con_vida"], "Found dead": df["loc_sin_vida"],
                      "Still missing": df["desap_y_nollocal"]})
    yrs, cols = d.index, ["Found alive", "Found dead", "Still missing"]
    colors = [ALIVE, st.INK, st.RED]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8.6), sharex=True,
                                   gridspec_kw={"height_ratios": [2.1, 1]})
    fig.subplots_adjust(left=0.09, right=0.97, top=0.885, bottom=0.16, hspace=0.10)
    st.title(fig, "Mexico's disappeared, by year and outcome",
             f"Every reported disappearance since 2000 — {int(d['Still missing'].sum()):,} of these people are still missing",
             x=0.09)

    bottom = pd.Series(0.0, index=yrs)
    for c, col in zip(cols, colors):
        ax1.bar(yrs, d[c], bottom=bottom, color=col, width=0.85)
        bottom += d[c]
    # direct band labels at the right edge instead of a legend
    y_cum = d.loc[2025].cumsum()
    for c, col in zip(cols, [st.BLUE, st.INK, st.RED]):
        ymid = y_cum[c] - d.loc[2025, c] / 2
        ax1.annotate(c.upper(), xy=(2025.6, ymid), fontsize=9, weight="bold",
                     color=col, va="center", annotation_clip=False)
    ax1.set_ylabel("People who disappeared")
    ax1.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax1.set_xlim(1999.2, 2028.6)
    ax1.annotate("2006–07: militarized\n'war on drugs' begins",
                 xy=(2007, d.loc[2007].sum()), xytext=(2001.5, 15000),
                 fontsize=8.5, color=st.INK,
                 arrowprops=dict(arrowstyle="->", color=st.MUTED, lw=1))

    share = d.div(d.sum(axis=1), axis=0)
    bottom = pd.Series(0.0, index=yrs)
    for c, col in zip(cols, colors):
        ax2.bar(yrs, share[c], bottom=bottom, color=col, width=0.85)
        bottom += share[c]
    ax2.set_ylim(0, 1)
    ax2.set_ylabel("Share of outcomes")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    ax2.set_xlabel("Year of disappearance")
    ax2.annotate("older cohorts\nstay missing:\ntime does not\nfind people", xy=(2026.2, 0.93),
                 va="top", fontsize=9, color=st.RED, weight="bold", annotation_clip=False)

    st.caption(fig, "Top: absolute counts. Bottom: the same years as shares. The rise is real incidence, not accumulation;\n"
                    "the still-missing share is LARGEST for pre-2007 cohorts. Source: RNPDNO dashboard API. 'Located' includes\n"
                    "contested 2023 censo reclassifications (see methodology).", x=0.09)
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
