# Nest 2D Allostery Mapper Closeout Protocol

Date: `2026-05-02`

Status: `blind_pocket_split_boundary_set`

Companion inputs:

- [Nest 2D Allostery Benchmark Extraction](../artifacts/validation/nest2d_allostery_benchmark/nest2d_allostery_benchmark_report.md)
- [Nest 2D Allostery Label Bridge](../artifacts/validation/nest2d_allostery_label_bridge/nest2d_allostery_label_bridge_report.md)
- [Nest 2D Allostery Label Manifest Template](../artifacts/validation/nest2d_allostery_label_bridge/nest2d_allostery_label_manifest_template.csv)
- [Nest 2D Allostery Graph Mapper Report](../artifacts/validation/nest2d_allostery_graph_mapper/nest2d_allostery_graph_mapper_report.md)
- [Nest 2D-2 Allostery Pocket / Path Mapper Report](../artifacts/validation/nest2d_allostery_pocket_path_mapper/nest2d_allostery_pocket_path_mapper_report.md)
- [Nest 2D-3 Allostery Ligand-Contact Diagnostic](../artifacts/validation/nest2d_allostery_ligand_contact_diagnostic/nest2d_allostery_ligand_contact_diagnostic_report.md)
- [Nest 2D-4 Blind Pocket Split Mapper](../artifacts/validation/nest2d_allostery_blind_pocket_split_mapper/nest2d_allostery_blind_pocket_split_mapper_report.md)
- [Nest 2D-5 Ligand-Informed Split Mapper](../artifacts/validation/nest2d_allostery_ligand_informed_split_mapper/nest2d_allostery_ligand_informed_split_mapper_report.md)

## Purpose

This protocol combines the Nest 2D next steps into one allostery closeout run.
The current Nest 2D result gives the benchmark surface: `100` real AlloBench
PDB rows, `10` existing allosteric-site prediction tool columns, and baseline
difficulty statistics. The closeout run turns those same rows into graph-scored
biological objects and compares the Mirror mapper against tool baselines and
graph-naive controls.

## Current Benchmark Read

- real PDB rows: `100`
- existing AlloBench tool columns: `10`
- best mean Jaccard tool: `PASSer_Ensemble`
- best mean Jaccard: `0.19733`
- mean best-per-protein Jaccard: `0.38549`
- median best-per-protein Jaccard: `0.381`
- rows with any tool >= `0.2` Jaccard: `68`
- rows with any tool >= `0.5` Jaccard: `38`
- rows where all tools are zero / failed: `8`
- mean pairwise tool-score correlation: `0.235671399`

Interpretation:

`0.19733` mean Jaccard is a low but useful baseline. It means the allostery
lane is difficult enough that a mapper beating the strongest table-level tool
and graph-naive controls would be meaningful.

## Combined Closeout Run

Use the same `100` PDB rows and compare:

| Comparator | Role |
| --- | --- |
| Mirror mapper | candidate architecture-path / pocket scoring lane |
| `APOP` | existing allostery tool baseline |
| `PASSer_Rank` | existing allostery tool baseline |
| `PASSer_AutoML` | existing allostery tool baseline |
| `PASSer_Ensemble` | strongest current mean-Jaccard baseline |
| `Ohm` | existing allostery tool baseline |
| `ALLO` | existing allostery tool baseline |
| `AllositePro` | existing allostery tool baseline |
| `STRESS` | existing allostery tool baseline |
| `AlloPred` | existing allostery tool baseline |
| `Allosite` | existing allostery tool baseline |
| `fpocket` | added pocket candidate baseline |
| `P2Rank` | added pocket candidate baseline |
| `PrankWeb` | added pocket candidate baseline |
| degree centrality | graph-naive control |
| betweenness / closeness centrality | graph-naive control |
| shortest active-site path | graph-naive communication-path control |
| random pocket | random structural control |
| shuffled allosteric labels | label-shuffle control |

## First Graph Mapper Execution

The first implementation pass is now complete:

- official AlloBench source CSV joined to the benchmark rows
- source label overlap: `98/100` PDB rows
- RCSB structures resolved into residue-contact graphs: `98`
- scored rows: `98`
- contact cutoff: `8.0 A`
- random trials: `500`

Result:

