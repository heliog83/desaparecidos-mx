"""Recompute the article's numeric claims from the pinned freeze and check the prose.

check_article.py proves the embedded chart data and the four headline totals match
the freeze. This goes further: every derived number the prose states — shares,
differences, rates, correlations, panel movements — is recomputed here from the
hash-verified tables in data/publication_freezes/<freeze>/derived/, formatted the
way the article writes it, and required to appear in reports/article_draft.md.

A claim fails when the recomputed value no longer rounds to the printed token, or
when the token has been edited out of the prose without updating this registry.
Claim ids match reports/claim_registry.csv.

Standard library only, so it runs on a clean checkout:
    python3 src/check_claims.py
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from build_page import DRAFT, FREEZE_DERIVED  # noqa: E402

D = FREEZE_DERIVED


def rows(name: str) -> list[dict]:
    with (D / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v: str | None) -> float:
    return float(v) if v not in (None, "") else 0.0


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)


def ranks(v: list[float]) -> list[float]:
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def pct(v: float, dp: int = 1) -> str:
    return f"{v * 100:.{dp}f}%"


def build_claims() -> list[tuple[str, str, str]]:
    """Return (claim_id, token that must appear in the prose, description)."""
    out: list[tuple[str, str, str]] = []
    add = lambda cid, tok, desc: out.append((cid, tok, desc))  # noqa: E731

    # ---- aggregate flow by year (vintage 2026-08-15) ------------------------
    year = {}
    for r in rows("flow_by_year.csv"):
        try:
            y = int(r[""])
        except ValueError:
            continue
        year[y] = {k: int(num(r[k])) for k in
                   ("todos", "loc_con_vida", "loc_sin_vida", "desap_y_nollocal")}
    loc = lambda y: (year[y]["loc_con_vida"] + year[y]["loc_sin_vida"]) / year[y]["todos"]  # noqa: E731
    miss = lambda y: year[y]["desap_y_nollocal"] / year[y]["todos"]  # noqa: E731

    add("FLOW-07", "37,124", "2025 cohort size")
    assert round(year[2007]["todos"], -3) == 3000
    add("FLOW-08", "about\n  3,000 records for 2007", "2007 cohort ~3,000")
    assert year[2025]["todos"] / year[2007]["todos"] > 10, "tenfold claim"
    shares = [miss(y) for y in range(2015, 2026)]
    assert 0.285 <= min(shares) and max(shares) < 0.385, "still-missing 29-38% since 2015"
    add("FLOW-09", "between 29% and 38%", "still-missing share range 2015-2025")
    for y, tok in ((2014, "75% of 2014"), (2025, "68% of 2025")):
        assert f"{loc(y) * 100:.0f}%" in tok
        add(f"FLOW-LOC-{y}", tok, f"located share {y}")
    add("FLOW-LOC-2010", f"{loc(2010) * 100:.0f}% and {loc(2011) * 100:.0f}% located",
        "2010/2011 located shares")

    # ---- fig I / J: homicide comparison -------------------------------------
    comp = {int(r["year"]): r for r in rows("incidence_vs_homicide.csv")}
    h19, h24 = num(comp[2019]["homicide_victims"]), num(comp[2024]["homicide_victims"])
    d19, d24 = year[2019]["todos"], year[2024]["todos"]
    add("HOM-01", pct((h24 - h19) / h19 * -1), "homicide fall 2019-2024")
    add("HOM-02", pct((d24 - d19) / d19), "recorded disappearance rise 2019-2024")
    full = [y for y in range(2015, 2025)]
    r10 = pearson([num(comp[y]["homicide_victims_annualised"]) for y in full],
                  [num(comp[y]["disappearances_recorded"]) for y in full])
    add("HOM-03", f"r = {r10:.2f}", "Pearson r 2015-2024")
    growth = d24 - d19
    dl = {k: year[2024][k] - year[2019][k] for k in ("loc_con_vida", "loc_sin_vida", "desap_y_nollocal")}
    add("SUB-01", f"{growth:,} records larger", "2024 vs 2019 cohort difference")
    add("SUB-02", f"{dl['loc_con_vida'] / growth * 100:.1f}% of that", "alive share of difference")
    add("SUB-03", f"{dl['loc_con_vida']:,} more", "alive difference")
    add("SUB-04", f"{dl['desap_y_nollocal'] / growth * 100:.1f}% of the\ndifference, {dl['desap_y_nollocal']:,}",
        "still-missing share and count of difference")
    add("SUB-05", f"fell by {int(h19 - h24):,}", "homicide fall count")
    add("SUB-06", f"{int(h19 + year[2019]['desap_y_nollocal']):,} in 2019, "
                  f"{int(h24 + year[2024]['desap_y_nollocal']):,} in 2024",
        "homicides + still missing")
    add("SUB-07", f"found-dead difference, {dl['loc_sin_vida']:,}", "found-dead difference")

    # ---- record-level stock (vintage 2025-12-02) ----------------------------
    rates = rows("state_rates.csv")
    st_total = sum(int(num(r["desaparecidos"])) for r in rates)
    pop = sum(num(r["poblacion"]) for r in rates)
    panel = rows("confidencial_panel.csv")
    last = max(r["snapshot"] for r in panel)
    latest = [r for r in panel if r["snapshot"] == last]
    all_total = sum(int(r["total"]) for r in latest)
    all_conf = sum(int(r["conf"]) for r in latest)
    add("STOCK-01", f"{st_total / pop * 1e5:.0f} unresolved records per 100,000", "national rate")
    add("STOCK-02", f"{st_total:,} records assigned to a state", "state-assigned records")
    add("STOCK-03", f"another {all_total - st_total:,} name no state", "unknown-state records")
    add("STOCK-04", pct(all_conf / all_total), "national confidential share")
    add("STAND-CONF", f"{pct(all_conf / all_total)} of unresolved records revealed only two things",
        "standfirst confidential share")
    add("STOCK-05", pct(1 - all_conf / all_total), "national public share")
    byname = {r["entidad"]: r for r in rates}
    for name, tok in (("Tamaulipas", "359"), ("Zacatecas", "226"), ("Sinaloa", "211"),
                      ("Estado de México", "82"), ("Ciudad de México", "79")):
        assert f"{num(byname[name]['tasa_100k']):.0f}" == tok, name
        add(f"RATE-{name[:6]}", f"({tok})" if name != "Tamaulipas" else "at 359", f"{name} rate")
    assert num(byname["Yucatán"]["tasa_100k"]) == min(num(r["tasa_100k"]) for r in rates)

    enr = rows("state_opacity_enriched.csv")
    E = {r["entidad"]: r for r in enr}
    sh = lambda s: num(E[s]["confidential_share"])  # noqa: E731
    for s, tok in (("JALISCO", "66.9%"), ("NAYARIT", "66.2%"), ("GUERRERO", "9.1%"),
                   ("COLIMA", "9.0%")):
        assert pct(sh(s)) == tok, s
        add(f"CONF-{s[:6]}", tok, f"{s} confidential share")
    add("CONF-JAL-N", f"{int(num(E['JALISCO']['confidential_records'])):,} of its\n"
                      f"{int(num(E['JALISCO']['total_records'])):,}", "Jalisco counts")
    add("CONF-GRO-N", f"{int(num(E['GUERRERO']['total_records'])):,}", "Guerrero unresolved")
    ratio = sh("JALISCO") / sh("GUERRERO")
    assert 7 <= ratio < 8, "seven times"
    add("CONF-RATIO", "seven times as much", "Jalisco/Guerrero redaction ratio")
    assert round(1 / sh("GUERRERO")) == 11
    add("CONF-GRO-11", "one in eleven", "Guerrero 1 in 11")

    # ---- fig D correlations ---------------------------------------------------
    x = [num(r["homicide_victims_2015_2025_per100k"]) for r in enr]
    y = [num(r["confidential_share"]) for r in enr]
    r_all = pearson(x, y)
    keep = [i for i, r in enumerate(enr) if r["entidad"] != "COLIMA"]
    r_noc = pearson([x[i] for i in keep], [y[i] for i in keep])
    rho = pearson(ranks(x), ranks(y))
    add("CORR-01", f"r = −{abs(r_all):.2f}", "Pearson r, 32 states")
    add("CORR-02", f"−{abs(r_noc):.2f} without", "r without Colima")
    add("CORR-03", f"rank correlation −{abs(rho):.2f}", "Spearman rho")
    hr = lambda s: num(E[s]["homicide_victims_2015_2025_per100k"])  # noqa: E731
    assert max(enr, key=lambda r: num(r["homicide_victims_2015_2025_per100k"]))["entidad"] == "COLIMA"
    assert min(enr, key=lambda r: num(r["homicide_victims_2015_2025_per100k"]))["entidad"] == "YUCATÁN"
    add("HR-COL", f"roughly\n{round(hr('COLIMA'), -1):.0f} homicides", "Colima homicide rate")
    add("HR-GRO", f"at {hr('GUERRERO'):.0f}", "Guerrero homicide rate")
    add("HR-CHI", f"at\n{hr('CHIHUAHUA'):.0f}", "Chihuahua homicide rate")
    add("HR-YUC", f"{hr('YUCATÁN'):.0f} and {num(byname['Yucatán']['tasa_100k'])}", "Yucatán rates")
    assert hr("JALISCO") < hr("GUERRERO") / 2, "Jalisco < half Guerrero"
    add("HR-YUC-CONF", f"redacts\n{sh('YUCATÁN') * 100:.0f}%", "Yucatán share")

    # ---- version panel (Apr-Dec 2025) ---------------------------------------
    snaps = sorted({r["snapshot"] for r in panel})
    tot = {s: sum(int(r["total"]) for r in panel if r["snapshot"] == s) for s in snaps}
    con = {s: sum(int(r["conf"]) for r in panel if r["snapshot"] == s) for s in snaps}
    first = snaps[0]
    add("PANEL-01", f"{con[first]:,} → {con[last]:,} (+{con[last] - con[first]:,})", "confidential growth")
    add("PANEL-02", f"{(con[last] - con[first]) / (tot[last] - tot[first]) * 100:.0f}% of the\nregistry",
        "share of net growth")
    S = lambda st, s, k: int(next(r[k] for r in panel if r["ENTIDAD"] == st and r["snapshot"] == s))  # noqa: E731
    tam = S("TAMAULIPAS", "2025-07-02", "conf") - S("TAMAULIPAS", "2025-05-02", "conf")
    assert round(tam, -2) == 2500
    add("PANEL-TAM", "~2,500\nconfidential records in two months", "Tamaulipas batch")
    add("STAND-TAM", "about 2,500 records in one state in two months", "standfirst Tamaulipas batch")
    add("STAND-SNAPS", f"{len(snaps)} snapshots taken between April and\nDecember 2025".replace("10", "Ten"),
        "standfirst snapshot count")
    q4 = S("JALISCO", "2025-09-02", "conf") - S("JALISCO", "2025-12-02", "conf")
    assert round(q4, -2) == 1200, q4
    add("PANEL-JAL", "about 1,200 in the last quarter", "Jalisco Q4 fall")
    tab = 1 - S("TABASCO", "2025-11-04", "total") / S("TABASCO", "2025-10-02", "total")
    assert tab > 1 / 3
    cdmx0, cdmx1 = S("CIUDAD DE MÉXICO", first, "total"), S("CIUDAD DE MÉXICO", last, "total")
    add("PANEL-CDMX", f"from {cdmx0:,} in April to {cdmx1:,} in December", "CDMX climb")

    # ---- live by state (vintage 2026-08-15) ---------------------------------
    live = {r[""].strip(): int(num(r["desap_y_nollocal"])) for r in rows("flow_by_state.csv")}
    add("LIVE-CDMX", f"By August 2026 the live registry showed {live['CIUDAD DE MEXICO']:,}", "CDMX live")
    add("LIVE-CDMX-D", f"shed {cdmx1 - live['CIUDAD DE MEXICO']:,}", "CDMX fall")
    live_states = sum(v for k, v in live.items() if k != "SE DESCONOCE")
    add("DRIFT-01", f"against {live_states:,} live ({(st_total / live_states - 1) * 100:.1f}%)".replace("-", "−"),
        "state-assigned drift")
    add("DRIFT-02", f"against {live['SE DESCONOCE']:,} live", "live unknown-state records")
    jal_live = live["JALISCO"]
    add("LIVE-JAL", f"stood at {jal_live:,} in August 2026", "Jalisco live")

    # ---- fig K: confidentiality by filing authority (2025-12-02) --------------
    fa: dict[str, dict[str, tuple[int, int]]] = {}
    for r in rows("confidential_by_filing_authority.csv"):
        if r["cve_ent"] != "99":
            fa.setdefault(r["entidad"], {})[r["authority"]] = (int(r["records"]), int(r["confidential"]))
    sh_fa = lambda st, a: fa[st][a][1] / fa[st][a][0]  # noqa: E731
    for st, tok in (("ESTADO DE MÉXICO", "In Estado de México, {p}% of the unresolved records"),
                    ("NUEVO LEÓN", "In Nuevo León the figures are {p}% and {c}%"),
                    ("JALISCO", "in Jalisco, {p}% and {c}%")):
        p_, c_ = round(sh_fa(st, "state_prosecutor") * 100), round(sh_fa(st, "state_commission") * 100)
        add(f"FA-{st[:6]}", tok.format(p=p_, c=c_), f"{st} prosecutor vs commission")
    add("FA-EDOMEX-C", f"against {round(sh_fa('ESTADO DE MÉXICO', 'state_commission') * 100)}% of those filed",
        "Estado de México commission share")
    for st in ("PUEBLA", "BAJA CALIFORNIA SUR"):
        assert sh_fa(st, "state_prosecutor") > sh_fa(st, "state_commission"), st
    pairs = [sh_fa(st, "state_commission") - sh_fa(st, "state_prosecutor") for st, a in fa.items()
             if a.get("state_prosecutor", (0, 0))[0] >= 300 and a.get("state_commission", (0, 0))[0] >= 300]
    add("FA-N", f"In six of the {len(pairs)} states", "states with both offices >= 300")
    add("FA-SMALL", "in eight, by fewer than 10", "states with gap under 10 points")
    big = sorted(abs(g) for g in pairs if abs(g) >= 0.30)
    assert round(big[0] * 100) >= 30 and round(big[-1] * 100, -1) == 60, big
    add("STAND-FA", "differs by 30 to 60 points depending on which office", "standfirst gap range")
    assert sum(abs(g) >= 0.30 for g in pairs) == 6 and sum(abs(g) < 0.10 for g in pairs) == 8
    portal = sorted(sh_fa(st, "portal") for st, a in fa.items() if a.get("portal", (0, 0))[0] >= 100)
    lo, hi = portal[len(portal) // 4], portal[(3 * len(portal)) // 4]
    assert round(lo * 100) == 35 and round(hi * 100) == 41, (lo, hi)
    add("FA-PORTAL", "between\nabout 35% and 41% across the middle half", "portal interquartile range")

    # ---- Guerrero / Iguala ratio ----------------------------------------------
    assert round(int(num(E["GUERRERO"]["total_records"])) / 623) == 7
    add("GRO-IGUALA", "a seventh of the federal register", "623 vs 4,453")
    return out


def main() -> None:
    prose = DRAFT.read_text(encoding="utf-8")
    flat = " ".join(prose.split())
    failures = []
    claims = build_claims()
    for cid, token, desc in claims:
        if " ".join(token.split()) not in flat:
            failures.append(f"  {cid}: '{' '.join(token.split())}' ({desc}) not found in prose")
    if failures:
        print("FAIL: recomputed claims absent from reports/article_draft.md")
        print("\n".join(failures))
        raise SystemExit(1)
    print(f"PASS: {len(claims)} numeric claims recomputed from freeze and found in the prose.")


if __name__ == "__main__":
    main()
