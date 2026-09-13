"""
SHOW IT. The owner's standing instruction, and he had to repeat it:

    "U have to show me this stuff in screenshots my eyes and input will help u
     like they always do"                                    -- 2026-09-13
    "you don't even try and use all the tools to actually watch things as they
     play it visually ... you just be trying to look at frames, and then you lie
     about what's rendering in the frame."          -- OWNER LAW #4

A penetration number is not a picture of hair going through his face. This renders
the hair sim from his own FRONT and SIDE orthographic frames, over the whole take,
and marks EVERY vertex the measurement flagged -- at the size and colour of its own
depth -- directly on the pixels. Collision OFF and collision ON, same frames, side
by side, so the comparison is of the variable and not of two different shots.

The projection is not a guess: it is the same head frame (face_plate.head_frame)
and the same orthographic scale the renderer used, so a marked pixel is the pixel
that vertex occupies.

    vendor/blender/blender -b -P tools/hair/hair_motion.py -- ... --contact-out X.npz
    ./.trippedd_venv/bin/python tools/character/render_penetration_proof.py \
        --on X_on.npz --off X_off.npz --frames-dir docs/evidence/hair_motion \
        --out docs/evidence/collision
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import face_plate as FP
from face_plate import MM
import igl
from PIL import Image, ImageDraw, ImageFont


def depths(npz, pair_a="HAIR_SIM", pair_b="MARS_MESH_SKIN", subset="MARS_FACE_SKIN"):
    z = np.load(npz)
    Bf = z["%s/tris" % pair_b]
    Sf = z["%s/tris" % subset]
    keys = {tuple(sorted(map(int, f))): i for i, f in enumerate(Bf)}
    mask = np.zeros(len(Bf), dtype=bool)
    for f in Sf:
        k = tuple(sorted(map(int, f)))
        if k in keys:
            mask[keys[k]] = True
    A = z["%s/verts" % pair_a]
    out = []
    for fi in range(A.shape[0]):
        S, I, _, _ = igl.signed_distance(
            np.ascontiguousarray(A[fi], dtype=np.float64),
            np.ascontiguousarray(z["%s/verts" % pair_b][fi], dtype=np.float64),
            np.ascontiguousarray(Bf, dtype=np.int32),
            igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
        S = np.asarray(S); I = np.asarray(I, dtype=np.int64)
        d = np.where((S < 0) & mask[np.clip(I, 0, len(mask) - 1)], -S, 0.0) / MM
        out.append(d)
    return np.array(out), A, z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--on", required=True)
    ap.add_argument("--off", required=True)
    ap.add_argument("--frames-on", required=True)
    ap.add_argument("--frames-off", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tol-mm", type=float, default=1.0)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    D_on, A_on, z = depths(a.on)
    D_off, A_off, _ = depths(a.off)
    worst = int(np.argmax(D_on.max(axis=1)))

    # THE CAMERA BASIS IS HIS HEAD FRAME, NOT THE WORLD AXES. His head rests about
    # 32.6 degrees pitched back from world up, and the FRONT camera's right vector
    # is measured at (-0.995, 0.055, -0.081) -- very nearly MINUS world x. So a
    # marker projected with world x/z is mirrored left-for-right AND sheared
    # vertically, while still producing a picture that looks entirely plausible.
    # That is the worst kind of wrong: an overlay you would read as evidence.
    # Rebuild the exact (right, up, forward) triple the renderer built its cameras
    # from, out of the same face_plate.head_frame, so a marked pixel is the pixel
    # that vertex actually occupies.
    ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    _fit, _sets, _canon = FP.load_fit(ROOT)
    hx, hup, hfwd = FP.head_frame(_sets)
    P0 = z["MARS_MESH_SKIN/verts"][0]
    ctr = P0.mean(0)
    rad = float(np.linalg.norm(P0 - ctr, axis=1).max())
    BASIS = {}
    # FRONT IS +fwd. face_plate.head_frame documents fwd as "out of the face" and its
    # own plate camera sits at centre + fwd*CAM_DIST -- the plates the owner DREW ON are
    # framed that way. Every camera here used -fwd, so every "FRONT" render in this
    # session was shot from BEHIND HIS HEAD. Measured against his own drawn features:
    # dot(nostril direction, fwd) = +0.68 (L) and +0.93 (R), so fwd points at his face.
    # Never re-derive this from a world axis; derive it from a feature he marked.
    for _nm, _dv in (("FRONT", np.asarray(hfwd, float)), ("SIDE", np.asarray(hx, float))):
        _d = _dv / np.linalg.norm(_dv)
        _u = np.asarray(hup, float).copy()
        _u -= _d * np.dot(_u, _d)
        _u /= np.linalg.norm(_u)
        BASIS[_nm] = (np.cross(_u, _d), _u, _d)
    panels = []
    # THE FRAMES MUST COME FROM THEIR OWN RUN. Pointing both halves of an A/B at
    # one render directory would label ON pixels as OFF, which is precisely the
    # thing he has caught before: describing a render in words the pixels do not
    # support.
    for label, D, A, fdir in (("COLLISION OFF", D_off, A_off, a.frames_off),
                              ("COLLISION ON", D_on, A_on, a.frames_on)):
        for cam in ("FRONT", "SIDE"):
            src = os.path.join(fdir, "hair_%s_%02d.png" % (cam, worst))
            if not os.path.exists(src):
                print("missing render %s -- run hair_motion without --no-render" % src)
                return 2
            im = Image.open(src).convert("RGB")
            W, H = im.size
            dr = ImageDraw.Draw(im, "RGBA")
            # the render cameras are ORTHO with ortho_scale = rad*2.3, looking down
            # -fwd (FRONT) and +x (SIDE); a pixel is therefore a world column and the
            # projection is exact rather than fitted
            sc = rad * 2.3
            P = A[worst]
            rel = P - ctr
            r_, u_, d_ = BASIS[cam]
            # an ORTHO camera's image coordinates are the components along its own
            # right and up vectors; depth along d is discarded, which is exactly
            # what makes a pixel a world column
            px = ((rel @ r_) / sc + 0.5) * W
            py = (0.5 - (rel @ u_) / sc) * H
            d = D[worst]
            hit = np.nonzero(d > a.tol_mm)[0]
            for i in hit:
                r = 1.5 + 3.0 * min(1.0, d[i] / 25.0)
                c = (255, int(max(0, 200 - 8 * d[i])), 40, 210)
                dr.ellipse([px[i] - r, py[i] - r, px[i] + r, py[i] + r], fill=c)
            dr.rectangle([0, 0, W, 26], fill=(0, 0, 0, 190))
            dr.text((7, 6), "%s  %s  frame %d   %d verts through his face, deepest %.2f mm"
                    % (label, cam, worst, len(hit), float(d.max())), fill=(255, 220, 120))
            panels.append(im)

    W, H = panels[0].size
    sheet = Image.new("RGB", (W * 2, H * 2), (14, 14, 16))
    for i, im in enumerate(panels):
        sheet.paste(im, ((i % 2) * W, (i // 2) * H))
    outp = os.path.join(a.out, "hair_through_face_AB.png")
    sheet.save(outp)
    print("wrote %s" % outp)
    print("worst frame %d   OFF %.2f mm / %d verts   ON %.2f mm / %d verts"
          % (worst, D_off[worst].max(), int((D_off[worst] > a.tol_mm).sum()),
             D_on[worst].max(), int((D_on[worst] > a.tol_mm).sum())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
