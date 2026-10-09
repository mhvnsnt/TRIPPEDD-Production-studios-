"""Is the commissure a HOLE, a FUNNEL, or a gap between sparse faces?

Projecting his own scan's skin onto the vertices that are there did not close it,
so the vertices are not the problem. Three possibilities remain and one map tells
them apart: for every (x,z) over the corner, find the SHALLOWEST MARS_MESH
crossing. If nothing shallow exists, his exterior genuinely stops there.
"""
import bpy, bmesh, json, os
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
eo=head.evaluated_get(deps); hm=eo.to_mesh(); pm=[p.material_index for p in hm.polygons]; eo.to_mesh_clear()
print("shallowest MARS_MESH crossing, mm into his face  (s = skin material, c = cavity):")
hdr="       "+"".join("%8.0f"%x for x in range(-30,31,5))
print(hdr)
for zz in (6,4,2,0,-2,-4,-6):
    row=[]
    for xx in range(-30,31,5):
        p=FRAME@Vector((xx*MM,0.0,zz*MM)); cur=p+OUTW*0.9; best=None; bestm=None
        for _ in range(8):
            hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,cur,-OUTW,distance=2.0)
            if not hit: break
            if ob.original==head:
                d=(FINV@lo).y/MM
                if best is None or d<best:
                    best=d; bestm="c" if (pm[fi] if fi<len(pm) else 0) in ORAL else "s"
            cur=lo+(-OUTW)*1e-4
        row.append("%8s"%("--" if best is None else "%+.0f%s"%(best,bestm)))
    print("  z%+3d "%zz+"".join(row))
# and is there a boundary loop out there?
bm=bmesh.new(); bm.from_mesh(me); W=head.matrix_world
bnd=[e for e in bm.edges if len(e.link_faces)==1]
pts=np.array([list(FINV@(W@v.co)) for e in bnd for v in e.verts])/MM if bnd else np.zeros((0,3))
print("\nboundary (single-face) edges on MARS_MESH: %d"%len(bnd))
if len(pts):
    far=(np.abs(pts[:,0])>16)&(np.abs(pts[:,2])<10)
    print("  of those, out at the commissures (|x|>16, |z|<10): %d edge-ends"%int(far.sum()))
inv=0
for p in me.polygons:
    c=W@p.center; n=(W.to_3x3()@p.normal)
    if abs((FINV@c).x)/MM>16 and abs((FINV@c).z)/MM<8 and (FINV@c).y/MM<12:
        if n.dot(OUTW)<0: inv+=1
print("  faces near the commissure lip plane whose normal points INTO his head: %d"%inv)
bm.free()
