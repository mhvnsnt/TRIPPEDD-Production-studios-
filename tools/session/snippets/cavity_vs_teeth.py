"""MESH blocks 485 of 800 crowns. Split that into HIS SKIN and the CARVED CAVITY
WALL -- they are the same object and the same question cannot answer both."""
import bpy, json, os, math
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0.0,-1.0,0.0))).normalized()
AP=(Vector(MA["aperture"]["cornerLeft"])+Vector(MA["aperture"]["cornerRight"]))/2.0
head=bpy.data.objects["MARS_MESH"]; arm=bpy.data.objects["MARS_RIG"]; scene=bpy.context.scene
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
for n in ("lip_lower_depress","lip_upper_raise","mouth_funnel"):
    kb=head.data.shape_keys.key_blocks.get(n)
    if kb: kb.value=1.0
pb=arm.pose.bones["jaw"]; pb.rotation_mode="XYZ"; pb.rotation_euler=(math.radians(30),0,0)
bpy.context.view_layer.update(); deps=bpy.context.evaluated_depsgraph_get()

eo=head.evaluated_get(deps); hm=eo.to_mesh(); HM=eo.matrix_world
poly_mat=[p.material_index for p in hm.polygons]
names=[m.name if m else "?" for m in head.data.materials]
# where does each material's surface sit, in depth?
for si,nmat in enumerate(names):
    vi=set()
    for p in hm.polygons:
        if p.material_index==si: vi.update(p.vertices)
    if not vi: continue
    P=np.array([list(FINV@(HM@hm.vertices[i].co)) for i in vi])/MM
    sel=(np.abs(P[:,0])<30)&(np.abs(P[:,2])<24)
    if sel.sum()<5: continue
    Q=P[sel]
    print("%-42s n=%-6d in the mouth box: depth y %+7.2f .. %+7.2f (5th pct %+6.2f)"
          %(nmat[:42],int(sel.sum()),Q[:,1].min(),Q[:,1].max(),np.percentile(Q[:,1],5)))
eo.to_mesh_clear()

eye=Vector(AP)+OUTW*1.2
c=Counter(); tot=0
for nm in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER"):
    ob=bpy.data.objects[nm]; e2=ob.evaluated_get(deps); m=e2.to_mesh(); M=e2.matrix_world
    P=[M@v.co.copy() for v in m.vertices]
    ti=set()
    for p in m.polygons:
        mt=ob.data.materials[p.material_index] if p.material_index<len(ob.data.materials) else None
        if mt and "TEETH" in mt.name.upper(): ti.update(p.vertices)
    e2.to_mesh_clear()
    L=np.array([list(FINV@p) for p in P])
    for i in sorted(ti,key=lambda j:L[j][1])[:400]:
        p=P[i]; d=p-eye; ln=d.length
        hit,lo,_n,fi,hob,_mm=scene.ray_cast(deps,eye,d/ln,distance=ln+0.5); tot+=1
        if not hit or (lo-p).length<=0.5*MM: c["VISIBLE"]+=1; continue
        if hob.original==head:
            mi=poly_mat[fi] if fi<len(poly_mat) else 0
            c["MESH/"+names[mi][:22]]+=1
        else: c[hob.name.replace("MARS_","")]+=1
print()
for k,v in c.most_common(8): print("   %-34s %4d  (%.0f%%)"%(k,v,100.0*v/tot))
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
pb.rotation_euler=(0,0,0); bpy.context.view_layer.update()
