"""
ONE COMMAND, ONE BLENDER LAUNCH, THE WHOLE TRUTH ABOUT HIS MOUTH.

    "we need a more efficient pipeline, bro. You're wasting my sessions."
                                                        -- the owner, 2026-09-13

He is right, and this is the receipt: answering "what does his mouth actually
look like, and what is it made of" cost TEN separate Blender launches -- render
before, render after, false-colour before, false-colour after, a control with the
skin hidden, a ray fan, a straddle count, a sequence each way. Each launch is a
minute of his session and a turn of mine, and every one of them was the same
scene loaded from scratch.

This does all of it in one process, for as many rigs as you name:

  * renders the pose ladder in BEAUTY (what he sees)
  * renders the same poses FALSE-COLOURED BY MATERIAL, so his face texture, the
    cavity, teeth, gums, tongue and sock are each a known colour
  * counts the pixels of each and prints the table
  * renders the mouth opening as a SEQUENCE, because a mouth opening is motion
  * writes machine-readable JSON and publishes the frames as evidence

WHY FALSE-COLOUR BY MATERIAL AND NOT BY OBJECT: the cavity walls ARE MARS_MESH.
Colouring by object cannot tell his face from the inside of his mouth, and that
is exactly the distinction the whole question turns on.

WHY THE VIEW TRANSFORM IS FORCED TO STANDARD FOR THE ID PASS: AgX or Filmic
re-map an emission colour, so the pixels no longer equal the colour that was
assigned and every count is wrong by an amount nobody can see. Standard, look
None, exposure 0, gamma 1 -- then a pixel IS its material.

AND IT NEVER TRUSTS hide_render. MARS_MOUTH_SOCK, MARS_TEETH_* and MARS_TONGUE
shipped with hide_render = True, and scene.ray_cast IGNORES that flag -- which is
how a survey reported "sock 9.9%, teeth 2.2%" of a frame containing zero pixels
of either. Visibility is reported per object, per rig, in the JSON.

  vendor/blender/blender -b -P tools/character/mouth_truth.py -- \
      --rig assets/rigs/MARS_FACE.blend \
      --compare BEFORE=/path/old.blend \
      --out renders/_mouth_truth --seq --publish
"""
import bpy, sys, os, json, math
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d=None): return argv[argv.index(f) + 1] if f in argv else d
def opts(f): return [argv[i + 1] for i, a in enumerate(argv) if a == f]
def flag(f): return f in argv
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("mouth_truth.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))

OUT  = os.path.abspath(opt("--out", os.path.join(ROOT, "renders/_mouth_truth")))
RES  = int(opt("--res", "900"))
SEQN = int(opt("--seq-frames", "18"))
os.makedirs(OUT, exist_ok=True)

MA = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = float(MA["aperture"]["width"]); MM = MW / 50.0
FRAME = Matrix(MA["frame"]["matrix"]); FINV = FRAME.inverted()
AP = (Vector(MA["aperture"]["cornerLeft"]) + Vector(MA["aperture"]["cornerRight"])) / 2.0
# OUT OF HIS FACE, CHECKED AGAINST HIS TEETH -- every "FRONT" camera in this
# project was once behind his head. Local +y is the direction the aperture gets
# deeper, and his teeth sit deeper than his lips, so out-of-the-face is -y.
OUTW = (FRAME.to_3x3() @ Vector((0.0, -1.0, 0.0))).normalized()
UPW  = (FRAME.to_3x3() @ Vector((0.0,  0.0, 1.0))).normalized()

# name -> the colour it renders as in the ID pass. Anything unlisted is HIS SKIN.
IDCOL = {
    "MARS_ORAL_MAT":   (1.00, 0.45, 0.00),   # the cavity carved out of his head
    "MARS_TEETH_MAT":  (1.00, 1.00, 1.00),
    "MARS_GUM_MAT":    (1.00, 0.85, 0.00),
    "MARS_TONGUE_MAT": (1.00, 0.05, 0.25),
    "MARS_SOCK_MAT":   (0.55, 0.00, 1.00),
}
SKIN = (0.10, 0.35, 0.55)
LABEL = {SKIN: "his_skin", IDCOL["MARS_ORAL_MAT"]: "cavity",
         IDCOL["MARS_TEETH_MAT"]: "teeth", IDCOL["MARS_GUM_MAT"]: "gums",
         IDCOL["MARS_TONGUE_MAT"]: "tongue", IDCOL["MARS_SOCK_MAT"]: "sock"}
ORAL = ("cavity", "teeth", "gums", "tongue", "sock")

POSES = [
    ("rest",   0.0, {}),
    ("jaw18", 18.0, {}),
    ("open",  30.0, {"lip_lower_depress": 1.0, "lip_upper_raise": 1.0,
                     "mouth_funnel": 1.0}),
]

def load(path):
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(path))
    me = bpy.data.objects.get("MARS_MESH")
    arm = bpy.data.objects.get("MARS_RIG")
    if me is None or arm is None: die("%s has no MARS_MESH / MARS_RIG" % path)
    return me, arm