| Metric | Value |
| --- | ---: |
| Mirror mean Jaccard | `0.013452` |
| Best existing AlloBench tool mean Jaccard | `0.197330` |
| Best existing tool | `PASSer_Ensemble` |
| Degree mean Jaccard | `0.006597` |
| Closeness mean Jaccard | `0.017282` |
| Active-proximity mean Jaccard | `0.031329` |
| Random mean Jaccard | `0.014990` |
| Random-control p-value | `0.722555` |

Clean read:

```text
The first contact-only residue graph mapper sets the low baseline for Nest 2D.
It validates the data bridge and the execution mechanics, while exact residue
top-k contact scoring stays below the strongest AlloBench tool baseline and
below the active-proximity graph control.
```

What moved:

- allosteric labels are now attached from the public AlloBench source
- active-site labels are attached
- real PDB structures are cached locally for execution
- residue-contact graphs exist for the scored rows
- graph controls and random / shuffled controls run on the same objects

Remaining gate:

- mapper support moves through pocket/path scoring rather than contact-only
  residue scoring
- allostery is better represented through pocket-level and communication-path
  scoring than through exact residue recovery from plain contact graphs

## 2D-2 Pocket / Path Upgrade

The Waka strategy upgrade is now complete on the same `98` scored structures:

- chain-resolved active-site sources
- geometric pocket candidates from residue-contact neighborhoods
- active-site-to-pocket path / bottleneck score
- graph pocket controls: degree, closeness, active proximity, random pockets,
  and shuffled labels

Result:

| Metric | Value |
| --- | ---: |
| Mirror pocket/path mean Jaccard | `0.032975` |
| Previous contact-only Mirror mean Jaccard | `0.013452` |
| Degree pocket mean Jaccard | `0.010861` |
| Closeness pocket mean Jaccard | `0.018515` |
| Active-proximity pocket mean Jaccard | `0.014508` |
| Random pocket mean Jaccard | `0.012007` |
| Random-control p-value | `0.001996` |
| Label-shuffle p-value | `0.001996` |
| Best existing AlloBench tool mean Jaccard | `0.197330` |

Clean read:

```text
Pocket/path scoring improves the biological representation and beats graph
pocket controls. The strongest existing AlloBench tool remains the higher
blind-prediction closeout bar.
```

## 2D-3 Ligand-Contact Diagnostic

The next feature-source diagnostic used bound ligand/contact geometry already
present in the PDB files while the external pocket-tool lane remains queued.

Result:

| Metric | Value |
| --- | ---: |
| Scored source rows | `94` |
| Mean ligand-contact Jaccard | `0.263504` |
| Median ligand-contact Jaccard | `0.230952` |
| Rows >= `0.2` Jaccard | `56` |
| Rows >= `0.5` Jaccard | `12` |
| Best existing AlloBench tool mean Jaccard | `0.197330` |

Clean read:

```text
Bound-ligand contact geometry confirms the AlloBench labels map onto real
pocket/contact structure and supplies a strong feature source for the next
blind allosteric mapper.
```

## 2D-4 Blind Pocket Split Mapper

The blind split pass tested the pocket/path idea under held-out evaluation.
It trained structural feature weights on `5` folds and evaluated held-out PDB
rows using structural pocket/path features only:

- geometric pocket candidates
- chain-resolved active-site sources
- active-site-to-pocket distance and communication-path features
- degree, closeness, active-proximity, random, and label-shuffle controls

Result:

| Metric | Value |
| --- | ---: |
| CV blind Mirror pocket/path mean Jaccard | `0.017703` |
| 2D-2 untuned pocket/path mean Jaccard | `0.032975` |
| Best existing AlloBench tool mean Jaccard on scored rows | `0.201357` |
| Degree pocket mean Jaccard | `0.008222` |
| Closeness pocket mean Jaccard | `0.015044` |
| Active-proximity pocket mean Jaccard | `0.015651` |
| Random candidate mean Jaccard | `0.014310` |
| Random-control p-value | `0.251497` |
| Label-shuffle p-value | `0.061876` |

Clean read:

```text
2D-4 sets the blind-CV boundary. Structural pocket/path features carry
directional signal over simple graph controls, while held-out allostery
recovery points the closeout path toward stronger pocket candidates or
ligand-informed features.
```

## 2D-5 Ligand-Informed Split Mapper

The 2D-5 pass ran the better-input branch in the ligand-bound application
setting. It kept the 2D-4 held-out fold discipline and added bound modulator
geometry as an input surface:

