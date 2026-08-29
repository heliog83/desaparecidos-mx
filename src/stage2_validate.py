"""
Stage 2 — load & validate a clandestine-finds dataset.

Enforces the docs/stage2-schema.md contract (columns, enums, types, state
vocabulary) and prints a provenance-aware summary so the dataset stays honest as it
grows. This is a sample, not a census — see the schema doc.

Two provenances share the schema and must not be read the same way:

* ``source_type='journalism'`` — hand-coded find events. Carries real attribution,
  so ``led_by`` means something. Tiny and non-random.
* ``source_type='registry'``   — the CNB/Quinto Elemento grave registry. Has NO
  attribution field, so every row is ``led_by='state'`` by default. That is the
  absence of a column, not a finding about who searched. Reporting an attribution
  breakdown over these rows would manufacture a result.

Run:  python src/stage2_validate.py [path/to/file.csv]
Exits non-zero when validation fails.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "stage2" / "clandestine_finds.csv"

REQUIRED = ["event_id", "date", "date_precision", "state", "municipality", "collective",
            "led_by", "graves_found", "bodies_found", "remains_bags", "persons_identified",
            "source_outlet", "source_url", "consulted", "source_type", "confidence", "notes"]
ENUMS = {
    "date_precision": {"day", "month", "year", "approx"},
    "led_by": {"collective", "state", "joint", "unknown"},
    "confidence": {"high", "med", "low"},
    "source_type": {"journalism", "registry"},
}
INT_COLS = ["graves_found", "bodies_found", "remains_bags", "persons_identified"]

# Must match `entidad` in the Stage-1 tables, or Stage-2 rows cannot be joined to
# Stage-1 by state — which is the whole point of the schema's state rule.
CANONICAL_STATES = {
    "AGUASCALIENTES", "BAJA CALIFORNIA", "BAJA CALIFORNIA SUR", "CAMPECHE",
    "CHIAPAS", "CHIHUAHUA", "COAHUILA", "COLIMA", "CIUDAD DE MÉXICO", "DURANGO",
    "ESTADO DE MÉXICO", "GUANAJUATO", "GUERRERO", "HIDALGO", "JALISCO",
    "MICHOACÁN", "MORELOS", "NAYARIT", "NUEVO LEÓN", "OAXACA", "PUEBLA",
    "QUERÉTARO", "QUINTANA ROO", "SAN LUIS POTOSÍ", "SINALOA", "SONORA",
    "TABASCO", "TAMAULIPAS", "TLAXCALA", "VERACRUZ", "YUCATÁN", "ZACATECAS",
    "SE DESCONOCE",
}


def validate(df: pd.DataFrame) -> list[str]:
    errs = []
    missing_cols = [c for c in REQUIRED if c not in df.columns]
    if missing_cols:
        return [f"missing columns: {missing_cols}"]
    if df["event_id"].duplicated().any():
        dupes = df.loc[df["event_id"].duplicated(), "event_id"].tolist()
        errs.append(f"duplicate event_id: {dupes[:10]}{'...' if len(dupes) > 10 else ''}")
    for col, allowed in ENUMS.items():
        bad = set(df[col].dropna()) - allowed
        if bad:
            errs.append(f"{col}: invalid values {bad} (allowed {allowed})")
    for col in INT_COLS:
        coerced = pd.to_numeric(df[col], errors="coerce")
        bad = df[col].notna() & coerced.isna()
        if bad.any():
            errs.append(f"{col}: non-numeric in rows {df.index[bad].tolist()[:10]}")
    if df["source_url"].isna().any() or (df["source_url"] == "").any():
        errs.append("every row needs a source_url")

    unjoinable = sorted(set(df["state"].dropna()) - CANONICAL_STATES)
    if unjoinable:
        errs.append(
            f"state values that will not join to Stage-1 `entidad`: {unjoinable}"
        )

    # A dated row must actually carry a date; an undated one must not claim precision.
    dated = df["date_precision"].isin({"day", "month", "year"})
    blank = df["date"].isna() | (df["date"].astype(str).str.strip() == "")
    if (dated & blank).any():
        errs.append(
            f"{int((dated & blank).sum())} rows claim date_precision "
            f"day/month/year but have no date"
        )
    return errs


def summarize(df: pd.DataFrame) -> None:
    kinds = df["source_type"].value_counts().to_dict()
    print(f"\nProvenance: {kinds}")

    coded = df[df["source_type"] == "journalism"]
    registry = df[df["source_type"] == "registry"]

    if not coded.empty:
        print("\nAttribution (led_by) — journalism-coded rows only, where it is real:")
        print(coded["led_by"].value_counts().to_string())
    if not registry.empty:
        print(
            f"\n{len(registry):,} registry rows excluded from the attribution "
            f"breakdown: that source has no attribution field, so their "
            f"led_by='state' records a missing column, not a searcher."
        )

    print("\nReported totals (LOWER BOUNDS — sample, not census):")
    for label, subset in (("journalism", coded), ("registry", registry)):
        if subset.empty:
            continue
        graves = int(pd.to_numeric(subset["graves_found"], errors="coerce").sum())
        bodies = int(pd.to_numeric(subset["bodies_found"], errors="coerce").sum())
        print(f"  {label:11s} graves_found: {graves:>6,}   bodies_found: {bodies:>6,}")

    print(f"\nConfidence mix: {df['confidence'].value_counts().to_dict()}")

    if not coded.empty:
        print(
            "\nReminder: the journalism rows are illustrative seeds. Expand from "
            "Quinto Elemento / FUNDENL / news before drawing any conclusion."
        )
    if not registry.empty:
        print(
            "Reminder: the registry rows are a geographic baseline, not evidence "
            "about collectives. Never caption them as madres buscadoras work."
        )
    print("Never present either total as the true number of graves.")


def main() -> None:
    target_csv = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_CSV
    if not target_csv.exists():
        raise SystemExit(f"Missing {target_csv} — see docs/stage2-schema.md")
    df = pd.read_csv(target_csv)
    try:
        shown = target_csv.relative_to(ROOT)
    except ValueError:
        shown = target_csv
    print(f"Loaded {len(df):,} rows from {shown}")

    errs = validate(df)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print("  -", e)
        summarize(df)
        sys.exit(1)

    print("schema OK ✓")
    summarize(df)


if __name__ == "__main__":
    main()
