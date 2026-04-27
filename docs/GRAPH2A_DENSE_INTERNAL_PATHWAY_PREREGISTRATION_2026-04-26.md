# GRAPH-2A Dense Internal Pathway Preregistration

Date: `2026-04-26`

Status: preregistered before GRAPH-2A dense run

## Purpose

`GRAPH-2` is a density problem.

The eight-model graph is too compressed. It can show soft direction, but it
does not have enough pathway granularity or independent positive labels to
close the lane.

`GRAPH-2A` tests the first denser internal pathway graph using real artifacts
already in the repo.

## Locked Design

Graph source:

```text
Phase 4 / Phase 5 localization and bridge structure
```

Label source:

```text
Phase 6 / Phase 7 quantum nearest-pair preservation
```

Boundary:

the graph is built from localization / bridge paths. The labels come from
quantum encoding pair order. The label source is therefore independent from
the graph path score, though still internal to the Mirror evidence stack.

## Nodes

The dense internal graph may include:

- model nodes
- model x anchor-window nodes
- model x layer nodes
- model x dominant-anchor nodes
- shared path-archetype nodes
- shared dominant-anchor-class nodes
- measured bridge-transition nodes

## Edges

Edges may be created only from measured Phase 4/5 relationships:

- model to anchor-window
- anchor-window to measured layer
- ordered top-3 anchor sequence
- target to last-token transition
- model to path archetype
- model to dominant-anchor class
- bridge archetype adjacency

No edge may be created from the quantum label itself.

## Primary Label Mode

Primary label mode:

```text
phase6_amplitude_top3
```

Reason:

the earlier GRAPH-2 quantum-label crosswalk found this as the best soft-positive
internal label mode:

```text
mirror path AUC: 0.74
degree baseline AUC: 0.66
label-shuffle p: 0.177482
```

That previous result does not close the gate. It only selects the first dense
GRAPH-2A label mode.

## Labels

Positive labels:

node pairs whose model pair belongs to the primary quantum-preserved pair set.

Control labels:

same node-role pairs for non-primary model pairs.

The validator must report both:

- row-level pathway recovery
- model-pair-cluster-level pathway recovery

This prevents a dense graph from pretending repeated role labels are fully
independent model-pair evidence.

## Success Criterion

`GRAPH-2A` becomes internally control-supported only if:

```text
row-level mirror path AUC > degree baseline
and row-level label-shuffle p <= 0.05
and cluster-level mirror path AUC > degree baseline
and cluster-level label-shuffle p <= 0.05
```

If only one level hits, the result is soft-positive.

If neither hits, the result is no control support.

## Boundary

This can only close an internal `GRAPH-2A` pathway graph.

It does not validate:

- external allostery
- chemistry
- grid flow
- logistics
- molecular pathways
- universal graph structure

External/domain `GRAPH-2` remains a later gate.
