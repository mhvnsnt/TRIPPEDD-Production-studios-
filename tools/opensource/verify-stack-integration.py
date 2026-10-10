#!/usr/bin/env python3
"""Fail-closed verification for the TRIPPEDD full-upstream stack."""
import json, os, subprocess, sys
from pathlib import Path
ROOT=Path(os.environ.get("TRIPPEDD_OPENSOURCE_ROOT",".trippedd/opensource"))
REQUIRED=["flamenco","opencue","opentimelineio","opencolorio","openimageio","openexr","openvdb","natron","kitsu","comfyui","vapoursynth","mlt"]
def sh(*args):
    return subprocess.run(args,capture_output=True,text=True,check=False)
rows=[]; failed=False
for name in REQUIRED:
    p=ROOT/name
    row={"name":name,"path":str(p),"git":False,"revision":None,"healthy":False}
    if (p/".git").exists():
        row["git"]=True
        r=sh("git","-C",str(p),"rev-parse","HEAD")
        if r.returncode==0:
            row["revision"]=r.stdout.strip()
            row["healthy"]=True
    rows.append(row); failed |= not row["healthy"]
report={"root":str(ROOT),"required":len(REQUIRED),"healthy":sum(r["healthy"] for r in rows),"failed":sum(not r["healthy"] for r in rows),"components":rows}
print(json.dumps(report,indent=2,sort_keys=True))
Path("stack-integration-report.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
sys.exit(40 if failed else 0)
