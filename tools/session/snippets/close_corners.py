"""HIS LIPS MUST MEET AT REST. THE OPENING BELONGS IN THE MIDDLE.

    "when the mouth is closed, the lips should meet. At rest it should be maybe a
     little opening slightly in the middle ... there's too many corner openings
     at rest."                                         -- the owner, 2026-09-13

Cross-sectioned at rest: from x -15 to +20 mm his lips ARE closed (skin all the
way). Beyond that the camera meets cavity, teeth and sock directly -- the carved
aperture runs past the corners of his own mouth on both sides, and his measured
aperture corners are at +/-25.26 mm.

The repair is at the CAVITY, not at his lips: any ORAL_MAT vertex sitting level
with or in front of his skin at the corners is pushed back behind it. His skin is
never moved -- the face he is keeps every vertex it has.
"""
import bpy, bmesh, json, os
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
DEEPER=(FRAME.to_3x3()@Vector((0,1,0))).normalized()
head=bpy.data.objects["MARS_MESH"]; arm=bpy.data.objects["MARS_RIG"]; sc=bpy.context.scene
me=head.data
if me.get("corners_closed"):
    print("the corners have already been closed"); return
names=[m.name if m else "?" for m in me.materials]
ORAL=[i for i,n in enumerate(names) if "ORAL" in n.upper()]
if not ORAL:
    print("*** REFUSED: MARS_MESH has no oral material"); return
CORNER=float(json.load(open(os.path.join(ROOT,"renders/_session/params.json"))).get("cornerFromMM",16.0))
BEHIND=float(json.load(open(os.path.join(ROOT,"renders/_session/params.json"))).get("behindMM",2.0))

def leak():
    for k in me.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    arm.pose.bones["jaw"].rotation_euler=(0,0,0); bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    c=Counter(); side=Counter()
    for xx in np.arange(-30,30.01,0.3):
        for zz in np.arange(-20,16.01,0.3):
            p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
            hit,lo,_n,fi,ob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
            if not hit: continue
            n=ob.original.name
            oral = n in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE","MARS_MOUTH_SOCK")
            if n=="MARS_MESH":
                eo=head.evaluated_get(deps); hm=eo.to_mesh()
                mi=hm.polygons[fi].material_index if fi<len(hm.polygons) else 0
                eo.to_mesh_clear()
                oral = mi in ORAL
            if oral:
                c["total"]+=1
                side["corner" if abs(xx)>CORNER else "middle"]+=1
    return c["total"],side

# which oral-material verts sit at the corners
W=head.matrix_world
oral_v=set()
for p in me.polygons:
    if p.material_index in ORAL: oral_v.update(p.vertices)
L={i:FINV@(W@me.vertices[i].co) for i in oral_v}
corner=[i for i in oral_v if abs(L[i].x)/MM > CORNER]
print("oral-material vertices: %d, of which at the corners (|x| > %.0f mm): %d"
      %(len(oral_v),CORNER,len(corner)))
if not corner:
    print("nothing at the corners"); return

# his SKIN depth nearby, so the cavity can be put behind it rather than behind a guess
from mathutils.bvhtree import BVHTree
skin_tris=[]; skin_v=[v.co.copy() for v in me.vertices]
for p in me.polygons:
    if p.material_index in ORAL: continue
    vs=list(p.vertices)
    for k in range(1,len(vs)-1): skin_tris.append([vs[0],vs[k],vs[k+1]])
bvh=BVHTree.FromPolygons([tuple(v) for v in skin_v],skin_tris)

before,sb=leak()
print("before: %d rays reach something oral at REST  (corner %d, middle %d)"
      %(before,sb["corner"],sb["middle"]))

moved=0; worst=0.0
for i in corner:
    co=me.vertices[i].co
    loc,nrm,fi,dist=bvh.find_nearest(co)
    if loc is None: continue
    ly=FINV@(W@loc)
    want=ly.y + BEHIND*MM          # this much deeper than his skin, in mouth-frame y
    cur=L[i].y
    if cur >= want: continue
    d=(want-cur)
    me.vertices[i].co = co + (W.inverted().to_3x3() @ (DEEPER*d))
    moved+=1; worst=max(worst,d/MM)
me.update(); bpy.context.view_layer.update()
print("pushed %d corner cavity vertices back, worst %.2f mm"%(moved,worst))
after,sa=leak()
print("after:  %d rays reach something oral at REST  (corner %d, middle %d)"
      %(after,sa["corner"],sa["middle"]))
if after>=before:
    print("*** REFUSED: the rest leak did not fall (%d -> %d)"%(before,after)); return
me["corners_closed"]=moved
out=(bpy.data.filepath or os.path.join(ROOT,"assets/rigs/MARS_FACE.blend"))
# SAVE THE BLEND THIS SESSION ACTUALLY HAS OPEN, not a hardcoded canonical
# path. Run against a REVIEW blend on a second session port, these snippets
# each wrote their result straight over assets/rigs/MARS_FACE.blend -- an
# unreviewed promotion nobody asked for, and the same way the good mouth was
# lost under the eye work. A repair belongs to the file it was run on.
bpy.ops.wm.save_as_mainfile(filepath=out)
print("saved -> %s"%out)
