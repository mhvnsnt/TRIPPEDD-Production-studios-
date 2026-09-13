"""Render the mouth from the live session AND publish it as evidence, in one call.
The publication is not something anyone has to remember: it happens here."""
import bpy, json, os, math, subprocess, hashlib
from mathutils import Vector, Matrix
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
# PARAMETERS COME THROUGH A FILE, NOT THE ENVIRONMENT. The session is a
# long-lived process started once; environment variables set by a client call
# never reach it, so the first run of this silently published under the default
# label. A file is read at call time and cannot go stale that way.
_pp=os.path.join(ROOT,"renders/_session/params.json")
_P=json.load(open(_pp)) if os.path.exists(_pp) else {}
TAG=_P.get("tag","mouth"); SET=_P.get("set","mars/mouth")
NOTE=_P.get("note",""); STATUS=_P.get("status","PENDING")
OUT=os.path.join(ROOT,"renders/_session"); os.makedirs(OUT,exist_ok=True)
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
p=os.path.join(OUT,"%s.png"%TAG); sc.render.filepath=p
bpy.ops.render.render(write_still=True)
for k in head.data.shape_keys.key_blocks:
    if k.name!="Basis": k.value=0.0
pb.rotation_euler=(0,0,0); bpy.context.view_layer.update()
shown=[o.name for o in bpy.data.objects if o.type=="MESH" and not o.hide_render]
hidden=[o.name for o in bpy.data.objects if o.type=="MESH" and o.hide_render]
r=subprocess.run([os.path.join(ROOT,".trippedd_venv/bin/python"),
    os.path.join(ROOT,"tools/publish_visual.py"),
    "--src",p,"--set",SET,"--label",TAG,
    "--source-blend",os.path.relpath(bpy.data.filepath,ROOT) if bpy.data.filepath.startswith(ROOT) else bpy.data.filepath,
    "--tool","tools/session/snippets/render_and_publish.py",
    "--status",STATUS,"--note",NOTE,
    "--camera","orthographic, out of his face (+fwd), ortho_scale=MW*2.6, jaw 30 + lip keys",
    "--view-transform",sc.view_settings.view_transform,
    "--blender",bpy.app.version_string,
    "--shown",",".join(shown),"--hidden",",".join(hidden)],
    capture_output=True,text=True)
print(r.stdout.strip() or r.stderr.strip())
