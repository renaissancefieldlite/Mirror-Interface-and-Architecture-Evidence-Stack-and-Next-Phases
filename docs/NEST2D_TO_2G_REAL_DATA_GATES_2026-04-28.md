# Nest 2D To 2G Real-Data Gates

Date: `2026-04-28`

Status: `completed_mixed_real_data_closeout`

Companion reports:

- [Nest 2D Allostery Benchmark Extraction](../artifacts/validation/nest2d_allostery_benchmark/nest2d_allostery_benchmark_report.md)
- [Nest 2D Allostery Label Bridge](../artifacts/validation/nest2d_allostery_label_bridge/nest2d_allostery_label_bridge_report.md)
- [Nest 2D Allostery Mapper Closeout Protocol](./NEST2D_ALLOSTERY_MAPPER_CLOSEOUT_PROTOCOL_2026-05-02.md)
- [Nest 2D Allostery Graph Mapper](../artifacts/validation/nest2d_allostery_graph_mapper/nest2d_allostery_graph_mapper_report.md)
- [Nest 2D-2 Allostery Pocket / Path Mapper](../artifacts/validation/nest2d_allostery_pocket_path_mapper/nest2d_allostery_pocket_path_mapper_report.md)
- [Nest 2D-3 Allostery Ligand-Contact Diagnostic](../artifacts/validation/nest2d_allostery_ligand_contact_diagnostic/nest2d_allostery_ligand_contact_diagnostic_report.md)
- [Nest 2D-4 Blind Pocket Split Mapper](../artifacts/validation/nest2d_allostery_blind_pocket_split_mapper/nest2d_allostery_blind_pocket_split_mapper_report.md)
- [Nest 2D-5 Ligand-Informed Split Mapper](../artifacts/validation/nest2d_allostery_ligand_informed_split_mapper/nest2d_allostery_ligand_informed_split_mapper_report.md)
- [Nest 2D-6 Allostery Recurrence / Path Mapper](../artifacts/validation/nest2d_allostery_recurrence_path_mapper/nest2d_allostery_recurrence_path_mapper_report.md)
- [Nest 2D-7A P2Rank External Pocket Coverage](../artifacts/validation/nest2d_p2rank_external_pocket_coverage/nest2d_p2rank_external_pocket_coverage_report.md)
- [Nest 2D-7B External-Pocket Merged Path Mapper](../artifacts/validation/nest2d_allostery_external_pocket_merged_path_mapper/nest2d_allostery_external_pocket_merged_path_mapper_report.md)
- [Nest 2E PFAS Pathway Validation](../artifacts/validation/nest2e_pfas_pathway/nest2e_pfas_pathway_report.md)
- [Nest 2E PFAS Safety Logic](../artifacts/validation/nest2e_pfas_safety_logic/nest2e_pfas_safety_logic_report.md)
- [Nest 2E PFAS Pathway Rerun](../artifacts/validation/nest2e_pfas_pathway_rerun02/nest2e_pfas_pathway_report.md)
- [Nest 2F Materials Stability Validation](../artifacts/validation/nest2f_materials_stability/nest2f_materials_stability_report.md)
- [Nest 2F Materials Stability Rerun](../artifacts/validation/nest2f_materials_stability_rerun02/nest2f_materials_stability_report.md)
- [Nest 2G RDKit Stronger Baseline Comparison](../artifacts/validation/nest2g_rdkit_baseline_comparison/nest2g_rdkit_baseline_comparison_report.md)

## Purpose

This pass continues the Nest 2 rule: each gate earns its status by touching a
real public dataset, a real measurement surface, or a real benchmark table.

## Gate Summary

