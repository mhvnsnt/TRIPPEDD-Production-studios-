#!/usr/bin/env python3
"""Fail-fast preflight for the In the Bushes EP01 render pipeline."""
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
SCENE=ROOT/"show/in-the-bushes/animatic/ep01-origin-opening-v2.scene.json"
RENDER=ROOT/"show/in-the-bushes/animatic/ep01-origin-opening-v2.render-plan.json"
BUILDER=ROOT/"show/in-the-bushes/tools/build_origin_opening.py"
CHAR_BUILDER=ROOT/"show/in-the-bushes/tools/build_origin_opening_character.py"
RIG=ROOT/"show/in-the-bushes/tools/teen_performance_v2.py"
SOURCE_TEST=ROOT/"show/in-the-bushes/tools/test_render_source.py"
ACTIVE_TEEN_DESIGN=ROOT/"show/in-the-bushes/assets/teens/teen-character-design-v1.svg"
ASSETS=[ROOT/"show/in-the-bushes/assets/ep01-opening-alley.svg",ACTIVE_TEEN_DESIGN,ROOT/"show/in-the-bushes/assets/props/generic-beer-throw-kit.svg",ROOT/"show/in-the-bushes/assets/fx/police-light-sweep.svg",ROOT/"show/in-the-bushes/assets/busch/busch-wake.svg",ROOT/"show/in-the-bushes/assets/busch/busch-look-away.svg",ROOT/"show/in-the-bushes/assets/busch/busch-reaction.svg",ROOT/"show/in-the-bushes/assets/ep01-opening-title.svg"]
def main():
    failures=[]
    for path in [SCENE,RENDER,BUILDER,CHAR_BUILDER,RIG,SOURCE_TEST,*ASSETS]:
        if not path.is_file(): failures.append(f"missing source: {path.relative_to(ROOT)}")
    try:
        scene=json.loads(SCENE.read_text()); render=json.loads(RENDER.read_text())
        if scene.get("totalFrames")!=888 or scene.get("fps")!=24: failures.append("scene master is not 888 frames at 24fps")
        if render.get("totalFrames")!=888 or render.get("fps")!=24 or render.get("resolution")!=[1920,1080]: failures.append("render plan does not match 1920x1080 / 888 frames at 24fps")
        if render.get("activeBuilder")!="show/in-the-bushes/tools/build_origin_opening_character.py": failures.append("render plan is not using the character-performance builder")
        if render.get("characterSource")!="show/in-the-bushes/tools/teen_performance_v2.py": failures.append("render plan is not using the clean procedural teen rig")
        active_assets=[a for s in render.get("shots",[]) for a in s.get("assets",[])]
        if "teen-group-origin-states.svg" in active_assets: failures.append("obsolete stick-figure teen sheet is still active")
        if "teen-character-design-v1.svg" not in active_assets: failures.append("richer teen character design is not referenced")
    except Exception as exc: failures.append(f"cannot parse render inputs: {exc}")
    for source in (BUILDER,CHAR_BUILDER,RIG,SOURCE_TEST):
        p=subprocess.run([sys.executable,"-m","py_compile",str(source)],cwd=ROOT,capture_output=True,text=True)
        if p.returncode: failures.append(f"Python syntax check failed: {source.relative_to(ROOT)}")
    if not failures:
        p=subprocess.run([sys.executable,str(SOURCE_TEST)],cwd=ROOT,capture_output=True,text=True,timeout=30)
        if p.returncode: failures.append("procedural SVG smoke suite failed: "+((p.stdout+p.stderr).strip().splitlines() or ["unknown failure"])[-1])
    raster=next((x for x in ("rsvg-convert","magick","convert") if shutil.which(x)),None)
    ffmpeg=shutil.which("ffmpeg"); ffprobe=shutil.which("ffprobe")
    print("In the Bushes EP01 render preflight")
    print(f"- Active teen backend: {'present' if RIG.is_file() else 'MISSING'}")
    print(f"- SVG rasterizer: {raster or 'MISSING'}")
    print(f"- FFmpeg: {ffmpeg or 'MISSING'}")
    print(f"- FFprobe: {ffprobe or 'MISSING'}")
    if not raster: failures.append("no SVG rasterizer: install rsvg-convert or ImageMagick")
    if not ffmpeg: failures.append("FFmpeg is required for delivery rendering")
    if not ffprobe: failures.append("FFprobe is required for final media QC")
    if failures:
        print("\nPREFLIGHT FAIL"); [print("- "+x) for x in failures]; return 1
    print("\nPREFLIGHT PASS: source graph, procedural character generation, and render dependencies are present.")
    return 0
if __name__=="__main__": raise SystemExit(main())
