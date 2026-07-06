# Who Decides a Record Becomes CONFIDENCIAL?

Status: answered at the federal-mechanism level. Consulted 2026-07-06.

This note answers the keystone question behind the opacity thread: is redaction in the
RNPDNO public version driven by federal rules, state rules, fiscalía practice, family
consent, or something else? Short answer: **a federal consent rule, operationalized by
the capturing authorities (mostly state fiscalías), with missing consent documentation
defaulting to confidential — and at least one state (Jalisco) applying a blanket
non-consent policy to everything it submits.**

## The legal rule (federal)

Ley General en Materia de Desaparición (DOF 2017-11-17):

- **Art. 108**: personal data in the Registro Nacional may only be used to determine the
  fate/whereabouts of the person. Families who provide information have the right to
  request that the disappeared person's information **not be made public**, and must be
  informed of this right *before* providing the information.
- **Art. 109**: the CNB must publish a public version of the registry, per the applicable
  transparency and data-protection law (Ley General de Transparencia art. 116 makes
  personal data confidential by default).

So the *de jure* mechanism is family consent, collected at capture time.

Source: [Oficio SEGOB/CNBP/1349/2020](../data/external/legal_docs/Oficio_SEGOB_CNBP_1349_2020_consulta_INAI.pdf)
(CNB consulta to INAI, 2020-08-12, signed by Karla Quintana; local copy saved;
original: https://www.gob.mx/cms/uploads/attachment/file/570563/Oficio_SEGOB_CNBP_1349_2020.pdf).

## The operational reality (from the CNB's own numbers, Aug 2020)

The same oficio (pp. 5, 11) documents, as of 2020-08-07, universe of 73,388 reported
disappeared:

- Data source/quality/completeness "es responsabilidad de las autoridades que la emiten
  — hasta ahora, **78.79% fiscalías y procuradurías**".
- **77.40% of records (56,803) had NO information at all on whether the family consents
  to publication** — largely records predating the Ley General.
- Only 22.60% (16,585) had recorded consent info. Of the 14,295 identified as family
  reporters: **52.31% refused publication, 46.98% agreed**. So when actually asked,
  families split roughly half/half.
- **Footnote 3 (the Jalisco smoking gun):** "Existen instituciones, como la **Fiscalía de
  Jalisco**, que ha manifestado que la información que remite al RNPDNO no puede ser
  pública en virtud de que las familias ... han expresado directamente no dar su
  consentimiento autorizado para hacerla pública, por lo que no podría realizarse
  publicación alguna relacionada con dichos datos." — i.e., Jalisco's Fiscalía declares
  its *entire submission* non-publishable.

The CNB's position: consent cannot be presumed, so absent documentation the default is
confidentiality. **The CONFIDENCIAL share therefore mixes three very different things:**

1. genuine family opt-outs (~half of the asked minority);
2. missing consent paperwork defaulting to confidential (the 77% bulk in 2020);
3. blanket fiscalía-level policies (Jalisco, documented above).

Cross-state variation in redaction is thus primarily **capture/institutional practice**,
not family preference or crisis intensity — confirming the working hypothesis in
[case-selection.md](case-selection.md).

## Journalist verification that the official framing fails

The public platform's own note (quoted in Data Cívica's methodology) claims CONFIDENCIAL
records "corresponden a informes en los que la persona solicitó que no se compartieran su
información." Reporting shows this is often false:

- ZonaDocs / "Desaparecidos: el engaño estadístico de México" (2024-11-21,
  https://www.zonadocs.mx/2024/11/21/desaparecidos-el-engano-estadistico-de-mexico/):
  39,299 confidential records (34.77% at that date); **4,765 cases in six states have
  ACTIVE public search notices yet appear confidential** (Edomex 2,691, Jalisco 1,026,
  Veracruz 684, Puebla 271, Guanajuato 84, Tabasco 9). Authorities admitted they perform
  **no risk assessment** to justify confidentiality. Documented case: María de Jesús
  Solís (son disappeared in Zapopan, 2020) — "never signed for confidential status,
  wants maximum visibility." Researcher Jorge Ramírez Plascencia calls
  confidentiality-despite-family-authorization "a disaster and a paradox."
- A dónde van los desaparecidos (2021-04-08,
  https://adondevanlosdesaparecidos.org/2021/04/08/cnbp-incumple-orden-del-inai-de-entregar-base-de-datos-de-personas-desaparecidas/):
  INAI resolution **RRA 09082/20** (Dec 2020) and at least two more ordered the CNB to
  release a public-version database; the CNB resisted citing lack of family consent but
  **could not produce the consent declarations**; under pressure delivered only 50,204
  of 175,371 records.
- Data Cívica, "Las personas desaparecidas y borradas por el Estado" (methodology PDF,
  https://volveradesaparecer.datacivica.org/assets/pdf/Metodologia_Personas_desaparecidas_borradas.pdf):
  timeline of registry versions (RNPED 2012–2018 → gap → RNPDNO dashboard 2020 →
  person-level public version Aug 2023 → "Buscador" Dec 2023 post-"censo").
  Distinguishes *confidencializados* (FUB retained, name hidden) from *borrados*
  (removed entirely). NB: their erased-names analysis compares the **Aug 2023 vs Dec 2023**
  person-level lists.

## Consequences for our analysis

- Our `CONFIDENCIAL` flag (36.8% national) must be described as an **administrative
  redaction artifact**, never as "families chose privacy."
- Cross-state redaction comparisons (figs 08–15) measure *institutional publication
  practice* — which is exactly what makes them interesting, and exactly why they cannot
  be controlled away as noise.
- Jalisco's 67% share now has a documented candidate explanation dating to at least 2020
  (blanket fiscalía policy) — see [cases/jalisco.md](cases/jalisco.md).
- Whether CONFIDENCIAL *grew* across registry versions remains open; Data Cívica's
  version snapshots (Aug 2023 vs Dec 2023) are the data to test it. Parked per scope
  guardrail.

## Remaining open sub-questions

1. Did the 77% "no consent info" bulk shrink after 2020 (new capture forms), and did
   states re-contact families? No evidence found yet.
2. Is there any INAI *Pleno* formal answer to the 2020 CNB consulta (as opposed to the
   access-request resolutions)? Not located; the consulta may never have received a
   formal dictamen.
