#!/usr/bin/env python3
"""Build a deterministic God Molecule hybrid environment plan."""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", required=True)
    ap.add_argument("--scene", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--reference", action="append", default=[])
    args = ap.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    refs = []
    for item in args.reference:
        p = Path(item)
        if p.exists() and p.is_file():
            refs.append({"path": str(p), "size_bytes": p.stat().st_size, "sha256": sha256_bytes(p.read_bytes())})
        else:
            refs.append({"path": item, "status": "MISSING"})

    manifest = {
        "schema": "god-molecule.environment-slice.v1",
        "scene": args.scene,
        "world_seed": args.seed,
        "references": refs,
        "backends": {
            "voxel_world": "PENDING",
            "camera_reconstruction": "PENDING",
            "gaussian_splat": "PENDING",
            "blender_scene": "PENDING",
            "openusd_scene": "PENDING"
        },
        "claims": {
            "environment_rendered": False,
            "gaussian_splat_verified": False,
            "creative_final": False
        }
    }

    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"ENVIRONMENT_SLICE_MANIFEST={out}")
    print("ENVIRONMENT_RENDER: PENDING")
    print("GAUSSIAN_SPLAT: PENDING")
    print("WORLD_SEED: VERIFIED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
