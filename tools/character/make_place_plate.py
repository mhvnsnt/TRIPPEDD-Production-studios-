"""
A PLATE HE CAN TAP ON, AND A POSITION MAP SO A TAP IS AN EXACT 3D POINT.

Owner: *"Those are wrong white lines and white dots, how can you give me the
ability to place them?"*

He should place them. The previous route -- render a plate, he draws on it in an
image editor, a reader extracts the strokes by colour, a lifter raycasts them onto
the mesh -- put his "eyelid" lines 85 mm up on his FOREHEAD. Somewhere in that
chain the 2D->3D mapping is wrong, and no amount of re-drawing fixes a broken lift.

THIS REMOVES THE LIFT ENTIRELY. Alongside the beauty render, every pixel's own
surface position is written out: `pos[y][x]` IS the 3D point the camera sees at
that pixel. A tap at (x, y) therefore returns an exact surface point with no
raycast, no depth prior, no scale assumption and nothing to get wrong. Pixels that
see nothing are marked, so a tap on the background is refused instead of silently
snapping somewhere plausible.

The camera is his own head frame, facing +fwd (out of the face) -- the convention
face_plate documents and the one every camera in this repo got backwards until it
was checked against his nostrils.

    vendor/blender/blender -b -P tools/character/make_place_plate.py -- --res 1024
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V, Matrix as M

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("make_place_plate.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
MM = FP.MM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

RES  = int(opt("--res", "1024"))
GRID = int(opt("--grid", "512"))          # resolution of the position map handed to the page
OUT  = os.path.join(ROOT, "docs", "evidence", "place")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"))
scene = bpy.context.scene
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
for ob in bpy.data.objects:
    if ob.name.startswith("MARS_EYE_"):
        ob.hide_render = True             # his PAINTED eyes must be what he sees
    if ob.type == "ARMATURE":
        ob.hide_render = True
if o.data.shape_keys:
    for k in o.data.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0

fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
P = np.array([v.co[:] for v in o.data.vertices])
W = np.array(o.matrix_world)
Pw = P @ W[:3, :3].T + W[:3, 3]
ctr = Pw.mean(0)
rad = float(np.linalg.norm(Pw - ctr, axis=1).max())

d_ = np.asarray(fwd, float); d_ /= np.linalg.norm(d_)
u_ = np.asarray(up, float).copy(); u_ -= d_ * np.dot(u_, d_); u_ /= np.linalg.norm(u_)
r_ = np.cross(u_, d_)
SCALE = rad * 1.55                        # ortho width in world units
org = ctr + d_ * rad * 3

scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = scene.render.resolution_y = RES
scene.render.film_transparent = False
scene.view_settings.view_transform = "Standard"
try: scene.eevee.taa_render_samples = 32
except Exception: pass
wd = bpy.data.worlds.new("W"); scene.world = wd; wd.use_nodes = True
wd.node_tree.nodes["Background"].inputs[0].default_value = (0.06, 0.06, 0.08, 1)
wd.node_tree.nodes["Background"].inputs[1].default_value = 1.9
for nm, a_, b_, c_, e_ in (("K", -0.9, 0.7, 1.7, 300), ("F", 1.2, 0.15, 1.3, 260),
                           ("T", 0.0, 1.5, 0.9, 180)):
    L = bpy.data.lights.new(nm, type="AREA"); L.energy = e_; L.size = rad * 1.6
    ob = bpy.data.objects.new(nm, L); scene.collection.objects.link(ob)
    ob.location = tuple(ctr + (x * a_ + up * b_ + fwd * c_) * rad * 2.0)
    ob.rotation_euler = (V(tuple(ctr)) - V(ob.location)).to_track_quat("-Z", "Y").to_euler()

cd = bpy.data.cameras.new("PLACE"); cd.type = "ORTHO"; cd.ortho_scale = SCALE
cam = bpy.data.objects.new("PLACE", cd); scene.collection.objects.link(cam)
cam.matrix_world = M(((r_[0], u_[0], d_[0], org[0]), (r_[1], u_[1], d_[1], org[1]),
                      (r_[2], u_[2], d_[2], org[2]), (0, 0, 0, 1)))
scene.camera = cam
plate = os.path.join(OUT, "MARS_place_plate.png")
scene.render.filepath = plate
bpy.ops.render.render(write_still=True)
print("rendered %s" % plate, flush=True)

# ---- THE POSITION MAP -----------------------------------------------------
# One ray per grid cell, straight down the camera axis, against the EVALUATED mesh.
# An ORTHO camera means every ray is parallel, so this is exactly the inverse of the
# projection the render used -- a pixel and a world column are the same thing.
dg = bpy.context.evaluated_depsgraph_get()
ev = o.evaluated_get(dg)
pos = np.full((GRID, GRID, 3), np.nan, dtype=np.float32)
hits = 0
Winv = np.array(o.matrix_world.inverted())
for j in range(GRID):
    v = 0.5 - (j + 0.5) / GRID           # +up at the top row
    for i in range(GRID):
        u = (i + 0.5) / GRID - 0.5
        o_w = ctr + r_ * (u * SCALE) + u_ * (v * SCALE) + d_ * (rad * 3)
        o_l = np.array(o_w) @ Winv[:3, :3].T + Winv[:3, 3]
        d_l = np.array(-d_) @ Winv[:3, :3].T
        ok, loc, nrm, idx = ev.ray_cast(V(tuple(o_l)), V(tuple(d_l)))
        if ok:
            lw = np.array(loc) @ W[:3, :3].T + W[:3, 3]
            pos[j, i] = lw
            hits += 1
    if j % 64 == 0:
        print("  position map row %d/%d" % (j, GRID), flush=True)
print("position map: %d of %d cells hit the surface (%.1f%%)"
      % (hits, GRID * GRID, 100.0 * hits / (GRID * GRID)), flush=True)
if hits < 0.15 * GRID * GRID:
    die("only %.1f%% of the plate hit the mesh. A position map that mostly misses "
        "would refuse most of his taps and look like the tool is broken."
        % (100.0 * hits / (GRID * GRID)))

np.savez_compressed(os.path.join(OUT, "position_map.npz"), pos=pos,
                    centre=ctr, right=r_, up=u_, fwd=d_, scale=np.array([SCALE]),
                    grid=np.array([GRID]), mm=np.array([MM]))
meta = {
    "schema": "trippedd.place-plate/v1",
    "plate": os.path.relpath(plate, ROOT),
    "positionMap": os.path.relpath(os.path.join(OUT, "position_map.npz"), ROOT),
    "res": RES, "grid": GRID,
    "orthoScale": float(SCALE), "mmPerUnit": float(MM),
    "camera": {"centre": [float(c) for c in ctr],
               "right": [float(c) for c in r_],
               "up": [float(c) for c in u_],
               "forward": [float(c) for c in d_]},
    "surfaceHitFraction": round(hits / float(GRID * GRID), 4),
    "note": "pos[j][i] is the exact 3D surface point the camera sees at that cell. A tap "
            "needs no raycast and no depth prior; NaN means the tap missed the head and "
            "must be refused rather than snapped somewhere plausible.",
}
json.dump(meta, open(os.path.join(OUT, "place_plate.json"), "w"), indent=2)
print("wrote %s" % os.path.join(OUT, "place_plate.json"), flush=True)
