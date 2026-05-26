# Nest 3 Gases / Liquids / Phases NIST Support Read

Date: `2026-05-26`

Run ID: `nest3_gases_liquids_phases_nist_2026-05-26`

Status: `real_data / NIST_Chemistry_WebBook / thermophysical_phase_gate / support`

## Source

Primary source: `NIST Chemistry WebBook Thermophysical Properties of Fluid Systems`

Source page: `https://webbook.nist.gov/chemistry/fluid/`

Dataset DOI / SRD reference: `https://doi.org/10.18434/T4D303`

Local source tables used: `water_sat.tsv`, `co2_sat.tsv`, `methane_sat.tsv`,
and `nitrogen_sat.tsv`.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | saturated liquid property rows |
| `control` | saturated vapor property rows |
| `group holdout` | species-held-out GroupKFold |
| `feature boundary` | phase label, pair ID, and surface-tension missingness excluded |

## Results

| Metric | Value |
| --- | ---: |
| Records | 4808 |
| Target / control records | 2404 / 2404 |
| Species | 4 |
| Saturation pairs | 2404 |
| Feature count | 13 |
| Observed ROC AUC | 0.929272 |
| Observed balanced accuracy | 0.849210 |
| Shuffled-label mean AUC | 0.499840 |
| Shuffled-label p | 0.004975 |
| Feature-shuffle AUC | 0.489769 |
| No-density/volume AUC | 0.925063 |
| Pressure-temperature-only AUC | 0.500000 |

## Interpretation

This is the first executable `Nest 3 / Gases / Liquids / Phases` source gate.
It tests whether real thermophysical property vectors from NIST separate
saturated liquid and vapor rows while holding out entire species.

Read as `support`.

## Boundary

This is a saturation liquid/vapor source gate, not a full phase-diagram
closeout. The no-density/volume and pressure-temperature-only controls keep the
obvious property-family and shared-condition boundaries visible.

Next gate: supercritical / isobaric rows, pressure-band holdouts, and a
multi-phase extension that includes saturation, liquid, vapor, and
supercritical operating regions where NIST source tables support the labels.
