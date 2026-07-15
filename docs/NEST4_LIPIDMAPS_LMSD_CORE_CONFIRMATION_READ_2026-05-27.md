# LIPID MAPS LMSD Core Confirmation Read

Date: `2026-05-27`

Run ID: `nest4_lipidmaps_lmsd_core_confirmation_2026-05-27`

Status: `real_data / LIPID_MAPS_LMSD / independent_lipid_class_candidate_support / HMDB_open`

## Source

Dataset: LIPID MAPS Structure Database (LMSD) public REST export.

LMSD download page: https://lipidmaps.org/databases/lmsd/download

REST export used: https://www.lipidmaps.org/rest/compound/lm_id/LM/all/download

Local source file:

```text
private-local source table: experiments/nest4_lipidmaps_independent_lipid/data/raw/LMSD_all_download.tsv
```

Parse notes:

- source date line: `05/28/26`
- raw data lines: `50452`
- parsed rows: `50449`
- skipped malformed rows: `3`
- structure rows after cleaning/deduplication: `49811`
- features used: `31`

LMSD lipid-core rows after cleaning:

| Core label | Rows |
| --- | ---: |
| `Fatty Acyls [FA]` | `11636` |
| `Glycerophospholipids [GP]` | `10543` |
| `Glycerolipids [GL]` | `7795` |
| `Polyketides [PR]` | `7206` |
| `Sphingolipids [SP]` | `4621` |
| `Sterols [ST]` | `4068` |
| `Prenol Lipids [PR]` | `2592` |
| `Saccharolipids [SL]` | `1350` |

## Universal Data Pattern Packet

| Field | Read |
| --- | --- |
| `source` | LIPID MAPS LMSD public lipid structure rows |
| `state` | LMSD lipid-core labels, with a primary GP/SP contrast |
| `control` | shuffled labels and per-feature row shuffle |
| `transform` | formula counts, exact mass, element ratios, unsaturation proxy, SMILES-derived structural counts |
| `invariant` | independent lipid-core labels should remain separable from real structure/property rows |
| `drift` | LMSD class imbalance, malformed rows, formula variants, SMILES lexical bias, class-family overlap |
| `score` | ROC-AUC, average precision, balanced accuracy, macro AUC/F1, permutation p-value |
| `failure mode` | observed score near shuffled/control score, or separation only surviving through label/text leakage |

Names, systematic names, class strings, IDs, and source metadata are excluded
from the feature matrix.

## Primary Binary Core Contrast

Target/control:

```text
Glycerophospholipids [GP] vs Sphingolipids [SP]
```

Rows:

- total: `6000`
- target: `3000`
- control: `3000`

| Metric | Observed | Shuffled-label control | Feature-shuffle control |
| --- | ---: | ---: | ---: |
| `ROC-AUC mean` | `0.999506` | `0.500031` | `0.510393` |
| `Average precision mean` | `0.999569` | `not repeated` | `0.508678` |
| `Balanced accuracy mean` | `0.990833` | `not repeated` | `0.509333` |
| `F1 mean` | `0.990878` | `not repeated` | `0.521474` |
| `Permutation p-value` | `0.009901` | `100 repeats` | `n/a` |

## Multiclass Lipid-Core Panel

The multiclass panel uses all cleaned LMSD core labels with at least `1000`
source rows, then draws a deterministic balanced sample.

Rows by label:

| Core label | Sample rows |
| --- | ---: |
| `Fatty Acyls [FA]` | `1200` |
| `Glycerolipids [GL]` | `1200` |
| `Glycerophospholipids [GP]` | `1200` |
| `Polyketides [PR]` | `1200` |
| `Prenol Lipids [PR]` | `1200` |
| `Saccharolipids [SL]` | `1200` |
| `Sphingolipids [SP]` | `1200` |
| `Sterols [ST]` | `1200` |

| Metric | Observed | Shuffled-label control | Feature-shuffle control |
| --- | ---: | ---: | ---: |
| `Macro ROC-AUC mean` | `0.991753` | `not repeated` | `0.494685` |
| `Balanced accuracy mean` | `0.918646` | `0.125333` | `0.124583` |
| `Macro F1 mean` | `0.918256` | `not repeated` | `0.121665` |
| `Permutation p-value` | `0.019608` | `50 repeats` | `n/a` |

## Top Primary-Contrast Feature Effects

| Feature | target minus control mean | effect size |
| --- | ---: | ---: |
| `p_to_c_ratio` | `0.022728` | `3.308028` |
| `formula_P` | `1.040667` | `3.086193` |
| `formula_N` | `-2.343333` | `-2.004546` |
| `smiles_bracket_count` | `-50.814667` | `-1.891638` |
| `n_to_c_ratio` | `-0.023793` | `-1.844131` |
| `smiles_ring_digits` | `-9.518333` | `-1.779207` |
| `smiles_len` | `-191.864667` | `-1.649376` |
| `smiles_branches` | `-32.046667` | `-1.589414` |
| `formula_O` | `-19.016000` | `-1.437498` |
| `hetero_atoms` | `-20.324333` | `-1.437149` |
| `heavy_atoms_selected` | `-48.772667` | `-1.417362` |
| `exactmass` | `-696.638150` | `-1.391796` |

## Support Read

This is the first independent LIPID MAPS confirmation row for the Nest 4
biomolecular primitive lane. It does not reuse ChEBI ontology membership. LMSD
lipid-core labels remain separable from structure/property features while
shuffled-label and feature-shuffle controls collapse.

Public-safe wording:

```text
LIPID MAPS LMSD source gate completed. Independent lipid-core labels show
candidate support under UDP controls using public LMSD structure/property rows.
This confirms the lipid branch as a separate public source lane from ChEBI.
```

## Boundary

This is not HMDB metabolomics, not GlyTouCan glycan confirmation, not a clinical
metabolism claim, not a nutrition recommendation, and not paired HRV/Muse/Thermo
physiology.

## Next Gate

Run:

```text
GlyTouCan glycan/carbohydrate confirmation
```

Then:

```text
HMDB access/download check
HRV + Muse + Thermo paired physiology manifest
```
