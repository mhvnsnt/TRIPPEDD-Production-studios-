#!/usr/bin/env python3
import bpy, math, os
from mathutils import Vector

OUT = os.environ.get("TRIPPEDD_IDENT_FRAME_DIR", "/tmp/trippedd-ident-frames")
os.makedirs(OUT, exist_ok=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 480
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.filepath = os.path.join(OUT, "frame_")
scene.render.film_transparent = False
scene.world.color = (0.003, 0.001, 0.008)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

def mat(name, color, metallic=0.0, rough=0.35, emission=0.0):
    m=bpy.data.materials.new(name=name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Metallic"].default_value=metallic
    bs.inputs["Roughness"].default_value=rough
    if emission:
        bs.inputs["Emission Color"].default_value=(*color,1)
        bs.inputs["Emission Strength"].default_value=emission
    return m

white=mat("white",(0.95,0.95,1.0),0.1,0.25,0.5)
red=mat("bastard_red",(0.65,0.015,0.008),0.25,0.3,0.8)
orange=mat("bastard_orange",(1.0,0.18,0.015),0.1,0.25,1.4)
green=mat("bush_green",(0.01,0.55,0.08),0.15,0.3,0.8)
lime=mat("bush_lime",(0.45,1.0,0.02),0.0,0.25,1.2)
blue=mat("molecule_blue",(0.015,0.22,1.0),0.3,0.2,1.8)
pink=mat("molecule_pink",(1.0,0.02,0.52),0.15,0.22,1.6)
purple=mat("network_purple",(0.32,0.01,0.9),0.35,0.25,1.6)
cyan=mat("network_cyan",(0.0,0.75,1.0),0.25,0.2,1.8)

def cube(name,loc,scale,material,bevel=0.12):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    b=o.modifiers.new("soft_edges","BEVEL"); b.width=bevel; b.segments=3
    o.data.materials.append(material); return o

def sphere(name,loc,scale,material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material); return o

def torus(name,loc,major,minor,material):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=48, minor_segments=12, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(material); return o

def text(name,body,loc,size,material,extrude=0.025):
    c=bpy.data.curves.new(name,"FONT"); c.body=body; c.align_x="CENTER"; c.align_y="CENTER"
    c.size=size; c.extrude=extrude; c.bevel_depth=0.008
    o=bpy.data.objects.new(name,c); bpy.context.collection.objects.link(o); o.location=loc
    o.data.materials.append(material); return o

def active(o,start,end):
    o.hide_render=True; o.keyframe_insert(data_path="hide_render",frame=max(1,start-1))
    o.hide_render=False; o.keyframe_insert(data_path="hide_render",frame=start)
    o.hide_render=False; o.keyframe_insert(data_path="hide_render",frame=end)
    o.hide_render=True; o.keyframe_insert(data_path="hide_render",frame=min(480,end+1))

def point_at(o,target):
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()

bpy.ops.object.camera_add(location=(0,-18,3.8))
cam=bpy.context.object; scene.camera=cam; cam.data.lens=52
for f,loc in [(1,(0,-18,3.8)),(120,(2.5,-16,4.6)),(240,(-2.5,-17,3.0)),(360,(2,-16,4.2)),(480,(-1.5,-18,3.5))]:
    cam.location=loc; point_at(cam,(0,0,0.2)); cam.keyframe_insert(data_path="location",frame=f); cam.keyframe_insert(data_path="rotation_euler",frame=f)

for loc,energy,color,size in [
    ((-7,-8,8),1900,(1,0.03,0.06),6),((7,-6,5),1700,(0.04,0.25,1),5),((0,2,10),1300,(0.45,0.04,1),4)
]:
    bpy.ops.object.light_add(type="AREA",location=loc)
    l=bpy.context.object; l.data.energy=energy; l.data.color=color; l.data.shape="DISK"; l.data.size=size; point_at(l,(0,0,0))

brand=text("brand","TRIPPEDD",(0,1.3,2.6),1.18,white,0.045)
brand.rotation_euler=(math.radians(78),0,0); brand.keyframe_insert(data_path="rotation_euler",frame=1)
brand.rotation_euler.z=math.tau; brand.keyframe_insert(data_path="rotation_euler",frame=480)
net=text("network","NETWORK",(0,1.35,1.55),0.38,cyan,0.018); net.rotation_euler=(math.radians(78),0,0)

specs=[("THE BASTARD",1,120,orange),("IN THE BUSHES",121,240,lime),("GOD MOLECULE",241,360,pink),("TRIPPEDD",361,480,cyan)]
for i,(body,s,e,m) in enumerate(specs):
    t=text("title_"+str(i),body,(0,1.25,-1.5),0.72,m,0.035); t.rotation_euler=(math.radians(78),0,0); active(t,s,e)

for i in range(8):
    a=i*math.tau/8
    o=cube("b_"+str(i),(math.cos(a)*4.4,0,math.sin(a)*2.6),(.58,.58,.58),red if i%2 else orange)
    o.rotation_euler=(a,a*0.5,a*0.2); o.keyframe_insert(data_path="rotation_euler",frame=1)
    o.rotation_euler.x+=math.tau; o.rotation_euler.y+=math.pi; o.keyframe_insert(data_path="rotation_euler",frame=120); active(o,1,120)
r=torus("b_ring",(0,0,0),3.2,.18,orange); r.keyframe_insert(data_path="rotation_euler",frame=1)
r.rotation_euler=(math.pi,math.tau,math.pi/2); r.keyframe_insert(data_path="rotation_euler",frame=120); active(r,1,120)

for i in range(22):
    a=i*math.tau/22
    o=sphere("leaf_"+str(i),(math.cos(a)*4.2,0,math.sin(a)*2.6),(0.5,0.32,0.95),green if i%2 else lime)
    o.rotation_euler=(0,a,0); o.keyframe_insert(data_path="location",frame=121)
    o.location.z+=0.8*math.sin(a); o.keyframe_insert(data_path="location",frame=240); active(o,121,240)
for i in range(9):
    o=cube("bush_bar_"+str(i),(-6+i*1.5,0,-2.1),(.5,.18,.12),lime); active(o,121,240)

atoms=[(-2.8,0,0,blue),(0,0,2.1,pink),(2.8,0,0,blue),(0,0,-2.1,pink),(0,0,0,white)]
for i,(x,y,z,m) in enumerate(atoms):
    o=sphere("atom_"+str(i),(x,y,z),(0.62,0.62,0.62),m)
    o.keyframe_insert(data_path="rotation_euler",frame=241); o.rotation_euler=(math.tau,math.pi,math.pi/2)
    o.keyframe_insert(data_path="rotation_euler",frame=360); active(o,241,360)
for i in range(3):
    o=torus("m_ring_"+str(i),(0,0,0),2.8+i*.28,.105,blue if i%2==0 else pink)
    o.rotation_euler=(i*.6,i*.8,i*.4); o.keyframe_insert(data_path="rotation_euler",frame=241)
    o.rotation_euler.x+=math.pi; o.rotation_euler.y+=math.tau; o.keyframe_insert(data_path="rotation_euler",frame=360); active(o,241,360)

for i in range(7):
    o=cube("net_"+str(i),((i-3)*1.7,0,(i%2)*1.8-0.9),(.58,.58,.58),cyan if i%2 else purple)
    o.keyframe_insert(data_path="rotation_euler",frame=361); o.rotation_euler=(math.pi*1.5,math.tau,math.pi)
    o.keyframe_insert(data_path="rotation_euler",frame=480); active(o,361,480)
for i in range(3):
    o=torus("net_ring_"+str(i),(0,0,0),2.0+i*.65,.12,purple if i%2 else cyan)
    o.rotation_euler=(i*.5,0,i*.8); o.keyframe_insert(data_path="rotation_euler",frame=361)
    o.rotation_euler.x+=math.pi; o.rotation_euler.z+=math.tau; o.keyframe_insert(data_path="rotation_euler",frame=480); active(o,361,480)

scene.use_nodes=True
nt=scene.node_tree; nt.nodes.clear()
rl=nt.nodes.new("CompositorNodeRLayers"); glare=nt.nodes.new("CompositorNodeGlare")
glare.glare_type="FOG_GLOW"; glare.quality="HIGH"; glare.threshold=0.7; glare.size=7
comp=nt.nodes.new("CompositorNodeComposite"); nt.links.new(rl.outputs["Image"],glare.inputs["Image"]); nt.links.new(glare.outputs["Image"],comp.inputs["Image"])
try: scene.view_settings.look="AgX - Medium High Contrast"
except Exception: pass
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,"trippedd-ident.blend"))
bpy.ops.render.render(animation=True)
