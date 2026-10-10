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

_MAIN = main


def _run():
    rc = _MAIN()
    rc2 = linework_agreement()
    return rc or rc2



# ---------------------------------------------------------------------------
# THE CHECK THAT CAN EXPRESS THE FAILURE THE ONE ABOVE CANNOT.
#
# Everything above interrogates canonical_fit.json for INTERNAL consistency:
# do the index sets overlap, is the opening in a plausible range, is the lid far
# enough from the brow. All of that passes happily on a fit that is seated on the
# wrong features entirely -- and MEASURED on 2026-09-12, this one is: MediaPipe's
# FaceLandmarker misfits this face by one feature vertically (brow ring on his
# EYES, lid rings on his CHEEKS, nose ring on his LIP), and the fit was built
# from it, reporting a 0.0000 mm residual while being wrong by up to 38.9 mm.
#
# A fit can only be checked against something OUTSIDE itself. The owner's drawn
# linework is that something.
import json as _json
from pathlib import Path as _Path

_LW3D = ROOT / "renders/_rig_measure/linework_3d.json"
_TOL_MM = 8.0


def linework_agreement():
    """Compare the canonical fit to the owner's own drawn lines, in millimetres.

    NOT_ATTEMPTED when he has not marked a plate yet -- which is reported as
    exactly that, never folded into a PASS.
    """
    if not _LW3D.is_file():
        print("FACE_AUTHORITY/LINEWORK: NOT_ATTEMPTED — no owner linework lifted to 3D "
              "(run tools/character/ingest_linework.py then linework_to_3d.py). "
              "The fit above is unchecked against anything outside itself.")
        return 0
    import math
    lw = _json.loads(_LW3D.read_text()).get("sets", {})
    fit = _json.loads(FIT.read_text()).get("sets", {})
    mm = 0.1930 / 50.0
    worst, worst_name, compared = -1.0, None, 0
    for name, pts in lw.items():
        ref = fit.get(name)
        # linework_3d carries scalar measurements alongside the point sets
        if not isinstance(pts, list) or not pts or not isinstance(pts[0], list): continue
        if not isinstance(ref, list) or not ref or not isinstance(ref[0], list): continue
        # symmetric Hausdorff, both directions -- one direction alone can be small
        # while the other is large, which is exactly how a short line hiding inside
        # a long one reads as agreement
        d = max(
            max(min(math.dist(a, b) for b in ref) for a in pts),
            max(min(math.dist(b, a) for a in pts) for b in ref),
        ) / mm
        compared += 1
        if d > worst: worst, worst_name = d, name
    # a PERFECT match must not read as "nothing was checked" -- count the
    # comparisons, never infer them from the size of the disagreement
    if compared == 0:
        print("FACE_AUTHORITY/LINEWORK: NOT_ATTEMPTED — no set names in common")
        return 0
    if worst > _TOL_MM:
        print("FACE_AUTHORITY/LINEWORK: FAIL — canonical_fit disagrees with the owner's "
              "drawn line by %.1f mm at %s (tolerance %.1f mm). HIS MARKS ARE THE "
              "AUTHORITY (OWNER LAW #5); the fit is what must move." % (worst, worst_name, _TOL_MM))
        return 41
    print("FACE_AUTHORITY/LINEWORK: PASS — worst disagreement with the owner's drawn "
          "lines %.1f mm at %s" % (worst, worst_name))
    return 0


if __name__ == "__main__":
    raise SystemExit(_run())
