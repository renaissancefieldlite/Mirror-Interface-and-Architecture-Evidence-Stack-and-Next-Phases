#!/usr/bin/env python3
"""Validate a Gemma-native SAE recurrence branch.

The first bounded SAE branch was trained on GLM / Hermes dense V8 activations
with 4096-dim hidden states. Gemma uses a 2560-dim hidden state, so it gets its
own model-native SAE rather than being forced through the GLM / Hermes encoder.

This runner:

1. loads real Gemma dense V8 exports for base, rerun_02, and prompt_set_02
2. trains a bounded SAE on the Gemma base dense activation sample
3. applies the same Gemma SAE to rerun_02 and prompt_set_02
4. tests context separation and base-to-set transfer against shuffled labels
5. records feature-lift recurrence so Gemma becomes the third SAE branch
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
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[2]
POINT_ROOT = ROOT / "artifacts" / "v8" / "residual_stream_bridge"
OUT = ROOT / "artifacts" / "validation" / "v8_sae_gemma_recurrence_validation"
MODEL_PATH = OUT / "sae_models" / "v8_sae_gemma_recurrence_state.pt"

SEED = 67
LATENT_DIM = 64
MAX_PER_GROUP = 180
BATCH_SIZE = 256
EPOCHS = 8
LEARNING_RATE = 1e-3
L1_WEIGHT = 1e-3
SHUFFLES = 100
CONTEXTS = ("lattice", "neutral", "technical")
SETS = {
    "base": POINT_ROOT / "point_clouds_dense_trajectory_gemma_base",
    "rerun_02": POINT_ROOT / "point_clouds_dense_trajectory_gemma_rerun_02",
    "prompt_set_02": POINT_ROOT / "point_clouds_dense_trajectory_gemma_prompt_set_02",
}


@dataclass(frozen=True)
class DenseSet:
    name: str
    points: np.ndarray
    labels: dict[str, np.ndarray]


@dataclass(frozen=True)
class EncodedSet:
    name: str
    z: np.ndarray
    labels: dict[str, np.ndarray]


class SparseAutoencoder(torch.nn.Module):
    def __init__(self, input_dim: int, latent_dim: int) -> None:
        super().__init__()
        self.encoder = torch.nn.Linear(input_dim, latent_dim)
        self.decoder = torch.nn.Linear(latent_dim, input_dim)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        z = torch.relu(self.encoder(x))
        return self.decoder(z), z


def stable_seed(name: str) -> int:
    return SEED + sum((idx + 1) * ord(char) for idx, char in enumerate(name))


def require_inputs() -> None:
    for set_name, directory in SETS.items():
        path = directory / "gemma_v8_hidden_point_cloud.npz"
        if not path.exists():
            raise SystemExit(f"{set_name} Gemma dense input missing: {path}")


def load_gemma_set(set_name: str, directory: Path) -> DenseSet:
    rng = np.random.default_rng(stable_seed(set_name))
    path = directory / "gemma_v8_hidden_point_cloud.npz"
    data = np.load(path, allow_pickle=True)
    points = data["points"]
    context = data["context_label"]
    layer_depth = data["layer_depth"]
    token_region = data["token_region"]
    sampled_points: list[np.ndarray] = []
    labels: dict[str, list[Any]] = defaultdict(list)

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
                labels["model"].extend(["gemma"] * take)
                labels["source_set"].extend([set_name] * take)
                labels["source_path"].extend([str(path.relative_to(ROOT))] * take)

    if not sampled_points:
        raise RuntimeError(f"No Gemma rows sampled for {set_name}")
    return DenseSet(
        name=set_name,
        points=np.vstack(sampled_points).astype(np.float32, copy=False),
        labels={key: np.asarray(value) for key, value in labels.items()},
    )


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
    generator = torch.Generator().manual_seed(SEED)
    history: list[dict[str, float]] = []

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
    tensor = torch.from_numpy(scaled)
    model.eval()
    outputs = []
    with torch.no_grad():
        for start in range(0, tensor.shape[0], BATCH_SIZE):
            _, z = model(tensor[start : start + BATCH_SIZE])
            outputs.append(z.cpu().numpy().astype(np.float32))
    return np.vstack(outputs)


def validate_within(encoded: EncodedSet) -> dict[str, Any]:
    y = encoded.labels["context_label"]
    train_x, test_x, train_y, test_y = train_test_split(
        encoded.z,
        y,
        test_size=0.30,
        random_state=SEED,
        stratify=y,
    )
    clf = LogisticRegression(max_iter=1000, random_state=SEED)
    clf.fit(train_x, train_y)
    observed = float(balanced_accuracy_score(test_y, clf.predict(test_x)))
    rng = np.random.default_rng(stable_seed(encoded.name))
    shuffled = []
    for _ in range(SHUFFLES):
        control = LogisticRegression(max_iter=1000, random_state=SEED)
        control.fit(train_x, rng.permutation(train_y))
        shuffled.append(float(balanced_accuracy_score(test_y, control.predict(test_x))))
    arr = np.asarray(shuffled, dtype=float)
    p_value = float((np.sum(arr >= observed) + 1) / (SHUFFLES + 1))
    return {
        "observed_balanced_accuracy": round(observed, 9),
        "shuffled_mean": round(float(arr.mean()), 9),
        "shuffled_p95": round(float(np.quantile(arr, 0.95)), 9),
        "p_value": round(p_value, 9),
        "supported": bool(observed > np.quantile(arr, 0.95) and p_value <= 0.05),
    }


def validate_transfer(train: EncodedSet, test: EncodedSet) -> dict[str, Any]:
    train_y = train.labels["context_label"]
    test_y = test.labels["context_label"]
    clf = LogisticRegression(max_iter=1000, random_state=SEED)
    clf.fit(train.z, train_y)
    observed = float(balanced_accuracy_score(test_y, clf.predict(test.z)))
    rng = np.random.default_rng(stable_seed(f"{train.name}_to_{test.name}"))
    shuffled = []
    for _ in range(SHUFFLES):
        control = LogisticRegression(max_iter=1000, random_state=SEED)
        control.fit(train.z, rng.permutation(train_y))
        shuffled.append(float(balanced_accuracy_score(test_y, control.predict(test.z))))
    arr = np.asarray(shuffled, dtype=float)
    p_value = float((np.sum(arr >= observed) + 1) / (SHUFFLES + 1))
    return {
        "train_set": train.name,
        "test_set": test.name,
        "observed_balanced_accuracy": round(observed, 9),
        "shuffled_mean": round(float(arr.mean()), 9),
        "shuffled_p95": round(float(np.quantile(arr, 0.95)), 9),
        "p_value": round(p_value, 9),
        "supported": bool(observed > np.quantile(arr, 0.95) and p_value <= 0.05),
    }


def lift_vector(encoded: EncodedSet) -> np.ndarray:
    y = encoded.labels["context_label"]
    lattice = encoded.z[y == "lattice"].mean(axis=0)
    controls = encoded.z[y != "lattice"].mean(axis=0)
    return lattice - controls


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0.0:
        return 0.0
    return float(np.dot(a, b) / denom)


def top_feature_overlap(a: np.ndarray, b: np.ndarray, top_k: int = 10) -> dict[str, Any]:
    a_top = set(np.argsort(a)[-top_k:].tolist())
    b_top = set(np.argsort(b)[-top_k:].tolist())
    intersection = sorted(a_top & b_top)
    union = a_top | b_top
    return {
        "top_k": top_k,
        "intersection_count": len(intersection),
        "jaccard": round(float(len(intersection) / len(union)) if union else 0.0, 9),
        "intersection_features": intersection,
    }


def write_profiles(encoded_sets: list[EncodedSet], path: Path) -> None:
    rows = []
    for encoded in encoded_sets:
        for context in CONTEXTS:
            mask = encoded.labels["context_label"] == context
            sub = encoded.z[mask]
            for feature_id in range(encoded.z.shape[1]):
                values = sub[:, feature_id]
                rows.append(
                    {
                        "source_set": encoded.name,
                        "model": "gemma",
                        "context": context,
                        "feature_id": feature_id,
                        "mean_activation": float(values.mean()),
                        "activation_rate": float(np.mean(values > 1e-6)),
                    }
                )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 SAE Gemma Recurrence Validation Report",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Why Gemma Gets A Native Branch",
        "",
        (
            "Gemma dense V8 vectors are 2560-dimensional, while the first GLM / Hermes SAE branch is 4096-dimensional. "
            "This run keeps the evidence clean by training a Gemma-native SAE on Gemma base vectors, then applying that same locked Gemma encoder to rerun_02 and prompt_set_02."
        ),
        "",
        "## Sample",
        "",
    ]
    for set_name, summary in report["sample"].items():
        lines.extend(
            [
                f"### {set_name}",
                "",
                f"- rows: `{summary['rows']}`",
                f"- features: `{summary['features']}`",
                f"- context counts: `{summary['context_counts']}`",
                "",
            ]
        )
    lines.extend(["## Within-Set Feature Separation", ""])
    for set_name, result in report["within_set"].items():
        lines.append(
            f"- `{set_name}`: balanced accuracy `{result['observed_balanced_accuracy']}`, "
            f"shuffle p95 `{result['shuffled_p95']}`, p `{result['p_value']}`, supported `{result['supported']}`"
        )
    lines.extend(["", "## Base-To-Set Transfer", ""])
    for key, result in report["transfer"].items():
        lines.append(
            f"- `{key}`: balanced accuracy `{result['observed_balanced_accuracy']}`, "
            f"shuffle p95 `{result['shuffled_p95']}`, p `{result['p_value']}`, supported `{result['supported']}`"
        )
    lines.extend(["", "## Feature Lift Recurrence", ""])
    for key, result in report["lift_recurrence"].items():
        lines.append(
            f"- `{key}`: cosine `{result['cosine']}`, top-feature jaccard `{result['top_feature_overlap']['jaccard']}`, "
            f"shared top features `{result['top_feature_overlap']['intersection_features']}`"
        )
    lines.extend(["", "## Training History", ""])
    for row in report["training_history"]:
        lines.append(
            f"- epoch `{int(row['epoch'])}`: loss `{row['loss']:.6f}`, mse `{row['mse']:.6f}`, l1 `{row['l1']:.6f}`"
        )
    lines.extend(["", "## Exports", ""])
    for key, value in report["exports"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Next Gates", ""])
    for item in report["next_gates"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    require_inputs()
    OUT.mkdir(parents=True, exist_ok=True)
    dense_sets = [load_gemma_set(name, path) for name, path in SETS.items()]
    base = next(item for item in dense_sets if item.name == "base")
    model, history, mean, std = train_sae(base.points)
    encoded_sets = [EncodedSet(item.name, encode(model, item.points, mean, std), item.labels) for item in dense_sets]
    by_name = {encoded.name: encoded for encoded in encoded_sets}

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "state_dict": model.state_dict(),
            "mean": mean,
            "std": std,
            "config": {
                "model": "gemma",
                "input_dim": int(mean.shape[0]),
                "latent_dim": LATENT_DIM,
                "epochs": EPOCHS,
                "max_per_group": MAX_PER_GROUP,
                "seed": SEED,
            },
            "training_history": history,
        },
        MODEL_PATH,
    )

    within = {encoded.name: validate_within(encoded) for encoded in encoded_sets}
    transfer = {
        "base_to_rerun_02": validate_transfer(by_name["base"], by_name["rerun_02"]),
        "base_to_prompt_set_02": validate_transfer(by_name["base"], by_name["prompt_set_02"]),
    }
    lifts = {name: lift_vector(encoded) for name, encoded in by_name.items()}
    lift_recurrence = {}
    for target in ("rerun_02", "prompt_set_02"):
        lift_recurrence[f"base_to_{target}"] = {
            "cosine": round(cosine(lifts["base"], lifts[target]), 9),
            "top_feature_overlap": top_feature_overlap(lifts["base"], lifts[target], top_k=10),
        }

    recurrence_supported = (
        within["base"]["supported"]
        and within["rerun_02"]["supported"]
        and within["prompt_set_02"]["supported"]
        and transfer["base_to_rerun_02"]["supported"]
        and transfer["base_to_prompt_set_02"]["supported"]
    )
    status = "sae_gemma_recurrence_supported" if recurrence_supported else "sae_gemma_recurrence_partial"
    profiles_path = OUT / "v8_sae_gemma_recurrence_feature_profiles.csv"
    write_profiles(encoded_sets, profiles_path)
    sample = {
        encoded.name: {
            "rows": int(encoded.z.shape[0]),
            "features": int(encoded.z.shape[1]),
            "context_counts": dict(Counter(encoded.labels["context_label"].tolist())),
            "model_counts": dict(Counter(encoded.labels["model"].tolist())),
        }
        for encoded in encoded_sets
    }
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "clean_read": (
            "Gemma is now integrated as a model-native SAE branch. The Gemma SAE recurrence run trains on real Gemma base dense V8 activations and carries the locked Gemma encoder into rerun_02 and prompt_set_02, giving the next gates a third-model SAE recurrence surface alongside GLM / Hermes."
        ),
        "state_config": {
            "model": "gemma",
            "input_dim": int(mean.shape[0]),
            "latent_dim": LATENT_DIM,
            "epochs": EPOCHS,
            "max_per_group": MAX_PER_GROUP,
            "seed": SEED,
        },
        "sets": {name: str(path.relative_to(ROOT)) for name, path in SETS.items()},
        "sample": sample,
        "within_set": within,
        "transfer": transfer,
        "lift_recurrence": lift_recurrence,
        "training_history": history,
        "exports": {
            "feature_profiles": str(profiles_path.relative_to(ROOT)),
            "sae_state": str(MODEL_PATH.relative_to(ROOT)),
        },
        "next_gates": [
            "run SAE feature-edge recurrence with GLM / Hermes plus the Gemma-native branch",
            "run direct SAE feature/circuit ablations across recurrent branches",
            "run MLP depth recurrence after SAE recurrence is logged",
            "move to Nest 2D allostery, 2E PFAS safety, 2F materials, and 2G descriptor/model controls",
        ],
    }
    json_path = OUT / "v8_sae_gemma_recurrence_validation_report.json"
    md_path = OUT / "v8_sae_gemma_recurrence_validation_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_report(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
