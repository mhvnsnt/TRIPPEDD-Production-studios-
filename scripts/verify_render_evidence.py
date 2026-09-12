#!/usr/bin/env python3
"""Verify that a render receipt is backed by the exact bytes it claims.

This is a post-render evidence check, not visual QC. It proves that a receipt
points at a real artifact, that the artifact is retrievable, and that its
SHA-256/format metadata match the bytes on disk. It never grants visual or
physical PASS by itself.

Usage:
    python scripts/verify_render_evidence.py --receipt path/to/receipt.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

EXPECTED_SCHEMA = "trippedd.render-evidence/v1"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_PREFIX = b"\xff\xd8\xff"


def fail(message: str) -> None:
    raise SystemExit(f"RENDER_EVIDENCE: FAIL — {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.is_file(), f"missing receipt: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read receipt: {exc}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        fail(f"cannot read rendered bytes: {exc}")
    return digest.hexdigest()


def inspect_image(path: Path) -> tuple[str, int, int]:
    """Return (format, width, height) using container-level format headers."""
    try:
        with path.open("rb") as handle:
            header = handle.read(32)
    except OSError as exc:
        fail(f"cannot inspect rendered bytes: {exc}")

    if header.startswith(PNG_SIGNATURE):
        require(len(header) >= 24, "PNG is truncated before IHDR dimensions")
        require(header[12:16] == b"IHDR", "PNG has no valid IHDR chunk")
        width, height = struct.unpack(">II", header[16:24])
        return "png", width, height

    if header.startswith(JPEG_PREFIX):
        # JPEG dimensions require marker walking; reject them here rather than
        # guessing. The evidence verifier deliberately supports only formats
        # whose dimensions it can prove from the bytes it reads.
        fail("JPEG evidence is not supported yet; use PNG for first-shot stills")

    fail("rendered artifact is not a supported PNG image")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    receipt_path = args.receipt.resolve()
    receipt = load_json(receipt_path)

    require(receipt.get("schema") == EXPECTED_SCHEMA, "unsupported render-evidence schema")
    require(receipt.get("rendered") is True, "receipt does not assert rendered=true")
    require(receipt.get("shot_id"), "receipt is missing shot_id")
    require(receipt.get("scene_id"), "receipt is missing scene_id")
    require(receipt.get("world_id"), "receipt is missing world_id")
    require(receipt.get("executor") == "Blender", "executor must be Blender")

    artifact = receipt.get("artifact", {})
    output = artifact.get("path")
    expected_hash = artifact.get("sha256")
    expected_size = artifact.get("bytes")
    expected_format = artifact.get("format")
    expected_width = artifact.get("width")
    expected_height = artifact.get("height")

    require(isinstance(output, str) and output, "receipt is missing artifact.path")
    require(isinstance(expected_hash, str) and len(expected_hash) == 64, "receipt is missing artifact.sha256")
    require(isinstance(expected_size, int) and expected_size > 0, "receipt is missing artifact.bytes")
    require(expected_format == "png", "artifact.format must be png")
    require(isinstance(expected_width, int) and expected_width > 0, "receipt is missing artifact.width")
    require(isinstance(expected_height, int) and expected_height > 0, "receipt is missing artifact.height")

    output_path = Path(output)
    if not output_path.is_absolute():
        output_path = (receipt_path.parent / output_path).resolve()
    require(output_path.is_file(), f"rendered artifact is not retrievable: {output_path}")

    actual_size = output_path.stat().st_size
    require(actual_size == expected_size, f"artifact byte count mismatch: receipt={expected_size}, actual={actual_size}")

    actual_hash = sha256(output_path)
    require(actual_hash == expected_hash, f"artifact SHA-256 mismatch: receipt={expected_hash}, actual={actual_hash}")

    actual_format, actual_width, actual_height = inspect_image(output_path)
    require(actual_format == expected_format, f"artifact format mismatch: receipt={expected_format}, actual={actual_format}")
    require(actual_width == expected_width, f"artifact width mismatch: receipt={expected_width}, actual={actual_width}")
    require(actual_height == expected_height, f"artifact height mismatch: receipt={expected_height}, actual={actual_height}")

    print("RENDER_EVIDENCE: PASS")
    print(f"  shot: {receipt['shot_id']}")
    print(f"  scene: {receipt['scene_id']}")
    print(f"  artifact: {output_path}")
    print(f"  sha256: {actual_hash}")
    print(f"  dimensions: {actual_width}x{actual_height}")
    print("  visual_qc: NOT_EVALUATED")
    print("  physical_qc: NOT_EVALUATED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
