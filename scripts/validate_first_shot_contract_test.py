#!/usr/bin/env python3
"""Standard-library regression tests for the fail-closed first-shot contract."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_first_shot_contract.py"


def run_validator(repo_root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo-root", str(repo_root)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def clone_contract() -> Path:
    temp = Path(tempfile.mkdtemp(prefix="trippedd-first-shot-test-"))
    for relative in ("config", "docs", "environments"):
        source = ROOT / relative
        if source.exists():
            shutil.copytree(source, temp / relative)
    return temp


class FirstShotContractTests(unittest.TestCase):
    def test_clean_contract_passes(self) -> None:
        result = run_validator(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("FIRST_SHOT_CONTRACT: PASS", result.stdout)
        self.assertIn("BLOCKED_UNTIL_REAL_RENDER", result.stdout)

    def test_identity_substitution_fails(self) -> None:
        temp = clone_contract()
        self.addCleanup(shutil.rmtree, temp, ignore_errors=True)
        path = temp / "docs/production-studio/god-molecule-first-shot.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["character"]["id"] = "GENERATED_MARS"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        result = run_validator(temp)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("canonical character identity mismatch", result.stdout + result.stderr)

    def test_fake_pre_render_evidence_fails(self) -> None:
        temp = clone_contract()
        self.addCleanup(shutil.rmtree, temp, ignore_errors=True)
        path = temp / "docs/production-studio/god-molecule-first-shot.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["evidence"]["rendered_pixels"] = "fake/render.png"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        result = run_validator(temp)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fabricated evidence", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
