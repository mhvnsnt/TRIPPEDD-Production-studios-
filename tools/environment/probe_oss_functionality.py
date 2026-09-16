#!/usr/bin/env python3
"""Run bounded functional probes for installed OSS production tools.

Capability discovery is not enough: this probe exercises tiny real operations
when the tools are installed. It never reads production evidence as PASS and
never promotes a render, QC result, or approval.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> dict[str, object]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=30)
        return {"status": "PASS" if p.returncode == 0 else "FAIL", "returncode": p.returncode,
                "stdout": p.stdout[-2000:], "stderr": p.stderr[-2000:]}
    except Exception as exc:
        return {"status": "FAIL", "returncode": None, "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(".artifacts/evidence/oss_functional_probes.json"))
    args = parser.parse_args()
    results: dict[str, object] = {}
    with tempfile.TemporaryDirectory(prefix="trippedd-oss-probe-") as td:
        root = Path(td)
        png = root / "probe.png"
        # Minimal valid 1x1 RGBA PNG. Generated locally; never production evidence.
        png.write_bytes(bytes.fromhex(
            "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
            "0000000d49444154789c63f8cfc0f01f00050001ff89993d1d0000000049454e44ae426082"
        ))
        iinfo = shutil.which("iinfo")
        idiff = shutil.which("idiff")
        oiiotool = shutil.which("oiiotool")
        results["OpenImageIO"] = {
            "status": "AVAILABLE" if any((iinfo, idiff, oiiotool)) else "UNAVAILABLE",
            "functional_probe": {
                "iinfo": run([iinfo, str(png)]) if iinfo else {"status": "UNAVAILABLE"},
                "idiff_self": run([idiff, str(png), str(png)]) if idiff else {"status": "UNAVAILABLE"},
                "oiiotool_info": run([oiiotool, "--info", str(png)]) if oiiotool else {"status": "UNAVAILABLE"},
            },
        }
        blender = shutil.which("blender")
        results["Blender"] = {"status": "AVAILABLE" if blender else "UNAVAILABLE",
                               "functional_probe": run([blender, "--version"]) if blender else {"status": "UNAVAILABLE"}}
        results["OpenCue"] = {"status": "AVAILABLE" if shutil.which("cueadmin") else "UNAVAILABLE",
                               "functional_probe": run([shutil.which("cueadmin"), "--help"]) if shutil.which("cueadmin") else {"status": "UNAVAILABLE"}}
        results["OpenRV"] = {"status": "AVAILABLE" if shutil.which("rv") else "UNAVAILABLE",
                              "functional_probe": run([shutil.which("rv"), "-version"]) if shutil.which("rv") else {"status": "UNAVAILABLE"}}
        results["xSTUDIO"] = {"status": "AVAILABLE" if shutil.which("xstudio") else "UNAVAILABLE",
                               "functional_probe": run([shutil.which("xstudio"), "--version"]) if shutil.which("xstudio") else {"status": "UNAVAILABLE"}}

    payload = {
        "schema": "trippedd.oss-functional-probes/v1",
        "status": "PROBED",
        "evidence_status": "NOT_ATTEMPTED",
        "results": results,
        "policy": {
            "synthetic_probe_artifact_only": True,
            "functional_probe_is_not_production_evidence": True,
            "functional_probe_is_not_visual_qc": True,
            "functional_probe_is_not_physical_qc": True,
            "tool_availability_never_promotes_production": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
