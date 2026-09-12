"""
CARVE THE EYE APERTURES — so the blink has something to close over.

Same operation that opened the mouth, and for the same reason: an eye is an
APERTURE with anatomy behind it. Mars's eyes are painted into the scan -- the
surface there is unbroken skin with an iris in the texture -- so the lid had
nothing to travel over and eye_look_L / eye_look_R drove zero geometry.

ONE DIFFERENCE FROM THE MOUTH, AND IT MATTERS: a mouth is CLOSED at rest and a
pair of eyes is OPEN. So the mouth cutter was the lip contour flattened to a
slit, while these cut the measured lid contour at full size -- the rest pose is
the open eye, and the blink closes it.

  vendor/blender/blender -b -P tools/character/eye_sockets.py --
"""
import bpy, bmesh, sys, os, json, math, mathutils

sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_ORAL.blend"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_ORAL.blend"))
DONOR = os.path.abspath(opt("--donor", "assets/donor/gnm_eyes"))
V = mathutils.Vector
import numpy as np

# ── the appearance spec is CANON and it is READ, not remembered ─────────────
# HIS EYES ARE WHITE ON PURPOSE. The GNM donor ships sclera, iris and pupil as
# separate vertex classes, and a build that helpfully shades the iris blue
# because the donor has one has redesigned the character. In the canonical
# variant all three parts take the SCLERA material -- the geometry underneath
# stays capable of a pupil the moment a scene asks for one.
APPEAR = json.load(open(os.path.abspath("assets/rigs/MARS_appearance.json")))
VARIANT = opt("--variant", APPEAR.get("activeVariant", "canonical"))
# HOW MUCH OF THE MEASURED LID CONTOUR TO CUT.
# 0.86 cuts an opening wider than a correctly-seated 23 mm globe can back, so
# rays over the top of the eye reach the socket tunnel -- 18% of the aperture.
# Inflating the globe to plug that is what produced the bulging, too-round eye
# the owner rejected. The opening is the thing that should be smaller: a rest
# eye is NARROW, and a wide-eyed look comes from lifting the lid, not from
# carving a bigger hole. Swept against the real cut, not chosen.
INFLATE = float(opt("--inflate", "0.78"))
PROBE = "--probe" in argv        # report the hole instead of refusing, for diagnosis
if VARIANT not in APPEAR["variants"]:
    sys.exit("unknown appearance variant %r; have %s" % (VARIANT, list(APPEAR["variants"])))
VSPEC = APPEAR["variants"][VARIANT]

A = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
C = A["contours"]
# Every anatomical size in this project is stated through the measured mouth
# width: MW = 50 mm, so 1 mm = MW/50. An eyeball is 24 mm and a palpebral
# fissure is 28-30 mm, which is what makes "too small" a measurable claim
# rather than an impression.
MW_ANCHOR = 0.1930
EM = json.load(open(os.path.join(DONOR, "manifest.json")))

bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects["MARS_MESH"]
scene = bpy.context.scene
for stale in list(bpy.data.objects):
    if stale.name.startswith(("MARS_EYE", "MARS_LID_CUTTER")):
        bpy.data.objects.remove(stale, do_unlink=True)
for md in [m for m in head.modifiers if m.name.startswith("EYE_APERTURE")]:
    head.modifiers.remove(md)

def spec_mat(key):
    """Build a material from the appearance spec, by name."""
    sp = APPEAR["materials"][key]
    m = bpy.data.materials.new("MARS_%s_MAT" % key); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = tuple(sp["baseColor"])
    b.inputs["Roughness"].default_value = sp.get("roughness", 0.5)
    b.inputs["Specular IOR Level"].default_value = sp.get("specular", 0.5)
    if sp.get("subsurface"):
        b.inputs["Subsurface Weight"].default_value = sp["subsurface"]
    if sp.get("emission"):
        b.inputs["Emission Color"].default_value = tuple(sp["emission"])
        b.inputs["Emission Strength"].default_value = sp.get("emissionStrength", 0.0)
    return m

# Mars's eyes read WHITE and self-luminous in the scan. That is his look, and
# this adds an eye that can move -- it does not redesign the character's eye.
_cache = {}
def M(key):
    if key not in _cache: _cache[key] = spec_mat(key)
    return _cache[key]
