"""HIS CORNER SKIN IS CAVED IN 38-52 mm. PUT IT BACK, FROM HIS OWN SCAN.

Traced every crossing of a rest ray:
    x -28   CAVITY@+38.2   <- nothing in front of it. No skin at all.
    x -24   CAVITY@+44.7
    x -18   CAVITY@+51.8
    x -15   skin@+0.3      <- his lip is right here
    x   0   skin@-4.9
    x +28   CAVITY@+39.2

So the corners are not a hole and not a protrusion: the head's own surface has
been pulled 38-52 mm INTO his face there by the carve. That is also why pushing
those vertices deeper changed the leak by nothing -- they were already deep, and
my repair moved them the wrong way.

THE AUTHORITY IS HIS UNCARVED SCAN, which still has that skin. Blender's own
SHRINKWRAP projects the caved-in vertices back onto it. His lips, his cheeks and
everything the carve did NOT damage are excluded by a vertex group, so only the
broken corners move.
"""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from collections import Counter
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
P=json.load(open(os.path.join(ROOT,"renders/_session/params.json")))
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
CORNER=float(P.get("cornerFromMM",16.0)); DEEP=float(P.get("deeperThanMM",12.0))
head=bpy.data.objects["MARS_MESH"]; me=head.data; arm=bpy.data.objects["MARS_RIG"]; sc=bpy.context.scene
if me.get("corner_skin_repaired"):
    print("the corner skin has already been repaired"); return
names=[m.name if m else "?" for m in me.materials]
ORAL=[i for i,n in enumerate(names) if "ORAL" in n.upper()]
W=head.matrix_world

def rest_leak():
    for k in me.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    arm.pose.bones["jaw"].rotation_euler=(0,0,0); bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    eo=head.evaluated_get(deps); hm=eo.to_mesh(); pm=[p.material_index for p in hm.polygons]; eo.to_mesh_clear()
    c=Counter()
    for xx in np.arange(-30,30.01,0.4):
        for zz in np.arange(-14,12.01,0.4):
            p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
            hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
            if not hit: continue
            n=ob.original.name
            oral = n in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE","MARS_MOUTH_SOCK")
            if n=="MARS_MESH":
                mi=pm[fi] if fi<len(pm) else 0
                oral = mi in ORAL
            if oral: c["corner" if abs(xx)>CORNER else "middle"]+=1
    return c

# ---- his uncarved scan, as the authority
src=os.path.join(ROOT,"assets/source_models/MARS_LOD2.glb")
if not os.path.exists(src):
    print("*** REFUSED: %s is missing -- his uncarved scan is the only authority for "
          "what that skin looked like"%src); return
pre={o.name for o in bpy.data.objects}
bpy.ops.import_scene.gltf(filepath=src)
newo=[o for o in bpy.data.objects if o.name not in pre and o.type=="MESH"]
if not newo:
    print("*** REFUSED: the scan imported no mesh"); return
scan=newo[0]
if len(newo)>1:
    bpy.ops.object.select_all(action="DESELECT")
    for o in newo: o.select_set(True)
    bpy.context.view_layer.objects.active=newo[0]; bpy.ops.object.join(); scan=bpy.context.view_layer.objects.active
scan.name="MARS_SCAN_REF"; scan.hide_render=True
print("uncarved scan: %d verts"%len(scan.data.vertices))

# ---- which vertices are the caved-in corners
cand=[]
for i,v in enumerate(me.vertices):
    l=FINV@(W@v.co)
    if abs(l.x)/MM>CORNER and l.y/MM>DEEP: cand.append(i)
print("caved-in corner vertices (|x| > %.0f mm and deeper than %.0f mm): %d"
      %(CORNER,DEEP,len(cand)))
if len(cand)<10:
    bpy.data.objects.remove(scan); print("nothing to repair"); return

before=rest_leak()
print("before: rest leak corner %d, middle %d"%(before["corner"],before["middle"]))

g=head.vertex_groups.get("CORNER_REPAIR") or head.vertex_groups.new(name="CORNER_REPAIR")
for i in cand: g.add([i],1.0,"REPLACE")
md=head.modifiers.new("CORNER_SHRINKWRAP","SHRINKWRAP")
md.target=scan; md.wrap_method="NEAREST_SURFACEPOINT"
md.vertex_group=g.name
# SHRINKWRAP CANNOT BE APPLIED ON A MESH WITH SHAPE KEYS, so the result is read
# off the evaluated mesh and written into the vertices by hand.
bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
eo=head.evaluated_get(deps); em=eo.to_mesh()
newco={i:em.vertices[i].co.copy() for i in cand}
eo.to_mesh_clear()
head.modifiers.remove(md)
moved=0; worst=0.0
B=me.shape_keys.key_blocks["Basis"].data
for i in cand:
    d=(newco[i]-me.vertices[i].co).length/MM
    if d<1e-6: continue
    delta=newco[i]-me.vertices[i].co
    me.vertices[i].co=newco[i]
    for k in me.shape_keys.key_blocks:      # carry the move into every key
        k.data[i].co=k.data[i].co+delta
    moved+=1; worst=max(worst,d)
me.update(); bpy.context.view_layer.update()
print("projected %d corner vertices back onto his scan, worst move %.2f mm"%(moved,worst))
after=rest_leak()
print("after:  rest leak corner %d, middle %d"%(after["corner"],after["middle"]))
bpy.data.objects.remove(scan)
if after["corner"]>=before["corner"]:
    print("*** REFUSED: the corner leak did not fall (%d -> %d)"%(before["corner"],after["corner"]))
    return
me["corner_skin_repaired"]=moved
out=(bpy.data.filepath or os.path.join(ROOT,"assets/rigs/MARS_FACE.blend"))
# SAVE THE BLEND THIS SESSION ACTUALLY HAS OPEN, not a hardcoded canonical
# path. Run against a REVIEW blend on a second session port, these snippets
# each wrote their result straight over assets/rigs/MARS_FACE.blend -- an
# unreviewed promotion nobody asked for, and the same way the good mouth was
# lost under the eye work. A repair belongs to the file it was run on.
bpy.ops.wm.save_as_mainfile(filepath=out)
print("corner leak %d -> %d, middle %d -> %d; saved -> %s"
      %(before["corner"],after["corner"],before["middle"],after["middle"],out))