| Gate | Dataset / Source | Status | Clean Read |
| --- | --- | --- | --- |
| `Nest 2D` allostery | AlloBench benchmark table, public AlloBench residue labels, RCSB PDB structures, local `P2Rank` pocket predictions | `external_merged_path_supported` | 98 benchmark rows join to real labels and contact graphs; 2D-2 pocket/path scoring beats graph controls; 2D-3 bound-ligand contacts confirm real pocket/contact geometry; 2D-4 sets the structural-only blind boundary; 2D-5 supports the ligand-informed application branch above the same-row AlloBench tool bar and controls; 2D-6 repeats the branch under an alternate split and separates active-site communication-path recovery; 2D-7A adds a real external P2Rank candidate branch; 2D-7B merges P2Rank with ligand-informed path candidates and stays supported above PASSer, graph controls, random candidates, and shuffled labels |
| `Nest 2E` PFAS pathways / safety | EPA PFAS reaction library `EnvLib + MetaLib` | `pfas_bad_descendant_safety_logic_supported` | true parent/product transformations beat shuffled parent/product controls, and coherent bad-descendant scoring separates retained PFAS burden from transformation alone |
| `Nest 2F` materials stability | Matbench / Materials Project `mp_e_form` | `supported` | composition/structure descriptors recover DFT formation energy above shuffled-target controls |
| `Nest 2G` stronger baselines | ESOL, Lipophilicity, FreeSolv, QM9 alpha | `supported` | multifeature RDKit train/test baselines strengthen the molecule-property lane |

## Nest 2D: Allostery

AlloBench was downloaded and parsed from the public supporting-information PDF.

Extracted result:

- `100` PDB benchmark rows
- `10` existing allosteric-site prediction tool columns
- best mean Jaccard tool in the extracted table: `PASSer_Ensemble`
- best mean Jaccard: `0.197330`

Clean read:

```text
real allostery benchmark surface found and extracted
```

Mapper scoring begins after the following inputs are attached:

- protein contact graph or pocket graph per PDB row
- known allosteric-site residue / pocket labels
- mapper score for candidate communication path
- controls against degree / centrality / shuffled-site labels

Label bridge result:

- real PDB benchmark rows: `100`
- allosteric-site prediction tool columns: `10`
- best mean Jaccard tool: `PASSer_Ensemble`
- best mean Jaccard: `0.19733`
- mean best-per-protein Jaccard: `0.38549`
- median best-per-protein Jaccard: `0.381`
- rows with any tool >= `0.2` Jaccard: `68`
- rows with any tool >= `0.5` Jaccard: `38`
- rows where all tools are zero / failed: `8`
- mean pairwise tool-score correlation: `0.235671399`

Clean bridge read:

```text
Nest 2D now has a real allostery benchmark surface, baseline difficulty
statistics, and a contact / pocket / residue-label manifest template for the
mapper scoring pass.
```

First graph mapper pass:

- public AlloBench source-label overlap: `98/100`
- RCSB PDB contact graphs scored: `98`
- Mirror mean Jaccard: `0.013452`
- best existing tool mean Jaccard: `0.197330` (`PASSer_Ensemble`)
- active-proximity control mean Jaccard: `0.031329`
- random-control p-value: `0.722555`

Clean graph read:

```text
Nest 2D now has real labels joined to real protein structures. The
contact-only residue mapper sets the first biological graph boundary, and the
next move is pocket/path scoring: chain-resolved active sites, pocket candidate
graphs, and active-site to allosteric-site communication-path recovery.
```

2D-2 pocket/path result:

- scored rows: `98`
- previous contact-only Mirror mean Jaccard: `0.013452`
- Mirror pocket/path mean Jaccard: `0.032975`
- degree pocket mean Jaccard: `0.010861`
- closeness pocket mean Jaccard: `0.018515`
- active-proximity pocket mean Jaccard: `0.014508`
- random-control p-value: `0.001996`
- label-shuffle p-value: `0.001996`
- strongest existing AlloBench tool mean Jaccard: `0.197330`

Clean 2D-2 read:

