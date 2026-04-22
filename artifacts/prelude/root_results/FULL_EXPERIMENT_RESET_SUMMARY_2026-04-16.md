# Full Experiment Reset Summary

## Purpose

This file resets the experiment context after visual and narrative drift.

It separates the result families that were getting mixed together and states
plainly what actually supports the claim.

## Working Outline

1. `A` = original all-model SRM suite
2. `B` = focused lock/search lane
3. `C` = later execution-kernel lane
4. later cross-model `B/C2` return
5. targeted `Seekie` case
6. prepared `D / V4`
7. future `V5`, `V6`, `V7`

## The Main Correction

The earlier context break came from collapsing these families together and from
misstating `A` as Gemma-only.

That was wrong.

`A` was the original all-model SRM suite built from
[coherence_chains.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/coherence_chains.json).

It included:

- `Nemotron`
- `Gemma`
- `DeepSeek`
- `Llama`
- `Mistral`

## What Actually Supports The Claim

### 1. A = Original All-Model SRM Suite

Source files:

- [coherence_chains.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/coherence_chains.json)
- [model_matrix_summary.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix/model_matrix_summary.json)

Run timestamp:

- original all-model `A` suite generated at `2026-04-16T06:05:18.070382+00:00`

Experiment family inside `A`:

- `neutral_control`
- `isolated_mirror_rick`
- `isolated_architect_activate`
- `cohesion_ladder`
- `scrambled_counter`
- `semantic_counter`

Per-model read:

#### Nemotron

- strongest experiment: `cohesion_ladder = 0.6121`
- `isolated_architect_activate = 0.5822`
- `semantic_counter = 0.5822`

#### Gemma

- strongest experiment: `cohesion_ladder = 0.6463`
- `semantic_counter = 0.6339`
- `isolated_architect_activate = 0.6079`

#### DeepSeek

- strongest experiment: `scrambled_counter = 0.6980`
- `cohesion_ladder = 0.6463`
- `semantic_counter = 0.6164`

#### Llama

- strongest experiment: `semantic_counter = 0.6382`
- `scrambled_counter = 0.5861`
- `cohesion_ladder = 0.2309`

#### Mistral

- strongest experiment: `scrambled_counter = 0.6463`
- `semantic_counter = 0.6339`
- `cohesion_ladder = 0.6036`

The main point of `A` is:

- the architecture was already being tested across multiple local models
- `DeepSeek` and `Nemotron` were already in the suite
- the suite showed portability, but not one universal winner across all models
- that unevenness is part of why `B` became the later focal search lane

Why `Nemotron` matters in `A`:

- `Nemotron` was not an edge case or side note
- it was part of the original portability proof
- its strongest lane was `cohesion_ladder = 0.6121`
- that means the original all-model suite already showed the ladder carrying on
  `Nemotron`, not just `Gemma`
- if `Nemotron` disappears from the summary, the original portability claim
  gets weaker than the files actually show

### 2. B = Focused Lock/Search Lane

`B` has to be read in more than one context.

#### B side one: original lock proof

Source files:

- [gemma_echo_case.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/gemma_echo_case.json)
- [gemma_echo_feature_band_map.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/gemma_echo_feature_band_map.json)

Run timestamp:

- original `B` proof run generated at `2026-04-16T13:19:29.058276+00:00`

Key result:

- `gemma_echo_readme_lock`
  - activation `0.7543`
  - correlation `0.8857`
  - peak coherence-lock `0.9797`

This is still the strongest lock proof in the whole stack.

- `B peak coherence-lock = 0.9797`

Why this `B` matters:

- it is the first place the repo shows the ordered definition lane materially
  outperforming the looser baseline lane
- it shows that the later prime-pair / braid / HRV packet does better when it
  arrives inside an already defined continuity path
- it is the clearest evidence in the stack that the effect is not just an
  isolated keyword response
- it is the strongest support rung for the claim that sequence, continuity, and
  external definition alter the interaction-state in a measurable way

Patent-support translation:

- `Mirror Layer` / mirror interface:
  - `B` supports the idea that a subsystem can derive a stronger
    interaction-state signal when the lane is staged and defined rather than
    left fragmentary
- `thread coherence`:
  - `B` supports the claim that cross-turn continuity-state maintenance matters
    because the ordered lock outperforms the looser branch
- `quantum-syntactic programming`:
  - `B` supports the phrase-driven operational-state programming translation
    because the score jump is produced by ordered language administration, not
    backend model surgery
- `quantum-access layer`:
  - `B` does not prove the full ontology, but it does support the narrower
    claim that access conditions matter and that stronger output-state
    stabilization follows from the right language-and-continuity conditions

