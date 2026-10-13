"""Fig 29 / article fig K: confidentiality depends on which office filed the report.

A CONFIDENCIAL record keeps two descriptive fields: the state, and ORIGEN_REPORTE,
the authority that filed it. That second field makes one test possible. If
redaction reflected what families chose, it should not depend much on which office
happened to take the case. Within the same state, it depends on it enormously.

Two steps, so a clean checkout can redraw the chart without the 23 MB mirror:

  --derive MIRROR   Tabulate records and confidential records by state x filing
                    authority from the record-level mirror into the freeze
                    (derived/confidential_by_filing_authority.csv). Do this only
                    when cutting or amending a freeze, and re-hash it in manifest.json.
  (default)         Draw the figure from that hash-pinned table.

Authority groups (from ORIGEN_REPORTE):
  state_prosecutor     FISCALIA GENERAL DE <state> / PROCURADURIA GENERAL DE JUSTICIA ...
  state_commission     COMISION LOCAL DE BUSQUEDA DE PERSONAS ...
  portal               PORTAL — families reporting directly to the national commission online
  national_commission  COMISION NACIONAL DE BUSQUEDA DE PERSONAS (not via the portal)
  federal              FGR, its special prosecutor for crimes against women, legacy PGR offices
  unknown              SE DESCONOCE

Descriptive, not causal: case mix differs by channel (the portal skews to family
self-reports and recent years).

Run:  MPLBACKEND=Agg python src/filing_authority.py [--derive path/to/mirror.csv]
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data" / "publication_freezes" / "2026-08-15"
TABLE = FREEZE / "derived" / "confidential_by_filing_authority.csv"
NUMBERED = ROOT / "reports" / "figures" / "29_confidential_by_filing_authority.png"

# A state is charted only when both state offices filed enough cases for a share to
# mean something; 300 keeps 17 states and drops the thin cells.
MIN_RECORDS = 300


def authority(origin: str) -> str:
    o = (origin or "").strip().upper()
    if o == "PORTAL":
        return "portal"
    if o.startswith("COMISION LOCAL"):
        return "state_commission"
    if o.startswith("COMISION NACIONAL"):
        return "national_commission"
    if o in ("SE DESCONOCE", ""):
        return "unknown"
    if "REPUBLICA" in o or o.startswith("SUBPROCURADURIA") or o.startswith("FISCALIA ESPECIAL"):
        return "federal"
    if o.startswith("FISCALIA GENERAL") or o.startswith("PROCURADURIA GENERAL DE JUSTICIA"):
        return "state_prosecutor"
    raise ValueError(f"unclassified ORIGEN_REPORTE: {origin!r}")


def derive(mirror: Path) -> None:
    counts: dict[tuple[str, str, str], list[int]] = defaultdict(lambda: [0, 0])
    with mirror.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["CVE_ENT"].zfill(2), row["ENTIDAD"], authority(row["ORIGEN_REPORTE"]))
            counts[key][0] += 1
            counts[key][1] += row["ESTATUS_VICTIMA"] == "CONFIDENCIAL"
    with TABLE.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cve_ent", "entidad", "authority", "records", "confidential"])
        for (cve, ent, auth), (n, c) in sorted(counts.items()):
            w.writerow([cve, ent, auth, n, c])
    total = sum(v[0] for v in counts.values())
    print(f"wrote {TABLE.relative_to(ROOT)}  ({total:,} records)")


def load() -> dict[str, dict[str, tuple[int, int]]]:
    by_state: dict[str, dict[str, tuple[int, int]]] = defaultdict(dict)
    with TABLE.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["cve_ent"] == "99":
                continue
            by_state[r["entidad"]][r["authority"]] = (int(r["records"]), int(r["confidential"]))
    return by_state


def label(name: str) -> str:
    out = name.title()
    for t in (" De ", " Del ", " La "):
        out = out.replace(t, t.lower())
    return out


def draw() -> None:
    import matplotlib.pyplot as plt

    import article_style as st

    st.apply()
    data = load()
    rows = []
    for state, auth in data.items():
        p, c, q = auth.get("state_prosecutor"), auth.get("state_commission"), auth.get("portal")
        if p and c and p[0] >= MIN_RECORDS and c[0] >= MIN_RECORDS:
            rows.append((label(state), p[1] / p[0], c[1] / c[0],
                         q[1] / q[0] if q and q[0] >= 100 else None))
    # Widest gap at the top: the point of the chart is the distance between the dots.
    rows.sort(key=lambda r: abs(r[2] - r[1]))

    fig, ax = plt.subplots(figsize=(8.2, 0.34 * len(rows) + 2.4))
    for i, (_, p, c, q) in enumerate(rows):
        ax.plot([p, c], [i, i], color="#c9c3b8", lw=2.2, zorder=1, solid_capstyle="round")
        if q is not None:
            ax.plot([q], [i], marker="|", ms=13, mew=2, color=st.MUTED, zorder=2)
        ax.plot([p], [i], "o", ms=8, color=st.INK, zorder=3)
        ax.plot([c], [i], "o", ms=8, mfc=st.PAPER, mec=st.RED, mew=2.2, zorder=3)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows])
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.set_xlim(0, 1)
    ax.set_xticks([0, .2, .4, .6, .8, 1])
    ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.xaxis.tick_top()
    ax.grid(axis="x", color=st.MUTED, alpha=0.22, lw=0.7)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["top"].set_visible(True)
    ax.tick_params(axis="y", length=0)

    handles = [
        plt.Line2D([], [], ls="", marker="o", ms=8, color=st.INK, label="Filed by a state prosecutor"),
        plt.Line2D([], [], ls="", marker="o", ms=8, mfc=st.PAPER, mec=st.RED, mew=2.2,
                   label="Filed by a state search commission"),
        plt.Line2D([], [], ls="", marker="|", ms=13, mew=2, color=st.MUTED,
                   label="Reported by families via the national portal"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.45, -0.01), ncol=2,
              fontsize=9, handletextpad=0.4, columnspacing=1.4)
    fig.suptitle("Same state, different office, different secrecy", x=0.03, ha="left",
                 fontsize=15, fontweight="bold", color=st.INK)
    fig.text(0.03, 0.955 - 0.004 * (25 - len(rows)),
             "Share of each office's unresolved records marked CONFIDENCIAL, December 2025",
             ha="left", fontsize=10, color=st.MUTED)
    st.caption(fig, f"States where both offices filed at least {MIN_RECORDS} unresolved records "
               f"({len(rows)} of 32). Portal tick shown where families filed at least 100.\n"
               "Descriptive: case mix differs by channel. Source: RNPDNO public record-level "
               "version, 2025-12-02 (lapanquecita mirror).", x=0.03)
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    fig.savefig(NUMBERED, dpi=200)
    print(f"wrote {NUMBERED.relative_to(ROOT)}")
    st.save(fig, "K_filing_authority.png")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--derive":
        derive(Path(sys.argv[2]))
    draw()
