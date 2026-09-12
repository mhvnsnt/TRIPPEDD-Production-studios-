#!/usr/bin/env python3
"""Inspect an image artifact with optional OpenImageIO support.

This proves image readability/metadata only. It never grants production PASS,
visual QC, or physical QC. The exact file hash remains the authoritative byte
identity in the render evidence receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def native_png(path: Path) -> dict[str, object]:
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("unsupported or truncated PNG")
    width, height = struct.unpack(">II", header[16:24])
    return {"format": "png", "width": width, "height": height}


def oiio_inspect(path: Path) -> dict[str, object] | None:
    if importlib.util.find_spec("OpenImageIO") is None:
        return None
    import OpenImageIO as oiio  # type: ignore
    inp = oiio.ImageInput.open(str(path))
    if inp is None:
        raise ValueError(f"OpenImageIO could not open artifact: {path}")
    try:
        spec = inp.spec()
        return {
            "format": path.suffix.lower().lstrip("."),
            "width": int(spec.width),
            "height": int(spec.height),
            "channels": int(spec.nchannels),
            "format_description": str(spec.format),
            "oiio": True,
        }
    finally:
        inp.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, required=True)
    args = parser.parse_args()
    image = args.image.resolve()
    if not image.is_file():
        raise SystemExit(f"IMAGE_ARTIFACT: BLOCKED — missing artifact: {image}")
    try:
        inspection = oiio_inspect(image)
        backend = "OpenImageIO" if inspection is not None else "native-header"
        if inspection is None:
            inspection = native_png(image)
        result = {
            "schema": "trippedd.image-artifact-inspection/v1",
            "status": "INSPECTED",
            "evidence_status": "NOT_ATTEMPTED",
            "backend": backend,
            "path": str(image),
            "bytes": image.stat().st_size,
            "sha256": sha256(image),
            "inspection": inspection,
            "policy": {
                "artifact_identity_is_sha256": True,
                "inspection_is_not_visual_qc": True,
                "inspection_is_not_physical_qc": True,
                "inspection_is_not_production_approval": True,
            },
        }
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print(f"IMAGE_ARTIFACT: BLOCKED — {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
