#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, html, json, shutil, subprocess
from pathlib import Path

VIDEO={".mp4",".mov",".mkv",".webm",".avi"}
IMAGE={".png",".jpg",".jpeg",".webp"}

def sha256(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def run(*cmd):
    subprocess.run(cmd,check=True)

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
        dst=out/(f"frame-{i+1:03d}.jpg")
        run("ffmpeg","-y","-hide_banner","-loglevel","error","-ss",f"{t:.6f}","-i",str(p),"-frames:v","1","-vf","scale=640:-2:force_original_aspect_ratio=decrease","-q:v","3",str(dst))
        frames.append(dst)
    return frames

def make_contact_sheet(frames, dst):
    if not frames: return
    cmd=["montage",*[str(x) for x in frames],"-thumbnail","320x320>","-tile","4x","-geometry","+8+8","-background","black",str(dst)]
    run(*cmd)

def write_index(root, manifest):
    rows=[]
    for item in manifest["inputs"]:
        rows.append(f"<h2>{html.escape(Path(item['packetFile']).name)}</h2>")
        for frame in item["keyframes"]:
            rel=Path(frame).as_posix()
            rows.append(f'<a href="{html.escape(rel)}"><img loading="lazy" src="{html.escape(rel)}" width="320"></a>')
    doc="<!doctype html><meta charset=utf-8><title>TRIPPEDD Visual Evidence</title><style>body{font-family:sans-serif;background:#111;color:#eee}img{margin:4px;border:1px solid #555}</style><h1>TRIPPEDD Visual Evidence — pixels, not verdicts</h1>"+''.join(rows)
    (root/"index.html").write_text(doc+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("inputs",nargs="+",type=Path)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--frames",type=int,default=12)
    a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    root=a.out/"keyframes"; root.mkdir(exist_ok=True)
    manifest={"schemaVersion":2,"visualInspection":"EVIDENCE_ONLY","inputs":[]}
    all_frames=[]
    for src in a.inputs:
        if not src.is_file() or src.stat().st_size==0: raise SystemExit("missing/empty: "+str(src))
        dst=a.out/"media"/src.name; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
        e={"source":str(src),"packetFile":str(dst.relative_to(a.out)),"sha256":sha256(src),"bytes":src.stat().st_size}
        if src.suffix.lower() in VIDEO:
            e["media"]=probe(src)
            frames=extract(src,root/src.stem,a.frames)
            e["keyframes"]=[str(x.relative_to(a.out)) for x in frames]
            all_frames.extend(frames)
        elif src.suffix.lower() in IMAGE:
            e["keyframes"]=[str(dst.relative_to(a.out))]
            all_frames.append(dst)
        else:
            continue
        manifest["inputs"].append(e)
    (a.out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    if all_frames:
        make_contact_sheet(all_frames,a.out/"CONTACT-SHEET.jpg")
    write_index(a.out,manifest)
    print(json.dumps(manifest,indent=2))

if __name__=="__main__":
    main()
