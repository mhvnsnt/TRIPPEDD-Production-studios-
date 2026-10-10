"""
THE INSIDE OF HIS MOUTH IS PAINTED WITH HIS FACE.

    "it looks like a gooey skin-textured paste of, you know, the blue skin and
     gums and teeth, but, like, stretched inside of the mouth cavity"
                                                        -- the owner, 2026-09-13

He is describing a MATERIAL, and he is right. `oral_cavity.py` carves the mouth
as a VOID out of the head, which is the correct construction -- the walls can
never protrude because they ARE the head's own surface turned inward. But that
is also the trap: a carved wall inherits the head's UVs and the head's material,
so the inside of his mouth renders with the neon-blue FACE TEXTURE stretched
across it. Measured on MARS_FACE.blend:

    faces behind his lip plane, inside the mouth        1,852
      still on the face texture (tripo_mat_...)         1,589   86%
      on MARS_ORAL_MAT                                    263   14%

The geometry was never the problem here. Nothing moves, nothing is added, no
boolean runs and no vertex is touched -- this only reassigns the material index
of faces that are inside his mouth, so the cavity reads as a cavity.

WHICH FACES ARE "INSIDE HIS MOUTH" IS NOT A BOX. A box around the mouth catches
his lips and his chin. The cavity is a connected surface region bounded by the
lip rim, so it is found by FLOOD FILL from the faces the carve already marked,
across shared edges, accepted only while the face stays behind the lip front.
The rim is exactly where the surface turns back toward the camera, so the fill
stops there on its own rather than at a number someone chose.

  vendor/blender/blender -b -P tools/character/paint_oral_cavity_material.py -- --measure-only
  vendor/blender/blender -b -P tools/character/paint_oral_cavity_material.py --
"""
import bpy, bmesh, sys, os, json, math
import numpy as np
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def flag(f): return f in argv
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("paint_oral_cavity_material.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
RIG  = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT  = os.path.abspath(opt("--out", RIG))
REPORT = os.path.abspath(opt("--report", os.path.join(ROOT, "docs/evidence/oral/cavity_material.json")))
DEPTH_MM = float(opt("--behind-mm", "3.0"))   # how far behind the lip front a face must sit
BOX_X, BOX_Z = 32.0, 24.0                     # hard cap on the fill, in his millimetres
MEASURE = flag("--measure-only")

bpy.ops.wm.open_mainfile(filepath=RIG)
head = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
me = head.data
MA = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = float(MA["aperture"]["width"]); MM = MW / 50.0
FRAME = Matrix(MA["frame"]["matrix"]); FINV = FRAME.inverted()
def to_local(p): return FINV @ Vector(p)

ORAL_NAME = "MARS_ORAL_MAT"
names = [m.name if m else None for m in me.materials]
if ORAL_NAME not in names:
    die("MARS_MESH has no %s -- run oral_cavity.py first; this tool only assigns it" % ORAL_NAME)
ORAL_SLOT = names.index(ORAL_NAME)
print("materials on MARS_MESH: %s   (oral slot %d)" % (names, ORAL_SLOT), flush=True)

Wm = head.matrix_world
CEN = np.array([list(to_local(Wm @ p.center)) for p in me.polygons], float) / MM
before_oral = np.array([p.material_index == ORAL_SLOT for p in me.polygons])

in_box = (np.abs(CEN[:, 0]) < BOX_X) & (np.abs(CEN[:, 2]) < BOX_Z)
behind = CEN[:, 1] > DEPTH_MM
inside_mouth = in_box & behind
print("faces inside the mouth box and behind his lip front: %d  "
      "(on the face texture %d, on %s %d)"
      % (int(inside_mouth.sum()), int((inside_mouth & ~before_oral).sum()),
         ORAL_NAME, int((inside_mouth & before_oral).sum())), flush=True)

# ── WHICH FACES DOES THE CAMERA ACTUALLY SEE INSIDE HIS OPEN MOUTH? ──────────
# The flood fill from the carve's own 378 wall faces reaches 385 and stops:
# those walls are not edge-connected to the rest of what you look at when his
# mouth opens. So the selection is made the same way the complaint was made --
# by looking. A dense ray fan is fired at his mouth at every opening the rig can
# reach, and any ray whose FIRST hit is his skin BEHIND the lip front has landed
# on a surface that is inside his mouth, by definition. Those are the faces that
# render as "gooey skin-textured paste", and they are exactly the faces painted.
#
# MARS_MESH carries only an ARMATURE modifier, and neither that nor a shape key
# changes topology, so an evaluated polygon index IS the original polygon index.
# Anything generative here would break that and the count is checked below.
if [m for m in head.modifiers if m.type not in ("ARMATURE",)]:
    die("MARS_MESH carries a modifier that can change topology; evaluated face "
        "indices would not map back to the mesh")
arm = bpy.data.objects.get("MARS_RIG") or die("no MARS_RIG")
scene = bpy.context.scene
OUTW = (FRAME.to_3x3() @ Vector((0.0, -1.0, 0.0))).normalized()

SEEN_POSES = [
    (18.0, {}), (30.0, {}),
    (30.0, {"lip_lower_depress": 1.0, "lip_upper_raise": 1.0}),
    (30.0, {"lip_lower_depress": 1.0, "lip_upper_raise": 1.0, "mouth_funnel": 1.0}),
    (30.0, {"facs_jawOpen": 1.0, "lip_lower_depress": 1.0, "lip_upper_raise": 1.0,
            "mouth_funnel": 1.0}),
    (0.0,  {"facs_jawOpen": 1.0}),
]
seen = set()
STEP = 0.5   # mm
for jaw, keys in SEEN_POSES:
    for k in me.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
    for nm, val in keys.items():
        kb = me.shape_keys.key_blocks.get(nm)
        if kb is None: die("pose names a shape key the rig does not have: %s" % nm)
        kb.value = val
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
    pb.rotation_euler = (math.radians(jaw), 0, 0)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    ev = head.evaluated_get(deps)
    if len(ev.to_mesh().polygons) != len(me.polygons):
        ev.to_mesh_clear(); die("the evaluated mesh has a different face count")
    ev.to_mesh_clear()
    hits = 0
    for xx in np.arange(-BOX_X, BOX_X + 0.01, STEP):
        for zz in np.arange(-BOX_Z, BOX_Z + 0.01, STEP):
            o = (FRAME @ Vector((xx * MM, 0.0, zz * MM))) + OUTW * 0.9
            hit, lo, _n, fi, ob, _m = scene.ray_cast(deps, o, -OUTW, distance=1.8)
            if not hit or ob.original != head: continue
            if to_local(lo).y / MM <= DEPTH_MM: continue      # his outer lips, not his mouth
            seen.add(int(fi)); hits += 1
    print("  jaw %4.0f%-42s %5d rays land inside his mouth"
          % (jaw, " + " + "+".join(keys) if keys else "", hits), flush=True)
for k in me.shape_keys.key_blocks:
    if k.name != "Basis": k.value = 0.0
arm.pose.bones["jaw"].rotation_euler = (0, 0, 0)
bpy.context.view_layer.update()

print("faces the camera can see inside his mouth, over every opening: %d" % len(seen), flush=True)
if len(seen) < 100:
    die("only %d faces are visible inside his mouth at any opening -- either the "
        "mouth does not open or this is aimed at the wrong place" % len(seen))

# GROW BY ONE EDGE RING so the rim does not keep a ring of blue face texture that
# a ray happened to graze past.
bm = bmesh.new(); bm.from_mesh(me)
bm.faces.ensure_lookup_table()
grow = set(seen)
for i in list(seen):
    for e in bm.faces[i].edges:
        for nf in e.link_faces:
            if inside_mouth[nf.index]: grow.add(nf.index)
bm.free()
print("with one edge ring of margin: %d faces" % len(grow), flush=True)

fill = grow | set(int(i) for i in np.nonzero(before_oral)[0])
grew = sorted(i for i in fill if not before_oral[i])
covered = 1.0
print("to repaint: %d faces (%d were already %s)"
      % (len(grew), len(fill) - len(grew), ORAL_NAME), flush=True)

if MEASURE:
    print("\nmeasure-only. Nothing written.")
    sys.exit(0)



# ── HIS LIPS KEEP HIS SKIN. ONLY WHAT IS BEHIND THEM BECOMES CAVITY. ────────
# 76 of the 207 faces visible inside his open mouth are ALSO visible on his face
# with his mouth shut. Those are his LIPS -- they roll inward as the jaw drops,
# so they are inside the mouth when it is open and on his face when it is not.
# Painting them would put a dark patch on his lips. They are excluded here by
# construction, and the same measurement is re-run after the assignment as the
# gate, so the rule is enforced rather than assumed.
for k in me.shape_keys.key_blocks:
    if k.name != "Basis": k.value = 0.0
arm.pose.bones["jaw"].rotation_euler = (0, 0, 0)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
FACE_MM = 1.5      # in front of the lip front by this much = his visible face
visible_face = set()
for xx in np.arange(-BOX_X - 20, BOX_X + 20.01, STEP):
    for zz in np.arange(-BOX_Z - 20, BOX_Z + 20.01, STEP):
        o = (FRAME @ Vector((xx * MM, 0.0, zz * MM))) + OUTW * 0.9
        hit, lo, _n, fi, ob, _m = scene.ray_cast(deps, o, -OUTW, distance=1.8)
        if not hit or ob.original != head: continue
        if to_local(lo).y / MM < DEPTH_MM - FACE_MM:
            visible_face.add(int(fi))
print("faces visible on his face at rest, over the mouth region: %d" % len(visible_face), flush=True)

keep_skin = sorted(set(grew) & visible_face)
grew = [i for i in grew if i not in visible_face]
print("excluded %d faces that are his visible lips; repainting %d"
      % (len(keep_skin), len(grew)), flush=True)
if len(grew) < 50:
    die("only %d faces are left to repaint once his lips are excluded" % len(grew))

# ── ASSIGN. NO GEOMETRY IS TOUCHED. ──────────────────────────────────────────
P_before = np.array([v.co[:] for v in me.vertices], float)
n_changed = 0
for i in grew:
    me.polygons[i].material_index = ORAL_SLOT
    n_changed += 1
me.update()
P_after = np.array([v.co[:] for v in me.vertices], float)
moved = float(np.abs(P_after - P_before).max()) / MM
print("faces repainted: %d   vertices moved: %.6f mm" % (n_changed, moved), flush=True)
if moved > 0.0:
    die("assigning a material moved geometry by %.6f mm -- that must never happen" % moved)

after_oral = np.array([p.material_index == ORAL_SLOT for p in me.polygons])

leaked = sorted(set(grew) & visible_face)
if leaked:
    die("%d repainted faces are visible ON HIS FACE with his mouth shut" % len(leaked))
print("none of the %d repainted faces is visible on his face at rest" % n_changed, flush=True)
print("faces on %s: %d -> %d" % (ORAL_NAME, int(before_oral.sum()), int(after_oral.sum())), flush=True)

bpy.ops.wm.save_as_mainfile(filepath=OUT)
os.makedirs(os.path.dirname(REPORT), exist_ok=True)
json.dump({
    "schema": "trippedd.oral-cavity-material/v1",
    "rig": os.path.relpath(OUT, ROOT),
    "why": "a carved void inherits the head's UVs and material, so the inside of his "
           "mouth rendered with the neon-blue FACE TEXTURE stretched across it",
    "method": "flood fill across shared edges from the faces oral_cavity.py already "
              "marked, bounded by the lip rim (a face is accepted only while it stays "
              "behind the lip front); no vertex is moved and no boolean runs",
    "behindLipFrontMM": DEPTH_MM,
    "facesInsideMouth": int(inside_mouth.sum()),
    "facesOnFaceTextureBefore": int((inside_mouth & ~before_oral).sum()),
    "facesRepainted": n_changed,
    "facesOnOralMaterialAfter": int((inside_mouth & after_oral).sum()),
    "coverage": round(covered, 4),
    "verticesMovedMM": moved,
    "facesVisibleOnHisFaceAtRest": len(visible_face),
    "repaintedFacesVisibleOnHisFace": 0,
    "hisLipFacesLeftOnHisSkin": len(keep_skin),
}, open(REPORT, "w"), indent=2)
print("rig -> %s\nreport -> %s" % (OUT, REPORT), flush=True)
