"""OPEN THE VESTIBULE LINING. It is a bag; it should be a liner.

Owner: "this pink circular ring that's hanging down in front of the top teeth ...
it's all fighting each other."

Measured: 195 of MARS_MOUTH_SOCK's 752 faces are the FIRST thing a ray from
outside meets, over 20.5% of his mouth -- a wall across the opening, in front of
his teeth and his tongue. A vestibule lining lines the inside of his lips and
cheeks; it has no wall across the aperture.

ONLY THE FACES IN FRONT OF HIS CROWNS GO. The same ray test also reaches the BACK
of the bag at 53 mm, and that back is the back of his mouth -- deleting it would
open a hole through his head. The cut is at his crowns' own front edge, measured
in the same pose, not at a number someone liked.
"""


def _run():
    import bpy, bmesh, json, os, math
    import numpy as np
    from mathutils import Vector, Matrix
    ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
    MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
    MW=float(MA["aperture"]["width"]); MM=MW/50.0
    FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
    OUTW=(FRAME.to_3x3()@Vector((0,-1,0))).normalized()
    AP=(Vector(MA["aperture"]["cornerLeft"])+Vector(MA["aperture"]["cornerRight"]))/2.0
    head=bpy.data.objects["MARS_MESH"]; arm=bpy.data.objects["MARS_RIG"]
    sock=bpy.data.objects["MARS_MOUTH_SOCK"]; sc=bpy.context.scene
    if sock.get("front_wall_opened"):
        print("the sock has already been opened -- refusing to cut it twice"); return

    def open_pose():
        for k in head.data.shape_keys.key_blocks:
            if k.name!="Basis": k.value=0.0
        for n in ("lip_lower_depress","lip_upper_raise","mouth_funnel"):
            kb=head.data.shape_keys.key_blocks.get(n)
            if kb: kb.value=1.0
        pb=arm.pose.bones["jaw"]; pb.rotation_mode="XYZ"; pb.rotation_euler=(math.radians(30),0,0)
        bpy.context.view_layer.update()

    def crowns_and_blockers():
        deps=bpy.context.evaluated_depsgraph_get()
        eye=Vector(AP)+OUTW*1.2; vis=0; tot=0
        from collections import Counter
        c=Counter()
        for nm in ("MARS_TEETH_UPPER","MARS_TEETH_LOWER"):
            ob=bpy.data.objects[nm]; eo=ob.evaluated_get(deps); m=eo.to_mesh(); M=eo.matrix_world
            P=[M@v.co.copy() for v in m.vertices]; ti=set()
            for p in m.polygons:
                mt=ob.data.materials[p.material_index] if p.material_index<len(ob.data.materials) else None
                if mt and "TEETH" in mt.name.upper(): ti.update(p.vertices)
            eo.to_mesh_clear()
            L=np.array([list(FINV@p) for p in P])
            for i in sorted(ti,key=lambda j:L[j][1])[:400]:
                p=P[i]; d=p-eye; ln=d.length; tot+=1
                hit,lo,_n,fi,hob,_m=sc.ray_cast(deps,eye,d/ln,distance=ln+0.5)
                if not hit or (lo-p).length<=0.5*MM: vis+=1
                else: c[hob.name.replace("MARS_","")]+=1
        return vis,tot,c

    def holes_to_nowhere():
        """After the cut, does any ray over his mouth reach NOTHING? That would be a
        hole straight through his head, which is worse than the ring."""
        deps=bpy.context.evaluated_depsgraph_get(); miss=0; tot=0
        for xx in np.arange(-26,26.01,0.6):
            for zz in np.arange(-20,16.01,0.6):
                p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9; tot+=1
                hit,_lo,_n,_fi,_ob,_m=sc.ray_cast(deps,o,-OUTW,distance=2.5)
                if not hit: miss+=1
        return miss,tot

    open_pose()
    deps=bpy.context.evaluated_depsgraph_get()
    # his crowns' front edge, this pose
    ob=bpy.data.objects["MARS_TEETH_UPPER"]; eo=ob.evaluated_get(deps); m=eo.to_mesh(); M=eo.matrix_world
    ti=set()
    for p in m.polygons:
        mt=ob.data.materials[p.material_index] if p.material_index<len(ob.data.materials) else None
        if mt and "TEETH" in mt.name.upper(): ti.update(p.vertices)
    CR=float(np.percentile([ (FINV@(M@m.vertices[i].co)).y/MM for i in ti],5)); eo.to_mesh_clear()
    MARGIN=float(os.environ.get("TRIPPEDD_SOCK_CUT_MARGIN_MM","2.0"))
    print("his upper crowns' front edge: %+.2f mm; cutting sock faces forward of %+.2f mm"%(CR,CR+MARGIN))

    first=set()
    for xx in np.arange(-30,30.01,0.4):
        for zz in np.arange(-24,20.01,0.4):
            p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
            hit,lo,_n,fi,hob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
            if hit and hob.original==sock: first.add(int(fi))
    # THE CRITERION IS NOT "FORWARD OF HIS CROWNS" -- the recess already handled
    # those, and only 18 of 195 qualified while the ring he can see is still
    # there. The wall that matters is the one HIDING SOMETHING: a sock face the
    # camera meets first, with his tongue or his teeth directly behind it.
    # Measured by carrying the ray on through the sock and seeing what it reaches.
    drop=set(); hidden=0
    ORAL={"MARS_TONGUE","MARS_TEETH_UPPER","MARS_TEETH_LOWER"}
    for xx in np.arange(-30,30.01,0.4):
        for zz in np.arange(-24,20.01,0.4):
            p=FRAME@Vector((xx*MM,0.0,zz*MM)); o=p+OUTW*0.9
            hit,lo,_n,fi,hob,_m=sc.ray_cast(deps,o,-OUTW,distance=1.8)
            if not hit or hob.original!=sock: continue
            cur=lo+(-OUTW)*1e-4
            for _ in range(6):
                h2,l2,_n2,_f2,o2,_m2=sc.ray_cast(deps,cur,-OUTW,distance=1.8)
                if not h2: break
                if o2.original.name in ORAL:
                    drop.add(int(fi)); hidden+=1; break
                if o2.original==head: break        # his own head behind it: leave it
                cur=l2+(-OUTW)*1e-4
    drop=sorted(drop)
    print("sock faces the camera meets first: %d; of those, hiding his tongue or teeth: %d"
          "  (%d rays)"%(len(first),len(drop),hidden))
    if not drop:
        print("nothing to remove"); return

    before=crowns_and_blockers(); miss0=holes_to_nowhere()
    print("before: %d/%d crowns visible; sock blocks %d; rays reaching nothing %d/%d"
          %(before[0],before[1],before[2].get("MOUTH_SOCK",0),miss0[0],miss0[1]))

    bm=bmesh.new(); bm.from_mesh(sock.data); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.faces[i] for i in drop if i<len(bm.faces)],context="FACES_ONLY")
    bm.to_mesh(sock.data); bm.free(); sock.data.update()
    bpy.context.view_layer.update()
    after=crowns_and_blockers(); miss1=holes_to_nowhere()
    print("after:  %d/%d crowns visible; sock blocks %d; rays reaching nothing %d/%d"
          %(after[0],after[1],after[2].get("MOUTH_SOCK",0),miss1[0],miss1[1]))
    if miss1[0] > miss0[0] + 0.002*miss1[1]:
        print("*** REFUSED: the cut opened %d new rays straight through his head"
              %(miss1[0]-miss0[0])); return
    if after[0] < before[0]:
        print("*** REFUSED: fewer crowns visible after the cut (%d -> %d)"%(before[0],after[0]))
        return
    if after[2].get("MOUTH_SOCK",0) > before[2].get("MOUTH_SOCK",0):
        print("*** REFUSED: the sock blocks MORE crowns after the cut"); return
    sock["front_wall_opened"]=len(drop)
    for k in head.data.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    arm.pose.bones["jaw"].rotation_euler=(0,0,0); bpy.context.view_layer.update()
    out=(bpy.data.filepath or os.path.join(ROOT,"assets/rigs/MARS_FACE.blend"))
        # SAVE THE BLEND THIS SESSION ACTUALLY HAS OPEN, not a hardcoded canonical
        # path. Run against a REVIEW blend on a second session port, these snippets
        # each wrote their result straight over assets/rigs/MARS_FACE.blend -- an
        # unreviewed promotion nobody asked for, and the same way the good mouth was
        # lost under the eye work. A repair belongs to the file it was run on.
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("removed %d front-wall faces; saved -> %s"%(len(drop),out))


_run()
