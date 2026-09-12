#!/usr/bin/env python3
"""Fail-closed preflight for the real MARS_LOD2 production GLB.

This gate deliberately does not fall back to MARS_source.glb, a donor head,
or a generated substitute. The landmark/socket/rig/blink pipeline is only
truthful when the requested production asset is actually present.

Usage:
  python tools/character/validate_mars_lod2_input.py \
    --asset assets/source_models/MARS_LOD2.glb \
    --output artifacts/evidence/mars_lod2_input_preflight.json

An expected SHA-256 may be supplied once the canonical LOD2 bytes have been
pinned. Until then, the gate verifies presence, GLB container validity, and
that the path is the production LOD2 path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

EXPECTED_PATH = Path("assets/source_models/MARS_LOD2.glb")
FORBIDDEN_FALLBACKS = {
    "MARS_source.glb",
    "MARS_source_model.glb",
    "MARS_CANONICAL.glb",
}


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--asset", default=str(EXPECTED_PATH))
    ap.add_argument("--output", required=True)
    ap.add_argument("--expected-sha256", default="")
    return ap.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inspect_glb(path: Path) -> dict:
    with path.open("rb") as f:
        header = f.read(12)
    if len(header) != 12:
        raise RuntimeError("GLB header is truncated")
    magic, version, length = struct.unpack("<4sII", header)
    if magic != b"glTF":
        raise RuntimeError("file does not have the glTF binary magic")
    if version != 2:
        raise RuntimeError(f"unsupported GLB version {version}; expected 2")
    if length != path.stat().st_size:
        raise RuntimeError(
            f"GLB header length {length} does not match file size {path.stat().st_size}"
        )
    return {"glb_magic": "glTF", "glb_version": version, "declared_bytes": length}


def main() -> int:
    a = parse_args()
    asset = Path(a.asset).resolve()
    out = Path(a.output)
    report = {
        "schema": "god-molecule.mars-lod2-input-preflight.v1",
        "asset_id": "MARS_LOD2",
        "required_relative_path": str(EXPECTED_PATH),
        "requested_path": str(asset),
        "identity": "MARS_CANONICAL",
        "substitution_allowed": False,
        "status": "FAIL",
    }

    try:
        if Path(a.asset) != EXPECTED_PATH:
            raise RuntimeError(
                f"wrong production path: {a.asset!r}; expected {str(EXPECTED_PATH)!r}"
            )
        if asset.name in FORBIDDEN_FALLBACKS:
            raise RuntimeError(f"fallback asset is forbidden: {asset.name}")
        if not asset.is_file():
            raise RuntimeError(
                "MARS_LOD2 production asset is absent from the checkout; "
                "do not substitute MARS_source.glb or donor/generated media"
            )
        report.update({
            "bytes": asset.stat().st_size,
            "sha256": sha256(asset),
            "container": inspect_glb(asset),
        })
        if a.expected_sha256 and report["sha256"] != a.expected_sha256.lower():
            raise RuntimeError(
                f"SHA-256 mismatch: expected {a.expected_sha256.lower()}, "
                f"got {report['sha256']}"
            )
        report["status"] = "PASS"
        print("MARS_LOD2_INPUT: PASS")
        print(json.dumps(report, indent=2))
    except Exception as exc:
        report["error"] = str(exc)
        print("MARS_LOD2_INPUT: FAIL", file=sys.stderr)
        print(json.dumps(report, indent=2), file=sys.stderr)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return 2

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
