"""Fig 20 / article fig E: consent accounting behind CONFIDENCIAL — the mechanism chart.

Data is NOT derived from microdata: hardcoded from the CNB's own consulta to INAI,
Oficio SEGOB/CNBP/1349/2020 pp. 5 & 11 (universe: 73,388 records at 2020-08-07).
Local copy: data/external/legal_docs/Oficio_SEGOB_CNBP_1349_2020_consulta_INAI.pdf
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import article_style as st

TOTAL = 73_388
NO_INFO = 56_803          # 77.40% — no record of whether the family consents
WITH_INFO = 16_585        # 22.60% — some consent info recorded
FAM_REFUSED = 7_478       # of 14,295 family reporters: 52.31% refused publication
FAM_AGREED = 6_717        # 46.98% agreed
FAM_OTHER = WITH_INFO - FAM_REFUSED - FAM_AGREED  # anonymous / unclear reporters

st.apply()
fig, ax = plt.subplots(figsize=(10, 3.9))
segments = [(NO_INFO, st.INK), (FAM_REFUSED, st.RED), (FAM_AGREED, st.BLUE),
            (FAM_OTHER, st.MUTED)]
x = 0
mids = []
for value, color in segments:
    ax.add_patch(Rectangle((x, 0), value, 1, facecolor=color, edgecolor="white", lw=1.5))
    mids.append(x + value / 2)
    x += value

ax.text(mids[0], 0.5, "No consent information exists\n56,803 records — 77.4%",
        ha="center", va="center", color="white", fontsize=12, weight="bold")
# small segments labeled outside the bar, staggered above/below with leader lines
ax.annotate("family asked: REFUSED publication\n7,478 (52% of those asked)",
            xy=(mids[1], 1.0), xytext=(mids[1] - 1_500, 1.30), ha="center", va="bottom",
            fontsize=9.5, weight="bold", color=st.RED,
            arrowprops=dict(arrowstyle="-", color=st.RED, lw=0.8))
ax.annotate("family asked: AGREED\n6,717 (47% of those asked)",
            xy=(mids[2], 0.0), xytext=(mids[2] + 500, -0.30), ha="center", va="top",
            fontsize=9.5, weight="bold", color=st.BLUE,
            arrowprops=dict(arrowstyle="-", color=st.BLUE, lw=0.8))

ax.set_xlim(0, TOTAL)
ax.set_ylim(-0.85, 2.0)
ax.axis("off")
ax.text(0, 1.92, "Who actually consented to confidentiality?",
        fontsize=15, weight="bold", color=st.INK, va="top")
ax.text(0, 1.60, "The CNB's own accounting of publication consent, Aug 2020 — 73,388 records. "
                 "Records without paperwork default to confidential.",
        fontsize=10, color=st.MUTED, va="top")
ax.text(0, -0.70, "Source: Oficio SEGOB/CNBP/1349/2020, pp. 5, 11 (CNB consulta to INAI). "
                  "Grey sliver: anonymous/unclear reporters.",
        fontsize=8, color=st.MUTED, va="top")

fig.tight_layout()
fig.savefig("reports/figures/20_consent_accounting.png", dpi=200, bbox_inches="tight")
print("wrote reports/figures/20_consent_accounting.png")
st.save(fig, "E_consent_accounting.png")
