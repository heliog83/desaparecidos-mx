"""Fig 21: Jalisco's registry conflict — federal vs state totals + event timeline.

Documented snapshots only (markers, not a continuous series). Definitions differ
between registries; the chart shows divergence between documented quotes, not a
measured series. Sources (all consulted 2026-07-06):
- RNPDNO Apr 2022 ~14,944 and May 2023 15,012 (+68 in ~13 months while the state
  issued 1,260 search bulletins): El Informador 2023-05-09.
- SISOVID (state) 13,976 at 2023-03-31: El Informador 2023-05-09.
- REPD 15,426 at 2025-02-28 vs RNPDNO 15,015 at 2025-03-13: SinEmbargo / press.
- REPD 16,064 through end 2025: Grupo Animal (ex Animal Político) verification.
- RNPDNO 12,964 unresolved at 2026-08-15: the publication freeze's dashboard-API
  pull (derived/flow_by_state.csv, desap_y_nollocal).
  (2026-10-12: a 2026-06-19 point, 12,776, was dropped. That pull was overwritten
  and never archived, so the value could not be verified.)
Events: CNB oficio 1349/2020 p.11 n.3; Informador/Animal Político (2022 stop);
Data Cívica (Dec 2023 censo/borrados); Proceso 2024-01-23 (denial); ZonaDocs
(Teuchitlán 2025-03-05); A dónde van los desaparecidos 2026-01-08 (new recount).
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec

import article_style as st
from datetime import date

st.apply()
C_FED, C_STATE, C_EVENT = st.RED, st.BLUE, st.INK

fed = [(date(2022, 4, 15), 14944), (date(2023, 5, 6), 15012),
       (date(2025, 3, 13), 15015), (date(2026, 8, 15), 12964)]
sta = [(date(2023, 3, 31), 13976), (date(2025, 2, 28), 15426),
       (date(2025, 12, 31), 16064)]

events = [
    (date(2020, 8, 12), "Fiscalía declares all its submissions non-publishable (CNB oficio to INAI)"),
    (date(2022, 3, 1), "State stops feeding the federal registry"),
    (date(2023, 12, 14), "Federal \u201Ccenso\u201D; erased-names controversy"),
    (date(2024, 1, 23), "\u201CJalisco does not manipulate its registry\u201D (official denial)"),
    (date(2025, 3, 5), "Teuchitlán extermination site found by Guerreros Buscadores"),
    (date(2026, 1, 8), "New federal recount announced"),
]

fig = plt.figure(figsize=(11.5, 7.6))
# Events used to be vertical lines carrying stacked text through the plot area, where
# the labels collided with each other and with the data. They now live in their own
# strip under the axis, numbered, with the wording in a key below.
gs = GridSpec(2, 1, height_ratios=[5, 1], hspace=0.08, figure=fig)
ax = fig.add_subplot(gs[0])
axe = fig.add_subplot(gs[1], sharex=ax)

XMIN, XMAX = date(2020, 3, 1), date(2026, 11, 1)

for i, (d, _) in enumerate(events, 1):
    ax.axvline(d, color=C_EVENT, lw=0.7, ls=":", alpha=0.28, zorder=1)

# Connectors show the ORDER of documented quotes, not a measured path between them.
ax.plot(*zip(*fed), color=C_FED, lw=1.0, ls=(0, (5, 4)), alpha=0.55, zorder=2)
ax.plot(*zip(*sta), color=C_STATE, lw=1.0, ls=(0, (5, 4)), alpha=0.55, zorder=2)
ax.scatter(*zip(*fed), color=C_FED, marker="o", s=58, zorder=3,
           label="Federal registry (RNPDNO)")
ax.scatter(*zip(*sta), color=C_STATE, marker="s", s=58, zorder=3,
           label="Jalisco state registry (SISOVID / REPD)")

fed_offsets = [(0, -17)] * len(fed)
for (d, v), off in zip(fed, fed_offsets):
    ax.annotate(f"{v:,}", (d, v), textcoords="offset points", xytext=off,
                ha="center", fontsize=9, color=C_FED, weight="bold")
sta_offsets = [(0, -18)] + [(0, 10)] * (len(sta) - 1)
for (d, v), off in zip(sta, sta_offsets):
    ax.annotate(f"{v:,}", (d, v), textcoords="offset points", xytext=off,
                ha="center", fontsize=9, color=C_STATE, weight="bold")

# The freeze: anchored to the span it describes rather than floating.
ax.annotate("", xy=(fed[0][0], 14580), xytext=(fed[1][0], 14580),
            arrowprops=dict(arrowstyle="<->", color=C_FED, lw=1.0))
ax.text(date(2022, 10, 25), 14430,
        "federal count grew by 68 in 13 months\nwhile the state issued 1,260 search bulletins",
        ha="center", va="top", fontsize=8.5, color=C_FED, style="italic")

ax.set_ylim(12300, 16900)
ax.set_xlim(XMIN, XMAX)
ax.set_ylabel("People recorded disappeared in Jalisco")
ax.grid(axis="y", color=st.MUTED, alpha=0.2, lw=0.7)
ax.set_axisbelow(True)
ax.spines[["top", "right", "bottom"]].set_visible(False)
ax.tick_params(axis="x", length=0, labelbottom=False)
ax.legend(loc="upper left", frameon=False, fontsize=9.5)
ax.set_title("One state, two registries: Jalisco's federal and state counts diverge",
             fontsize=13.5, weight="bold", loc="left", pad=30)
ax.text(0, 1.015, "Documented snapshots only. The dashed connector shows the order of "
                  "published quotes, not a measured path between them.",
        transform=ax.transAxes, fontsize=9.5, color=st.MUTED)

# ---- event strip -------------------------------------------------------------
axe.set_xlim(XMIN, XMAX)
axe.set_ylim(0, 1)
axe.axhline(0.62, color=st.MUTED, lw=0.9)
for i, (d, _) in enumerate(events, 1):
    axe.plot([d], [0.62], marker="o", ms=15, color=st.PAPER,
             mec=C_EVENT, mew=1.0, zorder=3)
    axe.text(d, 0.62, str(i), ha="center", va="center", fontsize=8.5,
             color=C_EVENT, weight="bold", zorder=4)
axe.xaxis.set_major_locator(mdates.YearLocator())
axe.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
axe.set_yticks([])
axe.spines[["top", "left", "right"]].set_visible(False)
axe.tick_params(axis="x", labelsize=10)

col = [events[:3], events[3:]]
for c, (chunk, x) in enumerate(zip(col, (0.055, 0.53))):
    start = c * 3
    text = "\n".join(f"({start + i + 1})  {label}" for i, (_, label) in enumerate(chunk))
    fig.text(x, 0.175, text, fontsize=8.5, color=C_EVENT, va="top", linespacing=1.9)

fig.text(0.055, 0.022,
         "Markers are documented snapshots, not a continuous series, and the two registries define their populations\n"
         "differently, so the gap between them is not a measured undercount. Sources: El Informador (2023-05-09), SinEmbargo\n"
         "(2025), Grupo Animal (2025), RNPDNO API pull (2026-08-15). Consulted 2026-08-15.",
         fontsize=7.5, color="#666666", va="bottom")

fig.subplots_adjust(left=0.075, right=0.98, top=0.90, bottom=0.27)
fig.savefig("reports/figures/21_jalisco_registry_divergence.png", dpi=200)
print("wrote reports/figures/21_jalisco_registry_divergence.png")
st.save(fig, "F_jalisco_divergence.png")
