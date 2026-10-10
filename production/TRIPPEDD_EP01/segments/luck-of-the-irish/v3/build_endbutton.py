#!/usr/bin/env python3
"""LOTI v3 end-button: Porky-style rings + mascot pop-up + stuttered line.
Builds the [52.5, 56.533) replacement segment (121 frames @30fps = 4.0333s).
"""
import math, subprocess, os
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1920, 1080, 30
NFRAMES = 121  # 4.0333s
D = os.path.expanduser("~/workspace/trippedd-studio-loti-v2/production/TRIPPEDD_EP01/segments/luck-of-the-irish/v3")
OUT = "/tmp/endbutton"

# ---------- 1. rings plate (drawn, not lifted) ----------
def rings_plate():
    img = Image.new("RGB", (W, H), (16, 12, 12))
    dr = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    RED, GOLD = (184, 40, 28), (232, 164, 32)
    # filled circles largest->smallest: alternating red/gold bullseye
    for r, col in [(780, RED), (695, GOLD), (610, RED), (525, GOLD),
                   (440, RED), (355, GOLD), (270, RED), (185, GOLD), (110, RED)]:
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    return img.convert("RGBA")

# ---------- 2. sticker mascot from raw cutout + white die-cut border ----------
def sticker():
    raw = Image.open(f"{D}/fx/sticker/mascot-cutout-raw.png").convert("RGBA")
    assert raw.size == (W, H), raw.size
    alpha = raw.split()[3]
    border = alpha.filter(ImageFilter.MaxFilter(15))  # ~7px each side
    white = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    white.putalpha(border)
    out = Image.alpha_composite(white, raw)
    return out

def ease_out_back(t):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def main():
    os.makedirs(f"{OUT}/frames", exist_ok=True)
    base = rings_plate()
    masc = sticker()
    cx, cy = W // 2, H // 2
    for f in range(NFRAMES):
        frame = base.copy()
        if f >= 118:
            frame = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        elif f >= 24:
            if f <= 38:  # pop with overshoot bounce, rising
                t = (f - 24) / 14
                s = max(ease_out_back(t), 0.001)
                dy = 160 * (1 - t) ** 2
            elif f <= 100:  # line: subtle bob + breathe
                s = 1 + 0.008 * math.sin(2 * math.pi * (f - 39) / 48)
                dy = 10 * math.sin(2 * math.pi * (f - 39) / 24)
            else:  # hold
                s, dy = 1.0, 0.0
            nw, nh = int(W * s), int(H * s)
            m = masc.resize((nw, nh), Image.LANCZOS)
            frame.alpha_composite(m, (int(cx - nw / 2), int(cy - nh / 2 + dy)))
        frame.convert("RGB").save(f"{OUT}/frames/f{f:04d}.png")
    print(f"wrote {NFRAMES} frames")

    # encode video segment
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS),
                    "-i", f"{OUT}/frames/f%04d.png",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-preset", "medium", "-r", str(FPS),
                    f"{OUT}/endseg_v.mp4"], check=True)
    # audio: silence 1.3s + line (peak-normalized to -1.5dB) + pad to 4.0333s
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/endbutton/line.mp3",
                    "-af", "volume=0.891,aresample=48000,adelay=1300|1300,apad=whole_dur=4.0333",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                    f"{OUT}/endseg_a.m4a"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/endseg_v.mp4",
                    "-i", f"{OUT}/endseg_a.m4a", "-c:v", "copy", "-c:a", "copy",
                    "-shortest", f"{OUT}/endseg.mp4"], check=True)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", f"{OUT}/endseg.mp4"], capture_output=True, text=True)
    print("endseg duration:", d.stdout.strip())

if __name__ == "__main__":
    main()
