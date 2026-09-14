"""
THE MOUTH RIM CANNOT BE BUILT OUT OF 261 FACES.

Owner, on the shipped rig: *"a bunch of really big, ugly triangles."* The same
sentence applies to the opening. The re-carve fixed the SHAPE of his mouth --
the aperture follows his own lip line and the corner crater went 44 of 483 cells
to 4 -- and `mouth_proof` went 7/8 to **8 of 8**. Then the pixels vetoed it:

    docs/evidence/mars/mouth/AB_shipped_vs_recarved.v001.png
    AT REST     the re-carve closes the corner gap the shipped rig shows. Better.
    WIDE OPEN   pale triangular SHARDS all round the rim and a large wedge at the
                lower left, where the shipped rectangular slot cuts clean. WORSE.

**That is not a carve problem and no cutter tuning fixes it.** It is the defect
already banked twice: *"THE LID CANNOT BE BUILT OUT OF THREE VERTICES"*, and
*"261 faces fill his entire mouth"*. Cutting a curve through triangles that are
17-23 mm2 -- against a whole-head median of 0.59 mm2 -- leaves slivers, and the
more of his mouth the seam recovers (teeth 9 -> 88 of 240) the more of them show.

So do to the mouth what `densify_eye_region.py` did to the lid: put geometry
where the feature is, and nowhere else. Same gates, because they are the ones
that make it safe:
  * every ORIGINAL vertex's rest position must be untouched (Blender keeps
    originals at the FRONT of the array; new verts are inserted between them,
    `smooth=0` so they sit ON the old surface)
  * every shape key layer rides through the bmesh subdivision, interpolated, so
    a new vertex gets the right offset in every key instead of landing at Basis
  * ONE cut per pass, repeated. A face on the BOUNDARY of the selection has only
    some edges cut, so Blender fans it from the opposite vertex: 3 cuts makes
    four slivers across one long edge, which is the very thing being fixed here.

THE AUTHORITY IS HIS MEASURED INNER-LIP CONTOUR, the same one the carve is lofted
from, and unlike the eye landmarks it checks out against things outside itself:
1.15 mm from his skin, 4.28 mm from the sock rim, and the painted texture's green
channel halves at it.

  vendor/blender/blender -b -P tools/character/densify_mouth_rim.py -- \
      --rig renders/_recarve/MARS_FACE_CANDIDATE.blend --out <same>
"""
import bpy, bmesh, sys, os, json, math
import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d


def die(msg):
    # BLENDER -b SWALLOWS THE ARGUMENT TO sys.exit(). Print and flush first, or a
    # fail-closed refusal exits 1 with nothing printed and reads like a crash.
    print("*** REFUSED: %s" % msg, flush=True)
    sys.exit(1)


RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT_RIG = os.path.abspath(opt("--out", RIG))
RADIUS = float(opt("--radius-mm", "8"))
PASSES = int(opt("--passes", "2"))
TARGET_MIN = int(opt("--target-min", "300"))   # verts within 3 mm of the contour after
# THE RIM IS NOT THE COARSEST PART OF HIS MOUTH, AND IT IS NOT WHAT HE IS SEEING.
# Measured at WIDE on the candidate, ray-classified by MATERIAL:
#   the carved cavity wall is 49.9% of every pixel inside his open mouth
#   it is 377 faces at a MEDIAN of 20.0 mm2 against his skin's 0.426 mm2 (47x)
#   neighbouring cavity faces sit 39.2 deg apart at p90 and 70.9 deg at worst
# and it is NOT a shading bug: those faces are 377/377 use_smooth and their
# shading normals bend 12.94 deg from the face normal at the median, MORE than
# his skin's 5.67. A surface that turns 39 deg between neighbours reads as a
# flat card however well it is smoothed.
# Densifying the RIM alone was run and rejected -- the render did not change --
# because the rim was never the thing covering half the opening.
INCLUDE_CAVITY = "--include-cavity" in argv
CAVITY_TARGET = float(opt("--cavity-target-mm2", "6.0"))
# AND THE RIM'S WORST FACES WERE NEVER BEING CUT AT ALL.
# subdivide_edges only cuts an edge when BOTH ends are selected, and the
# selection was "vertices within RADIUS of the contour". The faces that make his
# lips look jagged have edges up to 28.9 mm long -- longer than the band is wide
# -- so one end always fell outside and the edge was skipped every pass.
# The receipt: rim faces went 288 -> 3105 and the median 1.54 -> 0.03 mm2 while
# the MAX did not move one decimal place, 136.68 -> 136.68 mm2.
# Selecting by FACE fixes it: if a face is near his lip, take all of its verts,
# so all of its edges are cut and the face is actually subdivided.
RIM_BY_FACE = "--rim-by-face" in argv
RIM_MAX_TARGET = float(opt("--rim-max-mm2", "12.0"))
# AND EVEN BY-FACE IS NOT ENOUGH, BECAUSE THE BOUNDARY IS THE PROBLEM.
# A face with only SOME of its verts selected has only some edges cut, so Blender
# fans it from the opposite corner -- which yields long thin pieces, and one of
# them can be BIGGER than anything that was in the measured band before. Measured
# at radius 12: rim max 136.68 -> 183.88 mm2, a face fanned off a 214.64 mm2
# neighbour that the band never reached.
# FACE CLOSURE fixes it at the source: repeatedly take every vertex of every face
# that has ANY selected vertex. Then every face touching the selection is FULLY
# selected, every one of its edges is cut, and no face is ever fanned.
CLOSURE = int(opt("--face-closure", "0"))
# A FIXED BAND CAN NEVER FINISH THE JOB, BECAUSE THE BIG FACES ARE EVERYWHERE.
# Measured on the candidate: 65 faces over 12 mm2 lie within 10 mm of his lip
# contour, 99 within 12 mm, 239 within 25 mm, the worst 214.64 mm2. Whatever
# radius is chosen, the faces just outside it stay huge and keep reading as
# jagged the moment his mouth opens into them.
# So target SIZE, not distance: inside a generous region round his mouth, cut
# every face bigger than MAX_FACE, close over whole faces, and REPEAT until
# nothing in the region is over the limit. That terminates on the thing being
# asked for ("as many of the jagged triangles as possible made smaller") instead
# of on a radius somebody guessed.
# AND ONE FACE SURVIVED EVERY PASS, AT EXACTLY 136.68 mm2, THREE TIMES.
# Not a stubborn triangle -- face 19813 is a FIFTEEN-SIDED N-GON:
#   verts [23716, 10313, 9197, 23698, 31177, 28387, 29923, 23714, ... ] (15)
# subdivide_edges adds vertices ALONG an n-gon's edges and never splits the face,
# so its area is invariant however many passes run. Reading the same number to
# two decimal places after 3 passes and +214,408 vertices is the signature.
# This repo already banked the rule from the SURFACE_DEFORM work: TRIANGULATE
# FIRST, because cutting an n-gon afterwards hands two triangles to an edge that
# already had two faces.
TRIANGULATE = "--triangulate-region" in argv
MAX_FACE = float(opt("--max-face-mm2", "0"))     # 0 = off, use the band instead
REGION = float(opt("--region-mm", "30"))
SAVE = "--no-save" not in argv

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0                      # his own millimetre (OWNER's measured anchor)
SEAM = np.vstack([np.array(anat["contours"]["lip_inner_upper"], float),
                  np.array(anat["contours"]["lip_inner_lower"], float)])

bpy.ops.wm.open_mainfile(filepath=RIG)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH in %s" % RIG)
me = o.data
n0 = len(me.vertices)
keys0 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
P0 = np.array([v.co[:] for v in me.vertices], float)
W = np.array(o.matrix_world)
P0w = P0 @ W[:3, :3].T + W[:3, 3]


def to_seam(pts):
    return np.array([float(np.linalg.norm(SEAM - q, axis=1).min()) for q in pts]) / MM


def face_areas():
    return np.array([p.area for p in me.polygons], float) / (MM * MM)


def _ngons_now():
    C = np.array([p.center[:] for p in me.polygons]) @ W[:3, :3].T + W[:3, 3]
    dd = to_seam(C)
    return int(sum(1 for i, p in enumerate(me.polygons)
                   if dd[i] < RADIUS and len(p.vertices) > 3))


NGON_BEFORE = _ngons_now()

d0 = to_seam(P0w)
near0 = int((d0 < 3.0).sum())
# how coarse is the rim RIGHT NOW -- the number the owner's "big ugly triangles"
# is about, restricted to the faces that actually form the opening
fa = face_areas()
rim_f = [i for i, p in enumerate(me.polygons)
         if to_seam((np.array(p.center[:]) @ W[:3, :3].T + W[:3, 3])[None, :])[0] < RADIUS]
