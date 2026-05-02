# Nest 2D Allostery Mapper Closeout Protocol

Date: `2026-05-02`

Status: `closeout_protocol_locked_after_label_bridge`

Companion inputs:

- [Nest 2D Allostery Benchmark Extraction](../artifacts/validation/nest2d_allostery_benchmark/nest2d_allostery_benchmark_report.md)
- [Nest 2D Allostery Label Bridge](../artifacts/validation/nest2d_allostery_label_bridge/nest2d_allostery_label_bridge_report.md)
- [Nest 2D Allostery Label Manifest Template](../artifacts/validation/nest2d_allostery_label_bridge/nest2d_allostery_label_manifest_template.csv)

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

## Immediate Next Build

Build `nest2d_allostery_graph_mapper.py` with these stages:

- `download_structures`: pull PDB/mmCIF files for the manifest PDB IDs
- `build_contact_graphs`: residue nodes, spatial-contact edges
- `build_pocket_graphs`: pocket / residue-cluster nodes and proximity edges
- `attach_labels`: allosteric-site and active-site labels
- `run_baselines`: degree, centrality, shortest path, random pocket, shuffled labels
- `run_mapper`: candidate Mirror mapper path / pocket score
- `score`: Jaccard, communication-path recovery, permutation controls
- `report`: table against AlloBench tools, added pocket tools, and controls

