"""Where does his mouth leak at REST? 7 of 8 checks pass; the one failure is
cavity 1.9% + tongue 0.1% of the mouth area with every control at zero."""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
head=bpy.data.objects["MARS_MESH"]; arm=bpy.data.objects["MARS_RIG"]; sc=bpy.context.scene
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
arm.pose.bones["jaw"].rotation_euler=(0,0,0)
bpy.context.view_layer.update(); deps=bpy.context.evaluated_depsgraph_get()
names=[m.name if m else "?" for m in head.data.materials]
eo=head.evaluated_get(deps); hm=eo.to_mesh(); polymat=[p.material_index for p in hm.polygons]; eo.to_mesh_clear()
leaks=[]; c=Counter()
for xx in np.arange(-30,30.01,0.3):
    for zz in np.arange(-20,16.01,0.3):
        p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
        hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
        if not hit: continue
        nm=ob.original.name
        if nm=="MARS_MESH":
            mi=polymat[fi] if fi<len(polymat) else 0
            if "ORAL" in names[mi].upper(): c["cavity wall"]+=1; leaks.append((xx,zz))
        elif nm in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE","MARS_MOUTH_SOCK"):
            c[nm.replace("MARS_","")]+=1; leaks.append((xx,zz))
print("at REST, rays reaching something oral:", dict(c))
if leaks:
    L=np.array(leaks)
    print("  they are at x %+.1f..%+.1f mm, z %+.1f..%+.1f mm"%(L[:,0].min(),L[:,0].max(),L[:,1].min(),L[:,1].max()))
    for lo_,hi_ in ((-30,-15),(-15,-5),(-5,5),(5,15),(15,30)):
        n=int(((L[:,0]>=lo_)&(L[:,0]<hi_)).sum())
        if n: print("    x %+4d..%+4d mm : %d rays"%(lo_,hi_,n))
