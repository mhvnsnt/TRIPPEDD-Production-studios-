#!/usr/bin/env python3
"""Eye clearance ladder runner for Mars.

Parallel track with live Blender seating. Consumes geometry exported the same
way penetration_measure.py does, enforces the eye clearance contract, and
emits a machine-readable ladder receipt.

Hard rules (from docs/production/EYE_CLEARANCE_CONTRACT.md):
  1. Globe-class only (vertex_class / part mask).
  2. Rest penetration must be resolved before blink travel is trusted.
  3. Local lid travel, not global aperture.
  4. No invented geometry.
  5. PASS requires ladder receipt + reopened render frames.

Usage (after Claude exports contact geometry with eyes present):

  ./.trippedd_venv/bin/python tools/character/eye_clearance_ladder.py \
      geom.npz \
      --lid L_UPPER --globe EYE_L_GLOBE \
      --lid R_UPPER --globe EYE_R_GLOBE \
      --steps open,intermediate,closed \
      --tol-mm 0.5 \
      --out docs/evidence/eye_clearance

Exit:
  0  ladder receipt written (may still contain FAIL/UNKNOWN steps)
  3  REFUSED (missing geometry, missing class filter, or contract violation)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from face_plate import MW, MM
except Exception:
    MW = 0.1930
    MM = MW / 50.0

SCHEMA = "trippedd.eye-clearance-ladder/v1"
CONTRACT = Path(__file__).resolve().parents[2] / "tools/character/eye_clearance_contract.json"


def die(msg: str) -> None:
    print("\n*** REFUSED: %s\n" % msg, file=sys.stderr, flush=True)
    raise SystemExit(3)


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def load_contract() -> dict:
    if not CONTRACT.is_file():
        die("eye_clearance_contract.json missing — run from repo root after the contract commit")
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("geometry", help=".npz from export_contact_geometry.py (eyes present)")
    ap.add_argument("--lid", action="append", default=[],
                    help="lid part name (repeat; order matches --globe)")
    ap.add_argument("--globe", action="append", default=[],
                    help="globe part name (must be globe-class only)")
    ap.add_argument("--steps", default="open,intermediate,closed",
                    help="comma-separated ladder steps present in the geometry frames")
    ap.add_argument("--tol-mm", type=float, default=0.5)
    ap.add_argument("--out", default="docs/evidence/eye_clearance")
    ap.add_argument("--label", default="eye_clearance")
    args = ap.parse_args()

    contract = load_contract()
    if not contract.get("classFilter", {}).get("required", True):
        die("contract classFilter.required must be true")

    if len(args.lid) != len(args.globe) or not args.lid:
        die("provide matching --lid / --globe pairs (one per eye)")

    if not os.path.isfile(args.geometry):
        die("geometry file not found: %s" % args.geometry)

    z = np.load(args.geometry, allow_pickle=False)
    parts = [str(p) for p in z["__parts__"]]
    frames = list(z["__frames__"])
    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    if not steps:
        die("--steps produced an empty list")

    # Basic presence check — detailed penetration uses the existing
    # penetration_measure.py path (libigl). This runner enforces contract shape
    # and writes the ladder receipt the live track must fill.
    src_hash = sha256(args.geometry)
    os.makedirs(args.out, exist_ok=True)

    eyes = []
    for lid_name, globe_name in zip(args.lid, args.globe):
        if lid_name.replace(":", "__") not in parts and lid_name not in parts:
            die("lid part '%s' not in geometry. Available: %s" % (lid_name, parts))
        if globe_name.replace(":", "__") not in parts and globe_name not in parts:
            die("globe part '%s' not in geometry. Available: %s" % (globe_name, parts))
        eyes.append({"lid": lid_name, "globe": globe_name})

    # Skeleton receipt — live track fills measured fields after running
    # penetration_measure with the same pairs + class filter.
    receipt = {
        "schema": SCHEMA,
        "contract": "trippedd.eye-clearance-contract/v1",
        "sourceGeometry": os.path.relpath(args.geometry),
        "sourceHash": src_hash,
        "toleranceMM": args.tol_mm,
        "classFilter": "globe_only",
        "restBeforeBlink": True,
        "steps": steps,
        "eyes": [],
        "baseline_mm": contract.get("baseline_mm", {}),
        "status": "PENDING_MEASUREMENT",
        "note": (
            "Skeleton receipt. Run penetration_measure.py on the same geometry "
            "with globe-class pairs, then merge minClearanceMM / penetrationSamples "
            "per step. Rest penetration must be 0 (or documented residual) before "
            "blink travel is trusted. Render frames required for PASS."
        ),
    }

    for eye in eyes:
        steps_out = []
        for step in steps:
            steps_out.append({
                "step": step,
                "minClearanceMM": None,
                "penetrationSamples": None,
                "localTravelMM": None,
                "renderPath": None,
                "renderSHA256": None,
                "classFilter": "globe_only",
                "status": "PENDING",
            })
        receipt["eyes"].append({
            "lid": eye["lid"],
            "globe": eye["globe"],
            "steps": steps_out,
        })

    out_path = os.path.join(args.out, "%s_ladder.json" % args.label)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)
        fh.write("\n")

    print("eye clearance ladder skeleton -> %s" % out_path)
    print("schema: %s" % SCHEMA)
    print("eyes: %d  steps: %s" % (len(eyes), ",".join(steps)))
    print("NEXT: run penetration_measure on globe-class pairs, fill measured fields,")
    print("      attach reopened render frames, then re-evaluate for PASS.")
    print("Contract: tools/character/eye_clearance_contract.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
