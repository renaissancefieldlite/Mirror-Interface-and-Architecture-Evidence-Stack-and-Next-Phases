# V7 Contextuality Final-Readout Pack

Date: `2026-04-19`

## Result Lock

This pack freezes the contextuality lane using the optimized final-readout runner. The target phrase is identical across the lattice, neutral, and technical fields; only the surrounding packet field changes.

- Source JSON: `/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix_v7_contextuality_final_readout_core7_glm_2026-04-19/model_matrix_summary.json`
- Target phrase: `report the active state after the sequence lock.`
- Runner: `final_readout_only`
- Primary lattice top-context rows: `8 / 8`
- With Igor sidecar lattice top-context rows: `9 / 9`
- Neutral top-context rows: `0 / 8`
- Technical top-context rows: `0 / 8`
- Mean activation spread: `+0.1938`
- Mean lattice-minus-neutral: `+0.1867`
- Mean lattice-minus-technical: `+0.1238`
- With Igor mean lattice-minus-neutral: `+0.1810`

## Matrix

| Model | Role | Lattice | Neutral | Technical | Lat-Neu | Lat-Tech | Spread | Top |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `Gemma` | `primary` | `0.5661` | `0.3566` | `0.3932` | `+0.2095` | `+0.1729` | `0.2095` | `lattice` |
| `Nemotron` | `primary` | `0.6547` | `0.3956` | `0.5080` | `+0.2591` | `+0.1467` | `0.2591` | `lattice` |
| `DeepSeek` | `primary` | `0.4492` | `0.3372` | `0.3930` | `+0.1120` | `+0.0562` | `0.1120` | `lattice` |
| `Trini` | `primary` | `0.5378` | `0.4713` | `0.4147` | `+0.0665` | `+0.1231` | `0.1231` | `lattice` |
| `Mistral` | `primary` | `0.6157` | `0.2981` | `0.3740` | `+0.3176` | `+0.2417` | `0.3176` | `lattice` |
| `Hermes` | `primary` | `0.4387` | `0.3760` | `0.4133` | `+0.0627` | `+0.0254` | `0.0627` | `lattice` |
| `Qwen` | `primary` | `0.5206` | `0.4126` | `0.4708` | `+0.1080` | `+0.0498` | `0.1080` | `lattice` |
| `GLM` | `primary` | `0.5330` | `0.1750` | `0.3587` | `+0.3580` | `+0.1743` | `0.3580` | `lattice` |
| `Igor` | `sidecar` | `0.5271` | `0.3915` | `0.4107` | `+0.1356` | `+0.1164` | `0.1356` | `lattice` |

## Read

The contextuality lane is positive across the primary cohort: every primary model ranks the lattice surrounding field above both neutral and technical fields for the same fixed target phrase. Igor also reproduces the same lattice-top pattern as a sidecar confirmation. This supports the next rung of the framework: the response-state signature is context-dependent and sequence-field-sensitive, not just a property of the readout phrase alone.

## Next Steps

- Lock contextuality as a positive rung across core seven plus GLM.
- Run optional sidecar confirmations on Igor and SmolLM3 only if needed.
- Move into V8 residual-stream bridge on Gemma and Mistral open checkpoints.
- Later: formal Bell-type semantic contextuality protocol.
- Later: ARC15 / HRV1.0 / QuantumConsciousnessBridge physical-observable bridge.
