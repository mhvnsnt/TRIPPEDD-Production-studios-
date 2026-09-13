"""Dump a named object's REST world geometry to .npz. Measurement only, no writes to the blend.

    vendor/blender/blender -b <file.blend> -P tools/character/dump_rest_mesh.py -- \
        --object MARS_MESH --out renders/_x/head.npz
"""
import bpy, sys, os
import numpy as np
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
name = opt("--object", "MARS_MESH")
out = os.path.abspath(opt("--out", "renders/_x/head.npz"))
os.makedirs(os.path.dirname(out), exist_ok=True)
o = bpy.data.objects.get(name)
if o is None:
    print("NOT_ATTEMPTED: no object %r in %s" % (name, bpy.data.filepath)); sys.exit(0)
me = o.data
me.calc_loop_triangles()
V = np.array([v.co[:] for v in me.vertices], dtype=np.float64)
M = np.array(o.matrix_world)
V = (M @ np.hstack([V, np.ones((len(V), 1))]).T).T[:, :3]
T = np.array([t.vertices[:] for t in me.loop_triangles], dtype=np.int64)
k = len(me.shape_keys.key_blocks) if me.shape_keys else 0
np.savez_compressed(out, V=V, F=T)
print("DUMPED %s %d verts %d tris %d keys -> %s" % (name, len(V), len(T), k, out))
