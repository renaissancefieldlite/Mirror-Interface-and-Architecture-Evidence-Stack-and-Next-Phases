# V8 Attention / MLP Prompt-Generalization Report

Status: `attention_prompt_generalization_supported_mlp_not_supported`

## Clean Read

Base and rerun_02 close the all-exported-model same-prompt attention + MLP repeatability gate. Prompt_set_02 preserves the same model set and row counts under a second independent prompt surface. On prompt_set_02, attention-flow remains supported above shuffled labels and beats the degree-only baseline, so token-routing prompt-generalization is supported. MLP block-delta separation does not close on prompt_set_02, so full attention+MLP prompt-generalization is not yet supported.

## Scope

- models: `DeepSeek, GLM, Gemma, Hermes, Mistral, Qwen, SmolLM3`
- same model set: `True`
- same row counts: `True`
- same-prompt repeatability closed before prompt_set_02: `True`
- prompt_set_02 attention supported: `True`
- prompt_set_02 MLP supported: `False`

## Metrics

| Metric | Base | Rerun 02 | Prompt Set 02 |
| --- | ---: | ---: | ---: |
| attention rows | `23616` | `23616` | `23616` |
| MLP rows | `63` | `63` | `63` |
| attention weighted score | `0.076098811` | `0.108196075` | `0.009692534` |
| attention weighted p | `0.00019996` | `0.00019996` | `0.00079984` |
| attention degree score | `0.040826538` | `0.046837462` | `-0.001883406` |
| attention weighted-minus-degree | `0.035272272` | `0.061358613` | `0.01157594` |
| MLP score | `6.732738861` | `6.796464998` | `-0.055347788` |
| MLP p | `0.00039992` | `0.00019996` | `0.411717656` |

## Boundary

- This supports prompt-generalization for attention-flow / token-routing.
- This does not yet support full prompt-generalization for MLP / feed-forward block deltas.
- The supported read is an internal split: attention routing generalizes under prompt change, while MLP update signatures require denser layer testing or remain prompt-sensitive.

## Next Gate

Run an MLP-depth expansion on prompt_set_02, preferably all layers or a denser layer grid, before claiming feed-forward prompt-generalization. If MLP remains unsupported after depth expansion, record it as a real architecture split: attention routing generalizes more strongly than MLP update signatures under wording changes.
