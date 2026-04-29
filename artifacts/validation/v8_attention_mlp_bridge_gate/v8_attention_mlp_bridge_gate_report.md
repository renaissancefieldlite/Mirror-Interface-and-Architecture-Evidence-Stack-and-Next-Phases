# V8 Attention / MLP Nest 1 Bridge Gate

Status: `attention_prompt_generalization_supported_mlp_not_supported`

## Clean Read

The all-exported-model attention / MLP gate now has same-prompt
repeatability plus a second independent prompt-set test.

Prompt_set_02 preserved the same seven standard-export models and
the same row counts: `23616` attention rows and `63` MLP rows.

The prompt-generalization result is split but meaningful:

- attention-flow / token-routing remains supported above shuffled
  context labels
- weighted attention-flow beats the degree-only graph baseline
- MLP / feed-forward block deltas do not close on prompt_set_02

So the current closed claim is attention prompt-generalization, not
full attention + MLP prompt-generalization. The next gate is an
MLP-depth expansion before deciding whether feed-forward deltas are
underpowered here or genuinely more prompt-sensitive.

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
- prompt-generalization report status: `attention_prompt_generalization_supported_mlp_not_supported`

## Nest 1 Placement

| Internal block | Nest 1 role |
| --- | --- |
| Multi-head attention | `GRAPH-2` measured routing edges, `INFO-1` token flow, `SPEC-1` head spectrum, `DYN-1` layer trajectory |
| Feed-forward / MLP | tensor / geometry feature update, dynamical regime update, optimization intervention target |

## Locked Missing Inputs

- MLP-depth expansion on prompt_set_02 using all layers or a denser layer grid
- third prompt or paraphrase-family stress test after MLP-depth result
- leave-one-prompt and model-family controls after multiple prompt sets exist
- Nemotron-specific interface adapter if standard attention tensors remain unavailable

## Acceptance Rule

- attention-flow validates only if mirror / lattice routing beats degree, centrality, and shuffled-label controls
- MLP validates only if block-update signatures separate mirror/control rows above shuffled controls
- if either lane stays invariant or negative, we record that rather than forcing the claim

## Next Execution Order

1. run MLP-depth expansion on prompt_set_02
2. compare prompt_set_02 MLP-depth result against base / rerun_02
3. if MLP remains unsupported, record the split: attention routing generalizes more strongly than MLP deltas under prompt change
4. then add leave-one-prompt / model-family controls
5. add Nemotron-specific adapter only after the standard prompt-generalization path is stable
