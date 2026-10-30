"""Headless proof for the Pyro Shaping Pack (SPEC H-4).

For two contrasting looks (explosion_burst, fog_bank):
  apply look -> step the Mantaflow sim live (REPLAY cache) to frame 16 ->
  render one small Cycles still per look.

Then compare_pngs.py measures how different the two renders are.

Run via tests/run_test.sh (handles the flock box discipline), or directly:
  blender -b --factory-startup --python tests/test_pyro.py -- --out /tmp/pyro_test
"""
import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pyro_lib  # noqa: E402

TEST_FRAME = 16
FRAMES = (1, 20)
RESOLUTION = 28
LOOKS = ("explosion_burst", "fog_bank")


def setup_stage():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 8
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 96
    scene.render.resolution_y = 96
    scene.render.image_settings.file_format = "PNG"
    world = bpy.data.worlds.new("PyroTestWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
    bg.inputs[1].default_value = 0.0

    cam_data = bpy.data.cameras.new("Cam")
    cam = bpy.data.objects.new("Cam", cam_data)
    scene.collection.objects.link(cam)
    cam.location = (0.0, -7.5, 2.2)
    cam.rotation_euler = (1.35, 0.0, 0.0)
    scene.camera = cam

    light_data = bpy.data.lights.new("Key", "POINT")
    light_data.energy = 900.0
    light = bpy.data.objects.new("Key", light_data)
    scene.collection.objects.link(light)
    light.location = (2.5, -2.0, 4.5)


def run_look(look, out_dir):
    setup_stage()
    report, domain, _flow = pyro_lib.apply_look(
        look, resolution=RESOLUTION, frames=FRAMES)
    ds = domain.modifiers["Fluid"].domain_settings
    ds.cache_type = "REPLAY"  # step the solver live, no bake files needed
    scene = bpy.context.scene
    for frame in range(FRAMES[0], TEST_FRAME + 1):
        scene.frame_set(frame)
    out = os.path.join(out_dir, "render_%s_f%03d.png" % (look, TEST_FRAME))
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("TEST RENDER:", out, os.path.getsize(out), "bytes |", report)
    return out


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out_dir = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/pyro_test"
    os.makedirs(out_dir, exist_ok=True)
    for look in LOOKS:
        run_look(look, out_dir)
    print("TEST DONE")


if __name__ == "__main__":
    main()
