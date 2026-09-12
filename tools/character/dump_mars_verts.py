"""Dump the rigged head's vertex positions so the face donor can correspond to them."""
import bpy, sys, os
import numpy as np
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_FACE.blend"))
OUT = os.path.abspath(opt("--out", "assets/donor/gnm_face/_mars_verts.npy"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects["MARS_MESH"]
np.save(OUT, np.array([tuple(head.matrix_world @ v.co) for v in head.data.vertices], np.float64))
print("dumped %d vertices -> %s" % (len(head.data.vertices), OUT))
