#!/usr/bin/env python3
"""Functionally probe an already-rendered image without promoting it to evidence.

The probe proves that an actual artifact can be decoded and inspected through an
available open-source image stack. It never changes the render receipt or QC state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_python(path: Path) -> dict[str, object] | None:
    try:
        import OpenImageIO as oiio  # type: ignore
    except Exception:
        return None
    try:
        image = oiio.ImageInput.open(str(path))
        if image is None:
            return {"backend": "OpenImageIO-Python", "status": "DECODE_FAILED", "error": oiio.geterror()}
        spec = image.spec()
        metadata = {}
        for key in ("compression", "oiio:ColorSpace", "Software"):
            try:
                value = spec.getattribute(key)
                if value is not None:
                    metadata[key] = str(value)
            except Exception:
                pass
        image.close()
        return {
            "backend": "OpenImageIO-Python",
            "status": "FUNCTIONAL_PROBE",
            "width": int(spec.width),
            "height": int(spec.height),
            "channels": int(spec.nchannels),
            "format": str(spec.format),
            "metadata": metadata,
        }
    except Exception as exc:
        return {"backend": "OpenImageIO-Python", "status": "ERROR", "error": str(exc)}


def probe_iinfo(path: Path) -> dict[str, object] | None:
    tool = shutil.which("iinfo") or shutil.which("oiiotool")
    if not tool:
        return None
    command = [tool, "-v", str(path)] if Path(tool).name == "iinfo" else [tool, "--info", str(path)]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=15)
        text = (proc.stdout + proc.stderr).strip()
        return {
            "backend": Path(tool).name,
            "status": "FUNCTIONAL_PROBE" if proc.returncode == 0 else "DECODE_FAILED",
            "returncode": proc.returncode,
            "output": text[-8000:],
        }
    except (OSError, subprocess.SubprocessError) as exc:
        return {"backend": Path(tool).name, "status": "ERROR", "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    path = Path(args.artifact).resolve()
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"ARTIFACT_PROBE: BLOCKED — missing or empty artifact: {path}")

    result: dict[str, object] = {
        "schema": "trippedd.render-artifact-probe/v1",
        "status": "FUNCTIONAL_PROBE",
        "evidence_status": "NOT_ATTEMPTED",
        "artifact": {
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        },
        "policy": {
            "probe_is_not_evidence": True,
            "does_not_modify_render_receipt": True,
            "does_not_perform_visual_qc": True,
            "does_not_perform_physical_qc": True,
        },
        "backends": [],
    }
    for probe in (probe_python(path), probe_iinfo(path)):
        if probe is not None:
            result["backends"].append(probe)

    if not result["backends"]:
        result["status"] = "NO_PROBE_BACKEND"
        result["error"] = "Neither OpenImageIO Python nor iinfo/oiiotool is available"
    elif not any(item.get("status") == "FUNCTIONAL_PROBE" for item in result["backends"]):
        result["status"] = "DECODE_FAILED"

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "FUNCTIONAL_PROBE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
