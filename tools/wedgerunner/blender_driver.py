"""WedgeRunner in-Blender driver — runs INSIDE headless Blender.

DO NOT run this with system python; WedgeRunner launches it as:

    blender -b [scene.blend] --python-exit-code 1 \\
        --python blender_driver.py -- \\
        --variant-json <file> --out <render.png> [--scene-script <file>]

Injection mechanism (documented in README.md):
  1. The variant JSON is loaded; its ``params`` dict is exposed to the
     optional scene script as the global ``PARAMS`` (and ``VARIANT``).
  2. The scene script is exec'd. It builds/loads the scene and may read
     any param directly (the escape hatch for scene-specific knobs).
  3. Dotted params are then applied generically (see apply_params):
       render.engine / render.samples / render.resolution /
       render.resolution_x / render.resolution_y / render.film_transparent
       render.<anything else>      -> scene.render.<attr>
       cycles.<attr>                -> scene.cycles.<attr>
       eevee.<attr>                 -> scene.eevee.<attr>
       world.<attr>                 -> scene.world.<attr> (if a world exists)
       objects.<Name>.<attr>[.<sub>] -> bpy.data.objects[<Name>]
       scene.<path...>              -> attribute path under bpy.context.scene
       __fail__ = true              -> raise (deliberate-failure test hook)
     Any non-dotted key is NOT applied here; it is for the scene script.
  4. A single still is rendered to --out and a driver_result.json is
     written next to it. Any exception propagates (with
     --python-exit-code 1 Blender exits non-zero) so the host runner can
     record the variant as failed without guessing.
"""
import json
import os
import sys
import traceback

import bpy


def _parse_args(argv):
    args = {}
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    it = iter(range(len(argv)))
    for i in it:
        tok = argv[i]
        if tok.startswith("--") and i + 1 < len(argv):
            args[tok[2:]] = argv[i + 1]
            next(it, None)
    return args


def _set_path(root, path, value):
    obj = root
    parts = path.split(".")
    for part in parts[:-1]:
        obj = getattr(obj, part)
    setattr(obj, parts[-1], value)


def _coerce(value):
    return tuple(value) if isinstance(value, list) else value


def apply_params(scene, params):
    applied, skipped = [], []
    for key, value in params.items():
        if key == "__fail__" and value:
            raise RuntimeError("variant requested deliberate failure via __fail__")
        if "." not in key:
            skipped.append(key)  # scene-script-only param
            continue
        head, rest = key.split(".", 1)
        try:
            if head == "render":
                if rest == "engine":
                    scene.render.engine = value
                elif rest == "samples":
                    if hasattr(scene, "cycles"):
                        scene.cycles.samples = int(value)
                    if hasattr(scene, "eevee"):
                        scene.eevee.taa_render_samples = int(value)
                elif rest == "resolution":
                    scene.render.resolution_x = int(value[0])
                    scene.render.resolution_y = int(value[1])
                elif rest == "resolution_x":
                    scene.render.resolution_x = int(value)
                elif rest == "resolution_y":
                    scene.render.resolution_y = int(value)
                elif rest == "film_transparent":
                    scene.render.film_transparent = bool(value)
                else:
                    _set_path(scene.render, rest, _coerce(value))
            elif head == "cycles":
                _set_path(scene.cycles, rest, _coerce(value))
            elif head == "eevee":
                _set_path(scene.eevee, rest, _coerce(value))
            elif head == "world":
                if scene.world is None:
                    raise RuntimeError("param targets world but scene has no world")
                _set_path(scene.world, rest, _coerce(value))
            elif head == "objects":
                name, attr = rest.split(".", 1)
                obj = bpy.data.objects[name]  # KeyError -> variant fails honestly
                _set_path(obj, attr, _coerce(value))
            elif head == "scene":
                _set_path(scene, rest, _coerce(value))
            else:
                raise RuntimeError(f"unknown param root {head!r} in key {key!r}")
            applied.append(key)
        except Exception:
            print(f"WEDGERUNNER: failed applying param {key!r}={value!r}")
            raise
    return applied, skipped


def main():
    args = _parse_args(sys.argv)
    with open(args["variant-json"], encoding="utf-8") as fh:
        variant = json.load(fh)
    params = variant.get("params", {})
    out_path = os.path.abspath(args["out"])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    scene_script = args.get("scene-script")
    if scene_script:
        g = {"bpy": bpy, "PARAMS": params, "VARIANT": variant, "__name__": "__wedge_scene__"}
        with open(scene_script, encoding="utf-8") as fh:
            code = compile(fh.read(), scene_script, "exec")
        exec(code, g)

    scene = bpy.context.scene
    applied, skipped = apply_params(scene, params)

    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)

    if not (os.path.isfile(out_path) and os.path.getsize(out_path) > 0):
        raise RuntimeError(f"render finished but no output at {out_path}")
    result = {
        "variant": variant.get("name"),
        "status": "ok",
        "output": out_path,
        "output_bytes": os.path.getsize(out_path),
        "applied_params": applied,
        "scene_script_params": skipped,
        "engine": scene.render.engine,
        "resolution": [scene.render.resolution_x, scene.render.resolution_y],
    }
    with open(os.path.join(os.path.dirname(out_path), "driver_result.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(f"WEDGERUNNER_OK variant={variant.get('name')} out={out_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise
