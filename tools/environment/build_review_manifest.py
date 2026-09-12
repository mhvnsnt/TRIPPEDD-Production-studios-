#!/usr/bin/env python3
"""Build a deterministic review manifest for OpenRV/xSTUDIO-style viewers.

The manifest is a navigation/review aid only. It references the exact published
pixel artifacts and their SHA-256 values; it never creates visual or physical QC.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=Path, required=True)
    p.add_argument("--root", type=Path, default=None)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    index_path = args.index.resolve()
    index = json.loads(index_path.read_text(encoding="utf-8"))
    root = (args.root or index_path.parent).resolve()
    frames = []
    for item in index.get("frames", []):
        rel = Path(item["repoPath"])
        path = root / rel.name if root.name == rel.parent.name else root / rel
        if not path.is_file():
            # In CI, --root is normally the repository root; keep the manifest
            # fail-closed rather than inventing a viewer path.
            raise SystemExit(f"REVIEW_MANIFEST: BLOCKED — missing pixel artifact: {path}")
        actual = sha256(path)
        expected = item.get("sha256")
        if expected and actual != expected:
            raise SystemExit(
                f"REVIEW_MANIFEST: BLOCKED — SHA mismatch for {rel}: expected={expected} actual={actual}"
            )
        frames.append({
            "path": str(rel),
            "absolute_path": str(path),
            "sha256": actual,
            "pose": item.get("pose"),
            "camera": item.get("camera"),
            "publishedPx": item.get("publishedPx"),
        })

    result = {
        "schema": "trippedd.review-manifest/v1",
        "status": "READY_FOR_REVIEW",
        "evidence_status": "NOT_ATTEMPTED",
        "source_index": str(index_path),
        "set": index.get("set"),
        "frames": frames,
        "viewer_targets": ["OpenRV", "xSTUDIO"],
        "policy": {
            "review_manifest_is_not_visual_qc": True,
            "review_manifest_is_not_physical_qc": True,
            "exact_pixel_sha256_required": True,
            "visual_fail_remains_fail": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
