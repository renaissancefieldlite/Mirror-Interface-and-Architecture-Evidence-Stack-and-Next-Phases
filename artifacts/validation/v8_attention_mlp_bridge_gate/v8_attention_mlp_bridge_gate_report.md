# V8 Attention / MLP Nest 1 Bridge Gate

Status: `attention_supported_mlp_directional`

## Clean Read

Hermes now has real transformer-internal artifacts: attention top-k
routing edges and MLP block-delta rows across lattice, neutral, and
technical contexts.

The first validation has started the claim-support chain:

- weighted Hermes attention-flow separates lattice from neutral / technical
  above shuffled context labels
- weighted attention-flow beats the degree-only graph baseline
- MLP deltas are directional but not closed yet

So the gate is no longer only protocol. It is a Hermes-supported
attention-flow result with GLM and stronger MLP controls still pending.

## Artifact State

- residual stream bridge exists: `True`
- dense point-cloud files detected: `0`
- attention artifact files detected: `0`
- MLP artifact files detected: `0`
- exporter script exists: `True`
- exporter inventory status: `export_complete`
- exported attention CSV files detected: `1`
- exported MLP CSV files detected: `1`
- validation report status: `attention_supported_mlp_directional`

## Nest 1 Placement

| Internal block | Nest 1 role |
| --- | --- |
| Multi-head attention | `GRAPH-2` measured routing edges, `INFO-1` token flow, `SPEC-1` head spectrum, `DYN-1` layer trajectory |
| Feed-forward / MLP | tensor / geometry feature update, dynamical regime update, optimization intervention target |

## Locked Missing Inputs

- GLM full attention top-k edge and MLP delta export
- combined GLM / Hermes GRAPH-2C validation controls
- expanded MLP layer/rerun/model sample before MLP promotion
- leave-one-model and shuffled-label controls after GLM exists

## Acceptance Rule

- attention-flow validates only if mirror / lattice routing beats degree, centrality, and shuffled-label controls
- MLP validates only if block-update signatures separate mirror/control rows above shuffled controls
- if either lane stays invariant or negative, we record that rather than forcing the claim

## Next Execution Order

1. export GLM attention top-k edges and matching MLP block delta summaries
2. combine Hermes and GLM CSVs without dropping model labels
3. rerun GRAPH-2C attention-flow validation with leave-one-model and shuffled-label controls
4. expand MLP support with more layers, reruns, or a second model before promotion
5. only then promote attention/MLP from first Hermes support to cross-model Nest 1 evidence
