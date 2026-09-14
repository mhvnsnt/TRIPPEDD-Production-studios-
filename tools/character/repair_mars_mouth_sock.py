"""
SURGICAL REPAIR OF THE MARS MOUTH SOCK.

The mouth-volume survey found MARS_MOUTH_SOCK in front of the intended oral
space: it is the first surface across the tongue/roof region instead of a thin
vestibular lining behind the lips and cheeks. This tool does NOT remesh MARS.
It samples the measured mouth volume with rays, records exactly which sock
faces are frontmost, and can delete only those faces.

Workflow:
  1. --report-only : produce a face/ray evidence JSON; no geometry changes.
  2. --apply       : delete only sock faces actually hit as the frontmost
                     surface from the measured oral-volume sample.
  3. render the same open-mouth camera, reopen it, SHA it, then run mouth proof.

The operation deliberately leaves teeth, tongue, gums/palate, cavity wall and
MARS_MESH untouched. A vestibular sock face that is not frontmost in the oral
opening is retained.
"""
import bpy, bmesh, sys, os, json, math
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(name, default): return argv[argv.index(name) + 1] if name in argv else default
def flag(name): return name in argv
def die(msg):
    print("\n*** REFUSED: %s\n" % msg, flush=True)
    sys.exit(1)

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT = os.path.abspath(opt("--out", os.path.join(ROOT, "assets/variants/MARS_MOUTH_SOCK_SURGICAL_CANDIDATE.blend")))
REPORT = os.path.abspath(opt("--report", os.path.join(ROOT, "docs/evidence/oral/mouth_sock_surgical.json")))
APPLY = flag("--apply")

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
sock = bpy.data.objects.get("MARS_MOUTH_SOCK")
if sock is None:
    die("MARS_MOUTH_SOCK is absent")
head = bpy.data.objects.get("MARS_MESH")
if head is None:
    die("MARS_MESH is absent")

frame_path = os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")
if not os.path.exists(frame_path): die("missing mouth_anatomy.json")
MA = json.load(open(frame_path))
FRAME = Matrix(MA["frame"]["matrix"])
FINV = FRAME.inverted()
W = sock.matrix_world
WINV = W.inverted()

# The existing mouth-frame convention is independently checked by
# split_lip_seam.py: local -Y is outward, therefore +Y is into the mouth.
OUTWARD = (FRAME.to_3x3() @ Vector((0, -1, 0))).normalized()
INWARD = -OUTWARD

# Measured aperture. The sample is intentionally inside the aperture, not a
# guessed 1-mm band immediately under the incisors.
left = Vector(MA["aperture"]["cornerLeft"])
right = Vector(MA["aperture"]["cornerRight"])
center = (left + right) * 0.5
width = (right - left).length
L = FINV @ left
R = FINV @ right
C = FINV @ center

# Sample the actual roof-to-tongue volume. Bounds are derived from the mouth
# geometry when possible; explicit values are only used as conservative local
# frame bounds, not as a cutting plane for the mesh.
xs = float(opt("--x-margin-mm", "2.0")) / 1000.0
zs = float(opt("--z-margin-mm", "2.0")) / 1000.0
x0, x1 = min(L.x, R.x) - xs, max(L.x, R.x) + xs
# Use measured visible oral contents to establish vertical coverage. These
# names are intentional: missing content is a refusal, not a guess.
def local_bounds(ob_name):
    ob = bpy.data.objects.get(ob_name)
    if ob is None: return None
    pts = [FINV @ (ob.matrix_world @ v.co) for v in ob.data.vertices]
    if not pts: return None
    return min(p.z for p in pts), max(p.z for p in pts)

tongue_b = local_bounds("MARS_TONGUE") or local_bounds("MARS_TONGUE_MESH")
upper_b = local_bounds("MARS_TEETH_UPPER")
if tongue_b is None or upper_b is None:
    die("could not derive tongue and upper-tooth bounds for the oral-volume sample")
z0 = tongue_b[0] - zs
z1 = max(upper_b[1], tongue_b[1]) + zs

