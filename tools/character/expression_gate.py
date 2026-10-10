#!/usr/bin/env python3
"""Fail-closed validator for measured MARS facial-expression receipts."""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path

SCHEMA = "trippedd.mars-expression-measurement/v1"
CONTRACT = Path(__file__).with_name("mars_expression_contract.json")
AUTHORITY = Path(__file__).resolve().parents[2] / "assets/rigs/MARS_linework_authority.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str) -> int:
    print(f"UNKNOWN: {msg}", file=sys.stderr)
    return 45


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--write", type=Path)
    args = ap.parse_args()
    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read evidence: {exc}")
    if data.get("schema") != SCHEMA:
        return fail(f"schema must be {SCHEMA}")
    if not AUTHORITY.is_file():
        return fail("MARS linework authority is missing")
    required = ("control", "sourceHash", "authorityHash", "driver", "target", "visualEvidence", "states", "measurements")
    for key in required:
        if key not in data:
            return fail(f"missing required field: {key}")
    if data["authorityHash"] != sha256(AUTHORITY):
        return fail("authority hash does not match current committed linework authority")
    if data["driver"] in contract["forbiddenAuthority"]:
        return fail("forbidden generic landmark authority")
    if not isinstance(data["states"], list) or data["states"] != contract["motionProof"]["minimumStates"]:
        return fail("motion proof must contain neutral/activation/peak/release/neutral states in order")
    measurements = data["measurements"]
    if not isinstance(measurements, dict):
        return fail("measurements must be an object")
    for key in contract["motionProof"]["requiredMeasurements"]:
        value = measurements.get(key)
        if key == "outlierCount":
            if not isinstance(value, int) or value < 0:
                return fail("outlierCount must be a non-negative integer")
        elif not isinstance(value, (int, float)) or not math.isfinite(float(value)) or float(value) < 0:
            return fail(f"measurement {key} must be finite and non-negative")
    if not isinstance(data["visualEvidence"], str) or not data["visualEvidence"]:
        return fail("visualEvidence is required")
    result = {
        "schema": "trippedd.mars-expression-gate-result/v1",
        "status": "PASS",
        "control": data["control"],
        "driver": data["driver"],
        "target": data["target"],
        "sourceHash": data["sourceHash"],
        "authorityHash": data["authorityHash"],
        "visualEvidence": data["visualEvidence"],
        "measurements": measurements,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
