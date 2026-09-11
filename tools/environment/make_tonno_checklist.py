#!/usr/bin/env python3
"""Fail-closed checklist for SC-02 Tonnō Pass packages.

Does not apply the look — verifies a claimed Tonnō deliverable still respects identity.

Usage:
  python3 tools/environment/make_tonno_checklist.py /path/to/shot_dir
Expects optional:
  manifest.json with mars_sha256, world_seed, tonno_pass: true
  frames/ or stills/
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: make_tonno_checklist.py <shot_dir>")
        return 2
    root = Path(sys.argv[1])
    errors: list[str] = []
    notes: list[str] = []

    man_path = root / "manifest.json"
    if not man_path.is_file():
        errors.append("missing manifest.json")
        m = {}
    else:
        m = json.loads(man_path.read_text(encoding="utf-8"))

    if m.get("telemetry_substitution") is True:
        errors.append("telemetry_substitution")
    if m.get("identity_source") not in (None, "MARS_CANONICAL") and "mars" in json.dumps(m).lower():
        if m.get("identity_source") != "MARS_CANONICAL":
            errors.append("identity_source must be MARS_CANONICAL when Mars is claimed")
    if not m.get("mars_sha256"):
        notes.append("no mars_sha256 — OK only if Mars is fully out of frame")
    if m.get("tonno_pass") is not True and m.get("style_lane") != "tonno":
        notes.append("manifest does not flag tonno_pass/style_lane=tonno")

    frames = []
    for sub in ("frames", "stills", "tonno"):
        d = root / sub
        if d.is_dir():
            frames.extend(sorted(d.glob("*.png")) + sorted(d.glob("*.jpg")))
    if not frames:
        errors.append("no png/jpg frames under frames|stills|tonno")
    elif any(p.stat().st_size == 0 for p in frames):
        errors.append("empty media file")

    # Style claims must not excuse missing creative_final for upstream plates
    if m.get("covers_failed_3d") is True:
        errors.append("tonno must not cover failed 3d (covers_failed_3d)")

    print("TONNO_CHECKLIST")
    for n in notes:
        print(" NOTE:", n)
    if errors:
        print("TONNO: FAIL")
        for e in errors:
            print(" -", e)
        return 40
    print("TONNO: PASS_STRUCTURAL")
    print("frames:", len(frames))
    if m.get("mars_sha256"):
        print("mars_sha256:", m["mars_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