a0 = fa[rim_f] if rim_f else np.array([0.0])
print("before: %d verts within 3 mm of his lip contour · %d faces within %.0f mm "
      "(median %.2f mm2, max %.2f mm2)"
      % (near0, len(rim_f), RADIUS, float(np.median(a0)), float(a0.max())), flush=True)
print("        whole-head median face area %.2f mm2" % float(np.median(fa)), flush=True)

ORAL_SLOTS = {i for i, m in enumerate(me.materials)
              if m and m.name.split(".")[0] == "MARS_ORAL_MAT"}


def cavity_faces():
    return [p for p in me.polygons if p.material_index in ORAL_SLOTS]


def cavity_stats():
    """Median/max face area and the angle between neighbouring faces -- the two
    numbers that say whether the inside of his mouth can describe a surface."""
    fs = cavity_faces()
    if not fs:
        return 0, 0.0, 0.0, 0.0, 0.0
    ar = np.array([p.area for p in fs], float) / (MM * MM)
    adj = {}
    for p in fs:
        for k in p.edge_keys:
            adj.setdefault(k, []).append(np.array(p.normal[:], float))
    ang = []
    for k, ns in adj.items():
        if len(ns) != 2:
            continue
        c = float(np.dot(ns[0], ns[1]))
        ang.append(math.degrees(math.acos(max(-1.0, min(1.0, c)))))
    ang = np.array(ang) if ang else np.array([0.0])
    return (len(fs), float(np.median(ar)), float(ar.max()),
            float(np.percentile(ang, 90)), float(ang.max()))

c0 = cavity_stats()
print("cavity wall before: %d faces  area median %.2f max %.2f mm2  "
      "neighbour angle p90 %.1f max %.1f deg" % c0, flush=True)

sel = d0 < RADIUS
if RIM_BY_FACE:
    byface = np.zeros(n0, bool)
    for p_ in me.polygons:
        c = (np.array(p_.center[:]) @ W[:3, :3].T + W[:3, 3])[None, :]
        if to_seam(c)[0] < RADIUS:
            for i in p_.vertices:
                if i < n0:
                    byface[i] = True
    print("rim-by-face adds %d verts to the %d within %.0f mm (union %d) -- this is "
          "what lets a 28.9 mm edge be cut" % (int((byface & ~sel).sum()), int(sel.sum()),
                                               RADIUS, int((sel | byface).sum())), flush=True)
    sel = sel | byface
if INCLUDE_CAVITY:
    cav_v = set()
    for p in cavity_faces():
        cav_v.update(int(i) for i in p.vertices)
    extra = np.zeros(n0, bool)
    for i in cav_v:
        if i < n0:
            extra[i] = True
    print("adding %d cavity-wall verts to the %d rim verts (union %d)"
          % (int(extra.sum()), int(sel.sum()), int((sel | extra).sum())), flush=True)
    sel = sel | extra
for _c in range(CLOSURE):
    grow = np.zeros(n0, bool)
    for p_ in me.polygons:
        vs = [int(i) for i in p_.vertices if i < n0]
        if any(sel[i] for i in vs):
            for i in vs:
                grow[i] = True
    added = int((grow & ~sel).sum())
    sel = sel | grow
    print("  face closure %d: +%d verts (no face can now be partially cut) -> %d"
          % (_c + 1, added, int(sel.sum())), flush=True)

print("selecting %d of %d verts (rim within %.0f mm of his measured lip contour%s)"
      % (int(sel.sum()), n0, RADIUS,
         " + the MARS_ORAL_MAT cavity wall" if INCLUDE_CAVITY else ""), flush=True)
if sel.sum() < 20:
    die("only %d vertices lie within %.0f mm of the lip contour -- nothing to densify"
        % (int(sel.sum()), RADIUS))

bm = bmesh.new()
bm.from_mesh(me)
bm.verts.ensure_lookup_table()
shape_layers = list(bm.verts.layers.shape.keys())
print("carrying %d shape key layer(s) through the subdivision" % len(shape_layers), flush=True)

keep = set(int(i) for i in np.nonzero(sel)[0])

