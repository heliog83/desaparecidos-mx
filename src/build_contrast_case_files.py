"""
Build contrast-case evidence files for the opacity analysis.

Outputs:
  data/processed/contrast_cases.csv
  docs/case-selection.md
  docs/cases/<state-slug>.md

Run:
  python src/build_contrast_case_files.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ENRICHED = ROOT / "data" / "processed" / "state_opacity_enriched.csv"
OUT_CSV = ROOT / "data" / "processed" / "contrast_cases.csv"
DOCS = ROOT / "docs"
CASES = DOCS / "cases"

CASE_STATES = [
    {
        "entidad": "JALISCO",
        "role": "Primary high-scale / high-opacity case",
        "why_selected": "Largest confidential-record count and highest confidential share among large states.",
        "slug": "jalisco",
    },
    {
        "entidad": "TAMAULIPAS",
        "role": "High-disappearance-rate, high-scale comparison",
        "why_selected": "Very high unresolved rate and large case volume; opacity is above national cutoff but much lower than Jalisco.",
        "slug": "tamaulipas",
    },
    {
        "entidad": "ESTADO DE MÉXICO",
        "role": "Large-scale / lower-opacity comparison",
        "why_selected": "Largest total unresolved count, but lower confidential share than the national cutoff.",
        "slug": "estado-de-mexico",
    },
    {
        "entidad": "GUERRERO",
        "role": "Large-scale / low-opacity contrast",
        "why_selected": "Large unresolved count and high violence context, but one of the lowest confidential shares.",
        "slug": "guerrero",
    },
    {
        "entidad": "NAYARIT",
        "role": "Lower-scale / high-opacity contrast",
        "why_selected": "Small-to-medium volume but very high confidential share, close to Jalisco's opacity intensity.",
        "slug": "nayarit",
    },
    {
        "entidad": "COLIMA",
        "role": "Lower-scale / lower-opacity contrast",
        "why_selected": "High unresolved rate but very low confidential share, useful for separating crisis intensity from registry opacity.",
        "slug": "colima",
    },
]

SOURCE_LEADS = {
    "JALISCO": [
        ("Official search commission", "https://comisiondebusqueda.jalisco.gob.mx/"),
        ("Jalisco laws and protocols", "https://comisiondebusqueda.jalisco.gob.mx/leyes-y-protocolos"),
        ("Jalisco disappeared-persons registry / Fiscalía platform", "https://fiscaliaenpersonasdesaparecidas.jalisco.gob.mx/"),
        ("Jalisco official statement: 'Jalisco no borra a sus desaparecidos'", "https://jalisco.gob.mx/es/prensa/noticias/159252"),
        ("Jalisco privacy notice mentioning REPD data uses", "https://transparenciasitgej.jalisco.gob.mx/api/api/banco_archivos/298484/downloadWeb"),
    ],
    "TAMAULIPAS": [
        ("Official state search commission page", "https://www.tamaulipas.gob.mx/secretariageneral/organos/comision-estatal-de-busqueda-de-personas/"),
        ("Tamaulipas official gazette search results / commission references", "https://po.tamaulipas.gob.mx/"),
        ("Tamaulipas victims law / data-rights lead", "https://po.tamaulipas.gob.mx/wp-content/uploads/2026/03/Ley_Atencion_Victimas.pdf"),
    ],
    "ESTADO DE MÉXICO": [
        ("FGJ Estado de México", "https://fgjem.edomex.gob.mx/"),
        ("State transparency / personal-data lead", "https://fgjem.edomex.gob.mx/transparencia"),
        ("Red Lupa state pages", "https://imdhd.org/redlupa/"),
    ],
    "GUERRERO": [
        ("Official state search commission page", "https://www.guerrero.gob.mx/dependencia/sector-paraestatal/comision-estatal-de-busqueda-de-personas/"),
        ("Guerrero CEBP privacy notice", "https://www.guerrero.gob.mx/convocatoria/aviso-de-privacidad-cebp/"),
        ("Red Lupa state pages", "https://imdhd.org/redlupa/"),
    ],
    "NAYARIT": [
        ("Official state search commission page", "https://comisionestataldebusqueda.nayarit.gob.mx/"),
        ("Nayarit disappearance law PDF", "https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/leyes/Desaparicion_de_Personas_para_el_Estado_de_Nayarit_Ley_de_materia_de.pdf"),
        ("Red Lupa recommendations for Nayarit", "https://imdhd.org/redlupa/informes-y-analisis/recomendaciones/recomendaciones-nayarit/"),
    ],
    "COLIMA": [
        ("Official state search commission page", "https://www.col.gob.mx/busquedapersonas"),
        ("FGE Colima disappeared-persons page", "https://www.fgecolima.mx/servicios/personas/personas-desaparecidas"),
        ("Colima government notice: genetic donation campaign and confidentiality", "https://www.col.gob.mx/Portal/detalle_noticia/NjIwOTU%3D"),
        ("Red Lupa Colima profile", "https://imdhd.org/redlupa/informes-y-analisis/informes-estatales/region-bajio/personas-desaparecidas-colima/"),
    ],
}


def _fmt_int(value) -> str:
    if pd.isna(value):
        return "unknown"
    return f"{int(round(value)):,}"


def _fmt_float(value, digits=1) -> str:
    if pd.isna(value):
        return "unknown"
    return f"{value:,.{digits}f}"


def _fmt_pct(value, digits=1) -> str:
    if pd.isna(value):
        return "unknown"
    return f"{value:.{digits}%}"


def _md_link(label: str, url: str) -> str:
    return f"[{label}]({url})"


def _display_state(name: str) -> str:
    proper = {
        "ESTADO DE MÉXICO": "Estado de México",
        "CIUDAD DE MÉXICO": "Ciudad de México",
    }
    return proper.get(name, name.title())


def build_case_rows() -> pd.DataFrame:
    state = pd.read_csv(ENRICHED)
    case_meta = pd.DataFrame(CASE_STATES)
    out = case_meta.merge(state, on="entidad", how="left")
    if out["total_records"].isna().any():
        missing = out.loc[out["total_records"].isna(), "entidad"].tolist()
        raise ValueError(f"Missing state rows: {missing}")
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    return out


def write_selection_doc(cases: pd.DataFrame) -> None:
    lines = [
        "# Contrast Case Selection",
        "",
        "Last updated: 2026-06-19.",
        "",
        "The opacity chart gives us a pattern, not an explanation. The next learning step is",
        "to compare a small set of states that represent different combinations of crisis scale",
        "and registry opacity.",
        "",
        "## Selection Logic",
        "",
        "- Choose contrast cases, not just the highest values.",
        "- Keep the set small enough to research carefully.",
        "- Separate what the data shows from what external sources can verify.",
        "- Treat every case file as provisional until source review is complete.",
        "",
        "## Cases",
        "",
        "| State | Role | Typology | Total records | Confidential records | Confidential share | Why selected |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for row in cases.itertuples(index=False):
        lines.append(
            "| "
            f"{_display_state(row.entidad)} | "
            f"{row.role} | "
            f"{row.opacity_typology} | "
            f"{_fmt_int(row.total_records)} | "
            f"{_fmt_int(row.confidential_records)} | "
            f"{_fmt_pct(row.confidential_share)} | "
            f"{row.why_selected} |"
        )

    lines += [
        "",
        "## Evidence Questions",
        "",
        "Each state file uses the same questions:",
        "",
        "- What is the confidential share?",
        "- How many records are hidden?",
        "- What public details are missing?",
        "- Does the state have local search/fiscalia rules about data publication?",
        "- Are there official statements about privacy/redaction?",
        "- Do local collectives or journalists criticize registry opacity?",
        "- Has the state had major fosa discoveries or collective searches?",
        "- Does another source disagree with the official pattern?",
        "",
        "## Current Interpretation",
        "",
        "The working hypothesis is not that high opacity proves manipulation. The working",
        "hypothesis is narrower:",
        "",
        "> State-level public registry opacity may be shaped by administrative, legal, and",
        "> publication practices, not only by crisis intensity.",
        "",
        f"Generated case files live in `{CASES.relative_to(ROOT)}/`.",
        "",
    ]
    (DOCS / "case-selection.md").write_text("\n".join(lines))


def write_case_file(row: pd.Series) -> None:
    state_name = _display_state(str(row["entidad"]))
    leads = SOURCE_LEADS.get(row["entidad"], [])
    lead_lines = [f"- {_md_link(label, url)}" for label, url in leads] or ["- TBD"]

    missing_details = [
        "status split for confidential records",
        "date of disappearance",
        "date of report/registration",
        "sex",
        "birth date / age",
        "municipality",
    ]

    lines = [
        f"# {state_name} Case File",
        "",
        "Status: draft evidence file.",
        "",
        f"Role: {row['role']}",
        "",
        f"Why selected: {row['why_selected']}",
        "",
        "## Quantitative Snapshot",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Opacity typology | {row['opacity_typology']} |",
        f"| Total unresolved records in mirror | {_fmt_int(row['total_records'])} |",
        f"| Confidential records | {_fmt_int(row['confidential_records'])} |",
        f"| Confidential share | {_fmt_pct(row['confidential_share'])} |",
        f"| Known-detail share | {_fmt_pct(row['known_detail_share'])} |",
        f"| Unresolved records per 100k residents | {_fmt_float(row['tasa_100k'])} |",
        f"| Confidential records per 100k residents | {_fmt_float(row['confidential_records_per100k'])} |",
        f"| NO LOCALIZADA share among known statuses | {_fmt_pct(row['no_localizada_share_known'])} |",
        f"| Live RNPDNO resolution share | {_fmt_pct(row['resolution_share'])} |",
        f"| Found-dead among located share | {_fmt_pct(row['found_dead_among_located_share'])} |",
        f"| Homicide victims per 100k, 2015-2025 | {_fmt_float(row['homicide_victims_2015_2025_per100k'])} |",
        f"| Kidnapping victims per 100k, 2015-2025 | {_fmt_float(row['kidnapping_victims_2015_2025_per100k'])} |",
        f"| GDP per capita 2024, 2018 MXN | {_fmt_int(row['pibe_per_capita_2024_2018_mxn'])} |",
        f"| ENCIG corruption prevalence 2025 per 100k | {_fmt_int(row['corruption_prevalence_2025_per100k'])} |",
        "",
        "## What Confidential Records Hide Here",
        "",
    ]
    lines += [f"- {item}" for item in missing_details]
    lines += [
        "",
        "Interpretation rule: confidential records still count as unresolved people, but they",
        "cannot be used for year, sex, age, municipality, or status-specific analysis.",
        "",
        "## Evidence Checklist",
        "",
        "### Local Search/Fiscalia Rules About Publication",
        "",
        "Question: does the state have rules, protocols, notices, or registry language explaining",
        "what gets published, withheld, anonymized, or treated as confidential?",
        "",
        "Current status: not yet verified.",
        "",
        "Evidence to collect:",
        "",
        "- official state law or regulation",
        "- official commission/fiscalia registry page",
        "- privacy notice or personal-data notice",
        "- statement about public registry fields or redaction",
        "",
        "### Official Statements About Privacy/Redaction",
        "",
        "Question: has the state justified confidentiality as privacy, victim protection, child",
        "protection, investigation integrity, or another reason?",
        "",
        "Current status: not yet verified.",
        "",
        "### Collective Or Journalist Criticism",
        "",
        "Question: have families, collectives, journalists, NGOs, or transparency advocates",
        "criticized registry opacity, undercounting, reclassification, or deleted records in this state?",
        "",
        "Current status: not yet verified.",
        "",
        "### Fosas / Collective Search Context",
        "",
        "Question: has the state had major clandestine-grave discoveries or search-collective",
        "actions that could help explain why opacity matters locally?",
        "",
        "Current status: not yet verified.",
        "",
        "### Source Disagreement",
        "",
        "Question: do other sources disagree with the official pattern: Data Civica, Red Lupa,",
        "state registries, press reports, or local NGO datasets?",
        "",
        "Current status: not yet verified.",
        "",
        "## Source Leads",
        "",
    ]
    lines += lead_lines
    lines += [
        "",
        "## Preliminary Case Question",
        "",
        f"What would explain why {state_name} has this combination of crisis scale and",
        "public-registry opacity?",
        "",
        "## Claim Discipline",
        "",
        "Safe claim:",
        "",
        f"> In this snapshot, {state_name} has {_fmt_int(row['confidential_records'])}",
        f"> confidential unresolved records, representing {_fmt_pct(row['confidential_share'])}",
        "> of its unresolved records in the mirror.",
        "",
        "Unsafe claim without more evidence:",
        "",
        "> The state is hiding records intentionally.",
        "",
    ]
    (CASES / f"{row['slug']}.md").write_text("\n".join(lines))


def main() -> None:
    cases = build_case_rows()
    DOCS.mkdir(exist_ok=True)
    CASES.mkdir(parents=True, exist_ok=True)
    write_selection_doc(cases)
    for _, row in cases.iterrows():
        write_case_file(row)
    print(f"Wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"Wrote {(DOCS / 'case-selection.md').relative_to(ROOT)}")
    for meta in CASE_STATES:
        print(f"Wrote {(CASES / (meta['slug'] + '.md')).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
