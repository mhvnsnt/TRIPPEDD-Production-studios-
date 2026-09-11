#!/usr/bin/env python3
"""Deterministic frame builder for the In the Bushes EP01 origin opening.

The scene JSON and motion-block JSON are the timing source of truth. This
builder deliberately keeps animation dependency-light: Python composes SVG
layers, a local SVG rasterizer creates frames, and FFmpeg creates delivery
video. It supports the alley/police cold open without turning camera zoom into
the primary motion language.
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
    "alley": ASSETS / "ep01-opening-alley.svg",
    "teens": ASSETS / "teens/teen-group-origin-states.svg",
    "beer": ASSETS / "props/generic-beer-throw-kit.svg",
    "police_fx": ASSETS / "fx/police-light-sweep.svg",
    "busch_wake": ASSETS / "busch/busch-wake.svg",
    "busch_look": ASSETS / "busch/busch-look-away.svg",
    "busch_reaction": ASSETS / "busch/busch-reaction.svg",
    "title": ASSETS / "ep01-opening-title.svg",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def data_uri(path: Path) -> str:
    raw = base64.b64encode(path.read_bytes()).decode("ascii")
    return "data:image/svg+xml;base64," + raw


def ease(t: float, name: str) -> float:
    t = max(0.0, min(1.0, t))
    if name == "easeInCubic":
        return t**3
    if name == "easeOutCubic":
        return 1 - (1 - t) ** 3
    if name == "easeInOutCubic":
        return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2
    if name == "easeIn":
        return t * t
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
    return 0.0 if end == start else (frame - start) / (end - start)


def keyframe_value(block, frame, key, default=None):
    keys = block.get("keyframes", [])
    if not keys:
        return default
    if frame <= keys[0]["frame"]:
        return keys[0].get(key, default)
    if frame >= keys[-1]["frame"]:
        return keys[-1].get(key, default)
    for left, right in zip(keys, keys[1:]):
        if left["frame"] <= frame <= right["frame"]:
            if key not in left or key not in right:
                return left.get(key, default)
            t = (frame - left["frame"]) / (right["frame"] - left["frame"])
            a, b = left[key], right[key]
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return lerp(a, b, t)
            return a if t < 0.5 else b
    return default


def motion_transform(block, frame):
    t = block_at(block, frame)
    if t is None:
        return ""
    e = ease(t, block.get("easing", "linear"))
    name = block["id"]
    if name == "teen_run_out":
        pts = block["path"]["points"]
        u = e * (len(pts) - 1)
        i = min(len(pts) - 2, int(u))
        lt = u - i
        x, y = lerp(pts[i][0], pts[i + 1][0], lt), lerp(pts[i][1], pts[i + 1][1], lt)
        r = lerp(block["rotation"][0], block["rotation"][1], e)
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-1180 -650)"
    if name == "run_out_of_alley":
        p0, p1, p2 = block["path"]["p0"], block["path"]["p1"], block["path"]["p2"]
        x = (1-e)**2*p0[0] + 2*(1-e)*e*p1[0] + e**2*p2[0]
        y = (1-e)**2*p0[1] + 2*(1-e)*e*p1[1] + e**2*p2[1]
        r = lerp(block["rotation"][0], block["rotation"][1], e)
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-1180 -650)"
    if name == "throw_arc_spin":
        p0, p1, p2 = block["path"]["p0"], block["path"]["p1"], block["path"]["p2"]
        x = (1-e)**2*p0[0] + 2*(1-e)*e*p1[0] + e**2*p2[0]
        y = (1-e)**2*p0[1] + 2*(1-e)*e*p1[1] + e**2*p2[1]
        r = lerp(block["rotation"][0], block["rotation"][1], e)
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-1350 -560)"
    if name == "can_bounce":
        pts, rotations = block["path"]["points"], block["rotation"]
        u = e * (len(pts) - 1)
        i = min(len(pts) - 2, int(u))
        lt = u - i
        x, y = lerp(pts[i][0], pts[i + 1][0], lt), lerp(pts[i][1], pts[i + 1][1], lt)
        r = lerp(rotations[i], rotations[i + 1], lt)
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-1550 -570)"
    if name == "liquid_spill":
        p0, p1 = block["path"]["p0"], block["path"]["p1"]
        x, y = lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e)
        s = lerp(block["scale"][0], block["scale"][1], e)
        return f"translate({x:.2f} {y:.2f}) scale({s:.3f}) translate(-1650 -580)"
    if name == "busch_wake_rise":
        y = lerp(-block["position"][1], 0, e)
        s = lerp(block["scale"][0], block["scale"][1], e)
        return f"translate(0 {y:.2f}) scale({s:.3f})"
    return ""


def image(path: Path, transform="", opacity=1.0):
    href = data_uri(path)
    return (f'<image href="{href}" x="0" y="0" width="1920" height="1080" '
            f'preserveAspectRatio="none" opacity="{opacity:.4f}" transform="{escape(transform)}"/>')


def scene_shot(scene, frame):
    for shot in scene["shots"]:
        if shot["start"] <= frame < shot["start"] + shot["duration"]:
            return shot
    raise ValueError(f"No shot for frame {frame}")


def find_block(blocks, block_id, frame):
    for block in blocks:
        if block["id"] == block_id and block_at(block, frame) is not None:
            return block
    return None


def teen_layer(blocks, frame, shot_id):
    ids = {"S01": ["teen_hang_out"], "S02": ["teen_notice"], "S03": ["teen_panic", "grab_beer"],
           "S04": ["teen_run_out", "duck_hide", "peek_back"], "S05": ["catch_breath", "beer_realize"],
           "S06": ["question_pose", "group_glance_bush"], "S07": ["point_bush"],
           "S08": ["run_out_of_alley"], "S09": ["teen_flee"]}.get(shot_id, [])
    active = next((find_block(blocks, mid, frame) for mid in ids if find_block(blocks, mid, frame)), None)
    tr = motion_transform(active, frame) if active else ""
    return image(ASSET_MAP["teens"], tr) if active else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", default=str(SCENE))
    ap.add_argument("--motion", default=str(MOTION))
    ap.add_argument("--render-plan", default=str(RENDER))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--keep-svg", action="store_true")
    args = ap.parse_args()

    scene, motion = load(Path(args.scene)), load(Path(args.motion))
    _ = load(Path(args.render_plan))
    frames, fps = int(scene["totalFrames"]), int(scene["fps"])
    width, height = 1920, 1080
    out = Path(args.out)
    svg_dir, png_dir = out / "svg", out / "png"
    svg_dir.mkdir(parents=True, exist_ok=True); png_dir.mkdir(parents=True, exist_ok=True)
    raster = shutil.which("rsvg-convert") or shutil.which("magick") or shutil.which("convert")
    ffmpeg = shutil.which("ffmpeg")
    if not raster or not ffmpeg:
        raise SystemExit("Missing renderer: rsvg-convert/ImageMagick and FFmpeg are required.")

    blocks = motion["blocks"]
    for frame in range(frames):
        shot = scene_shot(scene, frame)
        layers = [image(ASSET_MAP["title"] if shot["id"] == "S13" and frame >= 864 else ASSET_MAP["alley"])]
        if shot["id"] != "S13":
            teens = teen_layer(blocks, frame, shot["id"])
            if teens: layers.append(teens)
        if shot["id"] in {"S01", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S11"}:
            beer_ids = {"S01":"can_handoff", "S03":"grab_beer", "S05":"can_rattle", "S08":"throw_arc_spin", "S09":"liquid_drip_loop", "S11":"look_down_cans"}
            bid = beer_ids.get(shot["id"])
            if bid:
                b = find_block(blocks, bid, frame)
                if b:
                    layers.append(image(ASSET_MAP["beer"], motion_transform(b, frame), 0.92))
        pfx = find_block(blocks, "police_light_sweep", frame)
        if pfx and shot["id"] in {"S02", "S03", "S04"}:
            x = keyframe_value(pfx, frame, "x", 0); opacity = keyframe_value(pfx, frame, "opacity", 0)
            layers.append(image(ASSET_MAP["police_fx"], f"translate({x:.2f} 0)", opacity))
        hr = find_block(blocks, "headlight_rise", frame)
        if hr and shot["id"] == "S02":
            t = block_at(hr, frame); op = lerp(hr["opacity"][0], hr["opacity"][1], ease(t, "easeIn")); sc = lerp(hr["scale"][0], hr["scale"][1], ease(t, "easeOutCubic"))
            layers.append(f'<ellipse cx="960" cy="690" rx="420" ry="180" fill="#dfe8ff" opacity="{op:.3f}" transform="scale({sc:.3f} 1)"/>')
        if shot["id"] == "S09":
            tw = find_block(blocks, "foliage_twitch", frame); sh = find_block(blocks, "foliage_shudder", frame); ep = find_block(blocks, "energy_pulse", frame)
            if tw:
                r = keyframe_value(tw, frame, "rotation", 0); layers.append(f'<g transform="rotate({r:.2f} 1580 760)"><circle cx="1580" cy="760" r="245" fill="none" stroke="#c8e6b8" stroke-width="10" opacity=".35"/></g>')
            if sh:
                s = keyframe_value(sh, frame, "scale", 1); layers.append(f'<circle cx="1580" cy="760" r="255" fill="none" stroke="#9ac48b" stroke-width="8" opacity=".25" transform="translate(1580 760) scale({s:.4f}) translate(-1580 -760)"/>')
            if ep:
                op = keyframe_value(ep, frame, "opacity", 0); layers.append(f'<circle cx="1580" cy="760" r="280" fill="none" stroke="#e8f6d5" stroke-width="18" opacity="{op:.3f}"/>')
        if shot["id"] in {"S10", "S11"}:
            b = find_block(blocks, "busch_wake_rise", frame)
            layers.append(image(ASSET_MAP["busch_wake"], motion_transform(b, frame) if b else ""))
        if shot["id"] == "S12": layers.append(image(ASSET_MAP["busch_look"]))
        if shot["id"] == "S13" and frame < 864: layers.append(image(ASSET_MAP["busch_reaction"]))

        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
               f'<title>In the Bushes EP01 origin frame {frame:04d}</title>{"".join(layers)}</svg>')
        svg_path = svg_dir / f"frame-{frame:04d}.svg"; svg_path.write_text(svg, encoding="utf-8")
        png_path = png_dir / f"frame-{frame:04d}.png"
        if raster.endswith("rsvg-convert"):
            cmd = [raster, "-w", str(720 if args.preview else width), "-h", str(405 if args.preview else height), "-o", str(png_path), str(svg_path)]
        else:
            cmd = [raster, "-background", "none", str(svg_path), str(png_path)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    output = out / ("preview_720p24.mp4" if args.preview else "master_1080p24.mp4")
    scale = "720:405" if args.preview else "1920:1080"
    subprocess.run([ffmpeg, "-y", "-framerate", str(fps), "-i", str(png_dir / "frame-%04d.png"), "-vf", f"scale={scale}:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)], check=True)
    print(output)
    if not args.keep_svg: shutil.rmtree(svg_dir)


if __name__ == "__main__": main()
