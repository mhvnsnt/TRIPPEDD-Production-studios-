"""Render and structurally audit the original-GLB oral recovery candidate.

This is deliberately independent of mouth_proof.py: the recovery gate must be able
to show the actual candidate pixels and audit the whole oral region, not only the
lip aperture or material ray counts.
"""
import bpy, os, sys, json, math, bmesh
from mathutils import Vector

argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
def opt(k,d): return argv[argv.index(k)+1] if k in argv else d
RIG=os.path.abspath(opt("--rig","MARS_FACE_ORIGINAL_GLB_ORAL_REVIEW.blend"))
OUT=os.path.abspath(opt("--out","oral_candidate_render"))
os.makedirs(OUT,exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=RIG)
scene=bpy.context.scene
head=bpy.data.objects.get("MARS_MESH")
arm=bpy.data.objects.get("MARS_RIG")
if not head or not arm:
    raise SystemExit("candidate missing MARS_MESH/MARS_RIG")

state={}
state_path="assets/rigs/MARS_face_state.json"
if os.path.exists(state_path):
    state=json.load(open(state_path))
sign=state.get("jawHinge",{}).get("openSign",1)

# Geometry audit: count the actual failure modes seen in the broken mouth.
def mesh_audit(o):
    me=o.data
    bm=bmesh.new(); bm.from_mesh(me); bm.edges.ensure_lookup_table(); bm.verts.ensure_lookup_table()
    loose=sum(1 for v in bm.verts if not v.link_edges)
    nonmanifold=sum(1 for e in bm.edges if not e.is_manifold)
    zero=0
    for f in bm.faces:
        if f.calc_area() < 1e-10: zero+=1
    bm.free()
    weighted=0
    if o.vertex_groups:
        for v in me.vertices:
            if any(g.group>=0 and g.weight>1e-6 for g in v.groups): weighted+=1
    return {"verts":len(me.vertices),"edges":len(me.edges),"faces":len(me.polygons),
            "loose_vertices":loose,"nonmanifold_edges":nonmanifold,
            "zero_area_faces":zero,"weighted_vertices":weighted,
            "weighted_percent":round(100*weighted/max(1,len(me.vertices)),2),
            "materials":[m.name if m else "" for m in me.materials]}

oral_names=["MARS_MOUTH_SOCK","MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE"]
audit={}
for n in ["MARS_MESH"]+oral_names:
    o=bpy.data.objects.get(n)
    if o and o.type=="MESH": audit[n]=mesh_audit(o)

# Apply the actual wide pose from the current rig. Never alter the host topology.
kb=head.data.shape_keys.key_blocks if head.data.shape_keys else []
for k in kb:
    if k.name!="Basis": k.value=0
if head.data.shape_keys:
    for n,v in {"lip_lower_depress":0.7,"lip_upper_raise":0.45,
                "lip_corner_L_up":0.2,"lip_corner_R_up":0.2}.items():
        if n in head.data.shape_keys.key_blocks: head.data.shape_keys.key_blocks[n].value=v
for b in arm.pose.bones:
    b.rotation_mode="XYZ"; b.rotation_euler=(0,0,0)
if "jaw" in arm.pose.bones:
    arm.pose.bones["jaw"].rotation_euler=(math.radians(sign*31.0),0,0)
if "tongue_root" in arm.pose.bones: arm.pose.bones["tongue_root"].rotation_euler=(math.radians(-14),0,0)
if "tongue_mid" in arm.pose.bones: arm.pose.bones["tongue_mid"].rotation_euler=(math.radians(-8),0,0)
bpy.context.view_layer.update()

# Camera framing is derived from the measured face bounds rather than arbitrary
# object bounds so the result can be compared with the Sep 12 anchor.
face_path="docs/evidence/linework/face_anatomy.json"
face=json.load(open(face_path)) if os.path.exists(face_path) else {}
centre=Vector(face.get("bounds",{}).get("centre",[0,0,0]))
size=Vector(face.get("bounds",{}).get("size",[1,1,1]))
head_h=size.z
mouth=Vector([-0.021031,-0.417486,0.231635])

def camera(name,loc,target,lens):
    d=bpy.data.cameras.new(name); d.lens=lens
    o=bpy.data.objects.new(name,d); scene.collection.objects.link(o)
    o.location=loc; o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat("-Z","Y").to_euler()
    return o

cams={
 "front":camera("RECOVERY_FRONT",(centre.x+0.18,centre.y-2.35,centre.z+head_h*.10),
                (centre.x,centre.y,centre.z+head_h*.02),85),
 "mouth":camera("RECOVERY_MOUTH",tuple(mouth+Vector((.05,-.85,.10))),mouth,50),
 "profile":camera("RECOVERY_PROFILE",(centre.x-2.30,centre.y-.05,centre.z),centre,70)
}
scene.render.engine="BLENDER_EEVEE_NEXT"
scene.render.resolution_x=scene.render.resolution_y=900
scene.render.film_transparent=False
scene.render.image_settings.file_format="PNG"

world=bpy.data.worlds.get("RECOVERY_WORLD") or bpy.data.worlds.new("RECOVERY_WORLD")
scene.world=world; world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.012,.014,.022,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.7

def light(name,loc,target,energy,size,color=(1,1,1)):
    d=bpy.data.lights.get(name) or bpy.data.lights.new(name,"AREA")
    d.energy=energy; d.shape="DISK"; d.size=size; d.color=color
    o=bpy.data.objects.get(name) or bpy.data.objects.new(name,d)
    if o.name not in scene.objects: scene.collection.objects.link(o)
    o.location=loc; o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat("-Z","Y").to_euler()
light("REC_KEY",(-1.05,-1.55,1.35),centre+Vector((0,0,.05)),260,1.1,(1,.96,.92))
light("REC_FILL",(1.30,-1.25,.55),centre+Vector((0,0,.05)),90,1.4,(.72,.82,1))
light("REC_MOUTH",tuple(mouth+Vector((.05,-.55,.10))),mouth,22,.30,(1,.93,.88))

# Render the requested WIDE pose with the source tongue controls, then a host-rig
# neutral-tongue control pass. The latter isolates armature-axis incompatibility
# without changing any mesh, weights, or host topology.
for tag,cam in cams.items():
    scene.camera=cam
    scene.render.filepath=os.path.join(OUT,"03_WIDE_"+tag+".png")
    bpy.ops.render.render(write_still=True)
if "tongue_root" in arm.pose.bones: arm.pose.bones["tongue_root"].rotation_euler=(0,0,0)
if "tongue_mid" in arm.pose.bones: arm.pose.bones["tongue_mid"].rotation_euler=(0,0,0)
bpy.context.view_layer.update()
scene.camera=cams["mouth"]
scene.render.filepath=os.path.join(OUT,"03_WIDE_mouth_neutral_tongue.png")
bpy.ops.render.render(write_still=True)

report={"status":"REVIEW_ONLY","rig":RIG,"pose":{"jawDeg":31,
 "shapeKeys":{n:v for n,v in {"lip_lower_depress":.7,"lip_upper_raise":.45,
 "lip_corner_L_up":.2,"lip_corner_R_up":.2}.items() if n in head.data.shape_keys.key_blocks},
 "tongueBones":{"tongue_root":-14,"tongue_mid":-8}},
 "audit":audit,
 "objects":{n:{"type":o.type,"verts":len(o.data.vertices) if o.type=="MESH" else None}
             for n,o in bpy.data.objects.items() if n in ["MARS_MESH"]+oral_names}}
with open(os.path.join(OUT,"oral_candidate_structural_audit.json"),"w") as f: json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
