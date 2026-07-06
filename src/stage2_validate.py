"""
Stage 2 — load & validate the hand-coded clandestine-finds dataset.

Enforces the docs/stage2-schema.md contract (columns, enums, types) and prints a quick summary
so the dataset stays honest as it grows. This is a sample, not a census — see the schema doc.

Run:  python src/stage2_validate.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "stage2" / "clandestine_finds.csv"

REQUIRED = ["event_id", "date", "date_precision", "state", "municipality", "collective",
            "led_by", "graves_found", "bodies_found", "remains_bags", "persons_identified",
            "source_outlet", "source_url", "consulted", "confidence", "notes"]
ENUMS = {
    "date_precision": {"day", "month", "year", "approx"},
    "led_by": {"collective", "state", "joint", "unknown"},
    "confidence": {"high", "med", "low"},
}
INT_COLS = ["graves_found", "bodies_found", "remains_bags", "persons_identified"]


def validate(df: pd.DataFrame) -> list[str]:
    errs = []
    missing_cols = [c for c in REQUIRED if c not in df.columns]
    if missing_cols:
        return [f"missing columns: {missing_cols}"]
    if df["event_id"].duplicated().any():
        errs.append(f"duplicate event_id: {df.loc[df['event_id'].duplicated(),'event_id'].tolist()}")
    for col, allowed in ENUMS.items():
        bad = set(df[col].dropna()) - allowed
        if bad:
            errs.append(f"{col}: invalid values {bad} (allowed {allowed})")
    for col in INT_COLS:
        coerced = pd.to_numeric(df[col], errors="coerce")
        bad = df[col].notna() & coerced.isna()
        if bad.any():
            errs.append(f"{col}: non-numeric in rows {df.index[bad].tolist()}")
    if df["source_url"].isna().any() or (df["source_url"] == "").any():
        errs.append("every row needs a source_url")
    return errs


def main():
    if not CSV.exists():
        raise FileNotFoundError(f"Missing {CSV} — see docs/stage2-schema.md")
    df = pd.read_csv(CSV)
    errs = validate(df)
    print(f"Loaded {len(df)} find-events from {CSV.relative_to(ROOT)}")
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print("  -", e)
    else:
        print("schema OK ✓")

    print("\nBy attribution (led_by):")
    print(df["led_by"].value_counts().to_string())
    print("\nReported totals (LOWER BOUNDS — sample, not census):")
    for col in ["graves_found", "bodies_found"]:
        print(f"  {col}: {int(pd.to_numeric(df[col], errors='coerce').sum())}")
    print(f"\nConfidence mix: {df['confidence'].value_counts().to_dict()}")
    print("\nReminder: these are illustrative seeds. Expand from Quinto Elemento / FUNDENL / news"
          " before drawing any conclusion. Never present as the true total.")


if __name__ == "__main__":
    main()
