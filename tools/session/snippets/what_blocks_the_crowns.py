# "we want the teeth to show at the top, not be covered by dark blue shadow lip
# stuff, like the lip hangs down too far in front of the teeth."
# 800 crown vertices, one ray each, classified by the MATERIAL of the first face
# hit -- MARS_TEETH_* carries teeth AND gums, so the OBJECT cannot answer this.
# And for anything blocked by HIS SKIN, report how far that face travels when the
# jaw opens, because a face that rides the jaw is more lip flap to shave.
import bpy, math, os, sys, json, mathutils, collections
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
kb = head.data.shape_keys.key_blocks
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]

def pose(jaw, shapes):
    for k in kb:
        if k.name != "Basis": k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * jaw), 0, 0)
    for n_, v in shapes.items():
        if n_ in kb: kb[n_].value = v
    bpy.context.view_layer.update()
    d = bpy.context.evaluated_depsgraph_get(); d.update(); head.evaluated_get(d)
    return d

WIDE = {"lip_lower_depress":0.7,"lip_upper_raise":0.45,"lip_corner_L_up":0.2,"lip_corner_R_up":0.2}
deps = pose(31.0, WIDE)

def matof(ob, idx):
    try:
        mi = ob.data.polygons[idx].material_index
        return (ob.data.materials[mi].name if 0 <= mi < len(ob.data.materials) else "?").split(".")[0]
    except Exception:
        return "?"

tu = bpy.data.objects["MARS_TEETH_UPPER"].evaluated_get(deps); tm = tu.to_mesh()
Mt = tu.matrix_world
crowns = []
for p in tm.polygons:
    mi = p.material_index
    if (tm.materials[mi].name if 0 <= mi < len(tm.materials) else "").split(".")[0] != "MARS_TEETH_MAT":
        continue
    crowns.append(Mt @ p.center)
tu.to_mesh_clear()
print("upper CROWN faces sampled: %d" % len(crowns))

OUTW = (F.world(V((F.cx, -1.0, 0.0))) - F.world(V((F.cx, 0.0, 0.0)))).normalized()
tally = collections.Counter(); blockers = collections.Counter()
for c in crowns:
    o = c + OUTW * (0.2 * MW)
    hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(deps, o, OUTW)
    if not hit:
        tally["VISIBLE"] += 1; continue
    m = matof(ob, idx)
    key = "HIS SKIN" if m.startswith("tripo") else ("%s/%s" % (ob.name, m))
    tally[key] += 1
    if key == "HIS SKIN": blockers[int(idx)] += 1
tot = sum(tally.values())
print("\n%-34s %6s %7s" % ("what the crown sees looking OUT", "rays", "share"))
for k, n in tally.most_common():
    print("%-34s %6d %6.1f%%  %s" % (k, n, 100.0*n/tot, "#"*int(40*n/tot)))

# for the skin blockers: how far do they ride the jaw? that decides shave vs keep
if blockers:
    me = head.data
    r = pose(0.0, {}); ev = head.evaluated_get(r); m0 = ev.to_mesh()
    R = np.array([(ev.matrix_world @ v.co)[:] for v in m0.vertices]); fs = [tuple(p.vertices) for p in m0.polygons]
    ev.to_mesh_clear()
    d2 = pose(31.0, WIDE); ev = head.evaluated_get(d2); m1 = ev.to_mesh()
    Wd = np.array([(ev.matrix_world @ v.co)[:] for v in m1.vertices]); ev.to_mesh_clear()
    MMu = MW/50.0
    print("\n%-9s %6s %11s %9s %9s" % ("FACE","rays","travel mm","z mm","area mm2"))
    rows=[]
    for fi, n in blockers.most_common(14):
        if fi >= len(fs): continue
        f = fs[fi]
        t = float(np.linalg.norm(R[list(f)].mean(0) - Wd[list(f)].mean(0)))/MMu
        c = F.local(V(R[list(f)].mean(0).tolist()))
        a = 0.5*float(np.linalg.norm(np.cross(R[f[1]]-R[f[0]], R[f[2]]-R[f[0]])))/(MMu*MMu)
        rows.append((fi,n,t,mm(c.z),a))
    for r_ in rows: print("%-9d %6d %11.2f %9.1f %9.2f" % r_)
    trav=[x[2] for x in rows]
    print("\nskin faces blocking crowns: %d distinct, %d rays" % (len(blockers), sum(blockers.values())))
    if trav: print("their jaw travel: median %.2f mm  max %.2f mm" % (float(np.median(trav)), max(trav)))
