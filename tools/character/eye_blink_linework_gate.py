#!/usr/bin/env python3
"""Fail-closed gate for Mars eye/blink authority.

Linework is the authority. MediaPipe and canonical_fit are diagnostic history only.
A rebuild may proceed only when the measured linework authority record and a unique
linework-derived 3-D lift are present.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "assets/references/mars_facial_linework/LINEWORK_INDEX.json"
AUTHORITY = ROOT / "assets/rigs/MARS_linework_authority.json"
EXPECTED = {"eye_opening_L_mm": 7.08, "eye_opening_R_mm": 8.24,
            "max_linework_reprojection_px": 0.0016, "lifted_points": 382}

def load(path: Path) -> dict:
    if not path.is_file():
        raise RuntimeError(f"MISSING_EVIDENCE: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))

def find_linework_3d() -> Path | None:
    candidates = []
    for root in (ROOT / "assets", ROOT / "docs", ROOT / "renders"):
        if not root.exists():
            continue
        for p in root.rglob("*.json"):
            n = p.name.lower()
            if "linework" in n and ("3d" in n or "lift" in n or "projection" in n):
                candidates.append(p)
    return candidates[0] if len(candidates) == 1 else None

def main() -> int:
    try:
        index = load(INDEX)
        authority = load(AUTHORITY)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr); return 40
    if index.get("status") != "P0_CANONICAL" or authority.get("status") != "P0_CANONICAL":
        print("FAIL: linework authority is not P0_CANONICAL", file=sys.stderr); return 41
    plates = index.get("plates", {})
    expected_paths = [plates.get("mars_linework_front_close", {}).get("path"),
                      plates.get("mars_linework_front_full", {}).get("path")]
    for rel in expected_paths:
        if not rel or not (ROOT / rel).is_file():
            print(f"MISSING_EVIDENCE: {rel or '<plate path absent>'}", file=sys.stderr); return 42
    m = authority.get("measurements", {})
    actuals = {"eye_opening_L_mm": m.get("eyeOpeningLMM"),
               "eye_opening_R_mm": m.get("eyeOpeningRMM"),
               "max_linework_reprojection_px": m.get("maxReprojectionPx"),
               "lifted_points": m.get("liftedPoints")}
    for key, expected in EXPECTED.items():
        actual = actuals[key]
        if actual is None:
            print(f"MISSING_MEASUREMENT: measurements.{key}", file=sys.stderr); return 43
        tolerance = 0.01 if key.endswith("mm") else 1e-6
        if abs(float(actual) - expected) > tolerance:
            print(f"FAIL: {key}={actual} expected {expected}", file=sys.stderr); return 44
    if authority.get("blinkAuthority", {}).get("fallback") != "FORBIDDEN":
        print("FAIL: blink fallback policy is not FORBIDDEN", file=sys.stderr); return 44
    lift = find_linework_3d()
    if lift is None:
        print("UNKNOWN: no unique linework-derived 3-D lift artifact was found; refusing MediaPipe/canonical_fit fallback.", file=sys.stderr)
        return 45
    print(f"PASS: authoritative linework plates present: {len(expected_paths)}")
    print(f"PASS: unique 3-D linework lift: {lift.relative_to(ROOT)}")
    print(f"TARGET: L={EXPECTED['eye_opening_L_mm']:.2f} mm R={EXPECTED['eye_opening_R_mm']:.2f} mm")
    print(f"TARGET: {EXPECTED['lifted_points']} lifted points; reprojection <= {EXPECTED['max_linework_reprojection_px']} px")
    print("PASS: MediaPipe/canonical_fit fallback is not permitted")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
