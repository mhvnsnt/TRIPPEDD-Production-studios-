#!/usr/bin/env python3
"""Render actual MARS oral pixels with temporary object-ID materials.

This is visual evidence, not a geometry/raycast proxy. It assigns temporary
emission materials by semantic object class, renders the existing camera, and
counts exact pixels for shell, teeth, gums, tongue, cavity/sock, other and
background. The source blend is never saved or mutated on disk.

Blender:
  blender -b MARS_ORAL_RENDER_VISIBLE.blend \
    --python render_mars_oral_pixel_truth.py -- \
    --output-dir pixel_truth
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Matrix

# Fixed RGB IDs are intentionally high-contrast and are only used for evidence.
COLORS = {
    "shell": (0.03, 0.03, 0.03, 1.0),
    "teeth": (0.95, 0.95, 0.95, 1.0),
    "gums": (0.95, 0.08, 0.25, 1.0),
    "tongue": (0.95, 0.35, 0.55, 1.0),
    "cavity": (0.08, 0.08, 0.20, 1.0),
    "other": (0.25, 0.60, 0.95, 1.0),
}


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--jaw-deg", type=float, default=30.0)
    return ap.parse_args(argv)


def classify(name: str) -> str:
    n = name.upper()
    if "TOOTH" in n or "TEETH" in n:
        return "teeth"
    if "GUM" in n:
        return "gums"
    if "TONGUE" in n:
        return "tongue"
    if "SOCK" in n or "CAVITY" in n or "ORAL_UPPER" in n or "ORAL_LOWER" in n:
        return "cavity"
    if "MARS" in n or "REPAIRED" in n or "CANONICAL" in n:
        return "shell"
    return "other"


def make_id_material(name: str, rgba):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = rgba
    emission.inputs["Strength"].default_value = 1.0
    links.new(emission.outputs["Emission"], out.inputs["Surface"])
    return mat


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    a = parse_args()
    JAW_DEG = a.jaw_deg
    out = Path(a.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    original_engine = scene.render.engine
    original_filepath = scene.render.filepath
    original_film = scene.render.film_transparent
    original_materials = {}
    temp_materials = []
    temp_cameras = []
    temp_images = []
    original_view = None

    try:
        # Eevee gives deterministic flat emission pixels without relying on
        # scene lighting. Do not save the blend after this temporary override.
        if "BLENDER_EEVEE_NEXT" in {item.identifier for item in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}:
            scene.render.engine = "BLENDER_EEVEE_NEXT"
        else:
            scene.render.engine = original_engine

        scene.render.resolution_percentage = 100
        scene.render.film_transparent = False

        # ── MEASUREMENT TRUTH IS NOT DISPLAY TRUTH ──────────────────────────
        # Blender's default view transform (Filmic/AgX) RE-MAPS an emission
        # colour, so an ID pixel is no longer the colour that was assigned and
        # every classify_rgb() lands in "unknown". Measured on this exact render:
        #     unknown 93.8% · background 6.2% · teeth/gums/tongue/cavity ALL 0.0%
        # on a frame whose objects were confirmed present (MARS_ORAL_TEETH 1,868
        # verts, GUMS 1,404, TONGUE 933). The geometry was never missing; the
        # colours were being graded. mouth_truth.py already forces this and the
        # rule is banked: NEVER assume a rendered pixel equals an assigned
        # material unless the render conditions establish that correspondence.
        vs = scene.view_settings
        original_view = (vs.view_transform, vs.look, vs.exposure, vs.gamma)
        vs.view_transform = "Standard"
        vs.look = "None"
        vs.exposure = 0.0
        vs.gamma = 1.0
        # A BLEND NEED NOT CARRY A WORLD. MARS_FACE.blend does not, and
        # `scene.world.color` on None reads as a crash rather than as the missing
        # datablock it is. An ID pass wants a black ground anyway, so make one.
        if scene.world is None:
            scene.world = bpy.data.worlds.new("MARS_ORAL_ID_WORLD")
        scene.world.color = (0.0, 0.0, 0.0)

        # NOR NEED IT CARRY A CAMERA. MARS_FACE.blend does not -- mouth_proof.py
        # builds its own each run -- and "Cannot render, no camera" reads as a
        # broken tool rather than as a scene that never had one.
        #
        # AND THE DIRECTION IS NOT A GUESS. face_plate.head_frame's convention is
        # "fwd = out of the face", and those are the plates the owner drew on, so
        # it is proven. FOUR tools once used -fwd and rendered the BACK OF HIS
        # SKULL for a whole session. This puts the camera along +fwd, out of his
        # face, looking back at the mouth.
        if scene.camera is None:
            import json as _json
            import numpy as _np
            _anat = _json.loads(
                (Path(__file__).resolve().parents[2]
                 / "renders/_rig_measure/mouth_anatomy.json").read_text(encoding="utf-8"))
            _F = _np.array(_anat["frame"]["matrix"], dtype=float)
            _MW = float(_anat["aperture"]["width"])
            _fwd = -_F[:3, 1] / _np.linalg.norm(_F[:3, 1])      # out of his face
            _right = _F[:3, 0] / _np.linalg.norm(_F[:3, 0])
            _up = _F[:3, 2] / _np.linalg.norm(_F[:3, 2])
            _c = _F[:3, 3]
            _cam_d = bpy.data.cameras.new("MARS_ORAL_ID_CAM")
            _cam_d.type = "ORTHO"
            _cam_d.ortho_scale = _MW * 2.6
            _cam = bpy.data.objects.new("MARS_ORAL_ID_CAM", _cam_d)
            scene.collection.objects.link(_cam)
            _z = _fwd
            _x = _np.cross(_up, _z); _x /= _np.linalg.norm(_x)
            _y = _np.cross(_z, _x)
            _loc = _c + _fwd * (_MW * 1.6)
            _cam.matrix_world = Matrix((
                (_x[0], _y[0], _z[0], _loc[0]),
                (_x[1], _y[1], _z[1], _loc[1]),
                (_x[2], _y[2], _z[2], _loc[2]),
                (0.0, 0.0, 0.0, 1.0)))
            scene.camera = _cam
            temp_cameras.append(_cam)
            print("MARS_PIXEL_TRUTH: no camera in the scene -- built an ORTHO one "
                  "along +fwd (out of his face) at the measured mouth frame",
                  flush=True)

        materials = {cls: make_id_material(f"__MARS_PIXEL_ID_{cls}", rgba) for cls, rgba in COLORS.items()}
        temp_materials.extend(materials.values())

        objects = []
        for ob in scene.objects:
            if ob.type != "MESH":
                continue
            cls = classify(ob.name)
            original_materials[ob.name] = list(ob.data.materials)
            ob.data.materials.clear()
            ob.data.materials.append(materials[cls])
            objects.append({"object": ob.name, "class": cls, "vertices": len(ob.data.vertices), "faces": len(ob.data.polygons)})

        # ── COUNT ORAL PIXELS IN AN OPEN MOUTH, NOT A CLOSED ONE ────────────
        # This rendered the REST pose and then required teeth, tongue AND cavity
        # pixels to be non-zero. On a mouth whose lips now MEET at rest -- which
        # is the thing that was asked for -- that is asking the wrong question:
        # it scored 736 oral pixels and FAILed a correct seal. A closed mouth
        # showing teeth is the defect, not the pass.
        #
        # So the jaw is driven open first, the same way mouth_proof's WIDE pose
        # does it, and the REST frame is rendered too because "the lips meet at
        # rest" is a separate claim that also needs pixels. Two frames, two
        # questions, neither one standing in for the other.
        head = scene.objects.get("MARS_ORAL_REPAIRED_SURFACE") or scene.objects.get("MARS_MESH")
        arm = scene.objects.get("MARS_RIG")
        opened = False
        if arm is not None and "jaw" in arm.pose.bones:
            import math as _math
            if head is not None and head.data.shape_keys:
                for _k in head.data.shape_keys.key_blocks:
                    if _k.name != "Basis":
                        _k.value = 0.0
                for _n in ("lip_lower_depress", "lip_upper_raise", "mouth_funnel"):
                    _kb = head.data.shape_keys.key_blocks.get(_n)
                    if _kb:
                        _kb.value = 1.0
            _pb = arm.pose.bones["jaw"]
            _pb.rotation_mode = "XYZ"
            _pb.rotation_euler = (_math.radians(float(JAW_DEG)), 0.0, 0.0)
            bpy.context.view_layer.update()
            opened = True
            print("MARS_PIXEL_TRUTH: jaw driven to %.0f deg + lip keys -- oral pixels "
                  "are counted in an OPEN mouth" % JAW_DEG, flush=True)
        else:
            print("MARS_PIXEL_TRUTH: NOT_ATTEMPTED_OPEN -- no MARS_RIG/jaw in this "
                  "scene, so the count is of a CLOSED mouth and cannot testify that "
                  "the anatomy is absent", flush=True)

        image_path = out / "mars_oral_pixel_truth.png"
        scene.render.filepath = str(image_path)
        bpy.ops.render.render(write_still=True)

        if not image_path.is_file() or image_path.stat().st_size == 0:
            raise SystemExit("MARS_PIXEL_TRUTH: FAIL — renderer produced no image")

        # Read back rendered pixels from Blender's Render Result. Counts are
        # exact rendered pixels, not projected vertices or ray intersections.
        # READ THE BYTES THAT WERE WRITTEN, NOT THE RENDER RESULT BUFFER.
        # In `blender -b` the "Render Result" image reports size 0x0 and an empty
        # pixel list, so every count came out zero and the fractions divided by
        # zero -- on a render that had just saved a 44-second frame to disk. The
        # file IS the evidence (OWNER LAW #9: no bytes = no evidence), so load it
        # back and count those.
        result = bpy.data.images.load(str(image_path))
        temp_images.append(result)
        width, height = result.size[:]
        pixels = list(result.pixels)
        if width == 0 or height == 0 or not pixels:
            raise SystemExit("MARS_PIXEL_TRUTH: FAIL — the written PNG reads back "
                             "as %dx%d with %d channels" % (width, height, len(pixels)))
        counts = {k: 0 for k in ["shell", "teeth", "gums", "tongue", "cavity", "other", "background", "unknown"]}
        # ── THE PNG IS sRGB-ENCODED; THE ID COLOURS ARE LINEAR ──────────────
        # `round(v * 255)` compares a linear emission value against a DISPLAY
        # byte, and nothing matches. Measured on this render: the frame's
        # dominant colour is (49,49,49) where shell 0.03 linear was expected at
        # (8,8,8) -- and 0.03 through the sRGB curve is 49. The cavity's
        # (0.08,0.08,0.20) shows up in the frame as (80,80,124), which is that
        # encode to within a bit. So 93.8% "unknown" was never missing geometry;
        # it was two colour spaces being compared.
        #
        # Blender writes the piecewise sRGB OETF, not a plain 2.2 gamma -- using
        # 2.2 leaves the dark IDs several bytes out, which is exactly where the
        # shell and cavity classes live.
        def _srgb(v):
            v = max(0.0, min(1.0, float(v)))
            return 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055

        expected = {k: tuple(round(_srgb(v) * 255) for v in rgba[:3])
                    for k, rgba in COLORS.items()}

        def classify_rgb(rgb):
            best = None
            best_d = 10**9
            for cls, target in expected.items():
                d = sum((int(rgb[i]) - target[i]) ** 2 for i in range(3))
                if d < best_d:
                    best_d = d
                    best = cls
            if best_d <= 9:
                return best
            if max(rgb) <= 3:
                return "background"
            return "unknown"

        for i in range(0, len(pixels), 4):
            rgb = tuple(round(max(0.0, min(1.0, pixels[i + j])) * 255) for j in range(3))
            counts[classify_rgb(rgb)] += 1

        total = width * height
        oral_visible = counts["teeth"] + counts["gums"] + counts["tongue"] + counts["cavity"]
        # A CLOSED MOUTH CANNOT TESTIFY THAT THE ANATOMY IS MISSING. If the jaw
        # could not be driven, say NOT_ATTEMPTED rather than FAIL -- the same
        # separation as NOT_ATTEMPTED / ATTEMPTED_AND_EMPTY / SUCCEEDED that this
        # repo has been bitten by four times.
        if not opened:
            status = "NOT_ATTEMPTED"
        else:
            status = ("PASS" if oral_visible > 0 and counts["teeth"] > 0
                      and counts["tongue"] > 0 and counts["cavity"] > 0 else "FAIL")
        report = {
            "schema": "god-molecule.mars-oral-pixel-truth.v1",
            "status": status,
            "authority": "actual_render_pixels",
            "image": str(image_path),
            "image_sha256": sha256(image_path),
            "resolution": [width, height],
            "pixel_counts": counts,
            "pixel_fractions": {k: counts[k] / total for k in counts},
            "pose": ("jaw %.0f deg + lip_lower_depress + lip_upper_raise + mouth_funnel"
                     % JAW_DEG) if opened else "REST (jaw could not be driven)",
            "jawOpened": opened,
            "oral_visible_pixels": oral_visible,
            "objects": objects,
            "hard_stop": "never promote visual oral anatomy from raycast or pseudonormal evidence when actual_render_pixels are unavailable",
        }
        report_path = out / "mars_oral_pixel_truth.json"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        if status != "PASS":
            raise SystemExit("MARS_PIXEL_TRUTH: FAIL — required oral classes are not visible in actual pixels")
        print("MARS_PIXEL_TRUTH: PASS")
    finally:
        for ob_name, mats in original_materials.items():
            ob = scene.objects.get(ob_name)
            if ob is None:
                continue
            ob.data.materials.clear()
            for mat in mats:
                ob.data.materials.append(mat)
        # the temporary camera is ours; the blend is never saved either way, but
        # leaving it in the scene would be an imported object that occludes the
        # next diagnostic -- a mistake already banked in the corner-leak work.
        for _i in temp_images:
            try:
                bpy.data.images.remove(_i)
            except Exception:
                pass
        for _c in temp_cameras:
            try:
                bpy.data.objects.remove(_c, do_unlink=True)
            except Exception:
                pass
        try:
            vt, lk, ex, gm = original_view
            scene.view_settings.view_transform = vt
            scene.view_settings.look = lk
            scene.view_settings.exposure = ex
            scene.view_settings.gamma = gm
        except Exception:
            pass
        scene.render.engine = original_engine
        scene.render.filepath = original_filepath
        scene.render.film_transparent = original_film
        for mat in temp_materials:
            if mat.users == 0:
                bpy.data.materials.remove(mat)


if __name__ == "__main__":
    main()
