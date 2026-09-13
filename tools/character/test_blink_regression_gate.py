#!/usr/bin/env python3
"""Regression tests for blink_regression_gate.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "tools/character/blink_regression_gate.py"


def run(channels: list[dict]) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as td:
        receipt = Path(td) / "blink.json"
        receipt.write_text(json.dumps({"channels": channels}), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(GATE), str(receipt)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )


def base(new_travel: tuple[float, float]) -> list[dict]:
    return [
        {"key": "blink_L", "travel_apertures": 0.0},
        {"key": "blink_R", "travel_apertures": 0.0},
        {"key": "blink_own_L", "lands_from_lid_line_mm": 4.7, "travel_apertures": new_travel[0]},
        {"key": "blink_own_R", "lands_from_lid_line_mm": 4.7, "travel_apertures": new_travel[1]},
    ]


def main() -> None:
    # Current measured state is intentionally rejected: targeting is correct,
    # but both new keys under-travel the measured aperture.
    current = run(base((0.86, 0.69)))
    assert current.returncode != 0
    assert "under-travels" in current.stderr + current.stdout

    passing = run(base((1.10, 1.02)))
    assert passing.returncode == 0, passing.stdout + passing.stderr
    assert "PASS:" in passing.stdout

    moved_legacy = run([
        {"key": "blink_L", "travel_apertures": 0.20},
        {"key": "blink_R", "travel_apertures": 0.0},
        {"key": "blink_own_L", "lands_from_lid_line_mm": 4.7, "travel_apertures": 1.10},
        {"key": "blink_own_R", "lands_from_lid_line_mm": 4.7, "travel_apertures": 1.02},
    ])
    assert moved_legacy.returncode != 0
    assert "legacy regression control changed" in moved_legacy.stderr + moved_legacy.stdout

    print("PASS: blink regression gate rejects current under-travel, accepts measured-pass shape, and protects legacy controls")


if __name__ == "__main__":
    main()
