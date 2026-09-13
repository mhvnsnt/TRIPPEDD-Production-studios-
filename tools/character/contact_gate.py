#!/usr/bin/env python3
"""Fail-closed contact/penetration gate for character evidence.

The gate consumes a measurement receipt produced by Blender/native simulation
or another reproducible measurement stage. It does not invent tolerances and
it never treats missing collision evidence as PASS.

Input JSON shape:
{
  "schema": "trippedd.contact-measurement/v1",
  "pair": "hair->head",
  "mode": "BLOCK",
  "penetrationMM": {"p50": 0.0, "p90": 0.0, "p99": 0.0, "max": 0.0},
  "violatingSamples": 0,
  "toleranceMM": 0.5,
  "selfCollision": "PASS|FAIL|NOT_ATTEMPTED",
  "visualEvidence": "path/to/sequence.json",
  "sourceHash": "...",
  "proxyHash": "..."
}

For BLOCK contacts, PASS requires complete measurements, zero penetration
beyond tolerance, zero violating samples, and visual evidence. ALLOW is a
contract declaration rather than a collision pass. STYLE_OVERRIDE requires
an explicit override reason and remains visible to downstream QC.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

SCHEMA = "trippedd.contact-measurement/v1"
MODES = {"BLOCK", "ALLOW", "STYLE_OVERRIDE"}
SELF_STATES = {"PASS", "FAIL", "NOT_ATTEMPTED"}
REQUIRED_STATS = ("p50", "p90", "p99", "max")


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 45


def finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--write", type=Path, help="write normalized gate result JSON")
    args = parser.parse_args()

    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read receipt: {exc}")

    if data.get("schema") != SCHEMA:
        return fail(f"schema must be {SCHEMA}")

    pair = data.get("pair")
    mode = data.get("mode")
    if not isinstance(pair, str) or not pair:
        return fail("pair is required")
    if mode not in MODES:
        return fail(f"mode must be one of {sorted(MODES)}")

    for field in ("sourceHash", "proxyHash", "visualEvidence"):
        if not isinstance(data.get(field), str) or not data[field]:
            return fail(f"{field} is required")

    if not finite_number(data.get("toleranceMM")) or float(data["toleranceMM"]) < 0:
        return fail("toleranceMM must be a finite non-negative number")

    if not isinstance(data.get("violatingSamples"), int) or data["violatingSamples"] < 0:
        return fail("violatingSamples must be a non-negative integer")

    self_collision = data.get("selfCollision")
    if self_collision not in SELF_STATES:
        return fail(f"selfCollision must be one of {sorted(SELF_STATES)}")

    penetration = data.get("penetrationMM")
    if not isinstance(penetration, dict):
        return fail("penetrationMM distribution is required")
    for stat in REQUIRED_STATS:
        if not finite_number(penetration.get(stat)) or float(penetration[stat]) < 0:
            return fail(f"penetrationMM.{stat} must be a finite non-negative number")

    tolerance = float(data["toleranceMM"])
    max_penetration = float(penetration["max"])
    violations = int(data["violatingSamples"])

    if mode == "BLOCK":
        passed = max_penetration <= tolerance and violations == 0
        if self_collision == "FAIL":
            passed = False
        if not passed:
            status = "FAIL"
            reason = "penetration or collision violations exceed the declared baseline gate"
        else:
            status = "PASS"
            reason = "BLOCK contact gate satisfied"
    elif mode == "ALLOW":
        status = "ALLOW"
        reason = "contact pair explicitly declared non-colliding"
    else:
        reason = data.get("overrideReason")
        if not isinstance(reason, str) or not reason.strip():
            return fail("STYLE_OVERRIDE requires overrideReason")
        status = "STYLE_OVERRIDE"

    result = {
        "schema": "trippedd.contact-gate-result/v1",
        "status": status,
        "pair": pair,
        "mode": mode,
        "reason": reason,
        "toleranceMM": tolerance,
        "penetrationMM": {k: float(penetration[k]) for k in REQUIRED_STATS},
        "violatingSamples": violations,
        "selfCollision": self_collision,
        "sourceHash": data["sourceHash"],
        "proxyHash": data["proxyHash"],
        "visualEvidence": data["visualEvidence"],
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0 if status in {"PASS", "ALLOW", "STYLE_OVERRIDE"} else 45


if __name__ == "__main__":
    raise SystemExit(main())
