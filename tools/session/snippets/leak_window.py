"""MY OWN LEAK NUMBER DEPENDS ON THE WINDOW I SAMPLED. Pin it down.

One snippet reported 981 leaking rays at rest; another, minutes later on the same
rig, reported 5. The only difference was the vertical band sampled. A metric that
changes by 200x with the window is not measuring his mouth -- it is measuring how
far above and below his mouth I chose to look, where a ray enters at a grazing
angle and finds the cavity from outside the lip line entirely.
"""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
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
def scan(zlo,zhi,step=0.3):
    c=Counter(); tot=0
    for xx in np.arange(-30,30.01,step):
        for zz in np.arange(zlo,zhi+0.001,step):
            p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9; tot+=1
            hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
            if not hit: continue
            n=ob.original.name
            oral = n in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE","MARS_MOUTH_SOCK")
            if n=="MARS_MESH":
                mi=pm[fi] if fi<len(pm) else 0
                oral = mi in ORAL
            if oral: c["corner" if abs(xx)>16 else "middle"]+=1
    return c,tot
for zlo,zhi in ((-20,16),(-14,12),(-10,8),(-6,6),(-4,4)):
    c,tot=scan(zlo,zhi)
    print("  z %+4.0f..%+4.0f  %6d rays  ->  corner %5d  middle %4d   (%.2f%% of the window)"
          %(zlo,zhi,tot,c["corner"],c["middle"],100.0*sum(c.values())/tot))
