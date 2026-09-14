# OWNER: "it was some skin vertices being stretched downward from skin weights".
# TEST IT. Take the skin vertices that end up hanging in the mouth opening at
# WIDE, and ask where they sit at REST and WHICH BONES move them.
# If they are fine at rest and travel down/forward when the jaw opens, it is
# WEIGHTS, and the fix is a weight repair, not geometry.
import bpy, math, os, sys, json, mathutils
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
kb = head.data.shape_keys.key_blocks
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]

def pose(jaw, shapes, tongue):
    for k in kb:
        if k.name != "Basis": k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * jaw), 0, 0)
    for n_, r in tongue.items():
        arm.pose.bones[n_].rotation_euler = tuple(math.radians(a) for a in r)
    for n_, v in shapes.items():
        if n_ in kb: kb[n_].value = v
    bpy.context.view_layer.update()
    d = bpy.context.evaluated_depsgraph_get(); d.update()
    return d

def coords(deps):
    e = head.evaluated_get(deps); m = e.to_mesh()
    out = [F.local(e.matrix_world @ v.co) for v in m.vertices]
    e.to_mesh_clear(); return out

REST = coords(pose(0.0, {}, {}))
WIDE = coords(pose(31.0, {"lip_lower_depress":0.7,"lip_upper_raise":0.45,
                          "lip_corner_L_up":0.2,"lip_corner_R_up":0.2},
                   {"tongue_root":(-14,0,0),"tongue_mid":(-8,0,0)}))
print("evaluated verts: rest %d  wide %d" % (len(REST), len(WIDE)))

# THE APERTURE BOX, and "in front of his lip plane" = local y < 0
HALF_X, ZTOP, ZBOT = 26.0, 22.0, -26.0
sus = []
for i, (r, w) in enumerate(zip(REST, WIDE)):
    x, y, z = mm(w.x - F.cx), mm(w.y), mm(w.z)
    if abs(x) > HALF_X or not (ZBOT < z < ZTOP) or y >= 0.0:
        continue
    rx, ry, rz = mm(r.x - F.cx), mm(r.y), mm(r.z)
    sus.append((i, rx, ry, rz, x, y, z, z - rz, y - ry))
print("skin verts hanging IN FRONT of his lip plane inside the aperture at WIDE: %d" % len(sus))
if sus:
    dz = sorted(s[7] for s in sus); dy = sorted(s[8] for s in sus)
    print("  their travel from REST:  dz median %+.2f  min %+.2f  max %+.2f mm   (negative = DOWNWARD)"
          % (dz[len(dz)//2], dz[0], dz[-1]))
    print("                           dy median %+.2f  min %+.2f  max %+.2f mm   (negative = FORWARD)"
          % (dy[len(dy)//2], dy[0], dy[-1]))
    at_rest_in = sum(1 for s in sus if s[3] > ZBOT and s[3] < ZTOP and abs(s[1]) < HALF_X and s[2] < 0.0)
    print("  of those, already in front of the lip plane AT REST: %d of %d" % (at_rest_in, len(sus)))

# WHICH BONES MOVE THEM -- read the actual vertex groups, never the names
vg = {g.index: g.name for g in head.vertex_groups}
tot = {}
for s in sus:
    for g in head.data.vertices[s[0]].groups:
        n = vg.get(g.group, "?")
        t = tot.setdefault(n, {"n": 0, "w": 0.0, "max": 0.0})
        if g.weight > 1e-4:
            t["n"] += 1; t["w"] += g.weight; t["max"] = max(t["max"], g.weight)
print()
print("%-22s %6s %9s %8s" % ("VERTEX GROUP", "verts", "sum w", "max w"))
for n, t in sorted(tot.items(), key=lambda kv: -kv[1]["w"]):
    print("%-22s %6d %9.2f %8.3f" % (n, t["n"], t["w"], t["max"]))

json.dump([list(s) for s in sus], open("renders/_tongue/skin_in_the_mouth.json", "w"))
print("\nwrote renders/_tongue/skin_in_the_mouth.json")
