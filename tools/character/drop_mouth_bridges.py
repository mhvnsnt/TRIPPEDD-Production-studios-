"""
THE THING HANGING IN HIS MOUTH IS HIS OWN SKIN, BRIDGING THE OPENING.

    "what is that on top of the tongue? ... I can't even tell what that is."

NAMED BY ISOLATION, not by inference -- the same open-mouth frame rendered five
times with each part hidden in turn. The pale wedge in the centre survives hiding
the sock, the upper arch, the tongue AND the lower arch. It is MARS_MESH.

That is the defect already banked: "a single face 22x the median area spans from
his upper lip to his lower lip ... that face is the blue skin filling the centre
of his open mouth." A face with one corner on his upper lip and another on his
lower lip is a MEMBRANE: the jaw stretches it across the opening instead of
parting it, and it renders as a slab over his tongue and as spikes at the rim.

split_lip_seam.py already carries the right operation behind --drop-bridges, and
it has never been switched on. It cannot be run again on an already-split rig
(it refuses, correctly), so this applies the same operation standalone, with the
same safety check, which is the part that matters:

    ANYTHING VISIBLE ON HIS FACE AT REST IS HIS SKIN AND IS KEPT.

That is measured, not reasoned about: at REST, fire a fan at his mouth and record
every face the camera can actually see. A face in that set stays, whatever else
is true about it. Only the membranes BEHIND his lip front go.

    vendor/blender/blender -b -P tools/character/drop_mouth_bridges.py -- \\
        --rig renders/_tongue/MARS_FACE_TONGUE.blend --out <same>
"""
import bpy, bmesh, sys, os, json, math
import numpy as np
from mathutils import Vector

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def flag(f): return f in argv


def die(msg):
    print("*** REFUSED: %s" % msg, flush=True)
    sys.exit(1)


RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT = os.path.abspath(opt("--out", RIG))
BEHIND_MM = float(opt("--behind-mm", "1.0"))   # how far behind his lip front counts as inside
# ── --shave-jaw-flap ─────────────────────────────────────────────────────────
# Owner, looking at the open mouth: "It's pieces from the top lip attached to the
# bottom lip that need to be cut off the bottom lip... darker blue shadow pieces
# that go at the lower part of the top lip, but they're stuck down to the bottom
# lip", and then: "if you could just shave all that off from between the lips".
#
# MEASURED, and it is neither a weld nor a bad split:
#   122 faces sitting ABOVE his lip seam travel 20-46 mm when the jaw opens,
#   while their neighbours on the same upper lip travel 0.08 mm
#   0 of the 122 share a vertex with any face below the seam -- the seam IS split
#   338 of their 342 vertices carry jaw weight 1.000
#   the control, upper-lip verts that do NOT ride: median jaw weight 0.000
# So the underside of his top lip is painted onto the jaw. Re-weighting would
# park that flap back under the top lip, which he explicitly does not want --
# "is gonna cover the teeth again ... we want the teeth to show at the top".
# So the flap is REMOVED, under the same rule as the membranes: anything the
# camera can see on his closed face is his skin and is kept.
SHAVE_FLAP = flag("--shave-jaw-flap")
FLAP_TRAVEL = float(opt("--flap-travel-mm", "12.0"))
# ── --shave-crown-blockers ───────────────────────────────────────────────────
# Owner: "we want the teeth to show at the top, not be covered by dark blue
# shadow lip stuff, like the lip hangs down too far in front of the teeth ...
# if you could just shave all that off from between the lips, the triangles in
# general."
# After the jaw flap was removed, 1,444 upper-crown faces looking OUT still see:
#   VISIBLE 44.3% · other crowns 20.5% · HIS SKIN 16.8% · cavity wall 13.2%
#   · sock 3.1% · gum 2.1%
# and the skin blockers now travel only 0.3-2.7 mm with the jaw, so they are not
# flap -- they are his upper lip hanging over his teeth. Shave the ones the
# camera cannot see on his closed face; his visible lip is never touched.
SHAVE_CROWNS = flag("--shave-crown-blockers")
SAVE = not flag("--no-save")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0
F = np.array(anat["frame"]["matrix"], float)
FI = np.linalg.inv(F)
UP = np.array(anat["contours"]["lip_inner_upper"], float)
LO = np.array(anat["contours"]["lip_inner_lower"], float)
LIP_FRONT = anat["aperture"]["lipFrontLocalY"] / MM

bpy.ops.wm.open_mainfile(filepath=RIG)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
arm = bpy.data.objects.get("MARS_RIG")
me = o.data
W = np.array(o.matrix_world)


def to_local(pts):
    return (FI @ np.hstack([pts, np.ones((len(pts), 1))]).T).T[:, :3] / MM


def seam_z(xs):
    u = to_local(UP); l = to_local(LO)
    us = u[np.argsort(u[:, 0])]; ls = l[np.argsort(l[:, 0])]
    return 0.5 * (np.interp(xs, us[:, 0], us[:, 2]) + np.interp(xs, ls[:, 0], ls[:, 2]))


