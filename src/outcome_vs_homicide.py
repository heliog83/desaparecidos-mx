"""Fig 27 / article fig J: did falling homicides move into the disappeared column?

Fig I shows homicides falling while recorded disappearances rise. The obvious
suspicion is substitution — that deaths are being recorded as disappearances so the
homicide statistic looks better. The registry's outcome split weighs against that
as the main explanation but cannot rule out part of it.

The 2024 cohort is 10,905 records larger than the 2019 cohort. Of that difference,
61.7% is people currently recorded as FOUND ALIVE, 36.8% still missing, and 1.4%
found dead. A killing recorded as a disappearance would sit in STILL MISSING, not in
found dead (2026-10 audit correction: an earlier version tested homicides + found
dead, the wrong pair). Homicides + still missing is nearly flat, 42,970 (2019) ->
42,326 (2024), so a partial shift cannot be excluded. Found dead is also
right-censored: the 2024 cohort has had far less time to be identified.

What this does NOT rule out, and the caption says so, has two forms. A body that is
never found enters neither statistic; that channel is mechanically real and this data
cannot size it. But a second form has been counted: 72,172 bodies entered Mexico's
forensic services between 2006 and 2023 and were never identified (Quinto Elemento
Lab / A donde van los desaparecidos, 2024-09-24). Those people were found and are in
state custody, and precisely because they are unidentified they cannot be matched to
any registry record. The chart rules out the strong version of the substitution
claim, not the weak one, and the weak one has a documented floor.

Note also that SESNSP counts victims named in investigation files, not bodies, so
it is not a clean count of deaths either.

Run:  MPLBACKEND=Agg python src/outcome_vs_homicide.py
"""
from __future__ import annotations

import csv
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt

import article_style as st

ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_FREEZE = "2026-08-15"
DERIVED = ROOT / "data" / "publication_freezes" / PUBLICATION_FREEZE / "derived"
FLOW_YEAR = DERIVED / "flow_by_year.csv"
SERIES = DERIVED / "incidence_vs_homicide.csv"

FIRST, LAST_COMPLETE, PROVISIONAL = 2015, 2024, 2025


def load() -> list[dict]:
    hom = {}
    with SERIES.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            hom[int(row["year"])] = int(row["homicide_victims_annualised"])

    rows = []
    with FLOW_YEAR.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                year = int(row.get("") or "")
            except ValueError:
                continue
            if FIRST <= year <= PROVISIONAL:
                num = lambda k: int(round(float(row.get(k) or 0)))
                rows.append({
                    "year": year,
                    "alive": num("loc_con_vida"),
                    "dead": num("loc_sin_vida"),
                    "missing": num("desap_y_nollocal"),
                    "homicides": hom[year],
                })
    return sorted(rows, key=lambda r: r["year"])


