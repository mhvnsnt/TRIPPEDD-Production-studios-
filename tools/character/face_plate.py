"""
ONE DEFINITION OF THE ANNOTATION PLATE'S GEOMETRY.

annotation_base.py renders the plate; ingest_linework.py reads the owner's marks
back off it. If those two ever disagreed about the camera by a pixel, his ground
truth would land somewhere it was never drawn -- and nothing would say so. So the
frame, the framing and the projection live here and both import them.

Pure numpy: this has to run inside Blender (bpy, no scipy) AND in the venv.

THE FRAME IS DERIVED FROM HIS FACE, NOT FROM WORLD AXES. Measured from the
canonical fit, his head rests pitched ~32.6 deg back from world up, so a
world-front camera photographs him from below and foreshortens the eyelid band --
the exact band he is marking.
"""
import os, json
import numpy as np

MW = 0.1930            # measured inter-commissure width
MM = MW / 50.0         # one millimetre, in scene units
CAM_DIST = 3.0         # ortho: distance is framing-neutral, but fix it so the
                       # recorded cameraOrigin is reproducible
PAD_W = 1.12
PAD_H = 1.42
LIFT  = 0.09           # frame centre lifted, so the forehead sigil is not cropped


def load_fit(root):
    fitp = os.path.join(root, "renders", "_rig_measure", "canonical_fit.json")
    npzp = os.path.join(root, "renders", "_rig_measure", "canonical_fit.npz")
    if not (os.path.exists(fitp) and os.path.exists(npzp)):
        raise SystemExit("REFUSED: no canonical fit -- run fit_canonical_face.py first")
    fit = json.load(open(fitp))
    sets = {k: np.array(v, float) for k, v in fit["sets"].items() if isinstance(v, list)}
    return fit, sets, np.load(npzp)["vertices"]


def head_frame(sets):
    """x = his left, up = brow-over-lips, fwd = out of the face. Right-handed."""
    x = sets["eyelid_L_lower"][0] - sets["eyelid_R_lower"][0]
    x = x / np.linalg.norm(x)
    brow = np.vstack([sets["eyebrow_R"], sets["eyebrow_L"]]).mean(0)
    lip = sets["lips_outer"].mean(0)
    up = brow - lip
    up -= x * np.dot(up, x)
    up /= np.linalg.norm(up)
    fwd = np.cross(x, up)
    if np.dot(fwd, [0, -1, 0]) < 0: fwd = -fwd
    return x, up, fwd


class Plate:
    """An orthographic plate: pixels <-> world columns, exactly."""

    def __init__(self, name, canon, x, up, fwd, cx, cu, half, res):
        self.name, self.res = name, res
        self.x, self.up, self.fwd = x, up, fwd
        self.centre = canon.mean(0)
        self.ortho = float(half * 2.0)
        self.origin = self.centre + x * cx + up * cu + fwd * CAM_DIST

    def project(self, p):
        rel = np.atleast_2d(np.asarray(p, float)) - self.origin
        px = (rel @ self.x / self.ortho + 0.5) * self.res
        py = (0.5 - rel @ self.up / self.ortho) * self.res
        out = np.stack([px, py], -1)
        return out[0] if np.ndim(p) == 1 else out

    def plane_point(self, px, py):
        """the world point on the camera plane that pixel (px,py) looks through"""
        return (self.origin
                + self.x * ((np.asarray(px, float) / self.res - 0.5) * self.ortho)
                + self.up * ((0.5 - np.asarray(py, float) / self.res) * self.ortho))

    def depth(self, p):
        return (np.atleast_2d(np.asarray(p, float)) - self.origin) @ self.fwd

    def manifest(self):
        return {"name": self.name, "res": self.res,
                "orthoScale": round(self.ortho, 6),
                "cameraOrigin": [round(float(v), 6) for v in self.origin]}


def face_plate(canon, x, up, fwd, res=1600, name="face"):
    P = (canon - canon.mean(0)) @ np.stack([x, up, fwd], 1)
    half = max(np.ptp(P[:, 0]) * PAD_W, np.ptp(P[:, 1]) * PAD_H) * 0.5
    cx = float(P[:, 0].mean())
    cu = float((P[:, 1].min() + P[:, 1].max()) * 0.5 + np.ptp(P[:, 1]) * LIFT)
    return Plate(name, canon, x, up, fwd, cx, cu, half, res)


def eye_plate(canon, sets, x, up, fwd, res=1600, name="eyes"):
    E = np.vstack([sets[k] for k in ("eyelid_R_upper", "eyelid_R_lower",
                                     "eyelid_L_upper", "eyelid_L_lower",
                                     "eyebrow_R", "eyebrow_L")])
    P = (E - canon.mean(0)) @ np.stack([x, up, fwd], 1)
    half = max(np.ptp(P[:, 0]), np.ptp(P[:, 1])) * 0.5 * 1.22
    cx = float((P[:, 0].min() + P[:, 0].max()) * 0.5)
    cu = float((P[:, 1].min() + P[:, 1].max()) * 0.5)
    return Plate(name, canon, x, up, fwd, cx, cu, half, res)


# ---------------------------------------------------------------- registration
# Kept identical to what annotation_base.py burns into the plate, so the reader
# can prove the image came back uncropped and unscaled.
def fiducial_geometry(res):
    t = max(2, res // 500)
    n = max(10, res // 40)
    ins = max(6, res // 160)
    return t, n, ins


def fiducial_mask(res, slack=12):
    """True where the registration marks live -- his strokes are never in here,
    which is how his GREEN lower-lid line stays separable from my GREEN border."""
    t, n, ins = fiducial_geometry(res)
    m = np.zeros((res, res), bool)
    edge = ins + max(t, n) + slack
    m[:edge, :] = True; m[-edge:, :] = True
    m[:, :edge] = True; m[:, -edge:] = True
    return m