if TRIANGULATE:
    bm.faces.ensure_lookup_table(); bm.verts.ensure_lookup_table()
    # ANY vertex, not ALL of them. Requiring every vertex left the 51-gons out --
    # they reach further than the band by definition, which is exactly what makes
    # them the worst faces. 136.68 -> 121.58 mm2 on the all-verts rule; the
    # remaining offender was simply the next n-gon the rule could not see.
    ngons = [f for f in bm.faces
             if len(f.verts) > 3 and any(v.index in keep for v in f.verts)]
    if ngons:
        worst = max(f.calc_area() for f in ngons) / (MM * MM)
        sides = max(len(f.verts) for f in ngons)
        print("  triangulating %d n-gon(s) in the selection (up to %d sides, worst "
              "%.2f mm2) -- subdivide_edges cannot split these" % (len(ngons), sides, worst),
              flush=True)
        for f in ngons:                       # their verts join the selection, or the
            for v in f.verts:                 # triangles they become are never cut
                keep.add(v.index)
        bmesh.ops.triangulate(bm, faces=ngons)
        bm.faces.ensure_lookup_table(); bm.verts.ensure_lookup_table()
        # CLOSE THE SELECTION AGAIN, ON THE NEW FACES.
        # Triangulating a fan-shaped n-gon yields one long triangle reaching far
        # outside the band, and those faces did not exist when the closure ran.
        # Left partially selected they are fanned again instead of cut, which is
        # exactly the residue the population gate kept catching (23 -> 12, 16 -> 5).
        for _c in range(max(1, CLOSURE)):
            grow = set()
            for f in bm.faces:
                vs = [v.index for v in f.verts]
                if any(i in keep for i in vs):
                    grow.update(vs)
            before_n = len(keep); keep |= grow
            print("    post-triangulate closure %d: +%d verts" % (_c + 1, len(keep) - before_n),
                  flush=True)
    else:
        print("  no n-gons in the selection", flush=True)

if MAX_FACE > 0:
    # ADAPTIVE: cut what is too big, wherever it is round his mouth, and stop
    # when nothing is. Every gate below still applies unchanged.
    Wm = np.array(o.matrix_world)
    for _p in range(PASSES):
        bm.faces.ensure_lookup_table(); bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
        C = np.array([f.calc_center_median()[:] for f in bm.faces], float)
        Cw = C @ Wm[:3, :3].T + Wm[:3, 3]
        # vectorised distance from every face centre to the measured contour
        d = np.sqrt(((Cw[:, None, :] - SEAM[None, :, :]) ** 2).sum(-1)).min(1) / MM
        A = np.array([f.calc_area() for f in bm.faces], float) / (MM * MM)
        big = np.nonzero((d < REGION) & (A > MAX_FACE))[0]
        inreg = int((d < REGION).sum())
        if len(big) == 0:
            print("  pass %d: nothing over %.1f mm2 left within %.0f mm of his lip contour"
                  % (_p + 1, MAX_FACE, REGION), flush=True)
            break
        vsel = set()
        for fi in big:
            vsel.update(v.index for v in bm.faces[int(fi)].verts)
        for _c in range(max(1, CLOSURE)):
            grow = set()
            for f in bm.faces:
                vs = [v.index for v in f.verts]
                if any(i in vsel for i in vs):
                    grow.update(vs)
            vsel |= grow
        edges = [e for e in bm.edges if e.verts[0].index in vsel and e.verts[1].index in vsel]
        print("  pass %d: %d of %d faces in the region are over %.1f mm2 "
              "(worst %.1f) -> subdividing %d edges"
              % (_p + 1, len(big), inreg, MAX_FACE, float(A[big].max()), len(edges)), flush=True)
        if not edges:
            break
        bmesh.ops.subdivide_edges(bm, edges=edges, cuts=1, use_grid_fill=(not TRIANGULATE), smooth=0.0)
        if TRIANGULATE:
            # NEVER LEAVE AN N-GON BEHIND. A partially-cut boundary face
            # becomes one, a 51-gon tessellates into slivers, and those
            # slivers are the shards on screen.
            bm.faces.ensure_lookup_table()
            # BY REGION, NOT BY `keep`. After pass 1 the new vertices carry
            # indices that are not in keep, so a keep-based test missed almost
            # every n-gon the pass had just made: 152 -> 15,650 in one run.
            _fc = np.array([f.calc_center_median()[:] for f in bm.faces]) @ W[:3, :3].T + W[:3, 3]
            _fd = to_seam(_fc)
            leftover = [f for i_, f in enumerate(bm.faces)
                        if len(f.verts) > 3 and _fd[i_] < RADIUS * 1.6]
            if leftover:
                bmesh.ops.triangulate(bm, faces=leftover)
                bm.faces.ensure_lookup_table()
                print('    a pass left %d n-gon(s); triangulated' % len(leftover), flush=True)
    PASSES_DONE = True
else:
    PASSES_DONE = False

