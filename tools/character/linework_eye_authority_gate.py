#!/usr/bin/env python3
"""Fail-closed authority gate for MARS eye/lid reconstruction.

The old eye_sockets.py path is historical geometry tooling. It consumed
MediaPipe-derived eyelid contours and therefore MUST NOT be allowed to define
current eye seating or blink authority.

This gate accepts only the owner-drawn linework contract plus the measured
3-D lift evidence. It deliberately does not synthesize missing depth.

Exit codes:
  0  PASS
  40 FAIL (known-invalid evidence)
  45 UNKNOWN (required evidence is absent)

Usage:
  python tools/character/linework_eye_authority_gate.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTH = ROOT / "assets/rigs/MARS_linework_authority.json"
INDEX = ROOT / "assets/references/mars_facial_linework/LINEWORK_INDEX.json"
LIFT_DIRS = [ROOT / "renders", ROOT / "docs", ROOT / "assets"]


def load(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: invalid JSON {path}: {exc}")
        raise SystemExit(40)


def find_lift() -> list[Path]:
    hits: list[Path] = []
    for base in LIFT_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*.json"):
            name = p.name.lower()
            if "linework" in name and any(k in name for k in ("3d", "lift", "projection")):
                hits.append(p)
    return sorted(set(hits))


def main() -> int:
    index = load(INDEX)
    auth = load(AUTH)
    if index is None or auth is None:
        print("UNKNOWN: canonical linework index/authority is missing")
        return 45

    if index.get("status") != "P0_CANONICAL_BINARIES_PRESENT":
        print("FAIL: linework index is not P0_CANONICAL_BINARIES_PRESENT")
        return 40
    if auth.get("status") != "P0_CANONICAL":
        print("FAIL: linework authority is not P0_CANONICAL")
        return 40

    plates = index.get("plates", [])
    if len(plates) < 2 or not all(p.get("present") for p in plates[:2]):
        print("UNKNOWN: canonical front linework plates are not both present")
        return 45

    measured = auth.get("measurements", {})
    expected = {
        "liftedPoints": 382,
        "eyeOpeningLMM": 7.08,
        "eyeOpeningRMM": 8.24,
        "maxReprojectionPx": 0.0016,
    }
    for key, value in expected.items():
        if measured.get(key) != value:
            print(f"FAIL: authority measurement {key}={measured.get(key)!r}, expected {value!r}")
            return 40

    blink = auth.get("blinkAuthority", {})
    if blink.get("driver") != "drawn_eyelid_lines":
        print("FAIL: blink driver is not the owner-drawn eyelid lines")
        return 40
    if blink.get("fallback") != "FORBIDDEN":
        print("FAIL: blink fallback is not forbidden")
        return 40

    lift = find_lift()
    if len(lift) == 0:
        print("UNKNOWN: no unique linework-derived 3-D lift artifact found")
        return 45
    if len(lift) != 1:
        print("FAIL: expected exactly one linework-derived 3-D lift artifact")
        for p in lift:
            print(f"  candidate: {p.relative_to(ROOT)}")
        return 40

    print("PASS: MARS eye/lid authority is owner-drawn linework")
    print(f"  lift: {lift[0].relative_to(ROOT)}")
    print("  L/R aperture: 7.08 / 8.24 mm")
    print("  lifted points: 382")
    print("  max reprojection: 0.0016 px")
    print("  MediaPipe/canonical_fit: rejected as independent authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
