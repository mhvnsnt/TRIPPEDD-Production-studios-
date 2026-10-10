"""Two candidate fixes for the sock clipping his crowns, A/B'd in one call.
Nothing is saved -- the session is restored to where it started."""
import bpy, json, os, math
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
ROOT = os.environ.get("TRIPPEDD_ROOT", "/home/user/TRIPPEDD-Production-studios-")
MA = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = float(MA["aperture"]["width"]); MM = MW/50.0
FRAME = Matrix(MA["frame"]["matrix"]); FINV = FRAME.inverted()
OUTW = (FRAME.to_3x3() @ Vector((0.0,-1.0,0.0))).normalized()
AP = (Vector(MA["aperture"]["cornerLeft"])+Vector(MA["aperture"]["cornerRight"]))/2.0
head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
sock = bpy.data.objects["MARS_MOUTH_SOCK"]
scene = bpy.context.scene

def pose_open():
    for k in head.data.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    for n in ("lip_lower_depress","lip_upper_raise","mouth_funnel"):
        kb=head.data.shape_keys.key_blocks.get(n)
        if kb: kb.value=1.0
    pb=arm.pose.bones["jaw"]; pb.rotation_mode="XYZ"; pb.rotation_euler=(math.radians(30),0,0)
    bpy.context.view_layer.update()

def crowns_visible():
    deps=bpy.context.evaluated_depsgraph_get()
    eye=Vector(AP)+OUTW*1.2
    tot=0; vis=0; blockers=Counter()
    for nm in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER"):
        ob=bpy.data.objects[nm]; eo=ob.evaluated_get(deps); m=eo.to_mesh(); M=eo.matrix_world
        P=[M@v.co.copy() for v in m.vertices]
        ti=set()
        for p in m.polygons:
            mt=ob.data.materials[p.material_index] if p.material_index<len(ob.data.materials) else None
            if mt and "TEETH" in mt.name.upper(): ti.update(p.vertices)
        eo.to_mesh_clear()
        L=np.array([list(FINV@p) for p in P])
        cand=sorted(ti,key=lambda i:L[i][1])[:400]
        for i in cand:
            p=P[i]; d=p-eye; ln=d.length
            hit,lo,_n,fi,hob,_mm=scene.ray_cast(deps,eye,d/ln,distance=ln+0.5)
            tot+=1
            if not hit or (lo-p).length<=0.5*MM: vis+=1
            else: blockers[hob.name.replace("MARS_","")]+=1
    return vis,tot,blockers

pose_open()
orig_loc = sock.location.copy(); orig_hide = sock.hide_render
base = crowns_visible()
print("as-is                      %d / %d crowns visible   blocked: %s"
      % (base[0],base[1],dict(base[2].most_common(4))))

sock.hide_render=True
sock.hide_viewport=True
bpy.context.view_layer.update()
r=crowns_visible()
print("sock hidden                %d / %d crowns visible   blocked: %s"
      % (r[0],r[1],dict(r[2].most_common(4))))
sock.hide_render=orig_hide; sock.hide_viewport=False; bpy.context.view_layer.update()

for mm_back in (2.0,4.0,6.0):
    sock.location = orig_loc + (FRAME.to_3x3() @ Vector((0,1,0))).normalized()*(mm_back*MM)
    bpy.context.view_layer.update()
    r=crowns_visible()
    print("sock pushed back %4.1f mm   %d / %d crowns visible   blocked: %s"
          % (mm_back,r[0],r[1],dict(r[2].most_common(4))))
sock.location = orig_loc
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
arm.pose.bones["jaw"].rotation_euler=(0,0,0)
bpy.context.view_layer.update()
print("session restored")
