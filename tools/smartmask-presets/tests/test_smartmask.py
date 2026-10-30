"""Acceptance test for SPEC S-1 + S-2 (Ucupaint wire-in + SmartMask presets).

Run headless with the wired Blender 4.5.3 (box discipline: serialize with
flock and check free RAM first):

    flock /tmp/heavy-test.lock bash -c '
      xvfb-run -a env -u PYTHONPATH <blender-4.5.3>/blender -b \
        --factory-startup --python tests/test_smartmask.py -- --out <dir>'

What it proves, with evidence printed as TEST lines and a JSON report:
  1. Ucupaint enables and reports version 3.0.0 (from its own extension
     manifest).
  2. Each of the four SmartMask presets builds its documented layer stack
     (base coat + masked effect layer, mask names/types, modifiers) on
     its own demo prop.
  3. Every preset's Ucupaint node group exports a baked Base Color
     texture without error, and the baked texture has real pixel
     variation (per-channel std-dev above a floor) - i.e. the
     mesh-driven masks actually modulate the stack, not sit inert.
  4. A preset library .blend (four demo props, one preset material each)
     and the baked Color PNGs are written to the --out directory.

Export-bake method (and why): Ucupaint 3.0.0's own bake operator
(wm.y_bake_all_targets) cannot run in background mode - its bookkeeping
(bake_common.remember_before_bake) reads bpy.context.space_data, which
is None headless, and raises AttributeError before baking anything
(reproduced verbatim in tests/output/TEST_LOG.md; GUI mode under xvfb
segfaults in GHOST/viewport code on this VM, also documented there).
The export proof therefore bakes each preset's Ucupaint node-group
'Color' output through Blender's Cycles EMIT bake - the stack being
sampled is 100% the Ucupaint layer stack; only the final sampling step
uses Cycles' baker instead of Ucupaint's bake-target wrapper. In an
interactive session, wm.y_bake_all_targets remains the one-click route.
"""

import json
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "presets"))

RESULTS = []


def test_line(name, ok, detail=""):
    RESULTS.append({"test": name, "ok": bool(ok), "detail": str(detail)})
    print(f"TEST {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)


def build_demo_prop(name, location_x):
    """A prop with features smart masks can bite on: beveled edges, four
    bolt heads on top (contact AO + more edges) and a recessed pocket on
    the front face (a real cavity for the AO dirt to live in)."""
    bpy.ops.mesh.primitive_cube_add(size=2, location=(location_x, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.width = 0.08
    bev.segments = 3
    bpy.ops.object.modifier_apply(modifier=bev.name)
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=1, use_grid_fill=True)
    bm.to_mesh(obj.data)
    bm.free()
    # Bolt heads on the top face, joined into the prop.
    for bx, by in ((-0.55, -0.55), (0.55, -0.55), (-0.55, 0.55), (0.55, 0.55)):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.13, depth=0.16, vertices=12,
            location=(location_x + bx, by, 1.04))
        bolt = bpy.context.active_object
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bolt.select_set(True)
        bpy.ops.object.join()
        bolt = None
    # Recessed pocket on the front (+Y) face via boolean difference.
    bpy.ops.mesh.primitive_cube_add(size=2, location=(location_x, 0.92, 0))
    cutter = bpy.context.active_object
    cutter.scale = (0.33, 0.18, 0.33)
    bpy.context.view_layer.objects.active = cutter
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bool_mod = obj.modifiers.new("Pocket", "BOOLEAN")
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    # UV unwrap the finished prop.
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.003)
    bpy.ops.object.mode_set(mode='OBJECT')
    return obj


def image_stats(image, stride=8):
    """Full-frame stats plus surface-only stats (non-black pixels, i.e.
    inside the UV islands - the honest measure of mask variation, since
    the empty margin is uniformly black)."""
    px = image.pixels[:]
    out = {}
    for ch, nm in ((0, "r"), (1, "g"), (2, "b")):
        vals = [px[i] for i in range(ch, len(px) - 3, 4 * stride)]
        surf = []
        for i in range(0, len(px) - 3, 4 * stride):
            if px[i] > 0.0 or px[i + 1] > 0.0 or px[i + 2] > 0.0:
                surf.append(px[i + ch])
        def ms(v):
            if not v:
                return {"mean": 0.0, "std": 0.0}
            m = sum(v) / len(v)
            var = sum((x - m) ** 2 for x in v) / len(v)
            return {"mean": m, "std": var ** 0.5}
        full = ms(vals)
        out[nm] = {**full, "surface_mean": ms(surf)["mean"],
                   "surface_std": ms(surf)["std"]}
    out["size"] = list(image.size)
    return out


