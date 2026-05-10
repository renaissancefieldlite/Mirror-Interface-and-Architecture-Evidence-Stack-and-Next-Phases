# V8 SAE Recurrent Branch Ablation Report

Status: `sae_recurrent_branch_ablation_partial`

## Clean Read

Direct SAE recurrent-branch ablation produced a partial read. The report identifies which recurrent feature or edge removals move transfer readout beyond matched random controls and which branches remain descriptive at this gate.

## Pair Results

### glm_hermes

#### base_to_rerun_02

- full transfer balanced accuracy: `0.522080657`
- shared top edge count: `63`
- endpoint feature count: `13`
- endpoint-feature ablation drop: `0.090389435`, random p95 `0.061963585`, p `0.00990099`, supported `True`
- edge-key ablation drop: `0.00664881`, random p95 `0.000232261`, p `0.00990099`, supported `True`

#### base_to_prompt_set_02

- full transfer balanced accuracy: `0.396043387`
- shared top edge count: `14`
- endpoint feature count: `7`
- endpoint-feature ablation drop: `0.017598115`, random p95 `0.019533489`, p `0.089108911`, supported `False`
- edge-key ablation drop: `0.000458832`, random p95 `0.00182857`, p `0.554455446`, supported `False`

### gemma

#### base_to_rerun_02

- full transfer balanced accuracy: `0.438346883`
- shared top edge count: `78`
- endpoint feature count: `29`
- endpoint-feature ablation drop: `0.027043001`, random p95 `0.024459489`, p `0.03960396`, supported `True`
- edge-key ablation drop: `0.003342298`, random p95 `0.003394727`, p `0.069306931`, supported `False`

#### base_to_prompt_set_02

- full transfer balanced accuracy: `0.368789521`
- shared top edge count: `39`
- endpoint feature count: `17`
- endpoint-feature ablation drop: `0.007906289`, random p95 `0.017333322`, p `0.237623762`, supported `False`
- edge-key ablation drop: `0.005148016`, random p95 `0.004070517`, p `0.01980198`, supported `True`

## Inputs

- `edge_path`: `artifacts/validation/v8_sae_feature_edge_recurrence/v8_sae_feature_edge_recurrence_edges.csv`
- `edge_rows`: `28284`
- `branch_counts`: `{'glm_hermes': 15000, 'gemma': 13284}`
- `set_counts`: `{'base': 9428, 'rerun_02': 9428, 'prompt_set_02': 9428}`
- `random_trials`: `100`
- `top_k_shared_edges`: `100`

## Next Gates

- run MLP depth recurrence
- move to Nest 2D allostery after MLP depth recurrence is logged
- keep ABC / D / V5 prelude provenance linked as the sequence-scoring origin scaffold
