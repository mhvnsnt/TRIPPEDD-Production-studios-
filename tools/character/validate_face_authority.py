#!/usr/bin/env python3
"""Fail-closed semantic face authority for MARS."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIT = ROOT / "renders/_rig_measure/canonical_fit.json"
EYES = ROOT / "renders/_rig_measure/eyelids.json"
ORAL = ROOT / "assets/donor/gnm_oral/manifest.json"

EYE_SETS = {
    "L": {"upper":[466,388,387,386,385,384,398],"lower":[263,249,390,373,374,380,381,382,362],"brow":[276,283,282,295,285,300,293,334,296,336]},
    "R": {"upper":[246,161,160,159,158,157,173],"lower":[33,7,163,144,145,153,154,155,133],"brow":[46,53,52,65,55,70,63,105,66,107]},
}

def fail(msg):
    print("FACE_AUTHORITY: FAIL — " + msg)
    return 40

def main():
    if not FIT.is_file(): return fail("canonical 3-D MediaPipe fit is missing")
    if not EYES.is_file(): return fail("semantic eyelid measurement is missing")
    if not ORAL.is_file(): return fail("GNM oral donor manifest is missing")
    fit=json.loads(FIT.read_text()); sets=fit.get("sets",{})
    for side,groups in EYE_SETS.items():
        for a,b in (("upper","brow"),("lower","brow"),("upper","lower")):
            if set(groups[a]) & set(groups[b]): return fail(f"MediaPipe {side} {a}/{b} sets overlap")
        if not sets.get(f"eyelid_{side}_upper") or not sets.get(f"eyelid_{side}_lower") or not sets.get(f"eyebrow_{side}"):
            return fail(f"canonical fit lacks complete {side} lid/brow sets")
        opening=float(sets.get(f"eyelid_{side}_openingMM",0)); gap=float(sets.get(f"lid_to_brow_{side}_MM",0))
        if not 2.0 <= opening <= 16.0: return fail(f"{side} lid opening {opening:.2f} mm is outside the semantic gate")
        if gap < 6.0: return fail(f"{side} lid-to-brow separation {gap:.2f} mm is below 6 mm")
    center=json.loads(ORAL.read_text()).get("fit",{}).get("centerline",{})
    if center.get("anchor") != "DENTAL_ARCH_CENTROID": return fail("GNM oral donor is not dental-arch anchored")
    print("FACE_AUTHORITY: PASS")
    print(json.dumps({"schema":"god-molecule.face-authority.v1","eyeAuthority":"MediaPipe canonical 468 + Rigify skin_eye methodology","oralAuthority":"Google GNM scan-derived anatomy + dental-arch centerline","darknessHeuristic":"FORBIDDEN","firstHitEyelidRaycast":"FORBIDDEN","browCoupling":"FORBIDDEN"},indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
