"""
Desaparecidos MX — interactive dashboard.

Surfaces the Stage-1 analysis (scale, geography, outcomes, opacity) from the committed
processed data. Run from the project root:

    streamlit run dashboard/app.py

Design: every view states its denominator/caveat inline — this data is easy to mislead with.
"""
from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
# Read the pinned publication freeze, not the mutable data/processed/ scratch
# directory that src/fetch_flow.py overwrites with live figures. Same pin as
# src/build_page.py, so the dashboard and the article never disagree.
PUBLICATION_FREEZE = "2026-08-15"
PROC = ROOT / "data" / "publication_freezes" / PUBLICATION_FREEZE / "derived"
STAGE2 = ROOT / "data" / "stage2"
FIG = ROOT / "reports" / "figures"

ALIVE, DEAD, MISSING, INK = "#7d9bb5", "#2b2b2b", "#7a1f1f", "#2b2b2b"

st.set_page_config(page_title="Desaparecidos MX", page_icon="🕯️", layout="wide")


# --------------------------------------------------------------------------- data
@st.cache_data
def load():
    tot = pd.read_csv(PROC / "flow_totales.csv", index_col=0)["0"].to_dict()
    yr = pd.read_csv(PROC / "flow_by_year.csv", index_col=0)
    yr.index = pd.to_numeric(yr.index, errors="coerce")
    yr = yr[yr.index.notna()]
    yr.index = yr.index.astype(int)
    yr = yr[(yr.index >= 1990) & (yr.index <= 2025)].sort_index()
    rates = pd.read_csv(PROC / "state_rates.csv")
    opac = pd.read_csv(PROC / "state_opacity_typology.csv")
    return tot, yr, rates, opac


tot, yr, rates, opac = load()


def metric_int(d, key, default=0):
    try:
        return int(str(d.get(key, default)).replace(",", ""))
    except (ValueError, TypeError):
        return default


# --------------------------------------------------------------------------- sidebar
st.sidebar.title("🕯️ Desaparecidos MX")
st.sidebar.markdown(
    "Quantifying Mexico's disappearance crisis and the work of the **madres buscadoras**."
)
st.sidebar.caption(
    "Source: RNPDNO (official registry) via community mirror + live dashboard flow. "
    "Figures are a snapshot and revise retroactively."
)
with st.sidebar.expander("⚠️ Read before interpreting", expanded=False):
    st.markdown(
        "- **Stock vs flow:** counts of the *still missing* differ from *all who disappeared*. "
        "The flow views include people since located.\n"
        "- **Opacity:** ~37% of records are `CONFIDENCIAL` (state only), unevenly by state — "
        "so cross-state ranks are partly a transparency artifact.\n"
        "- **'Located'** includes contested 2023 *censo* reclassifications.\n"
        "- Every person here is real. State uncertainty; avoid false precision."
    )
yr_range = st.sidebar.slider("Year of disappearance", 1990, 2025, (2000, 2025))

# --------------------------------------------------------------------------- header
tab1, tab2 = st.tabs(["Stage 1: Official Data", "Stage 2: Clandestine Graves"])

