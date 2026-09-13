"""NORMALS FIRST, THEN THE FILL.

The evidence ordered itself: projection failed, moving vertices failed, and a
plain holes_fill produced 2 faces and made the leak slightly worse. What is left
is that 53 faces near the commissure lip plane have normals pointing INTO his
head. Filling against inverted faces is how a 25-edge rim yields two triangles.

So: recalculate face normals across the whole shell (which is what makes the
answer well-defined -- doing it on a subset leaves the region's global orientation
arbitrary), MEASURE how many actually flip, refuse if it turns him inside out,
and only then fill.

Review blend only. Canonical is not written under any outcome.
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
names=[m.name if m else "?" for m in me.materials]
ORAL=[i for i,n in enumerate(names) if "ORAL" in n.upper()]
SKIN=next((i for i in range(len(names)) if i not in ORAL),0)

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

before=leak()
n0=len(me.vertices); f0=len(me.polygons)
print("before: corner %d, middle %d   (%d verts, %d faces)"%(before["corner"],before["middle"],n0,f0))

pre=[tuple(p.normal) for p in me.polygons]
bm=bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(me); bm.free(); me.update()
post=[tuple(p.normal) for p in me.polygons]
flip=sum(1 for a,b in zip(pre,post) if Vector(a).dot(Vector(b))<0)
print("recalc flipped %d of %d faces (%.2f%%)"%(flip,len(pre),100.0*flip/max(1,len(pre))))
if flip > len(pre)*0.5:
    print("*** REFUSED: recalc turned more than half his head inside out"); return

# how many of the commissure faces were the inverted ones?
inv=0
for p in me.polygons:
    c=W@p.center; l=FINV@c
    if abs(l.x)/MM>FROMX and abs(l.z)/MM<8 and l.y/MM<12:
        if (W.to_3x3()@p.normal).dot(OUTW)<0: inv+=1
print("faces near the commissure lip plane still pointing INTO his head: %d (was 53)"%inv)

bpy.context.view_layer.update()
mid=leak()
print("after recalc, before any fill: corner %d, middle %d"%(mid["corner"],mid["middle"]))

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
print("boundary edges at the commissures after recalc: %d"%len(target))
made=[]
if len(target)>=3:
    res=bmesh.ops.holes_fill(bm, edges=target, sides=0)
    made=[f for f in res.get("faces",[]) if f.is_valid]
    for f in made:
        f.material_index=SKIN; f.smooth=True
    if made:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
print("holes_fill created %d faces"%len(made))
bm.to_mesh(me); bm.free(); me.update(); bpy.context.view_layer.update()
if len(me.vertices)!=n0:
    print("*** REFUSED: vertex count changed %d -> %d"%(n0,len(me.vertices))); return
after=leak()
print("after:  corner %d, middle %d   (%d faces)"%(after["corner"],after["middle"],len(me.polygons)))
if after["corner"]>=before["corner"]:
    print("*** REFUSED: the corner leak did not fall (%d -> %d)"%(before["corner"],after["corner"])); return
if after["middle"]>before["middle"]+5:
    print("*** REFUSED: it changed his centre (%d -> %d)"%(before["middle"],after["middle"])); return
out=os.path.join(ROOT,"renders/_remesh/MARS_FACE_NORMALS_FILL.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("corner %d -> %d, middle %d -> %d; REVIEW candidate -> %s"
      %(before["corner"],after["corner"],before["middle"],after["middle"],out))
