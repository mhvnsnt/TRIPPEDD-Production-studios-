#!/usr/bin/env python3
"""Fail-closed validation of the persisted MVMP face authority."""
import argparse
import json
import os
import sys

from face_landmark_semantics import EYE_UPPER, EYE_LOWER, EYEBROW, IRIS

ap = argparse.ArgumentParser()
ap.add_argument("--authority", default="renders/_rig_measure/face_landmark_authority.json")
args = ap.parse_args()

if not os.path.exists(args.authority):
    raise SystemExit("IMAGE_UNAVAILABLE: face landmark authority does not exist")

a = json.load(open(args.authority))
if a.get("schema") != "trippedd.mars-face-landmark-authority/v1":
    raise SystemExit("FAILED: wrong face landmark authority schema")

landmarks = a.get("landmarks", {})
if len(landmarks) != 478:
    raise SystemExit("FAILED: authority contains %d landmarks, expected 478" % len(landmarks))

for side in ("L", "R"):
    for group_name, ids in (
        ("upper_lid", EYE_UPPER[side]),
        ("lower_lid", EYE_LOWER[side]),
        ("brow", EYEBROW[side]),
    ):
        missing = [i for i in ids if str(i) not in landmarks]
        if missing:
            raise SystemExit("FAILED: %s %s missing %s" % (side, group_name, missing))

    overlap = set(EYE_UPPER[side]) & set(EYEBROW[side])
    if overlap:
        raise SystemExit("FAILED: %s upper lid overlaps brow %s" % (side, sorted(overlap)))

    check = a.get("checks", {}).get(side, {})
    opening = float(check.get("opening", 0))
    width = float(check.get("eyeWidth", 0))
    separation = float(check.get("minUpperLidToBrow", 0))
    if opening <= 0 or width <= 0:
        raise SystemExit("FAILED: %s eye geometry is degenerate" % side)
    if separation < width * 0.08:
        raise SystemExit("FAILED: %s lid/brow registration collapsed" % side)

print("FACE AUTHORITY PASS")
for side in ("L", "R"):
    c = a["checks"][side]
    print("  %s opening %.6f / width %.6f / lid-brow %.6f"
          % (side, c["opening"], c["eyeWidth"], c["minUpperLidToBrow"]))
