#!/usr/bin/env python3
"""Build a fail-closed OpenCue job specification for a first-shot render.

OpenCue is a dispatcher here, never the production authority. This produces a
machine-readable job spec; actual submission belongs to the configured farm.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCENE = "GM-WORLD-0001-FIRST-SHOT"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--blender", default="blender")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1)
    parser.add_argument("--receipt")
    parser.add_argument("--spec-output", required=True)
    args = parser.parse_args()

    blend = Path(args.blend).resolve()
    if not blend.is_file() or blend.stat().st_size == 0:
        raise SystemExit("OPENCUE_JOB: BLOCKED — Blender scene is missing or empty")
    if args.start < 1 or args.end < args.start:
        raise SystemExit("OPENCUE_JOB: BLOCKED — invalid frame range")

    receipt_state = "LOCAL_RENDER_REQUIRED"
    if args.receipt:
        receipt_path = Path(args.receipt).resolve()
        if not receipt_path.is_file():
            raise SystemExit("OPENCUE_JOB: BLOCKED — supplied receipt does not exist")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt.get("bytes_reopened") is not True:
            raise SystemExit("OPENCUE_JOB: BLOCKED — receipt does not prove reopened bytes")
        if receipt.get("scene") != SCENE:
            raise SystemExit("OPENCUE_JOB: BLOCKED — receipt scene mismatch")
        receipt_state = "BYTES_REOPENED"

    output = str(Path(args.output_dir).resolve() / "frame_#####.png")
    job = {
        "schema": "trippedd.opencue-job/v1",
        "authority": "TRIPPEDD",
        "dispatcher": "OpenCue",
        "scene": SCENE,
        "fail_closed": True,
        "submission": "NOT_SUBMITTED",
        "production_gate": "BLOCKED_UNTIL_QC",
        "receipt_precondition": receipt_state,
        "job": {
            "show": "god-molecule",
            "shot": SCENE,
            "layer": "blender-render",
            "frame_range": f"{args.start}-{args.end}",
            "command": [args.blender, "-b", str(blend), "-o", output, "-F", "PNG", "-f", "#IFRAME#"],
            "output": output,
        },
        "policy": {
            "opencue_is_dispatcher_not_authority": True,
            "local_blender_path_must_be_tested_first": True,
            "queue_submission_does_not_equal_render_evidence": True,
            "exact_output_bytes_must_be_reopened_after_render": True,
            "visual_qc_required": True,
            "physical_qc_required_when_applicable": True,
        },
    }
    out = Path(args.spec_output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(job, indent=2))
    print(f"OPENCUE_JOB: READY_NOT_SUBMITTED ({out})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
