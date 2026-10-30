#!/usr/bin/env python3
"""check_blender.py -- dump the visible mouth shape per frame from Blender.

Run inside Blender AFTER the generated mouthswap_blender.py build script:

  blender -b --python mouthswap_blender.py --python check_blender.py \
      -- --out dump.json

Writes {"fps": N, "frames": {"1": "X", "2": "A", ...}} where each value is
the phoneme code of the single Mouth_<CODE> plane whose hide_render is off
at that frame (null if none, "MULTI:..." if more than one -- both are
failures the verifier will catch).
"""

import json
import sys

import bpy


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = "dump.json"
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    scene = bpy.context.scene
    frames = {}
    for f in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(f)
        visible = [obj.name.split("_", 1)[1]
                   for obj in bpy.data.objects
                   if obj.name.startswith("Mouth_") and not obj.hide_render]
        if len(visible) == 1:
            frames[str(f)] = visible[0]
        elif not visible:
            frames[str(f)] = None
        else:
            frames[str(f)] = "MULTI:" + ",".join(sorted(visible))
    with open(out, "w") as fh:
        json.dump({"fps": scene.render.fps, "frames": frames}, fh)
    print(f"MOUTHSWAP_CHECK frames={len(frames)} fps={scene.render.fps} "
          f"out={out}")


if __name__ == "__main__":
    main()
