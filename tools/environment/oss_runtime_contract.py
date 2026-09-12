#!/usr/bin/env python3
"""Resolve the optional OSS stack into an explicit runtime capability contract.

Capability discovery never becomes render or QC evidence. Production evidence
still requires exact artifact retrieval/reopen plus physical and visual gates.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get("OSS_RUNTIME_CONTRACT", ROOT / ".artifacts" / "evidence" / "oss_runtime_contract.json"))

PYTHON_CAPABILITIES = {
    "OpenTimelineIO": "opentimelineio",
    "NumPy": "numpy",
    "OpenImageIO": "OpenImageIO",
    "OpenColorIO": "PyOpenColorIO",
    "MaterialX": "MaterialX",
    "OpenAssetIO": "openassetio",
    "OpenCuePyOutline": "outline",
}

BINARY_CAPABILITIES = {
    "Blender": "blender",
    "FFmpeg": "ffmpeg",
    "OpenImageIO": "oiiotool",
    "OpenColorIO": "ocio",
    "OpenUSD": "usdcat",
    "Open Shading Language": "oslc",
    "OpenVDB": "vdb_print",
    "COLMAP": "colmap",
    "Natron": "Natron",
    "OpenCue": "cueadmin",
    "OpenCueSubmit": "cuesubmit",
    "OpenCueCommand": "cuecmd",
    "OpenCueRun": "pycuerun",
    "Rez": "rez",
    "OpenRV": "rv",
    "xSTUDIO": "xstudio",
}

ENVIRONMENT_CAPABILITIES = {
    "OpenEXR": ("OpenEXR_HOME", "OPENEXR_ROOT"),
    "MaterialX": ("MATERIALX_HOME", "MATERIALX_ROOT"),
    "OpenAssetIO": ("OPENASSETIO_HOME", "OPENASSETIO_ROOT"),
    "CUEBOT": ("CUEBOT_HOSTS",),
}


def command_version(command: str) -> dict[str, object]:
    path = shutil.which(command)
    if not path:
        return {"available": False, "command": command, "path": None, "version": None}
    for args in (("--version",), ("-version",), ("version",)):
        try:
            proc = subprocess.run([path, *args], capture_output=True, text=True, timeout=8)
            text = (proc.stdout or proc.stderr).strip().splitlines()
            if text:
                return {"available": True, "command": command, "path": path, "version": text[0][:240]}
        except (OSError, subprocess.SubprocessError):
            continue
    return {"available": True, "command": command, "path": path, "version": "AVAILABLE"}


def python_module(module: str) -> dict[str, object]:
    try:
        spec = importlib.util.find_spec(module)
    except (ImportError, AttributeError, ValueError):
        spec = None
    return {"available": spec is not None, "module": module, "origin": getattr(spec, "origin", None)}


def env_hint(names: tuple[str, ...]) -> dict[str, object]:
    present = [name for name in names if os.environ.get(name)]
    return {"available": bool(present), "signals": present}


def main() -> int:
    result = {
        "schema_version": 2,
        "status": "CAPABILITY_CONTRACT",
        "fail_closed": True,
        "evidence_status": "NOT_ATTEMPTED",
        "policy": {
            "capability_presence_is_not_evidence": True,
            "reviewer_must_open_exact_artifact_bytes": True,
            "visual_qc_required": True,
            "physical_qc_required_when_applicable": True,
            "proxy_never_canonical": True,
            "opencue_is_dispatcher_not_source_of_truth": True,
        },
        "python": {label: python_module(module) for label, module in PYTHON_CAPABILITIES.items()},
        "binaries": {label: command_version(command) for label, command in BINARY_CAPABILITIES.items()},
        "environment": {label: env_hint(names) for label, names in ENVIRONMENT_CAPABILITIES.items()},
    }
    available = sum(1 for value in result["python"].values() if value["available"])
    available += sum(1 for value in result["binaries"].values() if value["available"])
    hinted = sum(1 for value in result["environment"].values() if value["available"])
    total = len(result["python"]) + len(result["binaries"]) + len(result["environment"])
    result["summary"] = {
        "available_capabilities": available + hinted,
        "declared_capabilities": total,
        "coverage_fraction": round((available + hinted) / total, 4) if total else 0.0,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
