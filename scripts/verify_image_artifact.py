#!/usr/bin/env python3
"""Inspect an image artifact with the open-source image stack.

This proves readability/metadata only. It never grants production PASS, visual
QC, or physical QC. Exact byte identity remains the SHA-256 in the receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import struct
import subprocess
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


def oiio_cli_inspect(path: Path) -> dict[str, object] | None:
    tool = shutil.which("iinfo") or shutil.which("oiiotool")
    if not tool:
        return None
    name = Path(tool).name
    command = [tool, "-v", str(path)] if name == "iinfo" else [tool, "--info", str(path)]
    proc = subprocess.run(command, capture_output=True, text=True, timeout=15)
    output = ((proc.stdout or "") + (proc.stderr or "")).strip()
    if proc.returncode != 0:
        raise ValueError(f"{name} could not decode artifact: {output[-2000:]}")
    return {"tool": name, "oiio_cli": True, "output": output[-8000:]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, required=True)
    args = parser.parse_args()
    image = args.image.resolve()
    if not image.is_file() or image.stat().st_size == 0:
        raise SystemExit(f"IMAGE_ARTIFACT: BLOCKED — missing or empty artifact: {image}")
    try:
        inspection = oiio_inspect(image)
        backend = "OpenImageIO"
        if inspection is None:
            inspection = oiio_cli_inspect(image)
            backend = "OpenImageIO-CLI"
        if inspection is None:
            inspection = native_png(image)
            backend = "native-format-check"
            status = "FORMAT_CHECK_ONLY"
        else:
            status = "INSPECTED"
        result = {
            "schema": "trippedd.image-artifact-inspection/v2",
            "status": status,
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
                "native_fallback_is_not_decode_evidence": True,
            },
        }
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print(f"IMAGE_ARTIFACT: BLOCKED — {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
