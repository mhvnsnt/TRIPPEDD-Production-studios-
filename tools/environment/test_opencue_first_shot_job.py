#!/usr/bin/env python3
"""Adversarial tests for the OpenCue first-shot dispatcher contract."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "tools/environment/build_opencue_first_shot_job.py"


class OpenCueFirstShotTests(unittest.TestCase):
    def run_builder(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BUILDER), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=30,
        )

    def test_missing_blend_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "job.json"
            result = self.run_builder(
                "--blend", str(Path(tmp) / "missing.blend"),
                "--output-dir", str(Path(tmp) / "frames"),
                "--spec-output", str(out),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BLOCKED", result.stdout + result.stderr)
            self.assertFalse(out.exists())

    def test_missing_reopened_bytes_receipt_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blend = root / "scene.blend"
            blend.write_bytes(b"not-a-real-blend-but-nonempty")
            receipt = root / "receipt.json"
            receipt.write_text(json.dumps({"scene": "GM-WORLD-0001-FIRST-SHOT", "bytes_reopened": False}))
            out = root / "job.json"
            result = self.run_builder(
                "--blend", str(blend),
                "--output-dir", str(root / "frames"),
                "--receipt", str(receipt),
                "--spec-output", str(out),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reopened bytes", result.stdout + result.stderr)

    def test_ready_spec_never_submits_or_approves(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blend = root / "scene.blend"
            blend.write_bytes(b"nonempty-placeholder")
            receipt = root / "receipt.json"
            receipt.write_text(json.dumps({"scene": "GM-WORLD-0001-FIRST-SHOT", "bytes_reopened": True}))
            out = root / "job.json"
            result = self.run_builder(
                "--blend", str(blend),
                "--output-dir", str(root / "frames"),
                "--receipt", str(receipt),
                "--spec-output", str(out),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            job = json.loads(out.read_text())
            self.assertEqual(job["submission"], "NOT_SUBMITTED")
            self.assertEqual(job["production_gate"], "BLOCKED_UNTIL_QC")
            self.assertTrue(job["policy"]["opencue_is_dispatcher_not_authority"])
            self.assertTrue(job["policy"]["queue_submission_does_not_equal_render_evidence"])
            self.assertTrue(job["policy"]["exact_output_bytes_must_be_reopened_after_render"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
