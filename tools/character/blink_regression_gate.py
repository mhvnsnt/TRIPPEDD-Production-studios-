#!/usr/bin/env python3
"""Fail-closed regression gate for the MARS linework-derived blink.

Legacy blink keys remain negative controls. New blink keys are measured against
THEIR OWN local closure distance, not the unrelated line-to-line aperture.
Real eyeball clearance is a separate required gate once an eye assembly is
present; this gate never invents eye geometry or substitutes a global axis.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

LANDING_TOLERANCE_MM = 5.0
MIN_LOCAL_TRAVEL_RATIO = 1.0
LEGACY_MAX_TRAVEL_APERTURES = 0.01


def finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()

    data = json.loads(args.receipt.read_text(encoding="utf-8"))
    records = data.get("channels")
    if not isinstance(records, list) or not records:
        raise SystemExit("FAIL: channels[] is required")

    by_key = {r.get("key"): r for r in records if isinstance(r, dict)}
    for key in ("blink_L", "blink_R", "blink_own_L", "blink_own_R"):
        if key not in by_key:
            raise SystemExit(f"FAIL: missing required regression channel {key}")

    # Legacy controls must remain visibly broken; otherwise the regression
    # fixture has silently changed and no longer proves the old failure.
    for key in ("blink_L", "blink_R"):
        travel = by_key[key].get("travel_apertures")
        if not finite_number(travel) or abs(float(travel)) > LEGACY_MAX_TRAVEL_APERTURES:
            raise SystemExit(f"FAIL: legacy regression control changed: {key}")

    # New keys must hit the authored eyelid line and close >= their own local
    # required distance. The old global line-to-line aperture denominator is
    # deliberately forbidden because it measures the wrong geometry.
    for key in ("blink_own_L", "blink_own_R"):
        rec = by_key[key]
        landing = rec.get("lands_from_lid_line_mm")
        travel = rec.get("margin_travel_mm")
        required = rec.get("local_required_travel_mm")
        ratio = rec.get("travel_ratio")
        if not finite_number(landing):
            raise SystemExit(f"FAIL: {key} has no measured lid-line landing")
        if not finite_number(travel):
            raise SystemExit(f"FAIL: {key} has no measured margin travel")
        if not finite_number(required) or float(required) <= 0.0:
            raise SystemExit(f"FAIL: {key} has no positive local required travel")
        if not finite_number(ratio):
            raise SystemExit(f"FAIL: {key} has no local travel ratio")
        if float(landing) > LANDING_TOLERANCE_MM:
            raise SystemExit(f"FAIL: {key} misses lid line: {landing:.3f} mm")
        if float(ratio) < MIN_LOCAL_TRAVEL_RATIO:
            raise SystemExit(f"FAIL: {key} under-travels locally: {ratio:.3f}x")

    print("PASS: legacy blink controls remain broken and linework blink reaches each local closure target")
    return 0


if __name__ == "__main__":
    sys.exit(main())
