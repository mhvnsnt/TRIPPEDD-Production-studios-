"""STAGE C, ON BLENDER'S OWN DATA TRANSFER INSTEAD OF MY APPROXIMATION.

Two attempts failed the pixels, and both failures were in attribute transfer, not
in the remesh:
  attempt 1  physical gates ALL green, face shattered -- smoothing and custom
             split normals were never carried. A vertex position is not a surface.
  attempt 2  shading carried, facets fixed, STILL failed -- torn UV patches, from
             a per-loop UV transfer I hand-wrote.

Blender ships DATA TRANSFER for exactly this: UVs, custom split normals, vertex
groups and the smooth flag from one mesh onto another, seams included, as a
production operation. Writing an approximation beside it is OWNER LAW #3 broken,
and the pixels said so twice.

ORDER MATTERS, AND IT IS NOT OPTIONAL: modifier_apply REFUSES on a mesh that has
shape keys. So the transfer runs on bare geometry FIRST and the 89 keys are added
afterwards -- by the barycentric interpolation that already measured 0.000000 mm
drift on all 27,536 survivors, which is the one part of my own code the pixels
never faulted.

  mode C -- canonical shading kept from my own transfer, UVs via Data Transfer
  mode D -- UVs, custom normals, smooth flag and vertex groups all via Data Transfer
"""
import bpy, json, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform

ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
R=os.path.join(ROOT,"renders/_remesh")
_pp=os.path.join(ROOT,"renders/_session/params.json")
_P=json.load(open(_pp)) if os.path.exists(_pp) else {}
MODE=_P.get("mode","D").upper()
MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
MM=float(MA["aperture"]["width"])/50.0

def read_ply(path):
    with open(path) as f:
        head=[]; line=f.readline()
        while True:
            head.append(line.strip())
            if line.strip()=="end_header": break
            line=f.readline()
        nv=nf=0; cur=None
        for h in head:
            if h.startswith("element vertex"): nv=int(h.split()[-1]); cur="v"
            elif h.startswith("element face"): nf=int(h.split()[-1]); cur="f"
        V=[[float(x) for x in f.readline().split()[:3]] for _ in range(nv)]
        F=[[int(x) for x in f.readline().split()[1:4]] for _ in range(nf)]
    return V,F

NV,NF=read_ply(os.path.join(R,"head_remeshed.ply"))
src=bpy.data.objects["MARS_MESH"]; old=src.data
keys=[k.name for k in old.shape_keys.key_blocks]
groups=[g.name for g in src.vertex_groups]
print("mode %s -- source: %d verts, %d keys, %d groups, %d/%d faces smooth, custom normals %s"
      %(MODE,len(old.vertices),len(keys),len(groups),
        sum(1 for p in old.polygons if p.use_smooth),len(old.polygons),old.has_custom_normals),
      flush=True)

# ---- bare geometry object
nm=bpy.data.meshes.new("MARS_REMESH_MESH")
nm.from_pydata([tuple(p) for p in NV],[],[tuple(f) for f in NF]); nm.update()
# SMOOTH FIRST, THEN THE TRANSFER. A mesh from from_pydata is entirely FLAT, and a
# custom split normal cannot survive on a flat face -- mode C transferred UVs
# correctly and came back has_custom_normals=False for exactly that reason. The
# flag is one line and is not an approximation of anything, so it is set here and
# Blender's transfer supplies the normals themselves.
for f in nm.polygons: f.use_smooth=True
# AND THE UV LAYER HAS TO EXIST BEFORE THE TRANSFER HAS SOMEWHERE TO PUT IT.
# Measured: asking for UV alone (mode C) auto-created it, asking for UV AND
# CUSTOM_NORMAL together (mode D) came back with uv_layers=[] -- the layer was
# never made, so the UVs had nowhere to land while the normals arrived fine.
# Creating it explicitly, under the source's own name, removes the interaction.
for l in old.uv_layers:
    nm.uv_layers.new(name=l.name)
for m in old.materials: nm.materials.append(m)
tgt=bpy.data.objects.new("MARS_REMESH",nm)
bpy.context.scene.collection.objects.link(tgt)
tgt.matrix_world=src.matrix_world.copy()

