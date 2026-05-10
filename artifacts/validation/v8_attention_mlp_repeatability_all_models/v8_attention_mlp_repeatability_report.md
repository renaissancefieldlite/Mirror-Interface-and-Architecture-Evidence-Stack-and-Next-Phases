# V8 Attention / MLP All-Model Repeatability Report

Status: `repeatability_supported`

## Clean Read

The all-exported-model attention / MLP gate repeated under the same prompt/model/export setup. Row counts, model set, support status, and shuffled-label control support are preserved; the rerun attention-flow and MLP scores remain positive and control-supported. This is repeatability of the validation result, not a claim of byte-identical internal floats.

## Scope

- models: `DeepSeek, GLM, Gemma, Hermes, Mistral, Qwen, SmolLM3`
- same status: `True`
- same model set: `True`
- same row counts: `True`

## Metrics

| Metric | Base | Rerun | Delta |
| --- | ---: | ---: | ---: |
| attention rows | `23616` | `23616` | `0.0` |
| MLP rows | `63` | `63` | `0.0` |
| attention weighted score | `0.076098811` | `0.108196075` | `0.032097264` |
| attention weighted p | `0.00019996` | `0.00019996` | `0.0` |
| attention degree score | `0.040826538` | `0.046837462` | `0.006010924` |
| attention weighted-minus-degree | `0.035272272` | `0.061358613` | `0.026086341` |
| MLP score | `6.732738861` | `6.796464998` | `0.063726137` |
| MLP p | `0.00039992` | `0.00019996` | `-0.00019996` |

## Boundary

- This closes the first repeatability gate for the same all-exported-model prompt set.
- It does not yet close prompt-generalization; the next gate is a second independent prompt set.
- `Nemotron` remains an interface-adapter row for this exporter path.