def export_bake_color(obj, mat, sm, out_dir, preset_id):
    """Bake the Ucupaint group's Color output via Cycles EMIT (see header).

    Temporarily swaps the object's only material slot for a throwaway
    export material (group -> Emission -> Output), bakes, restores.
    Returns (stats_dict, png_path)."""
    tree, yp = sm.get_material_yp(mat)
    if tree is None:
        raise RuntimeError("no Ucupaint group on material")
    xmat = bpy.data.materials.new(f"Export_{preset_id}")
    xmat.use_nodes = True
    nt = xmat.node_tree
    nt.nodes.clear()
    grp = nt.nodes.new('ShaderNodeGroup')
    grp.node_tree = tree
    emi = nt.nodes.new('ShaderNodeEmission')
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(grp.outputs['Color'], emi.inputs['Color'])
    nt.links.new(emi.outputs['Emission'], out.inputs['Surface'])
    im = bpy.data.images.new(f"Export_{preset_id}_Color", 512, 512)
    node = nt.nodes.new('ShaderNodeTexImage')
    node.image = im
    node.select = True
    nt.nodes.active = node

    obj.data.materials[0] = xmat
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        r = bpy.ops.object.bake(type='EMIT', use_clear=True, margin=4)
        if 'FINISHED' not in r:
            raise RuntimeError(f"EMIT bake returned {r}")
        stats = image_stats(im)
        png = os.path.join(out_dir, f"baked_{preset_id}_Color.png")
        im.filepath_raw = png
        im.file_format = 'PNG'
        im.save()
    finally:
        obj.data.materials[0] = mat
    return stats, png


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out_dir = "."
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    import apply_smartmask_preset as sm

    bpy.ops.wm.read_factory_settings(use_empty=True)

    # --- S-1: add-on enables and is the pinned version -------------------
    try:
        sm.enable_ucupaint()
        test_line("ucupaint_enabled", True, f"module={sm.ADDON_MODULE}")
    except Exception as e:
        test_line("ucupaint_enabled", False, repr(e))
        return finish(out_dir)
    # Version from the installed extension's own manifest (extensions do
    # not expose bl_info on the package module).
    try:
        import glob
        import tomllib
        manifests = glob.glob(os.path.expanduser(
            "~/.config/blender/*/extensions/user_default/ucupaint/blender_manifest.toml"))
        ver = None
        if manifests:
            with open(manifests[0], "rb") as f:
                ver = tomllib.load(f).get("version")
        test_line("ucupaint_version_3_0_0", ver == "3.0.0",
                  f"manifest version={ver} path={manifests[:1]}")
    except Exception as e:
        test_line("ucupaint_version_3_0_0", False, repr(e))

    with open(sm.DEFAULT_JSON) as f:
        index = json.load(f)
    preset_ids = [p["id"] for p in index["presets"]]
    test_line("preset_index_has_4", len(preset_ids) == 4, f"ids={preset_ids}")

    # --- S-2: one demo prop per preset; apply + verify stack -------------
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 1
    bpy.context.scene.cycles.device = 'CPU'
    reports = {}
    bake_stats = {}
    for i, pid in enumerate(preset_ids):
        obj = build_demo_prop(f"SmartMaskProp_{pid}", location_x=i * 3.0)
        if i == 0:
            test_line("demo_prop_built", len(obj.data.vertices) > 100,
                      f"verts={len(obj.data.vertices)} "
                      f"uv={[u.name for u in obj.data.uv_layers]}")
        want = [p for p in index["presets"] if p["id"] == pid][0]
        try:
            rep = sm.apply_preset(obj, pid, index=index)
            reports[pid] = rep
            stack = {s["layer"]: s for s in rep["final_stack"]}
            eff = stack.get(want["effect_layer"]["name"])
            got_masks = [(m["name"], m["type"]) for m in eff["masks"]] if eff else []
            want_masks = [(m["name"], m["type"]) for m in want["masks"]]
            test_line(f"preset_{pid}_stack", got_masks == want_masks,
                      f"masks={got_masks}")
            test_line(f"preset_{pid}_base_layer",
                      index["base_layer"]["name"] in stack,
                      f"layers={list(stack)}")
            test_line(f"preset_{pid}_modifiers",
                      len(rep["modifiers"]) == sum(len(m.get('modifiers', [])) for m in want["masks"]),
                      f"modifiers={rep['modifiers']}")
        except Exception as e:
            import traceback; traceback.print_exc()
            test_line(f"preset_{pid}_stack", False, repr(e))
            continue

        # --- Export bake: masks must create pixel variation --------------
        mat = bpy.data.materials.get(f"SmartMask_{pid}")
        try:
            stats, png = export_bake_color(obj, mat, sm, out_dir, pid)
            bake_stats[pid] = {**stats, "file": os.path.basename(png)}
            test_line(f"bake_{pid}", True, f"png={os.path.basename(png)} size={stats['size']}")
            test_line(f"mask_variation_{pid}", stats["r"]["surface_std"] > 0.003,
                      f"baked Color R surface std={stats['r']['surface_std']:.4f} "
                      f"(floor 0.003), surface mean={stats['r']['surface_mean']:.4f}, "
                      f"full-frame std={stats['r']['std']:.4f}")
        except Exception as e:
            import traceback; traceback.print_exc()
            test_line(f"bake_{pid}", False, repr(e))

    # --- Library blend ----------------------------------------------------
    lib_path = os.path.join(out_dir, "smartmask_preset_library.blend")
    bpy.ops.wm.save_as_mainfile(filepath=lib_path)
    test_line("library_blend_saved", os.path.getsize(lib_path) > 10000,
              f"{lib_path} {os.path.getsize(lib_path)} bytes")

    report = {"results": RESULTS, "apply_reports": reports,
              "bake_stats": bake_stats}
    with open(os.path.join(out_dir, "test_report.json"), "w") as f:
        json.dump(report, f, indent=1, default=str)
    finish(out_dir)


def finish(out_dir):
    passed = sum(1 for r in RESULTS if r["ok"])
    print(f"TEST_ALL: {passed}/{len(RESULTS)} passed", flush=True)
    print("TEST_RESULT " + ("PASS" if passed == len(RESULTS) and RESULTS else "FAIL"),
          flush=True)


if __name__ == "__main__":
    main()
