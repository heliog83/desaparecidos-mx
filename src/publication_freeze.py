"""Build an immutable, dated publication-data freeze and headline-number audit.

The article uses two RNPDNO source streams that must not be presented as if they
share a cutoff date:

* record-level still-missing microdata: pinned mirror snapshot, 2025-12-02;
* aggregate outcomes (including located people): live RNPDNO API, captured now.

This script copies the record-level source, fetches the aggregate API into a new
date-stamped directory, derives the publication tables there, hashes every source,
and writes a Markdown audit. It refuses to overwrite an existing freeze.

Run:
    python src/publication_freeze.py --date YYYY-MM-DD
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import clean as cleaner
import fetch_flow


ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "data" / "external" / "data.csv"
CONSENT_PDF = (
    ROOT
    / "data"
    / "external"
    / "legal_docs"
    / "Oficio_SEGOB_CNBP_1349_2020_consulta_INAI.pdf"
)
VERSION_PANEL = ROOT / "data" / "processed" / "confidencial_panel.csv"
MIRROR_HISTORY = ROOT / "data" / "external" / "mirror_history"
FREEZE_ROOT = ROOT / "data" / "publication_freezes"
REPORTS = ROOT / "reports"

MIRROR_UPSTREAM_DATE = "2025-12-02"
MIRROR_UPSTREAM_COMMIT = "666b3e7605"

CONSENT = {
    "total": 73_388,
    "no_information": 56_803,
    "with_information": 16_585,
    "family_reporters": 14_295,
    "anonymous_or_unclear_reporters": 2_290,
    "family_refused_publication": 7_478,
    "family_agreed_to_publication": 6_717,
    # The oficio's two family-publication subtotals add to 14,195, not 14,295.
    # Preserve the 100-record source gap rather than silently assigning it.
    "family_publication_status_unaccounted": 100,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fetch_live_flow(raw_dir: Path, derived_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Fetch the same low-volume public endpoints as fetch_flow.py into the freeze."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    derived_dir.mkdir(parents=True, exist_ok=True)
    session = fetch_flow._session()

    response = session.post(
        fetch_flow.BASE + "Sociodemografico/Totales",
        data=fetch_flow._params("0"),
        timeout=40,
    )
    response.raise_for_status()
    totals = response.json()
    (raw_dir / "totales.json").write_text(
        json.dumps(totals, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    pd.Series(
        {
            k: fetch_flow._to_int(v) if "Porcentaje" not in k else v
            for k, v in totals.items()
        }
    ).to_csv(derived_dir / "flow_totales.csv")

    year_columns: dict[str, pd.Series] = {}
    state_columns: dict[str, pd.Series] = {}
    for status_name, status_code in fetch_flow.STATUS.items():
        for endpoint_name, endpoint_path in fetch_flow.ENDPOINTS.items():
            time.sleep(1.2)
            response = session.post(
                fetch_flow.BASE + endpoint_path,
                data=fetch_flow._params(status_code),
                timeout=40,
            )
            response.raise_for_status()
            if response.text[:1] not in "{[":
                raise RuntimeError(f"Non-JSON response for {endpoint_name}/{status_name}")
            payload = response.json()
            (raw_dir / f"{endpoint_name}_{status_name}.json").write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            series = fetch_flow._chart_to_totals(payload)
            target = year_columns if endpoint_name == "by_year" else state_columns
            target[status_name] = series

    by_year = pd.DataFrame(year_columns)
    by_state = pd.DataFrame(state_columns)
    by_year.to_csv(derived_dir / "flow_by_year.csv")
    by_state.to_csv(derived_dir / "flow_by_state.csv")
    return by_year, by_state, totals


def state_summary(clean: pd.DataFrame) -> pd.DataFrame:
    out = (
        clean.groupby(["CVE_ENT", "ENTIDAD"], dropna=False)
        .agg(records=("ID_VICTIMA", "size"), confidential=("confidencial", "sum"))
        .reset_index()
    )
    out["confidential_share"] = out["confidential"] / out["records"]
    return out.sort_values("confidential_share", ascending=False)


def snapshot_checks(raw: pd.DataFrame, clean: pd.DataFrame, states: pd.DataFrame) -> list[dict]:
    def state(name: str) -> pd.Series:
        row = states[states["ENTIDAD"].str.upper() == name.upper()]
        if row.empty:
            raise KeyError(name)
        return row.iloc[0]

    checks = [
        ("Mirror rows", len(raw), 133_566, 0),
        ("Unique victim IDs", raw["ID_VICTIMA"].nunique(), 133_566, 0),
        ("Confidential records", int(clean["confidencial"].sum()), 49_136, 0),
        ("National confidential share", clean["confidencial"].mean(), 0.368, 0.0006),
        ("Jalisco confidential share", state("JALISCO")["confidential_share"], 0.67, 0.006),
        ("Nayarit confidential share", state("NAYARIT")["confidential_share"], 0.66, 0.006),
        ("Guerrero confidential share", state("GUERRERO")["confidential_share"], 0.09, 0.006),
        ("Colima confidential share", state("COLIMA")["confidential_share"], 0.09, 0.006),
        ("Jalisco unresolved records", int(state("JALISCO")["records"]), 13_766, 0),
        ("Jalisco confidential records", int(state("JALISCO")["confidential"]), 9_216, 0),
        ("Guerrero unresolved records", int(state("GUERRERO")["records"]), 4_453, 0),
    ]
    result = []
    for label, actual, expected, tolerance in checks:
        passed = abs(float(actual) - float(expected)) <= tolerance
        result.append(
            {
                "claim": label,
                "actual": actual,
                "draft_expected": expected,
                "tolerance": tolerance,
                "status": "PASS" if passed else "REVISE",
            }
        )
    return result


def version_checks(panel: pd.DataFrame) -> tuple[dict, list[dict]]:
    national = panel.groupby("snapshot").agg(total=("total", "sum"), conf=("conf", "sum"))
    national["share"] = national["conf"] / national["total"]
    first, last = national.iloc[0], national.iloc[-1]
    net_conf = int(last["conf"] - first["conf"])
    net_total = int(last["total"] - first["total"])
    summary = {
        "first_snapshot": str(national.index[0]),
        "last_snapshot": str(national.index[-1]),
        "confidential_first": int(first["conf"]),
        "confidential_last": int(last["conf"]),
        "confidential_change": net_conf,
        "total_change": net_total,
        "share_first": float(first["share"]),
        "share_last": float(last["share"]),
        "confidential_share_of_net_growth": net_conf / net_total,
    }
    checks = [
        {"claim": "Version audit starts at 44,035 confidential", "actual": int(first["conf"]), "draft_expected": 44_035},
        {"claim": "Version audit ends at 49,136 confidential", "actual": int(last["conf"]), "draft_expected": 49_136},
        {"claim": "Confidential records increased by 5,101", "actual": net_conf, "draft_expected": 5_101},
        {"claim": "Confidential made up about 77% of net growth", "actual": net_conf / net_total, "draft_expected": 0.77},
    ]
    for check in checks:
        expected, actual = float(check["draft_expected"]), float(check["actual"])
        tolerance = 0.005 if expected < 1 else 0
        check["tolerance"] = tolerance
        check["status"] = "PASS" if abs(actual - expected) <= tolerance else "REVISE"
    return summary, checks


def flow_summary(by_year: pd.DataFrame) -> dict:
    frame = by_year.copy()
    frame.index = pd.to_numeric(frame.index, errors="coerce")
    frame = frame[frame.index.notna()]
    frame.index = frame.index.astype(int)
    frame = frame.loc[(frame.index >= 2000) & (frame.index <= 2025)]
    return {
        "period": "2000-2025",
        "found_alive": int(frame["loc_con_vida"].sum()),
        "found_dead": int(frame["loc_sin_vida"].sum()),
        "still_missing": int(frame["desap_y_nollocal"].sum()),
        "all_reported": int(frame["todos"].sum()),
        "year_2000_all_reported": int(frame.loc[2000, "todos"]),
        "year_2007_all_reported": int(frame.loc[2007, "todos"]),
        "year_2025_all_reported": int(frame.loc[2025, "todos"]),
    }


def fmt(value) -> str:
    if isinstance(value, float):
        return f"{value:.1%}" if abs(value) <= 1 else f"{value:,.2f}"
    return f"{value:,}" if isinstance(value, int) else str(value)


def write_report(
    path: Path,
    freeze_dir: Path,
    manifest: dict,
    checks: list[dict],
    manual_checks: list[str],
) -> None:
    rows = []
    for check in checks:
        rows.append(
            f"| {check['status']} | {check['claim']} | {fmt(check['actual'])} | "
            f"{fmt(check['draft_expected'])} |"
        )
    text = f"""# Publication data audit — {manifest['freeze_date']}

