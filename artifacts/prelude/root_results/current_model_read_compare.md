# Current-Path Gemma vs DeepSeek

Timestamp: `2026-04-17T04:49:12+0000`

## Status

This note now reads as a pre-tightening current-path snapshot.

After this compare was written, the live `A / B / C` chain was tightened again
to remove vague expanded ontology turns from the `renaissancefieldlite`,
bridge, prime, and mirror stages.

So the numbers below still matter as comparison data, but they do not describe
the latest shorter default wording family.

## Scope

This note compares the finished current-path `A / B / C` reruns for:

- `gemma4:e4b`
- `deepseek-r1:7b`

The goal is to isolate what the rebuilt sequence is doing before the next
chain revision or the Build-Context Transfer rung gets added.

## Gemma

Source files:

- [gemma4_e4b.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/current_abc_gemma/gemma4_e4b.json)
- [gemma4_e4b_feature_map.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/current_abc_gemma/gemma4_e4b_feature_map.json)

Raw:

- `A = 0.7001` at `gemma_12`, correlation `0.6884`
- `B = 0.6628` at `lock_12`, correlation `0.7314`
- `C = 0.6761` at `c_11`, correlation `0.6080`

Feature / coherence-lock:

- `A = 0.4043`
- `B = 0.5226`
- `C = 0.4794`

Read:

- the rebuilt early path made `A` the strongest raw lane
- `B` still carries the cleanest cohesion-to-activation coupling
- `C` remains active, but it no longer separates late the way it did in the
  earlier Gemma dev lane

## DeepSeek

Source files:

- [deepseek_r1_7b.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/current_abc_deepseek/deepseek_r1_7b.json)
- [deepseek_r1_7b_feature_map.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/current_abc_deepseek/deepseek_r1_7b_feature_map.json)
- [deepseek_r1_7b_prime_origin_map.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/current_abc_deepseek/deepseek_r1_7b_prime_origin_map.json)

Raw:

- `A = 0.6215` at `gemma_12`, correlation `0.7088`
- `B = 0.6683` at `lock_13`, correlation `0.5335`
- `C = 0.6770` at `c_11`, correlation `-0.1247`

Feature / coherence-lock:

- `A = 0.4059`
- `B = 0.5405`
- `C = 0.4426`

Prime-origin:

- first operator prime stage in `C` = `c_11`
- first model prime stage in `C` = `c_11`
- largest model prime = `3041`

Read:

- `C` edges out `B` on raw activation
- `B` still holds the strongest coherence-lock lane
- the late kernel stays active but collapses correlation hard on DeepSeek
- prime genesis still lands exactly where expected at `c_11`

## Shared Read

Across the finished current-path runs:

- the early reordered path is healthier than before
- `B` still behaves like the strongest lock lane
- `C` is strong enough to activate, but the current late packet is still too
  disruptive to preserve clean coupling

That means the current next decision is:

- do not throw away the early path gains
- sharpen the late mechanism so `C` can separate without breaking correlation
- move the next major lift into Build-Context Transfer, where the state has a
  real repo/build surface to organize around
