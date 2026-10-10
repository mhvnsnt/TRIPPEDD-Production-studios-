#!/usr/bin/env python3
"""Inspect an exact image artifact and emit a fail-closed evidence receipt.

This is deliberately separate from visual/physical QC. It proves that the named
bytes can be reopened and describes what the image reader actually decoded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(cmd: list[str]) -> dict[str, object]:
    exe = shutil.which(cmd[0])
    if not exe:
        return {"status": "UNAVAILABLE", "command": cmd}
    p = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=30)
    return {
        "status": "PASS" if p.returncode == 0 else "FAIL",
        "returncode": p.returncode,
        "command": cmd,
        "output": (p.stdout or p.stderr).strip().splitlines()[:80],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("image", type=Path)
    ap.add_argument("--expected-sha256")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    path = args.image.resolve()
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"IMAGE_UNAVAILABLE: {path}")

    digest = sha256(path)
    receipt = {
        "schema": "trippedd.image-artifact-receipt/v1",
        "artifact": {
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": digest,
            "extension": path.suffix.lower(),
        },
        "reopened": True,
        "evidence_status": "NOT_ATTEMPTED",
        "visual_qc": "NOT_ATTEMPTED",
        "physical_qc": "NOT_ATTEMPTED",
        "gate": "BLOCKED_UNTIL_QC",
        "policy": {
            "exact_bytes_required": True,
            "hash_must_match_when_expected": True,
            "artifact_inspection_is_not_visual_qc": True,
            "artifact_inspection_is_not_physical_qc": True,
        },
        "inspection": {
            "oiio_iinfo": run(["iinfo", str(path)]),
            "oiiotool_info": run(["oiiotool", "--info", str(path)]),
        },
    }
    if args.expected_sha256:
        receipt["artifact"]["expected_sha256"] = args.expected_sha256
        receipt["artifact"]["sha256_match"] = digest == args.expected_sha256
        if digest != args.expected_sha256:
            receipt["gate"] = "BLOCKED_HASH_MISMATCH"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["gate"] == "BLOCKED_UNTIL_QC" else 2


if __name__ == "__main__":
    raise SystemExit(main())
