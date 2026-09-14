#!/usr/bin/env python3
"""Build a review-only mouth candidate from the original MARS_FACE.glb donor.

The original GLB is treated as the immutable facial/cavity donor. Only the
three improved standalone oral meshes are replaced. No face topology,
mouth-sock topology, booleans, remeshes, welds, or reweights are performed.
"""
import argparse, json, os, bpy

ORAL=("MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE")
PROTECTED=("MARS_MESH","MARS_MOUTH_SOCK","MARS_RIG")

def args():
    av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser()
    p.add_argument("--host",required=True)
    p.add_argument("--interior",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--report",required=True)
    return p.parse_args(av)

import sys
def refuse(m): raise SystemExit("ORIGINAL_GLB_DONOR_REFUSED: "+m)

def main():
    a=args()
    bpy.ops.wm.open_mainfile(filepath=a.host)
    for n in PROTECTED:
        if bpy.data.objects.get(n) is None: refuse("missing "+n)
    if bpy.data.objects["MARS_MESH"].type!="MESH": refuse("MARS_MESH not mesh")
    if bpy.data.objects["MARS_RIG"].type!="ARMATURE": refuse("MARS_RIG not armature")
    host_arm=bpy.data.objects["MARS_RIG"]

    with bpy.data.libraries.load(a.interior,link=False) as (src,dst):
        avail=set(src.objects)
        missing=[n for n in ORAL if n not in avail]
        if missing: refuse("interior missing "+",".join(missing))
        dst.objects=list(ORAL)

    deleted=[]; appended=[]
    for n in ORAL:
        old=bpy.data.objects.get(n)
        if old:
            deleted.append({"name":n,"verts":len(old.data.vertices)})
            bpy.data.objects.remove(old,do_unlink=True)

    for ob in dst.objects:
        if ob is None or ob.type!="MESH": refuse("invalid appended oral object")
        if not any(c.objects.get(ob.name) is ob for c in ob.users_collection):
            bpy.context.scene.collection.objects.link(ob)
        world=ob.matrix_world.copy()
        ob.parent=host_arm; ob.parent_type="OBJECT"; ob.matrix_world=world
        mods=[m for m in ob.modifiers if m.type=="ARMATURE"]
        if not mods: mods=[ob.modifiers.new("MARS_ORAL_HOST_RIG","ARMATURE")]
        for m in mods: m.object=host_arm
        if n=="MARS_TONGUE":
            if not ob.data.shape_keys or len(ob.data.shape_keys.key_blocks)<2: refuse("tongue expression keys missing")
            if not any(g.name=="tongue_root" for g in ob.vertex_groups): refuse("tongue_root missing")
        elif not any(g.name in ("head","jaw") for g in ob.vertex_groups): refuse(n+" required rigid jaw/head group missing")
        appended.append({"name":ob.name,"verts":len(ob.data.vertices),"shapeKeys":len(ob.data.shape_keys.key_blocks) if ob.data.shape_keys else 0})

    for n in PROTECTED:
        if bpy.data.objects.get(n) is None: refuse("protected object disappeared "+n)
    for n in ORAL:
        if sum(1 for o in bpy.data.objects if o.name==n)!=1: refuse("duplicate "+n)

    os.makedirs(os.path.dirname(a.out),exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=a.out)
    report={"schema":"god-molecule.original-glb-oral-assembly.v1","status":"REVIEW_ONLY",
            "host":a.host,"interior":a.interior,"out":a.out,
            "donor":{"source":"original MARS_FACE.glb","face_topology_mutated":False,
                     "mouth_sock_preserved":True,"armature_preserved":True,
                     "host_mesh_vertices":len(bpy.data.objects["MARS_MESH"].data.vertices)},
            "deletedInterior":deleted,"appendedInterior":appended,
            "protection":["no boolean","no remesh","no weld","no seam split","no host reweight"],
            "promotionBlockedUntil":["open-mouth rendered pixels","profile silhouette","material survey","visual human review"]}
    os.makedirs(os.path.dirname(a.report),exist_ok=True)
    open(a.report,"w").write(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__=="__main__": main()