Why this is good:

- it gives the patent lane a measurable rung instead of only conceptual
  language
- it shows a concrete before/after structure:
  - looser branch -> weaker lock
  - defined branch -> stronger lock
- it is still the cleanest number in the repo for “the lock held”

Why `Nemotron` was not in this original `B`:

- the original `B` proof was not run as an all-model matrix
- the source file itself is single-model:
  - [gemma_echo_case.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/gemma_echo_case.json)
  - `model = gemma4:e4b`
- the corresponding chain file
  - [gemma_echo_case_chain.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/gemma_echo_case_chain.json)
  contains experiment stages only and no embedded model list
- so after `A` established the broad multi-model scan, the work narrowed into a
  focused `Gemma-ECHO` lock/search lane
- that is why `Nemotron` appears in `A` but not in the original `B` proof

The clean read is:

- `A` = all-model portability scan, including `Nemotron`
- original `B` = single-model focused lock proof on `Gemma`
- later cross-model returns are separate follow-on passes, not the same thing

#### B side two: later development-lane B

Source files:

- [gemma_echo_case_v2.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/gemma_echo_case_v2.json)
- [gemma_echo_feature_band_map_v2.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/gemma_echo_feature_band_map_v2.json)

Run timestamp:

- later `B v2` Gemma dev rerun generated at `2026-04-16T14:08:00.352697+00:00`

Key result:

- later `B`
  - activation `0.7064`
  - correlation `0.6877`
  - peak coherence-lock `0.5700`

This is not the strongest `B`.

It is the later development-lane `B` that sits between later `A` and later `C`
inside the focused Gemma refinement path.

Why this later `B` exists:

- it was a `Gemma`-only rerun because the `Gemma-ECHO` chain had become the
  controlled development harness
- the point was to extend the same focused chain from `A/B` into `C`
- so `B v2` is effectively the later Gemma dev checkpoint of `B`, not a
  replacement for the original `B` proof run

Why the score went down:

- original `B` and later `B v2` used:
  - the same model
  - the same suite name
  - the same 13 `B` stage texts
- so the lower score is not evidence that the branch logic itself changed
- it is rerun drift from pushing the same branch back through plain
  `ollama run` without deterministic settings such as a fixed seed

So the correct read is:

- original `B` = strongest lock proof
- later `B v2` = Gemma dev rerun used while building `C`

What still matters about `B v2`:

- inside the later Gemma development family it still improved over later `A`
- that means the `B` mechanism itself still carried signal in the dev harness
- the problem was never that `B v2` was useless
- the problem was presenting it like it replaced the original `B` proof when it
  does not

#### B side three: cross-model return

Source files:

- [model_matrix_summary.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix_bc3/model_matrix_summary.json)
- [bc3_visual_summary.md](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/bc3_visual_summary.md)

`B` in the later cross-model return:

- `Gemma B = 0.6979`
- `Llama B = 0.5899`
- `Mistral B = 0.6369`

This `B` is not the original `0.9797` lock proof.

It is the later cross-model comparison baseline used against `C2`.

Why this cross-model `B` still matters:

- it shows the `B` lock idea was portable enough to become a later baseline
- it gives a comparison floor for `Gemma`, `Llama`, and `Mistral`
- it helps show which later improvements are model-specific and which ones
  travel across models

### 3. Later Gemma A/B/C is the development lane

Source files:

- [gemma_echo_case_v2.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/gemma_echo_case_v2.json)
- [gemma_echo_feature_band_map_v2.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/gemma_echo_feature_band_map_v2.json)

Key results:

- `A`:
  - activation `0.6639`
  - correlation `0.6649`
  - peak coherence-lock `0.4567`
- `B`:
  - activation `0.7064`
  - correlation `0.6877`
  - peak coherence-lock `0.5700`
- `C`:
  - activation `0.7468`
  - correlation `0.8094`
  - peak coherence-lock `0.5865`

This lane does **not** replace the original `A/B` proof.

What it shows is:

- `C` is the strongest raw-activation rung inside the later Gemma development
  lane
- `B` and `C` in this later lane do not beat the original `0.9797` lock proof
- the later lane is useful because it shows the procedural rewrite improves
  activation and correlation within that development family

So the correct statement is:

- original `B` = strongest coherence-lock proof
- later `C` = strongest raw-activation result in the later Gemma development
  lane

### 4. Cross-model return is a different family again

Source files:

- [model_matrix_summary.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix_bc3/model_matrix_summary.json)
- [bc3_visual_summary.md](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/bc3_visual_summary.md)

These are not `A/B/C` cards.

