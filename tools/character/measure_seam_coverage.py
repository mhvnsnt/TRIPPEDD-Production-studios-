"""
DOES THE SEAM SPLIT REACH THE ENDS OF HIS MOUTH? IT DOES NOT.

A fully split seam CANNOT have a face on both sides of it -- a split makes
duplicate vertices that share no face. So 43 faces still bridging his lips means
the cut does not go all the way across, and this finds where it stops by looking
for the duplicate POSITIONS a split leaves behind.

Measured on the re-carved candidate:

    split pairs      x -22.5 .. +22.1 mm       ZERO beyond +-25 mm
    straddling faces x -28.3 .. +33.9 mm       9 of 43 beyond |x| 25
                     median area 13.98 mm2     against a head median of 0.44

So the worst bridges sit exactly where there is no split at all. That is a
COVERAGE result, not a resolution one -- which is why densifying the rim changed
the render by nothing and made the count worse (32 -> 38 faces at jaw 30).

The second group is different and should not be confused with it: straddlers at
x -20..-15 (5) and +15..+20 (7) sit INSIDE the split region, where the cut chain
passes through without separating every face adjacent to it.

    vendor/blender/blender -b -P tools/character/measure_seam_coverage.py -- \
        --rig renders/_recarve/MARS_FACE_CANDIDATE.blend
"""
import numpy as np
ROOT=os.getcwd()
import sys
RIG = sys.argv[sys.argv.index("--rig")+1] if "--rig" in sys.argv else "renders/_recarve/MARS_FACE_CANDIDATE.blend"
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,RIG))
anat=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MW=anat["aperture"]["width"]; MM=MW/50.0
F=np.array(anat["frame"]["matrix"],float); FI=np.linalg.inv(F)
UP=np.array(anat["contours"]["lip_inner_upper"],float)
LO=np.array(anat["contours"]["lip_inner_lower"],float)
o=bpy.data.objects["MARS_MESH"]; me=o.data
W=np.array(o.matrix_world)
V=np.array([v.co[:] for v in me.vertices],float)
Vw=V@W[:3,:3].T+W[:3,3]
L=(FI@np.hstack([Vw,np.ones((len(Vw),1))]).T).T[:,:3]/MM

def seam_z(x):
    u=np.array([(FI@np.array([*p,1.0]))[:3]/MM for p in UP]); l=np.array([(FI@np.array([*p,1.0]))[:3]/MM for p in LO])
    us=u[np.argsort(u[:,0])]; ls=l[np.argsort(l[:,0])]
    return 0.5*(np.interp(x,us[:,0],us[:,2])+np.interp(x,ls[:,0],ls[:,2]))

zs=np.array([seam_z(x) for x in L[:,0]])
EPS=0.2
side=np.where(L[:,2]>zs+EPS,1,np.where(L[:,2]<zs-EPS,-1,0))
inzone=(np.abs(L[:,0])<30)&(np.abs(L[:,2]-zs)<12)&(L[:,1]<20)

# WHERE IS THE SPLIT? a split creates DUPLICATE positions with no shared face.
# find vertices that share a position with another vertex, in the mouth zone.
from collections import defaultdict
key=defaultdict(list)
for i in np.nonzero(inzone)[0]:
    key[tuple(np.round(V[i],7))].append(int(i))
split_x=[L[v[0],0] for v in key.values() if len(v)>1]
print("SPLIT PAIRS in the mouth zone: %d" % len(split_x))
if split_x:
    sx=np.array(split_x)
    print("  they span x %+.1f .. %+.1f mm  (his aperture is +-25.0 mm)" % (sx.min(), sx.max()))
    h,edges=np.histogram(sx,bins=np.arange(-30,31,5))
    print("  split pairs per 5 mm bin:")
    for c,e in zip(h,edges): print("    x %+4.0f..%+4.0f : %d" % (e,e+5,c))

# and where do the straddlers sit
strad=[]
for p in me.polygons:
    vi=list(p.vertices)
    if not any(inzone[i] for i in vi): continue
    s=set(side[i] for i in vi if side[i]!=0)
    if 1 in s and -1 in s:
        c=np.array(p.center[:])@W[:3,:3].T+W[:3,3]
        lc=(FI@np.array([*c,1.0]))[:3]/MM
        strad.append((float(lc[0]), p.area/(MM*MM)))
print("\nSTRADDLING FACES AT REST: %d" % len(strad))
if strad:
    sx=np.array([s[0] for s in strad]); sa=np.array([s[1] for s in strad])
    print("  they span x %+.1f .. %+.1f mm, median area %.2f mm2" % (sx.min(), sx.max(), float(np.median(sa))))
    h,edges=np.histogram(sx,bins=np.arange(-30,31,5))
    print("  straddlers per 5 mm bin:")
    for c,e in zip(h,edges): print("    x %+4.0f..%+4.0f : %d" % (e,e+5,c))
