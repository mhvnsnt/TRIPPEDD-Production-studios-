# A FALSE-COLOUR ID PASS AT THE WIDE POSE.
# Every argument so far has been about coordinates. This renders the answer:
# HIS SKIN IS RED. If red appears inside the mouth opening, that is the thing
# he is describing, and its position on screen is not open to interpretation.
# View transform forced to Standard/None/0/1 so a pixel IS its material
# (MEASUREMENT TRUTH IS NOT DISPLAY TRUTH, already banked).
import bpy, json, os, sys, math, mathutils
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW

head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
kb = head.data.shape_keys.key_blocks
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]
for k in kb:
    if k.name != "Basis": k.value = 0.0
for b in arm.pose.bones:
    b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * 31.0), 0, 0)
for n_, r in {"tongue_root": (-14,0,0), "tongue_mid": (-8,0,0)}.items():
    arm.pose.bones[n_].rotation_euler = tuple(math.radians(a) for a in r)
for n_, v in {"lip_lower_depress":0.7,"lip_upper_raise":0.45,
              "lip_corner_L_up":0.2,"lip_corner_R_up":0.2}.items():
    if n_ in kb: kb[n_].value = v
bpy.context.view_layer.update()

COLOURS = {
    "tripo_mat_63779a1f-eb9a-4b4a-a12c-e90b88a426b1": (1.0, 0.0, 0.0),   # HIS SKIN  = RED
    "MARS_ORAL_MAT":   (0.10, 0.10, 0.14),   # carved cavity wall = near black
    "MARS_SOCK_MAT":   (0.00, 0.55, 1.00),   # mouth sock         = blue
    "MARS_TEETH_MAT":  (1.00, 1.00, 1.00),   # teeth              = white
    "MARS_GUM_MAT":    (1.00, 0.55, 0.75),   # gums               = pink
    "MARS_TONGUE_MAT": (0.20, 1.00, 0.30),   # tongue             = green
}
saved = {}
for m in bpy.data.materials:
    base = m.name.split(".")[0]
    if base not in COLOURS: continue
    m.use_nodes = True
    nt = m.node_tree
    out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if out is None: continue
    saved[m.name] = [l.from_node.name for l in out.inputs["Surface"].links]
    for l in list(out.inputs["Surface"].links): nt.links.remove(l)
    e = nt.nodes.new("ShaderNodeEmission")
    e.name = "_IDPASS"; e.inputs[0].default_value = tuple(COLOURS[base]) + (1.0,)
    nt.links.new(e.outputs[0], out.inputs["Surface"])

sc = bpy.context.scene
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"; sc.view_settings.exposure = 0.0; sc.view_settings.gamma = 1.0
sc.render.engine = "BLENDER_EEVEE_NEXT"
try: sc.eevee.taa_render_samples = 16
except Exception: pass
sc.render.resolution_x = sc.render.resolution_y = 900
sc.render.film_transparent = False
if sc.world is None:
    sc.world = bpy.data.worlds.new("W")
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.02, 0.03, 1)

# the SAME mouth camera mouth_proof builds, so this frame overlays that one
mouth_w = F.world(V((F.cx, 0.0, 0.0)))
cd = bpy.data.cameras.new("_IDCAM"); cd.lens = 50
cam = bpy.data.objects.new("_IDCAM", cd)
sc.collection.objects.link(cam)
cam.location = V(mouth_w) + V((0.05, -0.85, 0.10))
d = (V(mouth_w) - cam.location)
cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
sc.camera = cam
out = os.path.abspath("renders/_tongue/ID_WIDE.png")
sc.render.filepath = out
sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
print("wrote", out, os.path.getsize(out), "bytes")

for m in bpy.data.materials:            # put every shader back
    if m.name not in saved: continue
    nt = m.node_tree
    out_n = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    for l in list(out_n.inputs["Surface"].links): nt.links.remove(l)
    if saved[m.name]:
        src = nt.nodes[saved[m.name][0]]
        nt.links.new(src.outputs[0], out_n.inputs["Surface"])
    if "_IDPASS" in nt.nodes: nt.nodes.remove(nt.nodes["_IDPASS"])
bpy.data.objects.remove(cam, do_unlink=True)
print("shaders restored")