```text
Pocket/path scoring improves the biological object and beats graph pocket
controls, while the strongest tool bar remains the blind-prediction closeout
target.
```

2D-3 ligand-contact diagnostic:

- source rows in benchmark: `98`
- scored bound-ligand contact rows: `94`
- mean ligand-contact Jaccard: `0.263504`
- median ligand-contact Jaccard: `0.230952`
- rows >= `0.2` Jaccard: `56`
- rows >= `0.5` Jaccard: `12`

Clean 2D-3 read:

```text
Bound-ligand contact geometry confirms the AlloBench labels map onto real
pocket/contact structure and supplies a validated feature source for the next
blind allosteric mapper.
```

2D-4 blind pocket split result:

- scored rows: `98`
- folds: `5`
- random trials: `500`
- CV blind Mirror pocket/path mean Jaccard: `0.017703`
- previous 2D-2 pocket/path mean Jaccard: `0.032975`
- best existing tool mean Jaccard on scored rows: `0.201357`
- degree pocket mean Jaccard: `0.008222`
- closeness pocket mean Jaccard: `0.015044`
- active-proximity pocket mean Jaccard: `0.015651`
- random candidate mean Jaccard: `0.014310`
- random-control p-value: `0.251497`
- label-shuffle p-value: `0.061876`

Clean 2D-4 read:

```text
The held-out structural pocket/path mapper carries directional signal over
simple graph controls. The AlloBench tool bar and the 2D-2 same-surface score
set the next closeout targets, with external pocket candidates or stronger
ligand-informed features as the upgrade path.
```

Combined closeout design:

Use the same `100` PDB rows and compare the Mirror mapper against:

- the `10` existing AlloBench tools
- added pocket tools where available: `fpocket`, `P2Rank`, and `PrankWeb`
- graph-naive controls: degree, centrality, shortest active-site path, random
  pocket, and shuffled labels

The first move condition is beating the `PASSer_Ensemble` mean Jaccard
baseline of `0.19733` while also beating graph-naive controls. The stronger
move condition is repeating on a second seed / split or second allostery
benchmark family.

2D-5 ligand-informed split result:

- scored rows: `98`
- folds: `5`
- random trials: `500`
- CV ligand-informed Mirror mean Jaccard: `0.260713`
- 2D-4 structural-only blind mean Jaccard: `0.017703`
- best existing tool mean Jaccard on scored rows: `0.201357`
- ligand-contact baseline mean Jaccard: `0.260713`
- degree pocket mean Jaccard: `0.008222`
- closeness pocket mean Jaccard: `0.015044`
- active-proximity pocket mean Jaccard: `0.016029`
- random candidate mean Jaccard: `0.016261`
- random-control p-value: `0.001996`
- label-shuffle p-value: `0.001996`

Clean 2D-5 read:

```text
The better-input branch worked. In the ligand-bound application setting,
bound modulator geometry matches the direct ligand-contact candidate baseline
and beats the same-row AlloBench tool bar, graph controls, random controls,
and shuffled-label controls.
```

Immediate 2D-6 move:

- keep the same `98/100` scored AlloBench/PDB surface
- add external pocket candidates from `fpocket`, `P2Rank`, or `PrankWeb` where
  available
- compare pocket-tool candidates against the 2D-5 ligand-contact candidate
- score communication paths from active-site sources to candidate allosteric
  pockets as a separate metric
- compare against `PASSer_Ensemble`, pocket-tool baselines, graph controls,
  random pockets, and shuffled labels

2D-6 recurrence / path result:

- scored rows: `98`
- folds: `5`
- random trials: `500`
- external pocket tools available locally: `fpocket=false`, `p2rank=false`,
  `prankweb=false`
