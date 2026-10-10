#!/usr/bin/env python3
"""Stdlib regression checks for the facial-animation integration boundary."""
from __future__ import annotations

import tempfile
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BRIDGE = ROOT / "tools" / "character" / "facial_animation_bridge.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        source = root / "prepared.blend"
        output = root / "rigged.blend"
        report = root / "profile.json"
        source.write_bytes(b"fixture")
        result = subprocess.run([
            sys.executable, str(BRIDGE),
            "--blender", "blender",
            "--input", str(source),
            "--out", str(output),
            "--json", str(report),
            "--dry-run",
        ], text=True, capture_output=True)
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            return 1
        manifest = report.with_suffix(report.suffix + ".bridge.json")
        text = manifest.read_text(encoding="utf-8")
        for required in [
            '"upstream": "mdj128/facial-animation"',
            '"upstreamCommit": "5bd659df62fc4877be3183964cea1268d86ecf93"',
            '"canonicalSourceMutated": false',
            '"status": "PLANNED"',
        ]:
            if required not in text:
                print("FAIL: missing %s" % required)
                return 1
    print("PASS: facial-animation bridge dry-run contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
