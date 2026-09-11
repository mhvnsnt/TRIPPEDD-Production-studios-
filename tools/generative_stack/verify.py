#!/usr/bin/env python3
"""Verify the ten production runtimes and their expected local paths."""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]/"third_party"/"generative"
NAMES=["ComfyUI","InvokeAI","DiffSynth-Studio","LTX-Video","Wan2.1","Blender","OpenToonz","Synfig","Natron","MPFB2"]

ok=True
for name in NAMES:
    p=ROOT/name
    present=(p/".git").exists() or p.exists()
    if not present: ok=False
    print(("READY" if present else "MISSING"), name, p)

for exe in ["blender"]:
    try:
        r=subprocess.run([exe,"--version"],capture_output=True,text=True,timeout=15)
        print("EXEC",exe,"OK" if r.returncode==0 else "FAIL")
    except Exception as e:
        print("EXEC",exe,"UNAVAILABLE",e)

raise SystemExit(0 if ok else 1)
