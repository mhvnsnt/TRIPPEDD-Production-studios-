# IS EACH SUSPECT FACE A WALL OR A MEMBRANE?
# A cavity WALL has the air pocket on one side and his flesh on the other.
# A MEMBRANE hangs in the air pocket with air on BOTH sides -- it is the thing
# stretched across the middle of his open mouth, and it is exactly the defect
# already banked as "THE SKIN FILLING HIS MOUTH WAS 36 FACES SPANNING THE CREASE".
# Decided by PARITY against the closed shell, not by looking at a picture.
import bpy, math, os, sys, json, mathutils
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm  = lambda v: v / MW * 50.0
umm = lambda v: v * MW / 50.0

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
deps = bpy.context.evaluated_depsgraph_get(); deps.update()

# a REAL object carrying the evaluated shell, so ray_cast is exact and local
for junk in ("_PROBE",):
    if junk in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[junk], do_unlink=True)
ev = head.evaluated_get(deps); me = ev.to_mesh()
pm = bpy.data.meshes.new("_PROBE"); pm.from_pydata(
    [ev.matrix_world @ v.co for v in me.vertices], [],
    [list(p.vertices) for p in me.polygons])
pm.update()
probe = bpy.data.objects.new("_PROBE", pm)
bpy.context.scene.collection.objects.link(probe)
probe.hide_render = True   # NOT hide_viewport: a hidden object has no evaluated mesh and ray_cast refuses

DIRS = [V(d).normalized() for d in ((1, .11, .07), (-.09, 1, .13), (.05, .13, 1))]
def inside(p):
    """odd crossings of the closed shell in a majority of three directions."""
    votes = 0
    for d in DIRS:
        o = p.copy(); n = 0
        for _ in range(64):
            hit, loc, nor, idx = probe.ray_cast(o, d, distance=10.0)
            if not hit: break
            n += 1; o = loc + d * 1e-5
        votes += (n % 2)
    return votes >= 2

# sanity controls: a point deep in his skull must read INSIDE, a metre away OUTSIDE
deep = F.world(V((F.cx, umm(140.0), umm(40.0))))
far  = F.world(V((F.cx, umm(-1000.0), 0)))
print("CONTROL  deep in his head inside=%s   a metre in front inside=%s" % (inside(deep), inside(far)))

EPS = umm(1.6)
HALF_X, ZTOP, ZBOT = 26.0, 22.0, -26.0
tongue_front = None
tev = bpy.data.objects["MARS_TONGUE"].evaluated_get(deps); tme = tev.to_mesh()
tongue_front = min(mm(F.local(tev.matrix_world @ p.center).y)
                   for p in tme.polygons if abs(mm(F.local(tev.matrix_world @ p.center).x - F.cx)) < 7)
tev.to_mesh_clear()
print("his tongue's front-most midline face: %.2f mm" % tongue_front)

verdict = {}
for name in ("MARS_MESH", "MARS_MOUTH_SOCK"):
    ob = bpy.data.objects[name]; e = ob.evaluated_get(deps); m = e.to_mesh(); M = e.matrix_world
    wall = memb = 0; membs = []
    for p in m.polygons:
        c = M @ p.center; l = F.local(c)
        x, y, z = mm(l.x - F.cx), mm(l.y), mm(l.z)
        if abs(x) > HALF_X or not (ZBOT < z < ZTOP) or y >= tongue_front:
            continue
        mi = p.material_index
        mat = (m.materials[mi].name if 0 <= mi < len(m.materials) else "?").split(".")[0]
        if mat.startswith("tripo"):     # his exterior skin is a separate question
            continue
        nw = (M.to_3x3() @ p.normal).normalized()
        a, b = inside(c + nw * EPS), inside(c - nw * EPS)
        if a and b:   wall += 1        # buried entirely in flesh
        elif a or b:  wall += 1        # a real boundary: air one side, flesh the other
        else:
            memb += 1
            membs.append((p.index, x, y, z, p.area / MW / MW * 2500.0))
    e.to_mesh_clear()
    verdict[name] = membs
    print("%-18s  wall %3d   MEMBRANE (air on both sides) %3d   membrane area %.1f mm2"
          % (name, wall, memb, sum(r[4] for r in membs)))
    for r in sorted(membs, key=lambda r: -r[4])[:8]:
        print("      face %-7d x %6.1f  y %6.1f  z %6.1f   %7.2f mm2" % r)

json.dump({k: [list(r) for r in v] for k, v in verdict.items()},
          open("renders/_tongue/membranes.json", "w"), indent=1)
print("wrote renders/_tongue/membranes.json")
