"""RESTORE HIS SKIN AT THE TWO CAVED COMMISSURES. NOTHING ELSE MOVES.

Measured: his lips already meet from x -15 to +20 mm. At the commissures the
head's own surface is pulled 38-52 mm INTO his face by the carve. The uncarved
scan still has that skin.

THE SELECTION IS BOUNDED BY HIS LIP LINE, NOT BY A COORDINATE. The previous
attempt used "|x| > 16 mm AND deeper than 12 mm", which selected 22,998 vertices
-- most of his head -- and moved 3,217 of them up to 41 mm. Here a vertex must be
within a small radius of one of his two MEASURED commissure points AND be caved in
behind the local lip plane. Everything else is untouchable.

  * writes a REVIEW blend, never the canonical rig
  * the scan reference is REMOVED before any gate runs -- an imported reference
    occludes every diagnostic ray and once made the leak read 5 instead of 919
  * every move is capped, and a vertex that would travel further is left alone
"""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
P=json.load(open(os.path.join(ROOT,"renders/_session/params.json")))
RADIUS=float(P.get("commissureRadiusMM",14.0))
CAVED =float(P.get("cavedBehindMM",6.0))
MAXMOVE=float(P.get("maxMoveMM",22.0))
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
head=bpy.data.objects["MARS_MESH"]; me=head.data; arm=bpy.data.objects["MARS_RIG"]; sc=bpy.context.scene
W=head.matrix_world
names=[m.name if m else "?" for m in me.materials]
ORAL=[i for i,n in enumerate(names) if "ORAL" in n.upper()]

CL=Vector(MA["aperture"]["cornerLeft"]); CR=Vector(MA["aperture"]["cornerRight"])
lCL=FINV@CL; lCR=FINV@CR
MAXDEEP=float(P.get("maxDeepMM",60.0))
print("his measured commissures: L %s  R %s"%(["%.4f"%c for c in CL],["%.4f"%c for c in CR]))

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

# ---- the selection: near a commissure AND caved behind the local lip plane
LIPY=float(np.percentile([ (FINV@(W@me.vertices[i].co)).y/MM
    for i in range(len(me.vertices))
    if abs((FINV@(W@me.vertices[i].co)).x)/MM<12 and abs((FINV@(W@me.vertices[i].co)).z)/MM<4],50))
print("his lip plane sits at depth %+.2f mm (median of the central lip band)"%LIPY)
sel=[]
for i,v in enumerate(me.vertices):
    wp=W@v.co; l=FINV@wp
    # DISTANCE IN HIS LIP PLANE, NOT IN SPACE. The crater is a DEPTH displacement
    # of 38-52 mm, so a 14 mm sphere around the commissure POINT cannot reach a
    # single vertex of it -- the first version of this selection found 8. Lateral
    # and vertical distance to the commissure is what bounds a commissure; depth
    # is the thing being repaired and must not also be the thing gating it.
    d=min(((l.x-lCL.x)**2+(l.z-lCL.z)**2)**0.5,
          ((l.x-lCR.x)**2+(l.z-lCR.z)**2)**0.5)/MM
    if d>RADIUS: continue
    if l.y/MM < LIPY+CAVED: continue
    if l.y/MM > LIPY+MAXDEEP: continue      # the back of his skull is not his mouth
    sel.append(i)
print("commissure-bounded selection: %d vertices (within %.0f mm of a commissure and "
      "more than %.0f mm behind his lip plane)"%(len(sel),RADIUS,CAVED))
if not sel:
    print("nothing selected"); return
if len(sel)>2000:
    print("*** REFUSED: %d vertices is not a commissure repair"%len(sel)); return

before=leak()
print("before: rest leak corner %d, middle %d"%(before["corner"],before["middle"]))

# ---- his uncarved scan, as the source, removed again before any gate
src=os.path.join(ROOT,"assets/source_models/MARS_LOD2.glb")
pre={o.name for o in bpy.data.objects}
bpy.ops.import_scene.gltf(filepath=src)
newo=[o for o in bpy.data.objects if o.name not in pre and o.type=="MESH"]
scan=newo[0]
if len(newo)>1:
    bpy.ops.object.select_all(action="DESELECT")
    for o in newo: o.select_set(True)
    bpy.context.view_layer.objects.active=newo[0]; bpy.ops.object.join()
    scan=bpy.context.view_layer.objects.active
scan.name="MARS_SCAN_REF"
g=head.vertex_groups.get("COMMISSURE_REPAIR") or head.vertex_groups.new(name="COMMISSURE_REPAIR")
for i in sel: g.add([i],1.0,"REPLACE")
md=head.modifiers.new("COMMISSURE_WRAP","SHRINKWRAP")
md.target=scan; md.wrap_method="NEAREST_SURFACEPOINT"; md.vertex_group=g.name
bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
eo=head.evaluated_get(deps); em=eo.to_mesh()
newco={i:em.vertices[i].co.copy() for i in sel}
eo.to_mesh_clear(); head.modifiers.remove(md)
bpy.data.objects.remove(scan)          # BEFORE any measurement. It occludes every ray.
for o in [o for o in bpy.data.objects if o.name.startswith("MARS_SCAN_REF")]:
    bpy.data.objects.remove(o)
bpy.context.view_layer.update()

moved=0; worst=0.0; skipped=0
for i in sel:
    delta=newco[i]-me.vertices[i].co
    d=delta.length/MM
    if d<1e-6: continue
    if d>MAXMOVE: skipped+=1; continue        # capped: too far to be this commissure
    me.vertices[i].co=newco[i]
    for k in me.shape_keys.key_blocks: k.data[i].co=k.data[i].co+delta
    moved+=1; worst=max(worst,d)
me.update(); bpy.context.view_layer.update()
print("projected %d vertices onto his scan (worst %.2f mm); %d skipped over the %.0f mm cap"
      %(moved,worst,skipped,MAXMOVE))
after=leak()
print("after:  rest leak corner %d, middle %d"%(after["corner"],after["middle"]))
if after["corner"]>=before["corner"]:
    print("*** REFUSED: the corner leak did not fall (%d -> %d)"%(before["corner"],after["corner"])); return
if after["middle"]>before["middle"]*1.5+5:
    print("*** REFUSED: it opened his centre (%d -> %d)"%(before["middle"],after["middle"])); return
out=os.path.join(ROOT,"renders/_remesh/MARS_FACE_COMMISSURE.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("REVIEW candidate -> %s   (canonical untouched)"%out)
