# V8 Attention / MLP All-Model Coverage

Status: `all_exported_model_coverage_recorded`

This records which manifest models emitted standard attention / MLP rows through the current exporter path. A missing standard row is an interface/exporter boundary, not a negative behavioral or hidden-state result.

| Model | Status | Attention rows | MLP rows | Contexts |
| --- | --- | ---: | ---: | --- |
| `Gemma` | `standard_export_supported` | 1152 | 9 | lattice, neutral, technical |
| `Mistral` | `standard_export_supported` | 4608 | 9 | lattice, neutral, technical |
| `Qwen` | `standard_export_supported` | 2304 | 9 | lattice, neutral, technical |
| `DeepSeek` | `standard_export_supported` | 4032 | 9 | lattice, neutral, technical |
| `Hermes` | `standard_export_supported` | 4608 | 9 | lattice, neutral, technical |
| `Nemotron` | `interface_adapter_needed` | 0 | 0 | none |
| `GLM` | `standard_export_supported` | 4608 | 9 | lattice, neutral, technical |
| `SmolLM3` | `standard_export_supported` | 2304 | 9 | lattice, neutral, technical |

## Clean Read

- `7/8` manifest models emitted standard transformer-internal rows.
- `Nemotron` is checkpoint-ready but needs a model-specific interface adapter for this exporter path.
- all-exported-model validation should therefore be read as broad support across every standard-export model, not as a failed `Nemotron` row.