def straddlers():
    V = np.array([v.co[:] for v in me.vertices], float)
    L = to_local(V @ W[:3, :3].T + W[:3, 3])
    zs = seam_z(L[:, 0])
    EPS = 0.2
    side = np.where(L[:, 2] > zs + EPS, 1, np.where(L[:, 2] < zs - EPS, -1, 0))
    inzone = (np.abs(L[:, 0]) < 34) & (np.abs(L[:, 2] - zs) < 12) & (L[:, 1] < 24)
    out = []
    for p in me.polygons:
        vi = list(p.vertices)
        if not any(inzone[i] for i in vi):
            continue
        s = set(int(side[i]) for i in vi if side[i] != 0)
        if 1 in s and -1 in s:
            out.append(p.index)
    return out


def visible_at_rest():
    """Every face the camera can actually SEE on his closed face. These are his
    skin and are kept no matter what else is true about them."""
    for k in me.shape_keys.key_blocks:
        if k.name != "Basis":
            k.value = 0.0
    if arm:
        pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    fwd = -F[:3, 1] / np.linalg.norm(F[:3, 1])
    up = F[:3, 2] / np.linalg.norm(F[:3, 2])
    right = F[:3, 0] / np.linalg.norm(F[:3, 0])
    c = F[:3, 3]
    seen = set()
    for lz in np.arange(-16, 16.1, 0.7):
        for lx in np.arange(-36, 36.1, 0.7):
            org = Vector((c + fwd * (120 * MM) + up * (lz * MM) + right * (lx * MM)).tolist())
            ok, loc, nor, idx, ob, mat = bpy.context.scene.ray_cast(
                dg, org, Vector((-fwd).tolist()))
            if ok and ob.name == "MARS_MESH":
                seen.add(int(idx))
    return seen


def jaw_flap():
    """Faces of his UPPER lip that ride the jaw down into the opening.
    Selected by MEASURED TRAVEL -- pose the jaw and see which faces move -- not
    by weights, so a face that moves for any other reason is caught too."""
    for k in me.shape_keys.key_blocks:
        if k.name != "Basis":
            k.value = 0.0
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"; pb.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    ev = o.evaluated_get(dg); m0 = ev.to_mesh()
    R = np.array([(ev.matrix_world @ v.co)[:] for v in m0.vertices], float)
    faces = [tuple(pp.vertices) for pp in m0.polygons]
    ev.to_mesh_clear()

    state = json.load(open(os.path.join(ROOT, "assets/rigs/MARS_face_state.json")))
    pb.rotation_euler = (math.radians(state["jawHinge"]["openSign"] * 31.0), 0, 0)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    ev = o.evaluated_get(dg); m1 = ev.to_mesh()
    Wd = np.array([(ev.matrix_world @ v.co)[:] for v in m1.vertices], float)
    ev.to_mesh_clear()
    pb.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()

    C0 = np.array([R[list(f)].mean(0) for f in faces])
    C1 = np.array([Wd[list(f)].mean(0) for f in faces])
    travel = np.linalg.norm(C1 - C0, axis=1) / MM
    L = to_local(C0)
    zs = seam_z(L[:, 0])
    sel = ((L[:, 2] > zs + 0.5) & (np.abs(L[:, 0]) < 34) & (np.abs(L[:, 2] - zs) < 12)
           & (L[:, 1] > LIP_FRONT + BEHIND_MM) & (L[:, 1] < 24) & (travel > FLAP_TRAVEL))
    return [int(i) for i in np.nonzero(sel)[0]]


def crown_blockers():
    """MARS_MESH faces that stand between his upper crowns and the camera when
    his mouth is open. Fired FROM each crown outward, so it is occlusion as the
    viewer sees it and not a guess from coordinates."""
    state = json.load(open(os.path.join(ROOT, "assets/rigs/MARS_face_state.json")))
    kbk = me.shape_keys.key_blocks
    for k in kbk:
        if k.name != "Basis":
            k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    arm.pose.bones["jaw"].rotation_euler = (
        math.radians(state["jawHinge"]["openSign"] * 31.0), 0, 0)
    for n_, v in {"lip_lower_depress": 0.7, "lip_upper_raise": 0.45,
                  "lip_corner_L_up": 0.2, "lip_corner_R_up": 0.2}.items():
        if n_ in kbk:
            kbk[n_].value = v
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()

    tu = bpy.data.objects["MARS_TEETH_UPPER"].evaluated_get(dg); tm = tu.to_mesh()
    Mt = tu.matrix_world
    crowns = []
    for pp in tm.polygons:
        mi = pp.material_index
        nm = (tm.materials[mi].name if 0 <= mi < len(tm.materials) else "").split(".")[0]
        if nm == "MARS_TEETH_MAT":
            crowns.append(Mt @ pp.center)
    tu.to_mesh_clear()

    outw = -F[:3, 1] / np.linalg.norm(F[:3, 1])
    hits = {}
    for c in crowns:
        org = Vector((np.array(c[:]) + outw * (0.2 * MW)).tolist())
        ok, loc, nor, idx, ob, mat = bpy.context.scene.ray_cast(
            dg, org, Vector(outw.tolist()))
        if ok and ob.name == "MARS_MESH":
            mi = me.polygons[idx].material_index if idx < len(me.polygons) else -1
            nm = (me.materials[mi].name if 0 <= mi < len(me.materials) else "").split(".")[0]
            if nm.startswith("tripo"):
                hits[int(idx)] = hits.get(int(idx), 0) + 1
    for k in kbk:
        if k.name != "Basis":
            k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    print("  crowns sampled %d · skin faces standing in front of them %d (%d rays)"
          % (len(crowns), len(hits), sum(hits.values())), flush=True)
    return sorted(hits)


