#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tools/oss/physics_runtime_manifest.json"
VERIFY = ROOT / "tools/oss/verify_physics_runtime.py"


def main():
    data = json.loads(MANIFEST.read_text())
    lanes = data["lanes"]
    assert len(lanes) == 3
    assert data["canonical"]["mutationAllowed"] is False
    subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, check=True)

    bad = json.loads(json.dumps(data))
    bad["lanes"][0]["upstreamCommit"] = "floating"
    with tempfile.TemporaryDirectory() as td:
        bad_path = Path(td) / "physics_runtime_manifest.json"
        bad_path.write_text(json.dumps(bad), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(VERIFY), "--manifest", str(bad_path)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        assert result.returncode != 0, result.stdout
        assert "floating/invalid pin" in result.stdout, result.stdout
    print("PASS: physics runtime contract fixture accepts valid state and rejects floating pins")


if __name__ == "__main__":
    main()