# Start rays just outside the measured mouth plane. We need enough travel to
# encounter the intended cavity, but never shoot through the entire head.
# The ray's FIRST hit is authoritative for this diagnosis.
start_local_y = C.y - width * 0.35
end_local_y = C.y + width * 2.5
N_X = int(opt("--samples-x", "81"))
N_Z = int(opt("--samples-z", "61"))

deps = bpy.context.evaluated_depsgraph_get()
face_hits = {}
first_hits = {}
ray_total = 0
sock_first = 0

for ix in range(N_X):
    x = x0 + (x1 - x0) * ix / max(1, N_X - 1)
    for iz in range(N_Z):
        z = z0 + (z1 - z0) * iz / max(1, N_Z - 1)
        p_local = Vector((x, start_local_y, z))
        origin = FRAME @ p_local
        direction = INWARD.normalized()
        distance = max(width * 3.0, 0.10)
        hit, loc, normal, face_index, obj, _ = scene.ray_cast(
            deps, origin, direction, distance=distance)
        ray_total += 1
        if not hit or obj is None:
            continue
        name = obj.name
        first_hits[name] = first_hits.get(name, 0) + 1
        if obj != sock:
            continue
        sock_first += 1
        face_hits[int(face_index)] = face_hits.get(int(face_index), 0) + 1

report = {
    "status": "MEASURED",
    "rig": RIG,
    "sockObject": sock.name,
    "sample": {
        "rays": ray_total,
        "grid": [N_X, N_Z],
        "firstHitCounts": first_hits,
        "sockFirstHitRays": sock_first,
        "sockFirstHitShare": round(sock_first / ray_total, 6) if ray_total else 0,
        "oralVolumeLocalX": [x0, x1],
        "oralVolumeLocalZ": [z0, z1],
        "startLocalY": start_local_y,
        "endLocalY": end_local_y,
    },
    "candidateFaces": [
        {"faceIndex": int(i), "frontmostRayCount": int(n)}
        for i, n in sorted(face_hits.items(), key=lambda kv: (-kv[1], kv[0]))
    ],
    "geometryChanged": False,
}

if not face_hits:
    die("the measured oral-volume rays did not identify any frontmost sock faces")

if not APPLY:
    json.dump(report, open(REPORT, "w"), indent=2)
    print("REPORT_ONLY: %d sock faces are frontmost across %d/%d oral rays" %
          (len(face_hits), sock_first, ray_total), flush=True)
    print("REPORT=%s" % REPORT, flush=True)
    sys.exit(0)

bm = bmesh.new()
bm.from_mesh(sock.data)
bm.faces.ensure_lookup_table()
selected = [bm.faces[i] for i in face_hits if 0 <= i < len(bm.faces)]
if not selected:
    bm.free(); die("ray report face indices did not map to MARS_MOUTH_SOCK faces")

# Delete faces only. This preserves boundary vertices/edges so the vestibular
# lining can remain as a thin band. Blender documents "Only Faces" as deleting
# selected faces while retaining edges; that is exactly the operation wanted
# here, rather than dissolving/filling the obstruction back in.
for f in selected: f.select = True
bmesh.ops.delete(bm, geom=selected, context='FACES_ONLY')
bm.to_mesh(sock.data)
bm.free()
sock.data.update()

report["geometryChanged"] = True
report["removedFaceCount"] = len(selected)
report["removedFaceIndices"] = sorted(int(i) for i in face_hits)
report["postcondition"] = "render_same_open_camera_then_pixel_truth_and_SHA"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
os.makedirs(os.path.dirname(REPORT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
json.dump(report, open(REPORT, "w"), indent=2)

print("APPLIED: removed %d frontmost MARS_MOUTH_SOCK faces" % len(selected), flush=True)
print("VERTEX POSITIONS WERE NOT MOVED", flush=True)
print("CANDIDATE=%s" % OUT, flush=True)
print("REPORT=%s" % REPORT, flush=True)
