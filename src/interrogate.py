"""
Interrogate the dataset: what are we actually counting?

Prints the diagnostics behind docs/methodology.md so the caveats stay verifiable and
re-checkable when the data is refreshed. This is not analysis — it's data forensics.

Run:  python src/interrogate.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "external" / "data.csv"
PARQUET = ROOT / "data" / "processed" / "rnpdno_clean.parquet"


def main():
    raw = pd.read_csv(RAW, dtype="string")
    df = pd.read_parquet(PARQUET)
    n = len(raw)
    line = "-" * 64
    print(f"{line}\nTOTAL ROWS: {n:,}\n{line}")

    print("\n[1] UNIT OF ANALYSIS — is one row one person?")
    print(f"    ID_VICTIMA unique: {raw['ID_VICTIMA'].nunique():,} "
          f"(duplicates: {n - raw['ID_VICTIMA'].nunique():,})")

    print("\n[2] STOCK vs FLOW — is there a 'located' status?")
    print(raw["ESTATUS_VICTIMA"].value_counts(dropna=False).to_string().replace("\n", "\n    "))
    print("    -> No 'located' category => this is the STILL-MISSING stock, not all disappearances.")

    print("\n[3] REDACTION — is CONFIDENCIAL all-or-nothing?")
    conf, nodate = df["confidencial"], df["FECHA_DESAPARICION"].isna()
    print(f"    confidential: {conf.mean():.1%} | no disappearance date: {nodate.mean():.1%}")
    print(f"    of confidential w/o date: {nodate[conf].mean():.1%} | "
          f"of non-confidential w/o date: {nodate[~conf].mean():.1%}")

    print("\n[4] DATE FIELDS — is registration lag informative?")
    lag = (df["FECHA_REGISTRO"] - df["FECHA_DESAPARICION"]).dt.days
    lag = lag[lag.between(0, 365 * 40)]
    print(f"    lag days (n={len(lag):,}): median={lag.median():.0f}, mean={lag.mean():.0f}, "
          f"same-year={ (lag <= 365).mean():.1%}  -> not independently useful")

    print("\n[5] CATEGORY MIX — DESAPARECIDA vs NO LOCALIZADA by sex (non-confidential):")
    sub = df[~conf]
    print("    " + pd.crosstab(sub["ESTATUS_VICTIMA"], sub["SEXO"]).to_string().replace("\n", "\n    "))

    print(f"\n[6] COVERAGE OF KEY FIELDS (share of all {n:,} rows):")
    for col in ["SEXO", "ESTATUS_VICTIMA", "FECHA_DESAPARICION", "edad_desaparicion", "ENTIDAD"]:
        print(f"    {col:<20} {df[col].notna().mean():.1%}")

    print(f"\n{line}\nSee docs/methodology.md for what these mean for each chart.\n{line}")


if __name__ == "__main__":
    main()
