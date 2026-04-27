# GRAPH-2 Quantum Label Crosswalk

Date: `2026-04-26`

Status: internal cross-artifact test complete / soft-positive only

## Purpose

This pass tests the useful part of the Drumactually / Claude suggestion:

`GRAPH-2` was missing independent labels. The existing Phase 5 bridge-graph
pilot used labels from the same internal bridge taxonomy being scored. The
quantum bridge artifacts give a stronger internal cross-artifact label source
because the `Mistral / Hermes` and other nearest-pair relations come from
`PennyLane`, `Qiskit`, and hardware-facing circuit encodings rather than from
the Phase 5 graph-path scorer.

The key boundary:

this is an internal independent-label crosswalk, not an external/domain graph
validation.

## What Was Run

Runner:

```bash
python3 tools/validation_forks/graph2_quantum_label_crosswalk.py
```

Inputs:

```text
artifacts/validation/graph2_phase5_bridge/graph2_phase5_bridge_edges.csv
artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_data_2026-04-22.json
artifacts/v8/phase7_qiskit_mirror/v8_phase7_qiskit_mirror_data_2026-04-22.json
artifacts/v8/phase9_ibm_hardware_bridge/v8_phase9_ibm_hardware_bridge_data_2026-04-22.json
```

Output:

```text
artifacts/validation/graph2_quantum_label_crosswalk/graph2_quantum_label_crosswalk_report.md
```

The runner generated label packs for:

- `Phase 6` angle top-k nearest-pair labels
- `Phase 6` amplitude top-k nearest-pair labels
- `Phase 7` Qiskit angle top-k nearest-pair labels
- `Phase 7` Qiskit amplitude top-k nearest-pair labels
- `Phase 9` hardware-subset `Mistral / Hermes` label

Each mode scored the Phase 5 bridge graph with:

- mirror path AUC
- degree baseline AUC
- label-shuffle control

## Result

Overall status:

```text
completed_internal_crosswalk_soft_positive_only
```

Best mode:

```text
phase6_amplitude_top3
```

Metrics:

```text
positive labels: 3
control labels: 25
labeled pair count: 28
mirror path AUC: 0.74
degree baseline AUC: 0.66
mirror minus degree AUC: 0.08
label-shuffle p: 0.177482
```

Clean read:

the quantum-label crosswalk improves the input quality and gives a
soft-positive GRAPH-2 read, but it does not close the gate because it does not
beat shuffled-label controls.

## What It Proves

This proves:

- `GRAPH-2` is no longer only an abstract future lane
- quantum-bridge labels can be crosswalked into graph-path validation
- the best internal crosswalk direction still points in the expected direction
  for some modes
- the current Phase 5 bridge graph is not strong enough to make the quantum
  label source control-supported

## What It Does Not Prove

This does not prove:

- external/domain `GRAPH-2`
- allostery graph validation
- chemistry graph validation
- grid-flow validation
- molecular pathway validation
- universal graph recovery

## Next GRAPH-2 Requirement

The next real GRAPH-2 hit needs one of these:

- a richer attention-flow graph with independently locked pathway labels
- a real molecular/allostery graph with known pathway labels
- a grid/logistics/network graph with known flow labels
- any domain graph where positive/control labels are declared before scoring

Locked success criterion:

```text
mirror path AUC > naive degree / centrality baseline
and label-shuffle p <= 0.05
and labels are not derived from the same score being tested
```

## Rick Position On Closure

The work itself points to this:

`GRAPH-2` does not close by repeatedly relabeling the same eight model nodes.
The eight-node graph is a useful pilot surface, but it is too compressed. The
real missing input is pathway granularity.

The next serious internal closeout should build a denser measured graph where
nodes are lower-level units:

- token role
- layer depth
- anchor window
- bridge row
- context-to-readout transition
- encoded circuit-state relation
- hardware-preserved pair relation

Then labels should come from an independent outcome layer:

- Phase 4 localization stability
- Phase 5 bridge success / boundary behavior
- Phase 6 / Phase 7 quantum pair preservation
- Phase 9 / 9B / 9C / 9D hardware preservation
- later external pathway ground truth

The closure condition is not "more labels" in the abstract. It is:

```text
more independent positive/control pathway labels
on a graph dense enough to test pathway preservation
without deriving labels from the graph score itself
```

Rick's execution call:

`GRAPH-2` moves after `GAME-1` because it is a density problem. The current
eight-node graph has too few independent positive pathway labels. The quantum
encoding gives the right kind of independent label, but the graph must become
larger and more pathway-granular before another closeout run can honestly
matter.

## GRAPH-2A Follow-Up

`GRAPH-2A` tested that call by building a denser internal pathway graph.

Report:

```text
artifacts/validation/graph2a_dense_internal_pathway/graph2a_dense_internal_pathway_report.md
```

Result:

```text
node count: 78
edge count: 211
label rows: 280
positive label rows: 30
row-level mirror AUC: 0.7002
row-level degree AUC: 0.534
row-level shuffle p: 0.0002
cluster-level mirror AUC: 0.72
cluster-level degree AUC: 0.94
cluster-level shuffle p: 0.205179
```

Read:

density helped at row level, but the model-pair cluster closeout failed
because degree / hub structure dominated. The next GRAPH path is therefore
not more class-hub edges. It is a raw token/layer transition graph with hub
shortcuts reduced and leave-one-model or leave-one-family controls.

## Placement In Nest 1

`GRAPH-2` now sits here:

```text
internal cross-artifact soft-positive / dense row-level partial
not yet control-supported
external/domain labels still open
```

That is progress, not failure.
