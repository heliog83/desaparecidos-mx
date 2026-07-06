"""Fig 21: Jalisco's registry conflict — federal vs state totals + event timeline.

Documented snapshots only (markers, not a continuous series). Definitions differ
between registries; the chart shows divergence between documented quotes, not a
measured series. Sources (all consulted 2026-07-06):
- RNPDNO Apr 2022 ~14,944 and May 2023 15,012 (+68 in ~13 months while the state
  issued 1,260 search bulletins): El Informador 2023-05-09.
- SISOVID (state) 13,976 at 2023-03-31: El Informador 2023-05-09.
- REPD 15,426 at 2025-02-28 vs RNPDNO 15,015 at 2025-03-13: SinEmbargo / press.
- REPD 16,064 through end 2025: Grupo Animal (ex Animal Político) verification.
- RNPDNO 12,776 unresolved at 2026-06-19: our own dashboard-API pull
  (data/processed/flow_by_state.csv, desap_y_nollocal).
Events: CNB oficio 1349/2020 p.11 n.3; Informador/Animal Político (2022 stop);
Data Cívica (Dec 2023 censo/borrados); Proceso 2024-01-23 (denial); ZonaDocs
(Teuchitlán 2025-03-05); A dónde van los desaparecidos 2026-01-08 (new recount).
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import article_style as st
from datetime import date

st.apply()
C_FED, C_STATE, C_EVENT = st.RED, st.BLUE, st.INK

fed = [(date(2022, 4, 15), 14944), (date(2023, 5, 6), 15012),
       (date(2025, 3, 13), 15015), (date(2026, 6, 19), 12776)]
sta = [(date(2023, 3, 31), 13976), (date(2025, 2, 28), 15426),
       (date(2025, 12, 31), 16064)]

events = [
    (date(2020, 8, 12), "Fiscalía declares ALL its\nsubmissions non-publishable\n(CNB oficio to INAI)"),
    (date(2022, 3, 1), "State stops feeding\nthe federal registry"),
    (date(2023, 12, 14), 'Federal "censo";\nerased-names\ncontroversy'),
    (date(2024, 1, 23), '"Jalisco does not\nmanipulate its registry"\n(official denial)'),
    (date(2025, 3, 5), "Teuchitlán extermination site\nfound by Guerreros Buscadores"),
    (date(2026, 1, 8), "New federal\nrecount announced"),
]

fig, ax = plt.subplots(figsize=(11, 5.5))

for d, label in events:
    ax.axvline(d, color=C_EVENT, lw=0.8, ls=":", alpha=0.6, zorder=1)

ax.plot(*zip(*fed), color=C_FED, marker="o", ms=7, lw=1.5, ls="--", zorder=3,
        label="Federal registry (RNPDNO) — Jalisco unresolved")
ax.plot(*zip(*sta), color=C_STATE, marker="s", ms=7, lw=1.5, ls="--", zorder=3,
        label="Jalisco state registry (SISOVID/REPD)")

for d, v in fed:
    ax.annotate(f"{v:,}", (d, v), textcoords="offset points", xytext=(0, -16),
                ha="center", fontsize=8.5, color=C_FED, weight="bold")
for d, v in sta:
    ax.annotate(f"{v:,}", (d, v), textcoords="offset points", xytext=(0, 9),
                ha="center", fontsize=8.5, color=C_STATE, weight="bold")

# event labels staggered along the top; first one left-anchored so it clears the axis
tops = [16950, 18050, 16950, 18050, 16950, 18050]
for i, ((d, label), y) in enumerate(zip(events, tops)):
    ha = "left" if i == 0 else "center"
    ax.text(d, y, label, ha=ha, va="top", fontsize=7.5, color=C_EVENT)

# the freeze annotation
ax.annotate("federal count grew by only 68\nwhile the state issued 1,260\nsearch bulletins",
            xy=(date(2022, 10, 15), 14990), xytext=(date(2021, 6, 1), 13500),
            fontsize=8.5, color=C_FED, style="italic",
            arrowprops=dict(arrowstyle="-", color=C_FED, lw=0.8))

ax.set_ylim(12300, 18100)
ax.set_xlim(date(2020, 3, 1), date(2026, 11, 1))
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.spines[["top", "right"]].set_visible(False)
ax.set_title("One state, two registries: Jalisco's federal and state counts of the disappeared diverge",
             fontsize=13, weight="bold", loc="left", pad=14)
ax.legend(loc="lower left", frameon=False, fontsize=9)
ax.text(0, -0.13,
        "Markers are documented snapshots, not a continuous series; registry definitions differ. "
        "Sources: El Informador (2023-05-09), SinEmbargo (2025), Grupo Animal (2025), RNPDNO API pull "
        "(2026-06-19). Consulted 2026-07-06.",
        transform=ax.transAxes, fontsize=7.5, color="#666666")

fig.tight_layout()
fig.savefig("reports/figures/21_jalisco_registry_divergence.png", dpi=200, bbox_inches="tight")
print("wrote reports/figures/21_jalisco_registry_divergence.png")
st.save(fig, "F_jalisco_divergence.png")
