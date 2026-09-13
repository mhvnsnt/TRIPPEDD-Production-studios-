"""His lips must MEET at rest, with at most a slight parting in the MIDDLE.
721 rays leak beyond x -15 mm and 203 beyond +15 mm. Cross-section the corners."""
import bpy, bmesh, json, os
import numpy as np
from mathutils import Vector, Matrix
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
head=bpy.data.objects["MARS_MESH"]; arm=bpy.data.objects["MARS_RIG"]; sc=bpy.context.scene
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
arm.pose.bones["jaw"].rotation_euler=(0,0,0); bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
names=[m.name if m else "?" for m in head.data.materials]
eo=head.evaluated_get(deps); hm=eo.to_mesh(); pm=[p.material_index for p in hm.polygons]; eo.to_mesh_clear()
print("REST cross-section -- first surface met, by lateral position:")
for xx in (-28,-26,-24,-22,-20,-18,-15,-10,-5,0,5,10,15,20,24,28):
    row=[]
    for zz in (2.0,1.0,0.0,-1.0,-2.0):
        p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
        hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
        if not hit: row.append("  --  "); continue
        n=ob.original.name.replace("MARS_","")
        if n=="MESH":
            mi=pm[fi] if fi<len(pm) else 0
            n="CAVITY" if "ORAL" in names[mi].upper() else "skin"
        row.append("%6s"%n[:6])
    print("  x %+4d  "%xx+"".join(row))
# BOUNDARY EDGES -- a split leaves a real open edge; a hole in his lip line is one
bm=bmesh.new(); bm.from_mesh(head.data)
bnd=[e for e in bm.edges if len(e.link_faces)==1]
W=head.matrix_world
L=np.array([list(FINV@(W@v.co)) for e in bnd for v in e.verts])/MM if bnd else np.zeros((0,3))
print("\nMARS_MESH boundary (open) edges: %d"%len(bnd))
if len(L):
    near=(np.abs(L[:,2])<12)&(np.abs(L[:,0])<35)
    print("  near his lip line: %d edge-ends, x %+.1f..%+.1f mm"
          %(int(near.sum()),L[near,0].min() if near.any() else 0,L[near,0].max() if near.any() else 0))
    for lo_,hi_ in ((-35,-20),(-20,-10),(-10,10),(10,20),(20,35)):
        n=int((near&(L[:,0]>=lo_)&(L[:,0]<hi_)).sum())
        if n: print("    x %+4d..%+4d : %d"%(lo_,hi_,n))
bm.free()
