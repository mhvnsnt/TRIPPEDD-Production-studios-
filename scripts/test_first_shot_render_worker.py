#!/usr/bin/env python3
"""Standard-library regression tests for the first-shot render worker."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "scripts" / "run_first_shot_blender.py"


class FirstShotRenderWorkerTests(unittest.TestCase):
    def test_missing_blend_blocks_before_render(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out"
            receipt = output / "receipt.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(WORKER),
                    "--repo-root", str(ROOT),
                    "--blend", str(Path(directory) / "missing.blend"),
                    "--receipt", str(receipt),
                    "--output-dir", str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("RENDER_EVIDENCE: BLOCKED", result.stdout)
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertFalse(data["rendered"])
            self.assertIn("does not exist", data["error"])

    def test_worker_requires_blend_argument(self) -> None:
        result = subprocess.run(
            [sys.executable, str(WORKER), "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--blend", result.stdout)


if __name__ == "__main__":
    unittest.main()