# ---- BLENDER'S OWN DATA TRANSFER
bpy.context.view_layer.objects.active=tgt
tgt.select_set(True)
md=tgt.modifiers.new("DT","DATA_TRANSFER")
md.object=src
md.use_loop_data=True
md.loop_mapping="POLYINTERP_NEAREST"
md.data_types_loops={"UV"} if MODE=="C" else {"UV","CUSTOM_NORMAL"}
if MODE=="D":
    md.use_vert_data=True
    md.vert_mapping="POLYINTERP_NEAREST"
    md.data_types_verts={"VGROUP_WEIGHTS"}
    md.use_poly_data=True
    md.poly_mapping="POLYINTERP_PNORPROJ"
    md.data_types_polys={"SMOOTH"}
bpy.ops.object.datalayout_transfer(modifier=md.name)
bpy.ops.object.modifier_apply(modifier=md.name)   # legal: no shape keys yet
print("data transfer applied: loops=%s verts=%s polys=%s"
      %(md.data_types_loops if hasattr(md,'data_types_loops') else '-',
        getattr(md,'data_types_verts','-'),getattr(md,'data_types_polys','-')), flush=True)
print("  after transfer: uv layers=%s, %d/%d faces smooth, custom normals=%s, groups=%d"
      %([l.name for l in nm.uv_layers],sum(1 for p in nm.polygons if p.use_smooth),
        len(nm.polygons),nm.has_custom_normals,len(tgt.vertex_groups)), flush=True)

# ---- the old mesh as triangles, for the shape-key interpolation only
oldV=[v.co.copy() for v in old.vertices]
oldT=[]; oldTpoly=[]
for p in old.polygons:
    vs=list(p.vertices)
    for i in range(1,len(vs)-1): oldT.append((vs[0],vs[i],vs[i+1])); oldTpoly.append(p.index)
bvh=BVHTree.FromPolygons([tuple(v) for v in oldV],[list(t) for t in oldT])
keydata={k:[old.shape_keys.key_blocks[k].data[i].co.copy() for i in range(len(oldV))] for k in keys}
key_of={(round(v.x,7),round(v.y,7),round(v.z,7)):i for i,v in enumerate(oldV)}
surv={}
for j,p in enumerate(NV):
    i=key_of.get((round(p[0],7),round(p[1],7),round(p[2],7)))
    if i is not None: surv[j]=i
face_of_new={}
for j,p in enumerate(NV):
    if j in surv: continue
    loc,nrm,fi,dist=bvh.find_nearest(Vector(p))
    if fi is None or fi>=len(oldT): continue
    a,b,c=oldT[fi]
    face_of_new[j]=((oldV[a],oldV[b],oldV[c]),(a,b,c),loc)
print("survivors %d, new %d, lookup failures %d"
      %(len(surv),len(NV)-len(surv),len(NV)-len(surv)-len(face_of_new)), flush=True)

# ---- materials, per face
for f in nm.polygons:
    c=Vector((0,0,0))
    for vi in f.vertices: c+=Vector(NV[vi])
    c/=len(f.vertices)
    loc,nrm,fi,dist=bvh.find_nearest(c)
    if fi is not None and fi<len(oldTpoly): f.material_index=old.polygons[oldTpoly[fi]].material_index

# ---- RESTORE EXACT UVs ON EVERY FACE THAT SURVIVED UNTOUCHED
# POLYINTERP_NEAREST resamples UVs across ALL 34,147 verts, including the 27,536
# survivors whose UVs were already correct -- and it cannot reproduce a UV SEAM,
# where one vertex carries several UVs. That scrambled the texture over his whole
# head, far outside the region being rebuilt. Only the new region needs
# interpolated UVs; everywhere else the original is right by definition, so it is
# put back exactly. A face qualifies when all of its vertices are survivors AND
# the same triple exists as a face on the canonical mesh.
old_face_by_key={}
for p_ in old.polygons:
    old_face_by_key[tuple(sorted(p_.vertices))]=p_
old_loopuv={}
_uv=old.uv_layers.active
for p_ in old.polygons:
    old_loopuv[p_.index]={vi:_uv.data[li].uv.copy() for li,vi in zip(p_.loop_indices,p_.vertices)}
