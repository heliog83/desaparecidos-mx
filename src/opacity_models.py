"""
Opacity patterns & models — figs 11–13 (typology, correlations, regression coefficients).

Extracted verbatim from notebooks/04_opacity_patterns_and_models.ipynb so the opacity figures are
reproducible from src/ like the rest of the pipeline.

Run:  python src/opacity_models.py
"""
from pathlib import Path
import unicodedata

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

FIGDIR = ROOT / "reports" / "figures"
PROCESSED = ROOT / "data" / "processed"
FIGDIR.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

def norm_state(value):
    if pd.isna(value):
        return value
    value = str(value).upper().strip()
    return "".join(
        c for c in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(c)
    )

INK = "#2b2b2b"
RED = "#7a1f1f"
BLUE = "#3b5b7a"
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

records = pd.read_csv(ROOT / "data" / "external" / "data.csv", dtype="string")
records["state_key"] = records["ENTIDAD"].map(norm_state)
records["is_confidential"] = records["ESTATUS_VICTIMA"].eq("CONFIDENCIAL")

state = (
    records.groupby("state_key")
    .agg(
        entidad=("ENTIDAD", "first"),
        total_records=("ID_VICTIMA", "size"),
        confidential_records=("is_confidential", "sum"),
    )
    .reset_index()
)
state["confidential_share"] = state["confidential_records"] / state["total_records"]

known = records[~records["is_confidential"]]
cat = known.groupby("state_key")["ESTATUS_VICTIMA"].value_counts().unstack(fill_value=0).reset_index()
cat["known_records"] = cat.get("DESAPARECIDA", 0) + cat.get("NO LOCALIZADA", 0)
cat["no_localizada_share_known"] = cat.get("NO LOCALIZADA", 0) / cat["known_records"].replace(0, np.nan)
state = state.merge(cat[["state_key", "known_records", "no_localizada_share_known"]], on="state_key", how="left")

rates = pd.read_csv(PROCESSED / "state_rates.csv", dtype={"cve_ent": "string"})
rates["state_key"] = rates["entidad"].map(norm_state)
state = state.merge(rates[["state_key", "tasa_100k", "poblacion"]], on="state_key", how="left")

flow = pd.read_csv(PROCESSED / "flow_by_state.csv").rename(columns={"Unnamed: 0": "state_name"})
flow["state_key"] = flow["state_name"].map(norm_state)
flow["located_dead_share_all_disappeared"] = flow["loc_sin_vida"] / flow["todos"].replace(0, np.nan)
flow["still_missing_share_flow"] = flow["desap_y_nollocal"] / flow["todos"].replace(0, np.nan)
state = state.merge(
    flow[["state_key", "todos", "loc_sin_vida", "located_dead_share_all_disappeared", "still_missing_share_flow"]],
    on="state_key",
    how="left",
)

victims = pd.read_csv(
    ROOT / "data" / "external" / "assets" / "timeseries_victimas.csv",
    usecols=["PERIODO", "ENTIDAD", "DELITO", "TOTAL"],
)
victims["year"] = pd.to_datetime(victims["PERIODO"]).dt.year
homicide = victims[
    victims["year"].between(2015, 2025)
    & victims["DELITO"].eq("Homicidio doloso")
].copy()
homicide["state_key"] = homicide["ENTIDAD"].map(norm_state)
homicide = (
    homicide.groupby("state_key")["TOTAL"]
    .sum()
    .rename("homicidio_doloso_victims_2015_2025")
    .reset_index()
)
state = state.merge(homicide, on="state_key", how="left")
state["homicide_rate_2015_2025_per100k"] = (
    state["homicidio_doloso_victims_2015_2025"] / state["poblacion"] * 100_000
)

# SE DESCONOCE is analytically important, but it is not a state. Exclude it from state models.
state_model = state[state["state_key"].ne("SE DESCONOCE")].copy()
state_model.to_csv(PROCESSED / "state_opacity_model.csv", index=False)

state_model.sort_values("confidential_share", ascending=False).head(12)[[
    "entidad",
    "total_records",
    "confidential_share",
    "tasa_100k",
    "no_localizada_share_known",
    "located_dead_share_all_disappeared",
    "homicide_rate_2015_2025_per100k",
]]

plot = state_model.copy()
x_cut = plot["total_records"].median()
y_cut = records["is_confidential"].mean()

fig, ax = plt.subplots(figsize=(8.5, 6))
sizes = np.sqrt(plot["confidential_records"]) * 4
ax.scatter(
    plot["total_records"],
    plot["confidential_share"],
    s=sizes,
    color=BLUE,
    alpha=0.72,
    edgecolor="white",
    linewidth=0.7,
)

ax.axvline(x_cut, color=MUTED, linestyle="--", linewidth=1)
ax.axhline(y_cut, color=MUTED, linestyle="--", linewidth=1)

labels = set(plot.nlargest(6, "confidential_records")["entidad"])
labels |= set(plot.nlargest(6, "confidential_share")["entidad"])
for row in plot[plot["entidad"].isin(labels)].itertuples(index=False):
    ax.text(row.total_records, row.confidential_share, f" {row.entidad.title()}", fontsize=7)

ax.text(x_cut * 1.05, y_cut + 0.025, "high scale / high share", fontsize=8, color=RED)
ax.text(x_cut * 1.05, y_cut - 0.065, "high scale / lower share", fontsize=8, color=MUTED)
ax.text(plot["total_records"].min(), y_cut + 0.025, "lower scale / high share", fontsize=8, color=MUTED)

