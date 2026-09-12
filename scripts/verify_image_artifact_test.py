#!/usr/bin/env python3
"""Adversarial tests for image-artifact inspection.

These tests prove that the inspection layer rejects missing/corrupt media and
that a valid image is inspected without being promoted to production approval.
They intentionally use only the Python standard library plus the repository
script so they can run before optional OIIO installation succeeds.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_image_artifact.py"

# 1x1 RGBA PNG. The CRCs are part of the fixture so the OIIO path can decode it
# when available; the repository verifier remains responsible for interpretation.
VALID_PNG = bytes.fromhex(
    "89504e470d0a1a0a"
    "0000000d49484452000000010000000108060000001f15c489"
    "0000000d49444154789c6360f8cf00000003000101"  # compact zlib payload
    "0000000049454e44ae426082"
)


class VerifyImageArtifactAdversarialTests(unittest.TestCase):
    def run_verify(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VERIFY), "--image", str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=30,
        )

    def test_missing_artifact_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_verify(Path(tmp) / "missing.png")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BLOCKED", result.stdout + result.stderr)

    def test_truncated_png_header_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "truncated.png"
            path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"IHDR")
            result = self.run_verify(path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BLOCKED", result.stdout + result.stderr)

    def test_fake_png_dimensions_are_not_enough_for_decode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fake.png"
            path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                b"\x00\x00\x00\x0dIHDR"
                b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
            )
            result = self.run_verify(path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BLOCKED", result.stdout + result.stderr)

    def test_valid_png_is_inspected_not_approved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "valid.png"
            path.write_bytes(VALID_PNG)
            result = self.run_verify(path)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertIn(payload["status"], {"INSPECTED", "FORMAT_CHECK_ONLY"})
            self.assertEqual(payload["evidence_status"], "NOT_ATTEMPTED")
            self.assertTrue(payload["policy"]["inspection_is_not_production_approval"])
            self.assertEqual(len(payload["sha256"]), 64)


if __name__ == "__main__":
    unittest.main(verbosity=2)
