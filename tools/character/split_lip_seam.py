"""
THE LIPS ARE WELDED. SPLIT THE SEAM SO THEY CAN PART.

The cavity was never missing. `oral_cavity.py` carves it and the gate reports
seam 41/41 on the cavity wall; the GNM teeth (1,440 verts each), gums, tongue
(933 verts, 31 keys) and mouth sock (406 verts) are all in MARS_FACE.blend.
What is missing is a SEPARATION: the upper and lower lip surfaces share their
vertices, so the jaw can only stretch one continuous sheet. Measured, that is
nine of 240 teeth rays at the very best -- the owner's "small hole", and the
"stretching instead of opening" he described.

  "the lip seam needs to be a real split so the two lip surfaces can part,
   and the jaw needs to carry the lower one"        -- docs/evidence/oral/README.md

THE METHOD IS `open_mouth_surgery.py`'s (OWNER LAW #3 -- it was already in the
repo): find the seam, split every edge that crosses it, re-weight upper lip to
head and lower lip to jaw. Two deliberate departures, both measured:

  1. IT DOES NOT BUILD A MOUTH BAG. open_mouth_surgery.py adds a UV sphere
     behind the lips. MARS_FACE.blend already has MARS_MOUTH_SOCK and the GNM
     teeth/gums/tongue -- dropping a sphere in beside them is precisely the
     regression the owner named ("u regressed the perfect mouth with teeth
     tounge gums and oral bridges").

  2. IT DOES NOT USE face_anatomy.json. That is the MediaPipe pass that put his
     eyelids on his cheeks, and its `upper_lip` and `lower_lip` are 0.9 mm
     apart -- effectively one point, which cannot define a seam. The authority
     here is the INNER-LIP CONTOUR in mouth_anatomy.json, and unlike the eye
     landmarks it CHECKS OUT AGAINST THINGS OUTSIDE ITSELF:

         inner-lip curve -> head surface        mean 1.15 mm   max 1.98 mm
         inner-lip curve -> MARS_MOUTH_SOCK rim mean 4.28 mm   max 6.76 mm
         sock rim        -> teeth               mean 2.83 mm   max 4.91 mm
         painted texture green channel          0.128 -> 0.055 AT the contour

     The same MediaPipe pass that missed his eyes by 39 mm put his mouth within
     1.2 mm of his skin. A fit is not wrong everywhere because it is wrong
     somewhere -- but it has to be CHECKED everywhere, against something else.

    vendor/blender/blender -b -P tools/character/split_lip_seam.py -- --measure-only
    vendor/blender/blender -b -P tools/character/split_lip_seam.py --
"""
import bpy, bmesh, sys, os, json, math
import numpy as np
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def flag(f): return f in argv
def die(m):
    # BLENDER -b SWALLOWS THE ARGUMENT TO sys.exit(). A guard whose message
    # nobody can see is the "printed into a log nobody read" failure with extra
    # steps -- print it and flush before leaving.
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("split_lip_seam.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))

RIG      = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT      = os.path.abspath(opt("--out", RIG))
ZONE_MM  = float(opt("--zone-mm", "9"))     # how far from the seam curve counts as lip
HARD_MM  = float(opt("--hard-mm", "3.5"))   # inside this, weights are pure head / pure jaw
REPORT   = os.path.abspath(opt("--report", os.path.join(ROOT, "docs/evidence/oral/lip_seam.json")))
MEASURE  = flag("--measure-only")

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
head  = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH in %s" % RIG)
arm   = bpy.data.objects.get("MARS_RIG")  or die("no MARS_RIG in %s" % RIG)
me    = head.data

MA   = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW   = float(MA["aperture"]["width"])
MM   = MW / 50.0                  # CLAUDE.md: an adult mouth is ~50 mm across
FRAME = Matrix(MA["frame"]["matrix"]); FINV = FRAME.inverted()

# ── WHICH WAY IS OUT OF HIS FACE -- DERIVED FROM HIS TEETH, NOT A WORLD AXIS ──
# Every "FRONT" camera in this project was once behind his head. The mouth
# frame's local +y is the direction the aperture gets DEEPER (lipFrontLocalY
# -0.0405 -> deepestLocalY +0.0174), and his teeth sit deeper than his lips, so
# out-of-the-face is -y. Checked below against the actual teeth centroid.
def to_local(p): return FINV @ Vector(p)
OUTWARD = (FRAME.to_3x3() @ Vector((0.0, -1.0, 0.0))).normalized()

def world_verts(ob, evaluated=False):
    if evaluated:
        deps = bpy.context.evaluated_depsgraph_get()
        eo = ob.evaluated_get(deps); m = eo.to_mesh()
        try:
            W = eo.matrix_world
            return [W @ v.co.copy() for v in m.vertices]
        finally:
            eo.to_mesh_clear()
    W = ob.matrix_world
    return [W @ v.co for v in ob.data.vertices]

_tu = world_verts(bpy.data.objects["MARS_TEETH_UPPER"])
_ap = (Vector(MA["aperture"]["cornerLeft"]) + Vector(MA["aperture"]["cornerRight"])) / 2.0
_teeth_dir = (sum(_tu, Vector()) / len(_tu) - _ap).normalized()
if _teeth_dir.dot(OUTWARD) > -0.5:
    die("out-of-the-face direction does not point away from his teeth "
        "(dot %.3f). The mouth frame is not what this tool thinks it is."
        % _teeth_dir.dot(OUTWARD))
print("out-of-the-face %s   (dot with the direction to his teeth %.3f -- behind him, correct)"
      % (["%.3f" % c for c in OUTWARD], _teeth_dir.dot(OUTWARD)), flush=True)

# ── THE SEAM CURVE ───────────────────────────────────────────────────────────
# His inner-lip contour, in the mouth frame: lateral x -> seam height z. Upper
# and lower inner contours are averaged; on a closed mouth they are the same
# crease seen from either side (they measure 0.30 mm apart here).
IU = np.array(MA["contours"]["lip_inner_upper"], float)
IL = np.array(MA["contours"]["lip_inner_lower"], float)
SEAM_W = np.vstack([IU, IL])
SEAM_L = np.array([list(to_local(p)) for p in SEAM_W])
order  = np.argsort(SEAM_L[:, 0])
_cx, _ci = np.unique(np.round(SEAM_L[order, 0], 6), return_inverse=True)
_cz = np.array([SEAM_L[order, 2][_ci == i].mean() for i in range(len(_cx))])
X_MIN, X_MAX = float(_cx[0]), float(_cx[-1])

# ── THE SEAM IS THE CREASE IN HIS OWN MESH, NOT A CURVE LAID OVER IT ─────────
# Interpolating the contour's own height gave a cut that was open at both
# CORNERS and welded straight across the middle -- 44 crossing edges, and the
# centre of his mouth still read `skin` at every height. The contour was
# raycast onto the surface, so its height carries the raycast's own error, and
# a couple of millimetres there is the difference between cutting the crease
# and cutting the lip above it.
#
# His crease is a MEASURABLE FEATURE: along any vertical line through the
# mouth, the surface reaches its deepest point INTO the face exactly at the
# fold (at x=0 it dips to -4.89 mm where 2 mm above and below it sits at -7.05
# and -6.08). So the seam height is read off the mesh, bin by bin, and the
# contour is kept for what it is good for -- an outside check that the crease
# found is really his mouth and not some other fold.
_bm0 = bmesh.new(); _bm0.from_mesh(me); _bm0.verts.ensure_lookup_table()
_Wm = head.matrix_world
_PL = np.array([list(to_local(_Wm @ v.co)) for v in _bm0.verts], float)
_bm0.free()
NB = int(opt("--seam-bins", "44"))
_edges = np.linspace(X_MIN - 2.0 * MM, X_MAX + 2.0 * MM, NB + 1)
_bx, _bz = [], []
for _i in range(NB):
    _lo, _hi = _edges[_i], _edges[_i + 1]
    _c = 0.5 * (_lo + _hi)
    _ref = float(np.interp(_c, _cx, _cz))
    _sel = ((_PL[:, 0] >= _lo) & (_PL[:, 0] < _hi)
            & (np.abs(_PL[:, 2] - _ref) < 7.0 * MM))
    if _sel.sum() < 3: continue
    _cand = np.nonzero(_sel)[0]
    _deep = _cand[np.argmax(_PL[_cand, 1])]      # deepest INTO his face = the fold
    _bx.append(_c); _bz.append(float(_PL[_deep, 2]))
if len(_bx) < NB // 2:
    die("the crease resolved in only %d of %d bins across his mouth" % (len(_bx), NB))
_bx = np.array(_bx); _bz = np.array(_bz)
# median-of-3 smoothing: one stray bin should not kink the seam
_bzs = _bz.copy()
for _i in range(1, len(_bz) - 1):
    _bzs[_i] = float(np.median(_bz[_i - 1:_i + 2]))
# THE MEASURED CONTOUR WINS, AND IT IS MEASURED THAT IT WINS. The mesh-crease
# derivation above wanders: against the same mesh it reports 94 faces straddling
# his crease where the contour reports 36, and the split built on it recovered
# LESS of his mouth in pixels (oral anatomy 3.92% of frame vs 5.02%). It is kept
# because it is the only independent check on where his crease actually is -- the
# deviation printed below is that check -- but the contour is what is cut along.
_ux, _uz = (_bx, _bzs) if flag("--seam-from-mesh") else (_cx, _cz)

def seam_z_local(x):
    """Height of his lip crease directly above/below this lateral position."""
    return float(np.interp(x, _ux, _uz))

# OUTSIDE CHECK. The crease has to be his mouth, and the contour is the only
# independent thing that says where that is.
_dev = np.array([abs(_bzs[i] - float(np.interp(_bx[i], _cx, _cz))) for i in range(len(_bx))]) / MM
print("seam from his own mesh: %d bins across %.1f mm; deviation from the measured "
      "contour mean %.2f mm, max %.2f mm" % (len(_bx), (X_MAX - X_MIN) / MM,
                                             _dev.mean(), _dev.max()), flush=True)
if _dev.mean() > 4.0 or _dev.max() > 9.0:
    die("the crease found in his mesh is %.2f mm (max %.2f) from the measured lip "
        "contour -- that is not his mouth" % (_dev.mean(), _dev.max()))

W4 = np.array(head.matrix_world)
def to_world_np(P): return P @ W4[:3, :3].T + W4[:3, 3]

# ── HOW MANY TEETH THE CAMERA CAN ACTUALLY SEE ───────────────────────────────
# THREE INSTRUMENT BUGS ARE AVOIDED HERE, ALL THREE PREVIOUSLY MINE:
#   1. "did the ray hit the head" is not visibility -- a ray that enters the
#      mouth carries on and hits the back of the skull from INSIDE and reports a
#      hit either way. The test is whether the FIRST hit is AT the tooth.
#   2. tooth positions sampled once at rest, then the jaw rotated, aims the rays
#      at where the teeth used to be. MARS_TEETH_* carry armature modifiers, so
#      they are re-read from the EVALUATED depsgraph at every pose.
#   3. nothing jaw-weighted is being used as a cutter here at all.
TOL = 0.5 * MM

def _front_tooth_samples(n_each=120):
    """The front faces of his front teeth -- what 'showing teeth' means."""
    out = []
    for nm in ("MARS_TEETH_UPPER", "MARS_TEETH_LOWER"):
        P = world_verts(bpy.data.objects[nm], evaluated=True)
        L = np.array([list(to_local(p)) for p in P])
        keep = np.nonzero(np.abs(L[:, 0]) < 0.30 * MW)[0]
        if len(keep) == 0: keep = np.arange(len(P))
        keep = keep[np.argsort(L[keep, 1])][:n_each]      # smallest local y = most forward
        out.extend([(nm, int(i), P[int(i)]) for i in keep])
    return out

def teeth_visible(pose, n_each=120, detail=False):
    """pose: {"jaw": deg, "keys": {name: value}}"""
    for k in me.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
    for nm, val in (pose.get("keys") or {}).items():
        kb = me.shape_keys.key_blocks.get(nm)
        if kb is None: die("pose names a shape key the rig does not have: %s" % nm)
        kb.value = val
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
    pb.rotation_euler = (math.radians(pose.get("jaw", 0.0)), 0, 0)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()

    samples = _front_tooth_samples(n_each)
    eye = Vector(_ap) + OUTWARD * 1.2
    vis, blockers = 0, {}
    for nm, i, P in samples:
        d = (P - eye)
        L = d.length
        if L < 1e-9: continue
        d = d / L
        hit, loc, _n, _i, ob, _m = scene.ray_cast(deps, eye, d, distance=L + 0.5)
        if not hit or (loc - P).length <= TOL:
            vis += 1
        elif detail:
            blockers[ob.name if ob else "?"] = blockers.get(ob.name if ob else "?", 0) + 1
    pb.rotation_euler = (0, 0, 0)
    for k in me.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
    bpy.context.view_layer.update()
    return vis, len(samples), blockers

POSES = [
    ("rest",                                     {"jaw": 0.0}),
    ("jaw 18 deg",                               {"jaw": 18.0}),
    ("jaw 30 deg",                               {"jaw": 30.0}),
    ("jaw 18 + lip_lower_depress",               {"jaw": 18.0, "keys": {"lip_lower_depress": 1.0}}),
    ("jaw 18 + lower_depress + upper_raise",     {"jaw": 18.0, "keys": {"lip_lower_depress": 1.0, "lip_upper_raise": 1.0}}),
    ("jaw 30 + both lip keys",                   {"jaw": 30.0, "keys": {"lip_lower_depress": 1.0, "lip_upper_raise": 1.0}}),
    ("jaw 30 + both + mouth_funnel",             {"jaw": 30.0, "keys": {"lip_lower_depress": 1.0, "lip_upper_raise": 1.0, "mouth_funnel": 1.0}}),
    ("facs_jawOpen 1.0",                         {"jaw": 0.0,  "keys": {"facs_jawOpen": 1.0}}),
    ("facs_jawOpen + jaw 30 + lips + funnel",    {"jaw": 30.0, "keys": {"facs_jawOpen": 1.0, "lip_lower_depress": 1.0, "lip_upper_raise": 1.0, "mouth_funnel": 1.0}}),
]

def ladder(tag, detail=False):
    print("\n  %-42s teeth the camera can see" % tag, flush=True)
    rows = []
    for nm, pose in POSES:
        v, n, bl = teeth_visible(pose, detail=detail)
        top = (" blocked mostly by %s" % max(bl, key=bl.get)) if (detail and bl) else ""
        print("    %-40s %4d / %d%s" % (nm, v, n, top), flush=True)
        rows.append({"pose": nm, "visible": v, "of": n})
    return rows

print("\n================ BEFORE ================", flush=True)
before = ladder("BEFORE the seam split", detail=True)
best_before = max(r["visible"] for r in before)

if MEASURE:
    print("\nmeasure-only: best %d of %d. Nothing written." % (best_before, before[0]["of"]))
    sys.exit(0)

if me.get("lip_seam_split"):
    die("this rig's lip seam is already split -- refusing to split it twice")

# ── CLASSIFY, AND SPLIT ──────────────────────────────────────────────────────
n0    = len(me.vertices)
keys0 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
P0    = np.array([v.co[:] for v in me.vertices], float)
P0w   = to_world_np(P0)
P0l   = np.array([list(to_local(Vector(p))) for p in P0w])

d_seam = np.array([float(np.linalg.norm(SEAM_W - q, axis=1).min()) for q in P0w]) / MM
in_span = (P0l[:, 0] > X_MIN - 4.0 * MM) & (P0l[:, 0] < X_MAX + 4.0 * MM)
zone = (d_seam < ZONE_MM) & in_span
sz = np.array([seam_z_local(x) for x in P0l[:, 0]])
above = P0l[:, 2] > sz

upper = set(int(i) for i in np.nonzero(zone & above)[0])
lower = set(int(i) for i in np.nonzero(zone & ~above)[0])
print("\nlip zone (<= %.0f mm from his lip crease): %d upper, %d lower"
      % (ZONE_MM, len(upper), len(lower)), flush=True)
if len(upper) < 20 or len(lower) < 20:
    die("the lip seam did not resolve -- %d upper / %d lower" % (len(upper), len(lower)))

bm = bmesh.new()
bm.from_mesh(me)
bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
# SHAPE KEYS AND VERTEX GROUPS RIDE ALONG as bmesh vertex layers, and split_edges
# copies layer data onto the vertex it duplicates. Without this every one of the
# 88 keys would land at Basis on the new half of the seam and tear the face open.
shape_layers = list(bm.verts.layers.shape.keys())
has_deform = bm.verts.layers.deform.active is not None
print("carrying %d shape key layer(s) and %s through the split"
      % (len(shape_layers), "the vertex groups" if has_deform else "NO vertex groups"), flush=True)
if len(shape_layers) + 1 < len(keys0):
    die("bmesh sees %d shape layers for %d keys" % (len(shape_layers), len(keys0)))

# ── CUT THE FACES THAT SPAN HIS MOUTH. THERE IS NO EDGE TO SPLIT. ───────────
# Splitting edges opened the CORNERS of his mouth and left the centre welded, at
# 44 crossing edges and again at 98. Measured, that is not a tuning problem:
#
#     edges crossing the crease in the lip zone                44
#     FACES STRADDLING the crease                              55
#       their area              median 13.0 mm2   max 52.7 mm2
#       their longest edge      median  8.7 mm    max 22.5 mm
#     whole-head median face area                            0.59 mm2
#     widest stretch of his mouth with NO crossing edge        7.9 mm
#
# A single face 22x the median area spans from his upper lip to his lower lip, so
# across 7.9 mm of his mouth there is no edge for split_edges to act on at all.
# That face is what the jaw drags inward, and it is the blue skin filling the
# centre of his open mouth.
#
# So the faces are CUT first, with Blender's own bisect, which creates the
# crossing edges that were never there. His crease is a CURVE, so one plane
# cannot follow it (it wanders 7 mm in z across his mouth) -- it is bisected bin
# by bin, each bin's plane passing through that bin's own measured crease point.
def _side_of(co):
    L = to_local(Wm_ @ co)
    return 1.0 if L.z > seam_z_local(L.x) else -1.0

Wm_ = head.matrix_world
PLANE_NO = (FRAME.to_3x3() @ Vector((0.0, 0.0, 1.0))).normalized()
NBIN = int(opt("--cut-bins", "40"))
bedges = np.linspace(X_MIN - 2.0 * MM, X_MAX + 2.0 * MM, NBIN + 1)

# A VERTEX LYING EXACTLY ON THE CUT IS ON NEITHER SIDE. Without this epsilon
# every freshly bisected face reads as still straddling -- the bisect puts its new
# vertices exactly on the plane, `z > seam_z` calls that "below", and the count
# went 103 -> 117 on a pass that had cut every one of them correctly. The cut was
# working; the detector was not.
EPS = 0.2 * MM
def _sgn(l):
    z = seam_z_local(l.x)
    return 1 if l.z > z + EPS else (-1 if l.z < z - EPS else 0)

def _straddlers():
    out = []
    for f in bm.faces:
        L = [to_local(Wm_ @ v.co) for v in f.verts]
        if not any((d_of(v) < ZONE_MM) for v in f.verts): continue
        if not all(X_MIN - 4.0 * MM < l.x < X_MAX + 4.0 * MM for l in L): continue
        sgn = {_sgn(l) for l in L}
        if 1 in sgn and -1 in sgn: out.append(f)
    return out

_dcache = {}
def d_of(v):
    k = v.index
    if k not in _dcache:
        _dcache[k] = float(np.linalg.norm(SEAM_W - np.array(Wm_ @ v.co), axis=1).min()) / MM
    return _dcache[k]

if not flag("--no-cut"):
    # PER FACE, AT ITS OWN CREASE POSITION, AND ITERATED. One plane per x-BIN was
    # measured to make things WORSE -- 103 straddling faces became 117 -- because
    # a face here is up to 22.5 mm wide and spans several bins, so the bin's plane
    # cuts it somewhere that is not its crease and each fragment still straddles.
    # Each face is therefore cut with a plane through the crease at ITS OWN centre,
    # and because his crease still curves across a face that wide, the pass is
    # repeated until the count stops falling. Convergence is measured, not assumed.
    n_before = len(bm.verts)
    strad0 = _straddlers()
    print("faces straddling his crease, before the cut: %d" % len(strad0), flush=True)
    cut_faces, prev = 0, len(strad0)
    for _pass in range(int(opt("--cut-passes", "1"))):
        todo = _straddlers()
        if not todo: break
        for f in todo:
            if not f.is_valid: continue
            c = to_local(Wm_ @ f.calc_center_median())
            co = FRAME @ Vector((c.x, 0.0, seam_z_local(c.x)))
            geom = set([f]); geom.update(f.verts); geom.update(f.edges)
            try:
                bmesh.ops.bisect_plane(bm, geom=list(geom), dist=1e-7,
                                       plane_co=Wm_.inverted() @ co,
                                       plane_no=Wm_.inverted().to_3x3() @ PLANE_NO,
                                       clear_inner=False, clear_outer=False)
            except Exception as _e:
                die("bisect refused: %s" % _e)
            cut_faces += 1
        bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table(); bm.verts.index_update()
        _dcache.clear()
        now = len(_straddlers())
        print("  pass %d: cut %d faces, %d still straddle" % (_pass + 1, len(todo), now), flush=True)
        if now >= prev: break
        prev = now
    _dcache.clear()
    strad1 = _straddlers()
    print("cut %d faces; verts %d -> %d; straddling faces %d -> %d"
          % (cut_faces, n_before, len(bm.verts), len(strad0), len(strad1)), flush=True)
    # ONE PASS. A SECOND ONE MEASURED WORSE: 36 -> 23 -> 28. Once a wide face has
    # been cut at its centroid's crease height the fragments that still straddle are
    # the ends of a curve, and a second plane through THEIR centroids cuts them
    # somewhere worse than not at all. The residual is carried and the gate that
    # matters is further down -- how much of his mouth the seam actually spans, and
    # then the pixels.
    if len(strad1) >= len(strad0):
        die("the cut did not reduce the faces spanning his crease (%d -> %d)"
            % (len(strad0), len(strad1)))

bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table(); bm.verts.index_update()
_dcache.clear()

# ── THE SEAM IS WHERE AN UPPER FACE MEETS A LOWER FACE ───────────────────────
# Once the spanning faces are cut, the crease is a CHAIN OF VERTICES SITTING ON
# IT, shared by the faces above and below. No edge "crosses" it any more, so
# looking for crossing edges finds nothing. What has to be split is the chain
# itself: every edge whose two faces lie on OPPOSITE sides of his crease.
#
# Classifying the FACE by its centroid rather than the vertex by its height is
# also what makes this epsilon-free -- a centroid is never on the crease, while
# half the vertices now are, exactly.
face_side = {}
for f in bm.faces:
    c = to_local(Wm_ @ f.calc_center_median())
    if not (X_MIN - 4.0 * MM < c.x < X_MAX + 4.0 * MM): continue
    if not any(d_of(v) < ZONE_MM for v in f.verts): continue
    face_side[f.index] = 1 if c.z > seam_z_local(c.x) else -1

crossing = [e for e in bm.edges
            if len(e.link_faces) == 2
            and face_side.get(e.link_faces[0].index, 0) * face_side.get(e.link_faces[1].index, 0) < 0]
print("seam edges (an upper face meeting a lower face): %d" % len(crossing), flush=True)
if len(crossing) < 10:
    die("only %d seam edges -- nothing to split" % len(crossing))
_span = [to_local(Wm_ @ v.co).x for e in crossing for v in e.verts]
print("  they span %.1f mm of his %.1f mm mouth"
      % ((max(_span) - min(_span)) / MM, (X_MAX - X_MIN) / MM), flush=True)

bmesh.ops.split_edges(bm, edges=crossing)
bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table(); bm.verts.index_update()

# ── WHICH SIDE IS THIS VERTEX ON? ITS FACES, NOT ITS COORDINATES. ────────────
# The whole point of the split is that the two halves of a pair sit on TOP of
# one another. Asking "is this vertex above the seam" therefore gives BOTH of
# them the same answer, they get the same weights, and they travel together --
# measured, the seam gap came out 0.00 mm at every pose, on a jaw that moves the
# lip zone 26 mm. What tells them apart is which SURFACE they belong to, so the
# side is read from the centroid of the faces linked to the vertex.
Wm = head.matrix_world
side = {}
for v in bm.verts:
    if not v.link_faces: continue
    c = Vector((0, 0, 0))
    for f in v.link_faces: c += f.calc_center_median()
    c /= len(v.link_faces)
    cl = to_local(Wm @ c)
    vl = to_local(Wm @ v.co)
    if not (X_MIN - 4.0 * MM < vl.x < X_MAX + 4.0 * MM): continue
    side[v.index] = 1 if cl.z > seam_z_local(cl.x) else -1

bm.to_mesh(me)
bm.free()
me.update()

n1 = len(me.vertices)
P1 = np.array([v.co[:] for v in me.vertices], float)
print("verts %d -> %d (+%d)" % (n0, n1, n1 - n0), flush=True)

# ── GATES ON WHAT MUST NOT HAVE CHANGED ──────────────────────────────────────
drift = float(np.abs(P1[:n0] - P0).max()) / MM
print("original vertices' rest drift: %.6f mm" % drift, flush=True)
if drift > 1e-4:
    die("the cut MOVED original vertices by %.6f mm -- every measurement banked "
        "against this mesh would be invalidated" % drift)
keys1 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
if keys1 != keys0:
    die("shape keys changed: %d -> %d" % (len(keys0), len(keys1)))
B = np.array([d.co[:] for d in me.shape_keys.key_blocks["Basis"].data], float)
dead = []
for k in me.shape_keys.key_blocks:
    if k.name == "Basis": continue
    A = np.array([d.co[:] for d in k.data], float)
    if float(np.linalg.norm(A - B, axis=1).max()) / MM < 0.05:
        dead.append(k.name)
if dead:
    die("%d shape key(s) move nothing after the split -- they were torn, not carried: %s"
        % (len(dead), dead[:10]))
print("all %d shape keys still move; none landed at Basis" % (len(keys1) - 1), flush=True)

# ── RE-WEIGHT ACROSS THE NEW SEAM ────────────────────────────────────────────
# Without this the split changes nothing: both halves still carry the same
# blended weight and travel together. Feathered, not a cliff -- pure head / pure
# jaw only within HARD_MM of the crease, easing back to what the rig already had
# at the edge of the lip zone, so the lip parts without creasing the chin.
vg_jaw  = head.vertex_groups.get("jaw")  or die("no 'jaw' vertex group")
vg_head = head.vertex_groups.get("head") or die("no 'head' vertex group")
P1w = to_world_np(P1)
P1l = np.array([list(to_local(Vector(p))) for p in P1w])
d1  = np.array([float(np.linalg.norm(SEAM_W - q, axis=1).min()) for q in P1w]) / MM
in_span1 = (P1l[:, 0] > X_MIN - 4.0 * MM) & (P1l[:, 0] < X_MAX + 4.0 * MM)

gi_jaw, gi_head = vg_jaw.index, vg_head.index
n_up = n_lo = 0
for i in range(n1):
    sd = side.get(i)
    if sd is None or not (in_span1[i] and d1[i] < ZONE_MM): continue
    t = 1.0 if d1[i] <= HARD_MM else max(0.0, 1.0 - (d1[i] - HARD_MM) / (ZONE_MM - HARD_MM))
    w = {g.group: g.weight for g in me.vertices[i].groups}
    cur_j, cur_h = w.get(gi_jaw, 0.0), w.get(gi_head, 0.0)
    tgt_j, tgt_h = (0.0, 1.0) if sd > 0 else (1.0, 0.0)
    vg_jaw.add([i],  cur_j + (tgt_j - cur_j) * t, "REPLACE")
    vg_head.add([i], cur_h + (tgt_h - cur_h) * t, "REPLACE")
    if sd > 0: n_up += 1
    else: n_lo += 1
print("re-weighted across the seam: %d upper->head, %d lower->jaw "
      "(pure within %.1f mm, eased to %.0f mm)" % (n_up, n_lo, HARD_MM, ZONE_MM), flush=True)

me["lip_seam_split"] = True

# ── DOES THE SEAM ACTUALLY PART? ─────────────────────────────────────────────
# The teeth ladder is the question the owner asked, but it is an INDIRECT
# measure: a mouth can part and still show no teeth if something else occludes.
# Measure the thing that was built directly -- the split pairs sit on top of one
# another at rest, so their separation under a pose IS the aperture.
pair = {}
_key = {}
for i in range(n0):
    _key.setdefault(tuple(np.round(P1[i], 7)), i)
for j in range(n0, n1):
    i = _key.get(tuple(np.round(P1[j], 7)))
    if i is not None: pair[j] = i
print("split pairs recovered: %d of %d new vertices" % (len(pair), n1 - n0), flush=True)

def _ev_head():
    deps = bpy.context.evaluated_depsgraph_get()
    eo = head.evaluated_get(deps); m = eo.to_mesh()
    try:
        M = eo.matrix_world
        return np.array([list(M @ v.co) for v in m.vertices], float)
    finally:
        eo.to_mesh_clear()

def seam_gap(pose):
    for k in me.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
    for nm, val in (pose.get("keys") or {}).items():
        me.shape_keys.key_blocks[nm].value = val
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
    pb.rotation_euler = (math.radians(pose.get("jaw", 0.0)), 0, 0)
    bpy.context.view_layer.update()
    E = _ev_head()
    g = np.array([np.linalg.norm(E[j] - E[i]) for j, i in pair.items()]) / MM if pair else np.zeros(1)
    pb.rotation_euler = (0, 0, 0)
    for k in me.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
    bpy.context.view_layer.update()
    return g

print("\n  seam aperture -- how far the two lip surfaces travel apart", flush=True)
gaps = []
for nm, pose in POSES:
    g = seam_gap(pose)
    print("    %-40s mean %6.2f  max %6.2f mm" % (nm, g.mean(), g.max()), flush=True)
    gaps.append({"pose": nm, "meanMM": round(float(g.mean()), 3), "maxMM": round(float(g.max()), 3)})

print("\n================ AFTER =================", flush=True)
after = ladder("AFTER the seam split", detail=True)
best_after = max(r["visible"] for r in after)
of = after[0]["of"]

print("\nbest visible teeth: %d -> %d of %d" % (best_before, best_after, of), flush=True)

# A REFUSAL STILL HAS TO PRODUCE PIXELS. "The image is ready" without a
# retrievable image is NOT_ATTEMPTED (OWNER LAW #2), and a refusal nobody can
# look at is the same failure. --review-out writes the rejected rig somewhere it
# can be rendered and stepped through; it is never the canonical rig.
REVIEW = opt("--review-out", "")
if REVIEW:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(REVIEW))
    print("review copy -> %s  (NOT promoted)" % REVIEW, flush=True)

