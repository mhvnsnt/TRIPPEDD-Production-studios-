"""render_one.py — render exactly ONE frame inside Blender.

This script runs *inside* Blender (``blender -b scene.blend --python
render_one.py -- <json>``). It is invoked by checkpoint_render_driver.py,
never by hand in normal use.

It applies the render settings passed as a JSON blob after ``--`` and
renders a single frame to ``<output_dir>/<prefix><NNNN>.png``. Rendering
one frame per Blender process is the whole point of the checkpoint
pattern: if the machine / VM dies, at most one frame of work is lost.

Donor lineage: formalizes the Cape Jones render lanes' proven pattern —
``render_take.py`` (one take script, explicit Cycles settings) driven by
``render_driver_v2.sh`` (one frame per Blender invocation). See README.md.
"""

import json
import os
import sys

import bpy


def main() -> int:
    argv = sys.argv[sys.argv.index("--") + 1:]
    if not argv:
        print("[render_one] ERROR: no settings JSON after --", flush=True)
        return 2
    cfg = json.loads(argv[0])

    frame = int(cfg["frame"])
    outdir = cfg["output_dir"]
    prefix = cfg.get("prefix", "frame_")
    os.makedirs(outdir, exist_ok=True)

    sc = bpy.context.scene

    engine = cfg.get("engine", "CYCLES")
    sc.render.engine = engine
    if engine == "CYCLES":
        sc.cycles.device = cfg.get("device", "CPU")
        sc.cycles.samples = int(cfg.get("samples", 32))
        sc.cycles.use_adaptive_sampling = bool(cfg.get("adaptive_sampling", True))
        sc.cycles.adaptive_threshold = float(cfg.get("adaptive_threshold", 0.01))
        sc.cycles.use_denoising = bool(cfg.get("denoise", True))
        # Static sets are not re-synced per frame (Cape Jones gpu practice).
        sc.cycles.use_persistent_data = bool(cfg.get("persistent_data", True))
    elif engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.eevee.taa_render_samples = int(cfg.get("samples", 16))
        except Exception:
            pass

    if cfg.get("resolution_x"):
        sc.render.resolution_x = int(cfg["resolution_x"])
    if cfg.get("resolution_y"):
        sc.render.resolution_y = int(cfg["resolution_y"])
    if cfg.get("resolution_percentage"):
        sc.render.resolution_percentage = int(cfg["resolution_percentage"])
    if cfg.get("fps"):
        sc.render.fps = int(cfg["fps"])
    if cfg.get("view_transform"):
        sc.view_settings.view_transform = cfg["view_transform"]

    sc.render.image_settings.file_format = "PNG"
    sc.frame_start = frame
    sc.frame_end = frame
    sc.frame_set(frame)
    # Blender appends the 4-digit frame number to filepath automatically
    # when rendering an animation range; for a single frame we set the
    # exact target path and render with animation=True over [f, f].
    sc.render.filepath = os.path.join(outdir, prefix)
    sc.render.use_file_extension = True

    bpy.context.view_layer.update()
    print(
        f"[render_one] frame={frame} engine={engine} "
        f"samples={cfg.get('samples')} res={sc.render.resolution_x}x"
        f"{sc.render.resolution_y}@{sc.render.resolution_percentage}% "
        f"out={sc.render.filepath}",
        flush=True,
    )
    bpy.ops.render.render(animation=True)
    expected = os.path.join(outdir, f"{prefix}{frame:04d}.png")
    if not (os.path.isfile(expected) and os.path.getsize(expected) > 0):
        print(f"[render_one] ERROR: expected output missing: {expected}", flush=True)
        return 3
    print(f"[render_one] DONE frame={frame} -> {expected}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