with tab1:
    st.title("Mexico's disappeared — by the numbers")
    missing = metric_int(tot, "TotalDesaparecidos")
    located = metric_int(tot, "TotalLocalizados")
    dead = metric_int(tot, "TotalLocalizadosSV")
    glob = metric_int(tot, "TotalGlobal")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Still missing", f"{missing:,}")
    c2.metric("Since located", f"{located:,}", f"{located/glob:.0%} of all reports")
    c3.metric("Found dead", f"{dead:,}", "the Stage-2 anchor", delta_color="off")
    c4.metric("Total ever reported", f"{glob:,}")
    st.caption("Live RNPDNO dashboard totals. 'Found dead' = *localizadas sin vida* — the registry's "
               "closest proxy for recovery work by collectives and the state.")
    st.divider()

    # --------------------------------------------------------------------------- scale & outcomes
    st.header("1 · Scale & outcomes over time")
    lo, hi = yr_range
    d = yr[(yr.index >= lo) & (yr.index <= hi)]
    out = pd.DataFrame({
        "Found alive": d["loc_con_vida"], "Found dead": d["loc_sin_vida"],
        "Still missing": d["desap_y_nollocal"],
    }).reset_index(names="year")
    long = out.melt("year", var_name="outcome", value_name="people")
    long["people_display"] = long.apply(lambda row: -row["people"] if row["outcome"] == "Found alive" else row["people"], axis=1)
    norm = st.radio("Show", ["Absolute", "Share (100%)"], horizontal=True, label_visibility="collapsed")
    order = ["Found alive", "Found dead", "Still missing"]
    enc_y = alt.Y("people_display:Q", stack=("normalize" if norm.startswith("Share") else "zero"),
                  title=("Share" if norm.startswith("Share") else "People who disappeared"),
                  axis=alt.Axis(format=("%" if norm.startswith("Share") else "~s"), labelExpr="abs(datum.value)"))
    chart = (
        alt.Chart(long).mark_bar().encode(
            x=alt.X("year:O", title="Year of disappearance"),
            y=enc_y,
            color=alt.Color("outcome:N", scale=alt.Scale(domain=order, range=[ALIVE, DEAD, MISSING]),
                            legend=alt.Legend(title=None, orient="top")),
            order=alt.Order("outcome:N"),
            tooltip=["year", "outcome", alt.Tooltip("people:Q", format=",")],
        ).properties(height=380)
    )
    st.altair_chart(chart, use_container_width=True)
    still = int(d["desap_y_nollocal"].sum())
    st.caption(f"**{still:,}** people who disappeared {lo}–{hi} are still missing. The rise is real "
               "incidence (the 2006–07 militarized 'war on drugs' is the inflection), not a survivorship "
               "artifact — see docs/methodology.md.")
    st.divider()

    # --------------------------------------------------------------------------- geography
    st.header("2 · Geography")
    gcol1, gcol2 = st.columns([3, 2])
    with gcol1:
        metric_choice = st.radio("Rank states by", ["Per-capita rate (per 100k)", "Absolute count"],
                                 horizontal=True)
        if metric_choice.startswith("Per"):
            gdf = rates.sort_values("tasa_100k", ascending=False).head(15)
            xcol, xtitle, fmt = "tasa_100k", "Registered disappeared per 100,000", ".0f"
        else:
            gdf = rates.sort_values("desaparecidos", ascending=False).head(15)
            xcol, xtitle, fmt = "desaparecidos", "Registered disappeared (count)", ","
        bar = (
            alt.Chart(gdf).mark_bar(color=MISSING).encode(
                x=alt.X(f"{xcol}:Q", title=xtitle),
                y=alt.Y("entidad:N", sort="-x", title=None),
                tooltip=["entidad", alt.Tooltip(f"{xcol}:Q", format=fmt)],
            ).properties(height=420)
        )
        st.altair_chart(bar, use_container_width=True)
        st.caption("Count tracks population; the rate reveals intensity. They disagree sharply — "
                   "Edo. de México leads by count but falls below average per-capita.")
    with gcol2:
        img = FIG / "06_choropleth_rate.png"
        if img.exists():
            st.image(str(img), caption="Disappearance intensity per 100k (static choropleth).")

    st.divider()

    # --------------------------------------------------------------------------- opacity
    st.header("3 · Opacity — where the data goes dark")
    st.markdown("Redaction isn't uniform. This plots each state's **data opacity** (share of records "
                "withheld as `CONFIDENCIAL`) against the **scale** of its crisis, sized by local homicide rate.")
    o = opac.copy()
    o["confidential_share_pct"] = o.get("confidential_share_pct", o["confidential_share"] * 100)
    scatter = (
        alt.Chart(o).mark_circle(opacity=0.8).encode(
            x=alt.X("confidential_share:Q", title="Share of records redacted (CONFIDENCIAL)",
                    axis=alt.Axis(format="%")),
            y=alt.Y("tasa_100k:Q", title="Disappeared per 100k"),
            size=alt.Size("homicide_rate_2015_2025_per100k:Q", title="Homicide rate",
                          scale=alt.Scale(range=[30, 600])),
            color=alt.Color("opacity_typology:N", title="Typology",
                            scale=alt.Scale(scheme="set2")),
            tooltip=["entidad",
                     alt.Tooltip("confidential_share:Q", format=".0%", title="redacted"),
                     alt.Tooltip("tasa_100k:Q", title="per 100k"),
                     alt.Tooltip("homicide_rate_2015_2025_per100k:Q", format=",.0f", title="homicide rate")],
        ).properties(height=440).interactive()
    )
    st.altair_chart(scatter, use_container_width=True)
    nat_op = opac["confidential_share"].mean()
    st.caption(f"National redaction ≈ {nat_op:.0%}. High-opacity states (Jalisco, Nayarit) make their "
               "own counts hard to trust — opacity is a variable, not just noise.")

    st.divider()
    st.caption("Built with Streamlit · data in `data/processed/` · methodology in `docs/methodology.md`. "
               "Stage 2 (madres buscadoras) in progress.")