if best_after <= max(best_before * 2, best_before + 20):
    die("THE SEAM SPLIT DID NOT OPEN THE MOUTH -- %d of %d at best, was %d. "
        "Refusing to save a rig that still cannot speak." % (best_after, of, best_before))

bpy.ops.wm.save_as_mainfile(filepath=OUT)
os.makedirs(os.path.dirname(REPORT), exist_ok=True)
json.dump({
    "schema": "trippedd.lip-seam/v1",
    "rig": os.path.relpath(OUT, ROOT),
    "authority": "renders/_rig_measure/mouth_anatomy.json inner-lip contour",
    "authorityCheckedAgainst": {
        "headSurfaceMeanMM": 1.15, "sockRimMeanMM": 4.28,
        "sockRimToTeethMeanMM": 2.83,
        "paintedTextureGreenAtContour": [0.128, 0.055],
        "note": "the MediaPipe pass that put his eyelids on his cheeks put his mouth "
                "within 1.2 mm of his skin -- checked, not assumed",
    },
    "zoneMM": ZONE_MM, "hardMM": HARD_MM,
    "seamEdgesSplit": len(crossing),
    "vertsBefore": n0, "vertsAfter": n1,
    "upperLipVerts": n_up, "lowerLipVerts": n_lo,
    "originalVertexDriftMM": drift,
    "shapeKeysCarried": len(keys1),
    "seamAperture": gaps,
    "teethVisibleBefore": before, "teethVisibleAfter": after,
    "bestBefore": best_before, "bestAfter": best_after, "of": of,
}, open(REPORT, "w"), indent=2)
print("rig -> %s\nreport -> %s" % (OUT, REPORT), flush=True)
