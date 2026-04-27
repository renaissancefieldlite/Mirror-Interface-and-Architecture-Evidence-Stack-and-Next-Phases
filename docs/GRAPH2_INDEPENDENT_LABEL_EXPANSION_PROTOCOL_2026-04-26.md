# GRAPH-2 Independent Label Expansion Protocol

Date: `2026-04-26`

Status: expansion gate / no validation claim until independent labels exist

## Purpose

`GRAPH-2` tests whether the Mirror graph score recovers known pathways or
flows better than simple graph baselines.

The Phase 5 bridge-graph pilot is real progress:

- mirror path AUC: `0.74`
- degree baseline AUC: `0.6467`
- label-shuffle p: `0.166683`

That is a soft positive, not a closed win. The pilot labels are too small and
too internal to carry the full `GRAPH-2` claim.

## What Has To Change

The next `GRAPH-2` hit needs labels that are independent from the score being
tested.

Good label surfaces:

- attention-flow labels from real model traces
- allostery / protein communication paths
- molecular pathway labels
- grid-flow labels
- logistics or network-flow labels

Bad label surfaces:

- labels derived from the same mirror path score
- labels chosen after seeing the output
- labels without a declared source
- labels with only positives and no controls

## Required Files

The gate expects:

```text
edge CSV:
source,target,edge_weight,edge_type,edge_source,evidence_uri

label CSV:
source,target,label,label_class,label_source,label_method,evidence_uri,label_lock_date,notes
```

Minimum usable input:

- at least `10` positive pathway labels
- at least `10` control pathway labels
- every label row has `label_source`
- every label row has `evidence_uri`
- `label_method` is locked before scoring

## Expansion Gate

Run with no input to write templates and a blocked report:

```bash
python3 tools/validation_forks/graph2_independent_label_gate.py
```

Run with real inputs to audit whether the label pack is eligible:

```bash
python3 tools/validation_forks/graph2_independent_label_gate.py \
  --edge-csv path/to/edges.csv \
  --label-csv path/to/labels.csv
```

If the gate passes, run the existing pathway validator:

```bash
python3 tools/validation_forks/graph12_pathway_validation.py \
  --edge-csv path/to/edges.csv \
  --label-csv path/to/labels.csv \
  --out-dir artifacts/validation/graph2_domain_pathway
```

## Success Criterion

`GRAPH-2` becomes control-supported only if:

```text
mirror path AUC > naive degree / centrality baseline
and label-shuffle p <= 0.05
and labels are independently sourced before scoring
```

## Current Read

`GRAPH-2` is not failed.

It is a real internal pilot with a clear external-label path.

The next move is not more grammar. The next move is a real graph domain with
locked positive/control pathway labels.

## Boundary

This protocol validates graph pathway recovery only.

It does not validate chemistry, biology, allostery, grid planning, or any other
domain until the labels come from that domain.
