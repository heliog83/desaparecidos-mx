# International comparison — sourced figures and what they can support

Research memo, compiled 2026-08-16. **Not article copy.** This exists so a comparison
figure can be built from sourced numbers with their definitions attached, rather than
from remembered ones.

**Headline conclusion up front: the framing "Mexico is worse than war countries" does
not survive per-capita comparison and should not be published.** A stronger claim does
survive, and it is set out in §3.

---

## 1. The table

Every row states what it counts. These are *not* interchangeable measures, and the
table must never be published without the "counts what" column.

| Country / body | Figure | Counts what | As of | Source |
|---|---:|---|---|---|
| **Mexico** | **134,268** | People recorded disappeared or not located in the national registry (RNPDNO). Includes `NO LOCALIZADA` — no evidence of crime required. Peacetime. | 2026-08-15 | Own API capture [1] |
| **Colombia** | **136,010** | Persons given as disappeared **in connection with the armed conflict**; universe assembled by the state search unit | Mar 2026 | UBPD [2] |
| **Iraq** | **250,000 – 1,000,000** | Missing from decades of conflict, Ba'ath-era atrocity, wars and Da'esh. Authorities' own estimate; range spans a factor of four | current | ICMP [3] |
| **Syria** | **up to 300,000** | Missing; ICMP states estimates "run as high as" this | current | ICMP [4] |
| **Western Balkans** (incl. Bosnia) | **40,000** at end of conflict; **>70% accounted for**, so roughly 10,000 outstanding | Missing from the 1990s conflicts | current | ICMP [5] |
| **Argentina** | **~30,000** | Disappeared under the 1976–83 dictatorship. Explicitly **symbolic**, not a register | historical | widely cited; contested [6] |
| *UN WGEID* | *~59,000* | *Global* outstanding cases of **enforced** disappearance (state involvement) under active consideration | 2024 | WGEID [7] |
| *ICRC Family Links* | *284,400* | *Global* people registered missing with the Red Cross/Red Crescent network; +68% since 2019 | end-2024 | ICRC [8] |

## 2. Per capita — where the "worse than war" claim fails

Approximate rates against population at the relevant time. **Rounded, illustrative,
and the weakest row in this memo** — denominators for historical cases are contestable.

| | per 100,000 |
|---|---:|
| Iraq (high estimate) | ~2,200 |
| Syria | ~1,300 |
| Western Balkans | ~500 |
| Colombia | ~262 |
| Argentina | ~107 |
| **Mexico** | **~103** |

Mexico is at the **bottom** of this list. Per head of population it is not close to
Bosnia, Syria or Iraq, and it sits below Colombia. Any chart implying otherwise would
be wrong, and a reader who checks would find it in one calculation.

## 3. What the evidence does support

Three claims survive scrutiny. All three are stronger than the one they replace.

**a. Mexico's registry is the size of a sixty-year civil war's, and Mexico has not had
one.** Mexico 134,268 vs Colombia 136,010 — a difference of 1.3%. Colombia's universe
covers disappearances tied to an internationally recognised armed conflict running from
the 1950s. Mexico's is a peacetime registry, and the overwhelming majority of it
accumulated after 2006. That is the comparison to build the figure on.

**b. The accumulation is far faster.** Colombia's 136,010 spans six decades. Mexico
recorded **37,124 disappearances in 2025 alone** [1] — more than the entire Argentine
dictatorship's symbolic total, in one year.

**c. Only two countries clearly exceed Mexico, and both after decades of war.** Iraq
and Syria. Mexico exceeds the Western Balkans' entire wartime missing by 3.4×, and it
is 2.3× the UN's global count of *enforced* disappearances.

One more, worth using carefully: Mexico alone accounts for roughly **47% of the ICRC's
entire global registered missing caseload** (134,268 of 284,400). This overstates
Mexico's share of the world's missing — ICRC registers only cases reported to it, and
coverage is uneven — so it should be framed as a statement about *registration*, not
about reality.

## 4. Traps to avoid

- **Category mismatch is the main risk.** Mexico's figure includes `NO LOCALIZADA`,
  people with no evidence of a crime. Argentina's counts victims of a state programme;
  Bosnia's counts wartime missing; the WGEID's counts *enforced* disappearance only.
  Any chart mixing these without labels invites the rebuttal that it compares a police
  database to a war-crimes register — and that objection, once landed, would discredit
  the redaction analysis too.
- **Publish Mexico's own sensitivity.** State the figure excluding `NO LOCALIZADA`
  alongside it. Volunteering the weakness pre-empts the attack.
- **Argentina's 30,000 is symbolic and politically contested** in Argentina itself.
  Use it only with that stated.
- **Iraq's range is a factor of four.** Plot it as a range, never a point.
- **Stock vs cumulative.** Mexico's 134,268 is people *still* missing today; Colombia's
  136,010 is a universe of cases including those since resolved. These are not the same
  quantity, and the figure must say so.

## 5. Recommended chart

A dot plot, one row per country, **two panels**: absolute count and per-100,000 rate,
with Iraq drawn as a range. Colour by context — declared armed conflict, dictatorship,
peacetime — so the reader sees the category difference rather than being told about it.
The point lands on its own: the peacetime bar sits beside the war bars in panel one and
falls to the bottom in panel two, which is precisely the honest story.

## Sources

1. Own capture, RNPDNO public dashboard API, 2026-08-15;
   `data/publication_freezes/2026-08-15/`.
2. [UBPD, "en Colombia existen 136.010 personas que son buscadas por sus familias"](https://unidadbusqueda.gov.co/actualidad/registro-136010-personas-desaparecidas-colombia-abril-2026/),
   published 2026-04-08, cut-off March 2026.
3. [ICMP — Iraq](https://icmp.int/the-missing/where-are-the-missing/iraq/).
4. [ICMP — Syria](https://icmp.int/the-missing/where-are-the-missing/syria/).
5. [ICMP — Western Balkans](https://icmp.int/what-we-do/geographic-programs/western-balkans/).
6. Figure widely cited and explicitly contested; see
   [Buenos Aires Times on the debate](https://batimes.com.ar/news/opinion-and-analysis/30000-the-debate-about-how-many-were-disappeared-in-argentina.phtml).
7. [OHCHR — Working Group on Enforced or Involuntary Disappearances](https://www.ohchr.org/en/special-procedures/wg-disappearances).
   ~59,000 outstanding as of 2024. The WGEID annual report tables were not directly
   retrievable (HTTP 403); **verify against the primary report before publishing**.
8. [ICRC, missing registrations up ~70% in five years](https://www.icrc.org/en/news-release/missing-people-registered-increased-70-percent-five-years),
   284,400 registered at end-2024.

## Status

Figures 2–8 come from single web sources consulted 2026-08-16 and have **not** been
cross-checked against primary documents. Before publication: pull the WGEID annual
report directly, and confirm the ICMP country figures on ICMP's own country pages
rather than via press summaries.
