# OWNER: "the parts on the top lip are the parts that are being ripped out of the
# bottom lip. They fit back in perfectly... take the triangles from the top lip
# that are extra and move them down to the bottom lip, they fit like a puzzle."
#
# THAT IS A TESTABLE CLAIM. The lip seam was SPLIT -- duplicate vertices, each
# face assigned to the upper or the lower lip. If a face was assigned to the
# WRONG side it travels with the wrong lip when the jaw opens: a notch appears
# in one lip and a flap sticks out of the other, and at REST they sit together
# perfectly because that is where they were cut apart.
#
# So: measure every lip face's TRAVEL from REST to WIDE. His jaw carries the
# lower lip 46.9 mm and leaves the upper at 0.08 mm -- two populations that could
# not be further apart. A face sitting ABOVE the seam that travels with the lower
# lip (or below it travelling with the upper) is a mis-assigned puzzle piece.
import bpy, math, os, sys, json, mathutils
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
kb = head.data.shape_keys.key_blocks
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]
anat = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
SEAM = np.vstack([np.array(anat["contours"]["lip_inner_upper"], float),
                  np.array(anat["contours"]["lip_inner_lower"], float)])
MM = MW / 50.0

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
    e = head.evaluated_get(d); m = e.to_mesh()
    P = np.array([(e.matrix_world @ v.co)[:] for v in m.vertices], float)
    faces = [tuple(p.vertices) for p in m.polygons]
    e.to_mesh_clear()
    return P, faces

REST, FACES = pose(0.0, {}, {})
WIDE, _     = pose(31.0, {"lip_lower_depress":0.7,"lip_upper_raise":0.45,
                          "lip_corner_L_up":0.2,"lip_corner_R_up":0.2},
                   {"tongue_root":(-14,0,0),"tongue_mid":(-8,0,0)})
print("verts %d   faces %d" % (len(REST), len(FACES)))

C0 = np.array([REST[list(f)].mean(0) for f in FACES])
C1 = np.array([WIDE[list(f)].mean(0) for f in FACES])
travel = np.linalg.norm(C1 - C0, axis=1) / MM
d2seam = np.sqrt(((C0[:, None, :] - SEAM[None, :, :]) ** 2).sum(-1)).min(1) / MM
Cl = np.array([list(F.local(V(c))) for c in C0])
zl = (Cl[:, 2]) / MM                      # height above his lip seam, mm

BAND = d2seam < 10.0
print("faces within 10 mm of his lip contour: %d" % int(BAND.sum()))
t = travel[BAND]
print("their travel when the jaw opens: median %.2f  p10 %.2f  p90 %.2f  max %.2f mm"
      % (np.median(t), np.percentile(t,10), np.percentile(t,90), t.max()))

# TWO POPULATIONS: the upper lip stays, the lower lip rides the jaw.
STAY, RIDE = 8.0, 20.0
upper_band = BAND & (zl > 1.0)            # above his seam at REST
lower_band = BAND & (zl < -1.0)           # below it
print("\n%-34s %6s %8s %8s" % ("", "faces", "stay<8mm", "ride>20mm"))
for lab, m_ in (("ABOVE the seam (upper lip)", upper_band), ("BELOW the seam (lower lip)", lower_band)):
    print("%-34s %6d %8d %8d" % (lab, int(m_.sum()),
          int((m_ & (travel < STAY)).sum()), int((m_ & (travel > RIDE)).sum())))

wrong_up = np.nonzero(upper_band & (travel > RIDE))[0]   # on the top lip, riding the jaw
wrong_dn = np.nonzero(lower_band & (travel < STAY))[0]   # on the bottom lip, staying put
print("\nMIS-ASSIGNED PUZZLE PIECES")
print("  faces ON the upper lip that RIDE the jaw down : %d" % len(wrong_up))
print("  faces ON the lower lip that STAY with the top : %d" % len(wrong_dn))
areas = np.array([0.5*np.linalg.norm(np.cross(REST[f[1]]-REST[f[0]], REST[f[2]]-REST[f[0]]))
                  for f in FACES]) / (MM*MM)
for lab, idx in (("upper-riding", wrong_up), ("lower-staying", wrong_dn)):
    if not len(idx): continue
    print("  %s: area sum %.1f mm2, worst %.1f mm2, x %.1f..%.1f mm, z %.1f..%.1f mm"
          % (lab, areas[idx].sum(), areas[idx].max(),
             mm(Cl[idx,0].min()-F.cx), mm(Cl[idx,0].max()-F.cx), zl[idx].min(), zl[idx].max()))
    for i in idx[np.argsort(-areas[idx])][:8]:
        print("      face %-7d x %6.1f z %6.1f  travel %6.2f mm  area %6.2f mm2"
              % (i, mm(Cl[i,0]-F.cx), zl[i], travel[i], areas[i]))
json.dump({"upperRiding": [int(i) for i in wrong_up], "lowerStaying": [int(i) for i in wrong_dn]},
          open("renders/_tongue/lip_puzzle_pieces.json", "w"))
print("\nwrote renders/_tongue/lip_puzzle_pieces.json")
