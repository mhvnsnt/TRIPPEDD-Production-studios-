# Every skin vertex hanging in his mouth opening carries jaw weight 0.000.
# So ask the whole question: WHAT DOES THE JAW BONE ACTUALLY MOVE ON HIS SKIN?
# If the jaw group is empty or tiny, his lower lip and chin never follow the jaw,
# the teeth drop away from the skin, and the upper lip is left sheeted across the
# opening. That is a WEIGHTS defect and it is fixable as one.
import bpy, math, os, sys, json, mathutils
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
print("armature bones:", ", ".join(b.name for b in arm.data.bones))
print("vertex groups on MARS_MESH:", ", ".join(g.name for g in head.vertex_groups))
print("modifiers:", ", ".join("%s(%s)" % (m.name, m.type) for m in head.modifiers))
print()

vg = {g.name: g.index for g in head.vertex_groups}
for name, gi in sorted(vg.items()):
    ws = []
    for v in head.data.vertices:
        for g in v.groups:
            if g.group == gi and g.weight > 1e-4:
                ws.append((v.index, g.weight))
    if not ws:
        print("%-14s   0 verts" % name); continue
    w = sorted(x[1] for x in ws)
    zs = [mm(F.local(head.matrix_world @ head.data.vertices[i].co).z) for i, _ in ws]
    ys = [mm(F.local(head.matrix_world @ head.data.vertices[i].co).y) for i, _ in ws]
    print("%-14s %5d verts   w median %.3f max %.3f   z %7.1f..%7.1f  y %7.1f..%7.1f mm"
          % (name, len(ws), w[len(w)//2], w[-1], min(zs), max(zs), min(ys), max(ys)))

# THE DIRECT QUESTION: does his lower lip travel when the jaw opens?
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]
kb = head.data.shape_keys.key_blocks
def snap(jaw, shapes):
    for k in kb:
        if k.name != "Basis": k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * jaw), 0, 0)
    for n_, v in shapes.items():
        if n_ in kb: kb[n_].value = v
    bpy.context.view_layer.update()
    d = bpy.context.evaluated_depsgraph_get(); d.update()
    e = head.evaluated_get(d); m = e.to_mesh()
    out = [F.local(e.matrix_world @ v.co) for v in m.vertices]
    e.to_mesh_clear(); return out

REST = snap(0.0, {})
JAWONLY = snap(31.0, {})                      # the BONE alone, no lip shape keys
print()
print("JAW BONE AT 31 DEGREES, NO SHAPE KEYS -- what on his skin actually travels?")
bands = {"upper lip  z +2..+14": (2, 14), "lower lip  z -14..-2": (-14, -2),
         "chin       z -40..-16": (-40, -16), "forehead   z +45..+70": (45, 70)}
for label, (lo, hi) in bands.items():
    d = []
    for r, w in zip(REST, JAWONLY):
        z = mm(r.z); x = mm(r.x - F.cx)
        if lo < z < hi and abs(x) < 26.0 and mm(r.y) < 12.0:
            d.append((w - r).length / MW * 50.0)
    if not d:
        print("  %-24s no verts" % label); continue
    d.sort()
    print("  %-24s %5d verts   travel median %6.3f  p95 %6.3f  max %6.3f mm"
          % (label, len(d), d[len(d)//2], d[int(len(d)*0.95)], d[-1]))

for part in ("MARS_TEETH_LOWER", "MARS_TONGUE"):
    ob = bpy.data.objects[part]
    print("  %-24s parent=%s  parent_bone=%r  groups=%s" %
          (part, ob.parent.name if ob.parent else None, ob.parent_bone,
           ",".join(g.name for g in ob.vertex_groups) or "-"))
