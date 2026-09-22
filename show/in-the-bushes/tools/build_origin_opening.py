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
import importlib.util
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
RIG_PATH = ROOT / "show/in-the-bushes/tools/teen_performance.py"

ASSET_MAP = {
    "alley": ASSETS / "ep01-opening-alley.svg",
    "teens": ASSETS / "teens/teen-character-design-v1.svg",
    "beer_pack": ASSETS / "props/generic-six-pack.svg",
    "beer_can": ASSETS / "props/generic-can.svg",
    "beer_spill": ASSETS / "props/generic-beer-spill.svg",
    "busch_transform": ASSETS / "busch/busch-transform.svg",
    "police_fx": ASSETS / "fx/police-light-sweep.svg",
    "busch_wake": ASSETS / "busch/busch-wake.svg",
    "busch_look": ASSETS / "busch/busch-look-away.svg",
    "busch_reaction": ASSETS / "busch/busch-reaction.svg",
    "title": ASSETS / "ep01-opening-title.svg",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_teen_performance():
    spec = importlib.util.spec_from_file_location("in_the_bushes_teen_performance", RIG_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load procedural teen rig: {RIG_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.performance_layer


PERFORMANCE_LAYER = load_teen_performance()


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
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-200 -150)"
    if name == "can_bounce":
        pts, rotations = block["path"]["points"], block["rotation"]
        u = e * (len(pts) - 1)
        i = min(len(pts) - 2, int(u))
        lt = u - i
        x, y = lerp(pts[i][0], pts[i + 1][0], lt), lerp(pts[i][1], pts[i + 1][1], lt)
        r = lerp(rotations[i], rotations[i + 1], lt)
        return f"translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate(-70 -130)"
    if name == "liquid_spill":
        p0, p1 = block["path"]["p0"], block["path"]["p1"]
        x, y = lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e)
        s = lerp(block["scale"][0], block["scale"][1], e)
        return f"translate({x:.2f} {y:.2f}) scale({s:.3f}) translate(-130 -150)"
    if name == "busch_wake_rise":
        y = lerp(-block["position"][1], 0, e)
        s = lerp(block["scale"][0], block["scale"][1], e)
        # The Busch asset is placed at x=1280,y=460 in a 560x560 box. Apply
        # rise/scale around that box's center so the bush grows in place
        # instead of drifting toward the SVG origin as it wakes.
        cx, cy = 1560, 740
        return (f"translate({cx} {cy}) translate(0 {y:.2f}) scale({s:.3f}) "
                f"translate(-{cx} -{cy})")
    return ""


def image(path: Path, transform="", opacity=1.0, x=0, y=0, width=1920, height=1080, preserve="none"):
    href = data_uri(path)
    return (f'<image href="{href}" x="{x}" y="{y}" width="{width}" height="{height}" '
            f'preserveAspectRatio="{preserve}" opacity="{opacity:.4f}" transform="{escape(transform)}"/>')


def busch_image(path: Path, transform="", opacity=1.0):
    # Busch artwork is authored in a square 800x800 canvas. Never stretch it
    # to the 16:9 delivery frame; keep the character's silhouette intact at
    # the alley exit where the transformation happens.
    return image(path, transform, opacity, x=1280, y=460, width=560, height=560, preserve="xMidYMid meet")


def bush_transform_image(path: Path, transform="", opacity=1.0):
    """Render the foliage-only transformation state over the existing bush."""
    return image(path, transform, opacity, x=1280, y=460, width=560, height=560, preserve="xMidYMid meet")


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
    # The base builder uses the same richer procedural rig as the dedicated
    # character builder. Keeping this here prevents accidental fallback to
    # the obsolete stick-figure sheet when this script is invoked directly.
    active_shots = {"S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09"}
    if shot_id not in active_shots:
        return ""
    return PERFORMANCE_LAYER(frame, shot_id)


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
            beer_ids = {"S01":"can_handoff", "S03":"grab_beer", "S05":"can_rattle", "S08":"throw_arc_spin", "S09":"liquid_spill", "S11":"look_down_cans"}
            bid = beer_ids.get(shot["id"])
            if bid:
                b = find_block(blocks, bid, frame)
                if b:
                    prop_asset = ASSET_MAP["beer_can"] if bid in {"can_rattle","look_down_cans"} else ASSET_MAP["beer_pack"]
                    if bid == "liquid_spill":
                        prop_asset = ASSET_MAP["beer_spill"]
                    layers.append(image(prop_asset, motion_transform(b, frame), 0.92))
            # Keep authored physical follow-through visible: bounce and spill
            # are separate passes so the throw does not end abruptly.
            if shot["id"] == "S08":
                bounce = find_block(blocks, "can_bounce", frame)
                if bounce:
                    layers.append(image(ASSET_MAP["beer_can"], motion_transform(bounce, frame), 0.72))
            if shot["id"] == "S09":
            tw = find_block(blocks, "foliage_twitch", frame)
            sh = find_block(blocks, "foliage_shudder", frame)
            ep = find_block(blocks, "energy_pulse", frame)
            # The bush is the animated subject. Beer remains an ordinary prop.
            if tw:
                r = keyframe_value(tw, frame, "rotation", 0)
                layers.append(bush_transform_image(ASSET_MAP["busch_transform"], f"rotate({r:.2f} 1560 740)", 0.72))
            if sh:
                scale = keyframe_value(sh, frame, "scale", 1)
                layers.append(bush_transform_image(ASSET_MAP["busch_transform"], f"translate(1560 740) scale({scale:.4f}) translate(-1560 -740)", 0.82))
            if ep:
                op = keyframe_value(ep, frame, "opacity", 0)
                layers.append(bush_transform_image(ASSET_MAP["busch_transform"], f"scale({1.0 + op * 0.04:.4f})", 0.30 + op * 0.55))
        if shot["id"] in {"S10", "S11"}:
            b = find_block(blocks, "busch_wake_rise", frame)
            layers.append(busch_image(ASSET_MAP["busch_wake"], motion_transform(b, frame) if b else ""))
        if shot["id"] == "S12": layers.append(busch_image(ASSET_MAP["busch_look"]))
        if shot["id"] == "S13" and frame < 864: layers.append(busch_image(ASSET_MAP["busch_reaction"]))

        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
               f'<title>In the Bushes EP01 origin frame {frame:04d}</title>{"".join(layers)}</svg>')
        svg_path = svg_dir / f"frame-{frame:04d}.svg"; svg_path.write_text(svg, encoding="utf-8")
        png_path = png_dir / f"frame-{frame:04d}.png"
        if raster.endswith("rsvg-convert"):
            cmd = [raster, "-w", str(width), "-h", str(height), str(svg_path), "-o", str(png_path)]
        else:
            cmd = [raster, "-background", "none", "-density", "96", str(svg_path), str(png_path)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if args.preview and frame >= 24:
            break

    end_frame = min(frames - 1, 24) if args.preview else frames - 1
    mp4 = out / "in-the-bushes-ep01-origin-opening-v2.mp4"
    subprocess.run([
        ffmpeg, "-y", "-framerate", str(fps), "-start_number", "0",
        "-i", str(png_dir / "frame-%04d.png"), "-frames:v", str(end_frame + 1),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4)
    ], check=True)
    if not args.keep_svg:
        shutil.rmtree(svg_dir, ignore_errors=True)
    print(mp4)


if __name__ == "__main__":
    main()