for _p in range(0 if PASSES_DONE else PASSES):
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
    inside = [e for e in bm.edges
              if (e.verts[0].index in keep or e.verts[0].index >= n0)
              and (e.verts[1].index in keep or e.verts[1].index >= n0)]
    if not inside:
        break
    print("  pass %d: subdividing %d edges with 1 cut" % (_p + 1, len(inside)), flush=True)
    bmesh.ops.subdivide_edges(bm, edges=inside, cuts=1, use_grid_fill=(not TRIANGULATE), smooth=0.0)
    if TRIANGULATE:
        # NEVER LEAVE AN N-GON BEHIND. A partially-cut boundary face
        # becomes one, a 51-gon tessellates into slivers, and those
        # slivers are the shards on screen.
        bm.faces.ensure_lookup_table()
        # BY REGION, NOT BY `keep`. After pass 1 the new vertices carry
        # indices that are not in keep, so a keep-based test missed almost
        # every n-gon the pass had just made: 152 -> 15,650 in one run.
        _fc = np.array([f.calc_center_median()[:] for f in bm.faces]) @ W[:3, :3].T + W[:3, 3]
        _fd = to_seam(_fc)
        leftover = [f for i_, f in enumerate(bm.faces)
                    if len(f.verts) > 3 and _fd[i_] < RADIUS * 1.6]
        if leftover:
            bmesh.ops.triangulate(bm, faces=leftover)
            bm.faces.ensure_lookup_table()
            print('    a pass left %d n-gon(s); triangulated' % len(leftover), flush=True)
bm.to_mesh(me); bm.free(); me.update()

n1 = len(me.vertices)
P1 = np.array([v.co[:] for v in me.vertices], float)
print("verts %d -> %d (+%d)" % (n0, n1, n1 - n0), flush=True)

# ---- GATES ---------------------------------------------------------------
drift = float(np.abs(P1[:n0] - P0).max()) / MM
print("original vertices' rest drift: %.6f mm" % drift, flush=True)
if drift > 1e-4:
    die("subdivision moved the ORIGINAL vertices by %.6f mm. Every measurement "
        "banked against this mesh would be invalidated." % drift)

keys1 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
if keys1 != keys0:
    die("shape keys changed: %d -> %d" % (len(keys0), len(keys1)))

# AN UNTRANSFERABLE SHAPE IS OMITTED, NOT BANKED AS ZEROS -- so a key that now
# moves nothing is REPORTED rather than silently carried.
B = np.array([d.co[:] for d in me.shape_keys.key_blocks["Basis"].data], float)
dead = []
for k in me.shape_keys.key_blocks:
    if k.name == "Basis":
        continue
    A = np.array([d.co[:] for d in k.data], float)
    if float(np.linalg.norm(A - B, axis=1).max()) / MM < 0.05:
        dead.append(k.name)
if dead:
    print("  NOTE: %d key(s) move nothing afterwards: %s" % (len(dead), dead[:8]), flush=True)

P1w = P1 @ W[:3, :3].T + W[:3, 3]
d1 = to_seam(P1w)
near1 = int((d1 < 3.0).sum())
fa1 = face_areas()
rim_f1 = [i for i, p in enumerate(me.polygons)
          if to_seam((np.array(p.center[:]) @ W[:3, :3].T + W[:3, 3])[None, :])[0] < RADIUS]
a1 = fa1[rim_f1] if rim_f1 else np.array([0.0])
print("after:  %d verts within 3 mm of his lip contour · %d faces within %.0f mm "
      "(median %.2f mm2, max %.2f mm2)"
      % (near1, len(rim_f1), RADIUS, float(np.median(a1)), float(a1.max())), flush=True)
c1 = cavity_stats()
print("cavity wall after : %d faces  area median %.2f max %.2f mm2  "
      "neighbour angle p90 %.1f max %.1f deg" % c1, flush=True)
if INCLUDE_CAVITY and c1[1] > CAVITY_TARGET:
    die("the cavity wall is still %.2f mm2 per face at the median (wanted <= %.2f). "
        "It is half of every pixel inside his open mouth, so leaving it coarse "
        "leaves the defect he is looking at." % (c1[1], CAVITY_TARGET))

