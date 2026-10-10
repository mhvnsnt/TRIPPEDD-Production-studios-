#!/usr/bin/env python3
"""Wire: moviepy (MIT) video transcode helper — wave48 lane-b.

Reproduce:  python3 tools/wave48_lane_b/wire_moviepy_video.py
Exit nonzero on any gate failure.

Pipeline (all real bytes):
  1. Generate 24 deterministic 320x180 PNG frames (gradient + moving square).
  2. moviepy ImageSequenceClip @12fps -> 2.0s clip, write MP4 (libx264, crf 18).
  3. Re-open MP4 with moviepy, assert duration/fps/frame-count match source.
  4. Extract middle frame as PNG; byte-diff vs source frame (mean abs diff < 8).
  5. Write SHA256SUMS + log.
"""
import hashlib, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(ROOT, "proofs_moviepy")
FRAMES = os.path.join(PROOFS, "frames")
os.makedirs(FRAMES, exist_ok=True)

from PIL import Image, ImageDraw
import numpy as np
from moviepy import ImageSequenceClip, VideoFileClip

N, W, H, FPS = 24, 320, 180, 12

def gen_frames():
    paths = []
    for i in range(N):
        img = Image.new("RGB", (W, H))
        px = img.load()
        for y in range(H):
            for x in range(W):
                px[x, y] = (x * 255 // W, y * 255 // H, (x + y + i * 8) % 256)
        d = ImageDraw.Draw(img)
        sx = (i * 12) % (W - 40)
        d.rectangle([sx, 70, sx + 40, 110], fill=(255, 255, 255))
        d.text((8, 8), f"F{i:02d}", fill=(255, 255, 255))
        p = os.path.join(FRAMES, f"frame_{i:03d}.png")
        img.save(p)
        paths.append(p)
    return paths

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def main():
    log = []
    frames = sorted(os.path.join(FRAMES, f) for f in os.listdir(FRAMES) if f.endswith(".png")) \
        or gen_frames()
    assert len(frames) == N, f"expected {N} frames, got {len(frames)}"
    log.append(f"source frames: {len(frames)} PNGs {W}x{H}")

    clip = ImageSequenceClip(frames, fps=FPS)
    out_mp4 = os.path.join(PROOFS, "out.mp4")
    clip.write_videofile(out_mp4, codec="libx264", fps=FPS,
                         ffmpeg_params=["-crf", "18", "-pix_fmt", "yuv420p"],
                         logger=None)
    log.append(f"wrote {out_mp4} ({os.path.getsize(out_mp4)} bytes)")

    v = VideoFileClip(out_mp4)
    dur, fps = v.duration, v.fps
    n_dec = int(round(dur * fps))
    v.close()
    log.append(f"decoded: duration={dur:.3f}s fps={fps} frames~{n_dec}")
    assert abs(dur - N / FPS) < 0.05, f"duration drift: {dur}"
    assert n_dec == N, f"frame count mismatch: {n_dec} != {N}"

    # middle-frame pixel round-trip check (tolerant of H.264)
    mid = N // 2
    src = np.asarray(Image.open(frames[mid])).astype(np.int16)
    v = VideoFileClip(out_mp4)
    got = np.asarray(v.get_frame(mid / FPS)).astype(np.int16)
    v.close()
    got = got[:H, :W]
    mad = float(np.mean(np.abs(got - src)))
    log.append(f"middle-frame mean-abs-diff vs source: {mad:.3f} (gate < 8.0)")
    assert mad < 8.0, f"H.264 round-trip too lossy: {mad}"
    Image.fromarray(got.astype(np.uint8)).save(os.path.join(PROOFS, "frame_mid.png"))

    # sha256 manifest
    files = sorted(f for f in os.listdir(PROOFS) if f.endswith((".mp4", ".png"))) + \
            sorted(os.path.join("frames", f) for f in os.listdir(FRAMES) if f.endswith(".png"))
    sums = []
    for f in files:
        p = os.path.join(PROOFS, f)
        sums.append(f"{sha256(p)}  {f}")
    with open(os.path.join(PROOFS, "SHA256SUMS"), "w") as fh:
        fh.write("\n".join(sums) + "\n")
    with open(os.path.join(PROOFS, "log.txt"), "w") as fh:
        fh.write("\n".join(log) + "\n")
    print("\n".join(log))
    print(f"WIRE moviepy OK: {N} frames -> {os.path.basename(out_mp4)}, gates passed")

if __name__ == "__main__":
    sys.exit(main())
