# External Variable Plan

Last updated: 2026-06-19.

This project should add explanatory variables only when they answer a specific question about
registry opacity, disappearances, clandestine graves, or state response.

## Current rule

Do not use outside variables to "explain away" disappearances or redaction. Use them to test
limited hypotheses.

Good hypothesis:

> States with higher public-registry opacity may differ in violence context, administrative
> practice, institutional capacity, or socioeconomic structure.

Bad hypothesis:

> GDP/corruption/violence explains why records are confidential.

The second claim is too causal for a 32-state observational comparison.

## Variables added

### 1. GDP / GDP per capita

Source: INEGI, Producto Interno Bruto por Entidad Federativa (PIBE).

Status: added to `data/processed/state_opacity_enriched.csv` from the official INEGI PIBE
2024 CSV zip. The pipeline uses 2024 preliminary GDP in millions of pesos at 2018 prices
and computes GDP per capita with the local 2024 population table.

Use for:

- state capacity / economic scale proxy
- GDP per capita contrast
- whether high-opacity states cluster among economically larger states

Caveat:

- GDP does not measure prosecutor capacity, search capacity, forensic capacity, or political
  will directly.

Reference:

- https://www.inegi.org.mx/app/descarga/ficha.html?ag=0&f=csv&tit=1628436
- https://www.inegi.org.mx/programas/pibent/

### 2. Corruption experience / perception

Source: INEGI, Encuesta Nacional de Calidad e Impacto Gubernamental (ENCIG).

Status: added to `data/processed/state_opacity_enriched.csv` from INEGI ENCIG 2025 results
report, Cuadro 1. The pipeline includes corruption prevalence per 100,000 for 2025 and the
change from 2023 to 2025.

Use for:

- whether public-service corruption measures move with registry opacity
- contrast between corruption prevalence and disappearance-data opacity

Caveat:

- ENCIG measures experiences/perceptions in public services. It does not directly measure
  manipulation of disappearance registries.

Reference:

- https://www.inegi.org.mx/programas/encig/2025/
- https://inegi.org.mx/app/tabulados/interactivos/?bd=encig&px=ENCIG_PREVALENCIA_ENT

## Variables worth adding next

### 1. Institutional capacity

Possible variables:

- state forensic-services capacity
- number of forensic personnel
- search commission budget
- prosecutor budget
- backlog of unidentified remains
- number of SEMEFO / forensic facilities

Use for:

- testing whether opacity is linked to weak capacity rather than only violence or politics

Caveat:

- These may require transparency requests, reports, or manual extraction.

### 2. Violence and criminal-market proxies

Already partly local through `data/external/assets/timeseries_victimas.csv`:

- homicide victims
- kidnapping victims
- extortion victims
- femicide victims
- human trafficking victims
- rapto victims

Use for:

- checking whether opacity simply tracks violence intensity

Early result:

- In the current local model, opacity does not map cleanly onto homicide, kidnapping, or
  located-dead shares. That pushes us toward administrative/publication explanations, but does
  not prove them.

### 3. Historical registry snapshots

Best source family: Data Civica / Volver a desaparecer historical registry versions.

Use for:

- the most important unanswered opacity question: has `CONFIDENCIAL` grown over time?

Caveat:

- Requires versioned person-level snapshots or comparable aggregate fields by snapshot date.

Reference:

- https://volveradesaparecer.datacivica.org/datos-abiertos
