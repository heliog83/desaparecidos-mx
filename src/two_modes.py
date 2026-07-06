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
from matplotlib.patches import Rectangle

import article_style as st

st.apply()
C_CONF, C_KNOWN, C_COLL, C_GREY = st.RED, st.SAND, st.BLUE, st.INK

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
fig.suptitle("Two ways to disappear from the data", fontsize=14, weight="bold",
             x=0.02, ha="left")

# ---- Left: Jalisco, redaction -------------------------------------------------
jal_total, jal_conf = 13_766, 9_216
ax1.add_patch(Rectangle((0, 0), 1, jal_conf, facecolor=C_CONF))
ax1.add_patch(Rectangle((0, jal_conf), 1, jal_total - jal_conf, facecolor=C_KNOWN))
ax1.set_xlim(-0.9, 2.2)
ax1.set_ylim(0, 15_500)
ax1.text(0.5, jal_conf / 2, "CONFIDENCIAL\n9,216 records\n67%", ha="center",
         va="center", color="white", fontsize=11, weight="bold")
ax1.text(0.5, jal_conf + (jal_total - jal_conf) / 2, "with public\ndetails\n33%",
         ha="center", va="center", color="#555555", fontsize=9.5)
ax1.annotate("1,026 of these have ACTIVE\npublic search notices\n(ZonaDocs, 2024)",
             xy=(1.02, jal_conf * 0.75), xytext=(1.25, 10_800), fontsize=8.5,
             color=C_CONF, arrowprops=dict(arrowstyle="-", color=C_CONF, lw=0.8))
ax1.set_title("JALISCO — opacity by redaction\nrecorded, then hidden",
              loc="left", fontsize=11, weight="bold", color=C_CONF)
ax1.text(-0.85, 14_600, "13,766 unresolved records\n(public registry mirror)",
         fontsize=8.5, color="#555555")
ax1.axis("off")

# ---- Right: Guerrero, omission ------------------------------------------------
gro_total, gro_conf, iguala = 4_453, 403, 623
ax2.add_patch(Rectangle((0, 0), 1, gro_conf, facecolor=C_CONF))
ax2.add_patch(Rectangle((0, gro_conf), 1, gro_total - gro_conf, facecolor=C_KNOWN))
ax2.add_patch(Rectangle((1.35, 0), 0.55, iguala, facecolor=C_COLL))
ax2.set_xlim(-0.9, 3.4)
ax2.set_ylim(0, 15_500)
ax2.text(0.5, gro_total + 350, "4,453 registered\nstatewide — only\n9% confidential",
         ha="center", fontsize=8.5, color="#555555")
ax2.text(1.625, iguala + 350, "623 documented by\nthree collectives in\nIGUALA ALONE",
         ha="center", fontsize=8.5, color=C_COLL, weight="bold")
ax2.text(1.15, 6_500,
         "the registry looks transparent —\nbut collectives keep finding people\n"
         "who were never registered:\n260+ bodies located in Iguala,\n~70 in Acapulco, "
         "by families,\nnot the state (Tlachinollan/HRW)",
         fontsize=8.5, color=C_GREY)
ax2.set_title("GUERRERO — opacity by omission\nnever recorded at all",
              loc="left", fontsize=11, weight="bold", color=C_COLL)
ax2.axis("off")

fig.text(0.02, 0.015,
         "Panels use different denominators; the Iguala count is a documented example of "
         "under-registration, not a comparable measurement or a census. Sources: RNPDNO mirror "
         "microdata; ZonaDocs (2024-11-21); Tlachinollan; HRW (2019). Consulted 2026-07-06.",
         fontsize=7.5, color="#666666")

fig.tight_layout(rect=(0, 0.05, 1, 0.93))
fig.savefig("reports/figures/22_two_modes_of_opacity.png", dpi=200, bbox_inches="tight")
print("wrote reports/figures/22_two_modes_of_opacity.png")
st.save(fig, "G_two_modes.png")