ax.set_title("Opacity typology by state")
ax.set_xlabel("Total unresolved records")
ax.set_ylabel("Share marked CONFIDENCIAL")
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.text(
    0,
    -0.15,
    "Bubble size scales with confidential-record count. Vertical line = median state total; horizontal line = national confidential share.",
    transform=ax.transAxes,
    fontsize=8,
    color=MUTED,
)

fig.tight_layout()
fig.savefig(FIGDIR / "11_opacity_typology.png", bbox_inches="tight")
plt.show()

predictors = {
    "total_records": "Total unresolved records",
    "tasa_100k": "Unresolved rate per 100k",
    "no_localizada_share_known": "No-localizada share among known",
    "located_dead_share_all_disappeared": "Located-dead share",
    "still_missing_share_flow": "Still-missing share, live flow",
    "homicide_rate_2015_2025_per100k": "Homicide victim rate 2015-2025",
}

correlations = []
for col, label in predictors.items():
    sub = state_model[["confidential_share", col]].replace([np.inf, -np.inf], np.nan).dropna()
    correlations.append({
        "predictor": col,
        "label": label,
        "n_states": len(sub),
        "correlation_with_confidential_share": sub.corr().iloc[0, 1],
    })

corr = pd.DataFrame(correlations).sort_values("correlation_with_confidential_share")
corr

fig, ax = plt.subplots(figsize=(8, 4.6))
colors = [RED if v > 0 else BLUE for v in corr["correlation_with_confidential_share"]]
ax.barh(corr["label"], corr["correlation_with_confidential_share"], color=colors)
ax.axvline(0, color=INK, linewidth=1)
ax.set_title("Simple correlations with confidential-record share")
ax.set_xlabel("Pearson correlation")
ax.set_xlim(-1, 1)
for i, row in enumerate(corr.itertuples(index=False)):
    ax.text(
        row.correlation_with_confidential_share,
        i,
        f" {row.correlation_with_confidential_share:+.2f} (n={row.n_states})",
        va="center",
        fontsize=8,
    )
ax.text(
    0,
    -0.2,
    "Weak correlations are a finding: opacity is not explained by a single obvious crisis-intensity variable.",
    transform=ax.transAxes,
    fontsize=8,
    color=MUTED,
)
fig.tight_layout()
fig.savefig(FIGDIR / "12_opacity_correlations.png", bbox_inches="tight")
plt.show()

reg_predictors = [
    "tasa_100k",
    "no_localizada_share_known",
    "located_dead_share_all_disappeared",
    "homicide_rate_2015_2025_per100k",
    "total_records",
]

reg = state_model[["entidad", "confidential_share"] + reg_predictors].replace([np.inf, -np.inf], np.nan).dropna().copy()
X = reg[reg_predictors].copy()
X["log_total_records"] = np.log1p(X.pop("total_records"))

Xz = (X - X.mean()) / X.std(ddof=0)
y = reg["confidential_share"]
yz = (y - y.mean()) / y.std(ddof=0)

A = np.column_stack([np.ones(len(Xz)), Xz.values])
coef = np.linalg.lstsq(A, yz.values, rcond=None)[0]
pred = A @ coef
r2 = 1 - ((yz.values - pred) ** 2).sum() / ((yz.values - yz.mean()) ** 2).sum()

coef_table = pd.DataFrame({
    "predictor": ["intercept"] + list(Xz.columns),
    "standardized_coefficient": coef,
})
coef_table = coef_table[coef_table["predictor"].ne("intercept")].copy()
coef_table["abs_coef"] = coef_table["standardized_coefficient"].abs()
coef_table = coef_table.sort_values("standardized_coefficient")

print(f"States in model: {len(reg)}")
print(f"R-squared: {r2:.3f}")
coef_table[["predictor", "standardized_coefficient"]]

label_map = {
    "tasa_100k": "Unresolved rate per 100k",
    "no_localizada_share_known": "No-localizada share among known",
    "located_dead_share_all_disappeared": "Located-dead share",
    "homicide_rate_2015_2025_per100k": "Homicide victim rate 2015-2025",
    "log_total_records": "Log total unresolved records",
}
plot_coef = coef_table.copy()
plot_coef["label"] = plot_coef["predictor"].map(label_map)

fig, ax = plt.subplots(figsize=(8, 4.6))
colors = [RED if v > 0 else BLUE for v in plot_coef["standardized_coefficient"]]
ax.barh(plot_coef["label"], plot_coef["standardized_coefficient"], color=colors)
ax.axvline(0, color=INK, linewidth=1)
ax.set_title("Standardized regression coefficients for confidential share")
ax.set_xlabel("Coefficient, standardized scale")
for i, row in enumerate(plot_coef.itertuples(index=False)):
    ax.text(row.standardized_coefficient, i, f" {row.standardized_coefficient:+.2f}", va="center", fontsize=8)
ax.text(
    0,
    -0.22,
    f"OLS clue model, n={len(reg)} states, R2={r2:.2f}. Coefficients are not causal and are unstable with so few observations.",
    transform=ax.transAxes,
    fontsize=8,
    color=MUTED,
)
fig.tight_layout()
fig.savefig(FIGDIR / "13_opacity_regression_coefficients.png", bbox_inches="tight")
plt.show()
