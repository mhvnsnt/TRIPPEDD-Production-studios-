"""
VENDOR THE FACS BASIS — ICT-FaceKit, MIT, 53 NAMED expression shapes.

GNM gives anatomy (20 muscle territories, 383 expression deltas) but its basis
is PCA: `lower_face_region_074` is a direction in shape space with no name and
no FACS meaning. You cannot ask a PCA component for a smile.

ICT-FaceKit is the other half and it is the one that carries the NAMES. Its
expression set is FACS/ARKit-labelled GEOMETRY -- browDown_L, cheekPuff_R,
eyeBlink_L, jawOpen, mouthSmile_L, noseSneer_R -- 53 shapes on a 26,719-vertex
head, MIT licensed, from USC ICT's light-stage scans. Named shapes are what a
rig control can actually be wired to.

This reads the 158 shipped OBJs and banks ONLY what Mars needs: the neutral, the
53 expression deltas, the 68 Multi-PIE landmark indices, and the part ranges.
The 100 identity shapes are NOT vendored -- they vary WHO the face is, and Mars
is already who he is. They stay one `git clone` away and the manifest says so.

DELTAS, NOT ABSOLUTE SHAPES. Each OBJ is a full posed head; what transfers onto
another face is the displacement from neutral, so that is what is stored. It is
also ~40x smaller because most of a head does not move for a given expression.

  .trippedd_venv/bin/python tools/character/vendor_ict_facs.py --src <ict-clone>
"""
import os, sys, json, hashlib
import numpy as np

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
SRC = os.path.abspath(opt("--src", "vendor/ict/FaceXModel"))
OUT = os.path.abspath(opt("--out", "vendor/ict"))
os.makedirs(OUT, exist_ok=True)

# The 68-point Multi-PIE indices, copied from ICT-FaceKit's own README table.
LM68 = [1225, 1888, 1052, 367, 1719, 1722, 2199, 1447, 966, 3661, 4390, 3927,
        3924, 2608, 3272, 4088, 3443, 268, 493, 1914, 2044, 1401, 3615, 4240,
        4114, 2734, 2509, 978, 4527, 4942, 4857, 1140, 2075, 1147, 4269, 3360,
        1507, 1542, 1537, 1528, 1518, 1511, 3742, 3751, 3756, 3721, 3725, 3732,
        5708, 5695, 2081, 0, 4275, 6200, 6213, 6346, 6461, 5518, 5957, 5841,
        5702, 5711, 5533, 6216, 6207, 6470, 5517, 5966]

# Part ranges, from the README topology table. Inclusive on both ends there.
PARTS = {
    "face": (0, 9408), "head_and_neck": (9409, 11247), "mouth_socket": (11248, 13293),
    "eye_socket_left": (13294, 13677), "eye_socket_right": (13678, 14061),
    "gums_and_tongue": (14062, 17038), "teeth": (17039, 21450),
    "eyeball_left": (21451, 23020), "eyeball_right": (23021, 24590),
    "lacrimal_left": (24591, 24794), "lacrimal_right": (24795, 24998),
    "eye_blend_left": (24999, 25022), "eye_blend_right": (25023, 25046),
    "eye_occlusion_left": (25047, 25198), "eye_occlusion_right": (25199, 25350),
    "eyelashes_left": (25351, 26034), "eyelashes_right": (26035, 26718),
}

def read_obj_verts(path):
    """Vertices only, in file order. ICT's OBJs share one topology, so index i
    means the same anatomical point in every file -- which is the whole reason
    a delta is meaningful."""
    V = []
    with open(path, "r") as fh:
        for line in fh:
            if line.startswith("v "):
                p = line.split()
                V.append((float(p[1]), float(p[2]), float(p[3])))
    return np.asarray(V, np.float64)

def read_obj_faces(path):
    F = []
    with open(path, "r") as fh:
        for line in fh:
            if line.startswith("f "):
                idx = [int(t.split("/")[0]) - 1 for t in line.split()[1:]]
                F.append(idx)
    return F

