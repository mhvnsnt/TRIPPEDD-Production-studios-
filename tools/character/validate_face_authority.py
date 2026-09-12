#!/usr/bin/env python3
"""Fail-closed semantic face authority for MARS."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FIT=ROOT/"renders/_rig_measure/canonical_fit.json"
EYES=ROOT/"renders/_rig_measure/eyelids.json"
ORAL=ROOT/"assets/donor/gnm_oral/manifest.json"
EYE_SETS={
"L":{"upper":[466,388,387,386,385,384,398],"lower":[263,249,390,373,374,380,381,382,362],"brow":[276,283,282,295,285,300,293,334,296,336]},
"R":{"upper":[246,161,160,159,158,157,173],"lower":[33,7,163,144,145,153,154,155,133],"brow":[46,53,52,65,55,70,63,105,66,107]}}
def fail(msg): print("FACE_AUTHORITY: FAIL — "+msg); return 40
def main():
    if not FIT.is_file(): return fail("canonical 3-D MediaPipe fit missing")
    if not EYES.is_file(): return fail("semantic eyelid measurement missing")
    if not ORAL.is_file(): return fail("GNM oral donor manifest missing")
    sets=json.loads(FIT.read_text()).get("sets",{})
    for s,g in EYE_SETS.items():
        for a,b in (("upper","brow"),("lower","brow"),("upper","lower")):
            if set(g[a])&set(g[b]): return fail(f"MediaPipe {s} {a}/{b} sets overlap")
        if not sets.get(f"eyelid_{s}_upper") or not sets.get(f"eyelid_{s}_lower") or not sets.get(f"eyebrow_{s}"): return fail(f"{s} semantic sets missing")
        if not 2<=float(sets.get(f"eyelid_{s}_openingMM",0))<=16: return fail(f"{s} lid opening outside gate")
        if float(sets.get(f"lid_to_brow_{s}_MM",0))<6: return fail(f"{s} lid/brow gap below 6 mm")
    c=json.loads(ORAL.read_text()).get("fit",{}).get("centerline",{})
    if c.get("anchor")!="DENTAL_ARCH_CENTROID": return fail("oral donor is not dental-arch anchored")
    print("FACE_AUTHORITY: PASS")
    return 0
if __name__=="__main__": raise SystemExit(main())
