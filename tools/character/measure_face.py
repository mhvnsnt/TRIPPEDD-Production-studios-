"""
WHERE THE FACE ACTUALLY IS — measured, not guessed.

A rig built on bounding-box fractions ("the mouth is 30% up from the chin")
puts the jaw hinge in the wrong place on any head that is not the one those
fractions were tuned for, and the failure looks like bad animation rather than
a bad rig. So: render an ORTHOGRAPHIC front view of the real mesh, find the
landmarks with MediaPipe FaceMesh, and raycast each one back onto the surface
to recover a true 3D position.

Orthographic matters. Under perspective, a pixel does not map to a world column
and the back-projection is a guess with extra steps.

Stage 1 (Blender): render the ortho front view, record the exact camera framing.
Stage 2 (venv):    MediaPipe -> landmark pixels.
Stage 3 (Blender): raycast pixels -> 3D, write the measured anatomy.

  vendor/blender/blender -b -P tools/character/measure_face.py -- --stage 1 --lod LOD2
  .trippedd_venv/bin/python tools/character/measure_face.py --stage 2
  vendor/blender/blender -b -P tools/character/measure_face.py -- --stage 3 --lod LOD2
"""
import sys, os, json, math

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
def opt(f, d):
    return argv[argv.index(f) + 1] if f in argv else d

STAGE = opt("--stage", "1")
LOD = opt("--lod", "LOD2")
WORK = os.path.abspath(opt("--work", "renders/_rig_measure"))
RES = 1024
os.makedirs(WORK, exist_ok=True)

# ── stage 2 runs OUTSIDE Blender, in the venv that has MediaPipe ─────────────
if STAGE == "2":
    import cv2, numpy as np
    import mediapipe as mp

    shot = os.path.join(WORK, "front_ortho.png")
    if not os.path.exists(shot):
        sys.exit("stage 1 output missing: " + shot)
    img = cv2.imread(shot, cv2.IMREAD_UNCHANGED)
    if img is None:
        sys.exit("could not read " + shot)
    # Composite onto mid-grey: FaceMesh is trained on photographs, and a face
    # cut out against transparent or black loses the context it relies on.
    if img.shape[2] == 4:
        a = img[:, :, 3:4].astype(np.float32) / 255.0
        img = (img[:, :, :3].astype(np.float32) * a + 128 * (1 - a)).astype(np.uint8)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # MediaPipe 1.x REMOVED mp.solutions. The Tasks API replaces it and needs an
    # explicit model bundle, which is downloaded once rather than assumed.
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision

    model = os.path.join(os.getcwd(), ".trippedd_models", "face_landmarker.task")
    if not os.path.exists(model):
        sys.exit("missing " + model)

    landmarker = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=model),
        running_mode=vision.RunningMode.IMAGE,
        num_faces=1,
        output_face_blendshapes=True,
        min_face_detection_confidence=0.2,
        min_face_presence_confidence=0.2,
    ))
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
    result = landmarker.detect(mp_img)
    found = result.face_landmarks[0] if result.face_landmarks else None
    blendshapes = None
    if result.face_blendshapes:
        blendshapes = {c.category_name: round(float(c.score), 4) for c in result.face_blendshapes[0]}

    h, w = rgb.shape[:2]
    pts = [{"i": i, "x": lm.x * w, "y": lm.y * h, "z": lm.z} for i, lm in enumerate(found)]
    json.dump({"detected": True, "width": w, "height": h, "count": len(pts), "points": pts,
               "restBlendshapes": blendshapes},
              open(os.path.join(WORK, "landmarks.json"), "w"), indent=2)
    print("FaceLandmarker: %d landmarks in a %dx%d render" % (len(pts), w, h))
    if blendshapes:
        top = sorted(blendshapes.items(), key=lambda kv: -kv[1])[:5]
        print("  rest-pose blendshapes (top): " + ", ".join("%s %.2f" % t for t in top))
    sys.exit(0)

# ── stages 1 and 3 run inside Blender ───────────────────────────────────────
import bpy, mathutils

ROOT = os.getcwd()
LOD_FILE = os.path.join(ROOT, "assets/source_models", "MARS_%s.glb" % LOD)
if not os.path.exists(LOD_FILE):
    sys.exit("missing " + LOD_FILE)

def load_mars():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=LOD_FILE)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    if not meshes:
        sys.exit("the GLB imported no mesh")
    # One object to reason about. join() needs them all selected and one active.
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj

def bounds(obj):
    mn = mathutils.Vector((1e9,) * 3); mx = mathutils.Vector((-1e9,) * 3)
    for v in obj.data.vertices:
        w = obj.matrix_world @ v.co
        for i in range(3):
            mn[i] = min(mn[i], w[i]); mx[i] = max(mx[i], w[i])
    return mn, mx

