# Nest 4 Food / Nutrient Composition UDP Support Read

Date: `2026-05-21`

Run ID: `nest4_usda_food_nutrient_udp_2026-05-21`

Status: `real_data / USDA_FoodData_Central / food_nutrient_composition / metabolism_response_open`

## Source

Dataset: USDA FoodData Central Foundation Foods CSV, April 2026 release.

Download page: https://fdc.nal.usda.gov/download-datasets/

Archive: `FoodData_Central_foundation_food_csv_2026-04-30.zip`

This pass uses real USDA food composition tables:

- foundation foods total: `395`
- used target/control foods: `322`
- nutrient features used: `55`
- target foods: `177`
- control foods: `145`

Target state:

```text
protein/fat/mineral-dense food categories
```

Control state:

```text
fruit/vegetable categories
```

This is a real food/nutrient composition pass. It does not close clinical metabolism, diet response, metabolomics, microbiome, or paired HRV/Muse response.

## Universal Data Pattern Packet

| Field | Read |
| --- | --- |
| `source` | Official USDA FoodData Central Foundation Foods nutrient tables |
| `state` | protein/fat/mineral-dense food-category group |
| `control` | fruit/vegetable food-category group, shuffled labels, and per-feature row shuffle |
| `transform` | nutrient amount pivot per food plus standardized classifier |
| `invariant` | nutrient composition should separate category state across folds |
| `drift` | missing nutrients, category imbalance, measurement variation, feature scale |
| `score` | ROC-AUC, average precision, balanced accuracy, permutation p-value |
| `failure mode` | observed AUC near shuffled/control AUC, fold instability, or no category-state separation |

## Results

| Metric | Observed | Shuffled-label control | Feature-shuffle control |
| --- | ---: | ---: | ---: |
| `ROC-AUC mean` | `0.988659` | `0.489304` | `0.547055` |
| `Average precision mean` | `0.993494` | `not repeated` | `0.595525` |
| `Balanced accuracy mean` | `0.950290` | `not repeated` | `0.539053` |
| `Permutation p-value` | `0.009901` | `100 repeats` | `n/a` |

## Top Separating Nutrient Effects

| Nutrient feature | target minus control mean | effect size |
| --- | ---: | ---: |
| `Protein` | `15.635359` | `2.080077` |
| `Phosphorus, P` | `237.912527` | `1.537081` |
| `Zinc, Zn` | `1.862017` | `1.534575` |
| `Water` | `-34.341423` | `-1.346839` |
| `Energy (Atwater General Factors)` | `154.175570` | `1.039407` |
| `Energy (Atwater Specific Factors)` | `149.481313` | `1.030184` |
| `Total lipid (fat)` | `13.780412` | `1.013351` |
| `Vitamin C, total ascorbic acid` | `-22.825004` | `-0.893363` |
| `Fatty acids, total saturated` | `3.464732` | `0.788037` |
| `Magnesium, Mg` | `50.494045` | `0.757933` |
| `Iron, Fe` | `1.350151` | `0.735428` |
| `Fatty acids, total monounsaturated` | `3.449181` | `0.673078` |

## Support Read

This run upgrades the food/nutrient side of the metabolism bridge from mapped continuation to `candidate_support` for the USDA food-composition sublane.

The observed nutrient-vector separation sits far above shuffled-label and feature-shuffle controls. That shows the same Universal Data Pattern packet can be applied to a real nutrition composition surface:

```text
official food composition source -> state/control food class -> nutrient transform -> drift controls -> score -> support read
```

## Boundary

This is not a nutrition recommendation, diet claim, treatment claim, clinical metabolism claim, metabolomics validation, or paired HRV/Muse response claim.

Public-safe wording:

```text
First real USDA FoodData Central nutrient-composition pass completed. The lane now has candidate support for measured food-class nutrient-vector separation under UDP controls. Metabolic response and HRV/Muse pairing remain open.
```

## Next Gate

Run one of the following:

- HMDB / metabolite class rows;
- FoodData or FooDB nutrient-response refinement;
- paired food/metabolism plus HRV/Muse response session;
- pathway/module mapping between nutrients, metabolites, and physiology state windows.

