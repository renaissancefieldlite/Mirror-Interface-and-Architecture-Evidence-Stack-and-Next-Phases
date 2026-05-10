# Nest 2C Molecule Benchmark Expansion Report

Date: `2026-04-28`

Status: `completed_multi_benchmark_molecule_signal_supported`

## Purpose

This report expands `Engine 02V` from a single molecule-property validation
fork into a multi-benchmark check.

The goal is not to claim "all chemistry." The goal is narrower and testable:

```text
real molecule structure -> RDKit descriptors -> real measured or benchmarked
property target -> shuffled-target controls
```

If the descriptor score keeps signal above shuffled labels across multiple
datasets and control seeds, `Nest 2` moves from pending real-data validation mapping into a
real cheminformatics property lane.

## Datasets

| Dataset | Rows | Target | Why It Matters |
| --- | ---: | --- | --- |
| `ESOL / Delaney` | `1128` | measured log solubility | measured aqueous solubility property |
| `Lipophilicity / ChEMBL` | `4200` | experimental lipophilicity | drug-like property surface |
| `FreeSolv / SAMPL` | `642` | experimental hydration free energy | solvent / thermodynamic interaction surface |
| `QM9 alpha` | `133885` | polarizability `alpha` | large quantum-chemistry property benchmark |

## Locked Control

Each dataset was run twice:

- run `1`: seed `67`
- run `2`: seed `68`

Each run used:

- fixed molecule rows
- fixed `SMILES` parsing through `RDKit`
- fixed descriptor score
- shuffled-target permutation control
- `5000` permutations per run

The second run changes the shuffled-control seed only. The molecular data and
descriptor calculation stay fixed. This tests whether support depends on one
lucky shuffle seed.

## Result Table

| Dataset | Run | Rows | Pearson | Abs Pearson | Null Mean Abs | p | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `ESOL` | `1` | `1128` | `-0.5587` | `0.5587` | `0.0243` | `0.0002` | supported |
| `ESOL` | `2` | `1128` | `-0.5587` | `0.5587` | `0.0237` | `0.0002` | supported |
| `Lipophilicity` | `1` | `4200` | `0.2042` | `0.2042` | `0.0122` | `0.0002` | supported |
| `Lipophilicity` | `2` | `4200` | `0.2042` | `0.2042` | `0.0125` | `0.0002` | supported |
| `FreeSolv` | `1` | `642` | `-0.3951` | `0.3951` | `0.0323` | `0.0002` | supported |
| `FreeSolv` | `2` | `642` | `-0.3951` | `0.3951` | `0.0313` | `0.0002` | supported |
| `QM9 alpha` | `1` | `133885` | `-0.0898` | `0.0898` | `0.0022` | `0.0002` | supported |
| `QM9 alpha` | `2` | `133885` | `-0.0898` | `0.0898` | `0.0022` | `0.0002` | supported |

Source CSV:

```text
artifacts/validation/nest2c_molecule_benchmark_expansion/nest2c_molecule_benchmark_summary.csv
```

## What The Readouts Mean

`valid_rows` is the number of molecules that successfully parsed into `RDKit`
objects and had a usable target value.

`Pearson` measures whether the fixed molecular descriptor score moves with the
dataset target. Negative is still signal; it means higher descriptor values
track lower target values. The direction depends on the property.

`Abs Pearson` ignores direction and asks how strong the relationship is.

`Null Mean Abs` is the average absolute Pearson correlation after target labels
are randomly shuffled. This is the "what would random alignment usually look
like?" baseline.

`p` is the fraction of shuffled-control runs that matched or beat the real
absolute Pearson. With `5000` permutations, `0.0002` means the real descriptor
signal beat every shuffled run, so the result lands at the minimum measurable
floor for that run size.

## Clean Read

This is the first multi-benchmark real-data support for `Nest 2C`.

The descriptor score is not a final chemistry model, but the lane is no longer
bounded score schema. It maps real molecular structure into real property targets
across solubility, lipophilicity, hydration free energy, and quantum-chemistry
polarizability, and it survives shuffled-target controls across two seeds.

## Boundary

This does not validate:

- all chemistry
- allostery or protein signaling
- PFAS degradation or safe mineralization
- materials stability
- clinical biology

It validates a narrower statement:

```text
the Nest 2 structured-matter comparator has real molecule-property signal
across multiple public molecule benchmarks under shuffled-target controls
```

## Next Gates

1. `Nest 2D`: real allostery / protein graph labels.
2. `Nest 2E`: PFAS / contaminant degradation pathways with bad-descendant
   scoring.
3. `Nest 2F`: materials / crystal stability with `pymatgen`, `ASE`, or
   Materials Project style data.
4. `Nest 2G`: upgrade descriptor score from simple RDKit descriptor composite
   to locked feature families and baseline comparisons.