def show_oral():
    """hide_render is a RENDER flag and ray_cast ignores it. Report, then clear."""
    was = {}
    for nm in ("MARS_MOUTH_SOCK", "MARS_TEETH_UPPER", "MARS_TEETH_LOWER", "MARS_TONGUE"):
        o = bpy.data.objects.get(nm)
        if o is None: was[nm] = "ABSENT"; continue
        was[nm] = bool(o.hide_render)
        o.hide_render = False
    return was

def build_camera(scene, ortho=2.6):
    cd = bpy.data.cameras.new("MOUTHCAM")
    cam = bpy.data.objects.new("MOUTHCAM", cd); scene.collection.objects.link(cam)
    cd.type = "ORTHO"; cd.ortho_scale = MW * ortho
    cam.location = AP + OUTW * 0.9
    z = OUTW; x = UPW.cross(z).normalized(); y = z.cross(x)
    cam.matrix_world = Matrix(((x.x, y.x, z.x, cam.location.x),
                              (x.y, y.y, z.y, cam.location.y),
                              (x.z, y.z, z.z, cam.location.z), (0, 0, 0, 1)))
    scene.camera = cam
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = scene.render.resolution_y = RES
    scene.render.image_settings.file_format = "PNG"
    if scene.world is None: scene.world = bpy.data.worlds.new("W")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.06, 1)
    ld = bpy.data.lights.new("KEY", "AREA"); ld.energy = 120; ld.size = 0.6
    lo = bpy.data.objects.new("KEY", ld); scene.collection.objects.link(lo)
    lo.location = AP + OUTW * 0.55 + UPW * 0.12
    lo.rotation_euler = cam.rotation_euler
    return cam

def emission(col, name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs[0].default_value = (col[0], col[1], col[2], 1.0)
    e.inputs[1].default_value = 1.0
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0])
    return m

def to_id_materials():
    for ob in bpy.data.objects:
        if ob.type != "MESH": continue
        if not ob.data.materials: ob.data.materials.append(bpy.data.materials.new("bare"))
        for i, m in enumerate(ob.data.materials):
            col = IDCOL.get(m.name if m else "", SKIN)
            ob.data.materials[i] = emission(col, "ID_%s_%d" % (ob.name, i))

def standard_view(scene):
    # AgX / Filmic re-map an emission colour, so a pixel would no longer BE its
    # material and every count would be wrong by an amount nobody can see.
    vs = scene.view_settings
    try: vs.view_transform = "Standard"
    except TypeError: pass
    try: vs.look = "None"
    except TypeError: pass
    vs.exposure = 0.0; vs.gamma = 1.0

def pose(me, arm, jaw, keys):
    for k in me.data.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
    for nm, v in keys.items():
        kb = me.data.shape_keys.key_blocks.get(nm)
        if kb: kb.value = v
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
    pb.rotation_euler = (math.radians(jaw), 0, 0)
    bpy.context.view_layer.update()