obj = load_mars()
mn, mx = bounds(obj)
size = mx - mn
centre = (mn + mx) / 2

# glTF import puts +Y-up content into Blender's +Z-up. The face looks along -Y.
FACE_DIR = mathutils.Vector((0, -1, 0))
ortho_scale = max(size.x, size.z) * 1.05

if STAGE == "1":
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"   # flat, fast, and enough for landmarks
    scene.render.resolution_x = scene.render.resolution_y = RES
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "TEXTURE"

    cam_data = bpy.data.cameras.new("ORTHO")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = ortho_scale
    cam = bpy.data.objects.new("ORTHO", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    dist = size.y * 3 + 2
    cam.location = (centre.x, centre.y - dist, centre.z)
    cam.rotation_euler = (math.radians(90), 0, 0)   # look along +Y, i.e. at the face

    scene.render.filepath = os.path.join(WORK, "front_ortho.png")
    bpy.ops.render.render(write_still=True)

    json.dump({
        "lod": LOD, "res": RES, "orthoScale": ortho_scale,
        "camera": {"location": list(cam.location), "faceDir": list(FACE_DIR)},
        "bounds": {"min": list(mn), "max": list(mx), "size": list(size), "centre": list(centre)},
    }, open(os.path.join(WORK, "ortho_camera.json"), "w"), indent=2)
    print("stage 1: %s  (ortho scale %.3f)" % (scene.render.filepath, ortho_scale))
    sys.exit(0)

# ── stage 3: pixels -> 3D by raycasting the real surface ────────────────────
lm_path = os.path.join(WORK, "landmarks.json")
cam_path = os.path.join(WORK, "ortho_camera.json")
if not (os.path.exists(lm_path) and os.path.exists(cam_path)):
    sys.exit("run stages 1 and 2 first")
lms = json.load(open(lm_path))
if not lms.get("detected"):
    sys.exit("stage 2 found no face: " + lms.get("reason", ""))
cam_info = json.load(open(cam_path))
osc = cam_info["orthoScale"]

deps = bpy.context.evaluated_depsgraph_get()

def pixel_to_world(px, py):
    """Orthographic: a pixel IS a world column. Raycast it onto the surface."""
    u = (px / lms["width"]) - 0.5
    v = 0.5 - (py / lms["height"])
    x = centre.x + u * osc
    z = centre.z + v * osc
    origin = mathutils.Vector((x, mn.y - 1.0, z))
    hit, loc, nor, idx, o, mw = bpy.context.scene.ray_cast(deps, origin, mathutils.Vector((0, 1, 0)))
    return (hit, loc.copy() if hit else None, nor.copy() if hit else None)

# MediaPipe FaceMesh canonical indices.
GROUPS = {
    "chin": [152], "jaw_left": [172], "jaw_right": [397],
    "mouth_left": [61], "mouth_right": [291],
    "upper_lip": [13], "lower_lip": [14],
    "nose_tip": [1], "nose_bridge": [168],
    "eye_left_outer": [33], "eye_left_inner": [133], "eye_left_top": [159], "eye_left_bottom": [145],
    "eye_right_outer": [263], "eye_right_inner": [362], "eye_right_top": [386], "eye_right_bottom": [374],
    "brow_left": [105], "brow_right": [334],
    "forehead": [10], "cheek_left": [50], "cheek_right": [280],
    "ear_left": [234], "ear_right": [454],
}

measured, missed = {}, []
by_index = {p["i"]: p for p in lms["points"]}
for name, idxs in GROUPS.items():
    hits = []
    for i in idxs:
        p = by_index.get(i)
        if not p:
            continue
        hit, loc, nor = pixel_to_world(p["x"], p["y"])
        if hit:
            hits.append(loc)
    if hits:
        avg = sum(hits, mathutils.Vector()) / len(hits)
        measured[name] = [round(c, 5) for c in avg]
    else:
        missed.append(name)

out = {
    "lod": LOD,
    "method": "orthographic render -> MediaPipe FaceMesh -> raycast onto the real surface",
    "faceDirection": list(FACE_DIR),
    "bounds": cam_info["bounds"],
    "landmarks": measured,
    "missed": missed,
    "landmarkCount": lms["count"],
}
json.dump(out, open(os.path.join(WORK, "face_anatomy.json"), "w"), indent=2)

print("measured %d anatomical points (%d landmarks detected)" % (len(measured), lms["count"]))
for k in ["chin", "mouth_left", "mouth_right", "upper_lip", "lower_lip",
          "eye_left_outer", "eye_right_outer", "nose_tip", "ear_left", "ear_right"]:
    if k in measured:
        print("  %-16s %s" % (k, [round(c, 3) for c in measured[k]]))
if missed:
    print("  NOT HIT BY RAYCAST (reported, not invented): " + ", ".join(missed))
print("→ " + os.path.join(WORK, "face_anatomy.json"))