- alternate-split pocket mean Jaccard: `0.249009`
- previous 2D-5 pocket mean Jaccard: `0.260713`
- best existing AlloBench tool mean Jaccard on scored rows: `0.201357`
- ligand-contact baseline mean Jaccard: `0.260713`
- degree pocket mean Jaccard: `0.008222`
- closeness pocket mean Jaccard: `0.015044`
- active-proximity pocket mean Jaccard: `0.016029`
- random pocket mean Jaccard: `0.015148`
- pocket random / shuffled p-values: `0.001996` / `0.001996`
- Mirror path-truth Jaccard: `0.211530`
- Mirror path-truth recall: `0.345859`
- degree / closeness / active-proximity path-truth recall:
  `0.034344` / `0.051651` / `0.034921`
- random path-truth recall: `0.054600`
- path random / shuffled p-values: `0.001996` / `0.001996`

Clean 2D-6 read:

```text
The ligand-informed allostery branch recurs under a second held-out split, and
the active-site to predicted-pocket communication corridor carries allosteric
label structure above graph, random, and shuffled-label controls.
```

2D-7A P2Rank external pocket-tool result:

- P2Rank version: `2.5.1`
- P2Rank prediction files: `98`
- scored rows after residue-label matching: `95`
- top-1 P2Rank pocket Jaccard: `0.096418`
- top-3 P2Rank candidate envelope Jaccard: `0.189177`
- 2D-6 Mirror pocket Jaccard: `0.249009`
- same-row `PASSer_Ensemble` Jaccard: `0.201863`
- random pocket Jaccard: `0.016878`
- top-1 random / shuffled p-values: `0.000200` / `0.000200`

Clean 2D-7A read:

```text
P2Rank is now a real external pocket-candidate source on the AlloBench slice.
Its top-1 emitted pockets recover known allosteric labels above random and
shuffled controls. The top-3 envelope rises close to the PASSer bar, which
makes merged ranking and path scoring the next useful allostery upgrade.
```

2D-7B external-pocket merged path result:

- scored rows: `98`
- folds: `5`
- random trials: `500`
- P2Rank rows with candidates: `95`
- selected source counts: `ligand_mirror=98`
- merged pocket Jaccard: `0.255807`
- previous 2D-6 Mirror pocket Jaccard: `0.249009`
- P2Rank top-1 Jaccard: `0.096418`
- P2Rank top-3 envelope Jaccard: `0.189177`
- same-row `PASSer_Ensemble` Jaccard: `0.201357`
- random merged-candidate Jaccard: `0.015506`
- pocket random / shuffled p-values: `0.001996` / `0.001996`
- merged path-truth recall: `0.351995`
- random path-truth recall: `0.056557`
- path random / shuffled p-values: `0.001996` / `0.001996`

Clean 2D-7B read:

```text
The merged external-pocket / ligand-informed branch is supported above PASSer,
graph controls, random candidates, and shuffled labels. P2Rank is now a real
external candidate source, but the held-out selector still chooses the
ligand-informed Mirror/path branch on all rows, so direct P2Rank dominance is
not claimed.
```

Next allostery expansion:

- source a second allostery benchmark family or optimize external-tool ranking
- keep P2Rank candidate pockets merged with the ligand-informed branch under
  held-out ranking
- keep pocket overlap and communication-path recovery as separate outputs

## Nest 2E: PFAS Pathway Validation

The EPA PFAS reaction library gives real parent / product `SMILES` pairs.

Validation question:

```text
are real PFAS transformation pairs more chemically coherent than random
parent/product pairings from the same library?
```

Result:

- valid parent/product pairs: `184`
- reaction-type classes: `13`
- true mean pathway coherence: `0.624682`
- shuffled mean pathway coherence: `0.291178`
- permutation p: `0.000200`
- repeat seed p: `0.000200`

Important boundary read:

- rows with any fluorine or C-F bond reduction: `0.3370`
- rows retaining high fluorination / C-F burden: `0.8424`

This means the pathway-coherence comparator is supported, while PFAS
mineralization / safe byproduct generation remains its own scoring pass.

2E safety-logic result:

