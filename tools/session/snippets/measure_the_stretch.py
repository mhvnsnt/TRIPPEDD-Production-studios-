# The skin visible inside his mouth is 173 faces at |x| 21..31 mm -- HIS LIP
# CORNERS -- and the worst are 122-137 mm2 against a whole-head median of 0.43.
# Are they real skin, or single faces BRIDGING from his outer cheek across the
# lip rim into the cavity? A bridging face spans a huge DEPTH range; real skin
# on a surface does not. Measure the shape, do not infer it from the area.
import bpy, math, os, sys, json, mathutils, statistics as st
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]; me = head.data
M = head.matrix_world
faces = json.load(open("renders/_tongue/skin_faces_in_the_hole.json"))
print("examining %d faces" % len(faces))

def stats(p):
    vs = [F.local(M @ me.vertices[i].co) for i in p.vertices]
    ys = [mm(v.y) for v in vs]
    es = []
    for a in range(len(vs)):
        b = (a + 1) % len(vs)
        es.append(mm((vs[a] - vs[b]).length))
    # smallest angle of the triangle -- a sliver has one very small angle
    ang = []
    for a in range(len(vs)):
        u = vs[(a+1) % len(vs)] - vs[a]; w = vs[(a-1) % len(vs)] - vs[a]
        if u.length > 1e-9 and w.length > 1e-9:
            ang.append(math.degrees(u.angle(w)))
    return max(ys) - min(ys), max(es), min(ang) if ang else 0.0, p.area / MW / MW * 2500.0

rows = [(fi,) + stats(me.polygons[fi]) for fi in faces if fi < len(me.polygons)]
rows.sort(key=lambda r: -r[4])

print("\n%-9s %10s %10s %9s %10s" % ("FACE", "y span mm", "longest mm", "min ang", "area mm2"))
for r in rows[:12]:
    print("%-9d %10.2f %10.2f %9.2f %10.2f" % r)

span = sorted(r[1] for r in rows); edge = sorted(r[2] for r in rows)
ang  = sorted(r[3] for r in rows); area = sorted(r[4] for r in rows)
q = lambda a, f: a[min(len(a) - 1, int(len(a) * f))]
print("\nTHESE 173 FACES        median      p95       max")
print("  depth span        %9.2f %8.2f %9.2f mm" % (q(span,.5), q(span,.95), span[-1]))
print("  longest edge      %9.2f %8.2f %9.2f mm" % (q(edge,.5), q(edge,.95), edge[-1]))
print("  smallest angle    %9.2f %8.2f %9.2f deg (min %.2f)" % (q(ang,.5), q(ang,.95), ang[-1], ang[0]))
print("  area              %9.2f %8.2f %9.2f mm2" % (q(area,.5), q(area,.95), area[-1]))

# THE CONTROL: the same four statistics over his WHOLE head, so "huge" is a
# comparison and not an adjective.
allr = [stats(p) for p in me.polygons]
span = sorted(r[0] for r in allr); edge = sorted(r[1] for r in allr)
ang  = sorted(r[2] for r in allr); area = sorted(r[3] for r in allr)
print("\nWHOLE HEAD (%d faces)   median      p95       max" % len(allr))
print("  depth span        %9.2f %8.2f %9.2f mm" % (q(span,.5), q(span,.95), span[-1]))
print("  longest edge      %9.2f %8.2f %9.2f mm" % (q(edge,.5), q(edge,.95), edge[-1]))
print("  smallest angle    %9.2f %8.2f %9.2f deg" % (q(ang,.5), q(ang,.95), ang[-1]))
print("  area              %9.2f %8.2f %9.2f mm2" % (q(area,.5), q(area,.95), area[-1]))
