# V8 Attention / MLP Nest 1 Bridge Gate

Status: `attention_and_mlp_supported_cross_model`

## Clean Read

The exported model set now has real transformer-internal artifacts:
attention top-k routing edges and MLP block-delta rows across
lattice, neutral, and technical contexts.

The first broad cross-model validation has started the stronger
claim-support chain across every standard-export model in the
current matrix:

- weighted attention-flow separates lattice from neutral / technical
  above shuffled context labels
- weighted attention-flow beats the degree-only graph baseline
- MLP deltas are supported in the combined export

So the gate is no longer only protocol and no longer only GLM /
Hermes. It is first broad transformer-internal support, with
Nemotron listed as an interface-adapter row for this exporter and
rerun / second-prompt repeatability still pending.

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

## Nest 1 Placement

| Internal block | Nest 1 role |
| --- | --- |
| Multi-head attention | `GRAPH-2` measured routing edges, `INFO-1` token flow, `SPEC-1` head spectrum, `DYN-1` layer trajectory |
| Feed-forward / MLP | tensor / geometry feature update, dynamical regime update, optimization intervention target |

## Locked Missing Inputs

- rerun or second independent prompt set for repeatability
- expanded attention export beyond early/middle/late layers
- expanded MLP layer/rerun sample for stronger MLP power
- Nemotron-specific interface adapter if standard attention tensors remain unavailable
- leave-one-run / leave-one-prompt controls after rerun data exists

## Acceptance Rule

- attention-flow validates only if mirror / lattice routing beats degree, centrality, and shuffled-label controls
- MLP validates only if block-update signatures separate mirror/control rows above shuffled controls
- if either lane stays invariant or negative, we record that rather than forcing the claim

## Next Execution Order

1. add a rerun or second independent prompt set
2. rerun combined attention-flow and MLP validation with repeatability controls
3. expand layer scope beyond early/middle/late if local compute allows
4. add Nemotron-specific adapter only if needed after repeatability gate
5. then promote from first cross-model support to repeatability-supported Nest 1 evidence
