# Publication data audit — 2026-08-15

## Publication cutoffs

- **Still-missing microdata and redaction:** lapanquecita RNPDNO mirror snapshot dated 2025-12-02, pinned upstream commit `666b3e7605`.
- **Aggregate outcomes, including located people:** live RNPDNO public dashboard API captured 2026-08-15 23:49:53 America/Mexico_City (2026-08-16T05:49:53+00:00).
- **Consent mechanism:** CNB oficio SEGOB/CNBP/1349/2020, pp. 5 and 11 (universe dated 2020-08-07).
- **Batch changes:** ten pinned mirror snapshots, 2025-04-03 to 2025-12-02.

These sources answer different questions and must retain their own dates in the article.

## Automated claim checks

| Result | Claim | Recomputed | Draft value |
|---|---|---:|---:|
| PASS | Mirror rows | 133,566 | 133,566 |
| PASS | Unique victim IDs | 133,566 | 133,566 |
| PASS | Confidential records | 49,136 | 49,136 |
| PASS | National confidential share | 36.8% | 36.8% |
| PASS | Jalisco confidential share | 66.9% | 67.0% |
| PASS | Nayarit confidential share | 66.2% | 66.0% |
| PASS | Guerrero confidential share | 9.1% | 9.0% |
| PASS | Colima confidential share | 9.0% | 9.0% |
| PASS | Jalisco unresolved records | 13,766 | 13,766 |
| PASS | Jalisco confidential records | 9,216 | 9,216 |
| PASS | Guerrero unresolved records | 4,453 | 4,453 |
| PASS | Version audit starts at 44,035 confidential | 44,035 | 44,035 |
| PASS | Version audit ends at 49,136 confidential | 49,136 | 49,136 |
| PASS | Confidential records increased by 5,101 | 5,101 | 5,101 |
| PASS | Confidential made up about 77% of net growth | 77.0% | 77.0% |

## Fresh aggregate-flow capture

- Reported disappearances, 2000–2025: **352,294**.
- Found alive: **214,643**.
- Found dead: **20,551**.
- Still missing: **117,100**.
- All reported in 2000 / 2007 / 2025: **102 / 3,034 / 37,124**.

The draft and Figure A should be regenerated from this frozen flow table before publication; live totals are allowed to differ from the June 2026 exploratory pull.

## Manual source audit

| Result | Claim or figure | Finding | Publication decision |
|---|---|---|---|
| PASS | Current RNPDNO headline | The official dashboard displayed **407,253** total records, including **134,268 disappeared or not located** and **272,985 located**, for the period through 2026-08-15 23:55. Its displayed last-update time was 2026-08-15 23:54:55. This matches the frozen API response. | Use **134,268** only as the all-period live headline, with consultation time. Do not compare it directly with the 2000–2025 flow total of 117,100 still missing. |
| PASS WITH COPY REVISION | CNB consent accounting | Visual inspection of oficio pp. 5 and 11 confirms **73,388** records, **56,803** with no consent information, **16,585** with some information, and—among **14,295 family reporters**—**7,478** refusing publication and **6,717** agreeing. | Keep the counts, but revise Figure E as described below. |
| PASS | Active notices marked confidential | ZonaDocs reports **4,765** such cases across six states, including **1,026 in Jalisco**. The state subtotals printed by ZonaDocs sum to 4,765. | Safe with attribution to ZonaDocs and its 2024-11-21 cutoff. |
| PASS | Jalisco 2022–23 divergence | El Informador reports federal RNPDNO **14,944** in April 2022 and **15,012** at 2023-05-06; SISOVID reported **13,976** at 2023-03-31. It also reports **1,260** state search notices issued from May 2022 to 2023-05-04, of which 942 remained missing. | Figure F's historical points are supported. Describe them as documented snapshots, not a continuous series, and keep the differing registry definitions explicit. |
| PASS / REVISE | Guerrero collective figures | Tlachinollan supports **623 cases documented by three Iguala collectives** and **260 bodies recovered in Iguala**, of which 69 were identified and returned. For Acapulco it says **70 people were found alive** and **55 identified bodies were returned**. | Keep 623 and 260 with attribution and non-comparable-denominator warning. Replace “~70 bodies in Acapulco”; it is incorrect. |
| REVISE | Figure D | The plotted x-axis is unresolved disappearances per 100,000, but the caption and article interpret the comparison as homicide/violence. | Either change the prose to disappearance prevalence or rebuild the plot with the homicide-rate variable. Do not publish the current mixed version. |

Sources consulted for this manual audit:

- Official RNPDNO dashboard: https://versionpublicarnpdno.segob.gob.mx/Dashboard/ContextoGeneral
- CNB oficio SEGOB/CNBP/1349/2020, pp. 5 and 11: frozen local source in this data freeze
- ZonaDocs, “Desaparecidos: el engaño estadístico de México” (2024-11-21): https://www.zonadocs.mx/2024/11/21/desaparecidos-el-engano-estadistico-de-mexico/
- El Informador, “Borran cifras de Jalisco en el registro nacional” (2023-05-09): https://www.informador.mx/Desaparecidos-Borran-cifras-de-Jalisco-en-el-registro-nacional-l202305090001.html
- Tlachinollan, “Guerrero: territorio de personas desaparecidas” (2022): https://www.tlachinollan.org/guerrero-territorio-de-personas-desaparecidas/

## Required revisions before publication

1. **Regenerate Figure A and its text** from the frozen 2000–2025 flow table: 214,643 found alive; 20,551 found dead; 117,100 still missing; 352,294 reports in total.
2. **Correct the Acapulco comparison** everywhere. The source distinguishes 70 people found alive from 55 identified bodies returned to families.
3. **Resolve Figure D's variable mismatch** before interpreting the scatter.
4. **Rewrite Figure E's accounting.** The grey segment is not simply “anonymous/unclear reporters”: 2,290 records are anonymous, while the family subtotal leaves 100 of 14,295 records unclassified by the two published counts. The oficio also contains a prose sentence that appears to reverse its own 52.31%/46.98% counts. Use the printed counts, disclose the 100-record gap, and avoid the unsupported chart sentence “records without paperwork default to confidential.” A safer headline is: **“For most records, the CNB did not know whether families authorized publication.”**
5. **Keep source dates attached to every number.** The microdata/redaction snapshot (2025-12-02), live all-period dashboard (2026-08-15), 2000–2025 flow table (captured 2026-08-15), consent universe (2020-08-07), and investigative snapshots are not interchangeable.

## Publication status

**The data freeze and numerical audit are complete, but the draft is not yet publication-safe.** Fifteen automated claims pass. Four editorial changes above are required; none requires abandoning the project or its central finding.

## Reproducibility

Frozen inputs, raw API responses, derived tables, hashes and machine-readable checks are in:

`data/publication_freezes/2026-08-15`

Run `python src/publication_freeze.py --date 2026-08-15` only for a new date. Existing freezes are immutable and the script refuses to overwrite them.