neutral_path = os.path.join(SRC, "generic_neutral_mesh.obj")
if not os.path.exists(neutral_path):
    sys.exit("no ICT neutral at %s -- clone https://github.com/ICT-VGL/ICT-FaceKit" % SRC)

N = read_obj_verts(neutral_path)
print("ICT neutral: %d vertices" % len(N))
if len(N) != 26719:
    sys.exit("expected 26719 vertices, got %d -- the part ranges below would be wrong" % len(N))

faces = read_obj_faces(neutral_path)
quads = np.asarray([f for f in faces if len(f) == 4], np.int32)
tris = np.asarray([f for f in faces if len(f) == 3], np.int32)
print("faces: %d quads · %d tris" % (len(quads), len(tris)))

# Expression shapes = everything that is neither the neutral nor an identity.
shapes = sorted(f[:-4] for f in os.listdir(SRC)
                if f.endswith(".obj")
                and not f.startswith("identity")
                and f != "generic_neutral_mesh.obj")
print("expression shapes: %d" % len(shapes))

D = np.zeros((len(shapes), len(N), 3), np.float32)
stats = []
for i, nm in enumerate(shapes):
    V = read_obj_verts(os.path.join(SRC, nm + ".obj"))
    if len(V) != len(N):
        sys.exit("%s has %d vertices, neutral has %d -- topologies disagree" % (nm, len(V), len(N)))
    d = V - N
    D[i] = d
    mag = np.linalg.norm(d, axis=1)
    moved = int((mag > 1e-5).sum())
    stats.append((nm, moved, float(mag.max())))
    print("  %-18s %6d verts move · max %.4f" % (nm, moved, mag.max()))

dead = [s for s in stats if s[1] == 0]
if dead:
    sys.exit("these shapes are identical to the neutral, which means they were "
             "read wrong: %s" % ", ".join(s[0] for s in dead))

out_npz = os.path.join(OUT, "ict_facs.npz")
np.savez_compressed(
    out_npz,
    neutral=N.astype(np.float32),
    shape_names=np.array(shapes),
    deltas=D,
    quads=quads, tris=tris,
    landmarks68=np.array(LM68, np.int32),
    part_names=np.array(list(PARTS.keys())),
    part_ranges=np.array([PARTS[k] for k in PARTS], np.int32),
)
sha = hashlib.sha256(open(out_npz, "rb").read()).hexdigest()
size = os.path.getsize(out_npz)
print("\n%s  %.1f MB  sha256 %s" % (out_npz, size / 1e6, sha[:16]))

json.dump({
    "source": "ICT-VGL/ICT-FaceKit",
    "url": "https://github.com/ICT-VGL/ICT-FaceKit",
    "license": "MIT",
    "copyright": "2020 USC Institute for Creative Technologies",
    "what": "FACS/ARKit-named facial expression blendshapes on a common topology, "
            "derived from light-stage scans",
    "vendored": {
        "file": "ict_facs.npz", "bytes": size, "sha256": sha,
        "vertices": int(len(N)), "quads": int(len(quads)), "tris": int(len(tris)),
        "expressionShapes": len(shapes),
        "storedAs": "deltas from the neutral, float32 -- an absolute shape set would be "
                    "~40x larger and says nothing extra",
    },
    "notVendored": {
        "identityShapes": 100,
        "why": "identity shapes vary WHO the face is. Mars already is who he is, and "
               "his geometry is canonical and never regenerated. They remain available "
               "from the upstream clone.",
    },
    "shapes": [{"name": n, "movingVerts": m, "maxDisplacement": round(x, 5)}
               for n, m, x in stats],
    "landmarks68": "Multi-PIE 68-point indices as published in ICT-FaceKit's README",
    "parts": {k: list(v) for k, v in PARTS.items()},
}, open(os.path.join(OUT, "ict_facs.json"), "w"), indent=2)
print("manifest -> %s" % os.path.join(OUT, "ict_facs.json"))
