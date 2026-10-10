"""STAGE C -- put the rebuilt mouth back on his head, carrying everything with it.

The remesh gave that region 6,812 vertices where it had 530, and left all 27,335
vertices outside it EXACTLY where they were (0.000000 mm, checked by position
because PyMeshLab reorders). What comes back is bare geometry, so every attribute
has to be carried across:

  * 89 SHAPE KEYS  -- the whole FACS set, his linework blinks, every viseme
  * 11 VERTEX GROUPS -- jaw / head / neck / tongue bones, the hair weights
  * UVs -- without them his face texture lands somewhere else entirely
  * material assignment -- skin vs the carved cavity

A vertex that survived the remesh is matched by POSITION and its attributes are
COPIED, not interpolated: interpolating a vertex that did not move is a way to
introduce error into 27,335 places that were correct. Only genuinely new vertices
are interpolated, barycentrically, from the old triangle they sit on.

Nothing is saved. The gates below decide, and promotion is a separate step.
"""
import bpy, bmesh, json, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform

ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
R=os.path.join(ROOT,"renders/_remesh")
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MM=float(MA["aperture"]["width"])/50.0

def read_ply(path):
    with open(path) as f:
        head=[]; line=f.readline()
        while True:
            head.append(line.strip())
            if line.strip()=="end_header": break
            line=f.readline()
        nv=nf=0; cur=None; nprop=0
        for h in head:
            if h.startswith("element vertex"): nv=int(h.split()[-1]); cur="v"
            elif h.startswith("element face"): nf=int(h.split()[-1]); cur="f"
            elif h.startswith("property") and cur=="v": nprop+=1
        V=[[float(x) for x in f.readline().split()[:3]] for _ in range(nv)]
        F=[[int(x) for x in f.readline().split()[1:4]] for _ in range(nf)]
    return V,F

NV,NF=read_ply(os.path.join(R,"head_remeshed.ply"))
print("remeshed: %d verts, %d tris"%(len(NV),len(NF)))

head=bpy.data.objects["MARS_MESH"]; old=head.data
keys=[k.name for k in old.shape_keys.key_blocks]
groups=[g.name for g in head.vertex_groups]
print("carrying %d shape keys and %d vertex groups"%(len(keys),len(groups)))

# ---- the OLD mesh as triangles, for nearest-surface lookups
oldV=[v.co.copy() for v in old.vertices]
oldT=[]; oldTpoly=[]
for p in old.polygons:
    vs=list(p.vertices)
    for i in range(1,len(vs)-1):
        oldT.append((vs[0],vs[i],vs[i+1])); oldTpoly.append(p.index)
bvh=BVHTree.FromPolygons([tuple(v) for v in oldV],[list(t) for t in oldT])

# ---- attributes, read once
keydata={k:[old.shape_keys.key_blocks[k].data[i].co.copy() for i in range(len(oldV))] for k in keys}
gi={g.index:g.name for g in head.vertex_groups}
wts=[{gi[g.group]:g.weight for g in v.groups if g.group in gi} for v in old.vertices]
uvl=old.uv_layers.active
loopuv={}
for p in old.polygons:
    for li,vi in zip(p.loop_indices,p.vertices):
        loopuv.setdefault(p.index,{})[vi]=uvl.data[li].uv.copy()
polymat={p.index:p.material_index for p in old.polygons}

# ---- CUSTOM SPLIT NORMALS AND SMOOTH SHADING. The first attempt carried the
# geometry and all 89 keys with 0.000000 mm drift and still rendered FAR worse --
# his whole face shattered into facets. Measured: the canonical head is 54,681 of
# 54,720 faces SMOOTH with has_custom_normals=True, and a mesh built by
# from_pydata is 0 smooth with no custom normals. The remesh was not the problem;
# the shading was never carried. A vertex position is not a surface.
old_cn=[Vector((0,0,0)) for _ in oldV]; _cnt=[0]*len(oldV)
try:
    cn=old.corner_normals
    for p in old.polygons:
        for li,vi in zip(p.loop_indices,p.vertices):
            old_cn[vi]+=Vector(cn[li].vector); _cnt[vi]+=1
except Exception as _e:
    print("corner_normals unavailable (%s); falling back to vertex normals"%_e)
    for i,v in enumerate(old.vertices): old_cn[i]=v.normal.copy(); _cnt[i]=1
for i in range(len(oldV)):
    if _cnt[i]: old_cn[i]=(old_cn[i]/_cnt[i])
    if old_cn[i].length>1e-9: old_cn[i].normalize()
    else: old_cn[i]=Vector((0,0,1))
old_smooth=sum(1 for p in old.polygons if p.use_smooth)
print("old shading: %d of %d faces smooth, custom normals=%s"
      %(old_smooth,len(old.polygons),old.has_custom_normals), flush=True)