## Publication cutoffs

- **Still-missing microdata and redaction:** lapanquecita RNPDNO mirror snapshot dated {MIRROR_UPSTREAM_DATE}, pinned upstream commit `{MIRROR_UPSTREAM_COMMIT}`.
- **Aggregate outcomes, including located people:** live RNPDNO public dashboard API captured {manifest['captured_at_utc']}.
- **Consent mechanism:** CNB oficio SEGOB/CNBP/1349/2020, pp. 5 and 11 (universe dated 2020-08-07).
- **Batch changes:** ten pinned mirror snapshots, 2025-04-03 to 2025-12-02.

These sources answer different questions and must retain their own dates in the article.

## Automated claim checks

| Result | Claim | Recomputed | Draft value |
|---|---|---:|---:|
{os.linesep.join(rows)}

## Fresh aggregate-flow capture

- Reported disappearances, 2000–2025: **{manifest['flow']['all_reported']:,}**.
- Found alive: **{manifest['flow']['found_alive']:,}**.
- Found dead: **{manifest['flow']['found_dead']:,}**.
- Still missing: **{manifest['flow']['still_missing']:,}**.
- All reported in 2000 / 2007 / 2025: **{manifest['flow']['year_2000_all_reported']:,} / {manifest['flow']['year_2007_all_reported']:,} / {manifest['flow']['year_2025_all_reported']:,}**.

