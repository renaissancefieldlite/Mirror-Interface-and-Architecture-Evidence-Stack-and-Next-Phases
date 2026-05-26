# Nest 3 Ramdb Raman Hard Controls

Date: `2026-05-24`

Run ID: `nest3_ramdb_raman_hard_controls_2026-05-24`

Status: `real_data / NASA_Ames_Ramdb / hard_controls / public_transition_tables`

## Purpose

The first Ramdb pass separated amino-acid Raman records from mineral-standard records, but band-position shuffle stayed elevated. This run adds harder public-page controls before any phase-lock language is used.

Full raw / processed Ramdb CSV remains a separate gate because Ramdb sends the bundle link by email after a user form submission.

## Results

| Control pass | Records | Target / Control | Features | Observed AUC | Shuffled AUC | p | Feature-shuffle AUC | Band-shuffle AUC | Read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `amino_acid_vs_mineral_405nm` | 22 | 8 / 14 | 192 | 0.950000 | 0.485733 | 0.003984 | 0.166667 | 0.900000 | support |
| `pah_vs_amino_acid_405nm` | 12 | 4 / 8 | 189 | 1.000000 | 0.535222 | 0.035857 | 0.305556 | 0.888889 | support |
| `carbon_allotrope_vs_mineral_all_lasers` | 49 | 7 / 42 | 169 | 0.629630 | 0.546453 | 0.362550 | 0.490741 | 0.496296 | candidate / review |

## Interpretation

- `amino_acid_vs_mineral_405nm` tests whether the first support row survives same-laser filtering.
- `pah_vs_amino_acid_405nm` tests a same-laser organic aromatic versus biomolecular primitive split.
- `carbon_allotrope_vs_mineral_all_lasers` tests a material-family split with limited carbon-compound count.

Use the observed-vs-shuffled and observed-vs-feature-shuffle gap as the support read. Treat band-shuffle results as a warning layer: if band-shuffle stays high, the evidence is still class-level transition-structure support, not pure spectral-position / phase-lock closure.

## Boundary

These are public transition-table controls. They do not replace the full raw/processed CSV rerun. They also do not close Terahertz, Fire + Plasma, Fusion + Solar, Space / Time / Cycles, Gases / Liquids / Phases, Gravity / Orbits, EMF / Fields, or Oscillators / Resonance.

## Next Gate

Open the Fire + Plasma source gate and select a public combustion / flame-emission / plasma spectrum dataset with state/control labels.
