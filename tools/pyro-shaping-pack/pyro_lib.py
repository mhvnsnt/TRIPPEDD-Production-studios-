"""Pyro Shaping Pack - shared Mantaflow/Cycles preset applier (SPEC H-4).

Original studio tunings only. Loads a preset JSON (see presets/*.json) and
builds the matching gas domain + flow emitter + Cycles Principled Volume
material in the current Blender scene.

Used by apply_pyro.py (artist entry point), build_presets.py (generates the
pyro_presets.blend library file) and tests/test_pyro.py (headless proof).
"""
import json
import os

import bpy

PACK_DIR = os.path.dirname(os.path.abspath(__file__))
PRESET_DIR = os.path.join(PACK_DIR, "presets")

DOMAIN_SIZE = (4.0, 4.0, 4.0)
DOMAIN_LOCATION = (0.0, 0.0, 2.0)


def list_looks():
    return sorted(f[:-5] for f in os.listdir(PRESET_DIR) if f.endswith(".json"))


def load_preset(name):
    path = os.path.join(PRESET_DIR, name + ".json")
    if not os.path.exists(path):
        raise ValueError("unknown pyro look %r (have: %s)" % (name, ", ".join(list_looks())))
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _set_props(obj_settings, values, skipped):
    for key, value in values.items():
        if hasattr(obj_settings, key):
            try:
                setattr(obj_settings, key, value)
            except (TypeError, ValueError) as exc:
                skipped.append("%s=%r (%s)" % (key, value, exc))
        else:
            skipped.append("%s (no such property)" % key)


def build_volume_material(preset):
    """Create/replace the Cycles volume material for this look.

    Node recipe (documented in README.md): Material Output <- Principled
    Volume, Density from the 'density' grid attribute, Temperature from the
    'temperature' grid attribute driving blackbody fire colour, smoke tint
    from the 'flame' colour attribute (fire looks) or a flat base colour
    (pure-smoke looks).
    """
    name = "PyroVol_" + preset["name"]
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)
    pv = nt.nodes.new("ShaderNodeVolumePrincipled")
    pv.location = (0, 0)
    sh = preset["volume_shading"]
    pv.inputs["Density"].default_value = sh["density_multiplier"]
    pv.inputs["Density Attribute"].default_value = sh["density_attribute"]
    pv.inputs["Color"].default_value = tuple(sh["base_color"]) + (1.0,)
    pv.inputs["Color Attribute"].default_value = sh["color_attribute"]
    pv.inputs["Anisotropy"].default_value = sh["anisotropy"]
    pv.inputs["Emission Strength"].default_value = sh["emission_strength"]
    pv.inputs["Emission Color"].default_value = tuple(sh["emission_color"]) + (1.0,)
    pv.inputs["Blackbody Intensity"].default_value = sh["blackbody_intensity"]
    pv.inputs["Blackbody Tint"].default_value = tuple(sh["blackbody_tint"]) + (1.0,)
    pv.inputs["Temperature Attribute"].default_value = sh["temperature_attribute"]
    nt.links.new(pv.outputs["Volume"], out.inputs["Volume"])
    return mat


def _make_emitter(preset):
    em = preset["emitter"]
    x, y, z = em["location"]
    shape = em["shape"]
    if shape == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=em["radius"], location=(x, y, z))
    elif shape == "box":
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))
        bpy.context.object.scale = (em["radius"] * 2.0, em["radius"] * 2.0, em["height"])
        bpy.ops.object.transform_apply(scale=True)
    else:  # cylinder
        bpy.ops.mesh.primitive_cylinder_add(
            radius=em["radius"], depth=max(em["height"], 0.05), location=(x, y, z))
    obj = bpy.context.object
    obj.name = "PyroFlow_" + preset["name"]
    return obj


def apply_look(name, resolution=None, frames=(1, 48), cache_dir=None):
    """Build domain + emitter + volume material for `name` in the current scene.

    Removes any previous PyroDomain/PyroFlow objects first (idempotent).
    Returns (report_dict, domain_obj, flow_obj).
    """
    preset = load_preset(name)
    skipped = []

    for obj in list(bpy.data.objects):
        if obj.name.startswith("PyroDomain") or obj.name.startswith("PyroFlow"):
            bpy.data.objects.remove(obj, do_unlink=True)

    # --- domain ---
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=DOMAIN_LOCATION)
    domain = bpy.context.object
    domain.name = "PyroDomain"
    domain.scale = DOMAIN_SIZE
    bpy.ops.object.transform_apply(scale=True)
    mod = domain.modifiers.new("Fluid", "FLUID")
    mod.fluid_type = "DOMAIN"
    ds = mod.domain_settings
    ds.domain_type = "GAS"
    dvals = dict(preset["domain"])
    if resolution is not None:
        dvals["resolution_max"] = resolution
    _set_props(ds, dvals, skipped)
    ds.cache_frame_start, ds.cache_frame_end = frames
    if cache_dir:
        ds.cache_directory = cache_dir
        ds.cache_type = "ALL"
    mat = build_volume_material(preset)
    domain.data.materials.append(mat)

    # --- flow emitter ---
    flow_obj = _make_emitter(preset)
    fmod = flow_obj.modifiers.new("Fluid", "FLUID")
    fmod.fluid_type = "FLOW"
    fs = fmod.flow_settings
    fvals = dict(preset["flow"])
    fvals["smoke_color"] = tuple(fvals["smoke_color"])  # flow smoke_color is RGB (3 floats)
    _set_props(fs, fvals, skipped)
    flow_obj.hide_render = True  # emitter geometry is not a render prop

    # burst looks stop emitting after emit_frames: density keyframes 1 -> 0
    if preset.get("emit_frames"):
        start, stop = preset["emit_frames"]
        fs.density = fvals["density"]
        fs.keyframe_insert(data_path="density", frame=start)
        fs.density = 0.0
        fs.keyframe_insert(data_path="density", frame=stop + 1)
        fs.density = fvals["density"]

    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = frames
    report = {
        "look": name,
        "display_name": preset["display_name"],
        "resolution": ds.resolution_max,
        "frames": list(frames),
        "skipped_settings": skipped,
    }
    return report, domain, flow_obj