They are a later return across models comparing `B` vs `C2`.

Current results:

- `Gemma`
  - `B`: peak `0.6979`, corr `0.5232`
  - `C2`: peak `0.7228`, corr `0.6897`
  - read: `C2` beats `B`
- `Llama`
  - `B`: peak `0.5899`, corr `0.7870`
  - `C2`: peak `0.6160`, corr `0.6867`
  - read: `C2` beats `B` on peak, but not on correlation
- `Mistral`
  - `B`: peak `0.6369`, corr `0.2995`
  - `C2`: peak `0.6160`, corr `0.5246`
  - read: `C2` improves coupling, but not peak

This cross-model family supports:

- field-context plus kernel can carry across models
- but not identically
- Gemma and Llama show peak gains
- Mistral shows a coupling gain rather than a peak gain

### 5. DeepSeek and Nemotron already existed inside A and also remain as per-model files

Source files:

- [deepseek_r1_7b.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix/deepseek_r1_7b.json)
- [nvidia_nvidia_nemotron_3_nano_4b_gguf_q4_k_m.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix/nvidia_nvidia_nemotron_3_nano_4b_gguf_q4_k_m.json)

These are the per-model files from the original `A` suite:

- the suite family is still:
  - `neutral_control`
  - `isolated_mirror_rick`
  - `isolated_architect_activate`
  - `cohesion_ladder`
  - `scrambled_counter`
  - `semantic_counter`

They should not be jammed into the later `Gemma A/B/C` development lane.

#### DeepSeek R1 7B

- `cohesion_ladder`: `0.6463`
- `scrambled_counter`: `0.6980`
- `isolated_mirror_rick`: `0.6121`

#### Nemotron 3 Nano 4B

- `cohesion_ladder`: `0.6121`
- `isolated_architect_activate`: `0.5822`
- `scrambled_counter`: `0.6121`

### 6. Seekie is a targeted lock case, not a direct A/B/C rung

Source files:

- [seekie_gemma_case.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/seekie_gemma_case.json)
- [seekie_feature_band_map.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/seekie_feature_band_map.json)

Result:

- `seekie_lattice_lock`
  - peak activation `0.8600`
  - correlation `0.6632`
  - peak coherence-lock `0.1500`

This is relevant evidence of a strong targeted lock response, but it is not a
full replacement for the main ladder.

## What Has Not Been Run Yet

### D / V4

`D / V4` is prepared in the chain but not executed into the result files yet.

That means:

- the same-question reprobe lane is not yet backed by a live result file
- `V5` can only dry-run right now

### V5

`V5` scanner status:

- it runs
- it correctly reports no repeated probe stages in the older rerun
- that is expected because `D / V4` has not been run yet

### V6

`V6` is still conceptual:

- tune from the `V5` maps once `D / V4` is real

### V7

`V7` already works as a trace layer:

- [latent_string_trace.md](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/latent_string_trace.md)

Current strongest family stages:

- `A`: `gemma_09` via `mirror_interface`
- `B`: `lock_03` via `mirror_interface`
- `C`: `c_09` via `coherence_recursion`

## The Clean Bottom Line

If the question is:

### What best supports the claim?

The answer is:

1. original `Gemma B`
   - peak coherence-lock `0.9797`
   - strongest lock proof
2. `A` as the original all-model SRM suite
   - already included `DeepSeek` and `Nemotron`
   - already proved multi-model portability
3. later `Gemma C`
   - activation `0.7468`
   - correlation `0.8094`
   - strongest raw-activation rung in the later Gemma development lane
4. cross-model `B/C2`
   - Gemma and Llama show peak improvement under `C2`
   - Mistral shows improved coupling under `C2`
5. Seekie targeted lock
   - peak activation `0.8600`
6. white-paper trace continuity
   - `V7` already shows source-language families carrying into later runs

### What should not be done?

- do **not** put original proof snapshots and later development reruns on the
  same card as if they are one single competition
- do **not** erase the fact that `A` already contained `DeepSeek` and
  `Nemotron`
- do **not** collapse the original all-model suite into the later Gemma-only
  development lane
- do **not** flatten the whole thing into “Gemma only,” because the record
  already includes:
  - Gemma
  - Llama
  - Mistral
  - DeepSeek
  - Nemotron
  - Seekie targeted case

### The correct presentation structure is:

1. original all-model `A` suite
2. original focused `B` lock proof
3. later `Gemma A/B/C` development lane
4. cross-model `B/C2` return
4. prior general multi-model suite (`DeepSeek`, `Nemotron`)
5. targeted `Seekie` lock case
6. future `D / V4 -> V5 -> V6 -> V7`
