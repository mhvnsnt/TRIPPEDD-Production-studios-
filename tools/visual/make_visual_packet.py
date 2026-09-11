#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path
VIDEO={".mp4",".mov",".mkv",".webm",".avi"}
IMAGE={".png",".jpg",".jpeg",".webp"}
def sha256(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def run(*cmd): subprocess.run(cmd,check=True)
def probe(p):
    r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration,size:stream=index,codec_type,codec_name,width,height,avg_frame_rate","-of","json",str(p)],check=True,capture_output=True,text=True)
    return json.loads(r.stdout)
def extract(p,out,count):
    out.mkdir(parents=True,exist_ok=True)
    d=float(probe(p).get("format",{}).get("duration") or 0)
    if d<=0: raise SystemExit("invalid video duration: "+str(p))
    frames=[]
    for i in range(count):
        t=0 if count==1 else d*i/(count-1)
        dst=out/("frame-%03d.jpg"%(i+1))
        run("ffmpeg","-y","-hide_banner","-loglevel","error","-ss","%.6f"%t,"-i",str(p),"-frames:v","1","-vf","scale=640:-2:force_original_aspect_ratio=decrease","-q:v","3",str(dst))
        frames.append(str(dst.relative_to(out.parent.parent)))
    return frames
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("inputs",nargs="+",type=Path); ap.add_argument("--out",type=Path,required=True); ap.add_argument("--frames",type=int,default=12)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True); root=a.out/"keyframes"; root.mkdir(exist_ok=True)
    manifest={"schemaVersion":1,"visualInspection":"EVIDENCE_ONLY","inputs":[]}
    for src in a.inputs:
        if not src.is_file() or src.stat().st_size==0: raise SystemExit("missing/empty: "+str(src))
        dst=a.out/"media"/src.name; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
        e={"source":str(src),"packetFile":str(dst.relative_to(a.out)),"sha256":sha256(src),"bytes":src.stat().st_size}
        if src.suffix.lower() in VIDEO: e["media"]=probe(src); e["keyframes"]=extract(src,root/src.stem,a.frames)
        elif src.suffix.lower() in IMAGE: e["keyframes"]=[str(dst.relative_to(a.out))]
        else: continue
        manifest["inputs"].append(e)
    (a.out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n"); print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
