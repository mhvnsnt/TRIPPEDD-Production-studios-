# The midline strip that splits his tongue reads as CAVITY / SOCK material at
# +0.5 to +2.4 mm while his tongue front is at +43 mm. So something is hanging
# 40 mm in front of the tongue down the middle of his mouth.
# Find those FACES on the evaluated meshes and state what they are.
import bpy, math, os, sys, json, mathutils
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]
arm  = bpy.data.objects["MARS_RIG"]
kb   = head.data.shape_keys.key_blocks
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]
for k in kb:
    if k.name != "Basis": k.value = 0.0
for b in arm.pose.bones:
    b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * 31.0), 0, 0)
for n, (rx, ry, rz) in {"tongue_root": (-14,0,0), "tongue_mid": (-8,0,0)}.items():
    arm.pose.bones[n].rotation_euler = tuple(math.radians(a) for a in (rx, ry, rz))
for n, v in {"lip_lower_depress":0.7,"lip_upper_raise":0.45,
             "lip_corner_L_up":0.2,"lip_corner_R_up":0.2}.items():
    if n in kb: kb[n].value = v
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get(); deps.update()

# the aperture box, in his own millimetres, from the measured mouth frame
HALF_X, ZTOP, ZBOT = 26.0, 22.0, -26.0

def scan(objname):
    ob = bpy.data.objects[objname]
    ev = ob.evaluated_get(deps); me = ev.to_mesh()
    M = ev.matrix_world
    out = {}
    for p in me.polygons:
        c = F.local(M @ p.center)
        x, y, z = mm(c.x - F.cx), mm(c.y), mm(c.z)
        if abs(x) > HALF_X or not (ZBOT < z < ZTOP):   # inside the aperture only
            continue
        mi = p.material_index
        mat = (me.materials[mi].name if 0 <= mi < len(me.materials) else "?").split(".")[0]
        r = out.setdefault(mat, [])
        r.append((x, y, z, p.index, p.area))
    ev.to_mesh_clear()
    return out

print("%-18s %-18s %6s  %s" % ("OBJECT", "MATERIAL", "faces", "y front..back mm"))
store = {}
for name in ("MARS_MESH", "MARS_MOUTH_SOCK", "MARS_TONGUE", "MARS_TEETH_UPPER", "MARS_TEETH_LOWER"):
    for mat, rows in scan(name).items():
        ys = [r[1] for r in rows]
        print("%-18s %-18s %6d  %8.2f .. %8.2f" % (name, mat, len(rows), min(ys), max(ys)))
        store[(name, mat)] = rows

# THE MIDLINE. His tongue's own front face, and what sits in front of it there.
print()
print("MIDLINE COLUMN  |x| < 7 mm, z -26..+22 -- what lives in front of his tongue")
tongue = [r for r in store.get(("MARS_TONGUE","MARS_TONGUE_MAT"), []) if abs(r[0]) < 7]
tf = min((r[1] for r in tongue), default=None)
print("  tongue front-most face in the midline column: %.2f mm (%d faces)" % (tf, len(tongue)))
for (name, mat), rows in sorted(store.items()):
    if name == "MARS_TONGUE": continue
    fwd = [r for r in rows if abs(r[0]) < 7 and r[1] < tf]
    if not fwd: continue
    ys = [r[1] for r in fwd]; zs = [r[2] for r in fwd]
    print("  %-18s %-18s %5d faces IN FRONT of the tongue  y %.2f..%.2f  z %.1f..%.1f  area %.2f mm2"
          % (name, mat, len(fwd), min(ys), max(ys), min(zs), max(zs),
             sum(r[4] for r in fwd) / MW / MW * 2500.0))
