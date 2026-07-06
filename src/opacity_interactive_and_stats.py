"""
Build an interactive opacity typology chart and richer state-level clue analysis.

Outputs:
  data/processed/state_opacity_enriched.csv
  data/processed/opacity_variable_correlations.csv
  reports/figures/16_opacity_typology_interactive.html
  reports/figures/17_opacity_variable_correlations.png
  reports/figures/18_opacity_clue_model_coefficients.png

Run:
  python src/opacity_interactive_and_stats.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
EXTERNAL = ROOT / "data" / "external"
FIGDIR = ROOT / "reports" / "figures"

STATE_TYPOLOGY = PROC / "state_opacity_typology.csv"
FLOW_BY_STATE = PROC / "flow_by_state.csv"
VICTIMS = EXTERNAL / "assets" / "timeseries_victimas.csv"
POBLACION = EXTERNAL / "assets" / "poblacion.csv"
PIBE_ZIP = EXTERNAL / "inegi" / "pibe_2024_csv.zip"
PIBE_MEMBER = "conjunto_de_datos/conjunto_de_datos_pibe_actividad_pibe2024_p.csv"
OUT_ENRICHED = PROC / "state_opacity_enriched.csv"
OUT_CORR = PROC / "opacity_variable_correlations.csv"
OUT_PIBE = EXTERNAL / "inegi" / "pibe_state_2024_extracted.csv"
OUT_ENCIG = EXTERNAL / "inegi" / "encig_corruption_prevalence_2025_extracted.csv"

HTML_OUT = FIGDIR / "16_opacity_typology_interactive.html"
CORR_FIG = FIGDIR / "17_opacity_variable_correlations.png"
COEF_FIG = FIGDIR / "18_opacity_clue_model_coefficients.png"

INK = "#2b2b2b"
RED = "#7a1f1f"
BLUE = "#3b5b7a"
GOLD = "#9a6b1f"
GREEN = "#4f6f52"
MUTED = "#8b8b8b"

TYPE_ORDER = [
    "High scale / high opacity",
    "High scale / lower opacity",
    "Lower scale / high opacity",
    "Lower scale / lower opacity",
]

PALETTE = {
    "High scale / high opacity": RED,
    "High scale / lower opacity": BLUE,
    "Lower scale / high opacity": GOLD,
    "Lower scale / lower opacity": GREEN,
}


def _norm_state(s: pd.Series) -> pd.Series:
    out = (
        s.astype("string")
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("ascii")
        .str.strip()
    )
    replacements = {
        "MEXICO": "ESTADO DE MEXICO",
        "VERACRUZ DE IGNACIO DE LA LLAVE": "VERACRUZ",
        "COAHUILA DE ZARAGOZA": "COAHUILA",
        "MICHOACAN DE OCAMPO": "MICHOACAN",
        "MICHOACANO": "MICHOACAN",
    }
    return out.replace(replacements)


def _state_population_2024() -> pd.DataFrame:
    pop = pd.read_csv(POBLACION, dtype={"CVE": "string"})
    pop["cve_ent"] = pop["CVE"].str.zfill(5).str[:2]
    state_pop = (
        pop.groupby(["cve_ent", "Entidad"], as_index=False)["2024"]
        .sum()
        .rename(columns={"Entidad": "poblacion_entidad_nombre", "2024": "population_2024"})
    )
    state_pop["state_key"] = _norm_state(state_pop["poblacion_entidad_nombre"])
    return state_pop[["state_key", "population_2024"]]


def _extract_pibe_2024() -> pd.DataFrame:
    with zipfile.ZipFile(PIBE_ZIP) as zf:
        with zf.open(PIBE_MEMBER) as fh:
            pibe = pd.read_csv(fh)

    value_col = "2024<P>"
    pibe = pibe[
        pibe["Descriptores"].str.startswith("Millones de pesos a precios de 2018|", na=False)
    ].copy()
    out = pibe[["Descriptores", value_col]].copy()
    out["pibe_state_name"] = (
        out["Descriptores"]
        .str.split("|")
        .str[-1]
        .str.replace(r"<.*?>", "", regex=True)
        .str.strip()
    )
    out = out[~out["pibe_state_name"].eq("Estados Unidos Mexicanos")].copy()
    out["state_key"] = _norm_state(out["pibe_state_name"])
    out = out.rename(columns={value_col: "pibe_2024_millions_2018_mxn"})
    out["pibe_2024_millions_2018_mxn"] = pd.to_numeric(
        out["pibe_2024_millions_2018_mxn"], errors="coerce"
    )

    pop = _state_population_2024()
    out = out.merge(pop, on="state_key", how="left")
    out["pibe_per_capita_2024_2018_mxn"] = (
        out["pibe_2024_millions_2018_mxn"] * 1_000_000 / out["population_2024"]
    )
    out["pibe_source"] = "INEGI PIBE 2024 preliminary, millions of pesos at 2018 prices"
    OUT_PIBE.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_PIBE, index=False)
    return out[
        [
            "state_key",
            "pibe_state_name",
            "pibe_2024_millions_2018_mxn",
            "population_2024",
            "pibe_per_capita_2024_2018_mxn",
            "pibe_source",
        ]
    ]


def _encig_corruption_2025() -> pd.DataFrame:
    # Extracted from INEGI ENCIG 2025 results report, Cuadro 1:
    # "Victimas de actos de corrupcion en al menos uno de los tramites",
    # tasa por cada 100 mil habitantes, enero-diciembre 2023 y 2025.
    rows = [
        ("Aguascalientes", 11951, 13546),
        ("Baja California", 14644, 15598),
        ("Baja California Sur", 10522, 11575),
        ("Campeche", 11802, 12311),
        ("Coahuila de Zaragoza", 11464, 14619),
        ("Colima", 10262, 6992),
        ("Chiapas", 12600, 14192),
        ("Chihuahua", 21891, 18420),
        ("Ciudad de Mexico", 15739, 17905),
        ("Durango", 15322, 15334),
        ("Guanajuato", 10889, 11646),
        ("Guerrero", 18279, 17255),
        ("Hidalgo", 13107, 21452),
        ("Jalisco", 14580, 13514),
        ("Mexico", 12031, 17899),
        ("Michoacan de Ocampo", 12597, 12581),
        ("Morelos", 13679, 13605),
        ("Nayarit", 9460, 8915),
        ("Nuevo Leon", 13354, 16131),
        ("Oaxaca", 16712, 20330),
        ("Puebla", 11897, 15185),
        ("Queretaro", 12359, 9484),
        ("Quintana Roo", 16954, 17176),
        ("San Luis Potosi", 15617, 16720),
        ("Sinaloa", 17728, 19836),
        ("Sonora", 16124, 18355),
        ("Tabasco", 17938, 16171),
        ("Tamaulipas", 12710, 10813),
        ("Tlaxcala", 15242, 13170),
        ("Veracruz de Ignacio de la Llave", 13705, 11648),
        ("Yucatan", 11419, 15570),
        ("Zacatecas", 8912, 9366),
    ]
    out = pd.DataFrame(
        rows,
        columns=[
            "encig_state_name",
            "corruption_prevalence_2023_per100k",
            "corruption_prevalence_2025_per100k",
        ],
    )
    out["state_key"] = _norm_state(out["encig_state_name"])
    out["corruption_prevalence_change_2023_2025"] = (
        out["corruption_prevalence_2025_per100k"]
        - out["corruption_prevalence_2023_per100k"]
    )
    out["corruption_prevalence_pct_change_2023_2025"] = (
        out["corruption_prevalence_change_2023_2025"]
        / out["corruption_prevalence_2023_per100k"]
    )
    out["encig_source"] = (
        "INEGI ENCIG 2025 results report, Cuadro 1, corruption victims per 100k"
    )
    OUT_ENCIG.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_ENCIG, index=False)
    return out


def build_enriched() -> pd.DataFrame:
    state = pd.read_csv(STATE_TYPOLOGY)
    state["state_key"] = _norm_state(state["entidad"])

    pibe = _extract_pibe_2024()
    encig = _encig_corruption_2025()

    flow = pd.read_csv(FLOW_BY_STATE).rename(columns={"Unnamed: 0": "state_name"})
    flow["state_key"] = _norm_state(flow["state_name"])
    flow["resolution_share"] = flow["localizadas"] / flow["todos"].replace(0, np.nan)
    flow["found_dead_among_located_share"] = (
        flow["loc_sin_vida"] / flow["localizadas"].replace(0, np.nan)
    )
    flow["located_dead_share_all_disappeared"] = (
        flow["loc_sin_vida"] / flow["todos"].replace(0, np.nan)
    )
    flow["still_missing_share_flow"] = (
        flow["desap_y_nollocal"] / flow["todos"].replace(0, np.nan)
    )

    keep_flow = [
        "state_key",
        "todos",
        "localizadas",
        "loc_con_vida",
        "loc_sin_vida",
        "desap_y_nollocal",
        "resolution_share",
        "found_dead_among_located_share",
        "located_dead_share_all_disappeared",
        "still_missing_share_flow",
    ]
    out = state.merge(flow[keep_flow], on="state_key", how="left", suffixes=("", "_flow"))
    out = out.merge(pibe, on="state_key", how="left")
    out = out.merge(encig, on="state_key", how="left")

    victims = pd.read_csv(VICTIMS, usecols=["PERIODO", "ENTIDAD", "DELITO", "TOTAL"])
    victims["year"] = pd.to_datetime(victims["PERIODO"], errors="coerce").dt.year
    victims = victims[victims["year"].between(2015, 2025)].copy()
    victims["state_key"] = _norm_state(victims["ENTIDAD"])

    crimes = [
        "Homicidio doloso",
        "Secuestro",
        "Extorsión",
        "Feminicidio",
        "Trata de personas",
        "Rapto",
    ]
    crime_totals = (
        victims[victims["DELITO"].isin(crimes)]
        .pivot_table(index="state_key", columns="DELITO", values="TOTAL", aggfunc="sum")
        .reset_index()
    )
    crime_totals.columns.name = None

    rename = {
        "Homicidio doloso": "homicide_victims_2015_2025",
        "Secuestro": "kidnapping_victims_2015_2025",
        "Extorsión": "extortion_victims_2015_2025",
        "Feminicidio": "femicide_victims_2015_2025",
        "Trata de personas": "human_trafficking_victims_2015_2025",
        "Rapto": "abduction_victims_2015_2025",
    }
    crime_totals = crime_totals.rename(columns=rename)
    out = out.merge(crime_totals, on="state_key", how="left")

    for col in rename.values():
        out[f"{col}_per100k"] = out[col] / out["poblacion"] * 100_000

    out["known_detail_share"] = out["known_records"] / out["total_records"]
    out["log_total_records"] = np.log1p(out["total_records"])
    out["log_confidential_records"] = np.log1p(out["confidential_records"])
    out["confidential_records_per100k"] = (
        out["confidential_records"] / out["poblacion"] * 100_000
    )

    OUT_ENRICHED.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_ENRICHED, index=False)
    return out


def write_interactive(state: pd.DataFrame) -> None:
    scale_cutoff = state["total_records"].median()
    opacity_cutoff = (
        state["confidential_records"].sum() / state["total_records"].sum()
    )

    hover_cols = {
        "entidad": True,
        "opacity_typology": True,
        "total_records": ":,",
        "confidential_records": ":,",
        "confidential_share": ":.1%",
        "confidential_records_per100k": ":.1f",
        "tasa_100k": ":.1f",
        "known_records": ":,",
        "no_localizada_share_known": ":.1%",
        "todos": ":,",
        "resolution_share": ":.1%",
        "found_dead_among_located_share": ":.1%",
        "located_dead_share_all_disappeared": ":.1%",
        "homicide_victims_2015_2025_per100k": ":.1f",
        "kidnapping_victims_2015_2025_per100k": ":.1f",
        "extortion_victims_2015_2025_per100k": ":.1f",
        "femicide_victims_2015_2025_per100k": ":.2f",
        "human_trafficking_victims_2015_2025_per100k": ":.2f",
        "pibe_2024_millions_2018_mxn": ":,.0f",
        "pibe_per_capita_2024_2018_mxn": ":,.0f",
        "corruption_prevalence_2025_per100k": ":,.0f",
        "corruption_prevalence_change_2023_2025": ":,.0f",
    }

    fig = px.scatter(
        state,
        x="total_records",
        y="confidential_share",
        size="confidential_records",
        color="opacity_typology",
        category_orders={"opacity_typology": TYPE_ORDER},
        color_discrete_map=PALETTE,
        hover_name="entidad",
        hover_data=hover_cols,
        size_max=62,
        labels={
            "total_records": "Total unresolved records",
            "confidential_share": "Share marked CONFIDENCIAL",
            "opacity_typology": "Typology",
        },
        title="State opacity typology: scale vs. intensity",
    )

    fig.add_vline(
        x=scale_cutoff,
        line_dash="dash",
        line_color="rgba(120,120,120,.8)",
        annotation_text=f"median state total: {scale_cutoff:,.0f}",
        annotation_position="top left",
    )
    fig.add_hline(
        y=opacity_cutoff,
        line_dash="dash",
        line_color="rgba(120,120,120,.8)",
        annotation_text=f"national confidential share: {opacity_cutoff:.1%}",
        annotation_position="bottom right",
    )

    for _, row in state.nlargest(7, "confidential_records").iterrows():
        fig.add_annotation(
            x=row["total_records"],
            y=row["confidential_share"],
            text=str(row["entidad"]).title(),
            showarrow=False,
            xshift=16,
            font={"size": 10, "color": INK},
        )

    fig.update_traces(marker={"line": {"width": 0.8, "color": "white"}, "opacity": 0.82})
    fig.update_layout(
        template="plotly_white",
        font={"family": "Arial, sans-serif", "color": INK},
        legend_title_text="Typology",
        margin={"l": 70, "r": 40, "t": 80, "b": 80},
        annotations=list(fig.layout.annotations)
        + [
            go.layout.Annotation(
                text=(
                    "Bubble size = confidential records. Tooltip includes RNPDNO flow metrics "
                    "and SESNSP victim-rate proxies, 2015-2025."
                ),
                x=0,
                y=-0.16,
                xref="paper",
                yref="paper",
                showarrow=False,
                align="left",
                font={"size": 12, "color": MUTED},
            )
        ],
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=",")

    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(HTML_OUT, include_plotlyjs=True, full_html=True)


def _corr_rows(state: pd.DataFrame) -> pd.DataFrame:
    variables = {
        "log_total_records": "Scale: log unresolved records",
        "tasa_100k": "Unresolved records per 100k",
        "confidential_records_per100k": "Confidential records per 100k",
        "no_localizada_share_known": "No-localizada share among known",
        "resolution_share": "Resolution share, live RNPDNO",
        "found_dead_among_located_share": "Found-dead among located",
        "located_dead_share_all_disappeared": "Located-dead among all disappeared",
        "still_missing_share_flow": "Still-missing share, live RNPDNO",
        "homicide_victims_2015_2025_per100k": "Homicide victims per 100k",
        "kidnapping_victims_2015_2025_per100k": "Kidnapping victims per 100k",
        "extortion_victims_2015_2025_per100k": "Extortion victims per 100k",
        "femicide_victims_2015_2025_per100k": "Femicide victims per 100k",
        "human_trafficking_victims_2015_2025_per100k": "Human trafficking victims per 100k",
        "abduction_victims_2015_2025_per100k": "Rapto victims per 100k",
        "pibe_2024_millions_2018_mxn": "GDP 2024, constant 2018 MXN",
        "pibe_per_capita_2024_2018_mxn": "GDP per capita 2024, constant 2018 MXN",
        "corruption_prevalence_2025_per100k": "ENCIG corruption prevalence 2025",
        "corruption_prevalence_change_2023_2025": "ENCIG corruption change, 2023-2025",
    }
    rows = []
    for col, label in variables.items():
        sub = state[["confidential_share", col]].replace([np.inf, -np.inf], np.nan).dropna()
        rows.append(
            {
                "variable": col,
                "label": label,
                "n_states": len(sub),
                "pearson_r": sub["confidential_share"].corr(sub[col], method="pearson"),
                "spearman_r": sub["confidential_share"].rank().corr(sub[col].rank()),
            }
        )
    corr = pd.DataFrame(rows)
    corr["abs_spearman_r"] = corr["spearman_r"].abs()
    corr = corr.sort_values("abs_spearman_r", ascending=False)
    corr.to_csv(OUT_CORR, index=False)
    return corr


def write_correlation_figure(corr: pd.DataFrame) -> None:
    plot = corr.sort_values("spearman_r").copy()

    plt.rcParams.update(
        {
            "figure.dpi": 130,
            "savefig.dpi": 130,
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": MUTED,
            "axes.titleweight": "bold",
            "axes.titlecolor": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
        }
    )

    fig, ax = plt.subplots(figsize=(9, 6.2))
    colors = [RED if v > 0 else BLUE for v in plot["spearman_r"]]
    ax.barh(plot["label"], plot["spearman_r"], color=colors)
    ax.axvline(0, color=INK, linewidth=1)
    ax.set_title("Which available variables move with confidential-record share?")
    ax.set_xlabel("Spearman rank correlation with confidential share")
    ax.set_xlim(-1, 1)
    for i, row in enumerate(plot.itertuples(index=False)):
        ax.text(row.spearman_r, i, f" {row.spearman_r:+.2f}", va="center", fontsize=8)
    ax.text(
        0,
        -0.16,
        "Rank correlations, not causal estimates. Useful for finding patterns worth investigating.",
        transform=ax.transAxes,
        fontsize=8,
        color=MUTED,
    )
    fig.tight_layout()
    fig.savefig(CORR_FIG, bbox_inches="tight")
    plt.close(fig)


def write_clue_model(state: pd.DataFrame) -> pd.DataFrame:
    predictors = [
        "log_total_records",
        "tasa_100k",
        "no_localizada_share_known",
        "resolution_share",
        "located_dead_share_all_disappeared",
        "homicide_victims_2015_2025_per100k",
        "kidnapping_victims_2015_2025_per100k",
        "extortion_victims_2015_2025_per100k",
        "pibe_per_capita_2024_2018_mxn",
        "corruption_prevalence_2025_per100k",
    ]

    labels = {
        "log_total_records": "Scale: log unresolved records",
        "tasa_100k": "Unresolved records per 100k",
        "no_localizada_share_known": "No-localizada share among known",
        "resolution_share": "Resolution share, live RNPDNO",
        "located_dead_share_all_disappeared": "Located-dead among all disappeared",
        "homicide_victims_2015_2025_per100k": "Homicide victims per 100k",
        "kidnapping_victims_2015_2025_per100k": "Kidnapping victims per 100k",
        "extortion_victims_2015_2025_per100k": "Extortion victims per 100k",
        "pibe_per_capita_2024_2018_mxn": "GDP per capita 2024",
        "corruption_prevalence_2025_per100k": "ENCIG corruption prevalence 2025",
    }

    reg = state[["confidential_share"] + predictors].replace([np.inf, -np.inf], np.nan).dropna()
    X = reg[predictors]
    Xz = (X - X.mean()) / X.std(ddof=0)
    y = reg["confidential_share"]
    yz = (y - y.mean()) / y.std(ddof=0)

    design = np.column_stack([np.ones(len(Xz)), Xz.values])
    coef = np.linalg.lstsq(design, yz.values, rcond=None)[0]
    pred = design @ coef
    r2 = 1 - ((yz.values - pred) ** 2).sum() / ((yz.values - yz.mean()) ** 2).sum()

    out = pd.DataFrame(
        {
            "variable": predictors,
            "label": [labels[p] for p in predictors],
            "standardized_coefficient": coef[1:],
            "n_states": len(reg),
            "r_squared": r2,
        }
    ).sort_values("standardized_coefficient")

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [RED if v > 0 else BLUE for v in out["standardized_coefficient"]]
    ax.barh(out["label"], out["standardized_coefficient"], color=colors)
    ax.axvline(0, color=INK, linewidth=1)
    ax.set_title("Clue model for confidential-record share")
    ax.set_xlabel("Standardized OLS coefficient")
    for i, row in enumerate(out.itertuples(index=False)):
        ax.text(
            row.standardized_coefficient,
            i,
            f" {row.standardized_coefficient:+.2f}",
            va="center",
            fontsize=8,
        )
    ax.text(
        0,
        -0.18,
        f"OLS clue model, n={len(reg)} states, R2={r2:.2f}. Not causal; small sample and omitted institutional variables.",
        transform=ax.transAxes,
        fontsize=8,
        color=MUTED,
    )
    fig.tight_layout()
    fig.savefig(COEF_FIG, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    state = build_enriched()
    write_interactive(state)
    corr = _corr_rows(state)
    write_correlation_figure(corr)
    coef = write_clue_model(state)

    print(f"Wrote {OUT_ENRICHED.relative_to(ROOT)}")
    print(f"Wrote {OUT_CORR.relative_to(ROOT)}")
    print(f"Wrote {HTML_OUT.relative_to(ROOT)}")
    print(f"Wrote {CORR_FIG.relative_to(ROOT)}")
    print(f"Wrote {COEF_FIG.relative_to(ROOT)}")
    print("\nTop rank correlations with confidential share:")
    print(corr.head(8)[["label", "n_states", "spearman_r", "pearson_r"]].to_string(index=False))
    print("\nClue model coefficients:")
    print(coef[["label", "standardized_coefficient", "n_states", "r_squared"]].to_string(index=False))


if __name__ == "__main__":
    main()
