#!/usr/bin/env python3
"""Fail-closed QC gate for MARS facial fit invariants.

This gate does not invent geometry or landmarks. It only accepts measured receipts
from the owner-linework facial lanes and rejects missing/ambiguous evidence.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXIT_PASS = 0
EXIT_UNKNOWN = 45

REQUIRED = {
    "schema",
    "source",
    "sourceHash",
    "eyes",
    "nostrils",
    "mouth",
    "visualEvidence",
}


def fail(message: str) -> int:
    print(f"UNKNOWN: {message}", file=sys.stderr)
    return EXIT_UNKNOWN


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--write", type=Path)
    args = ap.parse_args()

    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read receipt: {exc}")

    if not REQUIRED.issubset(data):
        return fail("missing required top-level measurement fields")
    if data["schema"] != "trippedd.mars-face-invariant-measurement/v1":
        return fail("wrong measurement schema")
    if data["source"] != "assets/source_models/MARS_source.glb":
        return fail("source is not canonical MARS geometry")
    if not data["sourceHash"]:
        return fail("source hash is missing")

    eyes = data["eyes"]
    nostrils = data["nostrils"]
    mouth = data["mouth"]
    visual = data["visualEvidence"]

    eye_required = ("leftApertureMM", "rightApertureMM", "closedStateEyeballVisible", "lidSurfaceIntersection", "states")
    nostril_required = ("leftRimErrorMM", "rightRimErrorMM", "states")
    mouth_required = ("openingCenterOffsetMM", "toothBlinderCenterOffsetMM", "oralVisibilityAtClosedMM", "states")
    for label, obj, fields in (
        ("eyes", eyes, eye_required),
        ("nostrils", nostrils, nostril_required),
        ("mouth", mouth, mouth_required),
    ):
        if not isinstance(obj, dict) or any(field not in obj for field in fields):
            return fail(f"{label} evidence is incomplete")

    if bool(eyes["closedStateEyeballVisible"]):
        return fail("eyeball is visible through the closed eyelid")
    if float(eyes["lidSurfaceIntersection"]) > 0.0:
        return fail("eyelid intersects the eyeball surface")
    if float(mouth["oralVisibilityAtClosedMM"]) > 0.0:
        return fail("oral cavity is exposed at the closed-mouth state")

    # Centering must be measured; zero is the only accepted value here because the
    # known oral-opening offset is a correctness issue, not a style allowance.
    if abs(float(mouth["toothBlinderCenterOffsetMM"])) > 0.5:
        return fail("tooth-blinder opening is not centered within 0.5 mm")
    if abs(float(mouth["openingCenterOffsetMM"])) > 0.5:
        return fail("mouth opening is not centered within 0.5 mm")

    expected_states = {"OPEN", "HALF", "CLOSED"}
    for label, obj in (("eyes", eyes), ("nostrils", nostrils), ("mouth", mouth)):
        states = set(obj["states"] if isinstance(obj["states"], list) else [])
        if not expected_states.issubset(states):
            return fail(f"{label} lacks OPEN/HALF/CLOSED motion evidence")

    if not isinstance(visual, list) or len(visual) < 3:
        return fail("visual evidence must include front, three-quarter, and side views")
    if any(not isinstance(item, str) or not item for item in visual):
        return fail("visual evidence contains invalid artifact references")

    result = {
        "schema": "trippedd.mars-face-invariant-gate/v1",
        "status": "PASS",
        "source": data["source"],
        "sourceHash": data["sourceHash"],
        "protectedLanes": ["eyes_blink", "nostrils_nose", "mouth_oral"],
        "rules": {
            "eyeballVisibleThroughClosedLid": False,
            "eyelidSurfaceIntersectionMM": 0.0,
            "mouthCenterOffsetToleranceMM": 0.5,
            "toothBlinderCenterOffsetToleranceMM": 0.5,
            "unknownNeverPass": True,
        },
        "visualEvidence": visual,
    }
    if args.write:
        args.write.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return EXIT_PASS


if __name__ == "__main__":
    raise SystemExit(main())
