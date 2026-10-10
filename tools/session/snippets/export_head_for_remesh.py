"""STAGE A -- write his head, at REST, with the mouth region flagged.

PyMeshLab's isotropic remesher takes `selectedonly`, so the mouth region can be
rebuilt IN PLACE while the rest of his head is untouched and still attached. That
removes the whole extract-a-patch-and-stitch-it-back problem, which is where this
kind of repair usually goes wrong.

The flag rides in the PLY's `quality` field, which is the one per-vertex scalar
both sides agree on without a custom format.

REST POSITIONS, NOT THE EVALUATED MESH. Remeshing a posed mesh would bake the
pose into his rest shape and every one of the 88 shape keys would be measured
against the wrong basis.
"""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
OUT=os.path.join(ROOT,"renders/_remesh"); os.makedirs(OUT,exist_ok=True)
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
RADIUS=float(os.environ.get("TRIPPEDD_REMESH_RADIUS_MM","16"))
head=bpy.data.objects["MARS_MESH"]; me=head.data
W=np.array(head.matrix_world)
P=np.array([v.co[:] for v in me.vertices],float)
Pw=P@W[:3,:3].T+W[:3,3]
SEAM=np.vstack([np.array(MA["contours"]["lip_inner_upper"],float),
                np.array(MA["contours"]["lip_inner_lower"],float)])
d=np.array([float(np.linalg.norm(SEAM-q,axis=1).min()) for q in Pw])/MM
sel=(d<RADIUS).astype(np.float32)
tris=[]
for p in me.polygons:
    vs=list(p.vertices)
    for i in range(1,len(vs)-1): tris.append((vs[0],vs[i],vs[i+1]))
path=os.path.join(OUT,"head_rest.ply")
with open(path,"w") as f:
    f.write("ply\nformat ascii 1.0\n")
    f.write("comment MARS_MESH rest positions; quality=1 marks the mouth region\n")
    f.write("element vertex %d\n"%len(P))
    f.write("property float x\nproperty float y\nproperty float z\nproperty float quality\n")
    f.write("element face %d\nproperty list uchar int vertex_indices\nend_header\n"%len(tris))
    for i in range(len(P)):
        f.write("%.9f %.9f %.9f %.3f\n"%(P[i,0],P[i,1],P[i,2],sel[i]))
    for t in tris:
        f.write("3 %d %d %d\n"%t)
json.dump({"verts":int(len(P)),"tris":int(len(tris)),"selected":int(sel.sum()),
           "radiusMM":RADIUS,"mmPerUnit":MM,"ply":path,
           "shapeKeys":[k.name for k in me.shape_keys.key_blocks],
           "vertexGroups":[g.name for g in head.vertex_groups],
           "uvLayers":[l.name for l in me.uv_layers]},
          open(os.path.join(OUT,"head_rest.json"),"w"),indent=2)
print("wrote %s -- %d verts, %d tris, %d flagged within %.0f mm of his lip crease"
      %(path,len(P),len(tris),int(sel.sum()),RADIUS))
