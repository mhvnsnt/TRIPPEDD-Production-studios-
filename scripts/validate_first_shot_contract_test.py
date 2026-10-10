#!/usr/bin/env python3
"""Adversarial regression tests for the first-shot contract validator."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_first_shot_contract.py"


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), "--repo-root", str(root)], cwd=ROOT, text=True, capture_output=True, check=False)


def clone_contract(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "config", tmp_path / "config")
    shutil.copytree(ROOT / "docs", tmp_path / "docs")
    shutil.copytree(ROOT / "environments", tmp_path / "environments")


def test_clean_contract_passes() -> None:
    result = run_validator(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "FIRST_SHOT_CONTRACT: PASS" in result.stdout
    assert "BLOCKED_UNTIL_REAL_RENDER" in result.stdout


def test_identity_substitution_fails(tmp_path: Path) -> None:
    clone_contract(tmp_path)
    path = tmp_path / "docs/production-studio/god-molecule-first-shot.json"
    data = json.loads(path.read_text())
    data["character"]["id"] = "GENERATED_MARS"
    path.write_text(json.dumps(data))
    result = run_validator(tmp_path)
    assert result.returncode != 0
    assert "canonical character identity mismatch" in result.stdout


def test_fake_pre_render_evidence_fails(tmp_path: Path) -> None:
    clone_contract(tmp_path)
    path = tmp_path / "docs/production-studio/god-molecule-first-shot.json"
    data = json.loads(path.read_text())
    data["evidence"]["rendered_pixels"] = "fake/render.png"
    path.write_text(json.dumps(data))
    result = run_validator(tmp_path)
    assert result.returncode != 0
    assert "fabricated evidence" in result.stdout


if __name__ == "__main__":
    test_clean_contract_passes()
    print("FIRST_SHOT_CONTRACT_TESTS: PASS")
