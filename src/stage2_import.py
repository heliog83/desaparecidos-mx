"""Map the CNB / Quinto Elemento clandestine-grave registry into the Stage-2 schema.

WHAT THIS DATA IS — read before using it for anything
-----------------------------------------------------
This is the **state's own registry of clandestine graves**, published by Quinto
Elemento Lab from CNB records. It carries **no attribution**: it does not say who
located a grave. Every row therefore lands as ``led_by='state'`` and
``collective='unknown'`` — that is an artifact of the source having no attribution
field, *not* a finding that the state located these graves.

**It cannot answer the Stage-2 question.** Stage 2 asks how much recovery work is
done by collectives versus the state; a source with no attribution column is silent
on exactly that. This import is a geographic and volumetric baseline to code
journalism against. Never label it, chart it, or caption it as madres buscadoras
work. See docs/stage2-schema.md.

Unit of analysis differs from the hand-coded file, too. ``clandestine_finds.csv``
is one row per *find event*. Here one row is one *registry grave record*: 1,499 of
the 4,483 rows sit in exact-duplicate groups (same municipality, same date, same
count), which are genuinely separate graves, not data errors. Rows from the two
files are distinguished by ``source_type`` and must not be pooled naively.

Run:
    python src/stage2_import.py                   # uses the committed coord cache
    python src/stage2_import.py --refresh-coords  # re-fetch coords from the network
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "external" / "20231006-registro-fosas-cnb-quintoelab.csv"
OUTPUT = ROOT / "data" / "stage2" / "clandestine_finds_imported.csv"
COORD_CACHE = ROOT / "data" / "stage2" / "municipality_coords.csv"

COORD_URL = (
    "https://raw.githubusercontent.com/eduardoarandah/"
    "coordenadas-estados-municipios-localidades-de-mexico-json/master/data.csv"
)

SOURCE_OUTLET = "CNB/Quinto Elemento Lab"
SOURCE_URL = "https://quintoelab.org/project/fosas-clandestinas-nuevo-mapa-mexico"
CONSULTED = "2023-10-06"

# The project's canonical state vocabulary: the `entidad` values in
# data/publication_freezes/*/derived/state_opacity_enriched.csv. Accented, uppercase.
# The Stage-2 schema requires matching it so Stage-2 rows join to Stage-1 tables.
# An earlier version of this script stripped accents and expanded short names
# ("COAHUILA DE ZARAGOZA", "MEXICO"), which silently broke that join for 7 states.
CANONICAL_STATES = {
    "AGUASCALIENTES", "BAJA CALIFORNIA", "BAJA CALIFORNIA SUR", "CAMPECHE",
    "CHIAPAS", "CHIHUAHUA", "COAHUILA", "COLIMA", "CIUDAD DE MÉXICO", "DURANGO",
    "ESTADO DE MÉXICO", "GUANAJUATO", "GUERRERO", "HIDALGO", "JALISCO",
    "MICHOACÁN", "MORELOS", "NAYARIT", "NUEVO LEÓN", "OAXACA", "PUEBLA",
    "QUERÉTARO", "QUINTANA ROO", "SAN LUIS POTOSÍ", "SINALOA", "SONORA",
    "TABASCO", "TAMAULIPAS", "TLAXCALA", "VERACRUZ", "YUCATÁN", "ZACATECAS",
}

# Source spelling -> canonical. Keyed on the accent-stripped uppercase form so the
# source's own accenting does not matter.
STATE_ALIASES = {
    "COAHUILA DE ZARAGOZA": "COAHUILA",
    "DISTRITO FEDERAL": "CIUDAD DE MÉXICO",
    "CIUDAD DE MEXICO": "CIUDAD DE MÉXICO",
    "MEXICO": "ESTADO DE MÉXICO",
    "MICHOACAN": "MICHOACÁN",
    "MICHOACAN DE OCAMPO": "MICHOACÁN",
    "NUEVO LEON": "NUEVO LEÓN",
    "QUERETARO": "QUERÉTARO",
    "QUERETARO DE ARTEAGA": "QUERÉTARO",
    "SAN LUIS POTOSI": "SAN LUIS POTOSÍ",
    "VERACRUZ DE IGNACIO DE LA LLAVE": "VERACRUZ",
    "YUCATAN": "YUCATÁN",
    # The registry's own "unknown state" marker. Kept verbatim; it is a real
    # category, and collapsing it into a state would invent a location.
    "SE DESCONOCE": "SE DESCONOCE",
}


def strip_accents(value: str) -> str:
    return unicodedata.normalize("NFKD", value).encode("ASCII", "ignore").decode()


def normalize_state(state) -> str:
    if pd.isna(state):
        return "SE DESCONOCE"
    raw = str(state).strip().upper()
    folded = strip_accents(raw)
    if raw in CANONICAL_STATES:
        return raw
    if folded in STATE_ALIASES:
        return STATE_ALIASES[folded]
    # Accent-insensitive match against the canonical set.
    for canon in CANONICAL_STATES:
        if strip_accents(canon) == folded:
            return canon
    raise SystemExit(
        f"FAIL: unmapped state {state!r}. Add it to STATE_ALIASES rather than "
        f"letting an unjoinable value into the Stage-2 file."
    )


def refresh_coords(needed: set[int]) -> pd.DataFrame:
    """Fetch municipal-seat coordinates and cache the subset this dataset needs."""
    print(f"fetching municipal coordinates from {COORD_URL}")
    geo = pd.read_csv(
        COORD_URL,
        dtype={"CVE_ENT": str, "CVE_MUN": str, "CVE_LOC": str},
        low_memory=False,
    )
    # CVE_LOC 0001 is the cabecera municipal — the municipal seat, i.e. the town
    # centre. NOT the location of any grave. See the column naming below.
    seats = geo[geo["CVE_LOC"] == "0001"].copy()
    seats["cve_geo"] = (
        seats["CVE_ENT"].str.zfill(2) + seats["CVE_MUN"].str.zfill(3)
    ).astype(int)
    seats = seats[seats["cve_geo"].isin(needed)]
    out = (
        seats[["cve_geo", "LAT_DEC", "LON_DEC"]]
        .rename(columns={"LAT_DEC": "municipality_lat", "LON_DEC": "municipality_lon"})
        .drop_duplicates(subset="cve_geo")
        .sort_values("cve_geo")
    )
    COORD_CACHE.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(COORD_CACHE, index=False)
    print(f"wrote {COORD_CACHE.relative_to(ROOT)} ({len(out)} municipal seats)")
    return out


def load_coords(needed: set[int], refresh: bool) -> pd.DataFrame:
    if refresh:
        return refresh_coords(needed)
    if not COORD_CACHE.exists():
        raise SystemExit(
            f"FAIL: {COORD_CACHE.relative_to(ROOT)} is missing. Run with "
            f"--refresh-coords to rebuild it from the network.\n"
            f"(The previous version of this script fetched silently and fell back "
            f"to empty coordinates on any network error, producing a file that "
            f"looked fine but had no geography.)"
        )
    return pd.read_csv(COORD_CACHE)


def build_event_ids(df: pd.DataFrame) -> pd.Series:
    """Stable ids derived from row content, not from row order.

    The previous scheme numbered rows sequentially (CNB-2023-00001...), so any
    upstream re-sort or revision silently relabelled every event. These ids are a
    hash of the identifying fields plus an occurrence index that disambiguates the
    genuinely-duplicate grave records.
    """
    key = df[["cve_geo", "anio", "fecha", "graves"]].astype(str).agg("|".join, axis=1)
    digest = key.map(lambda k: hashlib.sha1(k.encode()).hexdigest()[:10])
    occurrence = key.groupby(key).cumcount() + 1
    return "CNB2023-" + digest + "-" + occurrence.astype(str)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh-coords",
        action="store_true",
        help="re-fetch municipal-seat coordinates and rewrite the committed cache",
    )
    args = parser.parse_args()

    if not SOURCE.exists():
        raise SystemExit(
            f"FAIL: {SOURCE.relative_to(ROOT)} is missing (gitignored raw source). "
            f"Download it from {SOURCE_URL}"
        )

    src = pd.read_csv(SOURCE)
    df = pd.DataFrame()
    df["cve_geo"] = pd.to_numeric(src["Cve_geo"], errors="coerce").astype("Int64")
    df["anio"] = pd.to_numeric(src["Año"], errors="coerce").astype("Int64")
    df["fecha"] = src["Fecha_hallazgo"].astype(str).replace({"nan": "", "NA": ""})
    df["graves"] = pd.to_numeric(src["Total_fosas"], errors="coerce").astype("Int64")

    # Deterministic order so ids do not depend on how the source happened to sort.
    df["municipality"] = src["Municipio"]
    df["state"] = src["Estado"].apply(normalize_state)
    df = df.sort_values(
        ["state", "municipality", "cve_geo", "anio", "fecha", "graves"],
        kind="mergesort",
        na_position="last",
    ).reset_index(drop=True)

    out = pd.DataFrame()
    out["event_id"] = build_event_ids(df)

    has_day = df["fecha"] != ""
    has_year = df["anio"].notna()
    out["date"] = ""
    out.loc[has_year, "date"] = df.loc[has_year, "anio"].astype(str) + "-01-01"
    out.loc[has_day, "date"] = df.loc[has_day, "fecha"]
    out["date_precision"] = "approx"
    out.loc[has_year, "date_precision"] = "year"
    out.loc[has_day, "date_precision"] = "day"

    out["state"] = df["state"]
    out["municipality"] = df["municipality"]

    # No attribution exists in this source. Both values record that absence.
    out["collective"] = "unknown"
    out["led_by"] = "state"

    out["graves_found"] = df["graves"]
    out["bodies_found"] = pd.NA
    out["remains_bags"] = pd.NA
    out["persons_identified"] = pd.NA

    out["source_outlet"] = SOURCE_OUTLET
    out["source_url"] = SOURCE_URL
    out["consulted"] = CONSULTED
    out["source_type"] = "registry"

    # Confidence describes the TEMPORAL RESOLUTION of the registry record, not
    # doubt about whether the grave exists. A blanket 'high' — as the previous
    # version wrote for all 4,483 rows, including 92 with no date at all — asserted
    # a precision the source does not have.
    out["confidence"] = "low"
    out.loc[has_year, "confidence"] = "med"
    out.loc[has_day, "confidence"] = "high"

    out["notes"] = "CNB clandestine-grave registry record; no attribution in source"

    # Municipal-seat centroids: the town centre of the municipality, repeated for
    # every grave in it. These are NOT grave coordinates and must never be drawn
    # as pins on a "grave locations" map. The column names say so on purpose.
    coords = load_coords(set(df["cve_geo"].dropna().astype(int)), args.refresh_coords)
    df_c = df[["cve_geo"]].astype("Int64").merge(
        coords.astype({"cve_geo": "Int64"}), on="cve_geo", how="left"
    )
    out["municipality_lat"] = df_c["municipality_lat"].values
    out["municipality_lon"] = df_c["municipality_lon"].values

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT, index=False)

    unjoinable = sorted(set(out["state"]) - CANONICAL_STATES - {"SE DESCONOCE"})
    missing_geo = int(out["municipality_lat"].isna().sum())
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(out):,} registry grave records")
    print(f"  graves_found total: {int(out['graves_found'].sum()):,}")
    print(f"  date precision: {out['date_precision'].value_counts().to_dict()}")
    print(f"  states unjoinable to Stage-1: {unjoinable or 'none'}")
    print(f"  rows without municipal-seat coordinates: {missing_geo}")
    print("  attribution: none in source — every row is led_by='state' by default,")
    print("  which is the absence of a field, not evidence about who searched.")
    if unjoinable:
        sys.exit(1)


if __name__ == "__main__":
    main()
