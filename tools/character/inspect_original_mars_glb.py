import bpy
import os, sys, json

argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
def arg(name, default=None):
    try: return argv[argv.index(name)+1]
    except (ValueError, IndexError): return default

src=arg("--glb")
out=arg("--out","original_glb_inspection")
os.makedirs(out, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)

objects=[]
for o in bpy.context.scene.objects:
    if o.type in {"MESH","ARMATURE","EMPTY","CAMERA","LIGHT"}:
        objects.append({
            "name":o.name,
            "type":o.type,
            "verts":sum(len(p.vertices) for p in o.data.polygons) if o.type=="MESH" else None,
            "polygons":len(o.data.polygons) if o.type=="MESH" else None,
            "materials":[m.name if m else None for m in o.data.materials] if o.type=="MESH" else [],
        })
with open(os.path.join(out,"inventory.json"),"w") as f:
    json.dump(objects,f,indent=2)

# Save an inspectable Blender conversion without modifying imported geometry.
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,"MARS_FACE_original_GLB_import.blend"))
print(json.dumps(objects,indent=2))
