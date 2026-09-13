#!/usr/bin/env python3
"""Deterministic rigid component registration for canonical character assembly.

This is intentionally small and dependency-light. It performs a Kabsch/Procrustes
rigid fit from corresponding landmarks, then fails closed when the fit exceeds
explicit RMS/max residual gates. It does not edit meshes. An optional Open3D
refinement belongs in a later adapter and must never replace this measured
landmark authority.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def kabsch(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Return 4x4 rigid transform mapping source landmarks to target landmarks."""
    if source.shape != target.shape or source.ndim != 2 or source.shape[1] != 3:
        raise ValueError("source/target must both be Nx3 with identical shape")
    if source.shape[0] < 3:
        raise ValueError("at least three corresponding landmarks are required")

    src_centroid = source.mean(axis=0)
    dst_centroid = target.mean(axis=0)
    src = source - src_centroid
    dst = target - dst_centroid
    h = src.T @ dst
    u, _, vt = np.linalg.svd(h)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1.0
        r = vt.T @ u.T
    t = dst_centroid - r @ src_centroid

    transform = np.eye(4, dtype=np.float64)
    transform[:3, :3] = r
    transform[:3, 3] = t
    return transform


def apply(transform: np.ndarray, points: np.ndarray) -> np.ndarray:
    return (points @ transform[:3, :3].T) + transform[:3, 3]


def metrics(source: np.ndarray, target: np.ndarray, transform: np.ndarray) -> dict[str, float]:
    aligned = apply(transform, source)
    residual = np.linalg.norm(aligned - target, axis=1)
    return {
        "landmark_count": int(len(residual)),
        "rms_residual": float(np.sqrt(np.mean(residual ** 2))),
        "max_residual": float(np.max(residual)),
        "mean_residual": float(np.mean(residual)),
    }


def register(
    source: np.ndarray,
    target: np.ndarray,
    *,
    max_rms: float,
    max_residual: float,
) -> dict[str, Any]:
    transform = kabsch(source, target)
    result = metrics(source, target, transform)
    result["pass"] = bool(
        result["rms_residual"] <= max_rms
        and result["max_residual"] <= max_residual
    )
    result["transform"] = transform.tolist()
    result["thresholds"] = {
        "max_rms": float(max_rms),
        "max_residual": float(max_residual),
    }
    if not result["pass"]:
        raise SystemExit(json.dumps({"status": "FAIL", **result}, indent=2))
    return {"status": "PASS", **result}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Nx3 .npy source landmarks")
    parser.add_argument("--target", required=True, type=Path, help="Nx3 .npy target landmarks")
    parser.add_argument("--output", required=True, type=Path, help="JSON receipt path")
    parser.add_argument("--max-rms", required=True, type=float)
    parser.add_argument("--max-residual", required=True, type=float)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--target-id", required=True)
    args = parser.parse_args()

    source = np.asarray(np.load(args.source), dtype=np.float64)
    target = np.asarray(np.load(args.target), dtype=np.float64)
    result = register(
        source,
        target,
        max_rms=args.max_rms,
        max_residual=args.max_residual,
    )
    result["source_id"] = args.source_id
    result["target_id"] = args.target_id
    result["source_sha256"] = __import__("hashlib").sha256(args.source.read_bytes()).hexdigest()
    result["target_sha256"] = __import__("hashlib").sha256(args.target.read_bytes()).hexdigest()
    result["authority"] = "landmark_kabsch"
    result["mesh_mutated"] = False
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
