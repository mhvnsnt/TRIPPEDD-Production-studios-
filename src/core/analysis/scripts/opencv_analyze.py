"""Frame-level visual analysis. Emits JSON on stdout; nothing is invented.

Samples frames at a fixed stride and reports mean luma, frame-to-frame
difference (motion proxy), and blank/near-black detection. Every number here is
computed from real decoded pixels.
"""
import sys, json
import cv2
import numpy as np

path = sys.argv[1]
max_samples = int(sys.argv[2]) if len(sys.argv) > 2 else 240

cap = cv2.VideoCapture(path)
if not cap.isOpened():
    print(json.dumps({"error": "could not open video"}))
    sys.exit(2)

fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
stride = max(1, total // max_samples) if total > 0 else 15

samples, prev = [], None
idx = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    if idx % stride == 0:
        g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(g, (64, 36))
        luma = float(np.mean(small))
        diff = float(np.mean(cv2.absdiff(small, prev))) if prev is not None else 0.0
        prev = small
        samples.append({
            "frame": idx,
            "t": (idx / fps) if fps > 0 else None,
            "luma": round(luma, 2),
            "motion": round(diff, 2),
            "blank": bool(luma < 8.0),
        })
    idx += 1
cap.release()

motions = [s["motion"] for s in samples[1:]]
print(json.dumps({
    "fps": fps, "frameCount": total, "sampled": len(samples), "stride": stride,
    "samples": samples,
    "motionMean": round(float(np.mean(motions)), 3) if motions else None,
    "motionMax": round(float(np.max(motions)), 3) if motions else None,
    "blankFrames": [s["frame"] for s in samples if s["blank"]],
}))
