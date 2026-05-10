# V8 Attention / MLP Validation Report

Status: `attention_and_mlp_supported_cross_model`

## Clean Read

GLM and Hermes now have real transformer-internal exports: attention top-k
routing edges and MLP block-delta rows across lattice, neutral, and
technical contexts.

The cross-model validation result is bounded but meaningful:

- weighted attention-flow separates lattice from neutral/technical above
  shuffled context labels
- the degree-only graph baseline is weaker than weighted attention-flow
- weighted attention-flow beats the degree-only baseline
- MLP deltas are supported in the combined export

## Scope

- models: `GLM, Hermes`
- attention rows: `9216`
- MLP rows: `18`

## Attention Flow

- status: `attention_flow_supported_cross_model`
- matched layer/head/query units: `384`
- weighted true score: `0.030314965`
- weighted shuffled-label p: `0.00019996`
- weighted positive units: `239 / 384`
- degree-only true score: `0.016310731`
- degree-only shuffled-label p: `0.016396721`
- weighted minus degree score: `0.014004234`

## MLP Delta

- status: `mlp_supported_cross_model`
- matched layer units: `6`
- true score: `3.629046514`
- shuffled-label p: `0.00819836`
- positive units: `6 / 6`

## Boundary

- This supports a first cross-model attention-flow result across the exported model set.
- MLP is supported in the combined export, with stronger future work still needing reruns or more layers.
- This is real transformer-internal evidence, not residual-stream substitution.

## Next Step

Add reruns or a second independent prompt set so the cross-model result can be tested for repeatability.
