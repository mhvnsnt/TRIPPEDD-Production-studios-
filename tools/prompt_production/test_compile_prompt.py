#!/usr/bin/env python3
"""Adversarial/unit tests for the prompt compiler."""

import json
import tempfile
import unittest
from pathlib import Path

from compile_prompt import compile_prompt


class PromptCompilerTests(unittest.TestCase):
    def test_mars_prompt_resolves_canonical_identity(self):
        result = compile_prompt(
            "Make the EP01 motel cold open. Mars wakes up, sits on the bed, looks toward the door, gets up and walks to the bathroom.",
            {"world_id": "GM-WORLD-MOTEL"},
        )
        self.assertEqual(result.schema, "trippedd.prompt-intent/v1")
        self.assertEqual(result.entities["character"], "MARS_CANONICAL")
        self.assertEqual(result.entities["world"], "GM-WORLD-MOTEL")
        self.assertEqual(result.status, "READY_FOR_ADAPTER")
        self.assertTrue(any(op.op == "solve_rig_motion" for op in result.operations))
        self.assertTrue(any(op.op == "inspect_pixels" for op in result.operations))

    def test_unknown_world_does_not_silently_create_canon(self):
        result = compile_prompt("Build a new alien city and put Mars in it.")
        self.assertEqual(result.status, "NEEDS_RESOLUTION")
        self.assertEqual(result.entities["character"], "MARS_CANONICAL")
        self.assertIsNone(result.entities["world"])
        self.assertIn("preserve_locked_canon", result.gates)

    def test_render_claim_is_never_production_approval(self):
        result = compile_prompt("Render Mars walking through the motel.", {"world_id": "GM-WORLD-MOTEL"})
        ops = {op.op: op for op in result.operations}
        self.assertIn("render_preview", ops)
        self.assertIn("inspect_pixels", ops)
        self.assertIn("write_evidence_receipt", ops)
        self.assertEqual(ops["render_preview"].args["actual_pixels_required"], True)
        self.assertEqual(ops["write_evidence_receipt"].args["bytes_reopened"], True)


if __name__ == "__main__":
    unittest.main()
