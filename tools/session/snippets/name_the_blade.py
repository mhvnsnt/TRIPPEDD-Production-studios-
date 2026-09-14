# WHAT IS THE THING HANGING DOWN THE MIDDLE OF HIS MOUTH?
# Owner: "Something is sticking so far forward. It's sticking through the front
# teeth. It's sitting on top of the tongue. It's all in the roof and area of the
# mouth that's supposed to be empty."
# Name it by OBJECT and MATERIAL, on a dense grid, at the WIDE pose the render
# was taken at -- never by looking at a picture and guessing.
import bpy, math, os, sys, json, mathutils
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW

head = bpy.data.objects["MARS_MESH"]
arm  = bpy.data.objects["MARS_RIG"]
kb   = head.data.shape_keys.key_blocks
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]

# the exact WIDE pose from face_poses
JAW = 31.0
SHAPES = {"lip_lower_depress": 0.7, "lip_upper_raise": 0.45,
          "lip_corner_L_up": 0.2, "lip_corner_R_up": 0.2}
TONGUE = {"tongue_root": (-14, 0, 0), "tongue_mid": (-8, 0, 0)}

for k in kb:
    if k.name != "Basis": k.value = 0.0
for b in arm.pose.bones:
    b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * JAW), 0, 0)
for n, (rx, ry, rz) in TONGUE.items():
    arm.pose.bones[n].rotation_euler = (math.radians(rx), math.radians(ry), math.radians(rz))
for n, v in SHAPES.items():
    if n in kb: kb[n].value = v
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get(); deps.update(); head.evaluated_get(deps)

def matname(ob, idx):
    try:
        mi = ob.data.polygons[idx].material_index
        return ob.data.materials[mi].name if 0 <= mi < len(ob.data.materials) else "?"
    except Exception:
        return "?"

NX, NZ, SPAN = 121, 91, 1.25
rows, tally = [], {}
grid = []
for iz in range(NZ):
    line = []
    lz = (0.5 - iz / (NZ - 1.0)) * MW * SPAN          # top row first
    for ix in range(NX):
        lx = F.cx + (ix / (NX - 1.0) - 0.5) * MW * SPAN
        o = F.world(V((lx, -0.40, lz)))
        d = (F.world(V((lx, 1.0, lz))) - o).normalized()
        hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(deps, o, d)
        if not hit:
            line.append("."); continue
        local = F.local(loc)
        key = (ob.name, matname(ob, idx))
        t = tally.setdefault(key, {"n": 0, "ymin": 9e9, "ymax": -9e9})
        t["n"] += 1
        ymm = local.y / MW * 50.0
        t["ymin"] = min(t["ymin"], ymm); t["ymax"] = max(t["ymax"], ymm)
        m = matname(ob, idx).split(".")[0]
        line.append({"MARS_TEETH_MAT": "T", "MARS_GUM_MAT": "g", "MARS_TONGUE_MAT": "o",
                     "MARS_SOCK_MAT": "s", "MARS_ORAL_MAT": "c"}.get(m, "#"))
        grid.append((ix, iz, lx, lz, ob.name, m, ymm))
    rows.append("".join(line))

print("WIDE pose, %d x %d rays.  # skin/unknown  T teeth  g gum  o tongue  s sock  c cavity" % (NX, NZ))
for i, r in enumerate(rows):
    if i % 2 == 0: print("%3d %s" % (i, r))
print()
print("%-26s %-18s %6s %9s %9s" % ("OBJECT", "MATERIAL", "rays", "front mm", "back mm"))
for (ob, mat), t in sorted(tally.items(), key=lambda kv: -kv[1]["n"]):
    print("%-26s %-18s %6d %9.2f %9.2f" % (ob, mat, t["n"], t["ymin"], t["ymax"]))
