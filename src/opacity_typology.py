"""
Opacity typology by state — figs 14–15 (typology colored, profiles).

Extracted verbatim from notebooks/05_opacity_typology_by_state.ipynb so the opacity figures are
reproducible from src/ like the rest of the pipeline.

Run:  python src/opacity_typology.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# Jupyter's display() isn't defined outside a notebook; fall back to print for parity.
display = print

ROOT = Path(__file__).resolve().parents[1]

PROCESSED = ROOT / "data" / "processed"
FIGDIR = ROOT / "reports" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

INK = "#2b2b2b"
RED = "#7a1f1f"
BLUE = "#3b5b7a"
GOLD = "#9a6b1f"
GREEN = "#4f6f52"
MUTED = "#8b8b8b"

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 130,
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": MUTED,
    "axes.titleweight": "bold",
    "axes.titlecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
})

state = pd.read_csv(PROCESSED / "state_opacity_model.csv")
records = pd.read_csv(ROOT / "data" / "external" / "data.csv", dtype="string", usecols=["ESTATUS_VICTIMA"])

scale_cutoff = state["total_records"].median()
opacity_cutoff = records["ESTATUS_VICTIMA"].eq("CONFIDENCIAL").mean()

print(f"Scale cutoff, median state total: {scale_cutoff:,.0f}")
print(f"Opacity cutoff, national CONFIDENCIAL share: {opacity_cutoff:.1%}")

def assign_typology(row):
    high_scale = row["total_records"] >= scale_cutoff
    high_opacity = row["confidential_share"] >= opacity_cutoff
    if high_scale and high_opacity:
        return "High scale / high opacity"
    if high_scale and not high_opacity:
        return "High scale / lower opacity"
    if not high_scale and high_opacity:
        return "Lower scale / high opacity"
    return "Lower scale / lower opacity"

state["opacity_typology"] = state.apply(assign_typology, axis=1)
state["scale_distance_from_cutoff"] = state["total_records"] - scale_cutoff
state["opacity_distance_from_cutoff"] = state["confidential_share"] - opacity_cutoff
state["confidential_share_pct"] = state["confidential_share"] * 100

state.to_csv(PROCESSED / "state_opacity_typology.csv", index=False)

state[[
    "entidad",
    "opacity_typology",
    "total_records",
    "confidential_records",
    "confidential_share",
    "tasa_100k",
]].sort_values(["opacity_typology", "confidential_share"], ascending=[True, False])

type_order = [
    "High scale / high opacity",
    "High scale / lower opacity",
    "Lower scale / high opacity",
    "Lower scale / lower opacity",
]

for typology in type_order:
    subset = state[state["opacity_typology"].eq(typology)].sort_values(
        ["confidential_share", "confidential_records"], ascending=False
    )
    print(f"\n{typology} ({len(subset)} states)")
    display(subset[[
        "entidad",
        "total_records",
        "confidential_records",
        "confidential_share",
        "tasa_100k",
    ]])

palette = {
    "High scale / high opacity": RED,
    "High scale / lower opacity": BLUE,
    "Lower scale / high opacity": GOLD,
    "Lower scale / lower opacity": GREEN,
}

fig, ax = plt.subplots(figsize=(9, 6.4))

for typology in type_order:
    subset = state[state["opacity_typology"].eq(typology)]
    ax.scatter(
        subset["total_records"],
        subset["confidential_share"],
        s=np.sqrt(subset["confidential_records"]) * 5,
        color=palette[typology],
        alpha=0.78,
        edgecolor="white",
        linewidth=0.8,
        label=typology,
    )

ax.axvline(scale_cutoff, color=MUTED, linestyle="--", linewidth=1)
ax.axhline(opacity_cutoff, color=MUTED, linestyle="--", linewidth=1)

label_states = set(state.nlargest(7, "confidential_records")["entidad"])
label_states |= set(state.nlargest(7, "confidential_share")["entidad"])
label_states |= {"GUERRERO", "CHIHUAHUA", "COLIMA"}

for row in state[state["entidad"].isin(label_states)].itertuples(index=False):
    ax.text(row.total_records, row.confidential_share, f" {row.entidad.title()}", fontsize=7)

ax.set_title("State opacity typology: scale vs. intensity")
ax.set_xlabel("Total unresolved records")
ax.set_ylabel("Share marked CONFIDENCIAL")
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.legend(frameon=False, fontsize=8, loc="lower right")
ax.text(
    0,
    -0.16,
    "Bubble size scales with confidential-record count. Cutoffs: median state total and national confidential share.",
    transform=ax.transAxes,
    fontsize=8,
    color=MUTED,
)

fig.tight_layout()
fig.savefig(FIGDIR / "14_opacity_typology_colored.png", bbox_inches="tight")
plt.show()

strategy = pd.DataFrame([
    {
        "typology": "High scale / high opacity",
        "interpretation": "Many unresolved people and a large share hidden from detailed public analysis.",
        "research_strategy": "Priority cases for source triangulation, state policy review, and historical snapshot checks.",
    },
    {
        "typology": "High scale / lower opacity",
        "interpretation": "Large crisis, but comparatively more public detail is available.",
        "research_strategy": "Good for substantive pattern analysis by date, sex, age, municipality, and rate.",
    },
    {
        "typology": "Lower scale / high opacity",
        "interpretation": "Smaller state total, but public detail is heavily limited.",
        "research_strategy": "Investigate publication rules; avoid overreading state trends because few detailed records remain.",
    },
    {
        "typology": "Lower scale / lower opacity",
        "interpretation": "Smaller state total and comparatively lower redaction.",
        "research_strategy": "Use as contrast cases, not as proof of better institutions without external validation.",
    },
])

strategy

profiles = (
    state.groupby("opacity_typology")
    .agg(
        states=("entidad", "count"),
        total_records=("total_records", "sum"),
        confidential_records=("confidential_records", "sum"),
        mean_confidential_share=("confidential_share", "mean"),
        median_rate_100k=("tasa_100k", "median"),
        median_homicide_rate=("homicide_rate_2015_2025_per100k", "median"),
    )
    .reindex(type_order)
    .reset_index()
)
profiles["share_of_all_confidential_records"] = profiles["confidential_records"] / state["confidential_records"].sum()
profiles

fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

colors = [palette[t] for t in profiles["opacity_typology"]]

axes[0].barh(profiles["opacity_typology"], profiles["confidential_records"], color=colors)
axes[0].set_title("Confidential records by typology")
axes[0].xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
for i, row in enumerate(profiles.itertuples(index=False)):
    axes[0].text(row.confidential_records, i, f" {row.confidential_records:,.0f}", va="center", fontsize=8)

axes[1].barh(profiles["opacity_typology"], profiles["mean_confidential_share"], color=colors)
axes[1].set_title("Mean confidential share by typology")
axes[1].xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
for i, row in enumerate(profiles.itertuples(index=False)):
    axes[1].text(row.mean_confidential_share, i, f" {row.mean_confidential_share:.0%}", va="center", fontsize=8)

fig.tight_layout()
fig.savefig(FIGDIR / "15_opacity_typology_profiles.png", bbox_inches="tight")
plt.show()

state["scale_distance_pct_of_cutoff"] = state["scale_distance_from_cutoff"] / scale_cutoff
state["opacity_distance_points"] = state["opacity_distance_from_cutoff"] * 100

borderline = state[
    state["scale_distance_pct_of_cutoff"].abs().le(0.25)
    | state["opacity_distance_points"].abs().le(5)
].copy()

borderline[[
    "entidad",
    "opacity_typology",
    "total_records",
    "scale_distance_pct_of_cutoff",
    "confidential_share",
    "opacity_distance_points",
]].sort_values("opacity_distance_points")

priority = []
for typology in type_order:
    subset = state[state["opacity_typology"].eq(typology)].copy()
    if typology == "High scale / high opacity":
        subset = subset.sort_values("confidential_records", ascending=False)
    elif typology == "High scale / lower opacity":
        subset = subset.sort_values("total_records", ascending=False)
    elif typology == "Lower scale / high opacity":
        subset = subset.sort_values("confidential_share", ascending=False)
    else:
        subset = subset.sort_values("confidential_share")
    priority.append(subset.head(3))

priority = pd.concat(priority)
priority[[
    "entidad",
    "opacity_typology",
    "total_records",
    "confidential_records",
    "confidential_share",
    "tasa_100k",
    "homicide_rate_2015_2025_per100k",
]]