newuv=nm.uv_layers.active
restored=0; interpolated=0
for f in nm.polygons:
    vs=list(f.vertices)
    if all(v in surv for v in vs):
        k=tuple(sorted(surv[v] for v in vs))
        op=old_face_by_key.get(k)
        if op is not None:
            d=old_loopuv[op.index]
            ok=True
            for li,vi in zip(f.loop_indices,vs):
                u=d.get(surv[vi])
                if u is None: ok=False; break
                newuv.data[li].uv=u
            if ok: restored+=1; continue
    interpolated+=len(f.loop_indices)
print("UVs: %d of %d faces restored EXACTLY from the canonical mesh; %d loops left "
      "to the transfer's interpolation (the rebuilt region)"
      %(restored,len(nm.polygons),interpolated), flush=True)
if restored < len(nm.polygons)*0.5:
    print("*** REFUSED: only %d of %d faces got their original UVs back"
          %(restored,len(nm.polygons))); return

# ---- shape keys, added AFTER the transfer because modifier_apply refuses otherwise
tgt.shape_key_add(name="Basis",from_mix=False)
for k in keys:
    if k!="Basis": tgt.shape_key_add(name=k,from_mix=False)
for k in keys:
    tbl=keydata[k]; dst=nm.shape_keys.key_blocks[k].data
    for j in range(len(NV)):
        if j in surv: dst[j].co=tbl[surv[j]]
        elif j in face_of_new:
            tri_co,tri_idx,loc=face_of_new[j]
            a,b,c=tri_idx
            dst[j].co=barycentric_transform(loc,tri_co[0],tri_co[1],tri_co[2],tbl[a],tbl[b],tbl[c])
        else: dst[j].co=Vector(NV[j])
print("89 shape keys written", flush=True)

# ---- GATES
fail=[]
kb=[k.name for k in nm.shape_keys.key_blocks]
if kb!=keys: fail.append("shape keys %d -> %d"%(len(keys),len(kb)))
B=np.array([d.co[:] for d in nm.shape_keys.key_blocks["Basis"].data],float)
dead=[k for k in keys if k!="Basis" and
      float(np.linalg.norm(np.array([d.co[:] for d in nm.shape_keys.key_blocks[k].data],float)-B,axis=1).max())/MM<0.05]
if dead: fail.append("%d key(s) move nothing"%len(dead))
inv={v:k for k,v in surv.items()}
drift=max(((Vector(NV[inv[i]])-oldV[i]).length/MM) for i in inv) if inv else 0.0
if drift>1e-4: fail.append("survivor rest drift %.6f mm"%drift)
sm=sum(1 for p in nm.polygons if p.use_smooth)
if sm<len(nm.polygons)*0.99: fail.append("only %d of %d faces smooth"%(sm,len(nm.polygons)))
if old.has_custom_normals and not nm.has_custom_normals: fail.append("no custom split normals")
if not nm.uv_layers: fail.append("no UV layer")
if MODE=="D" and len(tgt.vertex_groups)<len(groups):
    fail.append("vertex groups %d -> %d"%(len(groups),len(tgt.vertex_groups)))
print("gates: rest drift %.6f mm, %d/%d smooth, custom normals %s, uvs %s, groups %d"
      %(drift,sm,len(nm.polygons),nm.has_custom_normals,bool(nm.uv_layers),len(tgt.vertex_groups)),
      flush=True)
if fail:
    print("*** REFUSED: "+"; ".join(fail)); return

out=os.path.join(R,"MARS_FACE_REMESHED_%s.blend"%MODE)
name=src.name
src_mesh=src.data
src.data=nm; nm.name=name
# DO NOT TOUCH THE OBJECT'S VERTEX GROUPS. Weights live in the MESH's deform
# layer and Blender ties them to the object's group list by INDEX -- removing a
# group destroys the weights that were just transferred into it. The first
# version of this block removed all eleven and re-added them empty, so the
# armature drove nothing and his mouth rendered SHUT in a jaw-30 pose. The test
# was not even valid. The groups the transfer created on the temporary object are
# reconciled by NAME instead, and only ones that are missing are added.
if MODE=="D":
    have={g.name for g in src.vertex_groups}
    for g in tgt.vertex_groups:
        if g.name not in have: src.vertex_groups.new(name=g.name)
bpy.data.objects.remove(tgt)
bpy.data.meshes.remove(src_mesh)
bpy.ops.wm.save_as_mainfile(filepath=out)
print("STAGE C/%s complete -- %d verts, %d keys -> %s"%(MODE,len(nm.vertices),len(keys),out))
