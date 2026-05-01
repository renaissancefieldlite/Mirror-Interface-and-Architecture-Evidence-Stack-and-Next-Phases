# V8 MLP Depth Recurrence Report

Status: `mlp_depth_recurrence_directional`

## Clean Read

All-layer MLP depth recurrence is strongest on same-prompt rerun. Prompt-shift recurrence remains the pressure point.

## Inputs

- base CSV: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/v8_mlp_depth_base/v8_mlp_depth_base.csv`
- rerun_02 CSV: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/v8_mlp_depth_rerun_02/v8_mlp_depth_rerun_02.csv`
- prompt_set_02 CSV: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/v8_mlp_depth_prompt_set_02/v8_mlp_depth_prompt_set_02.csv`
- matched units per set: `246`

## Within-Set MLP Depth Separation

- `base`: status `mlp_depth_directional`, score `1.166711081`, p `0.029194161`, positive `180 / 246`
- `rerun_02`: status `mlp_depth_directional`, score `1.166711081`, p `0.024995001`, positive `180 / 246`
- `prompt_set_02`: status `mlp_depth_directional`, score `0.092328608`, p `0.316136773`, positive `146 / 246`

## Pair Recurrence

- `base_to_rerun_02`: status `recurrence_supported`, cosine `1.0`, p `0.00019996`, sign agreement `1.0`
- `base_to_prompt_set_02`: status `recurrence_open`, cosine `-0.166467701`, p `0.669466107`, sign agreement `0.528455285`
- `rerun_02_to_prompt_set_02`: status `recurrence_open`, cosine `-0.166467701`, p `0.671465707`, sign agreement `0.528455285`

## Depth Breakdown

### base_to_rerun_02

- `early`: status `recurrence_supported`, cosine `1.0`, p `0.00019996`, matched `80`
- `middle`: status `recurrence_supported`, cosine `1.0`, p `0.00019996`, matched `82`
- `late`: status `recurrence_supported`, cosine `1.0`, p `0.00019996`, matched `84`

### base_to_prompt_set_02

- `early`: status `recurrence_open`, cosine `-0.41512401`, p `0.559488102`, matched `80`
- `middle`: status `recurrence_open`, cosine `-0.032287554`, p `0.462707459`, matched `82`
- `late`: status `recurrence_open`, cosine `-0.042333213`, p `0.50609878`, matched `84`

### rerun_02_to_prompt_set_02

- `early`: status `recurrence_open`, cosine `-0.41512401`, p `0.566286743`, matched `80`
- `middle`: status `recurrence_open`, cosine `-0.032287554`, p `0.463707259`, matched `82`
- `late`: status `recurrence_open`, cosine `-0.042333213`, p `0.50529894`, matched `84`

## Leave-One-Model Prompt-Shift Controls

- remove `DeepSeek`: status `recurrence_directional`, cosine `0.173705401`, p `0.326734653`, matched `218`
- remove `GLM`: status `recurrence_open`, cosine `-0.176794651`, p `0.671265747`, matched `206`
- remove `Gemma`: status `recurrence_open`, cosine `-0.193443793`, p `0.677864427`, matched `204`
- remove `Hermes`: status `recurrence_open`, cosine `-0.198750459`, p `0.678464307`, matched `214`
- remove `Mistral`: status `recurrence_open`, cosine `-0.1706185`, p `0.660067986`, matched `214`
- remove `Qwen`: status `recurrence_open`, cosine `-0.346921638`, p `0.728654269`, matched `210`
- remove `SmolLM3`: status `recurrence_open`, cosine `-0.167563146`, p `0.671065787`, matched `210`

## Outcome

This keeps attention-flow and SAE as the stronger middle-layer mechanisms while preserving MLP as a measured open gate.
