"""Fig 22 / article fig G: two modes of registry opacity (Jalisco vs Guerrero).

The thesis chart. Both states remove people from public view; they do it at
different stages, which is why a low confidential share is not a clean bill of
health.

* JALISCO — opacity by REDACTION, and it is measurable. 13,766 unresolved records
  exist in the public mirror; 9,216 of them (66.9%) publish nothing but the state.
  You can count the records. You cannot read them.
* GUERRERO — opacity by OMISSION, and it is NOT measurable. Only 403 of 4,453
  records are confidential (9.1%), so on the redaction ranking Guerrero looks open.
  But that ranking only describes records that reached the registry. In Iguala
  alone three collectives document 623 cases, and during Holy Week 2026 three
  families reported disappearances to searchers that they had never reported to any
  authority.

The design carries the asymmetry: Jalisco's bar is closed because its quantity is
known, and Guerrero's ends in an open, fading edge because the missing quantity is
not. The 623 is drawn as a documented fragment beside that edge, deliberately NOT
as a segment of it — the two figures may overlap and cannot be netted.

Earlier versions of this figure were panels of text boxes, which read as a diagram
rather than a chart and left readers unsure what was being compared.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import article_style as st

st.apply()

JAL_TOTAL, JAL_CONF = 13766, 9216
GRO_TOTAL, GRO_CONF = 4453, 403
IGUALA = 623

JAL_PUBLIC = JAL_TOTAL - JAL_CONF
GRO_PUBLIC = GRO_TOTAL - GRO_CONF

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 6.9), sharex=True)
XMAX = 15200

for ax in (ax1, ax2):
    ax.set_xlim(0, XMAX)
    ax.set_ylim(-0.75, 0.95)
    ax.set_yticks([])
    ax.spines[["top", "left", "right"]].set_visible(False)
    ax.grid(axis="x", color=st.MUTED, alpha=0.22, lw=0.7)
    ax.set_axisbelow(True)

BAR_Y, BAR_H = 0.05, 0.42

# ---------------------------------------------------------------- Jalisco
ax1.barh(BAR_Y, JAL_PUBLIC, height=BAR_H, color=st.SAND, zorder=3)
ax1.barh(BAR_Y, JAL_CONF, left=JAL_PUBLIC, height=BAR_H, color=st.RED, zorder=3)
ax1.text(JAL_PUBLIC / 2, BAR_Y, f"{JAL_PUBLIC:,}\npublic fields", ha="center",
         va="center", fontsize=9.5, color=st.INK, zorder=4)
ax1.text(JAL_PUBLIC + JAL_CONF / 2, BAR_Y, f"{JAL_CONF:,} redacted\n66.9%",
         ha="center", va="center", fontsize=10.5, color=st.PAPER, weight="bold",
         zorder=4)
ax1.set_title("JALISCO — opacity by redaction, and you can measure it", loc="left",
              fontsize=11.5, weight="bold", color=st.RED, pad=8)
ax1.text(0, -0.38, "Every one of these 13,766 people is in the registry. For two "
                   "thirds of them the registry publishes\nonly the state and filing authority — no date, "
                   "age, sex, municipality or case status.",
         fontsize=9.5, color=st.INK, va="top")

# ---------------------------------------------------------------- Guerrero
ax2.barh(BAR_Y, GRO_PUBLIC, height=BAR_H, color=st.SAND, zorder=3)
ax2.barh(BAR_Y, GRO_CONF, left=GRO_PUBLIC, height=BAR_H, color=st.RED, zorder=3)
ax2.text(GRO_PUBLIC / 2, BAR_Y, f"{GRO_PUBLIC:,}\npublic fields", ha="center",
         va="center", fontsize=9.5, color=st.INK, zorder=4)
ax2.annotate(f"{GRO_CONF:,} redacted (9.1%)",
             xy=(GRO_TOTAL, BAR_Y + BAR_H / 2), xytext=(GRO_TOTAL + 160, 0.62),
             fontsize=9.5, color=st.RED,
             arrowprops=dict(arrowstyle="-", color=st.RED, lw=0.8))

# The open edge: the quantity beyond the registry is unknown, so the bar must not
# end in a straight line that implies one.
for i in range(46):
    x = GRO_TOTAL + i * 105
    ax2.add_patch(Rectangle((x, BAR_Y - BAR_H / 2), 105, BAR_H, zorder=2,
                            facecolor=st.MUTED, edgecolor="none",
                            alpha=max(0.0, 0.30 * (1 - i / 46))))
ax2.text(GRO_TOTAL + 2300, BAR_Y, "not in the registry at all\nsize unknown",
         ha="left", va="center", fontsize=10.5, color="#7b7b7b", style="italic",
         zorder=4)

# Iguala: a documented fragment, drawn OUTSIDE the bar so it cannot be read as a
# measured slice of the unknown.
ax2.add_patch(Rectangle((0, -0.52), IGUALA, 0.17, facecolor=st.BLUE,
                        edgecolor="none", zorder=3))
ax2.text(IGUALA / 2, -0.435, f"{IGUALA}", ha="center", va="center", fontsize=8.5,
         color=st.PAPER, weight="bold", zorder=4)
ax2.text(IGUALA + 420, -0.435,
         "documented by three collectives in Iguala alone \u2014 one city, a seventh of "
         "the state's whole register.\nSome are certainly also registered. Without case "
         "identifiers on both sides, the two cannot be netted.",
         fontsize=9.5, color=st.INK, va="center")

ax2.set_title("GUERRERO — opacity by omission, and you cannot", loc="left",
              fontsize=11.5, weight="bold", color=st.BLUE, pad=8)

ax2.set_xlabel("People recorded disappeared (registry snapshot, 2 December 2025)")
ax2.set_xticks(range(0, 15001, 2500))
ax2.set_xticklabels([f"{v:,}" for v in range(0, 15001, 2500)])

fig.suptitle("A low redaction share is not a clean bill of health",
             fontsize=14.5, weight="bold", x=0.055, ha="left", y=0.975)
fig.text(0.055, 0.935,
         "Two ways people go missing from public view: after they enter the registry, "
         "and before.", fontsize=10, color=st.MUTED, ha="left")

fig.text(0.055, 0.018,
         "The two panels answer different questions and share only an axis. Jalisco's split is measured inside one registry;\n"
         "Guerrero's open edge is not a measured quantity, and the Iguala bar is a documented example rather than an estimate\n"
         "of it. Sources: RNPDNO record-level microdata, 2025-12-02 [3]; ZonaDocs (2024-11-21); Tlachinollan; HRW (2019). "
         "Consulted 2026-07-06.",
         fontsize=7.5, color="#666666", va="bottom", linespacing=1.5)

fig.subplots_adjust(left=0.055, right=0.98, top=0.85, bottom=0.19, hspace=0.60)
fig.savefig("reports/figures/22_two_modes_of_opacity.png", dpi=200)
print("wrote reports/figures/22_two_modes_of_opacity.png")
st.save(fig, "G_two_modes.png")
