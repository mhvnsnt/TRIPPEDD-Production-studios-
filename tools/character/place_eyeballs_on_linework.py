"""
THE EYEBALLS EXIST AND THEY ARE ON HIS CHEEKS. PUT THEM ON HIS EYES.

Owner: "we DID make the eye/eyeball/optic geometry earlier ... don't mark eyeball
clearance as permanently NOT_ATTEMPTED ... find the earlier artifact."

He was right, and the artifact is `assets/donor/gnm_eyes/eye_{L,R}.npz` -- 1,926
vertices and 3,714 triangles per globe, an ICT-FaceKit eye assembly warped onto his
head. So clearance is not NOT_ATTEMPTED for lack of geometry.

MEASURED, BEFORE ANY OF IT COULD BE USED:

    eye_L centre is 82.54 mm from the centroid of the eyelid lines he drew
    eye_R centre is 81.81 mm; nearest globe VERTEX to his lid line, 55 mm

That is the same failure as everything else in this saga. The globes were placed
through `canonical_fit.json`, which is built from MediaPipe's landmarks, and
MediaPipe misfits this face by one whole feature vertically -- its eyelid rings land
on his CHEEKS. The globes inherited it. Running a blink clearance test against them
would have measured a lid against an eyeball that is 8 centimetres away and reported
a beautifully clean result.

THE GLOBE GEOMETRY IS NOT TOUCHED. Owner: "Do not touch the good eyeball geometry to
make the eyelids win." This applies a RIGID transform only -- the globe keeps its
shape, its radius and its own axes; it is moved onto the aperture his drawn lines
define, and the residual is reported.

WHERE A GLOBE BELONGS, derived rather than dialled:
  centre = (centroid of his upper+lower lid lines) pushed back along the head's
           inward normal by the globe's own measured radius, less the corneal
           protrusion that keeps the cornea flush with the lid aperture.
The radius is the globe's, not a number I picked; the direction is his head frame's
forward axis, not a traversal-order cross product.

    vendor/blender/blender -b -P tools/character/place_eyeballs_on_linework.py --
"""
import bpy, sys, os, json
import numpy as np

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("place_eyeballs_on_linework.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
MM = FP.MM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

# how far the cornea stands proud of the lid aperture plane. Anatomically the cornea
# is roughly flush with the lid margins in a neutral open eye; this is the one number
# that is a choice and it is stated rather than buried.
CORNEA_MM = float(opt("--cornea-mm", "1.5"))
# AUTO-DEPTH. Placing the globe with a chosen corneal protrusion put it THROUGH his
# lid margin at rest: measured, 11 verts on the left margin and 16 on the right sat
# inside the globe, deepest -3.08 mm -- and the giveaway was that the OLD blink key,
# which travels 0.00 apertures and moves nothing at all, reported the same
# penetration. A shape that does not move cannot cause a collision, so the collision
# was already there in the neutral pose. The depth is therefore SOLVED from his own
# lid margin rather than dialled: slide the globe along the head's inward axis until
# the closest margin vertex clears it by REST_CLEAR_MM.
AUTO = "--no-auto-depth" not in argv
REST_CLEAR_MM = float(opt("--rest-clearance-mm", "0.5"))
SAVE = "--no-save" not in argv

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"))
LW = json.load(open(os.path.join(ROOT, "docs/evidence/linework/linework_3d.json")))
S = {k: np.array(v, dtype=float) for k, v in LW["sets"].items()
     if isinstance(v, list) and len(v) and isinstance(v[0], list)}
fit, sets, canon = FP.load_fit(ROOT)
hx, hup, hfwd = FP.head_frame(sets)
inward = -np.asarray(hfwd, float)          # into the head
inward /= np.linalg.norm(inward)

report = {"schema": "trippedd.eyeball-placement/v1",
          "authority": "docs/evidence/linework/linework_3d.json -- the lines the OWNER drew",
          "corneaProtrusionMM": CORNEA_MM,
          "note": "RIGID placement only. The globe geometry, radius and axes are "
                  "unchanged; only where it sits was wrong.",
          "eyes": {}}

for side in ("L", "R"):
    p = os.path.join(ROOT, "assets/donor/gnm_eyes/eye_%s.npz" % side)
    if not os.path.exists(p):
        die("eye_%s.npz is missing. The globe is a real artifact in this repo and its "
            "absence is a retrieval failure, not a reason to skip the clearance gate." % side)
    z = np.load(p)
    V = z["vertices"].astype(float)
    F = z["triangles"].astype(np.int32)
    # THE RADIUS IS FITTED, NOT ASSUMED. Using centroid + max-vertex-distance gave
    # 15.74 mm on the left where a least-squares sphere fit gives 9.57 mm, and put the
    # "centre" 3.90 mm off the real one -- the assembly carries a corneal bulge, so its
    # farthest vertex is not its radius. That error is why the depth solve ran to its
    # 12 mm limit and still reported the lid 1.63 mm inside the globe.
    A_ = np.hstack([2 * V, np.ones((len(V), 1))])
    b_ = (V ** 2).sum(1)
    x_, *_ = np.linalg.lstsq(A_, b_, rcond=None)
    old_c = x_[:3]
    radius = float(np.sqrt(x_[3] + (old_c ** 2).sum()))
    _res = np.abs(np.linalg.norm(V - old_c, axis=1) - radius)
    print("eye %s: sphere fit radius %.2f mm (residual mean %.2f / p95 %.2f mm -- the "
          "assembly is not a perfect ball, so clearance is measured against the SURFACE "
          "direction by direction, not against this sphere)"
          % (side, radius / MM, _res.mean() / MM, np.percentile(_res, 95) / MM), flush=True)

    up_line = S["eyelid_%s_upper" % side]; lo_line = S["eyelid_%s_lower" % side]
    ap_pts = np.vstack([up_line, lo_line])
    ap_c = ap_pts.mean(0)
    new_c = ap_c + inward * (radius - CORNEA_MM * MM)
    solved = None
    if AUTO:
        # his lid margin, from his own drawn upper line, on the real mesh
        mesh = bpy.data.objects["MARS_MESH"]
        dg = bpy.context.evaluated_depsgraph_get()
        ev = mesh.evaluated_get(dg); me_ = ev.to_mesh()
        n_ = len(me_.vertices); co_ = np.empty(n_ * 3); me_.vertices.foreach_get("co", co_)
        Wm = np.array(ev.matrix_world)
        MW_ = co_.reshape(n_, 3) @ Wm[:3, :3].T + Wm[:3, 3]
        ev.to_mesh_clear()
        a_ = up_line[:-1]; b_ = up_line[1:]; ab_ = b_ - a_
        L2_ = np.einsum("ij,ij->i", ab_, ab_); L2_[L2_ == 0] = 1e-12
        dl = np.empty(len(MW_))
        for i_, q_ in enumerate(MW_):
            t_ = np.clip(np.einsum("ij,ij->i", q_ - a_, ab_) / L2_, 0.0, 1.0)
            dl[i_] = np.linalg.norm(a_ + ab_ * t_[:, None] - q_, axis=1).min()
        marg = MW_[dl <= 3.0 * MM]
        if len(marg) < 10:
            die("eye %s: only %d mesh vertices within 3 mm of his upper lid line" %
                (side, len(marg)))
        # CLEARANCE AGAINST THE ACTUAL SURFACE, DIRECTION BY DIRECTION. The globe is
        # star-shaped about its fitted centre but it is not a sphere, so "distance to
        # centre minus radius" would under-report the cornea and over-report the back.
        # For each margin vertex, look up the globe's own radius ALONG THAT DIRECTION.
        def surface_clear(c_try):
            rel = V - old_c
            rl = np.linalg.norm(rel, axis=1); rl[rl == 0] = 1e-12
            dirs = rel / rl[:, None]
            out = []
            for q in marg:
                v = q - c_try
                n = np.linalg.norm(v)
                if n < 1e-9: return -1e9
                u = v / n
                cosang = dirs @ u
                sel = cosang > 0.93                 # ~21 deg cone
                if not sel.any():
                    sel = cosang >= np.partition(cosang, -8)[-8]
                out.append(n - float(rl[sel].max()))
            return float(min(out)) / MM
        lo_, hi_ = -6.0, 30.0                      # mm of extra push-back to search
        for _ in range(26):
            mid = 0.5 * (lo_ + hi_)
            c_try = ap_c + inward * (radius - CORNEA_MM * MM + mid * MM)
            if surface_clear(c_try) < REST_CLEAR_MM: lo_ = mid
            else: hi_ = mid
        solved = 0.5 * (lo_ + hi_)
        new_c = ap_c + inward * (radius - CORNEA_MM * MM + solved * MM)
        final_clear = surface_clear(new_c)
        print("eye %s: auto-depth pushed the globe back %.2f mm -> rest margin "
              "clearance %.3f mm" % (side, solved, final_clear), flush=True)
        if final_clear < REST_CLEAR_MM - 0.05:
            die("eye %s: could not reach %.2f mm rest clearance even at the search "
                "limit (best %.3f mm). The globe may be larger than his aperture can "
                "accommodate, which is a real finding and not something to round away."
                % (side, REST_CLEAR_MM, final_clear))
    Vn = V - old_c + new_c

    before = float(np.linalg.norm(old_c - ap_c)) / MM
    after = float(np.linalg.norm(new_c - ap_c)) / MM
    near_before = float(min(np.linalg.norm(V - q, axis=1).min() for q in ap_pts)) / MM
    near_after = float(min(np.linalg.norm(Vn - q, axis=1).min() for q in ap_pts)) / MM

    name = "MARS_EYE_%s" % side
    if name in bpy.data.objects:
        ob = bpy.data.objects[name]
        bpy.data.objects.remove(ob, do_unlink=True)
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in Vn], [], [tuple(t) for t in F])
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    # follow the head like every other part does
    arm = next((a for a in bpy.data.objects if a.type == "ARMATURE"), None)
    if arm and "head" in arm.pose.bones:
        g = ob.vertex_groups.new(name="head")
        g.add(list(range(len(Vn))), 1.0, "REPLACE")
        m = ob.modifiers.new("EYE_ARM", "ARMATURE"); m.object = arm

    report["eyes"][side] = {
        "verts": int(len(V)), "tris": int(len(F)),
        "radiusMM": round(radius / MM, 3),
        "centreToHisApertureMM_before": round(before, 2),
        "centreToHisApertureMM_after": round(after, 2),
        "nearestGlobeVertToHisLidMM_before": round(near_before, 2),
        "nearestGlobeVertToHisLidMM_after": round(near_after, 2),
        "object": name,
        "autoDepthPushBackMM": round(solved, 3) if solved is not None else None,
    }
    print("eye %s: radius %.2f mm | centre->his aperture %.2f -> %.2f mm | "
          "nearest globe vert->his lid %.2f -> %.2f mm"
          % (side, radius / MM, before, after, near_before, near_after), flush=True)
    if after > before:
        die("eye %s: the placement moved the globe FURTHER from his own aperture "
            "(%.2f -> %.2f mm). Refusing to bank a worse fit." % (side, before, after))

if SAVE:
    out = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    print("saved %s" % out, flush=True)
od = os.path.join(ROOT, "docs", "evidence", "blink_own")
os.makedirs(od, exist_ok=True)
json.dump(report, open(os.path.join(od, "eyeball_placement.json"), "w"), indent=2)
print("wrote %s" % os.path.join(od, "eyeball_placement.json"), flush=True)
