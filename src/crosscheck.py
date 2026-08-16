"""
Option 3 — Bound the drift between our record-level mirror and the live registry.

Our field-level analysis rests on the lapanquecita mirror, a community-scraped snapshot that
FROZE at 2025-12-02 (upstream stopped publishing; see docs/data-refresh-2026-08-15.md). The
live RNPDNO dashboard keeps moving and revises retroactively. This script bounds how far the
mirror has drifted, so every state-level claim in the article can be checked against it.

Reference is now OUR OWN API pull (src/fetch_flow.py -> data/processed/flow_by_state.csv),
which supersedes the hand-collected press figures this script used to compare against. That
matters for three reasons: it covers all 32 states instead of 5, it is a like-for-like
definition (idEstatusVictima=7, desaparecidas + no localizadas — the mirror's universe), and
it carries a consultation date we control rather than one inferred from a news article. The
press figures are kept below as a historical provenance check, not as the reference.

Inputs:
  data/processed/rnpdno_clean.parquet   (mirror, snapshot 2025-12-02)
  data/processed/flow_by_state.csv      (live API, see API_PULL_DATE)
Output: printed report (no files written)

Run:  python src/crosscheck.py
"""
from __future__ import annotations

import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PARQUET = ROOT / "data" / "processed" / "rnpdno_clean.parquet"
FLOW_STATE = ROOT / "data" / "processed" / "flow_by_state.csv"

MIRROR_DATE = "2025-12-02"   # upstream commit 666b3e7605; mirror has not moved since
API_PULL_DATE = "2026-08-15"  # update when src/fetch_flow.py is re-run
API_COL = "desap_y_nollocal"  # still-missing = the mirror's universe
UNKNOWN = "SE DESCONOCE"      # API-only bucket: no state attributed
FLAG_PCT = 5.0                # |drift| at or above this gets flagged...
MIN_BASE = 1_000              # ...but only for states big enough for a % to mean anything.
                              # Campeche (n=148) swinging +24 records is 16% and is noise;
                              # CDMX moving -1,327 is 18% and is the finding. Without this
                              # guard the flag list ranks them identically.

# Historical provenance only — press figures we previously cross-checked against.
# Superseded by the API pull; retained so the earlier verdict stays auditable.
PRESS_NATIONAL = (134_481, "2026-05-27", "sdpnoticias citing RNPDNO")


def _norm(s: str) -> str:
    """Fold to ASCII uppercase so 'Ciudad de México' == 'CIUDAD DE MEXICO'."""
    return (unicodedata.normalize("NFKD", str(s))
            .encode("ascii", "ignore").decode().upper().strip())


def build() -> tuple[pd.DataFrame, int, int, int]:
    mirror = pd.read_parquet(PARQUET)["ENTIDAD"].map(_norm).value_counts()
    api = pd.read_csv(FLOW_STATE, index_col=0)[API_COL]
    api.index = [_norm(i) for i in api.index]

    api_unknown = int(api.get(UNKNOWN, 0))
    api_states = api.drop(index=UNKNOWN, errors="ignore")

    cmp = pd.DataFrame({"mirror": mirror, "live_api": api_states}).dropna()
    cmp["live_api"] = cmp.live_api.astype(int)
    cmp["drift"] = (cmp.live_api - cmp.mirror).astype(int)
    cmp["drift_pct"] = (cmp.drift / cmp.mirror * 100).round(1)
    return cmp.sort_index(), int(mirror.sum()), int(api_states.sum()), api_unknown


def main() -> None:
    cmp, mirror_total, api_total, api_unknown = build()

    print(f"MIRROR {MIRROR_DATE}  vs  LIVE API {API_PULL_DATE}")
    print("=" * 62)
    print("\nNATIONAL (state-attributable records)")
    d = api_total - mirror_total
    print(f"  mirror:   {mirror_total:,}")
    print(f"  live API: {api_total:,}   (+{api_unknown:,} more with no state attributed)")
    print(f"  drift:    {d:+,}  ({d / mirror_total * 100:+.2f}%)")
    print(f"  headline totals: {mirror_total:,} vs {api_total + api_unknown:,} "
          f"({(api_total + api_unknown - mirror_total) / mirror_total * 100:+.2f}%)")

    big = cmp[cmp.mirror >= MIN_BASE]
    flagged = big[big.drift_pct.abs() >= FLAG_PCT].sort_values("drift_pct")
    print(f"\nPER-STATE — flagged (|drift| >= {FLAG_PCT}% on a base of {MIN_BASE:,}+)")
    print(flagged.to_string() if len(flagged) else "  (none)")

    small = cmp[(cmp.mirror < MIN_BASE) & (cmp.drift_pct.abs() >= FLAG_PCT)]
    if len(small):
        print(f"\n  small-base states excluded from the flag (n < {MIN_BASE:,}) — "
              "large % on few records:")
        print("   " + "; ".join(f"{s} {int(r.drift):+,} on {int(r.mirror):,} ({r.drift_pct:+.1f}%)"
                                for s, r in small.sort_values("mirror").iterrows()))

    print("\nPER-STATE — full table (by drift)")
    print(cmp.sort_values("drift_pct").to_string())

    print("\nHISTORICAL CHECK (superseded, kept for provenance)")
    pn, pd_date, psrc = PRESS_NATIONAL
    print(f"  press figure {pn:,} ({pd_date}, {psrc}) vs mirror "
          f"{mirror_total:,}: {(mirror_total - pn) / pn:+.1%}")

    print("\nVERDICT")
    print(f"  National drift is {abs(d / mirror_total) * 100:.2f}% — the mirror remains sound as a")
    print("  national cross-section despite being frozen at " + MIRROR_DATE + ".")
    if len(flagged):
        worst = flagged.reindex(flagged.drift_pct.abs().sort_values(ascending=False).index)
        names = ", ".join(f"{s} ({r.drift_pct:+.1f}%)" for s, r in worst.head(4).iterrows())
        print(f"  Drift is NOT uniform by state. Largest movers: {names}.")
        print("  Any per-state claim from the mirror must be labelled to its snapshot date;")
        print("  a flagged state should carry its live figure in the caption.")


if __name__ == "__main__":
    main()
