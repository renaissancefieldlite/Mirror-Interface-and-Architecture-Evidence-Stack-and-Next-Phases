# Nest 4 Metabolism UDP Support Read

Date: `2026-05-21`

Run ID: `nest4_metabolism_diabetes_udp_2026-05-21`

Status: `real_data / first_pass / metabolic_state / nutrient_extension_open`

## Source

Dataset: `scikit-learn load_diabetes`

Underlying source: real diabetes clinical/metabolic benchmark containing baseline age, sex, BMI, blood pressure, and six serum measurements for diabetes patients, plus one-year disease-progression outcome.

This pass uses the highest and lowest progression quartiles to define a first target/control metabolic state test:

- raw samples: `442`
- used extreme-state samples: `223`
- high-progression state count: `111`
- low-progression control count: `112`
- measured features: `10`

This is a real metabolic clinical feature pass. It does not close food chemistry, nutrient response, metabolomics, microbiome, or paired HRV/Muse response.

## Universal Data Pattern Packet

| Field | Read |
| --- | --- |
| `source` | Real diabetes clinical/metabolic benchmark |
| `state` | high one-year disease-progression quartile |
| `control` | low one-year disease-progression quartile, shuffled labels, and per-feature row shuffle |
| `transform` | standardized clinical/metabolic feature vector plus logistic classifier |
| `invariant` | high vs low metabolic state separation should persist across stratified folds |
| `drift` | small sample size, quartile thresholding, feature scale, fold variance, shuffled controls |
| `score` | ROC-AUC, average precision, balanced accuracy, permutation p-value |
| `failure mode` | observed AUC near shuffled/control AUC, fold instability, or no separation |

## Results

| Metric | Observed | Shuffled-label control | Feature-shuffle control |
| --- | ---: | ---: | ---: |
| `ROC-AUC mean` | `0.962846` | `0.496071` | `0.498994` |
| `Average precision mean` | `0.963060` | `not repeated` | `0.525519` |
| `Balanced accuracy mean` | `0.896443` | `not repeated` | `0.493478` |
| `Permutation p-value` | `0.009901` | `100 repeats` | `n/a` |

## Top Separating Feature Effects

| Feature | high minus low mean | effect size |
| --- | ---: | ---: |
| `s5` | `0.074766` | `2.095901` |
| `bmi` | `0.071462` | `1.776795` |
| `s4` | `0.057842` | `1.345171` |
| `bp` | `0.055711` | `1.308725` |
| `s3` | `-0.051064` | `-1.191740` |
| `s6` | `0.046376` | `1.023561` |
| `s1` | `0.032088` | `0.697351` |
| `age` | `0.025335` | `0.585604` |
| `s2` | `0.026913` | `0.572692` |
| `sex` | `0.007253` | `0.152018` |

## Support Read

This run upgrades `Metabolism` from mapped continuation to `candidate_support` for the clinical metabolic-state sublane.

The observed high-vs-low progression state separates above shuffled-label and feature-shuffle controls. That shows the Universal Data Pattern packet can be applied to a real metabolic measurement surface:

```text
metabolic clinical source -> high/control state -> transform -> drift controls -> score -> support read
```

## Boundary

This is not a clinical predictor claim, treatment claim, nutrition claim, or metabolomics closeout.

Public-safe wording:

```text
First real metabolic-state pass completed on a public diabetes clinical/metabolic benchmark. The lane now has candidate support for measured high-vs-low metabolic state separation under UDP controls. Food/nutrient/metabolomics extension remains open.
```

## Next Gate

Run the same UDP packet on a public food, nutrient, metabolite, or pathway dataset:

- FoodData / FooDB nutrient vector rows;
- HMDB / metabolite class rows;
- pathway or metabolomics condition-vs-control rows;
- later paired food/metabolism plus HRV/Muse state-window response.

