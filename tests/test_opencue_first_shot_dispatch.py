import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.environment.opencue_first_shot_dispatch import EXPECTED_WORLD, SHOT_ID, build_job, load_receipt, verify_source


class OpenCueFirstShotDispatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.blend = self.root / "GM-WORLD-0001-FIRST-SHOT.blend"
        self.blend.write_bytes(b"real-resolved-blend-bytes")
        self.png = self.root / "frame_0001.png"
        self.png.write_bytes(b"real-rendered-png-placeholder")
        self.blend_sha = hashlib.sha256(self.blend.read_bytes()).hexdigest()
        self.png_sha = hashlib.sha256(self.png.read_bytes()).hexdigest()
        self.receipt = self.root / "render-receipt.json"
        self.receipt.write_text(json.dumps({
            "rendered": True,
            "shot_id": SHOT_ID,
            "world_id": EXPECTED_WORLD,
            "frame": 1,
            "source_scene": {"path": self.blend.name, "sha256": self.blend_sha},
            "artifact": {"path": self.png.name, "format": "png", "sha256": self.png_sha},
            "visual_qc": "NOT_EVALUATED",
            "physical_qc": "NOT_EVALUATED",
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_receipt_builds_dispatch_without_qc_promotion(self):
        receipt = load_receipt(self.receipt)
        verify_source(self.blend, receipt["source_scene"]["sha256"])
        spec = build_job(receipt, self.blend, "/shared/renders/first-shot")
        self.assertEqual(spec["world_seed"], 742918)
        self.assertEqual(spec["gate"], "BLOCKED_UNTIL_QC")
        self.assertTrue(spec["policy"]["queue_success_is_not_qc"])

    def test_source_hash_mismatch_blocks(self):
        with self.assertRaisesRegex(RuntimeError, "SHA-256 mismatch"):
            verify_source(self.blend, "0" * 64)

    def test_non_rendered_receipt_blocks(self):
        data = json.loads(self.receipt.read_text(encoding="utf-8"))
        data["rendered"] = False
        self.receipt.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "not a proven render"):
            load_receipt(self.receipt)


if __name__ == "__main__":
    unittest.main()
