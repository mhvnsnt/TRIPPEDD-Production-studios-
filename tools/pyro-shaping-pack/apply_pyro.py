"""Apply a Pyro Shaping Pack look to the current scene.

Run inside Blender:
  blender -b scene.blend --python apply_pyro.py -- --look campfire
  blender -b --python apply_pyro.py -- --look explosion_burst --res 56 --frames 1 64 --bake

Without --bake the setup is left in REPLAY cache mode so scrubbing steps the
sim live. With --bake a resumable ALL cache is written next to the .blend
(or to --cache-dir). Saves the scene in place only when a .blend was opened;
in factory scenes pass --save path/to/out.blend.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyro_lib  # noqa: E402


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--look", required=True, help="one of: " + ", ".join(pyro_lib.list_looks()))
    ap.add_argument("--res", type=int, default=None, help="override domain resolution")
    ap.add_argument("--frames", type=int, nargs=2, default=(1, 48))
    ap.add_argument("--bake", action="store_true")
    ap.add_argument("--cache-dir", default=None)
    ap.add_argument("--save", default=None)
    args = ap.parse_args(argv)

    cache_dir = args.cache_dir
    if args.bake and not cache_dir:
        base = os.path.dirname(bpy_file()) or os.getcwd()
        cache_dir = os.path.join(base, "pyro_cache_" + args.look)
    report, domain, _flow = pyro_lib.apply_look(
        args.look, resolution=args.res, frames=tuple(args.frames), cache_dir=cache_dir)
    print("PYRO APPLIED:", report)

    if args.bake:
        import bpy
        bpy.context.view_layer.objects.active = domain
        domain.select_set(True)
        bpy.ops.fluid.bake_all()
        print("PYRO BAKED to", cache_dir)

    out = args.save or bpy_file()
    if out:
        import bpy
        bpy.ops.wm.save_as_mainfile(filepath=out)
        print("PYRO SAVED:", out)


def bpy_file():
    import bpy
    return bpy.data.filepath


if __name__ == "__main__":
    main()
