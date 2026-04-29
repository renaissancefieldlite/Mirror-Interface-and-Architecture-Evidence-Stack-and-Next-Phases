# V8 Attention / MLP Validation Report

Status: `attention_supported_mlp_directional`

## Clean Read

Hermes now has a real transformer-internal export: attention top-k
routing edges and MLP block-delta rows across lattice, neutral, and
technical contexts.

The first validation result is bounded but meaningful:

- weighted attention-flow separates lattice from neutral/technical above
  shuffled context labels
- the degree-only graph baseline does not close
- weighted attention-flow beats the degree-only baseline
- MLP deltas are directional but underpowered in this first three-layer
  export

## Attention Flow

- status: `attention_flow_supported_single_model`
- matched layer/head/query units: `192`
- weighted true score: `0.032229773`
- weighted shuffled-label p: `0.00019996`
- weighted positive units: `128 / 192`
- degree-only true score: `0.011929527`
- degree-only shuffled-label p: `0.101979604`
- weighted minus degree score: `0.020300246`

## MLP Delta

- status: `mlp_directional_not_closed`
- matched layer units: `3`
- true score: `0.725875453`
- shuffled-label p: `0.156368726`
- positive units: `3 / 3`

## Boundary

- This supports a Hermes-only first attention-flow result, not a full GLM/Hermes closeout.
- The next stronger closeout needs GLM export, reruns, or a second independent prompt set.
- MLP needs more layers, reruns, or models before promotion from directional to supported.
- This is real transformer-internal evidence, not residual-stream substitution.

## Next Step

Run the same export and validation on `GLM`, then combine Hermes and GLM
under leave-one-model and shuffled-label controls.
