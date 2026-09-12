#!/usr/bin/env python3
"""Fail-closed gate for the MARS oral centerline.

The visible tooth/cavity seam must be centered on the measured mouth, not on
the donor's lip-band centroid. This catches the asymmetric "snarl" failure
before any mouth render can be promoted.

Usage:
  python tools/character/validate_mars_oral_centerline.py \
    --manifest assets/donor/gnm_oral/manifest.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--max-correction", type=float, default=0.020,
                    help="maximum allowed donor-frame lateral correction in native units")
    args = ap.parse_args()

    if not args.manifest.is_file():
        print("ORAL_CENTERLINE: BLOCKED — donor manifest missing")
        return 40

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    fit = data.get("fit", {})
    center = fit.get("centerline", {})
    if center.get("anchor") != "DENTAL_ARCH_CENTROID":
        print("ORAL_CENTERLINE: FAIL — donor is not anchored on the dental arch")
        return 41

    correction = abs(float(center.get("donorLocalX", 0.0)))
    if correction > args.max_correction:
        print(f"ORAL_CENTERLINE: FAIL — correction {correction:.6f} exceeds {args.max_correction:.6f}")
        return 42

    print("ORAL_CENTERLINE: PASS")
    print(json.dumps({
        "schema": "god-molecule.oral-centerline.v1",
        "anchor": center.get("anchor"),
        "donorLocalXCorrection": correction,
        "target": center.get("target"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
