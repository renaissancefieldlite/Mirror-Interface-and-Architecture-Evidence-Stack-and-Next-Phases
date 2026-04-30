#!/usr/bin/env python3
"""Bounded SAE pilot on real GLM / Hermes dense V8 activations.

This runner turns the SAE gate from protocol-only into a first real artifact:

1. load dense V8 hidden-state point clouds for GLM and Hermes
2. draw a stratified bounded sample across context, layer depth, and token region
3. train a small sparse autoencoder on the real activation vectors
4. export sparse feature activations, feature dictionaries, and feature edges
5. validate feature separation against shuffled-label controls

The runner intentionally keeps the model small and the outputs auditable. It
does not claim causal feature circuits or ablation support; those are the next
gate after feature/circuit export.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[2]
DENSE_DIR = ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "point_clouds_dense_trajectory"
EXPORT_ROOT = ROOT / "artifacts" / "validation" / "v8_sae_feature_circuit_exports"
VALIDATION_ROOT = ROOT / "artifacts" / "validation" / "v8_sae_feature_circuit_validation"

SEED = 67
LATENT_DIM = 64
MAX_PER_GROUP = 180
BATCH_SIZE = 256
EPOCHS = 8
LEARNING_RATE = 1e-3
L1_WEIGHT = 1e-3
TOP_K_ACTIVATIONS = 5
SHUFFLES = 100
CONTEXTS = ("lattice", "neutral", "technical")


@dataclass(frozen=True)
class SampleData:
    points: np.ndarray
    labels: dict[str, np.ndarray]


class SparseAutoencoder(torch.nn.Module):
    def __init__(self, input_dim: int, latent_dim: int) -> None:
        super().__init__()
        self.encoder = torch.nn.Linear(input_dim, latent_dim)
        self.decoder = torch.nn.Linear(latent_dim, input_dim)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        z = torch.relu(self.encoder(x))
        return self.decoder(z), z


def dense_inputs() -> list[tuple[str, Path]]:
    rows = []
    for path in sorted(DENSE_DIR.glob("*.npz")):
        name = path.name.replace("_v8_hidden_point_cloud.npz", "")
        if name in {"glm", "hermes"}:
            rows.append((name, path))
    if len(rows) != 2:
        raise RuntimeError(f"Expected GLM and Hermes dense inputs in {DENSE_DIR}, found {rows}")
    return rows


def load_stratified_sample() -> SampleData:
    rng = np.random.default_rng(SEED)
    sampled_points: list[np.ndarray] = []
    labels: dict[str, list[Any]] = defaultdict(list)

    for model_name, path in dense_inputs():
        data = np.load(path, allow_pickle=True)
        points = data["points"]
        context = data["context_label"]
        layer_depth = data["layer_depth"]
        token_region = data["token_region"]

        for context_label in CONTEXTS:
            for depth in sorted(np.unique(layer_depth)):
                for region in sorted(np.unique(token_region)):
                    mask = (context == context_label) & (layer_depth == depth) & (token_region == region)
                    idx = np.where(mask)[0]
                    if idx.size == 0:
                        continue
                    take = min(MAX_PER_GROUP, idx.size)
                    chosen = rng.choice(idx, size=take, replace=False)
                    sampled_points.append(points[chosen].astype(np.float32, copy=False))
                    for key in [
                        "context_label",
                        "context_id",
                        "layer_index",
                        "layer_depth",
                        "token_role",
                        "token_index",
                        "token_region",
                        "feature_family",
                    ]:
                        labels[key].extend(data[key][chosen].tolist())
                    labels["model"].extend([model_name] * take)
                    labels["source_path"].extend([str(path.relative_to(ROOT))] * take)

    if not sampled_points:
        raise RuntimeError("No sampled V8 points were collected")

    stacked = np.vstack(sampled_points).astype(np.float32, copy=False)
    label_arrays = {key: np.asarray(value) for key, value in labels.items()}
    return SampleData(points=stacked, labels=label_arrays)


def standardize(points: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = points.mean(axis=0, dtype=np.float64).astype(np.float32)
    std = points.std(axis=0, dtype=np.float64).astype(np.float32)
    std[std < 1e-6] = 1.0
    scaled = ((points - mean) / std).astype(np.float32)
    return scaled, mean, std


def train_sae(points: np.ndarray) -> tuple[SparseAutoencoder, list[dict[str, float]], np.ndarray, np.ndarray]:
    torch.manual_seed(SEED)
    scaled, mean, std = standardize(points)
    tensor = torch.from_numpy(scaled)
    model = SparseAutoencoder(points.shape[1], LATENT_DIM)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    history: list[dict[str, float]] = []

    generator = torch.Generator().manual_seed(SEED)
    for epoch in range(EPOCHS):
        permutation = torch.randperm(tensor.shape[0], generator=generator)
        total_loss = 0.0
        total_mse = 0.0
        total_l1 = 0.0
        for start in range(0, tensor.shape[0], BATCH_SIZE):
            batch = tensor[permutation[start : start + BATCH_SIZE]]
            optimizer.zero_grad(set_to_none=True)
            recon, z = model(batch)
            mse = torch.nn.functional.mse_loss(recon, batch)
            l1 = z.abs().mean()
            loss = mse + L1_WEIGHT * l1
            loss.backward()
            optimizer.step()
            total_loss += float(loss.detach()) * batch.shape[0]
            total_mse += float(mse.detach()) * batch.shape[0]
            total_l1 += float(l1.detach()) * batch.shape[0]
        denom = float(tensor.shape[0])
        history.append(
            {
                "epoch": float(epoch + 1),
                "loss": total_loss / denom,
                "mse": total_mse / denom,
                "l1": total_l1 / denom,
            }
        )
    return model, history, mean, std


def encode(model: SparseAutoencoder, points: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    scaled = ((points - mean) / std).astype(np.float32)
    model.eval()
    outputs = []
    with torch.no_grad():
        tensor = torch.from_numpy(scaled)
        for start in range(0, tensor.shape[0], BATCH_SIZE):
            _, z = model(tensor[start : start + BATCH_SIZE])
            outputs.append(z.cpu().numpy().astype(np.float32))
    return np.vstack(outputs)


def write_feature_activations(z: np.ndarray, labels: dict[str, np.ndarray], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "sample_id",
        "model",
        "prompt_set",
        "context",
        "layer_index",
        "layer_depth",
        "token_index",
        "token_role",
        "token_region",
        "feature_id",
        "activation",
        "sparsity",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for sample_id, row in enumerate(z):
            top = np.argsort(row)[-TOP_K_ACTIVATIONS:][::-1]
            sparsity = float(np.mean(row > 1e-6))
            for feature_id in top:
                activation = float(row[feature_id])
                if activation <= 0:
                    continue
                writer.writerow(
                    {
                        "sample_id": sample_id,
                        "model": labels["model"][sample_id],
                        "prompt_set": "dense_v8",
                        "context": labels["context_label"][sample_id],
                        "layer_index": int(labels["layer_index"][sample_id]),
                        "layer_depth": labels["layer_depth"][sample_id],
                        "token_index": int(labels["token_index"][sample_id]),
                        "token_role": labels["token_role"][sample_id],
                        "token_region": labels["token_region"][sample_id],
                        "feature_id": int(feature_id),
                        "activation": activation,
                        "sparsity": sparsity,
                    }
                )


def most_common(values: np.ndarray) -> str:
    if values.size == 0:
        return ""
    return Counter(values.tolist()).most_common(1)[0][0]


def write_feature_dictionary(
    z: np.ndarray,
    labels: dict[str, np.ndarray],
    model: SparseAutoencoder,
    path: Path,
) -> list[dict[str, Any]]:
    decoder_weight = model.decoder.weight.detach().cpu().numpy()
    rows: list[dict[str, Any]] = []
    for feature_id in range(z.shape[1]):
        values = z[:, feature_id]
        active = values > np.percentile(values, 90)
        if not np.any(active):
            active = values > 0
        lattice_mean = float(values[labels["context_label"] == "lattice"].mean())
        control_mean = float(values[labels["context_label"] != "lattice"].mean())
        rows.append(
            {
                "model": "glm_hermes_bounded_pilot",
                "layer_index": "mixed_dense_v8",
                "feature_id": feature_id,
                "top_context": most_common(labels["context_label"][active]),
                "top_layer_depth": most_common(labels["layer_depth"][active]),
                "top_token_region": most_common(labels["token_region"][active]),
                "top_token_role": most_common(labels["token_role"][active]),
                "mean_activation": float(values.mean()),
                "activation_rate": float(np.mean(values > 1e-6)),
                "lattice_lift_vs_controls": lattice_mean - control_mean,
                "decoder_norm": float(np.linalg.norm(decoder_weight[:, feature_id])),
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_feature_edges(z: np.ndarray, labels: dict[str, np.ndarray], path: Path) -> int:
    rows = []
    groups: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for idx, key in enumerate(zip(labels["model"], labels["context_label"], labels["token_region"], strict=False)):
        groups[key].append(idx)

    for (model_name, context_label, token_region), indices in groups.items():
        sub_idx = np.asarray(indices)
        layers = sorted(int(x) for x in np.unique(labels["layer_index"][sub_idx]))
        means = {}
        for layer in layers:
            layer_idx = sub_idx[labels["layer_index"][sub_idx] == layer]
            if layer_idx.size:
                means[layer] = z[layer_idx].mean(axis=0)
        for source_layer, target_layer in zip(layers[:-1], layers[1:], strict=False):
            if source_layer not in means or target_layer not in means:
                continue
            source = means[source_layer]
            target = means[target_layer]
            source_top = np.argsort(source)[-3:][::-1]
            target_top = np.argsort(target)[-3:][::-1]
            for source_feature in source_top:
                for target_feature in target_top:
                    rows.append(
                        {
                            "model": model_name,
                            "prompt_set": "dense_v8",
                            "context": context_label,
                            "token_region": token_region,
                            "source_layer": source_layer,
                            "source_feature_id": int(source_feature),
                            "target_layer": target_layer,
                            "target_feature_id": int(target_feature),
                            "edge_weight": float(source[source_feature] * target[target_feature]),
                            "edge_type": "adjacent_layer_mean_activation",
                        }
                    )
    rows = sorted(rows, key=lambda row: row["edge_weight"], reverse=True)[:5000]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def validate_features(z: np.ndarray, labels: dict[str, np.ndarray]) -> dict[str, Any]:
    y = labels["context_label"]
    train_x, test_x, train_y, test_y = train_test_split(
        z,
        y,
        test_size=0.30,
        random_state=SEED,
        stratify=y,
    )
    clf = LogisticRegression(max_iter=1000, random_state=SEED)
    clf.fit(train_x, train_y)
    pred = clf.predict(test_x)
    observed_acc = float(accuracy_score(test_y, pred))
    observed_balanced = float(balanced_accuracy_score(test_y, pred))

    rng = np.random.default_rng(SEED)
    shuffled_balanced = []
    shuffled_acc = []
    for _ in range(SHUFFLES):
        shuffled = rng.permutation(train_y)
        control = LogisticRegression(max_iter=1000, random_state=SEED)
        control.fit(train_x, shuffled)
        control_pred = control.predict(test_x)
        shuffled_acc.append(float(accuracy_score(test_y, control_pred)))
        shuffled_balanced.append(float(balanced_accuracy_score(test_y, control_pred)))
    shuffled_balanced_arr = np.asarray(shuffled_balanced)
    p_value = float((np.sum(shuffled_balanced_arr >= observed_balanced) + 1) / (SHUFFLES + 1))
    return {
        "classifier": "logistic_regression_on_sae_features",
        "contexts": list(CONTEXTS),
        "observed_accuracy": observed_acc,
        "observed_balanced_accuracy": observed_balanced,
        "shuffled_accuracy_mean": float(np.mean(shuffled_acc)),
        "shuffled_balanced_accuracy_mean": float(np.mean(shuffled_balanced_arr)),
        "shuffled_balanced_accuracy_p95": float(np.percentile(shuffled_balanced_arr, 95)),
        "shuffle_count": SHUFFLES,
        "shuffle_p_value": p_value,
        "feature_separation_supported": bool(
            observed_balanced > np.percentile(shuffled_balanced_arr, 95) and p_value <= 0.05
        ),
    }


def write_report(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 SAE Bounded Pilot Report",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Inputs",
        "",
        f"- dense rows sampled: `{report['sample']['rows']}`",
        f"- hidden size: `{report['sample']['hidden_size']}`",
        f"- latent features: `{report['config']['latent_dim']}`",
        f"- max rows per model/context/layer-depth/token-region group: `{report['config']['max_per_group']}`",
        "",
        "## Training",
        "",
        f"- final reconstruction MSE: `{report['training']['final_mse']:.6f}`",
        f"- final sparse activation L1: `{report['training']['final_l1']:.6f}`",
        f"- mean feature sparsity: `{report['training']['mean_feature_sparsity']:.6f}`",
        "",
        "## Feature-Control Validation",
        "",
        f"- observed balanced accuracy: `{report['validation']['observed_balanced_accuracy']:.6f}`",
        f"- shuffled balanced accuracy mean: `{report['validation']['shuffled_balanced_accuracy_mean']:.6f}`",
        f"- shuffled balanced accuracy p95: `{report['validation']['shuffled_balanced_accuracy_p95']:.6f}`",
        f"- shuffled-control p-value: `{report['validation']['shuffle_p_value']:.6f}`",
        f"- feature separation supported: `{report['validation']['feature_separation_supported']}`",
        "",
        "## Exports",
        "",
    ]
    for key, value in report["exports"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Next Gates", ""])
    for item in report["next_gates"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    VALIDATION_ROOT.mkdir(parents=True, exist_ok=True)
    (EXPORT_ROOT / "sae_models").mkdir(parents=True, exist_ok=True)

    sample = load_stratified_sample()
    model, history, mean, std = train_sae(sample.points)
    z = encode(model, sample.points, mean, std)
    validation = validate_features(z, sample.labels)

    model_path = EXPORT_ROOT / "sae_models" / "v8_sae_bounded_pilot_state.pt"
    torch.save(
        {
            "state_dict": model.state_dict(),
            "mean": mean,
            "std": std,
            "config": {
                "latent_dim": LATENT_DIM,
                "epochs": EPOCHS,
                "batch_size": BATCH_SIZE,
                "l1_weight": L1_WEIGHT,
                "seed": SEED,
            },
        },
        model_path,
    )
    activations_path = EXPORT_ROOT / "v8_sae_feature_activations.csv"
    dictionary_path = EXPORT_ROOT / "v8_sae_feature_dictionary.csv"
    edges_path = EXPORT_ROOT / "v8_sae_feature_circuit_edges.csv"
    write_feature_activations(z, sample.labels, activations_path)
    dictionary_rows = write_feature_dictionary(z, sample.labels, model, dictionary_path)
    edge_count = write_feature_edges(z, sample.labels, edges_path)

    status = (
        "feature_separation_supported_circuit_edges_exported"
        if validation["feature_separation_supported"]
        else "feature_exports_complete_control_support_pending"
    )
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "clean_read": (
            "Bounded SAE pilot trained on real GLM / Hermes dense V8 activations. "
            "Sparse features separate lattice / neutral / technical contexts above shuffled-label controls, "
            "and feature-to-feature edge exports are ready for the next circuit / ablation gate."
            if validation["feature_separation_supported"]
            else "Bounded SAE pilot trained on real GLM / Hermes dense V8 activations and exported features, "
            "dictionaries, and edges. Shuffled-label controls did not close the feature separation gate yet."
        ),
        "config": {
            "seed": SEED,
            "latent_dim": LATENT_DIM,
            "max_per_group": MAX_PER_GROUP,
            "epochs": EPOCHS,
            "batch_size": BATCH_SIZE,
            "l1_weight": L1_WEIGHT,
            "shuffles": SHUFFLES,
        },
        "sample": {
            "rows": int(sample.points.shape[0]),
            "hidden_size": int(sample.points.shape[1]),
            "context_counts": dict(Counter(sample.labels["context_label"].tolist())),
            "model_counts": dict(Counter(sample.labels["model"].tolist())),
        },
        "training": {
            "history": history,
            "final_mse": history[-1]["mse"],
            "final_l1": history[-1]["l1"],
            "mean_feature_sparsity": float(np.mean(z > 1e-6)),
        },
        "validation": validation,
        "top_lattice_lift_features": sorted(
            dictionary_rows,
            key=lambda row: row["lattice_lift_vs_controls"],
            reverse=True,
        )[:10],
        "exports": {
            "model": str(model_path.relative_to(ROOT)),
            "feature_activations": str(activations_path.relative_to(ROOT)),
            "feature_dictionary": str(dictionary_path.relative_to(ROOT)),
            "feature_circuit_edges": str(edges_path.relative_to(ROOT)),
            "edge_count": edge_count,
        },
        "next_gates": [
            "run feature/circuit edge controls beyond label-shuffle feature separation",
            "add prompt_set_02 and rerun_02 SAE exports for prompt-generalized feature support",
            "run optional ablations on top SAE features and top feature-circuit edges",
        ],
    }
    json_path = VALIDATION_ROOT / "v8_sae_feature_circuit_validation_report.json"
    md_path = VALIDATION_ROOT / "v8_sae_feature_circuit_validation_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_report(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path), "validation": validation}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
