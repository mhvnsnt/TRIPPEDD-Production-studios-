"""He can see a pink ring hanging in front of the top teeth. Name it -- object AND
material, per ray, over the mouth opening, with the depth each one sits at."""
import bpy, json, os, math
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
for n in ("lip_lower_depress","lip_upper_raise","mouth_funnel"):
    kb=head.data.shape_keys.key_blocks.get(n)
    if kb: kb.value=1.0
pb=arm.pose.bones["jaw"]; pb.rotation_mode="XYZ"; pb.rotation_euler=(math.radians(30),0,0)
bpy.context.view_layer.update(); deps=bpy.context.evaluated_depsgraph_get()
polymat={}; matnames={}
for ob in bpy.data.objects:
    if ob.type!="MESH": continue
    eo=ob.evaluated_get(deps); m=eo.to_mesh()
    polymat[ob.name]=[p.material_index for p in m.polygons]
    eo.to_mesh_clear()
    matnames[ob.name]=[mm.name if mm else "?" for mm in ob.data.materials]
def what(xx,zz):
    p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
    hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
    if not hit: return None,None,None
    nmo=ob.name.replace("MARS_","")
    mats=matnames.get(ob.name,[]); pm=polymat.get(ob.name,[])
    mi=pm[fi] if fi<len(pm) else 0
    mat=mats[mi].replace("MARS_","") if mi<len(mats) else "?"
    return nmo,mat,(FINV@lo).y/MM
print("what the camera meets, row by row down his open mouth (x across, z down):")
print("      " + "".join("%9.0f"%x for x in range(-20,21,5)))
for zz in range(12,-17,-2):
    row=[]
    for xx in range(-20,21,5):
        o,m,d=what(xx,zz)
        row.append("%9s"%("-" if o is None else (m[:8] if o in("MESH",) else o[:8])))
    print("z%+4d "%zz+"".join(row))
print()
print("and the DEPTH each one sits at (mm into his mouth):")
print("      " + "".join("%9.0f"%x for x in range(-20,21,5)))
for zz in range(12,-17,-2):
    row=[]
    for xx in range(-20,21,5):
        o,m,d=what(xx,zz)
        row.append("%9s"%("-" if d is None else "%.1f"%d))
    print("z%+4d "%zz+"".join(row))
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
pb.rotation_euler=(0,0,0); bpy.context.view_layer.update()
