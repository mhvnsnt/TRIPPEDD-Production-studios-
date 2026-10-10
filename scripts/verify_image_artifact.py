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
import zlib
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def native_png(path: Path) -> dict[str, object]:
    """Perform a conservative structural PNG check without claiming full decode.

    This fallback is deliberately weaker than OpenImageIO, but it must not accept
    a forged signature/header. It validates chunk boundaries, CRCs, IHDR, IDAT's
    zlib stream, and IEND. Pixel semantics remain FORMAT_CHECK_ONLY evidence.
    """
    data = path.read_bytes()
    signature = b"\x89PNG\r\n\x1a\n"
    if len(data) < 8 or data[:8] != signature:
        raise ValueError("unsupported or truncated PNG")

    offset = 8
    ihdr: tuple[int, int, int, int, int, int, int] | None = None
    idat = bytearray()
    saw_iend = False
    chunk_count = 0

    while offset < len(data):
        if len(data) - offset < 12:
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            raise ValueError("PNG chunk exceeds file bounds")
        chunk_data = data[offset + 8 : offset + 8 + length]
        stored_crc = struct.unpack(">I", data[offset + 8 + length : chunk_end])[0]
        calculated_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if stored_crc != calculated_crc:
            raise ValueError(f"PNG CRC mismatch in {chunk_type.decode('latin1')}")

        chunk_count += 1
        if chunk_type == b"IHDR":
            if length != 13 or ihdr is not None:
                raise ValueError("invalid PNG IHDR")
            ihdr = struct.unpack(">IIBBBBB", chunk_data)
            width, height, bit_depth, color_type, compression, filtering, interlace = ihdr
            if width == 0 or height == 0:
                raise ValueError("PNG dimensions must be nonzero")
            if compression != 0 or filtering != 0 or interlace not in (0, 1):
                raise ValueError("unsupported PNG encoding parameters")
            valid_depths = {
                0: {1, 2, 4, 8, 16},
                2: {8, 16},
                3: {1, 2, 4, 8},
                4: {8, 16},
                6: {8, 16},
            }
            if color_type not in valid_depths or bit_depth not in valid_depths[color_type]:
                raise ValueError("invalid PNG color type/bit depth")
        elif chunk_type == b"IDAT":
            if ihdr is None:
                raise ValueError("PNG IDAT precedes IHDR")
            idat.extend(chunk_data)
        elif chunk_type == b"IEND":
            if length != 0 or ihdr is None or not idat:
                raise ValueError("invalid PNG IEND/IDAT structure")
            if chunk_end != len(data):
                raise ValueError("PNG has data after IEND")
            saw_iend = True
            break

        offset = chunk_end

    if ihdr is None or not saw_iend or not idat:
        raise ValueError("PNG missing required IHDR/IDAT/IEND")

    try:
        decompressed = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise ValueError(f"PNG IDAT zlib stream is invalid: {exc}") from exc
    if not decompressed:
        raise ValueError("PNG decoded scanline stream is empty")

    width, height, bit_depth, color_type, _compression, _filtering, interlace = ihdr
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color_type]
    bits_per_pixel = channels * bit_depth
    row_bytes = (width * bits_per_pixel + 7) // 8
    if interlace == 0:
        expected = height * (row_bytes + 1)
        if len(decompressed) != expected:
            raise ValueError("PNG scanline data length does not match dimensions")
    else:
        # Adam7 has a more complex row layout; the zlib stream is still proven
        # structurally valid, but we intentionally do not claim pixel decoding.
        pass

    return {
        "format": "png",
        "width": width,
        "height": height,
        "chunks": chunk_count,
        "idat_zlib_valid": True,
        "native_structural_check": True,
    }


def oiio_inspect(path: Path) -> dict[str, object] | None:
    if importlib.util.find_spec("OpenImageIO") is None:
        return None
    import OpenImageIO as oiio  # type: ignore
    config = oiio.ImageSpec()
    config["imageinput:strict"] = 1
    inp = oiio.ImageInput.open(str(path), config)
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
