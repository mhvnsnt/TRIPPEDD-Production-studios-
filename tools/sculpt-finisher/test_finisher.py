# Headless proof test for Sculpt Finisher (Z-2) + FlowRetopo (Z-1).
#
# Run (Blender 4.5.3 on this studio box):
#   flock /tmp/heavy-test.lock bash -c \
#     'xvfb-run -a env -u PYTHONPATH <blender> -b --factory-startup \
#        --python test_finisher.py -- --out <output_dir>'
#
# Builds a blobby test sculpt (icosphere + Clouds displacement + painted
# vertex-color "Density"), then:
#   1. Z-2: runs the full Finisher chain on it; asserts the chain finished,
#      the ORIGINAL is untouched, a *_FINISHED duplicate exists, the GLB
#      export and all three baked maps (Normal/AO/Color) exist on disk
#      with nonzero size.
#   2. Z-1: runs FlowRetopo; asserts a *_RETOPO result exists and the log
#      line carries the mesh check + the honest Instant Meshes status.
#   3. Fail-soft probe: re-runs Z-2 with the export dir pointed at an
#      existing FILE; asserts the chain stops at the export step, reports
#      CANCELLED, renames the duplicate *_FAILED_export and leaves the
#      original untouched.
# Prints TEST_RESULT lines and writes results.json into the output dir.
# Exit code is non-zero (via an uncaught AssertionError) on any failure.

import json
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sculpt_finisher  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/sf_test_out"
os.makedirs(OUT, exist_ok=True)

results = {}


def check(name, cond, detail=""):
    results[name] = {"pass": bool(cond), "detail": detail}
    print(f"TEST_RESULT {name}: {'PASS' if cond else 'FAIL'} {detail}",
          flush=True)
    assert cond, f"{name}: {detail}"


sculpt_finisher.register()

# --- Build the blobby test sculpt -------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=1.0)
sculpt = bpy.context.active_object
sculpt.name = "BlobSculpt"

tex = bpy.data.textures.new("BlobNoise", type='CLOUDS')
tex.noise_scale = 0.35
mod = sculpt.modifiers.new("BlobDisplace", 'DISPLACE')
mod.texture = tex
mod.strength = 0.3
bpy.ops.object.modifier_apply(modifier=mod.name)

# Painted vertex colors: doubles as the color-bake source and the Z-1
# density map (attribute literally named "Density").
attr = sculpt.data.color_attributes.new(
    name="Density", type='FLOAT_COLOR', domain='POINT')
zs = [v.co.z for v in sculpt.data.vertices]
zmin, zmax = min(zs), max(zs)
for i, v in enumerate(sculpt.data.vertices):
    t = (v.co.z - zmin) / max(1e-6, (zmax - zmin))
    attr.data[i].color = (t, 0.5, 1.0 - t, 1.0)

mat = bpy.data.materials.new("BlobMat")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes.get("Principled BSDF")
attr_node = nt.nodes.new('ShaderNodeAttribute')
attr_node.attribute_name = "Density"
nt.links.new(attr_node.outputs['Color'], bsdf.inputs['Base Color'])
sculpt.data.materials.append(mat)

before_verts = len(sculpt.data.vertices)
before_check = sculpt_finisher.mesh_check(sculpt)
print(f"TEST sculpt built: {sculpt_finisher.format_check(before_check)}",
      flush=True)

s = bpy.context.scene.sculpt_finisher
s.voxel_size = 0.12
s.target_faces = 1500
s.multires_levels = 1
s.bake_resolution = 512
s.bake_samples = 8
s.bake_ray_distance = 0.3
s.bake_dir = os.path.join(OUT, "bakes")
s.export_dir = os.path.join(OUT, "export")
s.export_preset = 'GAME_GLB'

# --- 1. Z-2 full chain --------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')
sculpt.select_set(True)
bpy.context.view_layer.objects.active = sculpt
res = bpy.ops.object.sculpt_finisher_run()
check("z2_chain_finished", res == {'FINISHED'}, f"operator returned {res}")
check("z2_original_untouched",
      len(sculpt.data.vertices) == before_verts,
      f"original verts {before_verts} -> {len(sculpt.data.vertices)}")

fin = bpy.data.objects.get("BlobSculpt_FINISHED")
check("z2_finished_object_exists", fin is not None)
fin_check = sculpt_finisher.mesh_check(fin)
print(f"TEST z2 finished check: {sculpt_finisher.format_check(fin_check)}",
      flush=True)
results["z2_before"] = before_check
results["z2_after"] = fin_check

glb = os.path.join(OUT, "export", "BlobSculpt_FINISHED.glb")
check("z2_glb_exported", os.path.isfile(glb) and os.path.getsize(glb) > 0,
      f"{glb} size={os.path.getsize(glb) if os.path.isfile(glb) else 'MISSING'}")
for suffix in ("Normal", "AO", "Color"):
    png = os.path.join(OUT, "bakes", f"BlobSculpt_FINISHED_{suffix}.png")
    check(f"z2_bake_{suffix.lower()}",
          os.path.isfile(png) and os.path.getsize(png) > 0,
          f"{png} size={os.path.getsize(png) if os.path.isfile(png) else 'MISSING'}")

# --- 2. Z-1 FlowRetopo ---------------------------------------------------------
s.target_faces = 1200
bpy.ops.object.select_all(action='DESELECT')
sculpt.select_set(True)
bpy.context.view_layer.objects.active = sculpt
res = bpy.ops.object.flow_retopo_run()
check("z1_chain_finished", res == {'FINISHED'}, f"operator returned {res}")
retopo = bpy.data.objects.get("BlobSculpt_RETOPO")
check("z1_retopo_object_exists", retopo is not None)
rt_check = sculpt_finisher.mesh_check(retopo)
print(f"TEST z1 retopo check: {sculpt_finisher.format_check(rt_check)}",
      flush=True)
results["z1_after"] = rt_check
results["z1_last_log"] = s.last_log
check("z1_instant_meshes_status_reported",
      "Instant Meshes:" in s.last_log,
      s.last_log[:200])
check("z1_mesh_checked",
      "non_manifold_edges=" in s.last_log, s.last_log[:200])

# --- 3. Fail-soft probe ----------------------------------------------------------
blocker = os.path.join(OUT, "blocker_file")
with open(blocker, "w") as fh:
    fh.write("not a directory")
s.do_bake = False
s.do_multires = False
s.export_dir = blocker  # export step must fail: cannot makedirs over a file
bpy.ops.object.select_all(action='DESELECT')
sculpt.select_set(True)
bpy.context.view_layer.objects.active = sculpt
res = bpy.ops.object.sculpt_finisher_run()
check("failsoft_returns_cancelled", res == {'CANCELLED'},
      f"operator returned {res}")
failed_obj = bpy.data.objects.get("BlobSculpt_FAILED_export")
check("failsoft_duplicate_kept_named", failed_obj is not None,
      f"objects: {[o.name for o in bpy.data.objects]}")
check("failsoft_original_still_untouched",
      len(sculpt.data.vertices) == before_verts,
      f"original verts {len(sculpt.data.vertices)}")

with open(os.path.join(OUT, "results.json"), "w") as fh:
    json.dump(results, fh, indent=2)
print("TEST_ALL_PASS", flush=True)
