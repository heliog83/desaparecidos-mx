"""
Option 1 — Pull aggregate FLOW data (incl. located outcomes) from the live RNPDNO dashboard.

Our record-level mirror is the still-missing STOCK only. This hits the dashboard's JSON endpoints
(the mechanism the `reqrnpdno` crate documents — no captcha on the API itself) to retrieve aggregate
counts by status, INCLUDING located-alive / located-dead, by year and by state. That lets us:
  - measure true incidence by year (status=0, everyone who disappeared that year regardless of outcome)
  - measure resolution (located) vs still-missing
  - get located-DEAD by state (the key proxy for the Stage-2 buscadoras story)

Endpoints + the exact default parameter values were reverse-engineered from irvingfisica/reqrnpdno.
Be polite: this is a public-interest registry on a government box — low request volume, delays between.

Outputs:
  data/external/rnpdno_api/<key>.json     (raw responses, for provenance)
  data/processed/flow_totales.csv
  data/processed/flow_by_year.csv         (status x year, totals)
  data/processed/flow_by_state.csv        (status x state, totals)

Run:  python src/fetch_flow.py
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "external" / "rnpdno_api"
PROC = ROOT / "data" / "processed"
BASE = "https://versionpublicarnpdno.segob.gob.mx/"

# idEstatusVictima codes (from reqrnpdno diccionarios).
STATUS = {
    "todos": "0",            # desaparecidas + no localizadas + localizadas (everyone)
    "loc_con_vida": "2",
    "loc_sin_vida": "3",
    "desaparecidas": "4",
    "no_localizadas": "5",
    "localizadas": "6",
    "desap_y_nollocal": "7",  # still-missing (our mirror's universe)
}
ENDPOINTS = {
    "by_year": "SocioDemografico/AreaChartSexoAnio",
    "by_state": "SocioDemografico/BarChartSexoEstados",
}


def _params(estatus: str) -> dict:
    """Exact Parametros::new() defaults; only idEstatusVictima varies."""
    return {
        "titulo": "RNPDNO", "idEstatusVictima": estatus, "fechaInicio": "", "fechaFin": "",
        "idEstado": "0", "idMunicipio": "0", "mostrarFechaNula": "0", "idColonia": "0",
        "idNacionalidad": "0", "edadInicio": "", "edadFin": "", "mostrarEdadNula": "0",
        "idHipotesis": "", "idMedioConocimiento": "", "idCircunstancia": "", "tieneDiscapacidad": "",
        "idTipoDiscapacidad": "0", "idEtnia": "0", "idLengua": "0", "idReligion": "", "esMigrante": "",
        "idEstatusMigratorio": "0", "esLgbttti": "", "esServidorPublico": "", "esDefensorDH": "",
        "esPeriodista": "", "esSindicalista": "", "esONG": "", "idHipotesisNoLocalizacion": "0",
        "idDelito": "0",
    }


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"})
    s.get(BASE, timeout=30)  # establishes the session cookie
    return s


def _to_int(x) -> int:
    return int(str(x).replace(",", "").replace(" %", "").strip() or 0)


def _chart_to_totals(j: dict) -> pd.Series:
    """Sum the per-sex Series into a category->total Series aligned to XAxisCategories."""
    cats = j["XAxisCategories"]
    total = [0] * len(cats)
    for serie in j.get("Series", []):
        for i, v in enumerate(serie.get("data", serie.get("Data", []))):
            total[i] += _to_int(v)
    return pd.Series(total, index=cats)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROC.mkdir(parents=True, exist_ok=True)
    s = _session()

    # 1) National totals by status (the headline resolution breakdown).
    r = s.post(BASE + "Sociodemografico/Totales", data=_params("0"), timeout=40)
    totales = r.json()
    (RAW_DIR / "totales.json").write_text(json.dumps(totales, ensure_ascii=False, indent=2))
    pd.Series({k: _to_int(v) if "Porcentaje" not in k else v for k, v in totales.items()}) \
        .to_csv(PROC / "flow_totales.csv")
    print("Totales:", {k: totales[k] for k in
          ("TotalDesaparecidos", "TotalLocalizados", "TotalLocalizadosSV")})

    # 2) by-year and by-state, for each status of interest.
    year_cols, state_cols = {}, {}
    for skey, scode in STATUS.items():
        for ekey, epath in ENDPOINTS.items():
            time.sleep(1.2)  # be polite
            resp = s.post(BASE + epath, data=_params(scode), timeout=40)
            if resp.text[:1] not in "{[":
                print(f"  WARN {ekey}/{skey}: non-JSON ({resp.status_code})")
                continue
            j = resp.json()
            (RAW_DIR / f"{ekey}_{skey}.json").write_text(json.dumps(j, ensure_ascii=False))
            totals = _chart_to_totals(j)
            (year_cols if ekey == "by_year" else state_cols)[skey] = totals
            print(f"  ok {ekey:8} {skey:16} total={int(totals.sum()):,}")

    pd.DataFrame(year_cols).to_csv(PROC / "flow_by_year.csv")
    pd.DataFrame(state_cols).to_csv(PROC / "flow_by_state.csv")
    print(f"\nWrote flow_by_year.csv, flow_by_state.csv, flow_totales.csv to {PROC.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
