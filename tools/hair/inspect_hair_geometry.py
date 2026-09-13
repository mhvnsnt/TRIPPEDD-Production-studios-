import bpy, sys, os
import numpy as np
from mathutils import Vector as V, Matrix as M
R='/home/user/TRIPPEDD-Production-studios-/'
sys.path.insert(0,R+'tools/character'); import face_plate as FP
OUT=R+'docs/evidence/hair'; os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=R+'assets/source_models/MARS_source.glb')
o=max([x for x in bpy.data.objects if x.type=='MESH'],key=lambda x:len(x.data.vertices))
sc=bpy.context.scene
# FLAT CLAY: kill the texture entirely. A photogrammetry texture can paint strand
# detail onto geometry that has none, and that is exactly the question here.
for m in bpy.data.materials:
    if not m.use_nodes: continue
    for nd in m.node_tree.nodes:
        if nd.type!='BSDF_PRINCIPLED': continue
        for k,v in (("Specular IOR Level",0.15),("Roughness",0.85),("Metallic",0.0)):
            if k in nd.inputs:
                for l in list(nd.inputs[k].links): m.node_tree.links.remove(l)
                nd.inputs[k].default_value=v
        if "Base Color" in nd.inputs:
            for l in list(nd.inputs["Base Color"].links): m.node_tree.links.remove(l)
            nd.inputs["Base Color"].default_value=(0.55,0.55,0.57,1)
        if "Normal" in nd.inputs:
            for l in list(nd.inputs["Normal"].links): m.node_tree.links.remove(l)
sc.render.engine="BLENDER_EEVEE_NEXT"; sc.render.resolution_x=sc.render.resolution_y=900
sc.view_settings.view_transform="Standard"
w=bpy.data.worlds.new("W"); sc.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[0].default_value=(0.05,0.05,0.06,1)
w.node_tree.nodes["Background"].inputs[1].default_value=0.5
fit,sets,canon=FP.load_fit(R); x,up,fwd=FP.head_frame(sets)
V0=[o.matrix_world @ v.co for v in o.data.vertices]
P=np.array([[p.x,p.y,p.z] for p in V0]); C=P.mean(0); rad=float(np.linalg.norm(P-C,axis=1).max())
def light(nm,d,e):
    L=bpy.data.lights.new(nm,type="AREA"); L.energy=e; L.size=rad*2
    ob=bpy.data.objects.new(nm,L); sc.collection.objects.link(ob)
    ob.location=tuple(C+d*rad*2.5)
    ob.rotation_euler=(V(tuple(C))-V(ob.location)).to_track_quat("-Z","Y").to_euler()
light("k",(x*0.6+up*0.8+fwd*0.6),300); light("f",(-x*0.9+up*0.2+fwd*0.3),150)
light("r",(-fwd*1.0+up*0.5),200)
VIEWS={"TOP":(up, -fwd), "BACK":(-fwd, up), "SIDE":(x, up), "THREEQ":((x*0.8-fwd*0.8+up*0.3), up)}
for nm,(dirv,upv) in VIEWS.items():
    d=np.array(dirv,dtype=float); d/=np.linalg.norm(d)
    u=np.array(upv,dtype=float); u-=d*np.dot(u,d); u/=np.linalg.norm(u)
    r=np.cross(u,d)
    cd=bpy.data.cameras.new(nm); cd.type="ORTHO"; cd.ortho_scale=rad*2.15
    cam=bpy.data.objects.new(nm,cd); sc.collection.objects.link(cam)
    org=C+d*rad*3
    cam.matrix_world=M(((r[0],u[0],d[0],org[0]),(r[1],u[1],d[1],org[1]),(r[2],u[2],d[2],org[2]),(0,0,0,1)))
    sc.camera=cam; sc.render.filepath=os.path.join(OUT,"HAIR_CLAY_%s.png"%nm)
    bpy.ops.render.render(write_still=True)
    print("  rendered",nm,flush=True)
print("-> docs/evidence/hair/")
