# V8 MLP Depth Prompt Set 02 Validation Report

Status: `mlp_depth_prompt_set_02_open`

## Clean Read

The prompt_set_02 MLP gate now has a denser real transformer-internal export:
738 all-layer MLP rows across the local model matrix. This replaces the earlier
three-layer sample with a full layer-grid test for feed-forward / MLP deltas.

The result strengthens the MLP prompt_set_02 lane while keeping closeout open:
the all-layer grid is directional overall, early layers carry the strongest
signal, and shuffled-label controls remain above the observed score.

- overall status: `mlp_depth_directional`
- matched model/layer units: `246`
- true score: `0.092328608`
- shuffled-label p: `0.318936213`
- null p95: `0.299627005`
- positive units: `146 / 246`

## Prior Three-Layer Comparison

- prior prompt_set_02 status: `partial_or_unsupported`
- prior prompt_set_02 MLP supported: `False`
- prior rows: `63`
- prior true score: `-0.055347788`
- prior shuffled-label p: `0.411717656`

## Depth Breakdown

### Early

- status: `mlp_depth_directional`
- matched units: `80`
- true score: `0.369469331`
- shuffled-label p: `0.127174565`
- positive units: `56 / 80`

### Middle

- status: `mlp_depth_directional`
- matched units: `82`
- true score: `0.064314979`
- shuffled-label p: `0.215356929`
- positive units: `45 / 82`

### Late

- status: `mlp_depth_open`
- matched units: `84`
- true score: `-0.144268301`
- shuffled-label p: `0.615876825`
- positive units: `45 / 84`

## Leave-One-Model Controls

- remove `DeepSeek`: status `mlp_depth_open`, score `-0.033812578`, p `0.600679864`
- remove `GLM`: status `mlp_depth_directional`, score `0.071866582`, p `0.373925215`
- remove `Gemma`: status `mlp_depth_directional`, score `0.170158124`, p `0.225554889`
- remove `Hermes`: status `mlp_depth_directional`, score `0.267752365`, p `0.093381324`
- remove `Mistral`: status `mlp_depth_directional`, score `0.005171218`, p `0.476904619`
- remove `Qwen`: status `mlp_depth_directional`, score `0.087180559`, p `0.335732853`
- remove `SmolLM3`: status `mlp_depth_directional`, score `0.082942047`, p `0.356528694`

## Boundary

This keeps the prompt_set_02 MLP depth gate open while making the read more precise:
feed-forward deltas are directional overall, strongest in early layers, and weaker
than attention-flow under independent prompt wording. The next useful move is
rerun_02 / second export recurrence plus feature/circuit-level SAE controls,
rather than promoting MLP as closed from this grid alone.