if RIM_BY_FACE:
    # A SINGLE MAX CANNOT TELL ONE STUBBORN FACE FROM A COARSE RIM.
    # Gating on max refused a run that took the band from 52 oversized faces to 2
    # -- because one triangle has its centre 11.4 mm inside the band and a vertex
    # 22.3 mm outside it. That is the same error as judging a blink by counting
    # occlusion: the number cannot express the thing being asked about.
    # So gate on the POPULATION, which is what "jagged triangles" means, and
    # report the max beside it instead of letting it veto.
    over0 = int((a0 > RIM_MAX_TARGET).sum())
    over1 = int((a1 > RIM_MAX_TARGET).sum())
    print("  faces over %.0f mm2 in the band: %d -> %d   (worst %.2f -> %.2f mm2)"
          % (RIM_MAX_TARGET, over0, over1, float(a0.max()), float(a1.max())), flush=True)
    if over0 == 0:
        print("  nothing in the band was oversized to begin with", flush=True)
    elif over1 > max(2, int(0.2 * over0)):
        die("%d of %d oversized faces remain in the band (wanted at most %d). The "
            "median falling while the population stands still is the signature of "
            "edges that were never cut."
            % (over1, over0, max(2, int(0.2 * over0))))
    if float(a1.max()) > RIM_MAX_TARGET:
        print("  NOTE: %d face(s) still over the limit, worst %.2f mm2 -- named, not "
              "hidden. Their centres sit inside the band while a vertex reaches "
              "outside it." % (over1, float(a1.max())), flush=True)

if near1 < TARGET_MIN:
    die("the rim still has only %d vertices within 3 mm of his lip contour (wanted "
        ">= %d). Raise --passes or --radius-mm; an opening cut through this would "
        "shed the same shards with more steps." % (near1, TARGET_MIN))

# N-GONS ARE WHAT THE SHARDS ARE MADE OF, AND THIS TOOL WAS CREATING THEM.
# Measured across the chain: canonical 210 n-gons in the mouth region, max 15
# sides; after ONE densify pass 1,666, max 51. And they cannot be repaired
# afterwards -- triangulating them took the region from 704 slivers to 3,658.
# They must not be made. So the count is a GATE.
NGON_AFTER = _ngons_now()
print("  n-gons in the mouth region: %d -> %d" % (NGON_BEFORE, NGON_AFTER), flush=True)
if NGON_AFTER > NGON_BEFORE:
    die("this pass CREATED %d n-gon(s) in his mouth (%d -> %d). They tessellate "
        "into slivers and those slivers are the shards on screen."
        % (NGON_AFTER - NGON_BEFORE, NGON_BEFORE, NGON_AFTER))

rep = {"schema": "trippedd.densify-mouth-rim/v1", "rig": RIG, "out": OUT_RIG,
       "regionNgons": [NGON_BEFORE, NGON_AFTER],
       "radiusMM": RADIUS, "passes": PASSES,
       "authority": "his measured inner-lip contour (renders/_rig_measure/mouth_anatomy.json) "
                    "-- 1.15 mm from his skin, 4.28 mm from the sock rim, and the painted "
                    "texture's green channel halves at it",
       "vertsBefore": n0, "vertsAfter": n1,
       "within3mmBefore": near0, "within3mmAfter": near1,
       "rimFaceAreaMM2Before": {"count": len(rim_f), "median": round(float(np.median(a0)), 3),
                                "max": round(float(a0.max()), 3)},
       "rimFaceAreaMM2After": {"count": len(rim_f1), "median": round(float(np.median(a1)), 3),
                               "max": round(float(a1.max()), 3)},
       "wholeHeadMedianFaceAreaMM2": round(float(np.median(fa1)), 3),
       "originalRestDriftMM": round(drift, 8),
       "keysCarried": len(keys0) - 1, "keysMovingNothing": dead,
       "STALE_BECAUSE_VERTEX_COUNT_CHANGED": [
           "docs/evidence/hair/_valley_CAGE.npy -> _hairzones.npy (regenerate: "
           "tools/hair/valley_discriminator.py then tools/hair/hair_zones.py, IN THAT ORDER)",
           "assets/donor/gnm_face/_mars_verts.npy and assets/donor/facs/ "
           "(regenerate: dump_mars_verts.py then facs_donor.py)",
           "any tool that indexes MARS_MESH by vertex id"]}
od = os.path.join(ROOT, "docs", "evidence", "oral")
os.makedirs(od, exist_ok=True)
rp = os.path.join(od, "densify_mouth_rim.json")
json.dump(rep, open(rp, "w"), indent=2)
print("wrote %s" % rp, flush=True)

if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT_RIG, compress=True)
    print("saved %s" % OUT_RIG, flush=True)
else:
    print("--no-save: nothing written", flush=True)
