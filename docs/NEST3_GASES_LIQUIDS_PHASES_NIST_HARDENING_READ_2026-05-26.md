# Nest 3 Gases / Liquids / Phases NIST Hardening Read

Date: `2026-05-26`

Run ID: `nest3_gases_liquids_phases_nist_isobaric_supercritical_2026-05-26`

Status: `real_data / NIST_Chemistry_WebBook / isobaric_supercritical_gate / hardened support; pressure-temperature boundary visible`

## Source

Primary source: `NIST Chemistry WebBook Thermophysical Properties of Fluid Systems`

Source page: `https://webbook.nist.gov/chemistry/fluid/`

Dataset DOI / SRD reference: `https://doi.org/10.18434/T4D303`

Local source family: isobaric tables for water, carbon dioxide, methane, and
nitrogen at pressure bands `0.40Pc`, `0.75Pc`, `1.10Pc`, `1.50Pc`, and
`2.00Pc`.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | rows whose NIST `Phase` column is `supercritical` |
| `control` | rows whose NIST `Phase` column is `liquid` or `vapor` |
| `group holdout` | species-pressure-band groups and species-held-out controls |
| `feature boundary` | phase labels and source identifiers excluded from features |

## Results

| Metric | Value |
| --- | ---: |
| Records | 931 |
| Target / control records | 276 / 655 |
| Species | 4 |
| Pressure bands | 5 |
| Source tables | 20 |
| Feature count | 15 |
| Species-pressure AUC | 0.996067 |
| Species-pressure balanced accuracy | 0.944275 |
| Species-pressure shuffled-label mean AUC | 0.495844 |
| Species-pressure shuffled-label p | 0.004975 |
| Species-pressure feature-shuffle AUC | 0.485563 |
| Species-heldout AUC | 0.996465 |
| No-temperature/pressure AUC | 0.949132 |
| Temperature/pressure-only AUC | 0.941515 |

## Interpretation

This hardens the first `Nest 3 / Gases / Liquids / Phases` support row by
moving from saturation liquid/vapor pairs into real NIST isobaric rows that
include liquid, vapor, and supercritical phases.

Read as `hardened support; pressure-temperature boundary visible`.

## Boundary

This is a stronger phase-diagram support gate, but not a complete thermodynamic
state atlas. The pressure-temperature boundary is expected to carry information
because supercritical phase is physically defined by critical temperature and
pressure. The no-temperature/pressure control keeps the property-vector signal
visible separately from the obvious phase boundary.

Next gate: add isochoric or two-phase dome rows where available, pressure-band
leave-one-band-out controls, and a second source family for thermodynamic phase
tables.