# The socket is NOT oral tissue. Using the maroon oral material there put a red
# rim around each eye wherever the globe did not quite reach the lid margin.
# A near-black cool neutral reads as shadow, which is what an eye socket is.
M_SOCKET = M("SOCKET")
# class 0 sclera, 1 iris, 2 pupil -> whatever THIS VARIANT says they are
PARTS = VSPEC["eyeParts"]
CLASS_MAT = {0: M(PARTS["sclera"]), 1: M(PARTS["iris"]), 2: M(PARTS["pupil"])}
print("appearance variant %r: sclera->%s iris->%s pupil->%s"
      % (VARIANT, PARTS["sclera"], PARTS["iris"], PARTS["pupil"]))

before_n = len(head.data.vertices)
report = {}

for side in ("L", "R"):
    up = [V(p) for p in C["eye_%s_upper" % side]]
    lo = [V(p) for p in C["eye_%s_lower" % side]]
    ring = up + list(reversed(lo))[1:-1]
    centre = sum(ring, V((0, 0, 0))) / len(ring)
    ex = (up[-1] - up[0]).normalized()
    mid = len(up) // 2
    ez_ref = (up[mid] - lo[mid]).normalized()
    ey = ex.cross(ez_ref).normalized()
    if ey.y < 0: ey = -ey
    ez = ex.cross(ey).normalized()
    M = mathutils.Matrix(((ex.x, ey.x, ez.x, centre.x), (ex.y, ey.y, ez.y, centre.y),
                          (ex.z, ey.z, ez.z, centre.z), (0, 0, 0, 1)))
    Mi = M.inverted()
    loc = [Mi @ p for p in ring]
    # A consistent winding, or the lofted solid faces inward and DIFFERENCE
    # keeps the cutter instead of removing it -- the exact failure that put a
    # dark plug in his mouth for three passes.
    area = sum(loc[i].x * loc[(i + 1) % len(loc)].z - loc[(i + 1) % len(loc)].x * loc[i].z
               for i in range(len(loc))) * 0.5
    if area < 0: loc = [loc[0]] + list(reversed(loc[1:]))

    fissure = EM["eyes"]["eye_%s" % side]["fissureWidth"]
    bm = bmesh.new()
    rings = []
    # Straight prism through the lid: the aperture in the skin is the measured
    # contour, full size, because the rest pose of an eye is OPEN.
    # Cut slightly INSIDE the measured contour. MediaPipe's lid contour traces
    # the outer lid margin; cutting the whole of it leaves more hole than eye.
    for depth, inflate in ((-fissure * 0.35, INFLATE), (fissure * 0.06, INFLATE),
                           (fissure * 0.40, 0.80), (fissure * 0.70, 0.48)):
        rings.append([bm.verts.new(M @ V((p.x * inflate, depth, p.z * inflate))) for p in loc])
    N = len(loc)
    for a, b in zip(rings, rings[1:]):
        for i in range(N):
            bm.faces.new((a[i], a[(i + 1) % N], b[(i + 1) % N], b[i]))
    front = bm.verts.new(M @ V((0, -fissure * 0.45, 0)))
    back = bm.verts.new(M @ V((0, fissure * 0.80, 0)))
    for i in range(N):
        bm.faces.new((rings[0][(i + 1) % N], rings[0][i], front))
        bm.faces.new((rings[-1][i], rings[-1][(i + 1) % N], back))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if bm.calc_volume(signed=True) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    b_edges = sum(1 for e in bm.edges if e.is_boundary)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    vol = bm.calc_volume(signed=True)
    me = bpy.data.meshes.new("MARS_LID_CUTTER_%s_MESH" % side)
    bm.to_mesh(me); bm.free()
    cutter = bpy.data.objects.new("MARS_LID_CUTTER_%s" % side, me)
    scene.collection.objects.link(cutter)
    me.materials.append(M_SOCKET)
    print("lid cutter %s: boundary %d · non-manifold %d · signed volume %+.7f"
          % (side, b_edges, nm, vol))
    if b_edges or nm or vol <= 0:
        sys.exit("LID CUTTER %s IS NOT A VALID SOLID -- a boolean against it makes geometry, "
                 "not a socket" % side)

    md = head.modifiers.new("EYE_APERTURE_%s" % side, "BOOLEAN")
    md.operation = "DIFFERENCE"; md.object = cutter; md.solver = "EXACT"
    md.material_mode = "TRANSFER"
    bpy.context.view_layer.objects.active = head
    bpy.ops.object.modifier_apply(modifier=md.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

    f = np.load(os.path.join(DONOR, "eye_%s.npz" % side))
    verts, tris, cls = f["vertices"], f["triangles"], f["vertex_class"]
    eme = bpy.data.meshes.new("MARS_EYE_%s_MESH" % side)
    eme.from_pydata([tuple(map(float, v)) for v in verts], [],
                    [tuple(map(int, t)) for t in tris])
    eme.validate(verbose=False)
    slot_of = {}
    for c in sorted(set(int(x) for x in cls)):
        slot_of[c] = len(eme.materials); eme.materials.append(CLASS_MAT[c])
    for poly in eme.polygons:
        vs = [int(cls[i]) for i in poly.vertices]
        poly.material_index = slot_of[max(set(vs), key=vs.count)]
        poly.use_smooth = True
    ball = bpy.data.objects.new("MARS_EYE_%s" % side, eme)
    scene.collection.objects.link(ball)
    ball.rotation_mode = "XYZ"

    # THE GEOMETRY MUST BE THE SIZE THE DONOR SAYS IT IS.
    # MARS_ORAL.blend carried eyeballs of 17.3 mm for weeks while the donor npz
    # held 28.9 mm and its manifest agreed with the npz. The ratio was 1.673,
    # which is sqrt(3) -- these were the PRE-FIX globes from before the bbox
    # diagonal bug was corrected. The donor was fixed; this blend, which is
    # written in place and was never in the pipeline script, was not rebuilt.
    # Every eye measurement taken since was taken on the old geometry.
    # So: compare what landed against what the donor recorded, every run.
    _w = [ball.matrix_world @ v.co for v in eme.vertices]
    _ext = max(max(p[i] for p in _w) - min(p[i] for p in _w) for i in range(3))
    _claim = EM["eyes"]["eye_%s" % side]["eyeballDiameter"]
    if abs(_ext - _claim) > _claim * 0.02:
        sys.exit("EYE %s IS NOT THE SIZE THE DONOR RECORDED: %.4f in the blend vs %.4f in "
                 "assets/donor/gnm_eyes/manifest.json (ratio %.3f). A donor and the mesh "
                 "built from it disagreeing means one of them is stale -- re-run "
                 "gnm_eye_donor.py." % (side, _ext, _claim, _claim / max(_ext, 1e-9)))
    report["eye_%s" % side] = {"eyeballVerts": len(verts), "cutterVolume": round(vol, 8),
                               "variant": VARIANT, "eyeParts": PARTS,
                               "eyeballDiameter": round(_ext, 5),
                               "diameterMM": round(_ext / (MW_ANCHOR / 50.0), 1),
                               "fissureWidth": round(EM["eyes"]["eye_%s" % side]["fissureWidth"], 5),
                               "globeOverFissure": round(
                                   _ext / EM["eyes"]["eye_%s" % side]["fissureWidth"], 3)}

print("\nexterior %d -> %d verts (the lid apertures)" % (before_n, len(head.data.vertices)))

# Does a ray fired at each eye now land on an EYEBALL rather than on skin?
deps = bpy.context.evaluated_depsgraph_get()
for side in ("L", "R"):
    up = [V(p) for p in C["eye_%s_upper" % side]]
    lo = [V(p) for p in C["eye_%s_lower" % side]]
    centre = (sum(up, V((0, 0, 0))) + sum(lo, V((0, 0, 0)))) / (len(up) + len(lo))
    hits = {"eyeball": 0, "skin": 0, "miss": 0}
    for i in range(25):
        t = (i / 24.0 - 0.5)
        o = centre + V((0, -0.5, 0)) + (up[len(up) // 2] - lo[len(lo) // 2]) * t * 0.55
        hit, loc_, nor, idx, ob, mw = scene.ray_cast(deps, o, V((0, 1, 0)))
        k = "miss" if not hit else ("eyeball" if ob.name.startswith("MARS_EYE_") else "skin")
        hits[k] += 1
    report["eye_%s" % side]["rays"] = hits
    print("eye %s: %d/25 rays land on the EYEBALL (skin %d, miss %d)"
          % (side, hits["eyeball"], hits["skin"], hits["miss"]))
    if hits["eyeball"] < 8:
        sys.exit("EYE %s IS STILL BEHIND SKIN — the aperture did not open" % side)

    # DOES THE GLOBE FILL THE APERTURE? The line of rays above only asks whether
    # the eye is behind skin, and a globe at 60% of the fissure width passes it
    # comfortably -- the central rays still land on the ball while the socket
    # gapes at both ends. That is the render the owner described: a small low
    # eye with a dark crescent above it. Sweep the WHOLE aperture instead and
    # count what is behind it: anything that is neither eyeball nor skin is a
    # hole in his face.
    ax = (up[-1] - up[0]); fis = ax.length; ax = ax.normalized()
    upv = (up[len(up) // 2] - lo[len(lo) // 2]); opening = upv.length; upv = upv.normalized()
    grid = {"eyeball": 0, "skin": 0, "socket": 0, "nothing": 0}
    bad = []
    for i in range(25):
        for j in range(13):
            fu, fw = (i / 24.0 - 0.5) * 2.0, (j / 12.0 - 0.5) * 2.0
            o = (centre + ax * (fu * fis * 0.48)
                        + upv * (fw * opening * 0.48) + V((0, -0.5, 0)))
            hit, loc_, nor, idx, ob, mw = scene.ray_cast(deps, o, V((0, 1, 0)))
            if not hit:
                grid["nothing"] += 1
                bad.append((round(fu, 2), round(fw, 2)))
            elif ob.name.startswith("MARS_EYE_"):
                grid["eyeball"] += 1
            else:
                try:
                    mi = ob.data.polygons[idx].material_index
                    mn = ob.data.materials[mi].name if 0 <= mi < len(ob.data.materials) else ""
                except Exception:
                    mn = ""
                k = "socket" if "SOCKET" in mn or "ORAL" in mn else "skin"
                grid[k] += 1
                if k == "socket": bad.append((round(fu, 2), round(fw, 2)))
    tot = sum(grid.values())
    backed = 100.0 * grid["eyeball"] / tot
    report["eye_%s" % side]["apertureFill"] = {k: v for k, v in grid.items()}
    report["eye_%s" % side]["apertureBackedByGlobePercent"] = round(backed, 1)
    print("       aperture sweep: eyeball %.0f%% · skin %.0f%% · SOCKET %.0f%% · nothing %.0f%%"
          % (backed, 100.0 * grid["skin"] / tot,
             100.0 * grid["socket"] / tot, 100.0 * grid["nothing"] / tot))
    if bad:
        # WHERE the hole is decides the fix. A ring of socket at the canthi is a
        # globe too narrow for the cut; a band along the top or bottom is a cut
        # taller than the globe; a blob in the middle is a globe seated too deep.
        bu = [b[0] for b in bad]; bw = [b[1] for b in bad]
        print("       hole at: along-fissure %+.2f..%+.2f of half-width · "
              "vertical %+.2f..%+.2f of half-opening · |u|>0.7 in %d of %d"
              % (min(bu), max(bu), min(bw), max(bw),
                 sum(1 for u in bu if abs(u) > 0.7), len(bu)))
    if grid["socket"] + grid["nothing"] > tot * 0.02 and not PROBE:
        sys.exit("EYE %s HAS A HOLE IN IT: %.0f%% of the aperture shows socket or open space "
                 "rather than eyeball or lid. The globe does not fill the cut."
                 % (side, 100.0 * (grid["socket"] + grid["nothing"]) / tot))

bpy.ops.wm.save_as_mainfile(filepath=OUT)
json.dump(report, open("renders/_rig_measure/eye_sockets.json", "w"), indent=2)
print("\neye sockets + eyeballs -> %s" % OUT)