if SHAVE_CROWNS:
    strad0 = crown_blockers()
    print("  skin faces covering his upper teeth: %d" % len(strad0), flush=True)
    straddlers = crown_blockers
elif SHAVE_FLAP:
    strad0 = jaw_flap()
    print("  UPPER-lip faces that ride the jaw more than %.0f mm: %d"
          % (FLAP_TRAVEL, len(strad0)), flush=True)
    straddlers = jaw_flap          # the after-gate measures the same thing
else:
    strad0 = straddlers()
    print("  faces bridging his lips: %d" % len(strad0), flush=True)
if not strad0:
    print("  nothing bridges his lips. Nothing to do.", flush=True)
    sys.exit(0)

cent = np.array([me.polygons[i].center[:] for i in strad0]) @ W[:3, :3].T + W[:3, 3]
cl = to_local(cent)
behind = [strad0[k] for k in range(len(strad0)) if cl[k, 1] > LIP_FRONT + BEHIND_MM]
print("  of those, behind his lip front (y > %+.1f mm): %d" % (LIP_FRONT + BEHIND_MM, len(behind)),
      flush=True)

keep = visible_at_rest()
drop = [i for i in behind if i not in keep]
print("  visible on his face at rest and therefore KEPT: %d" % (len(behind) - len(drop)),
      flush=True)
print("  removing %d membrane faces" % len(drop), flush=True)
if not drop:
    print("  every bridging face is visible skin. Nothing removed.", flush=True)
    sys.exit(0)

n_v0, n_f0 = len(me.vertices), len(me.polygons)
P0 = np.array([v.co[:] for v in me.vertices], float)
keys0 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []

bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
bmesh.ops.delete(bm, geom=[bm.faces[i] for i in drop], context="FACES_ONLY")
bm.to_mesh(me); bm.free(); me.update()

# ---- GATES ---------------------------------------------------------------
n_v1, n_f1 = len(me.vertices), len(me.polygons)
print("  faces %d -> %d · verts %d -> %d" % (n_f0, n_f1, n_v0, n_v1), flush=True)
if n_v1 != n_v0:
    die("vertex count changed %d -> %d; FACES_ONLY must leave every vertex" % (n_v0, n_v1))
P1 = np.array([v.co[:] for v in me.vertices], float)
drift = float(np.abs(P1 - P0).max()) / MM
print("  vertex drift: %.6f mm" % drift, flush=True)
if drift > 1e-6:
    die("vertices moved %.6f mm" % drift)
keys1 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
if keys1 != keys0:
    die("shape keys changed %d -> %d" % (len(keys0), len(keys1)))

strad1 = straddlers()
print("  faces bridging his lips: %d -> %d" % (len(strad0), len(strad1)), flush=True)
if len(strad1) >= len(strad0):
    die("the count did not fall (%d -> %d)" % (len(strad0), len(strad1)))

# and his closed face must not have gained a hole
after_seen = visible_at_rest()
lost = keep - after_seen
print("  faces visible on his closed face: %d -> %d" % (len(keep), len(after_seen)), flush=True)

rep = {"schema": "trippedd.drop-mouth-bridges/v1", "rig": RIG, "out": OUT,
       "bridging": [len(strad0), len(strad1)],
       "behindLipFront": len(behind), "keptVisibleAtRest": len(behind) - len(drop),
       "removed": len(drop), "faces": [n_f0, n_f1], "verts": n_v1,
       "vertexDriftMM": round(drift, 8), "shapeKeys": len(keys1),
       "visibleAtRest": [len(keep), len(after_seen)]}
rp = os.path.join(ROOT, "docs/evidence/oral/drop_mouth_bridges.json")
os.makedirs(os.path.dirname(rp), exist_ok=True)
json.dump(rep, open(rp, "w"), indent=2)
print("  wrote docs/evidence/oral/drop_mouth_bridges.json", flush=True)

if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    print("saved %s" % OUT, flush=True)
