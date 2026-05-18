# Nest 2 Li Conductivity Real-Data Row

Status: `public_safe_support_read / local_not_yet_pushed`

## Front-Center Read

The membrane / conductivity branch now has a real Li solid-electrolyte support
row.

This row uses public literature-derived conductivity records and tests whether
formula composition, temperature, material family, and structure class recover
log conductivity and high-conductivity state above shuffled controls.

## Source

- Dataset: `foundry-ml/dataset_li_conductivity`
- Public page: <https://huggingface.co/datasets/foundry-ml/dataset_li_conductivity>

## Target QA

- rows: `372`
- literature sources: `152`
- material families: `12`
- chemical families: `6`
- high-conductivity class rows: `150`
- temperature range: `15.00` to `35.00` C
- log conductivity range: `-15.301030` to `-1.602060`
- shuffled controls per read: `250`

## State Map

| Variable | Conductivity expression |
| --- | --- |
| `state` | Li material formula, temperature, family, structure class, log conductivity |
| `control` | shuffled conductivity labels under fixed split / mode |
| `transform` | formula composition -> element fractions / family metadata -> conductivity readout |
| `drift` | chemistry-family shifts, source-group holdout, temperature and structural class variation |
| `quality` | real literature-source rows; group holdout by source for primary support read |
| `support` | regression and high-conductivity classification over shuffled controls |

## Regression Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `formula_source_group_holdout` | `110` | `294` | `78` | `0.700478` | `0.490242` | `1.500366` | `2.127306` | `0.003984` |
| `family_source_group_holdout` | `141` | `295` | `77` | `0.723221` | `0.496716` | `1.242952` | `1.760591` | `0.003984` |
| `formula_family_group_holdout` | `110` | `279` | `93` | `0.105857` | `-0.862131` | `2.782019` | `2.040066` | `0.314741` |

## Classification Results

| Mode | Features | Train | Test | ROC AUC | AP | Balanced Acc | Macro F1 | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `formula_source_group_holdout` | `110` | `275` | `97` | `0.702614` | `0.665255` | `0.669468` | `0.673558` | `0.003984` |
| `family_source_group_holdout` | `141` | `296` | `76` | `0.891199` | `0.866407` | `0.855509` | `0.855238` | `0.003984` |
| `formula_family_group_holdout` | `110` | `218` | `154` | `0.649597` | `0.616433` | `0.628581` | `0.596690` | `0.003984` |

## Read

Li conductivity seats the membrane / conductivity branch as a real
materials-response row.

The strongest support mode is source-heldout formula-plus-family classification:
ROC AUC `0.891199`, average precision `0.866407`, balanced accuracy `0.855509`,
macro F1 `0.855238`, p `0.003984`.

The regression read also clears controls under source holdout:
formula-only Pearson `0.700478`, p `0.003984`; formula-plus-family Pearson
`0.723221`, p `0.003984`.

The family-heldout regression boundary remains visible: Pearson `0.105857`,
p `0.314741`. That boundary is useful because it says the row is strongest
inside source-heldout literature generalization and still needs broader
cross-family transport hardening.

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | structured-matter / electrochemistry row gains ion-conductivity support |
| `Nest 3` | conductivity becomes a charge / transport / field-response bridge |
| `Nest 4` | membrane and ion-transport language now has a real materials-side precursor |
| `Nest 5` | convergence matrix can route conductivity as source-heldout support with family-heldout boundary |
| `FIG.14` | external adapter lane includes membrane / conductivity examples |
| `FIG.15` | support-state routing can separate source-heldout support from cross-family continuation |

## Next Gate

```text
Li conductivity seated
-> membrane / ion-transport crosswalk
-> dissolved oxygen / ROS or grid-flow row
```
