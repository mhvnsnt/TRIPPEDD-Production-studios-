#!/usr/bin/env python3
"""frame_interp/interpolate.py — deterministic frame-interpolation proof harness.

Wired tool: ffmpeg minterpolate (mi_mode=mci, motion-compensated).
RIFE was attempted and is documented as DEFERRED in FAILURES.md:
  - rife-ncnn-vulkan release download timed out in this sandbox (curl exit 28)
  - no Vulkan-capable GPU present, so the ncnn Vulkan build could not run here

Pipeline:
  1. Synthesize 4 input keyframes (PIL): black field, white square moving
     left->right across known positions. Reproducible: same bytes every run.
  2. Encode as 4-frame MP4 at 4 fps (lossless x264).
  3. Interpolate with ffmpeg minterpolate (fps=30, mi_mode=mci,
     mc_mode=aobmc, me_mode=bidir): 4 -> 16 frames.
  4. Extract all output frames as PNG; verify count, readability, and that the
     square centroid moves monotonically along the keyframe path.
Writes proofs/PROOFS.md with SHA-256 of inputs and outputs.
"""
import hashlib, json, os, subprocess, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs")
W, H = 320, 180
SQ = 40
N_IN, FPS_OUT, N_OUT = 4, 30, 16
X0, X1, Y = 120, 240, 60

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAILED:", " ".join(cmd), file=sys.stderr)
        print(r.stderr[-2000:], file=sys.stderr)
        sys.exit(2)
    return r

def _sprite():
    # deterministic textured sprite: seeded per-pixel noise + edge border,
    # so motion estimation has texture to lock onto (pure flat blocks break ME)
    import random
    rng = random.Random(1234)
    sp = Image.new("RGB", (SQ, SQ))
    px = sp.load()
    for yy in range(SQ):
        for xx in range(SQ):
            v = rng.randrange(60, 256)
            px[xx, yy] = (v, v // 2 + 60, 255 - v // 3)
    ImageDraw.Draw(sp).rectangle([0, 0, SQ - 1, SQ - 1], outline=(255, 255, 0), width=3)
    return sp

_SPRITE = _sprite()

def make_frame(x, path):
    im = Image.new("RGB", (W, H), (8, 12, 20))
    im.paste(_SPRITE, (x, Y))
    im.save(path)

def centroid(path):
    im = Image.open(path).convert("L")
    px = im.load()
    xs = [x for yy in range(H) for x in range(W) if px[x, yy] > 100]
    assert xs, f"no bright pixels in {path}"
    return sum(xs) / len(xs)

def main():
    os.makedirs(PROOFS, exist_ok=True)
    keys = [round(X0 + (X1 - X0) * i / (N_IN - 1)) for i in range(N_IN)]
    inputs = []
    for i, x in enumerate(keys, 1):
        p = os.path.join(PROOFS, f"keyframe_{i}.png")
        make_frame(x, p); inputs.append(p)
    kcen = [centroid(p) for p in inputs]
    assert all(abs(c - (x + SQ / 2)) < 1.0 for c, x in zip(kcen, keys)), "keyframe sanity failed"
    in_mp4 = os.path.join(PROOFS, "input_keys.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-framerate", "4", "-i",
         os.path.join(PROOFS, "keyframe_%d.png"),
         "-c:v", "libx264", "-crf", "0", "-pix_fmt", "yuv420p", in_mp4])
    out_mp4 = os.path.join(PROOFS, "interpolated.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", in_mp4, "-vf",
         f"minterpolate=fps={FPS_OUT}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:me=umh:search_param=32:vsbmc=1",
         "-c:v", "libx264", "-crf", "0", "-pix_fmt", "yuv420p", out_mp4])
    run(["ffmpeg", "-y", "-v", "error", "-i", out_mp4,
         os.path.join(PROOFS, "out_%02d.png")])
    frames = sorted(p for p in os.listdir(PROOFS)
                    if p.startswith("out_") and p.endswith(".png"))
    cents = [centroid(os.path.join(PROOFS, f)) for f in frames]
    # reopen check: every PNG must decode and have the expected size
    for f in frames:
        im = Image.open(os.path.join(PROOFS, f)); im.load()
        assert im.size == (W, H), f"size mismatch {f}"
    n = len(frames)
    mono = all(cents[i] <= cents[i + 1] + 2.0 for i in range(n - 1))
    lo, hi = keys[0] + SQ / 2 - 3.0, keys[-1] + SQ / 2 + 3.0
    onpath = all(lo <= c <= hi for c in cents)
    travel = max(cents) - min(cents)
    evidence = {
        "tool": "ffmpeg minterpolate (fps=30, mi_mode=mci, mc_mode=aobmc, me_mode=bidir)",
        "input_keyframes": N_IN, "output_frames": n, "expected_output_frames": N_OUT,
        "count_ok": n == N_OUT,
        "centroid_x": [round(c, 2) for c in cents],
        "monotonic_x": bool(mono), "on_motion_path": bool(onpath),
        "travel_span_px": round(travel, 2),
        "travel_ok": bool(travel > (keys[-1] - keys[0]) * 0.5),
    }
    artifacts = {"input_keys.mp4": in_mp4, "interpolated.mp4": out_mp4}
    for i, p in enumerate(inputs, 1):
        artifacts[f"keyframe_{i}.png"] = p
    for f in frames:
        artifacts[f] = os.path.join(PROOFS, f)
    hashes = {k: sha256(v) for k, v in sorted(artifacts.items())}
    lines = ["# PROOFS — frame_interp (ffmpeg minterpolate)", "",
             "## Verification", "```json", json.dumps(evidence, indent=2), "```",
             "", "## SHA-256", ""]
    for k, v in hashes.items():
        lines.append(f"- `{k}`: `{v}`")
    open(os.path.join(PROOFS, "PROOFS.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps(evidence, indent=2))
    ok = evidence["count_ok"] and mono and onpath and evidence["travel_ok"]
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
