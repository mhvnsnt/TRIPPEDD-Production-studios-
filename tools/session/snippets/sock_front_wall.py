"""THE SOCK HAS A FRONT WALL AND IT SHOULD NOT.

Owner: "there's this pink circular ring that's hanging down in front of the top
teeth ... it's all fighting each other." He is describing MARS_MOUTH_SOCK, and
the ray table says so: from z +2 down to z -12 it is the FIRST thing the camera
meets right across his mouth, at 0.4-15 mm depth, in front of his teeth and his
tongue.

A vestibule lining lines the inside of his lips and cheeks. It does not have a
wall across the mouth opening. So measure which of its faces are that wall --
the ones a ray from outside reaches before anything else -- and see what the
mouth looks like without them.
"""
import bpy, bmesh, json, os, math
import numpy as np
from mathutils import Vector, Matrix
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
AP=(Vector(MA["aperture"]["cornerLeft"])+Vector(MA["aperture"]["cornerRight"]))/2.0
head=bpy.data.objects["MARS_MESH"]; arm=bpy.data.objects["MARS_RIG"]
sock=bpy.data.objects["MARS_MOUTH_SOCK"]; sc=bpy.context.scene
def open_pose():
    for k in head.data.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    for n in ("lip_lower_depress","lip_upper_raise","mouth_funnel"):
        kb=head.data.shape_keys.key_blocks.get(n)
        if kb: kb.value=1.0
    pb=arm.pose.bones["jaw"]; pb.rotation_mode="XYZ"; pb.rotation_euler=(math.radians(30),0,0)
    bpy.context.view_layer.update()
open_pose()
deps=bpy.context.evaluated_depsgraph_get()
# which SOCK faces does a ray from outside hit FIRST? those are the front wall.
front=set(); tot=0; sockhits=0
for xx in np.arange(-30,30.01,0.4):
    for zz in np.arange(-24,20.01,0.4):
        p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
        hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8); tot+=1
        if hit and ob.original==sock:
            front.add(int(fi)); sockhits+=1
print("rays over his mouth: %d;  the sock is the FIRST thing met by %d of them (%.1f%%)"
      %(tot,sockhits,100.0*sockhits/tot))
print("distinct sock faces forming that front wall: %d of %d"%(len(front),len(sock.data.polygons)))
L=[]
for fi in front:
    if fi<len(sock.data.polygons):
        c=sock.matrix_world@sock.data.polygons[fi].center
        L.append(list(FINV@c))
if L:
    L=np.array(L)/MM
    print("  they sit at depth y %+.2f .. %+.2f mm, x %+.1f..%+.1f, z %+.1f..%+.1f"
          %(L[:,1].min(),L[:,1].max(),L[:,0].min(),L[:,0].max(),L[:,2].min(),L[:,2].max()))
json.dump(sorted(front), open(os.path.join(ROOT,"renders/_oral_contact/sock_front_faces.json"),"w"))
print("face list -> renders/_oral_contact/sock_front_faces.json")
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
arm.pose.bones["jaw"].rotation_euler=(0,0,0); bpy.context.view_layer.update()
