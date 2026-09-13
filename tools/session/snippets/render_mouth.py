"""A LEVEL 1 diagnostic render, in the live session. No launch."""
import bpy, json, os, math
from mathutils import Vector, Matrix
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
TAG=os.environ.get("TRIPPEDD_RENDER_TAG","session")
OUT=os.path.join(ROOT,"renders/_oral_contact"); os.makedirs(OUT,exist_ok=True)
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"])
FRAME=Matrix(MA["frame"]["matrix"])
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized(); UPW=(FRAME.to_3x3()@Vector((0,0,1))).normalized()
AP=(Vector(MA["aperture"]["cornerLeft"])+Vector(MA["aperture"]["cornerRight"]))/2.0
sc=bpy.context.scene
cam=bpy.data.objects.get("MOUTHCAM")
if cam is None:
    cd=bpy.data.cameras.new("MOUTHCAM"); cam=bpy.data.objects.new("MOUTHCAM",cd); sc.collection.objects.link(cam)
cam.data.type="ORTHO"; cam.data.ortho_scale=MW*2.6; cam.location=AP+OUTW*0.9
z=OUTW; x=UPW.cross(z).normalized(); y=z.cross(x)
cam.matrix_world=Matrix(((x.x,y.x,z.x,cam.location.x),(x.y,y.y,z.y,cam.location.y),
                         (x.z,y.z,z.z,cam.location.z),(0,0,0,1)))
sc.camera=cam
sc.render.engine="BLENDER_EEVEE_NEXT"; sc.render.resolution_x=sc.render.resolution_y=700
if sc.world is None: sc.world=bpy.data.worlds.new("W")
sc.world.use_nodes=True
sc.world.node_tree.nodes["Background"].inputs[0].default_value=(0.05,0.05,0.06,1)
if bpy.data.objects.get("KEYLIGHT") is None:
    ld=bpy.data.lights.new("KEYLIGHT","AREA"); ld.energy=120; ld.size=0.6
    lo=bpy.data.objects.new("KEYLIGHT",ld); sc.collection.objects.link(lo)
    lo.location=AP+OUTW*0.55+UPW*0.12; lo.rotation_euler=cam.rotation_euler
head=bpy.data.objects["MARS_MESH"]; arm=bpy.data.objects["MARS_RIG"]
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
for n in ("lip_lower_depress","lip_upper_raise","mouth_funnel"):
    kb=head.data.shape_keys.key_blocks.get(n)
    if kb: kb.value=1.0
pb=arm.pose.bones["jaw"]; pb.rotation_mode="XYZ"; pb.rotation_euler=(math.radians(30),0,0)
bpy.context.view_layer.update()
sc.render.filepath=os.path.join(OUT,"%s_open.png"%TAG)
bpy.ops.render.render(write_still=True)
print("wrote %s"%sc.render.filepath)
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
pb.rotation_euler=(0,0,0); bpy.context.view_layer.update()
