# Nest 2C Molecule Benchmark Expansion

Date: `2026-04-28`

Status: `completed_multi_benchmark_molecule_signal_supported`

Companion report:

- [Nest 2C Molecule Benchmark Expansion Report](../artifacts/validation/nest2c_molecule_benchmark_expansion/nest2c_molecule_benchmark_expansion_report.md)

## Purpose

`Nest 2C` expands the first `Engine 02V` molecule-property result beyond the
single Delaney / ESOL benchmark.

The validation question is:

```text
does the same structured-matter comparator carry real molecule-property signal
across multiple public datasets under shuffled-target controls?
```

## What Was Run

Four real molecule-property datasets were tested:

- `ESOL / Delaney`: measured aqueous solubility
- `Lipophilicity / ChEMBL`: experimental lipophilicity
- `FreeSolv / SAMPL`: experimental hydration free energy
- `QM9 alpha`: quantum-chemistry polarizability

Each dataset was run twice with different shuffled-control seeds:

- seed `67`
- seed `68`

All final runs used `5000` shuffled-target permutations.

## Result

All four datasets were control-supported across both seeds.

| Dataset | Rows | Abs Pearson | p | Read |
| --- | ---: | ---: | ---: | --- |
| `ESOL` | `1128` | `0.5587` | `0.0002` | strongest measured-property signal |
| `Lipophilicity` | `4200` | `0.2042` | `0.0002` | drug-like property signal |
| `FreeSolv` | `642` | `0.3951` | `0.0002` | thermodynamic / solvent interaction signal |
| `QM9 alpha` | `133885` | `0.0898` | `0.0002` | large quantum-chemistry property signal |

The exact repeated rows are preserved in:

```text
artifacts/validation/nest2c_molecule_benchmark_expansion/nest2c_molecule_benchmark_summary.csv
```

## Interpretation

This upgrades `Nest 2` from a structured-matter grammar map plus one molecule
benchmark into a multi-benchmark real-data molecule-property lane.

The result says:

```text
real molecule descriptors carry repeatable property signal across several
independent public molecule benchmarks, above shuffled-target controls
```

That is the correct claim. It is meaningful, but bounded.

## Boundary

This does not claim completed chemistry or physical validation across all
matter.

It does not yet validate:

- allostery / protein pathway communication
- PFAS / contaminant degradation pathways
- materials / crystal stability
- reaction safety or bad-descendant scoring on real reaction products

Those are next gates, not completed results.

## Why It Matters

The `Source Mirror Pattern` / Mirror Architecture score spine is now being
tested against real structured matter instead of only toy examples.

The current support is not rhetorical. It comes from:

- real molecules
- public datasets
- fixed descriptor scoring
- declared shuffled-target controls
- repeated control seeds
- consistent support across four property surfaces

## Next Step

Move from molecule-property benchmarks into pathway and graph validation:

1. `Nest 2D`: allostery / protein communication graph labels.
2. `Nest 2E`: PFAS / contaminant degradation-pathway labels and bad-descendant
   penalties.
3. `Nest 2F`: materials / crystal-stability labels.
4. `Nest 2G`: stronger descriptor families and baseline models.
