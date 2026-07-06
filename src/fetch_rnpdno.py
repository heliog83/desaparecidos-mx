"""
Fetch disappeared-persons data for the project.

The official RNPDNO has no clean download — its public dashboard
(https://versionpublicarnpdno.segob.gob.mx/) is fed by internal JSON endpoints that
must be scraped. This script is a STARTING POINT with two paths:

  Path A (recommended first): use Data Cívica's cleaned open data.
      https://volveradesaparecer.datacivica.org/datos-abiertos
      Download the CSV(s) once in a browser into data/external/, then load here.

  Path B (full pipeline): replicate the dashboard's JSON API calls. See the Rust crate
      `irvingfisica/reqrnpdno` and `lapanquecita/personas-desaparecidas` (Python) for the
      exact endpoints and payloads. Stub left below to fill in.

Run:
    python src/fetch_rnpdno.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
EXTERNAL = ROOT / "data" / "external"
PROCESSED = ROOT / "data" / "processed"


def load_datacivica(filename: str) -> pd.DataFrame:
    """Path A: load a Data Cívica CSV you've placed in data/external/."""
    path = EXTERNAL / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Expected {path}.\n"
            "Download the cleaned RNPDNO CSV from "
            "https://volveradesaparecer.datacivica.org/datos-abiertos "
            "and save it into data/external/."
        )
    return pd.read_csv(path)


def fetch_rnpdno_api() -> pd.DataFrame:
    """Path B: hit the RNPDNO dashboard JSON endpoints directly.

    TODO: implement using the endpoint/payload patterns from
    https://github.com/irvingfisica/reqrnpdno and
    https://github.com/lapanquecita/personas-desaparecidas
    """
    raise NotImplementedError("Direct RNPDNO scraping not implemented yet — see docstring.")


if __name__ == "__main__":
    for d in (RAW, EXTERNAL, PROCESSED):
        d.mkdir(parents=True, exist_ok=True)
    print("Data dirs ready. Next: download a Data Cívica CSV into data/external/,")
    print("then wire load_datacivica() into a cleaning step that writes data/processed/.")
