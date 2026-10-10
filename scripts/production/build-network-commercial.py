#!/usr/bin/env python3
"""Build the TRIPPEDD Network 20-second mixed-media ident.

Blender supplies real 3D animation; FFmpeg supplies the final broadcast encode
and 2D signal treatment; Python generates a deterministic rhythmic music bed.
The four-show scope is hard-locked.
"""
import math, os, struct, subprocess, wave
from pathlib import Path
ROOT=Path.cwd()
OUT=Path(os.environ.get("TRIPPEDD_COMMERCIAL_OUTPUT",ROOT/"public/production/TRIPPEDD-NETWORK-COMMERCIAL-E2E.mp4"))
OUT.parent.mkdir(parents=True,exist_ok=True)
FRAME_DIR=Path(os.environ.get("TRIPPEDD_IDENT_FRAME_DIR","/tmp/trippedd-ident-frames"))
FRAME_DIR.mkdir(parents=True,exist_ok=True)
BLENDER_SCRIPT=ROOT/"production/network-ident/blender_ident.py"
AUDIO_WAV=Path("/tmp/trippedd-ident-music.wav")

def require(cmd):
    if subprocess.run(["bash","-lc",f"command -v {cmd} >/dev/null 2>&1"],check=False).returncode:
        raise SystemExit(f"COMMERCIAL_BUILD_FAIL missing command: {cmd}")
for c in ("ffmpeg","blender"): require(c)
for p in FRAME_DIR.glob("frame_*.png"): p.unlink()
blend_file=FRAME_DIR/"trippedd-ident.blend"
if blend_file.exists(): blend_file.unlink()
env=os.environ.copy(); env["TRIPPEDD_IDENT_FRAME_DIR"]=str(FRAME_DIR)
subprocess.run(["blender","-b","--python",str(BLENDER_SCRIPT)],env=env,check=True)
frames=sorted(FRAME_DIR.glob("frame_*.png"))
if len(frames)!=480: raise SystemExit(f"COMMERCIAL_BUILD_FAIL expected 480 rendered frames, found {len(frames)}")

sr=48000; seconds=20; n=sr*seconds
def note_env(t,d): return max(0.0,1.0-t/d)
def sine(f,t): return math.sin(2*math.pi*f*t)
with wave.open(str(AUDIO_WAV),"wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    pcm=bytearray()
    for i in range(n):
        t=i/sr; beat=t/0.5; b=int(math.floor(beat)); local=t-b*0.5; x=0.0
        if local<0.16:
            e=math.exp(-22*local); f=78-38*(local/0.16); x+=0.42*e*sine(f,t)
        if (b%4) in (1,3) and local<0.12:
            e=math.exp(-35*local); noise=math.sin(2*math.pi*(1731+37*(i%19))*t); x+=0.22*e*noise
        sub=t%0.25
        if sub<0.045:
            x+=0.075*math.exp(-70*sub)*math.sin(2*math.pi*(5000+800*math.sin(2*math.pi*t))*t)
        roots=[55.0,65.41,73.42,61.74]; root=roots[min(3,int(t/5))]
        x+=0.115*sine(root,t)*(0.72+0.28*math.sin(2*math.pi*t/2.0))
        arp=[root*2,root*2.5,root*3,root*4,root*3]; f=arp[int((t%1.25)/0.25)]
        x+=0.055*sine(f,t)*note_env(t%0.25,0.25)
        left=max(-0.92,min(0.92,x)); right=max(-0.92,min(0.92,x*0.94))
        pcm+=struct.pack("<hh",int(left*32767),int(right*32767))
    w.writeframes(pcm)

vf="drawgrid=width=96:height=96:thickness=1:color=white@0.08,noise=alls=3:allf=t+u,vignette=PI/5,format=yuv420p"
cmd=["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate","24","-start_number","1","-i",str(FRAME_DIR/"frame_%04d.png"),"-i",str(AUDIO_WAV),"-filter_complex",f"[0:v]{vf}[v]","-map","[v]","-map","1:a","-t","20","-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-movflags","+faststart",str(OUT)]
subprocess.run(cmd,check=True)
print(f"BUILT={OUT}")
