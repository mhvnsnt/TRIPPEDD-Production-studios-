#!/usr/bin/env python3
"""Render and measure a real Mars blink. Fails if the brow moves or the eye stays open."""
import json
import math
import os
import sys

import bpy
import mathutils

ROOT = os.getcwd()
AUTH_PATH = os.path.join(ROOT, "renders", "_rig_measure", "face_landmark_authority.json")
BLEND = os.path.join(ROOT, "assets", "rigs", "MARS_FACE.blend")
OUT = os.path.join(ROOT, "renders", "_rig_measure", "blink_qc")
os.makedirs(OUT, exist_ok=True)

if not os.path.exists(AUTH_PATH):
    raise SystemExit("missing face landmark authority")
if not os.path.exists(BLEND):
    raise SystemExit("missing MARS_FACE.blend — build rig first")

auth = json.load(open(AUTH_PATH))
head = None

bpy.ops.wm.open_mainfile(filepath=BLEND)
head = bpy.data.objects.get("MARS_MESH")
if head is None:
    raise SystemExit("MARS_MESH missing")
for side in ("L", "R"):
    if head.data.shape_keys is None or head.data.shape_keys.key_blocks.get("blink_" + side) is None:
        raise SystemExit("blink_%s shape key missing" % side)
    if bpy.data.objects.get("MARS_EYE_" + side) is None:
        raise SystemExit("MARS_EYE_%s missing" % side)

V = mathutils.Vector

def pts(ids):
    return [V(auth["landmarks"][str(i)]["xyz"]) for i in ids]

groups = {
    "L": {
        "upper": auth["semantic_sets"]["eye_L_upper"],
        "lower": auth["semantic_sets"]["eye_L_lower"],
        "brow": auth["semantic_sets"]["brow_L"],
    },
    "R": {
        "upper": auth["semantic_sets"]["eye_R_upper"],
        "lower": auth["semantic_sets"]["eye_R_lower"],
        "brow": auth["semantic_sets"]["brow_R"],
    },
}

# Map authority coordinates to the current post-boolean head by nearest vertex.
# We intentionally do not reuse pre-boolean vertex indices.
kd = mathutils.kdtree.KDTree(len(head.data.vertices))
for i, v in enumerate(head.data.vertices):
    kd.insert(head.matrix_world @ v.co, i)
kd.balance()

def current_indices(ids):
    out = []
    for p in pts(ids):
        co, idx, dist = kd.find(p)
        if dist > 0.02:
            raise SystemExit("semantic point is %.5f from current head; registration drift" % dist)
        out.append(idx)
    return sorted(set(out))

tracked = {}
for side, g in groups.items():
    tracked[side] = {
        "upper": current_indices(g["upper"]),
        "lower": current_indices(g["lower"]),
        "brow": current_indices(g["brow"]),
    }

def world_positions(indices):
    return {i: head.matrix_world @ head.data.vertices[i].co.copy() for i in indices}

def eye_rays(side):
    up = pts(groups[side]["upper"])
    lo = pts(groups[side]["lower"])
    center = (sum(up, V((0,0,0))) + sum(lo, V((0,0,0)))) / (len(up) + len(lo))
    span = up[len(up)//2] - lo[len(lo)//2]
    opening = span.length
    origin = center + V((0, -10.0 * opening, 0))
    direction = V((0, 1, 0))
    deps = bpy.context.evaluated_depsgraph_get()
    hits = {"eyeball": 0, "other": 0, "miss": 0}
    for j in range(25):
        t = j / 24.0 - 0.5
        o = origin + span * t * 0.55
        hit, loc, nor, idx, obj, matrix = bpy.context.scene.ray_cast(deps, o, direction)
        if not hit:
            hits["miss"] += 1
        elif obj.name.startswith("MARS_EYE_"):
            hits["eyeball"] += 1
        else:
            hits["other"] += 1
    return hits, opening

def set_blink(value):
    for side in ("L", "R"):
        head.data.shape_keys.key_blocks["blink_" + side].value = value
    bpy.context.view_layer.update()

# Rest and closed measurements.
set_blink(0.0)
rest_pos = {side: world_positions(sorted(set(sum(tracked[side].values(), [])))) for side in tracked}
rest_rays = {}
openings = {}
for side in ("L", "R"):
    rest_rays[side], openings[side] = eye_rays(side)

set_blink(1.0)
closed_pos = {side: world_positions(sorted(set(sum(tracked[side].values(), [])))) for side in tracked}
closed_rays = {side: eye_rays(side)[0] for side in ("L", "R")}

report = {"schema": "trippedd.mars-blink-qc/v1", "eyes": {}, "renders": []}
for side in ("L", "R"):
    upper = tracked[side]["upper"]
    brow = tracked[side]["brow"]
    upper_travel = max((closed_pos[side][i] - rest_pos[side][i]).length for i in upper)
    brow_travel = max((closed_pos[side][i] - rest_pos[side][i]).length for i in brow)
    report["eyes"][side] = {
        "opening": openings[side],
        "upperLidTravel": upper_travel,
        "browLeakage": brow_travel,
        "restRays": rest_rays[side],
        "closedRays": closed_rays[side],
        "gates": {
            "upperLidMoves": upper_travel >= openings[side] * 0.50,
            "browStationary": brow_travel <= openings[side] * 0.01,
            "eyeballVisibleAtRest": rest_rays[side]["eyeball"] >= 8,
            "eyeballCoveredAtBlink": closed_rays[side]["eyeball"] <= 2,
        },
    }

# Fail before rendering if the motion contract is not met.
for side, e in report["eyes"].items():
    if not all(e["gates"].values()):
        raise SystemExit("BLINK FAILED %s: %s" % (side, json.dumps(e)))

# Render real before/after pixels.
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"

# Use existing camera when present; otherwise create a deterministic ortho camera.
if scene.camera is None:
    mn = V((1e9,)*3); mx = V((-1e9,)*3)
    for v in head.data.vertices:
        p = head.matrix_world @ v.co
        mn.x=min(mn.x,p.x); mn.y=min(mn.y,p.y); mn.z=min(mn.z,p.z)
        mx.x=max(mx.x,p.x); mx.y=max(mx.y,p.y); mx.z=max(mx.z,p.z)
    c=(mn+mx)/2
    camd=bpy.data.cameras.new("BLINK_QC_CAMERA")
    camd.type="ORTHO"; camd.ortho_scale=max(mx.x-mn.x,mx.z-mn.z)*0.45
    cam=bpy.data.objects.new("BLINK_QC_CAMERA",camd)
    scene.collection.objects.link(cam)
    cam.location=(c.x,c.y-((mx.y-mn.y)*3+1),c.z)
    cam.rotation_euler=(math.radians(90),0,0)
    scene.camera=cam

for value, name in ((0.0, "blink_rest.png"), (1.0, "blink_closed.png")):
    set_blink(value)
    scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    report["renders"].append(os.path.relpath(scene.render.filepath, ROOT))

with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(report, f, indent=2)

print("BLINK QC PASS")
print(json.dumps(report, indent=2))
