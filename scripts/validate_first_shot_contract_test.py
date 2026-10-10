#!/usr/bin/env python3
"""Adversarial regression tests for the first-shot contract validator."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_first_shot_contract.py"


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo-root", str(root)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def clone_contract(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "config", tmp_path / "config")
    shutil.copytree(ROOT / "docs", tmp_path / "docs")
    shutil.copytree(ROOT / "environments", tmp_path / "environments")


class FirstShotContractTests(unittest.TestCase):
    def test_clean_contract_passes(self) -> None:
        result = run_validator(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("FIRST_SHOT_CONTRACT: PASS", result.stdout)
        self.assertIn("BLOCKED_UNTIL_REAL_RENDER", result.stdout)

    def test_identity_substitution_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            clone_contract(tmp_path)
            path = tmp_path / "docs/production-studio/god-molecule-first-shot.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["character"]["id"] = "GENERATED_MARS"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = run_validator(tmp_path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("canonical character identity mismatch", result.stdout)

    def test_fake_pre_render_evidence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            clone_contract(tmp_path)
            path = tmp_path / "docs/production-studio/god-molecule-first-shot.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["evidence"]["rendered_pixels"] = "fake/render.png"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = run_validator(tmp_path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("fabricated evidence", result.stdout)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FirstShotContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("FIRST_SHOT_CONTRACT_TESTS: PASS" if result.wasSuccessful() else "FIRST_SHOT_CONTRACT_TESTS: FAIL")
    raise SystemExit(0 if result.wasSuccessful() else 1)
