"""FILL THE COMMISSURE HOLES. NO VERTEX MOVES.

Four bounded repairs that MOVED vertices were all refused -- pushing the cavity
wall deeper changed the leak by nothing, and projecting his own uncarved scan onto
the vertices that are there made it slightly worse. That ruled out displacement,
and the surface map says why:

    shallowest MARS_MESH crossing, mm into his face (s = skin, c = cavity)
      z +2    x -25  +42c   x -20  +50c        <- nothing within 40 mm of his lip plane
      z  0    x -30  +35c   x -25  +43c   x -20  +50c
      z -2    x -30  +36c   x -25  +44c   x +25  +44c
    everywhere else: skin, within a few mm of the lip plane

and the mesh agrees: **59 boundary (single-face) edge-ends at |x| > 16 mm**, with
53 faces near the commissure lip plane whose normals point INTO his head.

So it is a genuine hole with a real rim. That is a FILL -- Blender's own
holes_fill on the boundary loops -- not a projection, and it moves nothing that
already exists.
"""
import bpy, bmesh, json, os
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
P=json.load(open(os.path.join(ROOT,"renders/_session/params.json")))
FROMX=float(P.get("fromXMM",16.0)); ZBAND=float(P.get("zBandMM",10.0))
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
head=bpy.data.objects["MARS_MESH"]; me=head.data; arm=bpy.data.objects["MARS_RIG"]; sc=bpy.context.scene
W=head.matrix_world
if me.get("commissures_filled"):
    print("the commissures have already been filled"); return
names=[m.name if m else "?" for m in me.materials]
ORAL=[i for i,n in enumerate(names) if "ORAL" in n.upper()]
SKIN=[i for i in range(len(names)) if i not in ORAL]
if not SKIN:
    print("*** REFUSED: no skin material slot"); return
SKIN=SKIN[0]

def leak():
    for k in me.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    arm.pose.bones["jaw"].rotation_euler=(0,0,0); bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    eo=head.evaluated_get(deps); hm=eo.to_mesh(); pm=[p.material_index for p in hm.polygons]; eo.to_mesh_clear()
    c=Counter()
    for xx in np.arange(-30,30.01,0.3):
        for zz in np.arange(-14,12.01,0.3):
            p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
            hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
            if not hit: continue
            n=ob.original.name
            oral = n in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE","MARS_MOUTH_SOCK")
            if n=="MARS_MESH":
                mi=pm[fi] if fi<len(pm) else 0
                oral = mi in ORAL
            if oral: c["corner" if abs(xx)>16 else "middle"]+=1
    return c

n0=len(me.vertices); f0=len(me.polygons)
before=leak()
print("before: rest leak corner %d, middle %d   (%d verts, %d faces)"
      %(before["corner"],before["middle"],n0,f0))

bm=bmesh.new(); bm.from_mesh(me)
bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
def loc(v): return FINV@(W@v.co)
target=[]
for e in bm.edges:
    if len(e.link_faces)!=1: continue
    a,b=loc(e.verts[0]),loc(e.verts[1])
    if min(abs(a.x),abs(b.x))/MM < FROMX: continue
    if max(abs(a.z),abs(b.z))/MM > ZBAND: continue
    target.append(e)
print("boundary edges at the commissures: %d"%len(target))
if len(target)<3:
    bm.free(); print("*** REFUSED: only %d boundary edges out there -- nothing to fill"%len(target)); return

res=bmesh.ops.holes_fill(bm, edges=target, sides=0)
made=[f for f in res.get("faces",[]) if f.is_valid]
print("holes_fill created %d faces"%len(made))
if not made:
    bm.free(); print("*** REFUSED: holes_fill created nothing"); return
for f in made:
    f.material_index=SKIN
    f.smooth=True
bm.to_mesh(me); bm.free(); me.update()
n1=len(me.vertices); f1=len(me.polygons)
print("verts %d -> %d (must be unchanged), faces %d -> %d"%(n0,n1,f0,f1))
if n1!=n0:
    print("*** REFUSED: the fill changed the vertex count (%d -> %d)"%(n0,n1)); return
bpy.context.view_layer.update()
after=leak()
print("after:  rest leak corner %d, middle %d"%(after["corner"],after["middle"]))
if after["corner"]>=before["corner"]:
    print("*** REFUSED: the corner leak did not fall (%d -> %d)"%(before["corner"],after["corner"])); return
if after["middle"]>before["middle"]+5:
    print("*** REFUSED: it changed his centre (%d -> %d)"%(before["middle"],after["middle"])); return
me["commissures_filled"]=len(made)
out=os.path.join(ROOT,"renders/_remesh/MARS_FACE_FILLED.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("corner leak %d -> %d, middle %d -> %d; REVIEW candidate -> %s"
      %(before["corner"],after["corner"],before["middle"],after["middle"],out))
