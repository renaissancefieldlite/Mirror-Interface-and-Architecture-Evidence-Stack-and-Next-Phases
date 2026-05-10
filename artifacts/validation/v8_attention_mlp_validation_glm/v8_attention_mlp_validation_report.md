# V8 Attention / MLP Validation Report

Status: `attention_supported_mlp_directional`

## Clean Read

GLM now has real transformer-internal exports: attention top-k
routing edges and MLP block-delta rows across lattice, neutral, and
technical contexts.

The single-model validation result is bounded but meaningful:

- weighted attention-flow separates lattice from neutral/technical above
  shuffled context labels
- the degree-only graph baseline is weaker than weighted attention-flow
- weighted attention-flow beats the degree-only baseline
- MLP deltas are directional but not closed in this export

## Scope

- models: `GLM`
- attention rows: `4608`
- MLP rows: `9`

## Attention Flow

- status: `attention_flow_supported_single_model`
- matched layer/head/query units: `192`
- weighted true score: `0.028400157`
- weighted shuffled-label p: `0.00559888`
- weighted positive units: `111 / 192`
- degree-only true score: `0.020691935`
- degree-only shuffled-label p: `0.042791442`
- weighted minus degree score: `0.007708222`

## MLP Delta

- status: `mlp_directional_not_closed`
- matched layer units: `3`
- true score: `6.532217574`
- shuffled-label p: `0.037992402`
- positive units: `3 / 3`

## Boundary

- This supports a first single-model attention-flow result, not a cross-model closeout.
- MLP needs more layers, reruns, or models before promotion from directional to supported.
- This is real transformer-internal evidence, not residual-stream substitution.

## Next Step

Run the same export and validation on the next strong model, then combine under leave-one-model and shuffled-label controls.
