#!/usr/bin/env python3
"""Read-only 3D asset intake audit using Blender headless mode.

Usage:
  blender -b --python tools/asset_pipeline/scan_head.py -- /path/to/head.glb
"""
from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

BLENDER_SCRIPT = r'''
import bpy, json, sys
from mathutils import Vector
src = sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.read_factory_settings(use_empty=True)
ext = src.lower().rsplit(".",1)[-1]
if ext in {"glb","gltf"}: bpy.ops.import_scene.gltf(filepath=src)
elif ext == "fbx": bpy.ops.import_scene.fbx(filepath=src)
elif ext == "obj": bpy.ops.wm.obj_import(filepath=src)
elif ext in {"usd","usdz"}: bpy.ops.wm.usd_import(filepath=src)
elif ext == "blend": bpy.ops.wm.open_mainfile(filepath=src)
else: raise SystemExit("unsupported extension: "+ext)

meshes=[]; bones=[]; shape_keys=[]
mins=Vector((1e30,1e30,1e30)); maxs=Vector((-1e30,-1e30,-1e30))
for o in bpy.context.scene.objects:
    if o.type=="MESH":
        omin=Vector((1e30,1e30,1e30)); omax=Vector((-1e30,-1e30,-1e30))
        for c in o.bound_box:
            p=o.matrix_world @ Vector(c)
            omin=Vector((min(omin.x,p.x),min(omin.y,p.y),min(omin.z,p.z)))
            omax=Vector((max(omax.x,p.x),max(omax.y,p.y),max(omax.z,p.z)))
        mins=Vector((min(mins.x,omin.x),min(mins.y,omin.y),min(mins.z,omin.z)))
        maxs=Vector((max(maxs.x,omax.x),max(maxs.y,omax.y),max(maxs.z,omax.z)))
        sk=list(o.data.shape_keys.key_blocks.keys()) if o.data.shape_keys else []
        shape_keys += [{"object":o.name,"name":k} for k in sk]
        meshes.append({"name":o.name,"vertices":len(o.data.vertices),"polygons":len(o.data.polygons),"materials":[m.name for m in o.data.materials],"shape_keys":sk})
    elif o.type=="ARMATURE":
        bones += [b.name for b in o.data.bones]
dims=maxs-mins
print(json.dumps({"source":src,"objects":len(bpy.context.scene.objects),"meshes":meshes,"bones":bones,"shape_keys":shape_keys,"bounds":{"min":list(mins),"max":list(maxs),"dimensions":list(dims)}}))
'''

def main():
    if "--" not in sys.argv or len(sys.argv) < sys.argv.index("--")+2:
        raise SystemExit("asset path required")
    src=Path(sys.argv[sys.argv.index("--")+1]).resolve()
    if not src.exists(): raise SystemExit(f"asset not found: {src}")
    out=Path("build/asset_audits"); out.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile("w",suffix=".py",delete=False) as f:
        f.write(BLENDER_SCRIPT); helper=f.name
    try:
        r=subprocess.run(["blender","-b","--python",helper,"--",str(src)],text=True,capture_output=True)
        if r.returncode: raise SystemExit(r.stderr[-4000:])
        line=next((x for x in r.stdout.splitlines() if x.startswith("{")),None)
        if not line: raise SystemExit("Blender returned no JSON audit")
        data=json.loads(line)
        data["source_sha256"]=hashlib.sha256(src.read_bytes()).hexdigest()
        target=out/(src.stem+".json"); target.write_text(json.dumps(data,indent=2))
        print(target)
    finally:
        Path(helper).unlink(missing_ok=True)

if __name__=="__main__": main()
