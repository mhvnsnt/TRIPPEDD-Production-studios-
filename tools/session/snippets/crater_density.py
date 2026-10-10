"""Why did a commissure-bounded selection find only 8 vertices? Count what is there."""
import bpy, json, os
import numpy as np
from mathutils import Vector, Matrix
ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=float(MA["aperture"]["width"]); MM=MW/50.0
FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
head=bpy.data.objects["MARS_MESH"]; me=head.data; W=head.matrix_world
L=np.array([list(FINV@(W@v.co)) for v in me.vertices])/MM
names=[m.name if m else "?" for m in me.materials]
ORAL=[i for i,n in enumerate(names) if "ORAL" in n.upper()]
oral_v=set()
for p in me.polygons:
    if p.material_index in ORAL: oral_v.update(p.vertices)
print("the crater region, by lateral band (|z| < 8 mm):")
for lo,hi in ((-34,-28),(-28,-22),(-22,-16),(-16,-8),(-8,8),(8,16),(16,22),(22,28),(28,34)):
    m=(L[:,0]>=lo)&(L[:,0]<hi)&(np.abs(L[:,2])<8)
    n=int(m.sum())
    if not n: print("  x %+4d..%+4d : 0 verts"); continue
    deep=int((m&(L[:,1]>8)).sum())
    oral=sum(1 for i in np.nonzero(m)[0] if int(i) in oral_v)
    print("  x %+4d..%+4d : %4d verts, %4d deeper than 8 mm, %4d on oral material, "
          "depth %+6.1f..%+6.1f mm"%(lo,hi,n,deep,oral,L[m,1].min(),L[m,1].max()))
# face size in the crater
big=[]
for p in me.polygons:
    c=FINV@(W@p.center)
    if abs(c.x)/MM>16 and abs(c.z)/MM<8 and c.y/MM>8:
        big.append(p.area/(MM*MM))
if big:
    b=np.array(big)
    print("\nfaces in the crater: %d, area median %.1f mm2, max %.1f mm2 "
          "(his head's median is 0.42 mm2)"%(len(b),np.median(b),b.max()))
