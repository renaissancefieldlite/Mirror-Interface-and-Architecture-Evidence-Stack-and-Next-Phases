# Nest 3 THz Biology Manifest + Shared-Feature Holdout Read

Date: `2026-06-12`

Run ID: `nest3_thz_bio_manifest_shared_holdout_2026-06-12`

Status: `harmonized_manifest_and_cross_source_holdouts_complete`

## Gate State

This gate hardens the biological Terahertz lane after the first GEO panel.

The earlier panel showed that real public biological THz/control expression
rows exist, with `GSE178729` landing as the strongest same-source
support-bearing row and several other sources landing as candidate or weak/null
under held-out biological-replicate scoring.

This follow-up asked the harder question: does that source-specific biological
response transfer across public studies when the model is forced to use shared
features, shared mouse gene symbols, or shared GO-process pathway terms?

Plain English: the manifest is now seated, but the cross-source biological
transfer did not harden. The data supports a real biological THz source-gate
arc. It does not yet support a broad shared biological pathway claim.

## Harmonized Source Manifest

| Accession | Surface | Frequency | Power | Duration | Control | Role |
| --- | --- | --- | --- | --- | --- | --- |
| `GSE248763` | HUVEC / human umbilical vein endothelial cells | `2.52 THz` | `100 mW/cm2` | `10 min exposure; 12 h post-culture` | sham/control | manifest-only in this gate |
| `GSE243842` | C. elegans whole body | `0.26 THz` | not explicit in cached GEO matrix | not explicit in cached GEO matrix | control | manifest-only in this gate |
| `GSE41083` | mouse mesenchymal stem cells | `~10 THz` broadband | `1 mW/cm2` | `2 h exposure` | adjacent non-irradiated; same temperature reported | same-platform + mouse shared-feature holdout |
| `GSE41084` | mouse mesenchymal stem cells | `~10 THz` broadband | `1 mW/cm2` | `12 h exposure` | adjacent non-irradiated; same temperature reported | same-platform + mouse shared-feature holdout |
| `GSE41085` | mouse mesenchymal stem cells | `2.52 THz` continuous wave | `<1 mW/cm2` reported in series summary | `2 h exposure` | adjacent non-irradiated; same temperature reported | same-platform + mouse shared-feature holdout |
| `GSE44671` | mouse full-thickness dorsal skin | not explicit in cached GEO matrix | not explicit in cached GEO matrix | `1 h exposure; 24 h post-exposure sampling` | sham/control | mouse shared-gene/pathway holdout |
| `GSE178729` | mouse neuron culture | `3.1 THz` | not explicit in cached GEO matrix | `3 h/day from DIV5-DIV9; collected at DIV12` | control culture | manifest-only in this gate |

Manifest CSV emitted locally:

```text
experiments/nest3_thz_bio_exposure_geo_2026_06_11/results/nest3_thz_bio_harmonized_manifest_2026-06-12.csv
```

## Cross-Source Controls

Three stricter transfer gates were run:

- same-platform mMSC shared-probe leave-source-out across `GSE41083`,
  `GSE41084`, and `GSE41085`;
- mouse shared-gene-symbol leave-source-out across `GSE41083`, `GSE41084`,
  `GSE41085`, and `GSE44671`;
- mouse shared-GO-process pathway leave-source-out across the same mouse
  sources.

Each gate used unsupervised within-source z-scoring before leave-source-out
training. Controls included balanced label shuffles and feature-identity
shuffles.

## Result Summary

| Gate | Shared features | Balanced accuracy | ROC AUC | Label-shuffle p(AUC >= observed) | Feature-shuffle p(AUC >= observed) | Class |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| mMSC same-platform shared probes | `45,101` | `0.555556` | `0.518519` | `0.410000` | `0.570000` | weak/mixed |
| mouse shared gene symbols | `17,090` | `0.500000` | `0.465278` | `0.520000` | `0.560000` | weak/mixed |
| mouse shared GO-process pathways | `11,010` | `0.541667` | `0.548611` | `0.440000` | `0.420000` | weak/mixed |

The held-out source behavior was mixed. Some rows transferred in the expected
direction, but others inverted or collapsed. The most visible conflict is that
`GSE41084` behaves differently under source holdout even inside the same mMSC
platform family.

## Support Read

This gate strengthens the evidence discipline more than it strengthens the
biological claim.

The good news: the Terahertz biological lane now has a harmonized manifest with
real public exposure metadata across seven GEO sources. That keeps the bridge
alive and gives the next source-on/source-off work a clean target.

The honest limit: shared-feature and shared-pathway transfer stayed weak/mixed.
That means the current public GEO panel should be read as source-specific THz
biological response evidence, not as a universal THz biology pathway signature.

This matters because it keeps the architecture arc clean. The pattern is not
being forced to pass every projection. When the shared projection breaks, the
result tells us which physical control is missing: frequency, power, duration,
temperature, off-window, heat-matched, and source-disabled baselines.

## Boundary

This is not therapeutic proof, not medical THz tuning, and not a claim that THz
biology has a universal pathway response across tissues and platforms.

`GSE248763`, `GSE243842`, and `GSE178729` remain manifest/same-source rows in
this pass because orthology-backed cross-species projection and GPL21163
platform annotation were not seated here.

The complete physical-control matrix remains open.

## Next Gate

The next clean proof layer is one of:

1. local or partner THz/EMF source-on/source-off rows with source-disabled
   baseline, temperature, power, distance, duration, and instrument-state
   logging;
2. a public or partner frequency/power/duration stratified THz biological
   source with sham, off-window, and heat-matched controls;
3. an orthology-backed cross-species gene/pathway projection if HUVEC,
   C. elegans, neural culture, mMSC, and skin need to be placed into one shared
   biological pathway panel.

The preferred next run is local/partner source-on/source-off capture, because
that directly answers what the public GEO matrix cannot close.
