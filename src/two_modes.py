"""Fig 22: the thesis chart — two modes of registry opacity (Jalisco vs Guerrero).

Left: Jalisco redacts what it records (mirror microdata: 13,766 unresolved, 9,216
CONFIDENCIAL = 66.9%; ZonaDocs 2024-11-21 found 1,026 Jalisco confidential records
with ACTIVE public search notices). Right: Guerrero records little confidentially
(9.1%) but under-records — in Iguala alone three collectives document 623 cases
(Tlachinollan, consulted 2026-07-06) against ~3,800 registered statewide.
IMPORTANT: the two panels use different denominators and the Iguala figure is a
documented example, NOT a comparable measurement or a census.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import article_style as st

st.apply()
C_CONF, C_KNOWN, C_COLL, C_GREY = st.RED, st.SAND, st.BLUE, st.INK

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.4))
fig.suptitle("Two ways information can disappear from public view", fontsize=14,
             weight="bold", x=0.02, ha="left")


def evidence_box(ax, x, y, w, h, text, face, text_color=st.INK):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.015",
                           facecolor=face, edgecolor="none")
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=9.5, color=text_color, weight="bold")


for ax in (ax1, ax2):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

# Jalisco: a measured path inside the registry.
ax1.set_title("JALISCO — recorded, then redacted", loc="left", fontsize=11,
              weight="bold", color=C_CONF, pad=12)
evidence_box(ax1, 0.06, 0.67, 0.88, 0.16, "13,766 unresolved records\nin the Dec-2025 public mirror", C_KNOWN)
ax1.annotate("", xy=(0.5, 0.62), xytext=(0.5, 0.67),
             arrowprops=dict(arrowstyle="->", color=C_GREY, lw=1.2))
evidence_box(ax1, 0.06, 0.42, 0.88, 0.16, "9,216 marked CONFIDENCIAL\n67% of Jalisco records", C_CONF, "white")
ax1.annotate("", xy=(0.5, 0.37), xytext=(0.5, 0.42),
             arrowprops=dict(arrowstyle="->", color=C_GREY, lw=1.2))
evidence_box(ax1, 0.06, 0.17, 0.88, 0.16,
             "1,026 also had active public search notices\nZonaDocs, 2024", "#ead8d1", C_CONF)
ax1.text(0.06, 0.07, "Here the denominator and overlap are documented.",
         fontsize=8.5, color=st.MUTED)

# Guerrero: two evidence systems whose overlap is unknown.
ax2.set_title("GUERRERO — official and family records", loc="left", fontsize=11,
              weight="bold", color=C_COLL, pad=12)
evidence_box(ax2, 0.04, 0.59, 0.42, 0.24,
             "4,453 official\nunresolved records\nstatewide", C_KNOWN)
evidence_box(ax2, 0.54, 0.59, 0.42, 0.24,
             "623 cases documented\nby three collectives\nin Iguala", "#d7e3eb", C_COLL)
ax2.text(0.50, 0.49, "OVERLAP UNKNOWN", ha="center", fontsize=9.5,
         color=st.INK, weight="bold")
ax2.plot([0.25, 0.75], [0.54, 0.54], color=st.MUTED, lw=1)
ax2.text(0.50, 0.35,
         "The two figures cannot be added or subtracted.\n"
         "They show parallel systems of evidence, not a measured undercount.",
         ha="center", va="center", fontsize=9, color=st.INK)
ax2.text(0.50, 0.16,
         "Collectives are credited with the recovery of 260 bodies in Iguala,\n"
         "69 of them identified and returned. In Acapulco, Tlachinollan records\n"
         "70 people found alive and 55 identified bodies returned.",
         ha="center", va="center", fontsize=8.5, color=C_COLL)

fig.text(0.02, 0.02,
         "The panels answer different questions. Jalisco measures redaction inside one registry; Guerrero shows official and "
         "collective records whose person-level overlap has not been established. Sources: RNPDNO mirror microdata; ZonaDocs "
         "(2024-11-21); Tlachinollan; HRW (2019). Consulted 2026-07-06.",
         fontsize=7.5, color="#666666")

fig.tight_layout(rect=(0, 0.07, 1, 0.92))
fig.savefig("reports/figures/22_two_modes_of_opacity.png", dpi=200, bbox_inches="tight")
print("wrote reports/figures/22_two_modes_of_opacity.png")
st.save(fig, "G_two_modes.png")
