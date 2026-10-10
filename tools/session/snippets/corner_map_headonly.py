"""Shallowest head-surface crossing across the commissures, on a head with no rig.
Works on any carved head, so a narrower carve can be judged before anything is built
on top of it."""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
head=bpy.data.objects.get("MARS_MESH") or [o for o in bpy.data.objects if o.type=="MESH"][0]
me=head.data; sc=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
names=[m.name if m else "?" for m in me.materials]
ORAL=[i for i,n in enumerate(names) if "ORAL" in n.upper()]
pm=[p.material_index for p in me.polygons]
print("%s: %d verts, materials %s"%(head.name,len(me.vertices),names))
print("shallowest crossing, mm into his face (s = skin, c = cavity):")
print("       "+"".join("%8.0f"%x for x in range(-30,31,5)))
bad=0; tot=0
for zz in (4,2,0,-2,-4):
    row=[]
    for xx in range(-30,31,5):
        p=FRAME@Vector((xx*MM,0.0,zz*MM)); cur=p+OUTW*0.9; best=None; bm_=None
        for _ in range(8):
            hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,cur,-OUTW,distance=2.0)
            if not hit: break
            if ob.original==head:
                d=(FINV@lo).y/MM
                if best is None or d<best:
                    best=d; bm_="c" if (pm[fi] if fi<len(pm) else 0) in ORAL else "s"
            cur=lo+(-OUTW)*1e-4
        tot+=1
        if best is not None and bm_=="c" and best>15: bad+=1
        row.append("%8s"%("--" if best is None else "%+.0f%s"%(best,bm_)))
    print("  z%+3d "%zz+"".join(row))
print("\ncells where the nearest surface is CAVITY deeper than 15 mm (his skin missing): %d of %d"%(bad,tot))
