"""Is the corner a HOLE, or is it his exterior wearing the cavity material?

Pushing the corner cavity vertices 14.72 mm deeper changed the rest leak by
NOTHING (981 -> 981), which rules out a protruding wall. The other possibility is
that those ORAL_MAT faces ARE his outer surface at the commissure -- carved and
then labelled as cavity -- in which case there is no hole to close and the fix is
a material, not geometry.

The test: for each corner oral face, fire a ray at it from outside and see whether
ANY skin is met first. Nothing in front of it means it IS the exterior.
"""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
head=bpy.data.objects["MARS_MESH"]; me=head.data; arm=bpy.data.objects["MARS_RIG"]; sc=bpy.context.scene
for k in me.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
arm.pose.bones["jaw"].rotation_euler=(0,0,0); bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
names=[m.name if m else "?" for m in me.materials]
ORAL=[i for i,n in enumerate(names) if "ORAL" in n.upper()]
W=head.matrix_world
CORNER=16.0
exterior=[]; buried=[]
for p in me.polygons:
    if p.material_index not in ORAL: continue
    c=W@p.center
    lc=FINV@c
    if abs(lc.x)/MM <= CORNER: continue
    o=c+OUTW*0.35
    hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=0.7)
    if not hit: exterior.append(p.index); continue
    # did we land on this very face (nothing in front), or on skin first?
    if (lo-c).length < 1.5*MM and ob.original==head and fi<len(me.polygons) \
       and me.polygons[fi].material_index in ORAL:
        exterior.append(p.index)
    else:
        buried.append(p.index)
print("corner oral faces (|x| > %.0f mm): %d exterior (nothing in front of them), %d behind skin"
      %(CORNER,len(exterior),len(buried)))
if exterior:
    L=np.array([list(FINV@(W@me.polygons[i].center)) for i in exterior])/MM
    print("  the exterior ones sit at x %+.1f..%+.1f, z %+.1f..%+.1f, depth y %+.1f..%+.1f mm"
          %(L[:,0].min(),L[:,0].max(),L[:,2].min(),L[:,2].max(),L[:,1].min(),L[:,1].max()))
    left=int((L[:,0]<0).sum()); right=int((L[:,0]>0).sum())
    print("  his right corner %d faces, his left corner %d"%(left,right))
json.dump({"exterior":exterior,"buried":buried},
          open(os.path.join(ROOT,"renders/_oral_contact/corner_faces.json"),"w"))
