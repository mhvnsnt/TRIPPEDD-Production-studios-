#!/usr/bin/env python3
"""LOTI commercial v2 — segment builder. Run from the v2/ dir."""
import subprocess, os, sys, json

V2 = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(os.path.dirname(V2), "luck-of-the-irish-commercial-final.mp4")
FF = ["ffmpeg", "-y", "-v", "error"]

def run(cmd, label):
    print(f"[{label}]", flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FATAL: {label} failed", flush=True); sys.exit(1)

def cover(src, dst):
    """webp/png -> 1920x1080 cover png"""
    run(FF + ["-i", src, "-vf",
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=yuv420p",
        dst], f"cover {os.path.basename(dst)}")

def v1clip(ss, t, dst):
    run(FF + ["-ss", str(ss), "-t", str(t), "-i", V1, "-an",
        "-vf", "scale=1920:1080,fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", dst], f"v1clip {dst}")

def still_vid(png, dur, dst, extra_vf=""):
    vf = f"loop=loop=-1:size=32767,trim=duration={dur},setpts=N/FRAME_RATE/TB,format=yuv420p"
    if extra_vf: vf += "," + extra_vf
    run(FF + ["-i", png, "-vf", vf, "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-an", dst], f"still {dst}")

# ---------- 0. prep stills ----------
M1 = "m1.png"; M2 = "m2.png"; M3 = "m3.png"; HERO = "hero.png"
SB = "sb.png"; SL = "sl.png"
cover("media-generation-v2-morph1-becoming-0-31af0fb6-3039-4f79-8eac-e1e85d6c707e.webp", M1)
cover("media-generation-v2-morph2-halfway-0-cdeeba44-8524-4d89-afe9-ac8dcd3af13b.webp", M2)
cover("media-generation-v2-morph3-almost-0-e61caced-baa3-488e-923f-74aa112c88e6.webp", M3)
cover("media-generation-v2-mascot-hero-reveal-0-6c6004b9-a795-45f5-8596-f4448f4fb9d6.webp", HERO)
cover("media-generation-v2-starburst-0-3828ce11-0501-4513-9624-6babf555c821.webp", SB)
cover("media-generation-v2-speedlines-0-6084afef-9a8c-45cd-8661-ee33baad7385.webp", SL)

# ---------- 1. live segments from v1 ----------
import os as _os
if not _os.path.exists("seg01-live-a.mp4"):
    v1clip(0, 22.9, "seg01-live-a.mp4")
else:
    print("[seg01] exists, skipping", flush=True)

# seg02 ignite: v1 22.9-24.0 + starburst flash + punch-in + green pulse + speedlines
run(FF + ["-ss", "22.9", "-t", "1.1", "-i", V1, "-i", SB, "-i", SL, "-an",
    "-filter_complex",
    "[0:v]setpts=PTS-STARTPTS,format=yuv420p,"
    "scale=w='1920*(1+0.07*exp(-pow((t-0.25)*6,2)))':h='1080*(1+0.07*exp(-pow((t-0.25)*6,2)))':eval=frame,"
    "crop=1920:1080,"
    "eq=saturation='1+0.6*exp(-pow((t-0.3)*4,2))',format=gbrp[base];"
    "[1:v]scale=1920:1080,format=gbrp,fade=t=in:st=0:d=0.08,fade=t=out:st=0.18:d=0.15[sbf];"
    "[base][sbf]blend=all_mode=screen:all_opacity=0.9,format=gbrp[fl];"
    "[2:v]scale=1920:1080,format=gbrp,rotate=a='0.15*t':ow=1920:oh=1080:c=black@0[slr];"
    "[fl][slr]blend=all_mode=screen:all_opacity=0.15,format=yuv420p[out]",
    "-map", "[out]", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
    "seg02-ignite.mp4"], "seg02 ignite")

# seg04: v1 24-28 grade L1
run(FF + ["-ss", "24", "-t", "4", "-i", V1, "-i", SL, "-an",
    "-filter_complex",
    "[0:v]setpts=PTS-STARTPTS,format=yuv420p,eq=saturation=1.35,"
    "colorbalance=gs=0.25:gm=0.15,format=gbrp[base];"
    "[1:v]scale=1920:1080,format=gbrp,rotate=a='0.12*t':ow=1920:oh=1080:c=black@0[slr];"
    "[base][slr]blend=all_mode=screen:all_opacity=0.22,format=yuv420p[out]",
    "-map", "[out]", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
    "seg04-live-l1.mp4"], "seg04 live L1")

# seg06: v1 28-35 grade L2 + flash frames at local 3.5, 5.5
run(FF + ["-ss", "28", "-t", "7", "-i", V1, "-i", SL, "-an",
    "-filter_complex",
    "[0:v]setpts=PTS-STARTPTS,format=yuv420p,eq=saturation=1.55,"
    "colorbalance=gs=0.4:gm=0.25,"
    "drawbox=x=0:y=0:w=iw:h=ih:color=0xAAFFAA@0.55:t=fill:enable='between(t,3.5,3.57)+between(t,5.5,5.57)',format=gbrp[base];"
    "[1:v]scale=1920:1080,format=gbrp,rotate=a='0.1*t':ow=1920:oh=1080:c=black@0[slr];"
    "[base][slr]blend=all_mode=screen:all_opacity=0.32,format=yuv420p[out]",
    "-map", "[out]", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
    "seg06-live-l2.mp4"], "seg06 live L2")

# seg07: freeze v1 t35, 0.5s
run(FF + ["-ss", "35", "-i", V1, "-frames:v", "1", "-vf",
    "scale=1920:1080,format=yuv420p", "freeze35.png"], "freeze35 png")
still_vid("freeze35.png", 0.5, "seg07-freeze.mp4")

# ---------- 2. morph slam beats ----------
def slam(still_png, dst, label):
    # 0.3s starburst flash + 0.7s still with decaying shake
    run(FF + ["-i", SB, "-vf",
        "scale=1920:1080,format=yuv420p,loop=loop=-1:size=32767,trim=duration=0.3,"
        "setpts=N/FRAME_RATE/TB,fade=t=in:st=0:d=0.05,fade=t=out:st=0.2:d=0.1",
        "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-an",
        "tmp-flash.mp4"], label + " flash")
    shake = ("scale=2016:1134,"
             "crop=1920:1080:x='48+14*sin(2*PI*38*t)*exp(-6*t)':y='27+10*cos(2*PI*33*t)*exp(-6*t)',"
             "format=yuv420p")
    still_vid(still_png, 0.7, "tmp-hold.mp4", extra_vf=shake)
    run(FF + ["-i", "tmp-flash.mp4", "-i", "tmp-hold.mp4",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[out]",
        "-map", "[out]", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
        "-an", dst], label + " concat")

slam(M1, "seg03-morph1.mp4", "morph1")
slam(M2, "seg05-morph2.mp4", "morph2")
slam(M3, "seg08-morph3.mp4", "morph3")

# ---------- 3. iris: morph3 -> green -> mascot hero (3.3s) ----------
CLOSE_END = 1.65
run(FF + ["-i", M3, "-i", HERO, "-an", "-filter_complex",
    "[0:v]loop=loop=-1:size=32767,trim=duration=3.3,setpts=N/FRAME_RATE/TB,format=rgba[base];"
    "[1:v]loop=loop=-1:size=32767,trim=duration=3.3,setpts=N/FRAME_RATE/TB,format=rgba,"
    "geq=a='if(lt(hypot(X-960,Y-540),1103*max(0\\,(T-1.65))/1.65)\\,255\\,0)':r='r(X,Y)':g='g(X,Y)':b='b(X,Y)'[heroA];"
    "color=0x00A86B:size=1920x1080:rate=30:duration=3.3,format=rgba,"
    "geq=r='0':g='168':b='107':a='if(gt(hypot(X-960,Y-540)\\,1103*max(0\\,(1.65-T))/1.65)\\,255\\,0)'[grnA];"
    "[base][grnA]overlay=0:0:format=yuv420[tmp];"
    "[tmp][heroA]overlay=0:0:format=yuv420,format=yuv420p[out]",
    "-map", "[out]", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
    "seg09-iris.mp4"], "seg09 iris")

# ---------- 4. mascot hero hold: starburst bg pulsing + mascot floating (2.5s) ----------
run(FF + ["-i", SB, "-i", HERO, "-an", "-filter_complex",
    "[0:v]loop=loop=-1:size=32767,trim=duration=2.5,setpts=N/FRAME_RATE/TB,"
    "scale=w='1920*(1+0.06*sin(2*PI*t/1.2))':h='1080*(1+0.06*sin(2*PI*t/1.2))':eval=frame,"
    "crop=1920:1080,format=yuv420p[bg];"
    "[1:v]loop=loop=-1:size=32767,trim=duration=2.5,setpts=N/FRAME_RATE/TB,"
    "scale=900:-1,format=rgba[fg];"
    "[bg][fg]overlay=x='(W-w)/2':y='(H-h)/2+18*sin(2*PI*t/1.5)':format=yuv420,format=yuv420p[out]",
    "-map", "[out]", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
    "seg10-mascot.mp4"], "seg10 mascot")

print("VIDEO SEGMENTS DONE", flush=True)
