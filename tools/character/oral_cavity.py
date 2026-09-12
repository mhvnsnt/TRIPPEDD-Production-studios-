"""
CARVE THE ORAL CAVITY — out of Mars's own head, along his own measured mouth.

Every previous attempt put a separate dark object NEAR the mouth and hoped it
read as an interior. It cannot: a floating sphere has a front surface, and that
surface sat 0.0171 units — 8.9% of his mouth width — IN FRONT of the lip plane.
A ball shoved into the face, exactly as it rendered.

The cavity is not an object placed near the mouth. It is a VOID cut out of the
head, so its walls are the head's own surface turned inward and it can never
protrude through anything. The lips are the boundary of that void.

WHY THIS WAS NOT POSSIBLE BEFORE — the finding that unblocked it:
    MEASURED on MARS_LOD2: 47,021 verts, 104,281 edges, 68,237 of them BOUNDARY
    edges. The scan arrived as loose triangles — glTF split a vertex for every
    corner whose normal or UV differed, so two-thirds of the mesh's edges were
    shared with nothing.
    Welding at 1e-6 (one part in 840,000 of head height — no surface point moves
    by as much as a micron) gives 23,373 verts and EIGHT boundary edges. The head
    was watertight all along; only its index buffer said otherwise.
That is why edge-splitting tore the face into shards: the mesh was already
shards. It is also why a boolean could not be trusted. Both are fixed by welding
first, and the weld is verified to move nothing.

  vendor/blender/blender -b -P tools/character/oral_cavity.py -- --lod LOD2
"""
import bpy, bmesh, sys, os, json, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
LOD = opt("--lod", "LOD2")
WORK = os.path.abspath(opt("--work", "renders/_rig_measure"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_ORAL.blend"))
WELD = float(opt("--weld", "1e-6"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)

M_ANAT = json.load(open(os.path.join(WORK, "mouth_anatomy.json")))
FR = M_ANAT["frame"]
MW = M_ANAT["aperture"]["width"]                      # measured mouth width
FRAME = mathutils.Matrix(FR["matrix"])
FINV = FRAME.inverted()
V = mathutils.Vector

def to_local(p): return FINV @ V(p)
def to_world(p): return FRAME @ V(p)

# ── load and WELD ────────────────────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "assets/source_models", "MARS_%s.glb" % LOD))
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
if not meshes: sys.exit("the GLB imported no mesh")
bpy.ops.object.select_all(action="DESELECT")
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1: bpy.ops.object.join()
head = bpy.context.view_layer.objects.active
head.name = "MARS_MESH"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

before_pts = sorted(tuple(round(c, 6) for c in v.co) for v in head.data.vertices)
before_n = len(head.data.vertices)

bm = bmesh.new(); bm.from_mesh(head.data)
b0 = sum(1 for e in bm.edges if e.is_boundary)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=WELD)
b1 = sum(1 for e in bm.edges if e.is_boundary)
nm1 = sum(1 for e in bm.edges if not e.is_manifold)
# The eight leftover boundary edges are genuine pinholes in the scan. Fill them,
# or the boolean has an escape route and the "cavity" leaks out of the skull.
if b1:
    bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
    b2 = sum(1 for e in bm.edges if e.is_boundary)
else:
    b2 = 0
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(head.data); bm.free()
head.data.update()

after_pts = sorted(tuple(round(c, 6) for c in v.co) for v in head.data.vertices)
print("WELD  %d verts -> %d · boundary edges %d -> %d -> %d (holes filled) · non-manifold %d"
      % (before_n, len(head.data.vertices), b0, b1, b2, nm1))
# PROOF that no surface point moved: the welded set must be a subset of the
# original set of positions, with nothing new invented.
lost = set(after_pts) - set(before_pts)
if lost:
    sys.exit("WELD MOVED GEOMETRY — %d positions are not in the original scan. Refusing." % len(lost))
print("      every surviving vertex position is identical to the scan (0 moved)")

# ── the cavity solid, lofted from the MEASURED aperture curve ────────────────
# Ring 0 is literally the inner-lip contour MediaPipe found on his face, flattened
# in Z so the rest pose reads as closed lips rather than a parted mouth. Behind
# it the section grows into a real oral volume and then closes at the throat.
inner_up = [to_local(p) for p in M_ANAT["contours"]["lip_inner_upper"]]
inner_lo = [to_local(p) for p in M_ANAT["contours"]["lip_inner_lower"]]
loop = inner_up + list(reversed(inner_lo))[1:-1]          # closed polygon, 20 pts

def resample_closed(poly, n):
    """Even arc-length resampling of a closed polygon, in the local XZ plane.

    The cavity was rendering as a rectangular prism with hard corners. That was
    not the profile being wrong -- it was 20 samples of it, carried straight
    through to a 20-sided tube. Denser sampling of the SAME measured curve makes
    it read as an oral cavity instead of a box, and invents no new anatomy.
    """
    segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
    lens = [max(1e-12, math.hypot(b.x - a.x, b.z - a.z)) for a, b in segs]
    total = sum(lens)
    out, target, acc, k = [], 0.0, 0.0, 0
    for _ in range(n):
        while k < len(segs) - 1 and acc + lens[k] < target:
            acc += lens[k]; k += 1
        a, b = segs[k]
        t = min(1.0, max(0.0, (target - acc) / lens[k]))
        out.append(a.lerp(b, t))
        target += total / n
    return out

loop = resample_closed(loop, int(opt("--ring", "56")))
# Force a known winding in the local XZ plane. Whether the measured contour
# happens to come back clockwise or anticlockwise is an accident of which
# MediaPipe indices were listed first, and it decides which way the lofted
# solid's faces end up pointing.
_area = sum((loop[i].x * loop[(i + 1) % len(loop)].z - loop[(i + 1) % len(loop)].x * loop[i].z)
            for i in range(len(loop))) * 0.5
if _area < 0:
    loop = [loop[0]] + list(reversed(loop[1:]))
    print("contour wound clockwise; reversed so the loft faces outward")
N = len(loop)
SLIT_Z = float(opt("--slit-z", "0.42"))   # rest slit = 42% of the measured contour height
cx = sum(p.x for p in loop) / N
for p in loop:
    p.z *= SLIT_Z

def ellipse_ring(half_w, half_h, z_c, y, n=N):
    """A superellipse: a mouth is a flattened oval, not a circle."""
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        c, s = math.cos(t), math.sin(t)
        e = 2.05   # ~ellipse; 2.4 squared the corners off
        x = cx + half_w * math.copysign(abs(c) ** (2 / e), c)
        z = z_c + half_h * math.copysign(abs(s) ** (2 / e), s)
        out.append(V((x, y, z)))
    return out

# Align the ellipse's parametrisation with the contour loop's, so the loft does
# not twist: the contour starts at the LEFT corner and runs over the top.
def aligned_ring(half_w, half_h, z_c, y):
    r = ellipse_ring(half_w, half_h, z_c, y)
    base = loop
    best, bestd = 0, 1e18
    for k in range(N):
        d = sum(((r[(i + k) % N].x - base[i].x) ** 2 + (r[(i + k) % N].z - base[i].z) ** 2)
                for i in range(N))
        if d < bestd: best, bestd = k, d
    return [r[(i + best) % N] for i in range(N)]

# The cavity has to HOLD real anatomy. A 55 mm dental arch and a 45 mm tongue
# do not fit in a void half a mouth-width across, and the visible result is a
# small mouth with small teeth in it. Sized from the same millimetre anchor the
# teeth use: MW = 0.1930 units is a ~50 mm inter-commissure, so 1 mm = MW/50.
MM = MW / 50.0
HW = 36.5 * MM        # half-width: the mandibular body flares to 69 mm, and that is real
# y is measured along the frame's "into the head" axis, from the aperture centre.
FRONT = float(opt("--front", "-0.075"))    # start well clear of the lip surface
SECTIONS = [
    # (y,                    half_w,      half_h,      z_centre,  blend to ellipse)
    (FRONT,                  None,        None,        0.0,       0.0),   # prism: the slit
    (MW * 0.035,             None,        None,        0.0,       0.0),   # still the slit
    (MW * 0.13,              HW * 0.95,   MW * 0.30,  -MW * 0.06, 0.75),  # opening out
    (MW * 0.34,              HW * 0.92,   MW * 0.36,  -MW * 0.07, 1.0),   # the cavity
    (MW * 0.70,              HW * 0.84,   MW * 0.34,  -MW * 0.06, 1.0),   # mid
    (MW * 1.00,              HW * 0.58,   MW * 0.24,  -MW * 0.04, 1.0),   # toward the throat
    (MW * 1.18,              HW * 0.20,   MW * 0.09,  -MW * 0.02, 1.0),   # throat closes
]
CAP_Y = MW * 1.26

bm = bmesh.new()
rings = []
for (y, hw, hh, zc, blend) in SECTIONS:
    if blend <= 0.0:
        pts = [V((p.x, y, p.z)) for p in loop]
    else:
        el = aligned_ring(hw, hh, zc, y)
        pts = [loop[i].lerp(V((el[i].x, y, el[i].z)), blend) for i in range(N)]
        for p in pts: p.y = y
    rings.append([bm.verts.new(to_world(p)) for p in pts])
bm.verts.ensure_lookup_table()

for a, b in zip(rings, rings[1:]):
    for i in range(N):
        j = (i + 1) % N
        bm.faces.new((a[i], a[j], b[j], b[i]))
# front cap (in front of the face, gets cut away) and throat cap
front_c = bm.verts.new(to_world(V((cx, FRONT - MW * 0.05, 0.0))))
back_c = bm.verts.new(to_world(V((cx, CAP_Y, -MW * 0.02))))
for i in range(N):
    j = (i + 1) % N
    bm.faces.new((rings[0][j], rings[0][i], front_c))
    bm.faces.new((rings[-1][i], rings[-1][j], back_c))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
# THE CUTTER MUST BE A VALID SOLID, and this is checked rather than assumed.
# An open, non-manifold or inward-facing cutter does not make the boolean throw
# -- it makes it produce garbage, and the garbage looks like a dark plug sitting
# in the character's face. MEASURED before this check existed: 100 of 834
# oral-material vertices ended up IN FRONT of the lip surface at REST, and
# rendering the open mouth with teeth, tongue and gums all hidden still showed
# the plug, which is how it was finally pinned on the cutter.
_bound = sum(1 for e in bm.edges if e.is_boundary)
_nonman = sum(1 for e in bm.edges if not e.is_manifold)
_vol = bm.calc_volume(signed=True)
print("cutter solid: %d verts · boundary edges %d · non-manifold %d · signed volume %+.6f"
      % (len(bm.verts), _bound, _nonman, _vol))
if _bound or _nonman:
    sys.exit("THE CAVITY CUTTER IS NOT A CLOSED SOLID (%d boundary, %d non-manifold) -- a boolean "
             "against it produces geometry, not a void." % (_bound, _nonman))
if _vol < 0:
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    print("cutter normals pointed inward (volume %+.6f); flipped" % _vol)
    _vol = bm.calc_volume(signed=True)
if _vol <= 0:
    sys.exit("THE CAVITY CUTTER HAS NO POSITIVE VOLUME (%+.6f)" % _vol)

cav_me = bpy.data.meshes.new("MARS_ORAL_VOID_MESH")
bm.to_mesh(cav_me); bm.free()
cutter = bpy.data.objects.new("MARS_ORAL_VOID", cav_me)
bpy.context.scene.collection.objects.link(cutter)

oral = bpy.data.materials.new("MARS_ORAL_MAT")
oral.use_nodes = True
p = oral.node_tree.nodes["Principled BSDF"]
p.inputs["Base Color"].default_value = (0.055, 0.016, 0.030, 1)
p.inputs["Roughness"].default_value = 0.62
p.inputs["Specular IOR Level"].default_value = 0.30
cav_me.materials.append(oral)

print("cavity solid: %d rings x %d pts · depth %.4f (%.2f x mouth width) · max half-width %.4f"
      % (len(rings), N, CAP_Y - FRONT, (CAP_Y - FRONT) / MW, max(s[1] or HW for s in SECTIONS)))

# ── carve ────────────────────────────────────────────────────────────────────
head_pts_before = {tuple(round(c, 5) for c in v.co) for v in head.data.vertices}
md = head.modifiers.new("ORAL_CAVITY", "BOOLEAN")
md.operation = "DIFFERENCE"
md.object = cutter
md.solver = "EXACT"
md.material_mode = "TRANSFER"     # the void's walls get the oral material
bpy.context.view_layer.objects.active = head
bpy.ops.object.modifier_apply(modifier=md.name)
bpy.data.objects.remove(cutter, do_unlink=True)

print("carved: %d verts, %d faces, materials %s"
      % (len(head.data.vertices), len(head.data.polygons), [m.name for m in head.data.materials]))

# ── VERIFY the carve did what it claims ─────────────────────────────────────
# 1. The exterior AWAY from the mouth is untouched, vertex for vertex.
zone = MW * 0.95
kept, moved_out = 0, 0
for v in head.data.vertices:
    l = to_local(v.co)
    if abs(l.x - cx) > zone or abs(l.z) > zone * 0.6 or l.y > MW * 1.4:
        t = tuple(round(c, 5) for c in v.co)
        if t in head_pts_before: kept += 1
        else: moved_out += 1
print("outside the mouth zone: %d vertices identical to the scan, %d new/changed" % (kept, moved_out))
if moved_out > 0:
    sys.exit("THE CARVE CHANGED GEOMETRY OUTSIDE THE MOUTH — Mars's likeness is not negotiable.")

# 2. There is a real hole: a ray fired at the lip line must land on ORAL material.
#    Checking "did the ray get past a plane" is not enough — his face curves back
#    to local y +0.017 at the mouth corners, so a plane test counts cheek hits as
#    mouth hits. Material identity cannot be fooled that way: only the void's own
#    walls carry MARS_ORAL_MAT.
deps = bpy.context.evaluated_depsgraph_get()
ev = head.evaluated_get(deps)
ORAL_SLOTS = {i for i, m in enumerate(head.data.materials) if m and m.name == "MARS_ORAL_MAT"}

# The seam is a CURVE, not a plane -- his mouth corners sit lower than its
# centre. Firing every ray at a flat local z = 0 misses the slit wherever the
# seam has moved away from it, and reads as "no aperture" on a mouth that is
# cut correctly. MEASURED: the same cut scored 8/41 on a flat probe and 39/41
# following the seam.
def seam_at(x):
    pts = sorted((p.x, p.z) for p in loop)
    if x <= pts[0][0]: return pts[0][1]
    if x >= pts[-1][0]: return pts[-1][1]
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            t = 0.0 if x1 == x0 else (x - x0) / (x1 - x0)
            return z0 + t * (z1 - z0)
    return 0.0

def probe(offset_from_seam, n=41, span=0.9):
    hits = 0
    for i in range(n):
        lx = cx + (i / (n - 1.0) - 0.5) * MW * span
        local_z = seam_at(lx) + offset_from_seam
        o = to_world(V((lx, -0.35, local_z)))
        d = (to_world(V((lx, 1.0, local_z))) - o).normalized()
        hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(deps, o, d)
        if hit and idx >= 0:
            try: mi = ob.data.polygons[idx].material_index
            except Exception: mi = -1
            if mi in ORAL_SLOTS: hits += 1
    return hits

through_seam = probe(0.0)
above = probe(MW * 0.20)
below = probe(-MW * 0.20)
print("rays landing on CAVITY WALL:  seam %d/41 · upper lip %d/41 · lower lip %d/41"
      % (through_seam, above, below))
if through_seam < 20:
    sys.exit("NO APERTURE — the lip line does not see the cavity (%d/41)" % through_seam)
if above > 4 or below > 4:
    sys.exit("THE CUT IS TOO TALL — cavity visible %d/%d rays above/below the lip line at rest"
             % (above, below))

# 3. The oral material actually got onto faces.
oral_idx = [i for i, m in enumerate(head.data.materials) if m and m.name == "MARS_ORAL_MAT"]
oral_faces = sum(1 for f in head.data.polygons if f.material_index in oral_idx) if oral_idx else 0
print("faces carrying the oral material: %d" % oral_faces)
if oral_faces < 50:
    sys.exit("the cavity walls did not receive the oral material")

# 4. NOTHING ORAL MAY STICK OUT OF HIS FACE.
#    This is the check that was missing, and its absence cost a full pass. The
#    verification above only looked sideways and backwards -- it never asked
#    whether the carve had left geometry in FRONT of the lips. It had: 100 of
#    834 oral-material vertices, because an inward-facing cutter makes DIFFERENCE
#    keep the cutter's own shell. From outside that reads as a dark plug shoved
#    into the character's mouth, which is exactly what the creator saw twice.
LIP_FRONT = M_ANAT["aperture"]["lipFrontLocalY"]
oral_verts, protruding = set(), []
for f in head.data.polygons:
    if f.material_index in ORAL_SLOTS:
        oral_verts.update(f.vertices)
for vi in oral_verts:
    ly = to_local(head.data.vertices[vi].co).y
    if ly < LIP_FRONT:
        protruding.append(round(ly, 5))
print("oral-material vertices: %d · in front of the lip surface (local y < %.4f): %d"
      % (len(oral_verts), LIP_FRONT, len(protruding)))
if protruding:
    sys.exit("ORAL GEOMETRY PROTRUDES THROUGH HIS FACE — %d vertices as far forward as %.4f. "
             "Refusing to save. This is the plug, not a mouth."
             % (len(protruding), min(protruding)))

smoothed = 0
for f in head.data.polygons:
    if f.material_index in ORAL_SLOTS:
        f.use_smooth = True; smoothed += 1
print("smooth-shaded %d cavity faces (flat shading on the walls was most of the 'box')" % smoothed)

bpy.ops.wm.save_as_mainfile(filepath=OUT)
json.dump({
    "source": "assets/source_models/MARS_%s.glb" % LOD,
    "weld": {"distance": WELD, "vertsBefore": before_n, "vertsAfter": len(head.data.vertices),
             "boundaryEdgesBefore": b0, "boundaryEdgesAfterWeld": b1, "afterHoleFill": b2,
             "surfacePointsMoved": 0},
    "cavity": {"method": "void carved OUT of the head by boolean DIFFERENCE, lofted from the "
                         "MediaPipe inner-lip contour raycast onto the real surface",
               "restSlitZScale": SLIT_Z, "depth": round(CAP_Y - FRONT, 5),
               "depthInMouthWidths": round((CAP_Y - FRONT) / MW, 3),
               "sections": len(SECTIONS)},
    "verification": {"exteriorVertsIdenticalOutsideMouthZone": kept,
                     "exteriorVertsChangedOutsideMouthZone": moved_out,
                     "seamRaysOnCavityWall": through_seam, "raysAboveMouth": above, "raysBelowMouth": below,
                     "oralMaterialFaces": oral_faces, "oralVerticesProtrudingThroughFace": len(protruding)},
}, open(os.path.join(os.path.dirname(OUT), "MARS_oral_cavity.json"), "w"), indent=2)
print("\noral cavity → %s" % OUT)
