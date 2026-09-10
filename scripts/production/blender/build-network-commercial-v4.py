# V4 Blender commercial builder
# Generates a real 3D mixed-media four-show ident: animated camera, emissive
# geometry, particles, depth, lighting, transitions, and four distinct worlds.
import bpy, math, os, subprocess
from mathutils import Vector

OUT=os.environ.get("TRIPPEDD_COMMERCIAL_OUTPUT","/tmp/trippedd-v4")
os.makedirs(OUT,exist_ok=True)
FPS=24; FRAMES=FPS*20
W,H=1920,1080
SHOWS=[
 ("THE BASTARD",(0.55,0.04,0.015,1),(1.0,0.25,0.08,1)),
 ("IN THE BUSHES",(0.01,0.20,0.12,1),(0.55,1.0,0.18,1)),
 ("GOD MOLECULE",(0.03,0.06,0.32,1),(1.0,0.18,0.85,1)),
 ("TRIPPEDD",(0.08,0.0,0.18,1),(0.15,0.75,1.0,1)),
]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.render.engine='BLENDER_EEVEE_NEXT'
sc.render.resolution_x=W; sc.render.resolution_y=H; sc.render.resolution_percentage=100
sc.render.fps=FPS
sc.render.image_settings.file_format='PNG'
sc.render.film_transparent=False
sc.world.color=(0,0,0)

def mat(name,c,metal=0.0,emit=0.0):
 m=bpy.data.materials.new(name); m.diffuse_color=c
 m.use_nodes=True; bs=m.node_tree.nodes.get('Principled BSDF')
 bs.inputs['Base Color'].default_value=c; bs.inputs['Metallic'].default_value=metal; bs.inputs['Roughness'].default_value=.25
 if emit:
  bs.inputs['Emission Color'].default_value=c; bs.inputs['Emission Strength'].default_value=emit
 return m

def text(body,c,size=1.0):
 cu=bpy.data.curves.new('txt','FONT'); cu.body=body; cu.align_x='CENTER'; cu.size=size; cu.extrude=.025
 ob=bpy.data.objects.new(body,cu); bpy.context.collection.objects.link(ob); ob.data.materials.append(mat('text',c,0,.8)); return ob

def cube(name,loc,scale,ma,bevel=.12):
 bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('bevel','BEVEL'); mod.width=bevel; mod.segments=3
 o.data.materials.append(ma); return o

def ico(loc,scale,ma):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=scale,location=loc); o=bpy.context.object; o.data.materials.append(ma); return o

# camera
bpy.ops.object.camera_add(location=(0,-18,7),rotation=(math.radians(72),0,0))
cam=bpy.context.object; sc.camera=cam

# lights
bpy.ops.object.light_add(type='AREA', location=(0,-4,9)); key=bpy.context.object; key.data.energy=1400; key.data.shape='DISK'; key.data.size=8
bpy.ops.object.light_add(type='AREA', location=(8,1,2)); fill=bpy.context.object; fill.data.energy=900; fill.data.size=6

worldmat=mat('World',(0.01,0.01,0.02,1))
floor=cube('floor',(0,0,-2),(14,14,.2),worldmat,0)

for si,(title,bg,fg) in enumerate(SHOWS):
 start=si*FPS*5; end=(si+1)*FPS*5
 base=mat('base'+str(si),bg,0.35,0.12); glow=mat('glow'+str(si),fg,0.15,5.0)
 # world stage ring
 for j in range(18):
  a=2*math.pi*j/18
  r=6.5
  o=ico((r*math.cos(a),r*math.sin(a),-0.2+0.25*(j%2)),.28+0.08*(j%3),glow)
  o.rotation_euler=(0,0,a)
  o.keyframe_insert('rotation_euler',frame=start); o.rotation_euler.z=a+math.pi*2; o.keyframe_insert('rotation_euler',frame=end)
 # hero geometry
 hero=cube('hero'+str(si),(0,1,1.2),(2.3,1.1,1.1),glow,.25)
 hero.rotation_euler=(0,0,0.25*si); hero.keyframe_insert('rotation_euler',frame=start)
 hero.rotation_euler=(math.pi*.55,math.pi*.35,hero.rotation_euler.z+math.pi*1.7); hero.keyframe_insert('rotation_euler',frame=end)
 # secondary orbiting objects
 for j in range(7):
  a=2*math.pi*j/7; o=ico((0,0,1.5),.35,base)
  o.location=(4*math.cos(a),4*math.sin(a),1.5+1.5*math.sin(a))
  o.keyframe_insert('location',frame=start)
  o.location=(4*math.cos(a+math.pi),4*math.sin(a+math.pi),1.5-1.5*math.sin(a))
  o.keyframe_insert('location',frame=end)
 # titles float toward camera and rotate
 t=text(title,fg,1.05); t.location=(0,-1.4,3.8); t.rotation_euler=(math.radians(90),0,0)
 t.keyframe_insert('location',frame=start); t.keyframe_insert('scale',frame=start)
 t.location.y=-.4; t.scale=(1.18,1.18,1.18); t.keyframe_insert('location',frame=start+FPS*2); t.keyframe_insert('scale',frame=start+FPS*2)
 t.location.y=.8; t.scale=(.82,.82,.82); t.keyframe_insert('location',frame=end); t.keyframe_insert('scale',frame=end)
 # camera move makes each world feel like a shot, not a card
 cam.keyframe_insert('location',frame=start)
 cam.location=(5*math.sin(si*.9),-15+si*1.3,5.5+si*.5); cam.keyframe_insert('location',frame=start+FPS*2)
 cam.location=(-4*math.cos(si*.7),-13+si*.9,7.5); cam.keyframe_insert('location',frame=end)
 # lights follow palette
 key.data.color=fg[:3]; fill.data.color=fg[:3]
 key.keyframe_insert('data',frame=start); fill.keyframe_insert('data',frame=start)

# final network lockup
lock=text('TRIPPEDD NETWORK',(0.15,0.75,1,1),1.35); lock.location=(0,0,3.5); lock.rotation_euler=(math.radians(90),0,0)
lock.keyframe_insert('scale',frame=FRAMES-48); lock.scale=(1.4,1.4,1.4); lock.keyframe_insert('scale',frame=FRAMES-1)

sc.render.filepath=os.path.join(OUT,'frame_')
sc.frame_start=1; sc.frame_end=FRAMES
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'TRIPPEDD-V4.blend'))
bpy.ops.render.render(animation=True)
