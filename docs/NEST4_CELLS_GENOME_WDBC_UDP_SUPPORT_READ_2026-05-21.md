# Nest 4 Cells + Genome UDP Support Read

Date: `2026-05-21`

Run ID: `nest4_cells_genome_wdbc_udp_2026-05-21`

Status: `real_data / first_pass / cell_state_morphology / genome_extension_open`

## Source

Dataset: `scikit-learn load_breast_cancer`

Underlying source: Wisconsin Diagnostic Breast Cancer cell-nuclei feature dataset.

This is a real cell-morphology dataset with `569` samples and `30` measured nuclei features. It supports a first Cells + Genome lane pass through cell-state morphology. It does not close transcriptome, epigenome, or genome-sequence validation.

## Universal Data Pattern Packet

| Field | Read |
| --- | --- |
| `source` | Real cell-nuclei morphology dataset |
| `state` | malignant diagnostic class |
| `control` | benign diagnostic class, shuffled labels, and per-feature row shuffle |
| `transform` | standardized nuclei feature vector plus logistic classifier |
| `invariant` | class separation should persist across stratified folds |
| `drift` | class imbalance, feature scale, fold variance, shuffled controls |
| `score` | ROC-AUC, average precision, balanced accuracy, permutation p-value |
| `failure mode` | observed AUC near shuffled/control AUC, high fold instability, or no separation |

## Results

| Metric | Observed | Shuffled-label control | Feature-shuffle control |
| --- | ---: | ---: | ---: |
| `ROC-AUC mean` | `0.995106` | `0.504062` | `0.500819` |
| `Average precision mean` | `0.993507` | `not repeated` | `0.381848` |
| `Balanced accuracy mean` | `0.972199` | `not repeated` | `0.519056` |
| `Permutation p-value` | `0.009901` | `100 repeats` | `n/a` |

## Top Separating Feature Effects

| Feature | malignant minus benign mean | effect size |
| --- | ---: | ---: |
| `worst concave points` | `0.107793` | `2.604476` |
| `worst perimeter` | `54.364392` | `2.371866` |
| `mean concave points` | `0.062273` | `2.325082` |
| `worst radius` | `7.755010` | `2.323756` |
| `mean perimeter` | `37.289971` | `2.122999` |
| `mean radius` | `5.316306` | `2.051141` |
| `worst area` | `863.386881` | `1.969554` |
| `mean concavity` | `0.114717` | `1.871437` |
| `mean area` | `515.586219` | `1.861605` |
| `worst concavity` | `0.284368` | `1.752691` |

## Support Read

This run upgrades `Cells + Genome` from mapped continuation to `candidate_support` for the cell-state morphology sublane.

The observed class/state separation is far above shuffled-label and feature-shuffle controls. That is useful because it shows the same UDP packet can be applied to a real cellular measurement surface:

```text
cell measurement source -> state/control class -> transform -> drift controls -> score -> support read
```

## Boundary

This is not a clinical claim, diagnosis system, or genome/transcriptome closeout.

Public-safe wording:

```text
First real cell-state morphology pass completed on a public cell-nuclei dataset. The lane now has candidate support for measured cell-state separation under UDP controls. Genome/transcriptome extension remains open.
```

## Next Gate

Run the same UDP packet on a public expression, pathway, or perturbation dataset:

- transcriptome condition vs control;
- epigenome / chromatin accessibility;
- pathway module preservation;
- cell-signaling or perturb-seq response.

