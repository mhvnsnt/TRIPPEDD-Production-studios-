"""Recess MARS_MOUTH_SOCK behind his crowns, by measurement rather than by a number
someone liked. Measured defects it addresses: the sock front edge sits 1.28 mm IN
FRONT of his upper crowns (so it clips them -- 7% of all crown rays), and 9 of its
vertices are through HIS SKIN by up to 3.25 mm."""


def _run():
    import bpy, json, os, math
    import numpy as np
    from mathutils import Vector, Matrix
    ROOT=os.environ.get("TRIPPEDD_ROOT","/home/user/TRIPPEDD-Production-studios-")
    MA=json.load(open(os.path.join(ROOT,"renders/_rig_measure/mouth_anatomy.json")))
    MW=float(MA["aperture"]["width"]); MM=MW/50.0
    FRAME=Matrix(MA["frame"]["matrix"]); FINV=FRAME.inverted()
    DEEPER=(FRAME.to_3x3()@Vector((0,1,0))).normalized()     # into his mouth
    sock=bpy.data.objects["MARS_MOUTH_SOCK"]; head=bpy.data.objects["MARS_MESH"]
    arm=bpy.data.objects["MARS_RIG"]
    if sock.get("recessed"):
        print("sock already recessed -- refusing to move it twice"); return
    for k in head.data.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    for n in ("lip_lower_depress","lip_upper_raise","mouth_funnel"):
        kb=head.data.shape_keys.key_blocks.get(n)
        if kb: kb.value=1.0
    pb=arm.pose.bones["jaw"]; pb.rotation_mode="XYZ"; pb.rotation_euler=(math.radians(30),0,0)
    bpy.context.view_layer.update()
    def front(nm, matf=None):
        deps=bpy.context.evaluated_depsgraph_get()
        ob=bpy.data.objects[nm]; eo=ob.evaluated_get(deps); m=eo.to_mesh(); M=eo.matrix_world
        keep=None
        if matf:
            keep=set()
            for p in m.polygons:
                mt=ob.data.materials[p.material_index] if p.material_index<len(ob.data.materials) else None
                if mt and matf in mt.name.upper(): keep.update(p.vertices)
        P=np.array([list(FINV@(M@v.co)) for i,v in enumerate(m.vertices) if keep is None or i in keep])/MM
        eo.to_mesh_clear(); return float(np.percentile(P[:,1],5))
    crown=front("MARS_TEETH_UPPER","TEETH"); s0=front("MARS_MOUTH_SOCK")
    MARGIN=float(os.environ.get("TRIPPEDD_SOCK_MARGIN_MM","1.0"))
    need=(crown-s0)+MARGIN
    print("upper crowns front %+.2f mm, sock front %+.2f mm -> moving the sock %+.2f mm deeper"
          %(crown,s0,need))
    if need<=0:
        print("the sock is already behind his crowns -- nothing to do"); return
    sock.location = sock.location + DEEPER*(need*MM)
    bpy.context.view_layer.update()
    s1=front("MARS_MOUTH_SOCK")
    print("sock front now %+.2f mm (crowns %+.2f) -> %.2f mm behind them"%(s1,crown,s1-crown))
    if s1 < crown:
        sock.location = sock.location - DEEPER*(need*MM); bpy.context.view_layer.update()
        print("*** REFUSED: the move did not put it behind his crowns; reverted"); return
    sock["recessed"]=round(need,4)
    for k in head.data.shape_keys.key_blocks:
        if k.name!="Basis": k.value=0.0
    pb.rotation_euler=(0,0,0); bpy.context.view_layer.update()
    out=os.path.join(ROOT,"assets/rigs/MARS_FACE.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("saved -> %s"%out)


_run()
