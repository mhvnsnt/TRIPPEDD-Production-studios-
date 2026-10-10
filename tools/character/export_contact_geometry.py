"""
STAGE 1 OF THE COLLISION MEASUREMENT: dump what is ACTUALLY ON SCREEN, per frame.

The owner asked for collision detection so "hair can't face through the face" and
"the tongue can't face through the cheeks". That cannot be answered from a rig
description or a modifier setting -- it has to be answered from the EVALUATED
geometry, after the armature, the shape keys, the boolean that carves his mouth
cavity and the cloth cache have all run.

So this stage evaluates the depsgraph at every frame and writes world-space
vertices and triangles per named PART to a single .npz. It does no collision
maths at all, because Blender ships numpy 1.24 / py3.11 and the collision stack
(libigl, FCL, trimesh) lives in .trippedd_venv on numpy 2.x -- mixing the two
ABIs is how a compiled extension segfaults halfway through a bake.

Splitting it also means THE GEOMETRY ITSELF IS PUBLISHED EVIDENCE. Any agent, on
any model, can re-run stage 2 against the same .npz and get the same numbers
without owning a Blender or re-baking a cloth cache. OWNER LAW #2.

A PART is  OBJECT  or  OBJECT:VERTEX_GROUP  (region of an object, weight > 0.5).
A region part carries the faces whose vertices are ALL in the group, so a region
boundary never invents a triangle that spans two features.

    vendor/blender/blender -b <scene.blend> -P tools/character/export_contact_geometry.py -- \
        --part MARS_TONGUE --part MARS_MESH --part MARS_MESH:HAIR_REGION \
        --frames 1-36 --out docs/evidence/collision/oral_geom.npz
"""
import bpy, sys, os, json
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d=None):
    return argv[argv.index(f) + 1] if f in argv else d
def opts(f):
    return [argv[i + 1] for i, a in enumerate(argv) if a == f]
def die(m):
    # Blender -b swallows the argument to sys.exit(), so a refusal with no
    # printed reason reads exactly like a segfault. Print, flush, THEN exit.
    print("\n*** REFUSED: %s\n" % m, flush=True)
    sys.stdout.flush()
    sys.exit(1)

PARTS = opts("--part")
OUT   = opt("--out", "contact_geom.npz")
GROUP_MIN = float(opt("--group-min", "0.5"))
rng = opt("--frames", "1-1")
if "-" in rng:
    F0, F1 = (int(x) for x in rng.split("-", 1))
else:
    F0 = F1 = int(rng)
if not PARTS:
    die("no --part given. There is nothing to measure and an empty run must never "
        "report a clean sheet (a gate with zero checks reports 0/0 PASS).")

scene = bpy.context.scene
dg = bpy.context.evaluated_depsgraph_get()


def resolve(spec):
    name, _, grp = spec.partition(":")
    ob = bpy.data.objects.get(name)
    if ob is None:
        die("part '%s' names object '%s', which is not in this scene. Objects here: %s"
            % (spec, name, sorted(o.name for o in bpy.data.objects if o.type == "MESH")))
    if ob.type != "MESH":
        die("part '%s' is a %s, not a MESH" % (spec, ob.type))
    if grp and grp not in ob.vertex_groups:
        die("part '%s' names vertex group '%s' which object '%s' does not have. It has: %s"
            % (spec, grp, name, [g.name for g in ob.vertex_groups]))
    return ob, (grp or None)


def evaluate(ob, grp):
    """World-space verts + triangles of the EVALUATED object at the current frame."""
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    try:
        me.calc_loop_triangles()
        n = len(me.vertices)
        co = np.empty(n * 3, dtype=np.float64)
        me.vertices.foreach_get("co", co)
        co = co.reshape(n, 3)
        tri = np.empty(len(me.loop_triangles) * 3, dtype=np.int32)
        me.loop_triangles.foreach_get("vertices", tri)
        tri = tri.reshape(-1, 3)
        sel = None
        if grp is not None:
            gi = ob.vertex_groups[grp].index
            # The evaluated mesh keeps vertex groups when the modifier stack does
            # not change topology. When it does (a BOOLEAN does), fall back to the
            # ORIGINAL mesh's group and map by index only if the counts agree --
            # otherwise refuse rather than silently measure the wrong vertices.
            src = me if len(me.vertices) == len(ob.data.vertices) else ob.data
            if len(src.vertices) != len(me.vertices):
                die("part '%s:%s': the modifier stack changed the vertex count "
                    "(%d -> %d), so the vertex group cannot be mapped onto the "
                    "evaluated mesh. Measure the whole object, or bake the region "
                    "into its own object." % (ob.name, grp, len(ob.data.vertices), n))
            w = np.zeros(n)
            for vi, v in enumerate(src.vertices):
                for ge in v.groups:
                    if ge.group == gi:
                        w[vi] = ge.weight
            sel = w > GROUP_MIN
        mw = np.array(ob.matrix_world.to_4x4())
        world = co @ mw[:3, :3].T + mw[:3, 3]
        if sel is not None:
            if not sel.any():
                die("part '%s:%s' selects 0 vertices at weight > %.2f" % (ob.name, grp, GROUP_MIN))
            keep = np.zeros(n, dtype=bool); keep[sel] = True
            # only triangles ENTIRELY inside the region -- a boundary triangle that
            # spans two features is not part of either of them
            tri = tri[keep[tri].all(axis=1)]
            remap = -np.ones(n, dtype=np.int64)
            idx = np.nonzero(keep)[0]
            remap[idx] = np.arange(len(idx))
            tri = remap[tri]
            world = world[idx]
        return world, tri
    finally:
        ev.to_mesh_clear()


resolved = [(s,) + resolve(s) for s in PARTS]
store = {}
frames = list(range(F0, F1 + 1))
for fi, f in enumerate(frames):
    scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    for spec, ob, grp in resolved:
        V, T = evaluate(ob, grp)
        key = spec.replace(":", "__")
        if fi == 0:
            store["%s/tris" % key] = T.astype(np.int32)
            store["%s/nv" % key] = np.array([len(V)])
        else:
            if len(V) != int(store["%s/nv" % key][0]):
                die("part '%s' changed vertex count between frames (%d -> %d). "
                    "A moving vertex count means the pairs cannot be tracked."
                    % (spec, int(store["%s/nv" % key][0]), len(V)))
        store.setdefault("%s/verts" % key, []).append(V.astype(np.float32))
    if fi % 10 == 0:
        print("  frame %d/%d" % (f, frames[-1]), flush=True)

out = {}
for k, v in store.items():
    out[k] = np.stack(v) if isinstance(v, list) else v
out["__frames__"] = np.array(frames, dtype=np.int32)
out["__parts__"] = np.array([s.replace(":", "__") for s in PARTS])
out["__specs__"] = np.array(PARTS)
out["__blend__"] = np.array([bpy.data.filepath or "<unsaved>"])
os.makedirs(os.path.dirname(os.path.abspath(OUT)) or ".", exist_ok=True)
np.savez_compressed(OUT, **out)
print("\nwrote %s" % OUT, flush=True)
for s in PARTS:
    k = s.replace(":", "__")
    print("  %-28s %6d verts  %6d tris  x %d frames"
          % (s, int(out["%s/nv" % k][0]), len(out["%s/tris" % k]), len(frames)), flush=True)
