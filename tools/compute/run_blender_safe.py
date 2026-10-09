#!/usr/bin/env python3
"""Bounded Blender worker launcher. Heavy rendering stays outside the API process."""
import argparse,json,os,resource,subprocess,time
from pathlib import Path

def rss_bytes(): return int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*1024)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--blend",required=True); ap.add_argument("--output-dir",required=True); ap.add_argument("--frames",default="1-8"); ap.add_argument("--resolution",default="640x360"); ap.add_argument("--blender",default=os.environ.get("TRIPPEDD_BLENDER_BIN","blender")); ap.add_argument("--script",required=True); ap.add_argument("--job-id",required=True)
    a=ap.parse_args(); Path(a.output_dir).mkdir(parents=True,exist_ok=True); lo,hi=map(int,a.frames.split("-",1)); w,h=map(int,a.resolution.split("x"))
    env=dict(os.environ); env.update(TRIPPEDD_JOB_ID=a.job_id,TRIPPEDD_OUTPUT_DIR=str(Path(a.output_dir).resolve()),TRIPPEDD_RESOLUTION=f"{w}x{h}",TRIPPEDD_FRAME_START=str(lo),TRIPPEDD_FRAME_END=str(hi))
    t=time.time(); cp=subprocess.run([a.blender,"-b",a.blend,"--python",a.script],env=env)
    state="SUCCEEDED" if cp.returncode==0 else ("OOM" if cp.returncode<0 and abs(cp.returncode)==9 else "FAILED")
    print(json.dumps({"job_id":a.job_id,"exit_code":cp.returncode,"elapsed_seconds":time.time()-t,"peak_child_rss_bytes":rss_bytes(),"state":state})); return cp.returncode
if __name__=="__main__": raise SystemExit(main())
