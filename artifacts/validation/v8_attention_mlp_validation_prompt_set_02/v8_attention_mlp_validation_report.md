# V8 Attention / MLP Validation Report

Status: `partial_or_unsupported`

## Clean Read

The exported model set (`DeepSeek, GLM, Gemma, Hermes, Mistral, Qwen, SmolLM3`) now has real transformer-internal exports: attention top-k
routing edges and MLP block-delta rows across lattice, neutral, and
technical contexts.

The cross-model validation result is bounded but meaningful:

- weighted attention-flow separates lattice from neutral/technical above
  shuffled context labels
- the degree-only graph baseline is weaker than weighted attention-flow
- weighted attention-flow beats the degree-only baseline
- MLP deltas are not supported in this export

## Scope

- models: `DeepSeek, GLM, Gemma, Hermes, Mistral, Qwen, SmolLM3`
- attention rows: `23616`
- MLP rows: `63`

## Attention Flow

- status: `attention_flow_supported_cross_model`
- matched layer/head/query units: `984`
- weighted true score: `0.009692534`
- weighted shuffled-label p: `0.00079984`
- weighted positive units: `504 / 984`
- degree-only true score: `-0.001883406`
- degree-only shuffled-label p: `0.665266947`
- weighted minus degree score: `0.01157594`

## MLP Delta

- status: `mlp_unsupported`
- matched layer units: `21`
- true score: `-0.055347788`
- shuffled-label p: `0.411717656`
- positive units: `13 / 21`

## Boundary

- This supports a first cross-model attention-flow result across the exported model set.
- MLP is unsupported in this export; treat the result as attention-flow support only until MLP closes separately.
- This is real transformer-internal evidence, not residual-stream substitution.

## Next Step

Run an MLP-depth expansion or denser layer grid before promoting feed-forward / MLP support.
