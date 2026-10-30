"""TRIPPEDD SmartMask preset applier (SPEC S-2).

Applies one named preset from ``smartmask_presets.json`` to the active
object's active material inside Blender, building a real Ucupaint 3.0
layer stack: a solid base coat plus one masked effect layer whose masks
are computed from the mesh itself (AO / edge detect / world-space fake
lighting / procedural noise). Original studio construction - no settings
copied from any paid texturing tool.

Run inside Blender 4.5.3 (Ucupaint must be installed, see
``../install_ucupaint.sh``):

    blender -b file.blend --python apply_smartmask_preset.py -- \
        --preset edge_wear [--object ObjectName] [--json /path/to/index.json]

Presets: edge_wear, cavity_dirt, top_dust, paint_chips.
"""

import json
import os
import sys

import bpy

ADDON_MODULE = "bl_ext.user_default.ucupaint"
DEFAULT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "smartmask_presets.json")


def log(*a):
    print("[SmartMask]", *a, flush=True)


def enable_ucupaint():
    import addon_utils
    enabled, loaded = addon_utils.check(ADDON_MODULE)
    if not enabled:
        addon_utils.enable(ADDON_MODULE, default_set=True, persistent=True)
        enabled, loaded = addon_utils.check(ADDON_MODULE)
    if not (enabled and loaded):
        raise RuntimeError("Ucupaint add-on is not enabled/loaded")
    return True


def get_material_yp(mat):
    """Return (tree, yp) of the Ucupaint node group wired into mat, or (None, None)."""
    if not mat or not mat.use_nodes or not mat.node_tree:
        return None, None
    for node in mat.node_tree.nodes:
        if node.bl_idname == 'ShaderNodeGroup' and node.node_tree is not None:
            yp = getattr(node.node_tree, "yp", None)
            if yp is not None and yp.is_ypaint_node and len(yp.channels) > 0:
                return node.node_tree, yp
    return None, None


def ensure_yp_material(obj, material_name):
    """Create (or reuse) a material with a Ucupaint Principled stack on obj."""
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        mat = bpy.data.materials.new(material_name)
        mat.use_nodes = True
    if mat.name not in [m.name if m else None for m in obj.data.materials]:
        obj.data.materials.append(mat)
    obj.active_material_index = list(obj.data.materials).index(mat)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    tree, yp = get_material_yp(mat)
    if yp is None:
        r = bpy.ops.wm.y_quick_ypaint_node_setup(
            'EXEC_DEFAULT', type='BSDF_PRINCIPLED',
            enable_color=True, enable_metallic=True, enable_roughness=True,
            enable_height=True, enable_normal=True, enable_ao=True,
            use_orm_bake_target=True)
        if 'FINISHED' not in r:
            raise RuntimeError(f"y_quick_ypaint_node_setup failed: {r}")
        tree, yp = get_material_yp(mat)
    if yp is None:
        raise RuntimeError("Ucupaint node group not found after setup")
    return mat, tree, yp


def channel_index(yp, name):
    for i, ch in enumerate(yp.channels):
        if ch.name == name:
            return i
    return None


def set_channel_value(layer, yp, channel_name, value):
    """Set a VALUE-channel override on a layer; returns what was actually set."""
    idx = channel_index(yp, channel_name)
    if idx is None or idx >= len(layer.channels):
        return None
    ch = layer.channels[idx]
    ch.enable = True
    ch.override = True
    ch.override_value = float(value)
    return {"channel": channel_name, "override": bool(ch.override),
            "override_value": float(ch.override_value)}


def set_noise_params(layer, mask, noise):
    """Find the mask's Noise Texture node in the layer tree and set its inputs."""
    if not noise:
        return None
    tree_name = ".yP Layer " + layer.name
    candidates = []
    for g in bpy.data.node_groups:
        if g.name == tree_name or g.name.startswith(tree_name):
            candidates.append(g)
    for g in list(bpy.data.node_groups):
        if g not in candidates:
            candidates.append(g)
    for g in candidates:
        node = g.nodes.get(mask.source) if mask.source else None
        if node is not None and node.bl_idname == 'ShaderNodeTexNoise':
            for key, val in noise.items():
                if key in node.inputs:
                    node.inputs[key].default_value = float(val)
            return {"node": node.name, "tree": g.name,
                    "scale": node.inputs['Scale'].default_value}
    return None


def add_mask_modifier(mask, layer, modifier_type):
    """Add a mask modifier (INVERT/RAMP/...).

    Headless quirk (verified against Ucupaint 3.0.0 source): the
    y_new_mask_modifier operator DOES add the modifier and rebuild the
    layer wiring, then raises IndexError on a UI-list bookkeeping line
    (MaskModifier.execute -> ypui.layer_ui.masks[...], empty in a
    headless session). So: call the operator, ignore its exception, and
    check whether the modifier landed. Only if it did not, fall back to
    Ucupaint's own internal add_new_mask_modifier() - the same function
    the operator calls. (Calling both unconditionally would double-add:
    e.g. INVERT twice = no inversion.)
    """
    before = len(mask.modifiers)
    try:
        with bpy.context.temp_override(mask=mask, layer=layer):
            bpy.ops.wm.y_new_mask_modifier('EXEC_DEFAULT', type=modifier_type)
    except Exception as e:
        log("mask modifier operator raised (checking whether it landed):",
            type(e).__name__)
    if len(mask.modifiers) > before and mask.modifiers[-1].type == modifier_type:
        return "operator"
    import importlib
    mm = importlib.import_module(ADDON_MODULE + ".MaskModifier")
    mm.add_new_mask_modifier(mask, modifier_type)
    # Mirror what the operator does after adding: rebuild the layer wiring.
    try:
        na = importlib.import_module(ADDON_MODULE + ".node_arrangements")
        nc = importlib.import_module(ADDON_MODULE + ".node_connections")
        na.rearrange_layer_nodes(layer)
        nc.reconnect_layer_nodes(layer)
    except Exception as e:
        log("post-modifier rearrange/reconnect skipped:", repr(e))
    return "internal-api"


