# Nest 4 / Nest 2 UDP Support Arc Public-Safe Summary

Date: `2026-05-21`

Status: `public_safe_summary / real_data_only / repo_ready_docs_layer`

## Read

The May 21 run stack strengthens the Nest biology and biomolecular bridge with
five real-data UDP support reads. The shared packet is:

```text
source -> state/control -> transform -> drift controls -> score -> support read
```

Across the runs, observed target/control separation stays high when the real
state and feature structure are preserved. Shuffled-label and feature-shuffle
controls collapse toward chance.

## Support Rows

| Lane | Source surface | Target/control read | Observed ROC-AUC | Shuffled-label control | Feature-shuffle control | Support status |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `Cells + Genome` | WDBC cell nuclei morphology | malignant vs benign morphology | `0.995106` | `0.504062` | `0.500819` | `candidate_support`; morphology sublane |
| `Metabolism` | diabetes clinical/metabolic benchmark | high vs low progression quartile | `0.962846` | `0.496071` | `0.498994` | `candidate_support`; clinical metabolic-state proxy |
| `Food / Nutrients` | USDA FoodData Central Foundation Foods | protein/fat/mineral categories vs fruit/vegetable categories | `0.988659` | `0.489304` | `0.547055` | `candidate_support`; nutrient-composition bridge |
| `Biomolecular Primitives` | ChEBI class text + chemical properties | amino-acid vs fatty-acid rows | `0.981367` | `0.501045` | `0.508480` | `candidate_support`; first biochemical primitive read |
| `Biomolecular Primitives` | ChEBI `is_a` ontology + chemical properties | amino-acid descendants vs fatty-acid descendants | `0.993090` | `0.498564` | `0.508743` | `candidate_support`; ontology-backed closure gate |
| `Biomolecular Primitives` | ChEBI `is_a` ontology + chemical properties | nucleotide descendants vs carbohydrate descendants | `0.999957` | `0.499336` | `0.496904` | `candidate_support`; second ontology-backed closure gate |
| `Biomolecular Primitives` | LIPID MAPS LMSD public structure rows | glycerophospholipids vs sphingolipids | `0.999506` | `0.500031` | `0.510393` | `candidate_support`; independent lipid-source confirmation |
| `Biomolecular Primitives` | LIPID MAPS LMSD public structure rows | eight-way lipid-core panel | `0.918646` balanced accuracy | `0.125333` balanced accuracy | `0.124583` balanced accuracy | `candidate_support`; multiclass lipid-core panel |
| `Biomolecular Primitives` | GlyTouCan/GlyCosmos RDF glycan sequence rows | human source glycans vs mouse source glycans | `0.739219` | `0.499838` | `0.525007` | `candidate_support`; independent glycan-source confirmation |

## Public-Safe Interpretation

These runs support a structure-dependent read:

```text
The measured state/control separation depends on preserving the real source
pattern. When target/control labels or feature-to-row structure are broken, the
support signal collapses toward chance.
```

This does not turn every lane into a final closeout. It upgrades the mapped
Nest biology/metabolism/biomolecular bridge into a support-bearing arc with
specific remaining gates.

## Current Lane State

| Lattice row | Current read | Open gate |
| --- | --- | --- |
| `N4-03 Cells + Genome` | WDBC morphology candidate support | transcriptome / pathway / perturbation dataset |
| `N4-04 Metabolism` | diabetes + USDA + ChEBI bridge candidate support | direct metabolomics or HRV/Muse response pairing |
| `N2-07 Food Chemistry` | USDA nutrient-vector candidate support | FooDB / HMDB / paired physiology response |
| `N2-10 Vitamins + Nutrients` | USDA nutrient/mineral features seated | cofactor/HMDB class rows |
| `N2-13 Biomolecular Primitives` | ChEBI ontology-backed candidate support plus independent LIPID MAPS lipid-core and GlyTouCan glycan-source confirmations; HMDB verified as access-gated continuation | HMDB permission/download clearance |

## Figure / Visual Hook

Public-safe visual:

```text
visuals/nest4_udp_support_arc_2026-05-21.svg
```

## Boundary

This summary is repo-safe as a findings layer. It does not expose private raw
captures, private code mechanics, biometric exports, device identifiers, or
claim-sensitive execution details.

It does not claim clinical diagnosis, treatment, diet recommendation,
metabolomics closeout, or direct HRV/Muse response completion.

## Next Gates

1. Clear HMDB permission/download path if possible.
2. Pair nutrient/metabolite rows to HRV/Muse/Thermo state windows.
