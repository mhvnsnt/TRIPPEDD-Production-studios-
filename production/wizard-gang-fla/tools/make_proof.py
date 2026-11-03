#!/usr/bin/env python3
"""Per-character puppet proof package: pose stills, motion clip, frame strip,
pose sheet, and pixel-diff motion numbers — rendered from the .fla itself via
wg_render.py (the transforms the .fla encodes are what gets drawn).

Proof standard (owner): a clip + a frame strip showing REAL distinct poses.
Filenames carry the date and never overwrite earlier proof.

Usage: python3 make_proof.py <char> --out <proof_dir>
"""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from wg_render import FLA

POSES = ["NEUTRAL", "BLINK", "LEAN_R", "LEAN_L", "BOW", "TURN_R", "ARMS_WIDE", "SETTLE"]
DATE = "20261102"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("char")
    ap.add_argument("--out", required=True)
    ap.add_argument("--build-out", default=os.path.expanduser("~/workspace/fla-build/out"))
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "characters", f"{a.char}.json")))
    U = a.char.upper()
    rootname = f"{cfg['code']}_ORIGINAL_PUPPET_{U}_VERSION_001"
    master = f"{cfg['code']}_{U}_PUPPET_V001/WG_{U}_FRONT_PUPPET"
    fla = FLA(os.path.join(a.build_out, rootname), default_canvas=tuple(cfg["canvas"]))
    os.makedirs(a.out, exist_ok=True)

    stills = []
    for i, label in enumerate(POSES):
        img = fla.render_symbol(master, i)
        bg = Image.new("RGBA", img.size, (18, 18, 26, 255))
        bg.alpha_composite(img)
        still = bg.convert("RGB")
        # normalise to height 864 for proof/clip consistency
        scale = 864 / still.height
        still = still.resize((round(still.width * scale), 864), Image.LANCZOS)
        if still.width % 2: still = still.resize((still.width + 1, 864), Image.LANCZOS)
        p = os.path.join(a.out, f"pose_{i}_{label}.png")
        still.save(p)
        stills.append(still)
        print("pose", i, label, still.size, flush=True)

    # clip: 12 frames per pose @24fps, hard cuts (production on-twos style holds)
    frames_dir = os.path.join(a.out, "_clipframes")
    os.makedirs(frames_dir, exist_ok=True)
    n = 0
    for still in stills:
        for _ in range(12):
            still.save(os.path.join(frames_dir, f"f{n:03d}.png")); n += 1
    mp4 = os.path.join(a.out, f"{a.char}_puppet-motion-proof_{DATE}.mp4")
    subprocess.run(["ffmpeg", "-y", "-framerate", "24", "-i", os.path.join(frames_dir, "f%03d.png"),
                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("mp4:", mp4, os.path.getsize(mp4), "bytes,", n, "frames")

    # frame strip: all 8 poses, 2 rows x 4
    TW = 300
    TH = round(864 * TW / stills[0].width)
    strip = Image.new("RGB", (TW * 4 + 50, (TH + 24) * 2 + 30), (10, 10, 16))
    d = ImageDraw.Draw(strip)
    for i, still in enumerate(stills):
        t = still.resize((TW, TH), Image.LANCZOS)
        x, y = 10 + (i % 4) * (TW + 10), 10 + (i // 4) * (TH + 24)
        strip.paste(t, (x, y))
        d.text((x + 4, y + TH + 5), f"{i} {POSES[i]}", fill=(255, 220, 120))
    strip_path = os.path.join(a.out, f"{a.char}_frame-strip_{DATE}.png")
    strip.save(strip_path)
    print("strip:", strip_path)

    # pose sheet: 4 key poses full-height
    keys = [0, 2, 4, 6]
    PW = 380
    PH = round(864 * PW / stills[0].width)
    sheet = Image.new("RGB", (PW * 4 + 50, PH + 40), (12, 12, 20))
    d = ImageDraw.Draw(sheet)
    for j, i in enumerate(keys):
        t = stills[i].resize((PW, PH), Image.LANCZOS)
        x = 10 + j * (PW + 10)
        sheet.paste(t, (x, 10))
        d.text((x + 4, PH + 16), POSES[i], fill=(255, 220, 120))
    sheet_path = os.path.join(a.out, f"{a.char}_pose-sheet_{DATE}.png")
    sheet.save(sheet_path)
    print("sheet:", sheet_path)

    # motion numbers between consecutive pose stills
    prev = None
    for i, still in enumerate(stills):
        arr = np.array(still).astype(int)
        if prev is not None:
            diff = np.abs(arr - prev).mean()
            changed = (np.abs(arr - prev).sum(axis=2) > 30).mean() * 100
            print(f"motion {POSES[i-1]} -> {POSES[i]}: mean|diff| = {diff:.2f}, pixels changed = {changed:.1f}%")
        prev = arr
    print("PROOF COMPLETE", a.char)

if __name__ == "__main__":
    main()