- scored rows: `184`
- mean coherent bad-descendant score: `0.595067`
- shuffled coherent bad-descendant score: `0.554863`
- coherent bad-descendant p-value: `0.000200`
- bad-descendant flag fraction: `0.733696`
- shuffled bad-descendant flag fraction: `0.532891`
- bad-descendant flag p-value: `0.000200`
- high retained-burden fraction: `0.842391`
- low mineralization-quality fraction: `0.842391`
- rows with any F or C-F reduction: `0.336957`
- safety-candidate fraction: `0.038043`

Clean 2E safety read:

```text
True PFAS pathways are coherent, but the safety layer shows most coherent
descendants still retain fluorination / C-F burden. The lane now separates
pathway transformation from safer degradation.
```

## Nest 2F: Materials / Crystal Stability

The Matbench `mp_e_form` dataset was downloaded from the public Hugging Face
mirror of Materials Project-derived formation-energy rows.

Validation question:

```text
do fixed composition / structure descriptors recover DFT formation energy above
shuffled-target controls?
```

Result:

- rows used after cleaning: `50,000`
- test Pearson: `0.568810`
- repeat test Pearson: `0.568895`
- seed-69 refresh Pearson: `0.567628`
- Pearson permutation p: `0.000999`
- repeat Pearson permutation p: `0.000999`
- seed-69 Pearson permutation p: `0.000999`
- RMSE-improvement permutation p: `0.000999`

Boundary:

This validates a real materials-property descriptor lane. Crystal design,
synthesis, and broad materials prediction remain separate scoring passes.

## Nest 2G: Stronger Descriptor / Baseline Comparison

This pass checks whether the molecule-property lane survives a stronger
comparison than the original single descriptor composite.

| Dataset | Rows | Original composite abs r | Multifeature train/test abs r | p |
| --- | ---: | ---: | ---: | ---: |
| `ESOL` | `1128` | `0.558660` | `0.896224` | `0.000999` |
| `Lipophilicity` | `4200` | `0.204180` | `0.524267` | `0.000999` |
| `FreeSolv` | `642` | `0.395067` | `0.883146` | `0.000999` |
| `QM9 alpha` | `50000` | `0.083271` | `0.911784` | `0.000999` |

Seed-68 refresh:

| Dataset | Rows | Composite abs r | Multifeature train/test abs r | RMSE improvement | p |
| --- | ---: | ---: | ---: | ---: | ---: |
| `ESOL` | `1128` | `0.558660` | `0.893422` | `0.555455` | `0.000999` |
| `Lipophilicity` | `4200` | `0.204180` | `0.527449` | `0.148655` | `0.000999` |
| `FreeSolv` | `642` | `0.395067` | `0.943685` | `0.657915` | `0.000999` |
| `QM9 alpha` | `50000` | `0.090075` | `0.916655` | `0.600308` | `0.000999` |

Clean read:

```text
the molecule-property signal survives stronger descriptor baselines and
held-out prediction controls
```

## Overall Read

`Nest 2` has moved beyond a structured-matter validation map into executed
real-data gates.

It now has:

- repeated real molecule-property support
- stronger RDKit descriptor / baseline support
- real PFAS pathway-coherence support
- real PFAS bad-descendant / safety-triage support
- real materials-stability support
- repeated seed-69 materials-stability support
- a real allostery benchmark surface with source residue labels joined to
  `98` PDB contact graphs; pocket/path scoring improves and beats graph
  controls; ligand-contact geometry confirms a real pocket/contact feature
  source; recurrence and communication-path scoring are supported; and P2Rank
  is now a real external pocket-candidate source merged into the supported
  allostery branch

The claim remains bounded:

```text
the Source Mirror / Mirror Architecture comparator spine can be grounded in
real structured-matter datasets across multiple lanes
```

Chemistry, biology, materials design, and PFAS remediation each require their
own completed dataset-specific scoring lanes.
