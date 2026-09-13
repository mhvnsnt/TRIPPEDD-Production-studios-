"""HIS MOUTH LEAKS AT THE CORNERS AT REST, AND IT IS THE SOCK POKING PAST THEM.

mouth_proof scores the canonical rig 7 of 8 against yesterday's own gate, beating
it on every anatomy check (teeth 4.8 -> 8.7%, tongue 7.8 -> 8.4%, cavity
28.3 -> 28.5%). The single failure is REST: cavity 1.9% + tongue 0.1% where it
should be under 1%.

Measured where: of the rays that reach something oral with every control at zero,
721 are beyond x -15 mm and 203 beyond x +15 mm -- the CORNERS -- against about
57 across the whole centre. And what they reach is MOUTH_SOCK, 706 of them.

His aperture corners are at +/- 25 mm (MW = 50 mm). The sock spans -33.9 to
+33.2 mm, so it sticks out past the corners of his own mouth on both sides and
shows through the lip line at rest. Trim it back inside them.
"""
import bpy, bmesh, json, os, math
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
head=bpy.data.objects["MARS_MESH"]; arm=bpy.data.objects["MARS_RIG"]
sock=bpy.data.objects["MARS_MOUTH_SOCK"]; sc=bpy.context.scene
if sock.get("corners_trimmed"):
    print("the sock corners are already trimmed"); return
CL=FINV@Vector(MA["aperture"]["cornerLeft"]); CR=FINV@Vector(MA["aperture"]["cornerRight"])
HALF=max(abs(CL.x),abs(CR.x))/MM
MARGIN=float(json.load(open(os.path.join(ROOT,"renders/_session/params.json"))).get("marginMM",1.0)) \
       if os.path.exists(os.path.join(ROOT,"renders/_session/params.json")) else 1.0
LIMIT=HALF-MARGIN
print("his aperture half-width is %.2f mm; trimming sock faces beyond %.2f mm"%(HALF,LIMIT))

def oral_at_rest():
    for k in head.data.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    arm.pose.bones["jaw"].rotation_euler=(0,0,0)
    bpy.context.view_layer.update(); deps=bpy.context.evaluated_depsgraph_get()
    c=Counter(); tot=0
    for xx in np.arange(-30,30.01,0.3):
        for zz in np.arange(-20,16.01,0.3):
            p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9; tot+=1
            hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
            if hit and ob.original.name in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER",
                                            "MARS_TONGUE","MARS_MOUTH_SOCK"):
                c[ob.original.name.replace("MARS_","")]+=1
    return sum(c.values()),tot,c

def anatomy_when_open():
    for k in head.data.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    for n in ("lip_lower_depress","lip_upper_raise","mouth_funnel"):
        kb=head.data.shape_keys.key_blocks.get(n)
        if kb: kb.value=1.0
    pb=arm.pose.bones["jaw"]; pb.rotation_mode="XYZ"; pb.rotation_euler=(math.radians(30),0,0)
    bpy.context.view_layer.update(); deps=bpy.context.evaluated_depsgraph_get()
    n=0
    for xx in np.arange(-26,26.01,0.4):
        for zz in np.arange(-20,16.01,0.4):
            p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
            hit,lo,_n2,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
            if hit and ob.original.name in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE"):
                n+=1
    pb.rotation_euler=(0,0,0)
    for k in head.data.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    bpy.context.view_layer.update()
    return n

r0=oral_at_rest(); a0=anatomy_when_open()
print("before: %d of %d rays reach something oral at REST %s; %d reach teeth/tongue when OPEN"
      %(r0[0],r0[1],dict(r0[2]),a0))

drop=[]
for p in sock.data.polygons:
    c=FINV@(sock.matrix_world@p.center)
    if abs(c.x)/MM > LIMIT: drop.append(p.index)
print("sock faces beyond his lip corners: %d of %d"%(len(drop),len(sock.data.polygons)))
if not drop:
    print("nothing to trim"); return
bm=bmesh.new(); bm.from_mesh(sock.data); bm.faces.ensure_lookup_table()
bmesh.ops.delete(bm,geom=[bm.faces[i] for i in drop if i<len(bm.faces)],context="FACES_ONLY")
bm.to_mesh(sock.data); bm.free(); sock.data.update(); bpy.context.view_layer.update()
r1=oral_at_rest(); a1=anatomy_when_open()
print("after:  %d of %d rays reach something oral at REST %s; %d reach teeth/tongue when OPEN"
      %(r1[0],r1[1],dict(r1[2]),a1))
if r1[0]>=r0[0]:
    print("*** REFUSED: the trim did not reduce the REST leak (%d -> %d)"%(r0[0],r1[0])); return
if a1 < a0*0.95:
    print("*** REFUSED: it cost %d of %d teeth/tongue rays when his mouth is OPEN"%(a0-a1,a0)); return
sock["corners_trimmed"]=len(drop)
out=(bpy.data.filepath or os.path.join(ROOT,"assets/rigs/MARS_FACE.blend"))
# SAVE THE BLEND THIS SESSION ACTUALLY HAS OPEN, not a hardcoded canonical
# path. Run against a REVIEW blend on a second session port, these snippets
# each wrote their result straight over assets/rigs/MARS_FACE.blend -- an
# unreviewed promotion nobody asked for, and the same way the good mouth was
# lost under the eye work. A repair belongs to the file it was run on.
bpy.ops.wm.save_as_mainfile(filepath=out)
print("trimmed %d faces; REST leak %d -> %d rays; saved -> %s"%(len(drop),r0[0],r1[0],out))
