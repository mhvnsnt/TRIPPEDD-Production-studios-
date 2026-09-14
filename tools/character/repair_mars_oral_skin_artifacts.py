#!/usr/bin/env python3
"""Recover the MARS mouth *skin* from the pre-retopo checkpoint without replacing
the newer GNM oral stack.

This is deliberately broader than a lip-seam fix. It repairs the bounded oral
skin/deformation region: base positions, all shape-key positions by the same
delta (preserving expression deltas), and jaw/head weights. It never replaces
MARS_TEETH_*, MARS_GUM_*, MARS_TONGUE, MARS_MOUTH_SOCK or the cavity objects.

Input:
  --target current MARS_FACE.blend
  --skin-donor checkpoint MARS_FACE.blend
Output:
  --out review blend

The donor and target must have identical MARS_MESH topology. If they do not,
the tool REFUSES rather than guessing a correspondence.
"""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]

def die(msg):
    print("\n*** REFUSED: " + msg, flush=True)
    raise SystemExit(45)

def parse():
    ap=argparse.ArgumentParser()
    ap.add_argument("--target", default=str(ROOT/"assets/rigs/MARS_FACE.blend"))
    ap.add_argument("--skin-donor", default=str(ROOT/"assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_FACE.blend"))
    ap.add_argument("--mouth-frame", default=str(ROOT/"renders/_rig_measure/mouth_anatomy.json"))
    ap.add_argument("--out", default=str(ROOT/"assets/variants/MARS_FACE_ORAL_SKIN_RECOVERY_REVIEW.blend"))
    ap.add_argument("--influence-mm", type=float, default=10.0)
    ap.add_argument("--interior-extra-mm", type=float, default=12.0)
    ap.add_argument("--dry-run", action="store_true")
    return ap.parse_args()

def append_donor(path):
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        names = [n for n in src.objects if n == "MARS_MESH"]
        if not names: die("skin donor has no MARS_MESH")
        dst.objects = names
    ob = dst.objects[0]
    if ob is None: die("failed to append donor MARS_MESH")
    return ob

def world_to_local(frame_inv, p):
    return frame_inv @ (p if isinstance(p, Vector) else Vector(p))

