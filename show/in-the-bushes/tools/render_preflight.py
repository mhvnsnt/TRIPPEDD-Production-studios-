#!/usr/bin/env python3
"""Fail-fast preflight for the In the Bushes EP01 render pipeline.

This catches the two failure classes that previously made the build look
healthy while still being unrunnable: missing source assets and missing local
render dependencies. It intentionally does not install anything or pretend a
render succeeded.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCENE = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.scene.json"
RENDER = ROOT / "show/in-the-bushes/animatic/ep01-origin-opening-v2.render-plan.json"
BUILDER = ROOT / "show/in-the-bushes/tools/build_origin_opening.py"
CHAR_BUILDER = ROOT / "show/in-the-bushes/tools/build_origin_opening_character.py"
RIG = ROOT / "show/in-the-bushes/tools/teen_performance.py"

ASSETS = [
    ROOT / "show/in-the-bushes/assets/ep01-opening-alley.svg",
    ROOT / "show/in-the-bushes/assets/teens/teen-character-design-v1.svg",
    ROOT / "show/in-the-bushes/assets/props/generic-beer-throw-kit.svg",
    ROOT / "show/in-the-bushes/assets/fx/police-light-sweep.svg",
    ROOT / "show/in-the-bushes/assets/busch/busch-wake.svg",
    ROOT / "show/in-the-bushes/assets/busch/busch-look-away.svg",
    ROOT / "show/in-the-bushes/assets/busch/busch-reaction.svg",
    ROOT / "show/in-the-bushes/assets/ep01-opening-title.svg",
]


def version(exe: str) -> str:
    try:
        p = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10)
        return (p.stdout or p.stderr).splitlines()[0].strip()
    except Exception as exc:  # pragma: no cover - environment dependent
        return f"unavailable ({exc})"


def main() -> int:
    failures = []
    for path in [SCENE, RENDER, BUILDER, CHAR_BUILDER, RIG, *ASSETS]:
        if not path.is_file():
            failures.append(f"missing source: {path.relative_to(ROOT)}")

    try:
        scene = json.loads(SCENE.read_text(encoding="utf-8"))
        render = json.loads(RENDER.read_text(encoding="utf-8"))
        if scene.get("totalFrames") != 888 or scene.get("fps") != 24:
            failures.append("scene master is not 888 frames at 24fps")
        if render.get("totalFrames") != 888 or render.get("resolution") != [1920, 1080]:
            failures.append("render plan does not match 1920x1080 / 888 frames")
    except Exception as exc:
        failures.append(f"cannot parse render inputs: {exc}")

    raster = next((x for x in ("rsvg-convert", "magick", "convert") if shutil.which(x)), None)
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    blender = shutil.which("blender")
    opentoonz = next((x for x in ("OpenToonz", "opentoonz", "toonz") if shutil.which(x)), None)

    print("In the Bushes EP01 render preflight")
    print("- Python: available")
    print(f"- SVG rasterizer: {raster or 'MISSING'}")
    print(f"- FFmpeg: {ffmpeg or 'MISSING'}")
    print(f"- FFprobe: {ffprobe or 'MISSING'}")
    print(f"- Blender/Grease Pencil escalation backend: {blender or 'not installed (optional)'}")
    print(f"- OpenToonz production backend: {opentoonz or 'not installed (optional)'}")

    if not raster:
        failures.append("no SVG rasterizer: install rsvg-convert or ImageMagick")
    if not ffmpeg:
        failures.append("FFmpeg is required for delivery rendering")
    if not ffprobe:
        failures.append("FFprobe is required for final media QC")

    if failures:
        print("\nPREFLIGHT FAIL")
        for failure in failures:
            print("- " + failure)
        return 1

    print("\nPREFLIGHT PASS: source graph and required render dependencies are present.")
    print("Optional backends can be absent; the deterministic Python/SVG/FFmpeg path remains the default.")
    for exe in (raster, "ffmpeg", "ffprobe", blender, opentoonz):
        if exe:
            print(f"  {exe}: {version(exe)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
