#!/usr/bin/env python3
"""Small stdlib-only regression checks for depth/fracture evidence gate."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "tools" / "oss" / "depth_fracture_gate.py"

BASE = {
    "schema": "trippedd.oss-physics-evidence/v1",
    "status": "PASS",
    "upstreamCommit": "a" * 40,
    "inputSha256": "b" * 64,
    "outputSha256": "c" * 64,
    "visualEvidenceSha256": "d" * 64,
    "canonicalSourceMutated": False,
    "exactCommand": "blender --background scene.blend --python run.py",
}


def run(payload: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "receipt.json"
        p.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(["python3", str(GATE), str(p)], text=True, capture_output=True)


def main() -> int:
    depth = {**BASE, "lane": "midas_depth", "authority": "DERIVATIVE_DEPTH_EVIDENCE", "weightsLicenseStatus": "SEPARATELY_VERIFIED", "depthErrorQc": {"rmse": 0.1}}
    fracture = {**BASE, "lane": "shatter_it", "authority": "DERIVATIVE_FRACTURE_OUTPUT", "blenderVersion": "5.0.0", "dependencyLicenseInventory": [], "deterministic": True, "fragmentCount": 12, "collisionSmokeTest": True}
    bad = {**depth, "weightsLicenseStatus": "UNKNOWN"}
    for name, payload, expected in (("depth", depth, 0), ("fracture", fracture, 0), ("bad-depth", bad, 1)):
        result = run(payload)
        if result.returncode != expected:
            print(f"FAIL: {name}: rc={result.returncode} stdout={result.stdout!r} stderr={result.stderr!r}")
            return 1
    print("PASS: depth/fracture gate regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