def main():
    a=parse()
    target=Path(a.target).resolve()
    donor_path=Path(a.skin_donor).resolve()
    frame_path=Path(a.mouth_frame).resolve()
    if not target.is_file(): die("target blend missing: "+str(target))
    if not donor_path.is_file(): die("skin donor missing: "+str(donor_path))
    if not frame_path.is_file(): die("mouth frame missing: "+str(frame_path))

    bpy.ops.wm.open_mainfile(filepath=str(target))
    t=bpy.data.objects.get("MARS_MESH")
    if not t: die("target has no MARS_MESH")
    oral_names=("MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE","MARS_MOUTH_SOCK")
    oral_before={n:bpy.data.objects.get(n) is not None for n in oral_names}

    frame=json.loads(frame_path.read_text())
    A=frame["aperture"]
    MW=float(A["width"]); MM=MW/50.0
    F=Matrix(frame["frame"]["matrix"]); Fi=F.inverted()
    lip_front=float(A["lipFrontLocalY"]); deepest=float(A["deepestLocalY"])
    extra=a.interior_extra_mm*MM
    influence=a.influence_mm*MM

    donor=append_donor(str(donor_path))
    if len(t.data.vertices)!=len(donor.data.vertices):
        die("target/donor vertex counts differ: %d vs %d"%(len(t.data.vertices),len(donor.data.vertices)))
    if len(t.data.polygons)!=len(donor.data.polygons):
        die("target/donor face counts differ: %d vs %d"%(len(t.data.polygons),len(donor.data.polygons)))
    for i,(pf,pd) in enumerate(zip(t.data.polygons,donor.data.polygons)):
        if tuple(pf.vertices)!=tuple(pd.vertices):
            die("target/donor topology differs at face %d"%i)

    def local(i):
        return Fi @ (t.matrix_world @ t.data.vertices[i].co)

    # Two bounded zones:
    # 1) seam influence: restore skin weights around the measured lip contour.
    # 2) oral interior: restore skin positions/weights where skin is appearing
    # inside the mouth, including the roof/tongue volume the screenshots expose.
    xlo=min(float(A["cornerLeft"][0]),float(A["cornerRight"][0]))-extra
    xhi=max(float(A["cornerLeft"][0]),float(A["cornerRight"][0]))+extra
    zlo=min(float(p[2]) for p in frame["contours"]["lip_inner_lower"])-extra
    zhi=max(float(p[2]) for p in frame["contours"]["lip_inner_upper"])+extra

    indices=[]
    for i in range(len(t.data.vertices)):
        p=local(i)
        # inside/near the mouth aperture in its measured frame
        if xlo <= (F@p).x <= xhi and zlo <= (F@p).z <= zhi and p.y >= lip_front-influence and p.y <= deepest+extra:
            indices.append(i)

    # Also include a narrow seam-distance band using the actual measured contour.
    contour=[Vector(p) for p in frame["contours"]["lip_inner_upper"]+frame["contours"]["lip_inner_lower"]]
    def dcont(w):
        return min((w-q).length for q in contour)
    for i in range(len(t.data.vertices)):
        if i in indices: continue
        w=t.matrix_world@t.data.vertices[i].co
        if dcont(w)<=influence:
            indices.append(i)
    indices=sorted(set(indices))
    if len(indices)<100: die("bounded mouth recovery selected only %d vertices"%len(indices))

    # Current and donor must agree outside the selected repair region; this makes
    # the operation a surgical replacement rather than a hidden whole-head swap.
    selected=set(indices)
    outside_drift=0.0
    for i in range(len(t.data.vertices)):
        if i in selected: continue
        outside_drift=max(outside_drift,(t.data.vertices[i].co-donor.data.vertices[i].co).length/MM)
    print("target/donor topology: identical (%d verts, %d faces)"%(len(t.data.vertices),len(t.data.polygons)),flush=True)
    print("bounded oral-skin recovery selection: %d verts (%.1f%% of head)"%(len(indices),100*len(indices)/len(t.data.vertices)),flush=True)
    print("outside-selection donor/target base drift: %.6f mm"%outside_drift,flush=True)

    if a.dry_run:
        print("DRY_RUN: no blend written",flush=True); return 0

    # Preserve the current rig's shape keys by translating EVERY key vertex by the
    # same base correction. This restores the clean skin surface without erasing
    # the newer expression library.
    keys=t.data.shape_keys.key_blocks if t.data.shape_keys else []
    dbase={}
    for i in indices:
        d=(donor.data.vertices[i].co-t.data.vertices[i].co)
        dbase[i]=d
        t.data.vertices[i].co=donor.data.vertices[i].co
    for kb in keys:
        if kb.name=="Basis": continue
        for i,d in dbase.items():
            kb.data[i].co += d

    # Restore only the deformation groups that can pull skin into the mouth.
    # Do not touch other facial groups or any oral object.
    for gname in ("jaw","head"):
        tg=t.vertex_groups.get(gname); dg=donor.vertex_groups.get(gname)
        if not tg or not dg: die("missing jaw/head group in target or donor")
        for i in indices:
            vals=[g.weight for g in donor.data.vertices[i].groups if g.group==dg.index]
            w=vals[0] if vals else 0.0
            tg.add([i],w,"REPLACE")

    # Carry surface shading flags for selected faces only. Do not alter material
    # slots/indices: current oral material layout is protected.
    touched_faces=0
    for p in t.data.polygons:
        if any(v in selected for v in p.vertices):
            dp=donor.data.polygons[p.index]
            p.use_smooth=dp.use_smooth
            touched_faces+=1

    # Remove donor object; no donor geometry becomes part of the final scene.
    bpy.data.objects.remove(donor,do_unlink=True)

    # Assert protected oral objects survived.
    for n,was in oral_before.items():
        if was and bpy.data.objects.get(n) is None:
            die("protected oral object disappeared: "+n)

    t.data.update()
    out=Path(a.out).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))

    report={
      "schema":"god-molecule.mars-oral-skin-recovery/v1",
      "status":"REVIEW_ONLY",
      "target":str(target),
      "skinDonor":str(donor_path),
      "mouthFrame":str(frame_path),
      "selection":{"vertices":len(indices),"influenceMM":a.influence_mm,"interiorExtraMM":a.interior_extra_mm},
      "topology":{"vertices":len(t.data.vertices),"faces":len(t.data.polygons),"identicalToDonor":True},
      "basePositionRecovery":{"vertices":len(dbase),"outsideSelectionDriftMM":outside_drift},
      "shapeKeys":{"count":len(keys)-1 if keys else 0,"baseDeltaAppliedToAllKeys":True},
      "weights":{"groups":["jaw","head"],"vertices":len(indices)},
      "shading":{"facesTouched":touched_faces,"materialsChanged":False},
      "protectedOralObjects":oral_before,
      "canonicalWritten":False,
      "nextGates":["mouth_truth","aperture_survey","oral_render_visibility","human_review"],
      "reason":"broad oral-skin artifact recovery; not a lip-seam-only operation"
    }
    rp=out.with_suffix(".json"); rp.write_text(json.dumps(report,indent=2)+"\n")
    print("REVIEW_BLEND="+str(out),flush=True)
    print("REPORT="+str(rp),flush=True)
    print("PROTECTED_ORAL_STACK=PRESERVED",flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
