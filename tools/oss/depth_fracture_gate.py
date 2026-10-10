#!/usr/bin/env python3
"""Fail-closed adoption gate for MiDaS depth and Shatter It fracture receipts.

The gate validates evidence contracts only; it never promotes a derivative
artifact to canonical MARS authority. UNKNOWN is never PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_str(obj: dict, key: str) -> str | None:
    value = obj.get(key)
    return value if isinstance(value, str) and value else None


def check_common(receipt: dict) -> str | None:
    if receipt.get("schema") != "trippedd.oss-physics-evidence/v1":
        return "schema must be trippedd.oss-physics-evidence/v1"
    if receipt.get("status") != "PASS":
        return "status must be PASS"
    if not HEX40.fullmatch(str(receipt.get("upstreamCommit", ""))):
        return "upstreamCommit must be a 40-hex commit"
    for key in ("inputSha256", "outputSha256", "visualEvidenceSha256"):
        if not HEX64.fullmatch(str(receipt.get(key, ""))):
            return f"{key} must be a 64-hex SHA256"
    if receipt.get("canonicalSourceMutated") is not False:
        return "canonicalSourceMutated must be false"
    if receipt.get("exactCommand") in (None, "", "UNKNOWN"):
        return "exactCommand is required"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--verify-output", type=Path)
    args = ap.parse_args()

    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read receipt: {exc}")
    if not isinstance(receipt, dict):
        return fail("receipt must be an object")

    error = check_common(receipt)
    if error:
        return fail(error)

    lane = require_str(receipt, "lane")
    if lane == "midas_depth":
        if receipt.get("authority") != "DERIVATIVE_DEPTH_EVIDENCE":
            return fail("MiDaS authority must be DERIVATIVE_DEPTH_EVIDENCE")
        if receipt.get("weightsLicenseStatus") not in {"SEPARATELY_VERIFIED", "NOT_REQUIRED"}:
            return fail("MiDaS weights license/provenance is not verified")
        if not isinstance(receipt.get("depthErrorQc"), dict):
            return fail("depthErrorQc is required")
    elif lane == "shatter_it":
        if receipt.get("authority") != "DERIVATIVE_FRACTURE_OUTPUT":
            return fail("Shatter It authority must be DERIVATIVE_FRACTURE_OUTPUT")
        if receipt.get("blenderVersion") in (None, "", "UNKNOWN"):
            return fail("Blender version is required")
        if not isinstance(receipt.get("dependencyLicenseInventory"), list):
            return fail("dependencyLicenseInventory is required")
        if receipt.get("deterministic") is not True:
            return fail("fracture determinism must be true")
        if not isinstance(receipt.get("fragmentCount"), int) or receipt["fragmentCount"] < 1:
            return fail("fragmentCount must be a positive integer")
        if receipt.get("collisionSmokeTest") is not True:
            return fail("collisionSmokeTest must be true")
    else:
        return fail("unknown lane")

    if args.verify_output:
        actual = sha256_file(args.verify_output)
        if actual != receipt["outputSha256"]:
            return fail("output SHA256 does not match receipt")

    print(f"PASS: {lane} derivative evidence is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
