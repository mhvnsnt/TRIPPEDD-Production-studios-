#!/usr/bin/env python3
"""Wire: OpenCV (Apache-2.0) film-restoration filters — wave48 lane-b.

Reproduce:  python3 tools/wave48_lane_b/wire_opencv_restore.py
Exit nonzero on any gate failure.

Pipeline (all real bytes, seeded RNG):
  1. Generate deterministic 320x180 "clean" film frame (checker + gradient).
  2. Add seeded Gaussian noise -> noisy.png.
  3. cv2.fastNlMeansDenoising -> denoised.png.
     Gate: RMSE(denoised, clean) < RMSE(noisy, clean) * 0.9 (real improvement).
  4. Add a horizontal "scratch" bar -> scratched.png; cv2.inpaint (Telea) ->
     inpainted.png.
     Gate: RMSE over the scratch region after inpaint < RMSE before inpaint.
  5. Write SHA256SUMS + log.
"""
import hashlib, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(ROOT, "proofs_opencv")
os.makedirs(PROOFS, exist_ok=True)

import numpy as np
import cv2

W, H = 320, 180
SEED = 20261008

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def rmse(a, b, mask=None):
    d = (a.astype(np.float32) - b.astype(np.float32))
    if mask is not None:
        d = d[mask > 0]
    return float(np.sqrt(np.mean(d ** 2)))

def main():
    log = []
    log.append(f"opencv {cv2.__version__} | frame {W}x{H} | seed {SEED}")
    rng = np.random.default_rng(SEED)

    # clean frame: checker + diagonal gradient + text bars
    clean = np.zeros((H, W), np.uint8)
    for y in range(0, H, 20):
        for x in range(0, W, 20):
            clean[y:y+20, x:x+20] = 200 if ((x + y) // 20) % 2 else 60
    yy, xx = np.mgrid[0:H, 0:W]
    clean = np.clip(clean.astype(np.int16) + (xx + yy) // 6 - 40, 0, 255).astype(np.uint8)
    cv2.putText(clean, "W48 RESTORE", (90, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
    cv2.imwrite(os.path.join(PROOFS, "clean.png"), clean)

    # 1) denoise test
    noisy = np.clip(clean.astype(np.int16) + rng.normal(0, 25, (H, W)), 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(PROOFS, "noisy.png"), noisy)
    denoised = cv2.fastNlMeansDenoising(noisy, None, h=18,
                                        templateWindowSize=7, searchWindowSize=21)
    cv2.imwrite(os.path.join(PROOFS, "denoised.png"), denoised)
    r_noisy = rmse(noisy, clean)
    r_den = rmse(denoised, clean)
    log.append(f"denoise: RMSE noisy={r_noisy:.2f} denoised={r_den:.2f} "
               f"(gate: denoised < noisy*0.9)")
    assert r_den < r_noisy * 0.9, f"denoise failed: {r_den} >= {r_noisy * 0.9}"

    # 2) scratch inpaint test
    scratched = clean.copy()
    mask = np.zeros((H, W), np.uint8)
    mask[88:92, :] = 255          # horizontal film scratch
    mask[:, 200:202] = 255        # vertical scratch
    scratched[mask > 0] = 0
    cv2.imwrite(os.path.join(PROOFS, "scratched.png"), scratched)
    inpainted = cv2.inpaint(scratched, mask, 3, cv2.INPAINT_TELEA)
    cv2.imwrite(os.path.join(PROOFS, "inpainted.png"), inpainted)
    r_scr = rmse(scratched, clean, mask)
    r_inp = rmse(inpainted, clean, mask)
    log.append(f"inpaint: RMSE scratched={r_scr:.2f} inpainted={r_inp:.2f} "
               f"(gate: inpainted < scratched)")
    assert r_inp < r_scr, f"inpaint failed: {r_inp} >= {r_scr}"

    files = sorted(f for f in os.listdir(PROOFS) if f.endswith(".png"))
    with open(os.path.join(PROOFS, "SHA256SUMS"), "w") as fh:
        fh.write("\n".join(f"{sha256(os.path.join(PROOFS, f))}  {f}" for f in files) + "\n")
    with open(os.path.join(PROOFS, "log.txt"), "w") as fh:
        fh.write("\n".join(log) + "\n")
    print("\n".join(log))
    print("WIRE opencv-restore OK: denoise + scratch-inpaint gates passed")

if __name__ == "__main__":
    sys.exit(main())