def build(rows: list[dict]) -> None:
    st.apply()
    years = [r["year"] for r in rows]
    alive = [r["alive"] for r in rows]
    dead = [r["dead"] for r in rows]
    missing = [r["missing"] for r in rows]
    hom = [r["homicides"] for r in rows]

    fig, ax = plt.subplots(figsize=(11.5, 6.4))

    ax.bar(years, alive, color=st.BLUE, width=0.66, label="Found alive")
    ax.bar(years, dead, bottom=alive, color=st.INK, width=0.66, label="Found dead")
    ax.bar(years, missing, bottom=[a + d for a, d in zip(alive, dead)],
           color=st.RED, width=0.66, label="Still missing")

    n = years.index(LAST_COMPLETE) + 1
    ax.plot(years[:n], hom[:n], color="#c8791f", lw=2.6, zorder=5,
            marker="o", ms=5, label="Homicide victims (SESNSP)")
    ax.plot(years[n - 1:], hom[n - 1:], color="#c8791f", lw=1.6, ls=":", zorder=5)
    ax.plot([PROVISIONAL], [hom[-1]], marker="o", ms=6, mfc=st.PAPER,
            mec="#c8791f", mew=1.6, zorder=6)
    # To the right of the marker: below it lands inside the 2025 bar.
    ax.text(PROVISIONAL + 0.42, hom[-1], "2025\nprovisional", ha="left", va="center",
            fontsize=8.5, color=st.MUTED)

    # The claim under test lives in the thin dark band; point straight at it.
    ax.annotate(
        f"Found dead barely moves:\n{dead[years.index(2019)]:,} in 2019, "
        f"{dead[n-1]:,} in 2024",
        xy=(2022.38, alive[years.index(2022)] + dead[years.index(2022)] / 2),
        xytext=(2019.0, 37900), fontsize=9, color=st.INK, va="top",
        arrowprops=dict(arrowstyle="-", color=st.INK, lw=0.9, shrinkB=2))
    # Reversed out on its own backing: plain white text straddled the gap between
    # two bars and half of it disappeared against the page.
    ax.text(2020.5, 5200, "Most of the growth is\npeople later found alive",
            ha="center", va="center", fontsize=10.5, color=st.PAPER, weight="bold",
            bbox=dict(boxstyle="round,pad=0.5", fc=st.BLUE, ec="none", alpha=0.96),
            zorder=6)

    ax.set_xticks(years)
    ax.set_xlim(FIRST - 0.7, PROVISIONAL + 1.15)
    ax.set_ylim(0, 40500)
    ax.set_ylabel("People per year of disappearance")
    ax.grid(axis="y", color=st.MUTED, alpha=0.22, lw=0.7)
    ax.set_axisbelow(True)
    handles, labels = ax.get_legend_handles_labels()
    order = [labels.index(x) for x in
             ["Found alive", "Found dead", "Still missing", "Homicide victims (SESNSP)"]]
    ax.legend([handles[i] for i in order], [labels[i] for i in order],
              loc="upper left", frameon=False, fontsize=9.5, ncol=4,
              columnspacing=1.6, handlelength=1.6)

    st.title(
        ax,
        "Most of the extra records are people found alive",
        "Each bar is one year of disappearance, split by where the case stands now, "
        "with homicide victims for the same year overlaid.",
    )
    st.caption(fig, textwrap.fill(
        "Registry outcomes from the RNPDNO aggregate flow (publication freeze "
        f"{PUBLICATION_FREEZE}); homicide victims from SESNSP, annualised for 2025 from ten "
        "reported months and drawn detached. The 2024 cohort is 10,905 records larger than "
        "2019's: 61.7% of the difference is recorded found alive, 36.8% still missing and 1.4% "
        "found dead. A killing recorded as a disappearance would sit in 'still missing'; homicides "
        "plus still missing barely moved (42,970 to 42,326), so a partial shift cannot be ruled "
        "out, and recent cohorts have had less time to be identified. A body never found enters "
        "neither statistic; and "
        "separately, 72,172 bodies entered Mexico's forensic services between 2006 and 2023 "
        "without ever being identified, so they cannot be matched to any registry record either "
        "(Quinto Elemento Lab / A donde van los desaparecidos, 2024-09-24; a floor, since Morelos "
        "did not respond). SESNSP counts victims named in investigation files, not bodies.",
        width=118))
    fig.tight_layout(rect=(0, 0.19, 1, 1))

    numbered = ROOT / "reports" / "figures" / "27_outcome_vs_homicide.png"
    fig.savefig(numbered, dpi=200)
    print(f"wrote {numbered.relative_to(ROOT)}")
    st.save(fig, "J_outcome_vs_homicide.png")

    i19, i24 = years.index(2019), n - 1
    growth = sum(r[i24] - r[i19] for r in (alive, dead, missing))
    for name, series in (("alive", alive), ("dead", dead), ("missing", missing)):
        delta = series[i24] - series[i19]
        print(f"  {name:8s} {delta:>+7,} = {delta/growth*100:5.1f}% of +{growth:,}")


if __name__ == "__main__":
    build(load())
