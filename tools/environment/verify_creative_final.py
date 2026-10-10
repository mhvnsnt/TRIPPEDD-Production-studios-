#!/usr/bin/env python3
"""Verify that a first-shot render package contains real, reopenable bytes.

This verifier intentionally stops before visual/physical certification. Those
checks must consume the exact frame bytes and produce separate QC artifacts.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: verify_creative_final.py <shot_dir>")
        return 2
    root = Path(sys.argv[1])
    manifest_path = root / "manifest.json"
    frames_dir = root / "frames"
    if not manifest_path.is_file():
        print("RENDER_PACKAGE: FAIL\n - missing manifest.json")
        return 40

    try:
        m = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("RENDER_PACKAGE: FAIL\n - invalid manifest:", exc)
        return 40

    errors: list[str] = []
    frames = sorted(frames_dir.glob("frame_*.png")) if frames_dir.is_dir() else []
    if m.get("telemetry_substitution") is True:
        errors.append("telemetry_substitution true")
    if m.get("render_complete") is not True:
        errors.append("render_complete not true")
    if m.get("scene") != "GM-WORLD-0001-FIRST-SHOT":
        errors.append("unexpected scene id")
    if m.get("world_seed") != 742918:
        errors.append("unexpected world seed")
    if m.get("identity_source") != "MARS_CANONICAL":
        errors.append("canonical identity missing")
    if not m.get("mars_sha256"):
        errors.append("missing mars_sha256")
    if not frames:
        errors.append("no rendered frame bytes")
    if any(p.stat().st_size == 0 for p in frames):
        errors.append("empty frame file present")
    if m.get("frames") != len(frames):
        errors.append(f"frame count mismatch manifest={m.get('frames')} disk={len(frames)}")

    recorded = m.get("frame_sha256", {})
    reopened: dict[str, str] = {}
    for frame in frames:
        digest = sha256_file(frame)
        reopened[frame.name] = digest
        if recorded.get(frame.name) != digest:
            errors.append(f"frame hash mismatch: {frame.name}")

    if errors:
        print("RENDER_PACKAGE: FAIL")
        for error in errors:
            print(" -", error)
        return 40

    receipt = {
        "schema": "trippedd.render-receipt/v1",
        "scene": m["scene"],
        "world_seed": m["world_seed"],
        "identity_source": m["identity_source"],
        "mars_sha256": m["mars_sha256"],
        "frame_count": len(frames),
        "frame_sha256": reopened,
        "bytes_reopened": True,
        "visual_qc": "NOT_ATTEMPTED",
        "physical_qc": "NOT_ATTEMPTED",
        "gate": "BLOCKED_UNTIL_QC",
    }
    (root / "render_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("RENDER_PACKAGE: VERIFIED_BYTES")
    print("BYTES_REOPENED: true")
    print("VISUAL_QC: NOT_ATTEMPTED")
    print("PHYSICAL_QC: NOT_ATTEMPTED")
    print("GATE: BLOCKED_UNTIL_QC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