# ---- match survivors by POSITION
key_of={}
for i,v in enumerate(oldV):
    key_of[(round(v.x,7),round(v.y,7),round(v.z,7))]=i
surv={}
for j,p in enumerate(NV):
    i=key_of.get((round(p[0],7),round(p[1],7),round(p[2],7)))
    if i is not None: surv[j]=i
print("new verts matched to old by position: %d of %d (%d are genuinely new)"
      %(len(surv),len(NV),len(NV)-len(surv)))

def bary(p):
    loc,nrm,fi,dist=bvh.find_nearest(Vector(p))
    if fi is None or fi>=len(oldT): return None
    a,b,c=oldT[fi]
    return fi,(oldV[a],oldV[b],oldV[c]),(a,b,c),loc

def interp_vec(tri_idx,tri_co,loc,table):
    a,b,c=tri_idx
    return barycentric_transform(loc,tri_co[0],tri_co[1],tri_co[2],
                                 table[a],table[b],table[c])

# ---- build the new mesh, on a temporary OBJECT (shape_key_add lives on the
# object, not the mesh -- a Mesh has no shape_key_add and says so)
nm=bpy.data.meshes.new("MARS_MESH_REMESH")
nm.from_pydata([tuple(p) for p in NV],[],[tuple(f) for f in NF])
nm.update()
for m in old.materials: nm.materials.append(m)
tmp=bpy.data.objects.new("MARS_MESH_REMESH",nm)
bpy.context.scene.collection.objects.link(tmp)

missing=0
face_of_new={}
for j,p in enumerate(NV):
    if j in surv: continue
    r=bary(p)
    if r is None: missing+=1; continue
    face_of_new[j]=r
print("nearest-surface lookups failed for %d new verts"%missing, flush=True)

# ---- MATERIALS, per face, from the old face each new one sits on
for f in nm.polygons:
    c=Vector((0,0,0))
    for vi in f.vertices: c+=Vector(NV[vi])
    c/=len(f.vertices)
    loc,nrm,fi,dist=bvh.find_nearest(c)
    if fi is not None and fi<len(oldTpoly):
        f.material_index=polymat.get(oldTpoly[fi],0)

# ---- UVs, per loop
newuv=nm.uv_layers.new(name=uvl.name)
for f in nm.polygons:
    for li,vi in zip(f.loop_indices,f.vertices):
        if vi in surv:
            # a survivor keeps a UV from any old face that used it
            for pid,d in loopuv.items():
                if surv[vi] in d: newuv.data[li].uv=d[surv[vi]]; break
            continue
        r=face_of_new.get(vi)
        if r is None: continue
        fi,tri_co,tri_idx,loc=r
        pid=oldTpoly[fi]; d=loopuv.get(pid,{})
        uvs=[d.get(t) for t in tri_idx]
        if any(u is None for u in uvs): continue
        p3=[Vector((u.x,u.y,0.0)) for u in uvs]
        out=barycentric_transform(loc,tri_co[0],tri_co[1],tri_co[2],p3[0],p3[1],p3[2])
        newuv.data[li].uv=(out.x,out.y)

