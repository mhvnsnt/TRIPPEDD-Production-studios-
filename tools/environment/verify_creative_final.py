#!/usr/bin/env python3
"""Fail-closed verification for God Molecule creative-final packages.

Usage:
  python3 tools/environment/verify_creative_final.py /path/to/artifacts/env/GM-WORLD-0001-TEST
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: verify_creative_final.py <shot_dir>")
        return 2
    root = Path(sys.argv[1])
    errors: list[str] = []

    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        print("CREATIVE_FINAL: FAIL")
        print(" - missing manifest.json")
        return 40

    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    frames_dir = root / "frames"
    frames = sorted(frames_dir.glob("frame_*.png")) if frames_dir.is_dir() else []

    if m.get("telemetry_substitution") is True:
        errors.append("telemetry_substitution true")
    if m.get("creative_final") is not True:
        errors.append("creative_final not true")
    if not m.get("world_seed"):
        errors.append("missing world seed")
    if not m.get("mars_sha256"):
        errors.append("missing mars_sha256")
    if not frames:
        errors.append("no frame_*.png files")
    if any(p.stat().st_size == 0 for p in frames):
        errors.append("empty frame file present")
    expected = m.get("frames")
    if expected is not None and expected != len(frames):
        errors.append(f"frame count mismatch manifest={expected} disk={len(frames)}")
    if m.get("gaussian_splat") not in (None, "NOT_USED_IN_FIRST_PROOF", False, "disabled"):
        # First proof profile must keep splats off unless explicitly promoted
        if m.get("scene") == "GM-WORLD-0001-TEST" and m.get("gaussian_splat") not in (
            "NOT_USED_IN_FIRST_PROOF",
            False,
            "disabled",
            None,
        ):
            errors.append("first proof should not claim gaussian without promotion")

    if errors:
        print("CREATIVE_FINAL: FAIL")
        for e in errors:
            print(" -", e)
        return 40

    print("CREATIVE_FINAL: VERIFIED")
    print("frames:", len(frames))
    print("seed:", m.get("world_seed"))
    print("mars_sha256:", m.get("mars_sha256"))
    print("scene:", m.get("scene"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