The draft and Figure A should be regenerated from this frozen flow table before publication; live totals are allowed to differ from the June 2026 exploratory pull.

## Manual source checks still required

""" + "\n".join(f"- [ ] {item}" for item in manual_checks) + f"""

## Reproducibility

Frozen inputs, raw API responses, derived tables, hashes and machine-readable checks are in:

`{freeze_dir.relative_to(ROOT)}`

Run `python src/publication_freeze.py --date {manifest['freeze_date']}` only for a new date. Existing freezes are immutable and the script refuses to overwrite them.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Publication freeze date, YYYY-MM-DD")
    args = parser.parse_args()
    datetime.strptime(args.date, "%Y-%m-%d")

    final_dir = FREEZE_ROOT / args.date
    if final_dir.exists():
        raise FileExistsError(f"Refusing to overwrite existing freeze: {final_dir}")

    FREEZE_ROOT.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=f".{args.date}-", dir=FREEZE_ROOT))
    try:
        sources = temp_dir / "sources"
        raw_api = sources / "rnpdno_api"
        derived = temp_dir / "derived"
        sources.mkdir()
        derived.mkdir()

        shutil.copy2(MIRROR, sources / "rnpdno_mirror_2025-12-02.csv")
        shutil.copy2(CONSENT_PDF, sources / CONSENT_PDF.name)
        shutil.copy2(VERSION_PANEL, derived / "confidencial_panel.csv")

        raw = pd.read_csv(sources / "rnpdno_mirror_2025-12-02.csv", dtype="string")
        clean = cleaner.clean(raw)
        clean.to_parquet(derived / "rnpdno_clean.parquet", index=False)
        states = state_summary(clean)
        states.to_csv(derived / "state_redaction_summary.csv", index=False)

        by_year, by_state, totals = fetch_live_flow(raw_api, derived)
        by_state.to_csv(derived / "flow_by_state.csv")

        panel = pd.read_csv(derived / "confidencial_panel.csv", dtype={"CVE_ENT": "string"})
        version_summary, version_claims = version_checks(panel)
        claims = snapshot_checks(raw, clean, states) + version_claims
        pd.DataFrame(claims).to_csv(derived / "automated_claim_checks.csv", index=False)

        captured = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        manifest = {
            "freeze_date": args.date,
            "captured_at_utc": captured,
            "record_level_source": {
                "snapshot_date": MIRROR_UPSTREAM_DATE,
                "upstream_commit": MIRROR_UPSTREAM_COMMIT,
            },
            "aggregate_flow_source": {
                "url": fetch_flow.BASE,
                "captured_at_utc": captured,
            },
            "flow": flow_summary(by_year),
            "version_audit": version_summary,
            "consent_accounting": CONSENT,
            "automated_checks": claims,
            "source_hashes_sha256": {},
        }

        for source in sorted(temp_dir.rglob("*")):
            if source.is_file() and source.name != "manifest.json":
                manifest["source_hashes_sha256"][str(source.relative_to(temp_dir))] = sha256(source)
        (temp_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )

        manual_checks = [
            "Confirm the current unresolved headline total against the live RNPDNO interface and record the visible consultation time.",
            "Re-open Oficio SEGOB/CNBP/1349/2020 and visually verify 56,803, 7,478 and 6,717 on pp. 5 and 11.",
            "Re-check ZonaDocs' 4,765 national and 1,026 Jalisco active-search-notice contradictions.",
            "Re-check Jalisco federal/state divergence dates and totals against the cited primary or investigative sources.",
            "Re-check Guerrero/Iguala collective counts (623 cases, 260+ bodies and about 70 in Acapulco); keep them explicitly non-comparable proxies.",
            "Resolve Figure D's mismatch: its x-axis is unresolved-disappearance rate, but the existing caption discusses homicide rate.",
        ]
        report_path = REPORTS / f"publication_data_audit_{args.date}.md"
        write_report(report_path, final_dir, manifest, claims, manual_checks)

        os.replace(temp_dir, final_dir)
        print(f"Created immutable freeze: {final_dir.relative_to(ROOT)}")
        print(f"Wrote audit: {report_path.relative_to(ROOT)}")
        print(pd.DataFrame(claims)[["status", "claim", "actual", "draft_expected"]].to_string(index=False))
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


if __name__ == "__main__":
    main()