# ---- SMOOTH SHADING AND CUSTOM SPLIT NORMALS
for f in nm.polygons: f.use_smooth=True
newn=[]
for j in range(len(NV)):
    if j in surv: newn.append(old_cn[surv[j]])
    elif j in face_of_new:
        fi,tri_co,tri_idx,loc=face_of_new[j]
        a3,b3,c3=tri_idx
        bw=barycentric_transform(loc,tri_co[0],tri_co[1],tri_co[2],
                                 Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
        n=(old_cn[a3]*bw.x+old_cn[b3]*bw.y+old_cn[c3]*bw.z)
        newn.append(n.normalized() if n.length>1e-9 else Vector((0,0,1)))
    else: newn.append(Vector((0,0,1)))
try:
    nm.normals_split_custom_set_from_vertices([tuple(n) for n in newn])
    print("custom split normals set from %d vertex normals"%len(newn), flush=True)
except Exception as _e:
    print("could not set custom normals: %s"%_e, flush=True)

# ---- SHAPE KEYS
tmp.shape_key_add(name="Basis",from_mix=False)
for k in keys:
    if k=="Basis": continue
    tmp.shape_key_add(name=k,from_mix=False)
for k in keys:
    tbl=keydata[k]; dst=nm.shape_keys.key_blocks[k].data
    for j in range(len(NV)):
        if j in surv: dst[j].co=tbl[surv[j]]
        elif j in face_of_new:
            fi,tri_co,tri_idx,loc=face_of_new[j]
            dst[j].co=interp_vec(tri_idx,tri_co,loc,tbl)
        else: dst[j].co=Vector(NV[j])
print("shape keys written", flush=True)

# ---- VERTEX GROUPS
for g in groups: tmp.vertex_groups.new(name=g)
vg={g.name:g for g in tmp.vertex_groups}
for j in range(len(NV)):
    if j in surv:
        w=wts[surv[j]]
    elif j in face_of_new:
        fi,tri_co,tri_idx,loc=face_of_new[j]
        a3,b3,c3=tri_idx
        bw=barycentric_transform(loc,tri_co[0],tri_co[1],tri_co[2],
                                 Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
        w={}
        for gname in groups:
            val=(bw.x*wts[a3].get(gname,0.0)+bw.y*wts[b3].get(gname,0.0)
                 +bw.z*wts[c3].get(gname,0.0))
            if val>1e-6: w[gname]=min(1.0,max(0.0,val))
    else:
        w={}
    for gname,val in w.items(): vg[gname].add([j],val,"REPLACE")
print("vertex groups written", flush=True)

# ---- GATES ------------------------------------------------------------
fail=[]
if len(nm.vertices)!=len(NV): fail.append("vertex count")
kb=[k.name for k in nm.shape_keys.key_blocks]
if kb!=keys: fail.append("shape key names changed: %d -> %d"%(len(keys),len(kb)))
B=np.array([d.co[:] for d in nm.shape_keys.key_blocks["Basis"].data],float)
dead=[]
for k in keys:
    if k=="Basis": continue
    A=np.array([d.co[:] for d in nm.shape_keys.key_blocks[k].data],float)
    if float(np.linalg.norm(A-B,axis=1).max())/MM<0.05: dead.append(k)
if dead: fail.append("%d key(s) move nothing: %s"%(len(dead),dead[:6]))
sm_new=sum(1 for p in nm.polygons if p.use_smooth)
print("new shading: %d of %d faces smooth, custom normals=%s"
      %(sm_new,len(nm.polygons),nm.has_custom_normals), flush=True)
if sm_new < len(nm.polygons)*0.99: fail.append("only %d of %d faces smooth"%(sm_new,len(nm.polygons)))
if old.has_custom_normals and not nm.has_custom_normals:
    fail.append("the canonical head has custom split normals and the rebuilt one does not "
                "-- that alone shatters his face into facets")
# every ORIGINAL vertex must still be exactly where it was, and carry its own keys
surv_inv={v:k for k,v in surv.items()}
drift=0.0; keydrift=0.0
for i in range(len(oldV)):
    j=surv_inv.get(i)
    if j is None: continue
    drift=max(drift,(Vector(NV[j])-oldV[i]).length/MM)
    for k in ("Basis","facs_jawOpen","blink_own_L") if "blink_own_L" in keys else ("Basis","facs_jawOpen"):
        if k in keys:
            keydrift=max(keydrift,(nm.shape_keys.key_blocks[k].data[j].co-keydata[k][i]).length/MM)
print("survivors: rest drift %.6f mm, shape-key drift %.6f mm"%(drift,keydrift), flush=True)
if drift>1e-4: fail.append("survivor rest drift %.6f mm"%drift)
if keydrift>1e-4: fail.append("survivor shape-key drift %.6f mm"%keydrift)
wsum={g:sum(wts[i].get(g,0.0) for i in range(len(oldV))) for g in groups}
wsum2={g:0.0 for g in groups}
for v in nm.vertices:
    for gg in v.groups:
        wsum2[tmp.vertex_groups[gg.group].name]+=gg.weight
for g in ("jaw","head"):
    if g in wsum and wsum[g]>0:
        r=wsum2[g]/wsum[g]
        print("  weight total %-6s %.1f -> %.1f  (x%.3f)"%(g,wsum[g],wsum2[g],r), flush=True)

if fail:
    print("*** REFUSED: "+"; ".join(fail))
    bpy.data.objects.remove(tmp); bpy.data.meshes.remove(nm)
    return
json.dump({"newVerts":len(NV),"newTris":len(NF),"survivors":len(surv),
           "created":len(NV)-len(surv),"lookupFailures":missing,
           "keys":len(keys),"groups":len(groups)},
          open(os.path.join(R,"apply_stage.json"),"w"),indent=2)
out=os.path.join(R,"MARS_FACE_REMESHED.blend")
old_name=old.name
head.data=nm
nm.name=old_name
bpy.data.meshes.remove(old)
bpy.data.objects.remove(tmp)
bpy.ops.wm.save_as_mainfile(filepath=out)
print("STAGE C complete -- %d verts, %d keys, %d groups -> %s"
      %(len(nm.vertices),len(keys),len(groups),out))
