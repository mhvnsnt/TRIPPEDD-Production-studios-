#!/usr/bin/env python3
"""Fail-closed gate for a filled Mars eye clearance ladder receipt.

Mirrors contact_gate.py: never treats missing measurement as PASS.
Consumes the ladder JSON produced/filled after eye_clearance_ladder.py
+ penetration_measure.py + reopened render frames.

Exit:
  0  PASS
  45 FAIL / UNKNOWN (required evidence absent or rules violated)

Usage:
  ./.trippedd_venv/bin/python tools/character/eye_clearance_gate.py \
      docs/evidence/eye_clearance/eye_clearance_ladder.json \
      --write docs/evidence/eye_clearance/gate_result.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

SCHEMA = "trippedd.eye-clearance-ladder/v1"
REQUIRED_STEPS = ("open", "intermediate", "closed")


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 45


def finite_nonneg(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value)) and float(value) >= 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--write", type=Path, help="write normalized gate result JSON")
    parser.add_argument("--tol-mm", type=float, default=None,
                        help="override tolerance (default: receipt.toleranceMM)")
    args = parser.parse_args()

    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read receipt: {exc}")

    if data.get("schema") != SCHEMA:
        return fail(f"schema must be {SCHEMA}")

    if data.get("classFilter") != "globe_only":
        return fail("classFilter must be globe_only")

    if not data.get("restBeforeBlink", True):
        return fail("restBeforeBlink must be true")

    if data.get("status") == "PENDING_MEASUREMENT":
        return fail("receipt is still PENDING_MEASUREMENT — fill measured fields first")

    tol = args.tol_mm if args.tol_mm is not None else data.get("toleranceMM")
    if not finite_nonneg(tol):
        return fail("toleranceMM must be a finite non-negative number")
    tol = float(tol)

    eyes = data.get("eyes")
    if not isinstance(eyes, list) or len(eyes) < 1:
        return fail("eyes[] is required")

    problems: list[str] = []
    rest_ok = True

    for eye in eyes:
        if not isinstance(eye, dict):
            problems.append("eye entry is not an object")
            continue
        lid = eye.get("lid")
        globe = eye.get("globe")
        label = f"{lid}->{globe}"
        steps = eye.get("steps")
        if not isinstance(steps, list) or not steps:
            problems.append(f"{label}: steps[] missing")
            continue

        by_step = {s.get("step"): s for s in steps if isinstance(s, dict)}
        for required in REQUIRED_STEPS:
            if required not in by_step:
                problems.append(f"{label}: missing step '{required}'")

        for step_name, step in by_step.items():
            if step.get("classFilter") != "globe_only":
                problems.append(f"{label}/{step_name}: classFilter must be globe_only")

            clear = step.get("minClearanceMM")
            samples = step.get("penetrationSamples")
            render = step.get("renderPath")
            sha = step.get("renderSHA256")
            status = step.get("status")

            if clear is None or samples is None:
                problems.append(f"{label}/{step_name}: measured fields still null")
                continue
            if not finite_nonneg(clear):
                problems.append(f"{label}/{step_name}: minClearanceMM invalid")
            if not isinstance(samples, int) or samples < 0:
                problems.append(f"{label}/{step_name}: penetrationSamples invalid")

            # Rest / open step: penetration must be resolved first
            if step_name in ("open", "rest") and isinstance(samples, int) and samples > 0:
                residual = step.get("restResidualReason")
                if not isinstance(residual, str) or not residual.strip():
                    rest_ok = False
                    problems.append(
                        f"{label}/{step_name}: rest penetration={samples} without restResidualReason"
                    )

            if status not in ("PASS", "FAIL", "PENDING", "UNKNOWN"):
                problems.append(f"{label}/{step_name}: bad status {status!r}")

            # PASS on a step requires render evidence
            if status == "PASS":
                if not isinstance(render, str) or not render.strip():
                    problems.append(f"{label}/{step_name}: PASS without renderPath")
                if not isinstance(sha, str) or len(sha) < 16:
                    problems.append(f"{label}/{step_name}: PASS without renderSHA256")
                if isinstance(samples, int) and samples > 0 and step_name not in ("open", "rest"):
                    # blink steps may still report residual only if documented
                    if not step.get("documentedResidual"):
                        problems.append(
                            f"{label}/{step_name}: PASS with penetrationSamples={samples}"
                        )
                if finite_nonneg(clear) and float(clear) < 0:
                    problems.append(f"{label}/{step_name}: negative clearance")

    if problems:
        for p in problems:
            print(f"FAIL: {p}", file=sys.stderr)
        result = {
            "schema": "trippedd.eye-clearance-gate-result/v1",
            "status": "FAIL",
            "reason": "; ".join(problems[:8]),
            "toleranceMM": tol,
            "restBeforeBlinkOk": rest_ok,
            "receipt": str(args.receipt),
        }
        if args.write:
            args.write.parent.mkdir(parents=True, exist_ok=True)
            args.write.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return 45

    # All steps present and measured; aggregate status
    any_fail = False
    any_pending = False
    for eye in eyes:
        for step in eye.get("steps", []):
            st = step.get("status")
            if st == "FAIL":
                any_fail = True
            if st in ("PENDING", "UNKNOWN", None):
                any_pending = True

    if any_fail:
        status = "FAIL"
        reason = "one or more ladder steps marked FAIL"
    elif any_pending:
        status = "UNKNOWN"
        reason = "one or more ladder steps still PENDING/UNKNOWN"
    else:
        status = "PASS"
        reason = "all eyes/steps measured, globe_only, rest clean, renders present"

    result = {
        "schema": "trippedd.eye-clearance-gate-result/v1",
        "status": status,
        "reason": reason,
        "toleranceMM": tol,
        "restBeforeBlinkOk": rest_ok,
        "receipt": str(args.receipt),
        "sourceHash": data.get("sourceHash"),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0 if status == "PASS" else 45


if __name__ == "__main__":
    raise SystemExit(main())
