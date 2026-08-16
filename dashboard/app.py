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
PROC = ROOT / "data" / "processed"
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
tab1, tab2 = st.tabs(["Stage 1: Official Data", "Stage 2: Madres Buscadoras"])

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
    st.title("Madres Buscadoras: Clandestine Recoveries")
    try:
        fosas = pd.read_csv(ROOT / "data" / "stage2" / "clandestine_finds_imported.csv")
        
        # Metrics
        tot_graves = int(fosas["graves_found"].sum())
        tot_bodies = int(fosas["bodies_found"].sum()) if pd.notna(fosas["bodies_found"].sum()) else 0
        tot_remains = int(fosas["remains_bags"].sum()) if pd.notna(fosas["remains_bags"].sum()) else 0
        
        m1, m2, m3 = st.columns(3)
        if tot_bodies == 0 and tot_remains == 0:
            m1.metric("Total Graves", f"{tot_graves:,}")
            m2.metric("Municipalities Affected", int(fosas["municipality"].nunique()))
            
            top_state = fosas.groupby("state")["graves_found"].sum().idxmax()
            top_state_count = int(fosas.groupby("state")["graves_found"].sum().max())
            m3.metric("Top Hotspot State", f"{top_state} ({top_state_count:,})")
            
            st.caption("*Note: Figures reflect official CNB / Quinto Elemento Lab clandestine grave registries. Individual body and remains counts are unrecorded in official state entries.*")
        else:
            m1.metric("Total Graves", f"{tot_graves:,}")
            m2.metric("Total Bodies", f"{tot_bodies:,}")
            m3.metric("Total Remains Bags", f"{tot_remains:,}")
            
        st.divider()
        
        # Stacked bar chart
        st.subheader("Recoveries by Attribution")
        metric_choice = st.radio("Metric to plot", ["Total Graves", "Bodies / Remains"], horizontal=True, label_visibility="collapsed")
        
        if metric_choice == "Total Graves":
            fosas["chart_metric"] = fosas["graves_found"].fillna(0)
            y_title = "Total Graves"
        else:
            fosas["chart_metric"] = fosas["bodies_found"].fillna(0) + fosas["remains_bags"].fillna(0)
            y_title = "Total Recoveries (Bodies + Remains)"

        fosas["source_dataset"] = fosas["source_outlet"].fillna("Unknown Source")
        bar = alt.Chart(fosas).mark_bar().encode(
            x=alt.X("state:N", title="State", sort="-y", axis=alt.Axis(labelAngle=-45, labelLimit=500)),
            y=alt.Y("chart_metric:Q", title=y_title),
            color=alt.Color("led_by:N", title="Led By", scale=alt.Scale(domain=["collective", "state", "unknown"], range=["#7a1f1f", "#7d9bb5", "#cccccc"])),
            tooltip=["state", "municipality", "collective", "led_by", alt.Tooltip("chart_metric:Q", title=y_title), alt.Tooltip("source_dataset:N", title="Source")]
        ).properties(height=400)
        st.altair_chart(bar, use_container_width=True)
        st.divider()
        
        # Map
        st.subheader("Grave Locations")
        map_layer = st.radio("Map Style", ["Scatter Pins", "Density Heatmap"], horizontal=True, label_visibility="collapsed")
        map_data = fosas.dropna(subset=["lat", "lon"])
        if not map_data.empty:
            import pydeck as pdk
            
            if map_layer == "Density Heatmap":
                layer = pdk.Layer(
                    "HeatmapLayer",
                    data=map_data,
                    opacity=0.9,
                    get_position=["lon", "lat"],
                    get_weight="graves_found",
                    radiusPixels=30,
                    colorRange=[
                        [122, 31, 31],     # Dark red
                        [217, 72, 1],      # Orange
                        [241, 105, 19],
                        [253, 141, 60],
                        [253, 174, 107],
                        [255, 255, 255],   # White (peak hotspots)
                    ]
                )
            else:
                layer = pdk.Layer(
                    'ScatterplotLayer',
                    data=map_data,
                    get_position='[lon, lat]',
                    get_color='[122, 31, 31, 200]',
                    get_radius=20000,
                )

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=23.6,
                    longitude=-102.5,
                    zoom=4.5,
                    pitch=0,
                ),
                layers=[layer],
            ))
        else:
            st.info("No geocoded locations available for mapping.")
    except Exception as e:
        st.error(f"Could not load Stage 2 data: {e}")