- ligand-contact pocket candidate from PDB `HETATM` geometry
- ligand proximity and contact-fraction features
- same `98` AlloBench/PDB rows
- same `5` held-out folds
- same graph, random, shuffled-label, and same-row tool comparisons

Result:

| Metric | Value |
| --- | ---: |
| CV ligand-informed Mirror mean Jaccard | `0.260713` |
| 2D-4 structural-only blind mean Jaccard | `0.017703` |
| Best existing AlloBench tool mean Jaccard on scored rows | `0.201357` |
| Ligand-contact baseline mean Jaccard | `0.260713` |
| Degree pocket mean Jaccard | `0.008222` |
| Closeness pocket mean Jaccard | `0.015044` |
| Active-proximity pocket mean Jaccard | `0.016029` |
| Random candidate mean Jaccard | `0.016261` |
| Random-control p-value | `0.001996` |
| Label-shuffle p-value | `0.001996` |

Clean read:

```text
2D-5 supports the ligand-informed application branch. Bound modulator geometry
matches the direct ligand-contact candidate baseline and beats the same-row
AlloBench tool bar, graph controls, random controls, and shuffled-label
controls.
```

## Execution Sequence

1. Pull the `100` PDB structures listed in the AlloBench table.
2. Normalize structures into chain / residue / coordinate tables.
3. Build residue contact graphs from 3D coordinates.
4. Build pocket graphs from pocket / residue clusters.
5. Attach known allosteric-site residue or pocket labels from AlloBench / ASD.
6. Attach active-site residue labels from UniProt / M-CSA / AlloBench pipeline data.
7. Run added pocket tools on the same structures where local execution is available.
8. Run the Mirror mapper on the same graph units.
9. Score known allosteric-site recovery with Jaccard.
10. Score active-site to allosteric-site communication-path recovery.
11. Compare against the `10` AlloBench tool baselines.
12. Compare against added pocket tools and graph-naive controls.
13. Repeat with a second seed / split or a second allostery benchmark family.

## Required Data Columns

The label manifest should resolve these fields per PDB row:

| Column | Meaning |
| --- | --- |
| `pdb_id` | AlloBench protein row identifier |
| `protein_structure_uri` | local PDB/mmCIF structure path or source URI |
| `contact_graph_uri` | residue contact graph path |
| `pocket_graph_uri` | pocket / residue-cluster graph path |
| `known_allosteric_residue_labels_uri` | ground-truth allosteric-site residues or pocket labels |
| `known_active_site_residue_labels_uri` | active-site labels for communication-path direction |
| `candidate_mapper_score_uri` | Mirror mapper score output on the same graph units |
| `label_source` | source for labels, such as AlloBench / ASD / PDB / UniProt / M-CSA |
| `evidence_uri` | provenance record for the row |
| `ready_for_mapper_scoring` | boolean readiness flag |

## Scoring Targets

Primary target:

```text
known allosteric-site recovery
```

Score:

```text
Jaccard(predicted allosteric residues or pocket, known allosteric residues or pocket)
```

Secondary target:

```text
active-site -> allosteric-site communication path recovery
```

Score:

```text
path overlap / endpoint recovery / bottleneck recovery against known allosteric communication labels
```

## What Would Move Nest 2D

Nest 2D moves from `benchmark_ready` to `mapper_supported` if the Mirror mapper:

- beats the `PASSer_Ensemble` mean Jaccard baseline of `0.19733`
- beats graph-naive controls: degree, centrality, shortest path, random pocket,
  and shuffled labels
- repeats on a second seed / split or second allostery benchmark family

The stronger closeout is:

```text
Mirror mapper > best AlloBench tool baseline
and
Mirror mapper > graph-naive controls
and
repeat holds on second split / benchmark
```

## Immediate 2D-6 Upgrade

The next run keeps the same benchmark surface and broadens the better-input
branch beyond bound-ligand contact geometry:

- add real pocket-tool candidates where available: `fpocket`, `P2Rank`, or
  `PrankWeb`
- compare pocket-tool candidates against the 2D-5 ligand-contact candidate
- score active-site to allosteric-site communication paths and bottlenecks as
  separate metrics
- compare pocket/path recovery against `PASSer_Ensemble`, graph controls,
  random pockets, and shuffled labels
- repeat on a second split or second allostery set after the same-100-PDB
  ligand-informed run
