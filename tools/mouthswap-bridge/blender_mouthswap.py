#!/usr/bin/env python3
"""blender_mouthswap.py -- build a timed mouth-swap rig in Blender (SPEC T-2).

This is the Blender half of the MouthSwap bridge. It is used two ways:

  1. As the template the bridge (mouthswap_bridge.py) copies into an
     output folder with a plan embedded -- then you just open/run that
     generated mouthswap_blender.py inside Blender.
  2. Directly, with a plan JSON produced by the bridge:
       blender -b --python blender_mouthswap.py -- --plan mouthswap_plan.json

What it builds:
  * Scene fps and frame range set from the plan.
  * One image plane per mouth shape in a "MouthSwap" collection, each
    plane textured with that shape's mouth image (alpha respected).
  * Visibility (hide_viewport + hide_render) keyed with CONSTANT
    interpolation so exactly one mouth is exposed on every frame,
    frame-accurate at the plan's fps.

Re-running it in the same .blend replaces the previous MouthSwap rig.
Original implementation for TRIPPEDD Production Studios.
"""

import json
import os
import sys

import bpy

# The bridge replaces the next line with the embedded plan JSON when it
# generates a self-contained mouthswap_blender.py. Leave it as None here.
EMBEDDED_PLAN = None

PLANE_SIZE = 0.5  # metres; scale the MouthSwap collection to fit the rig


def load_plan():
    if EMBEDDED_PLAN is not None:
        return EMBEDDED_PLAN
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    plan_path = None
    if "--plan" in argv:
        plan_path = argv[argv.index("--plan") + 1]
    elif argv:
        plan_path = argv[0]
    if plan_path is None:
        beside = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "mouthswap_plan.json")
        plan_path = beside if os.path.isfile(beside) else "mouthswap_plan.json"
    with open(plan_path) as fh:
        return json.load(fh)


def all_fcurves(action):
    """F-curves of an action, across the legacy and layered action APIs."""
    fcurves = []
    try:
        fcurves.extend(list(action.fcurves))
    except Exception:
        pass
    if not fcurves:
        try:
            for layer in action.layers:
                for strip in layer.strips:
                    bag = getattr(strip, "channelbag", None)
                    if bag is not None:
                        fcurves.extend(list(bag.fcurves))
        except Exception:
            pass
    return fcurves


def set_constant_interpolation(obj):
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    for fc in all_fcurves(ad.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


def make_mouth_plane(code, image_path, collection):
    bpy.ops.mesh.primitive_plane_add(size=PLANE_SIZE, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = f"Mouth_{code}"
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection.objects.link(obj)

    mat = bpy.data.materials.new(name=f"MouthMat_{code}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    principled = nodes.get("Principled BSDF")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(image_path)
    links.new(tex.outputs["Color"], principled.inputs["Base Color"])
    links.new(tex.outputs["Alpha"], principled.inputs["Alpha"])
    for attr, value in (("blend_method", "BLEND"),
                        ("surface_render_method", "BLENDED")):
        try:
            setattr(mat, attr, value)
        except Exception:
            pass
    obj.data.materials.append(mat)
    return obj


def build(plan):
    scene = bpy.context.scene
    scene.render.fps = int(plan["fps"])
    scene.render.fps_base = 1.0
    scene.frame_start = int(plan.get("frame_start", 1))
    scene.frame_end = int(plan["frame_end"])
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        pass

    # Idempotent: remove a previous MouthSwap rig from this file.
    old = bpy.data.collections.get("MouthSwap")
    if old:
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    collection = bpy.data.collections.new("MouthSwap")
    scene.collection.children.link(collection)

    planes = {}
    for code, path in sorted(plan["mouth_files"].items()):
        planes[code] = make_mouth_plane(code, path, collection)

    cues = plan["cues"]
    if not cues:
        raise RuntimeError("plan has no cues")

    def key_visibility(obj, frame, hidden):
        obj.hide_render = hidden
        obj.hide_viewport = hidden
        obj.keyframe_insert(data_path="hide_render", frame=frame)
        obj.keyframe_insert(data_path="hide_viewport", frame=frame)

    first_code = cues[0]["phoneme"]
    for code, obj in planes.items():
        key_visibility(obj, scene.frame_start, code != first_code)
    current = first_code
    for cue in cues[1:]:
        code = cue["phoneme"]
        if code == current:
            continue
        frame = int(cue["frame"])
        key_visibility(planes[current], frame, True)
        key_visibility(planes[code], frame, False)
        current = code
    for obj in planes.values():
        set_constant_interpolation(obj)

    print(f"MOUTHSWAP_OK planes={len(planes)} cues={len(cues)} "
          f"frames={scene.frame_start}..{scene.frame_end} "
          f"fps={scene.render.fps}")


if __name__ == "__main__":
    build(load_plan())
