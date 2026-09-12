#!/usr/bin/env python3
"""Probe optional open-source production tools without turning absence into failure."""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get("OSS_PROBE_OUTPUT", ROOT / ".artifacts" / "evidence" / "oss_capabilities.json"))

PYTHON_MODULES = {"opentimelineio": "OpenTimelineIO", "numpy": "NumPy"}
BINARIES = {
    "blender": "Blender",
    "ffmpeg": "FFmpeg",
    "oiiotool": "OpenImageIO",
    "natron": "Natron",
    "cueadmin": "OpenCue",
    "colmap": "COLMAP",
}


def version_for(binary: str) -> str | None:
    path = shutil.which(binary)
    if not path:
        return None
    for args in (("--version",), ("-version",)):
        try:
            proc = subprocess.run([path, *args], capture_output=True, text=True, timeout=8)
            text = (proc.stdout or proc.stderr).strip().splitlines()
            if text:
                return text[0][:240]
        except (OSError, subprocess.SubprocessError):
            pass
    return "AVAILABLE"


result = {
    "status": "CAPABILITY_PROBE",
    "fail_closed": True,
    "python": {},
    "binaries": {},
}

for module, label in PYTHON_MODULES.items():
    result["python"][label] = {
        "module": module,
        "available": importlib.util.find_spec(module) is not None,
    }

for binary, label in BINARIES.items():
    value = version_for(binary)
    result["binaries"][label] = {
        "binary": binary,
        "available": value is not None,
        "version": value,
    }

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
