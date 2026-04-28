# GRAPH-2B Raw Token / Layer Pathway Preregistration

Date: 2026-04-27

## Purpose

`GRAPH-2B` is the next internal GRAPH-2 gate after `GRAPH-2A`.

`GRAPH-2A` showed real row-level signal, but the cluster-level control failed
because degree / hub structure dominated. `GRAPH-2B` therefore changes the
graph source and graph construction:

- graph source: real V8 raw hidden-state point-cloud exports
- node type: token / layer state rows, not Phase 5 summary hub nodes
- edge type: local layer transitions, local token transitions, and capped
  cross-model nearest-neighbor links
- label source: independently measured Phase 6 quantum encoding nearest pairs

This is still an internal Mirror-stack graph validation. It is not external
molecular, allostery, grid, logistics, attention-flow, or chemistry validation.

## Frozen Inputs

- Point-cloud source:
  `artifacts/v8/residual_stream_bridge/point_clouds_expanded/`
- Label source:
  `artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_data_2026-04-22.json`
- Primary positive label:
  Phase 6 amplitude top-3 nearest encoded pairs.

The positive model pairs are:

- `Mistral|Hermes`
- `GLM|Mistral`
- `GLM|Hermes`

Those labels come from the independent quantum-encoding artifact, not from the
raw token/layer graph score.

## Frozen Graph Construction

`GRAPH-2B` builds a public-safe graph from derived features only. It does not
publish raw hidden vectors.

Nodes are real point-cloud rows filtered to:

- `context_label in {lattice, neutral, technical}`
- token-window rows within the anchor neighborhood
- compact summary rows for `last_token` and `target_span_mean`

Edges are:

- layer-transition edges within the same model/context/token role/token offset
- token-transition edges within the same model/context/layer
- capped cross-model nearest-neighbor links within the same context, layer
  depth, token region, token role, token offset, and depth slot

The cross-model edge cap is intended to reduce hub shortcuts rather than make a
fully dense similarity graph.

## Frozen Scoring Rule

For each model pair and shared token/layer signature:

- compute the shortest graph path between the matched model-side node groups
- score as `1 / (1 + path_length)`
- score as `0` if no path exists
- compare against a degree baseline using the same matched node groups

The primary closeout is cluster-level, because row-level signatures are not
independent.

## Controls

The runner reports:

- row-level metrics
- model-pair cluster metrics
- exact shuffled-label control over model-pair labels
- layer-order shuffle control
- token-window shuffle control
- degree baseline

## Closeout Rule

`GRAPH-2B` is control-supported only if:

- cluster-level mirror/path AUC is greater than the degree baseline AUC
- exact shuffled-label `p <= 0.05`
- mirror/path AUC remains better than the degree baseline under the raw graph,
  not only under row-level expansion

If row-level succeeds but cluster-level fails, the lane remains soft-positive
and open.

## Next Forks

If `GRAPH-2B` is not control-supported, the next real GRAPH-2 inputs are:

- real attention-flow labels, if available from exported attention maps
- Nest 2 molecular / allostery graph labels
- grid-flow graph labels
- logistics / network path labels

Those are external/domain validation forks, not substitutes for this internal
raw token/layer graph gate.
