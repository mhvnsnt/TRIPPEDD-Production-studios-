"""Build a continuous authored TRIPPEDD network ident source.

This is deliberately GENERATED editorial material: it is not physical source,
creator likeness, or finished God Molecule footage. It exists to exercise the
same source -> analysis -> editorial -> render -> QC path before EP01.

Blender background mode renders 480 frames (20 seconds at 24fps) at 1280x720.
Existing non-empty frames are reused so a killed render can resume.
"""
import math
import os
import time
import bpy

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
OUT = os.path.join(ROOT, "production", "network-ident", "generated")
FRAMES = os.path.join(OUT, "frames")
FPS = 24
DURATION_SECONDS = 20
TOTAL_FRAMES = FPS * DURATION_SECONDS
START = int(os.environ.get("TRIPPEDD_FRAME_START", "1"))
END = int(os.environ.get("TRIPPEDD_FRAME_END", str(TOTAL_FRAMES)))
os.makedirs(FRAMES, exist_ok=True)
if START < 1 or END < START or END > TOTAL_FRAMES:
    raise SystemExit(f"Invalid network ident frame range: {START}-{END}; expected 1-{TOTAL_FRAMES}")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.film_transparent = False

world = bpy.data.worlds.new("TRIPPEDD Network Ident World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.004, 0.002, 0.015, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.12


def mat(name, rgba, emission=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgba, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgba, 1)
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*rgba, 1)
        bsdf.inputs["Emission Strength"].default_value = emission
    return m

MAGENTA = mat("NetworkMagenta", (0.8, 0.03, 0.45), 2.5)
CYAN = mat("NetworkCyan", (0.02, 0.65, 1.0), 2.5)
GOLD = mat("NetworkGold", (0.95, 0.55, 0.04), 2.0)
WHITE = mat("NetworkWhite", (0.8, 0.8, 0.8), 1.0)
DARK = mat("NetworkDark", (0.01, 0.01, 0.02), 0.0)

# Camera looks down the Z axis at a stage so all motion is authored in one shot.
bpy.ops.object.camera_add(location=(0, 0, 22), rotation=(0, 0, 0))
cam = bpy.context.object
cam.rotation_euler = (0, 0, 0)
scene.camera = cam
cam.data.type = "ORTHO"
cam.data.ortho_scale = 13.0

# Central symbolic molecule/head: intentionally generic, never creator likeness.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=2.0, location=(0, 0, 0))
core = bpy.context.object
core.name = "GodMolecule_SymbolicCore"
core.data.materials.append(CYAN)

# Forehead-like sigil is a simple original geometric mark, not a claimed sacred symbol.
for z, r in ((0.8, 0.55), (0.0, 0.42), (-0.8, 0.55)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.07, major_segments=24, minor_segments=6, location=(0, z, 2.0), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object
    o.name = "Original_Geometric_Mark"
    o.data.materials.append(GOLD)

for i in range(8):
    bpy.ops.mesh.primitive_torus_add(major_radius=2.8 + i * 0.48, minor_radius=0.035 + i * 0.006, major_segments=64, minor_segments=6, location=(0, 0, 0), rotation=(i * 0.19, i * 0.11, i * 0.27))
    ring = bpy.context.object
    ring.name = f"NetworkOrbit_{i:02d}"
    ring.data.materials.append((MAGENTA, CYAN, GOLD)[i % 3])


def text_obj(body, location, size, material):
    bpy.ops.object.text_add(location=location, rotation=(0, 0, 0))
    t = bpy.context.object
    t.data.body = body
    t.data.align_x = "CENTER"
    t.data.align_y = "CENTER"
    t.data.size = size
    t.data.extrude = 0.015
    t.data.materials.append(material)
    return t

labels = [
    text_obj("TRIPPEDD", (0, -4.9, 0), 0.82, WHITE),
    text_obj("THE BASTARD", (-4.3, 2.9, 0), 0.42, GOLD),
    text_obj("IN THE BUSHES", (4.3, 2.9, 0), 0.42, MAGENTA),
    text_obj("GOD MOLECULE", (0, 4.9, 0), 0.42, CYAN),
    text_obj("TRIPPEDD NETWORK", (0, 0, 0), 0.25, WHITE),
]

for loc, energy, size in [((-6, -5, 7), 1000, 5), ((6, -2, 7), 900, 4), ((0, 6, 7), 850, 4)]:
    bpy.ops.object.light_add(type="AREA", location=loc)
    light = bpy.context.object
    light.data.energy = energy
    light.data.shape = "DISK"
    light.data.size = size
    light.rotation_euler = (0, 0, 0)

scene["TRIPPEDD_PROVENANCE"] = "GENERATED"
scene["TRIPPEDD_ASSET_CLASS"] = "NETWORK_IDENT"
scene["TRIPPEDD_NETWORK"] = "TRIPPEDD network"
scene["TRIPPEDD_SHOW"] = "Trippedd"
scene["TRIPPEDD_STUDIO"] = "TRIPPEDD Production studios"
scene["TRIPPEDD_CONTINUITY"] = "SINGLE_CONTINUOUS_AUTHORED_PIECE"
scene["TRIPPEDD_DURATION_SECONDS"] = DURATION_SECONDS
scene["TRIPPEDD_FPS"] = FPS
scene["TRIPPEDD_TOTAL_FRAMES"] = TOTAL_FRAMES
scene["TRIPPEDD_SOURCE_TRUTH"] = "Generated proof material; not physical source evidence."
scene["TRIPPEDD_GOD_MOLECULE"] = "Symbolic development reference only; no creator likeness."
scene["TRIPPEDD_REFERENCES"] = "Trippedd; The Bastard; In the Bushes; God Molecule"

started = time.time()
total = END - START + 1
for frame in range(START, END + 1):
    path = os.path.join(FRAMES, f"frame-{frame:04d}.png")
    if os.path.isfile(path) and os.path.getsize(path) > 0:
        continue
    scene.frame_set(frame)
    phase = (frame - 1) / TOTAL_FRAMES
    core.rotation_euler = (phase * math.tau * 0.7, phase * math.tau * 0.9, phase * math.tau)
    core.scale = (1.0 + 0.12 * math.sin(phase * math.tau * 2), 1.0 + 0.08 * math.cos(phase * math.tau * 3), 1.0)
    for i in range(8):
        ring = bpy.data.objects.get(f"NetworkOrbit_{i:02d}")
        if ring:
            ring.rotation_euler.z += 0.025 + i * 0.004
            ring.scale.x = 1.0 + 0.08 * math.sin(phase * math.tau * (i + 1))
    labels[0].scale = (1.0 + 0.08 * math.sin(phase * math.tau * 2),) * 3
    labels[4].scale = (1.0 + 0.25 * math.sin(phase * math.tau * 4),) * 3
    cam.data.ortho_scale = 13.0 + 0.7 * math.sin(phase * math.tau)
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        raise RuntimeError(f"Missing rendered frame: {path}")
    done = frame - START + 1
    elapsed = max(time.time() - started, 0.001)
    rate = done / elapsed
    print(f"PRODUCTION_PROGRESS stage=network-ident status=RUNNING progress={done*100/total:.1f}% work={done}/{total} elapsed={elapsed:.1f}s rate={rate:.3f} frames/s eta={(total-done)/rate if rate else 0:.1f}s", flush=True)

blend = os.path.join(OUT, f"network-ident-{START:04d}-{END:04d}.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend)
print(f"PRODUCTION_FINAL stage=network-ident status=COMPLETED work={total}/{total} duration={DURATION_SECONDS}s elapsed={time.time()-started:.1f}s", flush=True)
