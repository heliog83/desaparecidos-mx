"""
Merge Stage 1 baseline data with new INEGI datasets (ENCIG 2025 and PIBE 2024).

This script:
1. Calculates the confidential_share per state from the RNPDNO baseline.
2. Merges this with state rates (population, disappearances).
3. Merges the result with corruption prevalence and economic capacity data.
4. Generates a unified dataset at `data/processed/state_correlations.csv`.
5. Plots two exploratory scatter charts (redaction vs corruption, redaction vs economic capacity) using Altair.

Run: .venv/bin/python src/merge_correlations.py
"""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
import altair as alt

ROOT = Path(__file__).resolve().parents[1]

# Inputs
PARQUET = ROOT / "data" / "processed" / "rnpdno_clean.parquet"
RATES_CSV = ROOT / "data" / "processed" / "state_rates.csv"
ENCIG_CSV = ROOT / "data" / "external" / "inegi" / "encig_corruption_prevalence_2025_extracted.csv"
PIBE_CSV = ROOT / "data" / "external" / "inegi" / "pibe_state_2024_extracted.csv"

# Outputs
OUT_CSV = ROOT / "data" / "processed" / "state_correlations.csv"
FIGDIR = ROOT / "reports" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

# Robust mapping for state names to cve_ent (2-digit code)
STATE_TO_CVE = {
    'AGUASCALIENTES': '01',
    'BAJA CALIFORNIA': '02',
    'BAJA CALIFORNIA SUR': '03',
    'CAMPECHE': '04',
    'COAHUILA': '05',
    'COAHUILA DE ZARAGOZA': '05',
    'COLIMA': '06',
    'CHIAPAS': '07',
    'CHIHUAHUA': '08',
    'CIUDAD DE MEXICO': '09',
    'DURANGO': '10',
    'GUANAJUATO': '11',
    'GUERRERO': '12',
    'HIDALGO': '13',
    'JALISCO': '14',
    'ESTADO DE MEXICO': '15',
    'MEXICO': '15',
    'MICHOACAN': '16',
    'MICHOACAN DE OCAMPO': '16',
    'MORELOS': '17',
    'NAYARIT': '18',
    'NUEVO LEON': '19',
    'OAXACA': '20',
    'PUEBLA': '21',
    'QUERETARO': '22',
    'QUINTANA ROO': '23',
    'SAN LUIS POTOSI': '24',
    'SINALOA': '25',
    'SONORA': '26',
    'TABASCO': '27',
    'TAMAULIPAS': '28',
    'TLAXCALA': '29',
    'VERACRUZ': '30',
    'VERACRUZ DE IGNACIO DE LA LLAVE': '30',
    'YUCATAN': '31',
    'ZACATECAS': '32',
}


def build_opacity_rates() -> pd.DataFrame:
    df = pd.read_parquet(PARQUET)
    df["cve_ent"] = df["CVE_ENT"].astype("string").str.zfill(2)
    
    state_opacity = df.groupby("cve_ent").agg(
        total_records=("confidencial", "size"),
        confidential_records=("confidencial", "sum"),
    ).reset_index()
    
    state_opacity["confidential_share"] = state_opacity["confidential_records"] / state_opacity["total_records"]
    return state_opacity


def plot_scatter_altair(df: pd.DataFrame, x_col: str, y_col: str, title: str, x_title: str, y_title: str, filename: str):
    df_plot = df.copy()
    
    # Identify top outliers to label
    label_states = set(
        df_plot.nlargest(3, y_col)["entidad"]
    ).union(df_plot.nlargest(3, x_col)["entidad"])
    
    df_plot["label"] = df_plot["entidad"].where(df_plot["entidad"].isin(label_states), "")
    
    chart = alt.Chart(df_plot).mark_circle(size=80, opacity=0.8, color="#3b5b7a", stroke="white", strokeWidth=0.6).encode(
        x=alt.X(f"{x_col}:Q", title=x_title),
        y=alt.Y(f"{y_col}:Q", title=y_title, axis=alt.Axis(format='%')),
        tooltip=["entidad", x_col, y_col]
    ).properties(
        title=title,
        width=550,
        height=400
    )
    
    text = alt.Chart(df_plot).mark_text(
        align='left',
        baseline='middle',
        dx=7,
        fontSize=10,
        color="#2b2b2b"
    ).encode(
        x=f"{x_col}:Q",
        y=f"{y_col}:Q",
        text='label'
    )
    
    final_chart = chart + text
    
    path = FIGDIR / filename
    final_chart.save(str(path))
    print(f"  wrote {path.relative_to(ROOT)}")


def main():
    print("Building confidentiality rates by state...")
    opacity_df = build_opacity_rates()
    
    print("Loading state rates baseline...")
    rates_df = pd.read_csv(RATES_CSV, dtype={"cve_ent": "string"})
    rates_df["cve_ent"] = rates_df["cve_ent"].str.zfill(2)
    
    print("Loading INEGI datasets...")
    encig = pd.read_csv(ENCIG_CSV)
    pibe = pd.read_csv(PIBE_CSV)
    
    # Map INEGI datasets to cve_ent
    encig["cve_ent"] = encig["state_key"].map(STATE_TO_CVE)
    if encig["cve_ent"].isna().any():
        print("WARNING: Unmapped ENCIG state keys:", encig[encig["cve_ent"].isna()]["state_key"].unique())
        
    pibe["cve_ent"] = pibe["state_key"].map(STATE_TO_CVE)
    if pibe["cve_ent"].isna().any():
        print("WARNING: Unmapped PIBE state keys:", pibe[pibe["cve_ent"].isna()]["state_key"].unique())
        
    # Select desired columns to merge
    encig_sub = encig[["cve_ent", "corruption_prevalence_2025_per100k"]]
    pibe_sub = pibe[["cve_ent", "pibe_per_capita_2024_2018_mxn"]]
    
    # Merge all
    merged = rates_df.merge(opacity_df, on="cve_ent", how="left")
    merged = merged.merge(encig_sub, on="cve_ent", how="left")
    merged = merged.merge(pibe_sub, on="cve_ent", how="left")
    
    # Save output
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT_CSV, index=False)
    print(f"\nSaved unified dataset to {OUT_CSV.relative_to(ROOT)}")
    print(f"Dataset shape: {merged.shape} (Expected 32 rows)")
    
    # Check for NaNs
    nans = merged[["corruption_prevalence_2025_per100k", "pibe_per_capita_2024_2018_mxn"]].isna().sum()
    if nans.sum() > 0:
        print("\nWARNING: Found missing values in merged dataset:")
        print(nans)
    
    # Generate scatter plots
    print("\nGenerating exploratory Altair plots...")
    plot_scatter_altair(
        merged,
        x_col="corruption_prevalence_2025_per100k",
        y_col="confidential_share",
        title="Opacity vs. Corruption Prevalence (2025)",
        x_title="Corruption Victims per 100k (ENCIG)",
        y_title="Share marked CONFIDENCIAL",
        filename="24_opacity_vs_corruption.html"
    )
    
    plot_scatter_altair(
        merged,
        x_col="pibe_per_capita_2024_2018_mxn",
        y_col="confidential_share",
        title="Opacity vs. Economic Capacity (PIBE 2024)",
        x_title="PIBE per capita (2018 MXN)",
        y_title="Share marked CONFIDENCIAL",
        filename="25_opacity_vs_pibe.html"
    )


if __name__ == "__main__":
    main()
