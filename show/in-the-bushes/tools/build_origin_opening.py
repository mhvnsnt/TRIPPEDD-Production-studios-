#!/usr/bin/env python3
"""Build a deterministic SVG-frame preview for In the Bushes EP01 origin opening.

Python stdlib creates frame SVGs; a local SVG rasterizer (rsvg-convert or
ImageMagick) and FFmpeg produce the video. Scene and motion JSON are the timing
source of truth.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import shutil
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[3]
SCENE = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.scene.json"
MOTION = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.motion-blocks.json"
RENDER = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.render-plan.json"
ASSETS = ROOT / "show/in-the-bushes/assets"
OUT = ROOT / "show/in-the-bushes/build/origin-opening-v2"

ASSET_MAP = {
    "env_night_bush": ASSETS / "ep01-opening-night.svg",
    "teen-group-run-hide.svg": ASSETS / "teens/teen-group-run-hide.svg",
    "generic-beer-throw-kit.svg": ASSETS / "props/generic-beer-throw-kit.svg",
    "busch-wake.svg": ASSETS / "busch/busch-wake.svg",
    "busch-look-away.svg": ASSETS / "busch/busch-look-away.svg",
    "busch-reaction.svg": ASSETS / "busch/busch-reaction.svg",
    "ep01-opening-title.svg": ASSETS / "ep01-opening-title.svg",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def data_uri(path: Path) -> str:
    raw = base64.b64encode(path.read_bytes()).decode("ascii")
    return "data:image/svg+xml;base64," + raw


def ease(t: float, name: str) -> float:
    t = max(0.0, min(1.0, t))
    if name == "easeOutCubic":
        return 1 - (1 - t) ** 3
    if name == "easeIn":
        return t * t
    if name == "easeInOutCubic":
        return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2
    if name == "easeOutBack":
        c1, c3 = 1.70158, 2.70158
        return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
    return t


def lerp(a, b, t):
    return a + (b - a) * t


def block_at(block, frame):
    start, end = block["frames"]
    if frame < start or frame > end:
        return None
    return 0 if end == start else (frame - start) / (end - start)


def motion_transform(motion, frame):
    t = block_at(motion, frame)
    if t is None:
        return ""
    e = ease(t, motion.get("easing", "linear"))
    name = motion["id"]
    if name == "teen_run_stop":
        x = lerp(motion["from"]["x"], motion["to"]["x"], e)
        y = lerp(motion["from"]["y"], motion["to"]["y"], e)
        r = lerp(motion["from"]["rotation"], motion["to"]["rotation"], e)
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-510 -650)"
    if name == "throw_arc_spin":
        p0, p1, p2 = motion["path"]["p0"], motion["path"]["p1"], motion["path"]["p2"]
        x = (1-e)**2*p0[0] + 2*(1-e)*e*p1[0] + e**2*p2[0]
        y = (1-e)**2*p0[1] + 2*(1-e)*e*p1[1] + e**2*p2[1]
        r = lerp(motion["rotation"][0], motion["rotation"][1], e)
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-520 -510)"
    if name == "can_bounce":
        pts = motion["path"]["points"]
        u = e * (len(pts) - 1)
        i = min(len(pts) - 2, int(u))
        lt = u - i
        x = lerp(pts[i][0], pts[i+1][0], lt)
        y = lerp(pts[i][1], pts[i+1][1], lt)
        rpts = motion["rotation"]
        r = lerp(rpts[i], rpts[i+1], lt)
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-1190 -520)"
    if name == "liquid_spill":
        p0, p1 = motion["path"]["p0"], motion["path"]["p1"]
        x, y = lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e)
        s = lerp(motion["scale"][0], motion["scale"][1], e)
        return f"translate({x:.2f} {y:.2f}) scale({s:.3f}) translate(-1350 -570)"
    if name == "busch_wake_rise":
        y = lerp(70, 0, e)
        s = lerp(motion["scale"][0], motion["scale"][1], e)
        return f"translate(0 {y:.2f}) scale({s:.3f})"
    return ""


def image(path: Path, transform="", opacity=1.0):
    href = data_uri(path)
    return (f'<image href="{href}" x="0" y="0" width="1920" height="1080" '
            f'preserveAspectRatio="none" opacity="{opacity}" transform="{escape(transform)}"/>')


def scene_shot(scene, frame):
    for shot in scene["shots"]:
        start = shot["start"]
        end = start + shot["duration"] - 1
        if start <= frame <= end:
            return shot
    raise ValueError(f"No shot for frame {frame}")


def find_block(blocks, block_id, frame):
    for block in blocks:
        if block["id"] == block_id and block_at(block, frame) is not None:
            return block
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", default=str(SCENE))
    ap.add_argument("--motion", default=str(MOTION))
    ap.add_argument("--render-plan", default=str(RENDER))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--preview", action="store_true", help="Render 720p preview instead of 1080p")
    ap.add_argument("--keep-svg", action="store_true")
    args = ap.parse_args()

    scene = load(Path(args.scene))
    motion = load(Path(args.motion))
    _render_plan = load(Path(args.render_plan))
    frames, fps = int(scene["totalFrames"]), int(scene["fps"])
    width, height = 1920, 1080
    out = Path(args.out)
    svg_dir, png_dir = out / "svg", out / "png"
    svg_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)

    raster = shutil.which("rsvg-convert") or shutil.which("magick") or shutil.which("convert")
    ffmpeg = shutil.which("ffmpeg")
    if not raster or not ffmpeg:
        raise SystemExit("Missing renderer. Install rsvg-convert (preferred) or ImageMagick, plus FFmpeg.")

    motion_blocks = motion["blocks"]
    for frame in range(frames):
        shot = scene_shot(scene, frame)
        layers = []
        if shot["id"] == "S11":
            layers.append(image(ASSET_MAP["ep01-opening-title.svg"]))
        else:
            layers.append(image(ASSET_MAP["env_night_bush"]))

        assets = shot.get("assets", [])
        if shot["id"] in {"S02", "S03", "S04"} and "teen-group-run-hide.svg" in assets:
            tr = next((motion_transform(b, frame) for b in motion_blocks if b["id"] == "teen_run_stop"), "")
            layers.append(image(ASSET_MAP["teen-group-run-hide.svg"], tr))
        if shot["id"] == "S05":
            for mid in ("throw_arc_spin", "can_bounce", "liquid_spill"):
                tr = next((motion_transform(b, frame) for b in motion_blocks if b["id"] == mid), "")
                if tr:
                    layers.append(image(ASSET_MAP["generic-beer-throw-kit.svg"], tr, 0.9))
        if shot["id"] in {"S07", "S08"}:
            tr = next((motion_transform(b, frame) for b in motion_blocks if b["id"] == "busch_wake_rise"), "")
            layers.append(image(ASSET_MAP["busch-wake.svg"], tr))
        if shot["id"] == "S09":
            layers.append(image(ASSET_MAP["busch-look-away.svg"]))
        if shot["id"] == "S10":
            layers.append(image(ASSET_MAP["busch-reaction.svg"]))

        # Keep subtle physical motion visible even where dedicated art is limited.
        twitch = find_block(motion_blocks, "foliage_twitch", frame)
        if twitch:
            t = block_at(twitch, frame)
            r = math.sin(t * math.pi * 4) * 2
            layers.append(f'<g transform="rotate({r:.2f} 1650 650)"></g>')
        shudder = find_block(motion_blocks, "foliage_shudder", frame)
        if shudder:
            t = block_at(shudder, frame)
            s = 1 + 0.025 * math.sin(t * math.pi * 5)
            layers.append(f'<g transform="translate(1650 650) scale({s:.4f}) translate(-1650 -650)"></g>')

        layer_markup = "".join(layers)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
               f'viewBox="0 0 {width} {height}"><title>In the Bushes EP01 origin opening '
               f'frame {frame:04d}</title>{layer_markup}</svg>')
        svg_path = svg_dir / f"frame-{frame:04d}.svg"
        svg_path.write_text(svg, encoding="utf-8")

        png_path = png_dir / f"frame-{frame:04d}.png"
        if raster.endswith("rsvg-convert"):
            cmd = [raster, "-w", str(720 if args.preview else width), "-h", str(405 if args.preview else height), "-o", str(png_path), str(svg_path)]
        else:
            cmd = [raster, "-background", "none", str(svg_path), str(png_path)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    output = out / ("preview_720p24.mp4" if args.preview else "master_1080p24.mp4")
    scale = "720:405" if args.preview else "1920:1080"
    subprocess.run([
        ffmpeg, "-y", "-framerate", str(fps), "-i", str(png_dir / "frame-%04d.png"),
        "-vf", f"scale={scale}:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(output)
    ], check=True)
    print(output)
    if not args.keep_svg:
        shutil.rmtree(svg_dir)


if __name__ == "__main__":
    main()
