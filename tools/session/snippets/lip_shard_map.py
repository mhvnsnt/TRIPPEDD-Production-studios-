# OWNER: "Use that thing that turns everything into colors so you can see where
# they're at and where to shave them ... it's still hanging down too far in front
# of the teeth on the top lip and parts shooting up in front of the teeth on the
# bottom lip."
# So colour the OFFENDERS THEMSELVES, not just the tissue types:
#   ORANGE = upper-lip skin standing in front of a tooth
#   YELLOW = lower-lip skin standing in front of a tooth
#   RED    = his skin, innocent
# Fired FROM each crown OUTWARD, so it is occlusion as the camera sees it.
import bpy, math, os, sys, json, mathutils
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
me = head.data; kb = me.shape_keys.key_blocks
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]
anat = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
UPc = np.array(anat["contours"]["lip_inner_upper"], float)
LOc = np.array(anat["contours"]["lip_inner_lower"], float)

WIDE = {"lip_lower_depress":0.7,"lip_upper_raise":0.45,"lip_corner_L_up":0.2,"lip_corner_R_up":0.2}
for k in kb:
    if k.name != "Basis": k.value = 0.0
for b in arm.pose.bones:
    b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * 31.0), 0, 0)
for n_, v in WIDE.items():
    if n_ in kb: kb[n_].value = v
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get(); dg.update()

def seam_z(x):
    u = np.array([list(F.local(V(p))) for p in UPc]); l = np.array([list(F.local(V(p))) for p in LOc])
    u = u[np.argsort(u[:,0])]; l = l[np.argsort(l[:,0])]
    return 0.5*(np.interp(x, u[:,0], u[:,2]) + np.interp(x, l[:,0], l[:,2]))

OUTW = (F.world(V((F.cx, -1.0, 0.0))) - F.world(V((F.cx, 0.0, 0.0)))).normalized()
blockers = {}
for part in ("MARS_TEETH_UPPER", "MARS_TEETH_LOWER"):
    t = bpy.data.objects[part].evaluated_get(dg); tm = t.to_mesh(); Mt = t.matrix_world
    for p in tm.polygons:
        mi = p.material_index
        if (tm.materials[mi].name if 0 <= mi < len(tm.materials) else "").split(".")[0] != "MARS_TEETH_MAT":
            continue
        o = (Mt @ p.center) + OUTW * (0.2 * MW)
        hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(dg, o, OUTW)
        if hit and ob.name == "MARS_MESH":
            m = (me.materials[me.polygons[idx].material_index].name
                 if idx < len(me.polygons) else "").split(".")[0]
            if m.startswith("tripo"):
                blockers[int(idx)] = blockers.get(int(idx), 0) + 1
    t.to_mesh_clear()

up, lo = [], []
for fi in blockers:
    c = F.local(head.matrix_world @ me.polygons[fi].center)
    up.append(fi) if c.z > seam_z(c.x) else lo.append(fi)
print("skin faces standing in front of a tooth: %d  (%d rays)" % (len(blockers), sum(blockers.values())))
print("  on the UPPER lip, hanging DOWN over the teeth : %d faces, %d rays"
      % (len(up), sum(blockers[i] for i in up)))
print("  on the LOWER lip, shooting UP over the teeth  : %d faces, %d rays"
      % (len(lo), sum(blockers[i] for i in lo)))
zs=[mm(F.local(head.matrix_world @ me.polygons[i].center).z) for i in up] or [0]
print("  upper offenders z %.1f..%.1f mm" % (min(zs), max(zs)))
zs=[mm(F.local(head.matrix_world @ me.polygons[i].center).z) for i in lo] or [0]
print("  lower offenders z %.1f..%.1f mm" % (min(zs), max(zs)))

MARKS = {"_MARK_UPPER": (1.0, 0.35, 0.0), "_MARK_LOWER": (1.0, 0.95, 0.0)}
base = len(me.materials)
for nm, col in MARKS.items():
    m = bpy.data.materials.get(nm) or bpy.data.materials.new(nm)
    m.use_nodes = True
    me.materials.append(m)
for fi in up: me.polygons[fi].material_index = base
for fi in lo: me.polygons[fi].material_index = base + 1

COLOURS = {
    "tripo_mat_63779a1f-eb9a-4b4a-a12c-e90b88a426b1": (1.0, 0.0, 0.0),
    "MARS_ORAL_MAT": (0.10,0.10,0.14), "MARS_SOCK_MAT": (0.0,0.55,1.0),
    "MARS_TEETH_MAT": (1,1,1), "MARS_GUM_MAT": (1.0,0.55,0.75),
    "MARS_TONGUE_MAT": (0.2,1.0,0.3),
    "_MARK_UPPER": MARKS["_MARK_UPPER"], "_MARK_LOWER": MARKS["_MARK_LOWER"],
}
for m in bpy.data.materials:
    b = m.name.split(".")[0]
    if b not in COLOURS: continue
    m.use_nodes = True; nt = m.node_tree
    out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if out is None: continue
    for l in list(out.inputs["Surface"].links): nt.links.remove(l)
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = tuple(COLOURS[b]) + (1.0,)
    nt.links.new(e.outputs[0], out.inputs["Surface"])

sc = bpy.context.scene
sc.view_settings.view_transform="Standard"; sc.view_settings.look="None"
sc.view_settings.exposure=0.0; sc.view_settings.gamma=1.0
sc.render.engine="BLENDER_EEVEE_NEXT"
try: sc.eevee.taa_render_samples = 16
except Exception: pass
sc.render.resolution_x = sc.render.resolution_y = 900
if sc.world is None: sc.world = bpy.data.worlds.new("W")
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value=(0.02,0.02,0.03,1)
mouth_w = F.world(V((F.cx, 0.0, 0.0)))
cd = bpy.data.cameras.new("_IDCAM"); cd.lens = 65
cam = bpy.data.objects.new("_IDCAM", cd); sc.collection.objects.link(cam)
cam.location = V(mouth_w) + V((0.02, -0.62, 0.06))
cam.rotation_euler = (V(mouth_w) - cam.location).to_track_quat("-Z","Y").to_euler()
sc.camera = cam
sc.render.filepath = os.path.abspath("renders/_tongue/LIP_SHARDS.png")
sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
print("wrote renders/_tongue/LIP_SHARDS.png")
