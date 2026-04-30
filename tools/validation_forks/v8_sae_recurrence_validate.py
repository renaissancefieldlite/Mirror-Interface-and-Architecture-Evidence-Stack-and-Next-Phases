#!/usr/bin/env python3
"""Validate SAE recurrence across base, rerun_02, and prompt_set_02.

The bounded SAE was trained on base GLM / Hermes dense V8 activations. This
runner applies that locked encoder to matching dense exports and tests whether
the sparse feature basis carries context structure across rerun and prompt
surfaces.
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
STATE_PATH = (
    ROOT
    / "artifacts"
    / "validation"
    / "v8_sae_feature_circuit_exports"
    / "sae_models"
    / "v8_sae_bounded_pilot_state.pt"
)
OUT = ROOT / "artifacts" / "validation" / "v8_sae_recurrence_validation"

SEED = 67
MAX_PER_GROUP = 120
BATCH_SIZE = 512
SHUFFLES = 100
CONTEXTS = ("lattice", "neutral", "technical")
SETS = {
    "base": POINT_ROOT / "point_clouds_dense_trajectory",
    "rerun_02": POINT_ROOT / "point_clouds_dense_trajectory_rerun_02",
    "prompt_set_02": POINT_ROOT / "point_clouds_dense_trajectory_prompt_set_02",
}


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


def require_inputs() -> None:
    if not STATE_PATH.exists():
        raise SystemExit(f"SAE state missing: {STATE_PATH}")
    for set_name, directory in SETS.items():
        paths = sorted(directory.glob("*_v8_hidden_point_cloud.npz"))
        present = {path.name.replace("_v8_hidden_point_cloud.npz", "") for path in paths}
        missing = {"glm", "hermes"} - present
        if missing:
            raise SystemExit(f"{set_name} dense input missing {sorted(missing)} in {directory}")


def load_sae() -> tuple[SparseAutoencoder, np.ndarray, np.ndarray, dict[str, Any]]:
    state = torch.load(STATE_PATH, map_location="cpu", weights_only=False)
    mean = np.asarray(state["mean"], dtype=np.float32)
    std = np.asarray(state["std"], dtype=np.float32)
    config = dict(state.get("config", {}))
    latent_dim = int(config.get("latent_dim", 64))
    model = SparseAutoencoder(int(mean.shape[0]), latent_dim)
    model.load_state_dict(state["state_dict"])
    model.eval()
    return model, mean, std, config


def sample_dense_set(set_name: str, directory: Path) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    rng = np.random.default_rng(SEED + abs(hash(set_name)) % 1000)
    sampled_points: list[np.ndarray] = []
    labels: dict[str, list[Any]] = defaultdict(list)
    for path in sorted(directory.glob("*_v8_hidden_point_cloud.npz")):
        model_name = path.name.replace("_v8_hidden_point_cloud.npz", "")
        if model_name not in {"glm", "hermes"}:
            continue
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
                    labels["source_set"].extend([set_name] * take)
                    labels["source_path"].extend([str(path.relative_to(ROOT))] * take)
    if not sampled_points:
        raise RuntimeError(f"No rows sampled for {set_name}")
    return np.vstack(sampled_points).astype(np.float32, copy=False), {k: np.asarray(v) for k, v in labels.items()}


def encode_points(model: SparseAutoencoder, points: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    scaled = ((points - mean) / std).astype(np.float32)
    tensor = torch.from_numpy(scaled)
    outputs = []
    with torch.no_grad():
        for start in range(0, tensor.shape[0], BATCH_SIZE):
            _, z = model(tensor[start : start + BATCH_SIZE])
            outputs.append(z.cpu().numpy().astype(np.float32))
    return np.vstack(outputs)


def encode_sets() -> tuple[list[EncodedSet], dict[str, Any]]:
    model, mean, std, config = load_sae()
    encoded = []
    for set_name, directory in SETS.items():
        points, labels = sample_dense_set(set_name, directory)
        z = encode_points(model, points, mean, std)
        encoded.append(EncodedSet(set_name, z, labels))
    return encoded, config


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
    rng = np.random.default_rng(SEED)
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


def validate_transfer(train: EncodedSet, test: EncodedSet, seed_offset: int) -> dict[str, Any]:
    train_y = train.labels["context_label"]
    test_y = test.labels["context_label"]
    clf = LogisticRegression(max_iter=1000, random_state=SEED)
    clf.fit(train.z, train_y)
    observed = float(balanced_accuracy_score(test_y, clf.predict(test.z)))
    rng = np.random.default_rng(SEED + seed_offset)
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
        "# V8 SAE Recurrence Validation Report",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
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
                f"- context counts: `{summary['context_counts']}`",
                f"- model counts: `{summary['model_counts']}`",
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
    encoded_sets, config = encode_sets()
    by_name = {encoded.name: encoded for encoded in encoded_sets}

    within = {encoded.name: validate_within(encoded) for encoded in encoded_sets}
    transfer = {
        "base_to_rerun_02": validate_transfer(by_name["base"], by_name["rerun_02"], 1),
        "base_to_prompt_set_02": validate_transfer(by_name["base"], by_name["prompt_set_02"], 2),
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
    status = "sae_recurrence_supported" if recurrence_supported else "sae_recurrence_partial"
    profiles_path = OUT / "v8_sae_recurrence_feature_profiles.csv"
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
            "The locked bounded SAE encoder recurs across base, rerun_02, and prompt_set_02 dense V8 exports. "
            "Within-set feature separation and base-trained transfer both beat shuffled-label controls, so the SAE feature layer now has prompt/rerun recurrence support."
            if recurrence_supported
            else "The locked bounded SAE encoder produced recurrence measurements across base, rerun_02, and prompt_set_02. "
            "The report records which recurrence paths beat shuffled controls and which paths need another export or stronger feature/circuit controls."
        ),
        "state_config": config,
        "sets": {name: str(path.relative_to(ROOT)) for name, path in SETS.items()},
        "sample": sample,
        "within_set": within,
        "transfer": transfer,
        "lift_recurrence": lift_recurrence,
        "exports": {
            "feature_profiles": str(profiles_path.relative_to(ROOT)),
        },
        "next_gates": [
            "run direct SAE feature/circuit ablations on the recurrent feature profile",
            "build matched feature-edge recurrence over base, rerun_02, and prompt_set_02",
            "move to Nest 2D allostery after the SAE recurrence/ablation read is logged",
        ],
    }
    json_path = OUT / "v8_sae_recurrence_validation_report.json"
    md_path = OUT / "v8_sae_recurrence_validation_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_report(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