with tab2:
    st.title("Clandestine Graves: What the Records Show")

    @st.cache_data
    def load_stage2():
        """Both Stage-2 files, tagged by provenance. Either may be absent."""
        frames, missing = [], []
        for name in ("clandestine_finds.csv", "clandestine_finds_imported.csv"):
            path = STAGE2 / name
            if path.exists():
                frames.append(pd.read_csv(path))
            else:
                missing.append(name)
        if not frames:
            return None, missing
        combined = pd.concat(frames, ignore_index=True, sort=False)
        if "source_type" not in combined.columns:
            combined["source_type"] = "journalism"
        combined["source_type"] = combined["source_type"].fillna("journalism")
        return combined, missing

    fosas, missing = load_stage2()

    if fosas is None:
        st.error(
            "No Stage-2 data found. Expected `data/stage2/clandestine_finds.csv` "
            "and/or `data/stage2/clandestine_finds_imported.csv`. Rebuild the "
            "import with `python src/stage2_import.py`."
        )
        st.stop()
    if missing:
        st.warning(f"Stage-2 file(s) not found, showing what is present: {missing}")

    registry = fosas[fosas["source_type"] == "registry"]
    coded = fosas[fosas["source_type"] == "journalism"]

    # The single most important caveat on this tab. Stated before any number.
    st.warning(
        "**This tab cannot tell you what the madres buscadoras found.** "
        f"{len(registry):,} of these {len(fosas):,} rows come from the CNB / Quinto "
        "Elemento Lab grave registry, which records *that* a grave exists but not "
        "*who located it* — it has no attribution field at all. Their "
        "`led_by = state` is a missing column, not a finding. Only the "
        f"{len(coded)} hand-coded journalism rows carry real attribution, and they "
        "are illustrative seeds, not a sample anyone should generalise from."
    )

    st.subheader("Registry baseline")
    st.caption(
        "CNB / Quinto Elemento Lab clandestine-grave registry, consulted "
        "2023-10-06. One row is one registry grave record — not one search event, "
        "and not one person. Bodies and remains are not recorded in this source, "
        "so no body count can be derived from it."
    )

    graves = pd.to_numeric(registry["graves_found"], errors="coerce")
    m1, m2, m3 = st.columns(3)
    m1.metric("Graves recorded", f"{int(graves.sum()):,}")
    # Count (state, municipality) pairs: municipality names repeat across states
    # (Abasolo exists in both Nuevo León and Tamaulipas), so a name-only nunique
    # undercounts.
    n_muni = registry[["state", "municipality"]].drop_duplicates().shape[0]
    m2.metric("Municipalities", f"{n_muni:,}")
    m3.metric("States", f"{registry['state'].nunique():,}")

    st.divider()

    # ---------------------------------------------------------------- by state
    st.subheader("Recorded graves by state")
    by_state = (
        registry.assign(graves=graves)
        .groupby("state", as_index=False)["graves"]
        .sum()
        .sort_values("graves", ascending=False)
    )
    bar = (
        alt.Chart(by_state)
        .mark_bar(color=MISSING)
        .encode(
            x=alt.X("state:N", title="State", sort="-y",
                    axis=alt.Axis(labelAngle=-45, labelLimit=500)),
            y=alt.Y("graves:Q", title="Graves recorded"),
            tooltip=["state", alt.Tooltip("graves:Q", title="Graves recorded")],
        )
        .properties(height=400)
    )
    st.altair_chart(bar, use_container_width=True)
    st.caption(
        "Counts are of *recorded* graves. A state can rank low because little was "
        "found or because little was registered; this chart cannot separate the two."
    )

    st.divider()

    # ------------------------------------------------------------------- map
    st.subheader("Where records concentrate, by municipality")
    st.caption(
        "⚠️ Points are **municipal seats — town centres**, not grave sites. The "
        "source gives no grave coordinates, so every grave in a municipality is "
        "drawn at the same civic centre point. Read this as a municipality-level "
        "count, never as a location."
    )
    geo_cols = {"municipality_lat", "municipality_lon"}
    if geo_cols.issubset(fosas.columns):
        muni = (
            registry.assign(graves=graves)
            .dropna(subset=["municipality_lat", "municipality_lon"])
            .groupby(
                ["state", "municipality", "municipality_lat", "municipality_lon"],
                as_index=False,
            )["graves"]
            .sum()
        )
        ungeocoded = int(registry["municipality_lat"].isna().sum())
        if muni.empty:
            st.info("No municipal-seat coordinates available.")
        else:
            import pydeck as pdk

            # Area scales with the count, so 40 graves does not look like 4.
            muni["radius"] = (muni["graves"] ** 0.5) * 4500
            st.pydeck_chart(
                pdk.Deck(
                    map_style=None,
                    initial_view_state=pdk.ViewState(
                        latitude=23.6, longitude=-102.5, zoom=4.3, pitch=0
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=muni,
                            get_position="[municipality_lon, municipality_lat]",
                            get_radius="radius",
                            get_fill_color=[122, 31, 31, 140],
                            pickable=True,
                        )
                    ],
                    tooltip={
                        "text": "{municipality}, {state}\n{graves} graves recorded"
                    },
                )
            )
            if ungeocoded:
                st.caption(
                    f"{ungeocoded:,} records are not drawn: no municipal-seat "
                    "coordinate was available for their municipality."
                )
    else:
        st.info("This dataset carries no municipality coordinates.")

    st.divider()

    # --------------------------------------------------- hand-coded seed rows
    st.subheader(f"Hand-coded find events ({len(coded)})")
    if coded.empty:
        st.info("No journalism-coded rows present.")
    else:
        st.caption(
            "The only rows with real attribution. Far too few to generalise from — "
            "shown so the coding schema stays visible while the dataset grows. "
            "See docs/stage2-schema.md."
        )
        st.dataframe(
            coded[[
                "date", "state", "municipality", "collective", "led_by",
                "graves_found", "bodies_found", "confidence", "source_outlet",
            ]],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            f"Attribution among these {len(coded)} events: "
            + ", ".join(
                f"{k} {v}" for k, v in coded["led_by"].value_counts().items()
            )
            + ". A count this small is an illustration, not a measurement."
        )

    st.divider()
    st.caption(
        "Stage 2 is in progress. The question it exists to answer — how much "
        "recovery work is done by collectives versus the state — cannot be "
        "answered by either source here: the registry has no attribution, and the "
        "coded sample is tiny. Expanding the coded set is the work that remains."
    )
