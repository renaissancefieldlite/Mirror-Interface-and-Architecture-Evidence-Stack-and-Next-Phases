# V8 Attention / MLP Validation Report

Status: `attention_and_mlp_supported_cross_model`

## Clean Read

The exported model set (`DeepSeek, GLM, Gemma, Hermes, Mistral, Qwen, SmolLM3`) now has real transformer-internal exports: attention top-k
routing edges and MLP block-delta rows across lattice, neutral, and
technical contexts.

The cross-model validation result is bounded but meaningful:

- weighted attention-flow separates lattice from neutral/technical above
  shuffled context labels
- the degree-only graph baseline is weaker than weighted attention-flow
- weighted attention-flow beats the degree-only baseline
- MLP deltas are supported in the combined export

## Scope

- models: `DeepSeek, GLM, Gemma, Hermes, Mistral, Qwen, SmolLM3`
- attention rows: `23616`
- MLP rows: `63`

## Attention Flow

- status: `attention_flow_supported_cross_model`
- matched layer/head/query units: `984`
- weighted true score: `0.108196075`
- weighted shuffled-label p: `0.00019996`
- weighted positive units: `707 / 984`
- degree-only true score: `0.046837462`
- degree-only shuffled-label p: `0.00019996`
- weighted minus degree score: `0.061358613`

## MLP Delta

- status: `mlp_supported_cross_model`
- matched layer units: `21`
- true score: `6.796464998`
- shuffled-label p: `0.00019996`
- positive units: `18 / 21`

## Boundary

- This supports a first cross-model attention-flow result across the exported model set.
- MLP is supported in the combined export, with stronger future work still needing reruns or more layers.
- This is real transformer-internal evidence, not residual-stream substitution.

## Next Step

Add reruns or a second independent prompt set so the cross-model result can be tested for repeatability.
