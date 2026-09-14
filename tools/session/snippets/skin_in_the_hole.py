# Stop filtering by coordinate boxes -- they keep catching his real lip.
# FIRE THE RAYS and keep only the ones that LAND ON SKIN while the hit is
# deeper than his own tooth line. That is skin you can SEE inside his mouth.
# Then name the faces, and ask whether they are there at REST too.
import bpy, math, os, sys, json, mathutils, collections
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm  = lambda v: v / MW * 50.0
umm = lambda v: v * MW / 50.0

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
    d = bpy.context.evaluated_depsgraph_get(); d.update(); head.evaluated_get(d)
    return d

def matof(ob, idx):
    try:
        mi = ob.data.polygons[idx].material_index
        return (ob.data.materials[mi].name if 0 <= mi < len(ob.data.materials) else "?").split(".")[0]
    except Exception:
        return "?"

deps = pose(31.0, {"lip_lower_depress":0.7,"lip_upper_raise":0.45,
                   "lip_corner_L_up":0.2,"lip_corner_R_up":0.2},
            {"tongue_root":(-14,0,0),"tongue_mid":(-8,0,0)})

NX, NZ, SPAN = 161, 121, 1.25
skin_hits = []      # (face_index, x, z, y_depth)
depth_hist = collections.Counter()
for iz in range(NZ):
    lz = (0.5 - iz / (NZ - 1.0)) * MW * SPAN
    for ix in range(NX):
        lx = F.cx + (ix / (NX - 1.0) - 0.5) * MW * SPAN
        o = F.world(V((lx, -0.40, lz)))
        d = (F.world(V((lx, 1.0, lz))) - o).normalized()
        hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(deps, o, d)
        if not hit or ob.name != "MARS_MESH": continue
        if matof(ob, idx) != "tripo_mat_63779a1f-eb9a-4b4a-a12c-e90b88a426b1": continue
        y = mm(F.local(loc).y)
        depth_hist[int(y // 2) * 2] += 1
        skin_hits.append((idx, mm(F.local(loc).x - F.cx), mm(F.local(loc).z), y))

print("DEPTH of every SKIN hit, in his own mm (0 = his lip plane, + = into his head)")
for k in sorted(depth_hist):
    if k < -20 or k > 40: continue
    print("  y %+4d..%+4d  %s %d" % (k, k + 2, "#" * min(60, depth_hist[k] // 40), depth_hist[k]))

# his upper crowns' front edge, measured, as the line that separates "his lip"
# from "skin inside his mouth"
tu = bpy.data.objects["MARS_TEETH_UPPER"].evaluated_get(deps); tm = tu.to_mesh()
crown_front = min(mm(F.local(tu.matrix_world @ v.co).y) for v in tm.vertices)
tu.to_mesh_clear()
print("\nhis upper crowns' front-most vertex: y %+.2f mm" % crown_front)

inside = [h for h in skin_hits if h[3] > crown_front + 2.0]
print("SKIN hits DEEPER than his crowns (skin visible inside his mouth): %d of %d skin hits"
      % (len(inside), len(skin_hits)))
faces = collections.Counter(h[0] for h in inside)
print("distinct faces responsible: %d" % len(faces))
me = head.data
tot = 0.0
print("\n%-9s %6s %8s %8s %8s %10s" % ("FACE", "rays", "x mm", "z mm", "y mm", "area mm2"))
for fi, n in faces.most_common(14):
    hs = [h for h in inside if h[0] == fi]
    a = me.polygons[fi].area / MW / MW * 2500.0 if fi < len(me.polygons) else float("nan")
    print("%-9d %6d %8.1f %8.1f %8.1f %10.2f"
          % (fi, n, sum(h[1] for h in hs)/n, sum(h[2] for h in hs)/n, sum(h[3] for h in hs)/n, a))
for fi in faces:
    if fi < len(me.polygons): tot += me.polygons[fi].area / MW / MW * 2500.0
print("total rest area of those faces: %.1f mm2" % tot)
json.dump(sorted(faces), open("renders/_tongue/skin_faces_in_the_hole.json", "w"))
print("wrote renders/_tongue/skin_faces_in_the_hole.json")
