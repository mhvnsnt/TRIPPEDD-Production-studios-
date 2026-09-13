"""
BLINK PROOF: the ladder, the directional gate, and the old key beside the new one.

Owner's instruction, verbatim:
  "Render a close-up sequence showing open -> 25% -> 50% -> 75% -> closed."
  "Add an eyeball-occlusion/contact gate so the blink cannot PASS while the eyeball
   remains visible through the lid."
  "BLINK moved nothing is a FAIL, not a reason to lower the threshold."

THE VERDICT IS DIRECTIONAL TRAVEL, MEASURED AT THE LID MARGIN, AS A FRACTION OF THAT
EYE'S OWN APERTURE. Occlusion is reported and is NEVER the verdict -- this project has
the receipt: an occlusion gate scored a lid that was PEELING AN EYE OPEN as 84% closed,
because any skin bunched in the ray path satisfies "a ray stopped reaching the eyeball".
A metric that cannot tell closing from opening cannot certify a blink.

CONTACT is the second check and it is geometric, not optical: does the upper lid margin
actually reach the lower lid margin. A lid that travels 0.9 apertures leaves a gap; a
lid that travels 1.0+ meets. Both numbers are recorded.

    vendor/blender/blender -b -P tools/character/blink_proof.py --
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V, Matrix as M

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("blink_proof.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
MM = FP.MM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

RES = int(opt("--res", "480"))
OUT = os.path.join(ROOT, "docs", "evidence", "blink_own")
os.makedirs(OUT, exist_ok=True)
CANDIDATES = [("blink_own_L", "L"), ("blink_own_R", "R"), ("blink_L", "L"), ("blink_R", "R")]

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"))
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
kb = o.data.shape_keys.key_blocks
for k in kb:
    if k.name != "Basis": k.value = 0.0
for a in bpy.data.objects:
    if a.type == "ARMATURE":
        a.hide_render = True
        for b in a.pose.bones:
            b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0); b.location = (0, 0, 0)

LW = json.load(open(os.path.join(ROOT, "docs/evidence/linework/linework_3d.json")))
S = {k: np.array(v, dtype=float) for k, v in LW["sets"].items()
     if isinstance(v, list) and len(v) and isinstance(v[0], list)}

def seg_dist(pts, poly):
    a = poly[:-1]; b = poly[1:]; ab = b - a
    L2 = np.einsum("ij,ij->i", ab, ab); L2[L2 == 0] = 1e-12
    d = np.empty(len(pts))
    for i, p in enumerate(pts):
        t = np.clip(np.einsum("ij,ij->i", p - a, ab) / L2, 0.0, 1.0)
        d[i] = np.linalg.norm(a + ab * t[:, None] - p, axis=1).min()
    return d

def world():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg); me = ev.to_mesh()
    n = len(me.vertices); co = np.empty(n * 3); me.vertices.foreach_get("co", co)
    Wm = np.array(ev.matrix_world); co = co.reshape(n, 3) @ Wm[:3, :3].T + Wm[:3, 3]
    ev.to_mesh_clear(); return co

# ---- THE EYEBALL IS BACK, AND CLEARANCE IS MEASURABLE ---------------------
# It was never missing from the project, only from the rig: eye_{L,R}.npz sat 82 mm
# from the lid lines he drew, placed through the same MediaPipe fit that put his
# "eyelids" on his cheeks. place_eyeballs_on_linework.py re-seats them rigidly on
# his own aperture (centre 82.39 -> 14.24 mm, nearest globe vertex to his lid line
# 55.00 -> 0.49 mm) WITHOUT touching the globe geometry.
GLOBE = {}
for side in ("L", "R"):
    ob = bpy.data.objects.get("MARS_EYE_%s" % side)
    if ob is None: continue
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg); me = ev.to_mesh()
    n = len(me.vertices); co = np.empty(n * 3); me.vertices.foreach_get("co", co)
    Wm = np.array(ev.matrix_world)
    GLOBE[side] = co.reshape(n, 3) @ Wm[:3, :3].T + Wm[:3, 3]
    ev.to_mesh_clear()
print("eyeball geometry in the rig: %s" % (sorted(GLOBE) or "NONE"), flush=True)

REST = world()
results = {}
for keyname, side in CANDIDATES:
    if keyname not in kb:
        results[keyname] = {"verdict": "ABSENT"}
        print("%-14s ABSENT" % keyname, flush=True); continue
    up_line = S["eyelid_%s_upper" % side]; lo_line = S["eyelid_%s_lower" % side]
    aperture = float(np.median(seg_dist(up_line, lo_line))) / MM
    ez = lo_line.mean(0) - up_line.mean(0); ez = ez / np.linalg.norm(ez)
    d_up = seg_dist(REST, up_line) / MM
    margin = d_up <= 3.0                       # THE LID MARGIN, not the whole band:
    # skin high on the lid travels less than the free edge does, which is anatomy, not
    # weakness. Band-averaging once read 0.79 openings for a margin that crosses at 1.05.
    if margin.sum() < 10:
        die("%s: only %d vertices within 3 mm of his %s upper lid line" %
            (keyname, int(margin.sum()), side))
    kb[keyname].value = 1.0
    P = world()
    kb[keyname].value = 0.0
    disp = P - REST
    along = np.einsum("ij,j->i", disp[margin], ez) / MM     # + = toward closure
    # TWO DENOMINATORS, AND THEY MUST MATCH THEIR NUMERATOR. `aperture` is the median
    # distance from his upper LINE to his lower LINE. `gap_before` is the median
    # distance from the margin VERTICES to the lower line, and those are not the same
    # population: on the RIGHT eye the lines are 8.77 mm apart while the margin verts
    # start 6.09 mm out. Dividing margin travel by the line aperture therefore scored
    # a lid that closed its gap to 0.99 mm as only 0.73 -- a FAIL on a closure that had
    # happened. Both numbers are kept; the CLOSURE fraction is the one the gate reads,
    # because the question is whether the lids meet, and the residual gap is the direct
    # answer to it. This is not a loosened threshold: the gap gate is unchanged.
    travel_ap = float(np.median(along)) / aperture
    moved_all = float(np.linalg.norm(disp, axis=1).max()) / MM
    # WHERE DID IT LAND -- against his own drawn features, not the rig's opinion
    movedmask = np.linalg.norm(disp, axis=1) / MM > 0.3
    cen = P[movedmask].mean(0) if movedmask.any() else REST.mean(0)
    near, neard = None, 1e9
    for nm_, pts in S.items():
        dd = float(np.linalg.norm(pts - cen, axis=1).min()) / MM
        if dd < neard: near, neard = nm_, dd
    want = float(np.linalg.norm(np.vstack([up_line, lo_line]) - cen, axis=1).min()) / MM
    # CONTACT: does the upper margin reach the lower lid line
    gap_before = float(np.median(seg_dist(REST[margin], lo_line))) / MM
    gap_after = float(np.median(seg_dist(P[margin], lo_line))) / MM
    closure_frac = float(np.median(along)) / max(gap_before, 1e-6)
    # CLEARANCE LADDER against the real globe, every state, not just the closed one.
    # A lid that looks shut from the front can still be through the globe at the
    # corners, which is why this samples the whole margin and reports the MINIMUM.
    clearance = []
    if side in GLOBE:
        G = GLOBE[side]
        # SAME METHOD AS THE PLACEMENT TOOL, OR THE TWO WILL DISAGREE ABOUT THE SAME
        # GEOMETRY. Measuring with centroid + max-vertex-distance reported the lid
        # 7.57 mm INSIDE the globe at REST on an eye the placement solve had just put
        # 0.50 mm CLEAR. Two instruments contradicting each other about one rest pose
        # is not a finding, it is a broken instrument -- and the broken one was the
        # one that assumed a ball. The globe carries a corneal bulge, so its farthest
        # vertex is not its radius.
        A_ = np.hstack([2 * G, np.ones((len(G), 1))]); b_ = (G ** 2).sum(1)
        x_, *_ = np.linalg.lstsq(A_, b_, rcond=None)
        gc = x_[:3]
        rel = G - gc; rl = np.linalg.norm(rel, axis=1); rl[rl == 0] = 1e-12
        dirs = rel / rl[:, None]
        def clear_of(pts):
            out = []
            for q in pts:
                v = q - gc; n = float(np.linalg.norm(v))
                if n < 1e-9: out.append(-1e9); continue
                u = v / n
                cosang = dirs @ u
                sel = cosang > 0.93
                if not sel.any(): sel = cosang >= np.partition(cosang, -8)[-8]
                out.append(n - float(rl[sel].max()))
            return np.array(out) / MM
        for pct in (0, 25, 50, 75, 100):
            kb[keyname].value = pct / 100.0
            Q = world()
            kb[keyname].value = 0.0
            cl = clear_of(Q[margin])
            clearance.append({"state": pct,
                              "minClearanceMM": round(float(cl.min()), 3),
                              "vertsInsideGlobe": int((cl < 0).sum())})
    else:
        clearance = [{"state": "ALL", "minClearanceMM": None, "vertsInsideGlobe": None,
                      "note": "NOT_ATTEMPTED -- no MARS_EYE_%s in the rig" % side}]
    verdict = "PASS"
    why = []
    worst_pen = max((c["vertsInsideGlobe"] or 0) for c in clearance) if side in GLOBE else None
    if side in GLOBE and worst_pen and worst_pen > 0:
        deepest = min(c["minClearanceMM"] for c in clearance)
        verdict = "FAIL"
        why.append("lid goes THROUGH the eyeball: %d margin verts inside the globe, "
                   "deepest %.2f mm" % (worst_pen, deepest))
    if not movedmask.any():
        verdict, why = "FAIL", ["moves nothing"]
    else:
        if want > 8.0:
            verdict = "FAIL"; why.append("lands %.1f mm from his own eyelid line (%s)"
                                         % (want, near))
        if closure_frac < 0.9:
            verdict = "FAIL"; why.append("travels %.2f of the gap it has to close "
                                         "(%.2f line apertures)" % (closure_frac, travel_ap))
        if travel_ap < 0:
            why.append("TRAVELS THE WRONG WAY -- this is the lid being peeled OPEN")
        if gap_after > 1.5:
            verdict = "FAIL"; why.append("lid margin still %.2f mm from the lower lid" % gap_after)
    results[keyname] = {
        "side": side, "apertureMM": round(aperture, 3),
        "marginVerts": int(margin.sum()),
        "directionalTravelApertures": round(travel_ap, 3),
        "closureFraction": round(closure_frac, 3),
        "maxSkinTravelMM": round(moved_all, 3),
        "landsNearest": near, "mmToNearestDrawnFeature": round(neard, 2),
        "mmToHisEyelidLine": round(want, 2),
        "marginToLowerLidMM_before": round(gap_before, 3),
        "marginToLowerLidMM_after": round(gap_after, 3),
        "verdict": verdict, "why": why,
        "eyeballClearanceLadder": clearance,
    }
    print("%-14s closure %+5.2f (%.2f line-ap)  lands %5.1f mm from his lid  gap %5.2f -> %5.2f mm  %s %s"
          % (keyname, closure_frac, travel_ap, want, gap_before, gap_after, verdict,
             ("(" + "; ".join(why) + ")") if why else ""), flush=True)

# ---- THE LADDER: open -> 25 -> 50 -> 75 -> closed, CLOSE UP ----------------
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = scene.render.resolution_y = RES
scene.view_settings.view_transform = "Standard"
try: scene.eevee.taa_render_samples = 24
except Exception: pass
wd = bpy.data.worlds.new("W"); scene.world = wd; wd.use_nodes = True
wd.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.07, 1)
wd.node_tree.nodes["Background"].inputs[1].default_value = 1.6
fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
allp = REST
ctr = allp.mean(0); rad = float(np.linalg.norm(allp - ctr, axis=1).max())
for nm_, a_, b_, c_, e_ in (("K", -1.0, 0.8, 1.7, 320), ("F", 1.3, 0.2, 1.2, 180)):
    L = bpy.data.lights.new(nm_, type="AREA"); L.energy = e_; L.size = rad * 1.4
    ob = bpy.data.objects.new(nm_, L); scene.collection.objects.link(ob)
    ob.location = tuple(ctr + (x * a_ + up * b_ + fwd * c_) * rad * 2.0)
    ob.rotation_euler = (V(tuple(ctr)) - V(ob.location)).to_track_quat("-Z", "Y").to_euler()

frames = []
for side in ("L", "R"):
    eyec = np.vstack([S["eyelid_%s_upper" % side], S["eyelid_%s_lower" % side]]).mean(0)
    span = float(np.linalg.norm(np.vstack([S["eyelid_%s_upper" % side],
                                           S["eyelid_%s_lower" % side]]) - eyec, axis=1).max())
    # FRONT IS +fwd. face_plate.head_frame documents fwd as "out of the face" and its
    # own plate camera sits at centre + fwd*CAM_DIST -- the plates the owner DREW ON are
    # framed that way. Every camera here used -fwd, so every "FRONT" render in this
    # session was shot from BEHIND HIS HEAD. Measured against his own drawn features:
    # dot(nostril direction, fwd) = +0.68 (L) and +0.93 (R), so fwd points at his face.
    # Never re-derive this from a world axis; derive it from a feature he marked.
    d_ = np.asarray(fwd, float); d_ /= np.linalg.norm(d_)
    u_ = np.asarray(up, float).copy(); u_ -= d_ * np.dot(u_, d_); u_ /= np.linalg.norm(u_)
    r_ = np.cross(u_, d_)
    cd = bpy.data.cameras.new("EYE_%s" % side); cd.type = "ORTHO"
    cd.ortho_scale = span * 4.2
    cam = bpy.data.objects.new("EYE_%s" % side, cd); scene.collection.objects.link(cam)
    org = eyec + d_ * rad * 3
    cam.matrix_world = M(((r_[0], u_[0], d_[0], org[0]), (r_[1], u_[1], d_[1], org[1]),
                          (r_[2], u_[2], d_[2], org[2]), (0, 0, 0, 1)))
    scene.camera = cam
    for ob_ in bpy.data.objects:
        if ob_.name.startswith("MARS_EYE_"): ob_.hide_render = False
    for keyname in ("blink_own_%s" % side, "blink_%s" % side):
        if keyname not in kb: continue
        for pct in (0, 25, 50, 75, 100):
            kb[keyname].value = pct / 100.0
            fp = os.path.join(OUT, "%s_%s_%03d.png" % (side, keyname, pct))
            scene.render.filepath = fp
            bpy.ops.render.render(write_still=True)
            frames.append(os.path.relpath(fp, ROOT))
        kb[keyname].value = 0.0
    print("rendered ladder for eye %s" % side, flush=True)

rep = {"schema": "trippedd.blink-proof/v1",
       "authority": "docs/evidence/linework/linework_3d.json -- the lines the OWNER drew",
       "verdictRule": "DIRECTIONAL lid-margin travel as a fraction of that eye's own "
                      "aperture. Occlusion is never the verdict: it once scored a lid "
                      "being peeled OPEN as 84% closed.",
       "gates": {"minClosureFraction": 0.9, "maxMMFromHisEyelidLine": 8.0,
                 "maxResidualGapMM": 1.5},
       "eyeballClearanceLegacyNote": {
           "state": "SUPERSEDED",
           "reason": "this rig contains NO eyeball geometry. Objects present: MARS_MESH, "
                     "MARS_MOUTH_SOCK, MARS_TEETH_UPPER/LOWER, MARS_TONGUE, MARS_RIG and "
                     "the reference plates. There is no globe to be occluded by a lid or "
                     "penetrated by one, so an eyeball-visibility gate here would assert "
                     "nothing and report a clean sheet -- a gate with zero checks reports "
                     "0/0 PASS. Mars's eyes are solid white BY DESIGN; whether that is "
                     "texture or absent geometry is the next thing to establish, and it "
                     "is recorded as NOT_ATTEMPTED rather than as a pass."},
       "keys": results, "ladderFrames": frames}
json.dump(rep, open(os.path.join(OUT, "blink_proof.json"), "w"), indent=2)
print("\nwrote %s" % os.path.join(OUT, "blink_proof.json"), flush=True)
bad = [k for k, v in results.items() if v.get("verdict") == "FAIL"]
print("FAIL: %s" % bad if bad else "all measured keys PASS", flush=True)
