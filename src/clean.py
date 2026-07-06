"""
Clean the raw RNPDNO microdata into an analysis-ready table.

Input:  data/external/data.csv      (one row per victim, from the RNPDNO mirror)
Output: data/processed/rnpdno_clean.parquet

Key decisions (documented because they shape every downstream number):
- "CONFIDENCIAL" is the registry's redaction marker. We convert it to missing (NaN) per
  field AND keep a boolean `confidencial` flag (rows where the core fields are redacted),
  because the *share of redacted records* is itself a finding.
- Dates are coerced; impossible values (year < 1950, or in the future) become NaT.
- age_at_disappearance is derived and clipped to [0, 110]; anything outside is set NaN.

Run:  python src/clean.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "external" / "data.csv"
OUT = ROOT / "data" / "processed" / "rnpdno_clean.parquet"

CONF = "CONFIDENCIAL"
DATE_COLS = ["FECHA_NACIMIENTO", "FECHA_DESAPARICION", "FECHA_REGISTRO"]


def _parse_date(s: pd.Series) -> pd.Series:
    s = s.replace(CONF, np.nan)
    d = pd.to_datetime(s, errors="coerce")
    # Drop impossible dates: before 1950 or in the future.
    bad = (d.dt.year < 1950) | (d > pd.Timestamp.now())
    return d.mask(bad)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Redaction flag: rows where status/sex are withheld.
    df["confidencial"] = (df["ESTATUS_VICTIMA"] == CONF) | (df["SEXO"] == CONF)

    # Normalize categoricals (CONFIDENCIAL -> missing).
    for col in ["SEXO", "ESTATUS_VICTIMA", "ENTIDAD", "MUNICIPIO", "ORIGEN_REPORTE"]:
        df[col] = df[col].replace(CONF, np.nan).astype("string").str.strip()
    df["SEXO"] = df["SEXO"].str.capitalize()  # Hombre / Mujer / Indeterminado

    # Dates.
    for col in DATE_COLS:
        df[col] = _parse_date(df[col])

    # Derived time fields off the disappearance date.
    df["anio_desaparicion"] = df["FECHA_DESAPARICION"].dt.year.astype("Int64")
    df["mes_desaparicion"] = df["FECHA_DESAPARICION"].dt.to_period("M").astype("string")

    # Age at disappearance.
    age = (df["FECHA_DESAPARICION"] - df["FECHA_NACIMIENTO"]).dt.days / 365.25
    df["edad_desaparicion"] = age.where((age >= 0) & (age <= 110)).round(1)
    df["grupo_edad"] = pd.cut(
        df["edad_desaparicion"],
        bins=[0, 12, 17, 29, 44, 59, 110],
        labels=["0-12", "13-17", "18-29", "30-44", "45-59", "60+"],
    )

    return df


def main() -> pd.DataFrame:
    if not RAW_CSV.exists():
        raise FileNotFoundError(f"Missing {RAW_CSV}. Run the fetch step first.")
    raw = pd.read_csv(RAW_CSV, dtype="string")
    df = clean(raw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)

    print(f"Cleaned {len(df):,} records -> {OUT.relative_to(ROOT)}")
    print(f"  redacted (confidencial): {df['confidencial'].mean():.1%}")
    print(f"  with valid disappearance date: {df['FECHA_DESAPARICION'].notna().mean():.1%}")
    print(f"  with usable age: {df['edad_desaparicion'].notna().mean():.1%}")
    return df


if __name__ == "__main__":
    main()
