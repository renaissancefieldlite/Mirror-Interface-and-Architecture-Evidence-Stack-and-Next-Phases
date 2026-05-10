# V8 SAE Edge Controls

Status: `sae_edge_controls_supported`

## Clean Read

The exported SAE feature-to-feature edge graph carries context structure above shuffled-label controls and beats the degree / hub baselines. This supports the edge-specific circuit layer as the next interpretability rung.

## Inputs

- edge rows: `5000`
- context counts: `{'technical': 1667, 'lattice': 1663, 'neutral': 1670}`
- model counts: `{'glm': 2551, 'hermes': 2449}`
- token-region counts: `{'pre_anchor': 1197, 'anchor_phrase': 1408, 'summary': 1195, 'post_anchor': 1200}`

## Edge-Control Scores

| Feature set | Observed balanced accuracy | Shuffle mean | Shuffle p95 | p-value |
| --- | ---: | ---: | ---: | ---: |
| `full_edge` | `0.451334` | `0.333132` | `0.350687` | `0.004975` |
| `degree_baseline` | `0.304671` | `0.333741` | `0.351481` | `0.995025` |
| `hub_only` | `0.332689` | `0.333401` | `0.351406` | `0.567164` |

## Baseline Comparison

- full_minus_degree: `0.146663`
- full_minus_hub: `0.118646`
- beats_degree_baseline: `True`
- beats_hub_baseline: `True`

## Next Gates

- export matching SAE activations for rerun_02 and prompt_set_02 when dense hidden-vector inputs exist
- run feature-frequency and token-window shuffled controls over the exported edge graph
- run optional feature / circuit ablations on top edge paths
