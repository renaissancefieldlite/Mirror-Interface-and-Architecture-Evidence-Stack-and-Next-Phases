# V8 Attention / MLP Nest 1 Bridge Gate

Status: `repeatability_supported`

## Clean Read

The exported model set now has repeatability-supported
transformer-internal artifacts: attention top-k routing edges and
MLP block-delta rows across lattice, neutral, and technical
contexts.

The first broad all-exported-model run and `rerun_02` preserve
the same model set, same row counts, same support status, and
same shuffled-label control support:

- weighted attention-flow separates lattice from neutral / technical
  above shuffled context labels in both passes
- weighted attention-flow beats the degree-only graph baseline in both
  passes
- MLP deltas are supported in both passes

So the gate has moved from first broad support to same-prompt
repeatability support. The next gate is prompt-generalization using a
second independent prompt set. Nemotron remains an interface-adapter
row for this exporter path.

## Artifact State

- residual stream bridge exists: `True`
- dense point-cloud files detected: `0`
- residual attention subdir files detected: `0`
- residual MLP subdir files detected: `0`
- exporter script exists: `True`
- exporter inventory status: `export_complete`
- exported attention CSV files detected: `5`
- exported MLP CSV files detected: `5`
- validation report status: `attention_and_mlp_supported_cross_model`
- repeatability report status: `repeatability_supported`

## Nest 1 Placement

| Internal block | Nest 1 role |
| --- | --- |
| Multi-head attention | `GRAPH-2` measured routing edges, `INFO-1` token flow, `SPEC-1` head spectrum, `DYN-1` layer trajectory |
| Feed-forward / MLP | tensor / geometry feature update, dynamical regime update, optimization intervention target |

## Locked Missing Inputs

- second independent prompt set for prompt-generalization
- expanded attention export beyond early/middle/late layers
- expanded MLP layer/rerun sample for stronger MLP power
- Nemotron-specific interface adapter if standard attention tensors remain unavailable
- leave-one-prompt and model-family controls after prompt-set expansion

## Acceptance Rule

- attention-flow validates only if mirror / lattice routing beats degree, centrality, and shuffled-label controls
- MLP validates only if block-update signatures separate mirror/control rows above shuffled controls
- if either lane stays invariant or negative, we record that rather than forcing the claim

## Next Execution Order

1. create second independent prompt set
2. export all standard models against prompt_set_02
3. validate prompt_set_02 and compare against base / rerun_02
4. expand layer scope beyond early/middle/late if local compute allows
5. add Nemotron-specific adapter only if needed after prompt-generalization gate