def render_to(scene, path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)

def count(path):
    """Classify every pixel by which material's colour it is nearest."""
    img = bpy.data.images.load(path)
    px = list(img.pixels)
    n = len(px) // 4
    refs = [SKIN] + list(IDCOL.values())
    tally = {LABEL[r]: 0 for r in refs}; tally["background"] = 0
    for i in range(n):
        r, g, b = px[4 * i], px[4 * i + 1], px[4 * i + 2]
        if r + g + b < 0.02: tally["background"] += 1; continue
        best, bd = None, 1e9
        for ref in refs:
            d = (r - ref[0]) ** 2 + (g - ref[1]) ** 2 + (b - ref[2]) ** 2
            if d < bd: bd, best = d, ref
        tally[LABEL[best]] += 1
    bpy.data.images.remove(img)
    return {k: 100.0 * v / n for k, v in tally.items()}, n

def run(tag, path):
    me, arm = load(path)
    vis = show_oral()
    scene = bpy.context.scene
    build_camera(scene)
    res = {"rig": path, "hideRenderWas": vis, "poses": {}}
    for nm, jaw, keys in POSES:
        missing = [k for k in keys if me.data.shape_keys.key_blocks.get(k) is None]
        if missing:
            print("  %s: rig has no %s -- pose skipped" % (nm, missing), flush=True)
            continue
        pose(me, arm, jaw, keys)
        b = os.path.join(OUT, "%s_%s_beauty.png" % (tag, nm))
        render_to(scene, b)
        res["poses"][nm] = {"beauty": os.path.basename(b)}
    to_id_materials(); standard_view(scene)
    for nm, jaw, keys in POSES:
        if nm not in res["poses"]: continue
        pose(me, arm, jaw, keys)
        p = os.path.join(OUT, "%s_%s_id.png" % (tag, nm))
        render_to(scene, p)
        share, npx = count(p)
        share["ORAL_TOTAL"] = sum(share[k] for k in ORAL)
        res["poses"][nm].update({"id": os.path.basename(p), "pixelShare": share,
                                 "pixels": npx})
    if flag("--seq"):
        pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
        for i in range(SEQN):
            t = 0.5 - 0.5 * math.cos(2 * math.pi * i / SEQN)
            pose(me, arm, 30.0 * t,
                 {k: t for k in ("lip_lower_depress", "lip_upper_raise", "mouth_funnel")})
            render_to(scene, os.path.join(OUT, "%s_seq_%02d.png" % (tag, i)))
        res["sequenceFrames"] = SEQN
    return res

rigs = [("AFTER", opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))]
for c in opts("--compare"):
    t, _, p = c.partition("=")
    rigs.append((t or "BEFORE", p))

report = {"schema": "trippedd.mouth-truth/v1", "mouthWidth": MW,
          "outOfFace": list(OUTW), "rigs": {}}
for tag, path in rigs:
    print("\n=== %s  %s ===" % (tag, path), flush=True)
    report["rigs"][tag] = run(tag, path)

cols = ["his_skin"] + list(ORAL) + ["ORAL_TOTAL", "background"]
print("\n%-22s%s" % ("", "".join("%11s" % c for c in cols)), flush=True)
for tag in report["rigs"]:
    for nm, d in report["rigs"][tag]["poses"].items():
        sh = d.get("pixelShare")
        if not sh: continue
        print("%-22s%s" % ("%s %s" % (tag, nm),
              "".join("%10.2f%%" % sh[c] for c in cols)), flush=True)
for tag, r in report["rigs"].items():
    hid = [k for k, v in r["hideRenderWas"].items() if v is True]
    if hid:
        print("\n%s: hide_render was TRUE on %s -- cleared for this measurement. "
              "ray_cast would NOT have seen that." % (tag, ", ".join(hid)), flush=True)

jp = os.path.join(OUT, "mouth_truth.json")
json.dump(report, open(jp, "w"), indent=2)
print("\nreport -> %s" % jp, flush=True)
