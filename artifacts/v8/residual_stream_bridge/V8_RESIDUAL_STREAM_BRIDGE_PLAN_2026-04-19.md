# V8 Residual-Stream Bridge Plan

Date: `2026-04-21T04:32:23.963419+00:00`

## Objective

V8 residual-stream bridge. Uses frozen V7 contextuality prompts to compare internal hidden-state structure for lattice, neutral, and technical fields.

## Frozen Source

- V7 contextuality source: `/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix_v7_contextuality_final_readout_core7_glm_2026-04-19/model_matrix_summary.json`
- Fixed target phrase: `report the active state after the sequence lock.`

## Model Manifest

### Gemma

- behavioral model tag: `gemma4:e4b-deterministic`
- checkpoint env override: `V8_GEMMA_CHECKPOINT`
- local checkpoint candidates: `/Volumes/Renaissance Hd/hf_checkpoints/google_gemma-4-E4B-it`
- contexts: `lattice, neutral, technical`

### Mistral

- behavioral model tag: `mistral:latest`
- checkpoint env override: `V8_MISTRAL_CHECKPOINT`
- local checkpoint candidates: `/Volumes/Renaissance Hd/hf_checkpoints/mistralai_Mistral-7B-Instruct-v0.3`
- contexts: `lattice, neutral, technical`

### Qwen

- behavioral model tag: `qwen2.5:3b`
- checkpoint env override: `V8_QWEN_CHECKPOINT`
- local checkpoint candidates: `/Volumes/Renaissance Hd/hf_checkpoints/Qwen_Qwen2.5-3B-Instruct`
- contexts: `lattice, neutral, technical`

### DeepSeek

- behavioral model tag: `deepseek-r1:7b`
- checkpoint env override: `V8_DEEPSEEK_CHECKPOINT`
- local checkpoint candidates: `/Volumes/Renaissance Hd/hf_checkpoints/deepseek-ai_DeepSeek-R1-Distill-Qwen-7B`
- contexts: `lattice, neutral, technical`

### Hermes

- behavioral model tag: `openhermes:latest`
- checkpoint env override: `V8_HERMES_CHECKPOINT`
- local checkpoint candidates: `/Volumes/Renaissance Hd/hf_checkpoints/teknium_OpenHermes-2.5-Mistral-7B`
- contexts: `lattice, neutral, technical`

### Nemotron

- behavioral model tag: `hf.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF:Q4_K_M`
- checkpoint env override: `V8_NEMOTRON_CHECKPOINT`
- local checkpoint candidates: `/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/local_checkpoints/nemotron_bf16_patched, /Volumes/Renaissance Hd/hf_checkpoints/nvidia_NVIDIA-Nemotron-3-Nano-4B-BF16`
- contexts: `lattice, neutral, technical`

### GLM

- behavioral model tag: `glm-4-9b-0414:q4_k_m`
- checkpoint env override: `V8_GLM_CHECKPOINT`
- local checkpoint candidates: `/Volumes/Renaissance Hd/hf_checkpoints/THUDM_GLM-4-9B-0414`
- contexts: `lattice, neutral, technical`

### SmolLM3

- behavioral model tag: `HuggingFaceTB/SmolLM3-3B`
- checkpoint env override: `V8_SMOLLM3_CHECKPOINT`
- local checkpoint candidates: `/Volumes/Renaissance Hd/hf_checkpoints/HuggingFaceTB_SmolLM3-3B`
- contexts: `lattice, neutral, technical`

## Comparisons

- `lattice_vs_neutral`
- `lattice_vs_technical`
- `technical_vs_neutral`

## Success Condition

Lattice context shows distinguishable layerwise residual-stream structure relative to neutral and technical controls, preferably in consistent layers/token spans across Gemma and Mistral.

## Runtime Rule

V8 runs on local `transformers` checkpoints only. Do not download during the probe run. If no checkpoint path is available, the runner should mark that model as `missing_checkpoint` rather than falling back to Ollama or network access.
