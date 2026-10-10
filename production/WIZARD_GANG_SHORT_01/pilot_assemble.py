#!/usr/bin/env python3
"""pilot_assemble.py — Wizard Gang pilot (SHORT_01) final assembly.

Builds the ~50s pilot from the 9 animated shot videos + title cards +
the synthesized soundscape. Two deliverables: 9:16 primary, 16:9 secondary.

Video fit strategy per shot (sources have mixed aspects):
- portrait/square sources: center-crop to target aspect
- wide sources (1472x528): slow Ken Burns pan across the frame (staged, deliberate)

Title cards: PIL-rendered (same approach as tools/video_pipeline/promo_assemble.py).
Audio: audio/soundscape_50s.wav (original synthesis, zero license baggage).
Dialogue is a SEPARATE draft stem (pending owner line approval) — NOT mixed in.

Usage:
    python3 pilot_assemble.py
Output:
    wizard-gang-pilot-9x16.mp4   (1080x1920)
    wizard-gang-pilot-16x9.mp4   (1920x1080)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from moviepy import (VideoFileClip, ImageClip, CompositeVideoClip,
                     AudioFileClip, concatenate_videoclips)

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
AUDIO = os.path.join(HERE, "audio", "soundscape_50s.wav")

# (filename glob prefix, start, dur, fit) — fit: "crop" | "pan"
SHOT_LIST = [
    ("shot01-rooftop",      2.0, 5.0, "pan"),   # 0-5
    ("shot02-ashes",        2.0, 6.0, "crop"),  # 5-11
    ("shot03-onyx",         2.0, 5.0, "pan"),   # 11-16
    ("shot04-echo",         2.0, 5.0, "crop"),  # 16-21
    ("shot05-static-cipher", 2.0, 6.0, "crop"), # 21-27
    ("shot06-hollow",       2.0, 5.0, "pan"),   # 27-32
    ("shot07-sombra",       2.0, 5.0, "crop"),  # 32-37
    ("shot08a-circle-empty", 2.0, 2.5, "pan"),  # 37-39.5
    ("shot08b-circle-kiko", 2.0, 2.5, "pan"),   # 39.5-42
]
# title cards: (text, dur) — 42-50
CARDS = [("WIZARD GANG", 4.0), ("TRIPPEDD", 4.0)]

FPS = 30


def find(prefix):
    for f in sorted(os.listdir(SHOTS)):
        if f.startswith("media-generation-" + prefix) and f.endswith(".mp4"):
            return os.path.join(SHOTS, f)
    raise FileNotFoundError(prefix)


def fit_clip(clip, W, H, mode):
    """Fit clip into WxH. 'crop': center-crop. 'pan': Ken Burns lateral pan."""
    src = clip.resized(height=H) if (clip.w / clip.h) < (W / H) else clip.resized(width=int(H * clip.w / clip.h))
    # normalize: ensure coverage
    if src.w < W or src.h < H:
        scale = max(W / src.w, H / src.h)
        src = src.resized((int(src.w * scale), int(src.h * scale)))
    if mode == "crop" or src.w <= W:
        x = (src.w - W) / 2
        y = (src.h - H) / 2
        return src.cropped(x1=x, y1=y, x2=x + W, y2=y + H)
    # pan: animate x across the surplus width
    surplus = src.w - W
    y = (src.h - H) / 2
    dur = clip.duration
    base = src.with_position(lambda t: (-surplus * t / dur, -y))
    return CompositeVideoClip([base], size=(W, H)).with_duration(dur)


def _font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def title_card(W, H, text, dur):
    img = Image.new("RGB", (W, H), (5, 5, 8))
    d = ImageDraw.Draw(img)
    f = _font(int(W * 0.11))
    bb = d.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    d.text(((W - tw) / 2, H / 2 - 60), text, font=f, fill=(245, 245, 245))
    return ImageClip(np.array(img), duration=dur)


def build(W, H, out):
    clips = []
    for prefix, start, dur, mode in SHOT_LIST:
        c = VideoFileClip(find(prefix)).subclipped(start, start + dur)
        clips.append(fit_clip(c, W, H, mode))
    for text, dur in CARDS:
        clips.append(title_card(W, H, text, dur))
    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(AUDIO).subclipped(0, video.duration)
    video = video.with_audio(audio)
    video.write_videofile(out, fps=FPS, codec="libx264",
                          audio_codec="aac", preset="medium")
    print(f"WROTE {out}  {video.duration:.1f}s @ {W}x{H}")


if __name__ == "__main__":
    build(1080, 1920, os.path.join(HERE, "wizard-gang-pilot-9x16.mp4"))
    build(1920, 1080, os.path.join(HERE, "wizard-gang-pilot-16x9.mp4"))
