"""
Confidentiality / opacity baseline — figs 08–10 (status mix, share by state, scale-vs-intensity).

Extracted verbatim from notebooks/03_confidentiality_and_opacity.ipynb so the opacity figures are
reproducible from src/ like the rest of the pipeline.

Run:  python src/opacity_confidentiality.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

CSV = ROOT / "data" / "external" / "data.csv"
FIGDIR = ROOT / "reports" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV, dtype="string")
df["is_confidential"] = df["ESTATUS_VICTIMA"].eq("CONFIDENCIAL")

INK = "#2b2b2b"
RED = "#7a1f1f"
MUTED = "#8b8b8b"
BLUE = "#3b5b7a"

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

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")

status = (
    df["ESTATUS_VICTIMA"]
    .value_counts(dropna=False)
    .rename_axis("status")
    .reset_index(name="records")
)
status["share"] = status["records"] / len(df)
status

plot_status = status.sort_values("records")

fig, ax = plt.subplots(figsize=(7, 3.8))
colors = [RED if s == "CONFIDENCIAL" else INK for s in plot_status["status"]]
ax.barh(plot_status["status"], plot_status["records"], color=colors)
ax.set_title("Status mix in the local RNPDNO mirror")
ax.set_xlabel("Records")
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))

for i, row in enumerate(plot_status.itertuples(index=False)):
    ax.text(row.records, i, f" {row.records:,.0f} ({row.share:.1%})", va="center", fontsize=9)

fig.tight_layout()
fig.savefig(FIGDIR / "08_status_mix_confidential.png", bbox_inches="tight")
plt.show()

fields = [
    "ID_VICTIMA",
    "ORIGEN_REPORTE",
    "FECHA_NACIMIENTO",
    "SEXO",
    "FECHA_DESAPARICION",
    "FECHA_REGISTRO",
    "ESTATUS_VICTIMA",
    "ENTIDAD",
    "MUNICIPIO",
]

availability = []
for status_value, sub in df.groupby("ESTATUS_VICTIMA", dropna=False):
    for field in fields:
        missing = sub[field].isna() | sub[field].eq("") | sub[field].eq("CONFIDENCIAL")
        availability.append({
            "status": status_value,
            "field": field,
            "available_share": round((~missing).mean(), 3),
        })

availability_table = (
    pd.DataFrame(availability)
    .pivot(index="field", columns="status", values="available_share")
    .reset_index()
)
availability_table

state_opacity = (
    df.groupby("ENTIDAD", dropna=False)
    .agg(
        total_records=("ID_VICTIMA", "size"),
        confidential_records=("is_confidential", "sum"),
    )
    .reset_index()
)
state_opacity["confidential_share"] = state_opacity["confidential_records"] / state_opacity["total_records"]

state_opacity.sort_values("confidential_share", ascending=False).head(12)

min_records = 1000
top_share = (
    state_opacity[state_opacity["total_records"] >= min_records]
    .sort_values("confidential_share", ascending=False)
    .head(15)
    .sort_values("confidential_share")
)

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(top_share["ENTIDAD"], top_share["confidential_share"], color=RED)
ax.set_title("States with the highest confidential-record share")
ax.set_xlabel("Share of records marked CONFIDENCIAL")
ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))

national_share = df["is_confidential"].mean()
ax.axvline(national_share, color=INK, linestyle="--", linewidth=1)
ax.text(national_share, -0.75, f" national {national_share:.0%}", fontsize=8)

for i, row in enumerate(top_share.itertuples(index=False)):
    ax.text(row.confidential_share, i, f" {row.confidential_share:.0%}", va="center", fontsize=8)

ax.text(
    0,
    -0.14,
    f"Only states with at least {min_records:,} total records. This measures public-data opacity, not proven intent.",
    transform=ax.transAxes,
    fontsize=8,
    color=MUTED,
)

fig.tight_layout()
fig.savefig(FIGDIR / "09_confidential_share_by_state.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(
    state_opacity["total_records"],
    state_opacity["confidential_share"],
    s=(state_opacity["confidential_records"] ** 0.5) * 3,
    color=BLUE,
    alpha=0.75,
    edgecolor="white",
    linewidth=0.6,
)
ax.set_title("Opacity has both scale and intensity")
ax.set_xlabel("Total unresolved records by state")
ax.set_ylabel("Share marked CONFIDENCIAL")
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))

label_states = set(
    state_opacity.nlargest(5, "confidential_records")["ENTIDAD"]
).union(state_opacity.nlargest(5, "confidential_share")["ENTIDAD"])

for row in state_opacity[state_opacity["ENTIDAD"].isin(label_states)].itertuples(index=False):
    ax.text(row.total_records, row.confidential_share, f" {row.ENTIDAD}", fontsize=7)

ax.text(
    0,
    -0.16,
    "Bubble size scales with confidential-record count. Labels mark the top states by count or share.",
    transform=ax.transAxes,
    fontsize=8,
    color=MUTED,
)

fig.tight_layout()
fig.savefig(FIGDIR / "10_confidential_scale_vs_intensity.png", bbox_inches="tight")
plt.show()
