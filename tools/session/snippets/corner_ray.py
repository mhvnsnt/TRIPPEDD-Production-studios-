"""One corner ray, every crossing, named. Stop circling and look at it."""
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
eo=head.evaluated_get(deps); hm=eo.to_mesh(); pm=[p.material_index for p in hm.polygons]; eo.to_mesh_clear()
def label(ob,fi):
    n=ob.original.name.replace("MARS_","")
    if n=="MESH":
        mi=pm[fi] if fi<len(pm) else 0
        return "CAVITY" if "ORAL" in names[mi].upper() else "skin"
    return n
for xx,zz in ((-28,0.0),(-24,0.0),(-20,0.0),(-18,0.0),(-15,0.0),(0,0.0),(+24,-1.0),(+28,-1.0)):
    p=FRAME@Vector((xx*MM,0.0,zz*MM)); cur=p+OUTW*0.9; parts=[]
    for _ in range(8):
        hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,cur,-OUTW,distance=2.0)
        if not hit: break
        parts.append("%s@%+.1f"%(label(ob,fi),(FINV@lo).y/MM))
        cur=lo+(-OUTW)*1e-4
    print("  x %+4d z %+4.1f : %s"%(xx,zz," -> ".join(parts) if parts else "MISS"))
