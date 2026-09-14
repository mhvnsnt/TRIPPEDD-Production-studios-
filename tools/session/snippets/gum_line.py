# OWNER: "some pink or magenta color stuff coming up too high in front of the
# bottom front teeth, eating them up ... they look like baby teeth growing out
# of the gums."
# PINK in the map is MARS_GUM_MAT. Measure the GINGIVAL MARGIN against the crowns
# it is supposed to sit at the base of. Real anatomy: the whole clinical crown
# stands proud of the gum -- a lower central incisor's crown is ~9 mm tall and
# essentially all of it is visible.
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
for k in kb:
    if k.name != "Basis": k.value = 0.0
for b in arm.pose.bones:
    b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get(); dg.update()

def split(objname):
    ob = bpy.data.objects[objname].evaluated_get(dg); m = ob.to_mesh(); M = ob.matrix_world
    out = {}
    for p in m.polygons:
        mi = p.material_index
        nm = (m.materials[mi].name if 0 <= mi < len(m.materials) else "?").split(".")[0]
        for vi in p.vertices:
            l = F.local(M @ m.vertices[vi].co)
            out.setdefault(nm, []).append((mm(l.x - F.cx), mm(l.y), mm(l.z)))
    ob.to_mesh_clear()
    return {k: np.array(v) for k, v in out.items()}

for arch, updown in (("MARS_TEETH_LOWER", +1), ("MARS_TEETH_UPPER", -1)):
    d = split(arch)
    T = d.get("MARS_TEETH_MAT"); G = d.get("MARS_GUM_MAT")
    print("\n=== %s ===  teeth verts %d   gum verts %d"
          % (arch, 0 if T is None else len(T), 0 if G is None else len(G)))
    if T is None or G is None: continue
    print("%8s %10s %10s %10s %10s %9s" %
          ("x band", "crown top", "crown base", "gum top", "crown mm", "exposed"))
    for lo in range(-24, 24, 6):
        hi = lo + 6
        t = T[(T[:,0] >= lo) & (T[:,0] < hi)]
        g = G[(G[:,0] >= lo) & (G[:,0] < hi)]
        if len(t) < 5 or len(g) < 5: continue
        if updown > 0:      # lower arch: crowns point UP, gum sits BELOW
            ctop, cbase, gtop = t[:,2].max(), t[:,2].min(), g[:,2].max()
            crown = ctop - cbase
            exposed = (ctop - max(gtop, cbase)) / crown if crown > 1e-6 else 0.0
        else:               # upper arch: crowns point DOWN, gum sits ABOVE
            ctop, cbase, gtop = t[:,2].min(), t[:,2].max(), g[:,2].min()
            crown = cbase - ctop
            exposed = (min(gtop, cbase) - ctop) / crown if crown > 1e-6 else 0.0
        print("%4d..%-4d %10.2f %10.2f %10.2f %10.2f %8.0f%%"
              % (lo, hi, ctop, cbase, gtop, crown, 100.0 * exposed))

    # how much of the crown does the gum stand IN FRONT of, seen from the camera?
    print("  anterior band |x| < 15 mm:")
    t = T[np.abs(T[:,0]) < 15]; g = G[np.abs(G[:,0]) < 15]
    print("    crowns  z %7.2f..%7.2f mm   front y %7.2f mm" % (t[:,2].min(), t[:,2].max(), t[:,1].min()))
    print("    gums    z %7.2f..%7.2f mm   front y %7.2f mm" % (g[:,2].min(), g[:,2].max(), g[:,1].min()))
    dy = t[:,1].min() - g[:,1].min()
    print("    the gum's front face is %+.2f mm %s the crowns' front face"
          % (abs(dy), "IN FRONT OF" if dy > 0 else "behind"))