def tighten_ramp_modifier(mask, stop_lo=0.45, stop_hi=0.58):
    """Make the newest RAMP modifier on mask act as a soft threshold."""
    for m in reversed(mask.modifiers):
        if m.type == 'RAMP' and getattr(m, 'ramp', ''):
            import importlib
            mc = importlib.import_module(ADDON_MODULE + ".common")
            tree = mc.get_mask_tree(mask)
            node = tree.nodes.get(m.ramp) if tree else None
            if node is not None and hasattr(node, 'color_ramp'):
                elems = node.color_ramp.elements
                if len(elems) >= 2:
                    elems[0].position = stop_lo
                    elems[1].position = stop_hi
                    return {"ramp_node": node.name, "stops": [stop_lo, stop_hi]}
    return None


def apply_preset(obj, preset_id, index=None, fresh=True):
    """Build the preset's layer stack on obj's (new) Ucupaint material.

    Returns a report dict describing exactly what was created.
    """
    enable_ucupaint()
    if index is None:
        with open(DEFAULT_JSON) as f:
            index = json.load(f)
    preset = None
    for p in index["presets"]:
        if p["id"] == preset_id:
            preset = p
            break
    if preset is None:
        raise ValueError(f"unknown preset id: {preset_id}")

    mat_name = f"SmartMask_{preset_id}"
    mat, tree, yp = ensure_yp_material(obj, mat_name)
    report = {"preset": preset_id, "material": mat.name, "tree": tree.name,
              "channel_overrides": [], "masks": [], "modifiers": []}

    if fresh:
        # Remove any layers from a previous application of this material.
        while len(yp.layers) > 0:
            yp.active_layer_index = 0
            try:
                bpy.ops.wm.y_remove_layer('EXEC_DEFAULT')
            except Exception:
                break

    base = index["base_layer"]
    bpy.ops.wm.y_new_layer('EXEC_DEFAULT', name=base["name"], type=base["type"],
                           solid_color=tuple(base["color"]))
    base_layer = yp.layers[0]
    for ch_name, val in base.get("channel_values", {}).items():
        got = set_channel_value(base_layer, yp, ch_name, val)
        if got:
            report["channel_overrides"].append({"layer": base["name"], **got})

    eff = preset["effect_layer"]
    bpy.ops.wm.y_new_layer('EXEC_DEFAULT', name=eff["name"], type=eff["type"],
                           solid_color=tuple(eff["color"]))
    layer = yp.layers[0]  # newest layer becomes active / top of stack
    report["effect_layer"] = layer.name
    for ch_name, val in eff.get("channel_values", {}).items():
        got = set_channel_value(layer, yp, ch_name, val)
        if got:
            report["channel_overrides"].append({"layer": eff["name"], **got})

    for m in preset["masks"]:
        bpy.ops.wm.y_new_layer_mask('EXEC_DEFAULT', name=m["name"], type=m["type"])
        mask = layer.masks[-1]
        applied = {}
        for key, val in m.get("params", {}).items():
            if hasattr(mask, key):
                setattr(mask, key, val)
                applied[key] = getattr(mask, key)
                if isinstance(applied[key], (tuple,)):
                    applied[key] = list(applied[key])
        report["masks"].append({"name": mask.name, "type": mask.type,
                                "params": applied})
        nz = set_noise_params(layer, mask, m.get("noise"))
        if nz:
            report["masks"][-1]["noise_node"] = nz
        for mod_type in m.get("modifiers", []):
            how = add_mask_modifier(mask, layer, mod_type)
            entry = {"mask": mask.name, "modifier": mod_type, "via": how}
            if mod_type == 'RAMP':
                entry["ramp"] = tighten_ramp_modifier(mask)
            report["modifiers"].append(entry)

    report["final_stack"] = [
        {"layer": l.name, "type": l.type,
         "masks": [{"name": mk.name, "type": mk.type,
                    "modifiers": [md.type for md in mk.modifiers]}
                   for mk in l.masks]}
        for l in yp.layers]
    return report


def main(argv):
    preset_id = None
    object_name = None
    json_path = None
    i = 0
    while i < len(argv):
        if argv[i] == '--preset':
            preset_id = argv[i + 1]; i += 2
        elif argv[i] == '--object':
            object_name = argv[i + 1]; i += 2
        elif argv[i] == '--json':
            json_path = argv[i + 1]; i += 2
        else:
            i += 1
    if not preset_id:
        raise SystemExit("usage: --preset <id> [--object <name>] [--json <path>]")
    index = None
    if json_path:
        with open(json_path) as f:
            index = json.load(f)
    obj = bpy.data.objects.get(object_name) if object_name else bpy.context.active_object
    if obj is None:
        raise SystemExit("no target object")
    report = apply_preset(obj, preset_id, index=index)
    log("APPLIED", json.dumps(report, indent=1, default=str))


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
