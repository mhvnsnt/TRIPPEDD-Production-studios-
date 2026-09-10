#!/usr/bin/env python3
"""Build the TRIPPEDD Network 20-second mixed-media ident.

Procedural, deterministic, and intentionally kinetic:
- four 5-second visual worlds
- four TRIPPEDD show identities
- moving geometric overlays, scanlines, grain and palette shifts
- authored TRIPPEDD wordmark
- generated electronic bed with bass/pulse/chime
"""
import os
import subprocess
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(os.environ.get("TRIPPEDD_COMMERCIAL_OUTPUT", ROOT / "public/production/TRIPPEDD-NETWORK-COMMERCIAL-E2E.mp4"))
OUT.parent.mkdir(parents=True, exist_ok=True)

shows = [
    ("THE BASTARD", "live / absurd / dangerous", "8B1E2D", "F5E7D0"),
    ("GOD MOLECULE", "dream / matter / perception", "081052", "FF4FD8"),
    ("SMOKE & MIRRORS", "light / geometry / physics", "10204A", "40C4FF"),
    ("TRIPPEDD", "everything is connected", "16002E", "7CFF6B"),
]

def seg(bg, fg, title, subtitle, variant):
    shape1 = {
        0: "drawbox=x='mod(180*t-220,w+440)-220':y=70:w=330:h=330:color=#"+fg+"@0.78:t=fill",
        1: "drawbox=x='mod(250*t-320,w+640)-320':y='h-390':w=420:h=420:color=#"+fg+"@0.62:t=fill",
        2: "drawbox=x='w-mod(210*t,w+500)-250':y='mod(120*t,h+500)-250':w=500:h=500:color=#"+fg+"@0.42:t=fill",
        3: "drawbox=x='mod(300*t,w+700)-350':y='h-mod(170*t,h+600)-300':w=360:h=360:color=#"+fg+"@0.58:t=fill",
    }[variant]
    shape2 = {
        0: "drawbox=x='w-mod(145*t,w+300)-120':y='mod(95*t,h+300)-150':w=240:h=240:color=#"+fg+"@0.45:t=fill",
        1: "drawbox=x='mod(100*t,w+500)-250':y='h-mod(155*t,h+500)-250':w=500:h=500:color=#"+fg+"@0.32:t=fill",
        2: "drawbox=x='mod(190*t,w+450)-225':y='mod(85*t,h+400)-200':w=450:h=450:color=#"+fg+"@0.35:t=fill",
        3: "drawbox=x='w-mod(260*t,w+600)-300':y='mod(110*t,h+500)-250':w=600:h=600:color=#"+fg+"@0.25:t=fill",
    }[variant]
    return (
        f"color=c=#{bg}:s=1280x720:r=24:d=5,"
        f"{shape1},{shape2},"
        f"drawgrid=width=64:height=64:thickness=1:color=#{fg}@0.16,"
        f"noise=alls=7:allf=t+u,"
        f"drawbox=x='w/2-250':y='h/2-120':w=500:h=240:color=#{bg}@0.72:t=fill,"
        f"drawbox=x='w/2-250':y='h/2-120':w=500:h=240:color=#{fg}@0.28:t=4,"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text='TRIPPEDD':fontcolor=#{fg}:fontsize=82:"
        f"x='w/2-text_w/2+8*sin(2*PI*t/2.5)':y='h/2-text_h/2-28',"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text='{title}':fontcolor=white:fontsize=40:"
        f"x='w/2-text_w/2':y='h/2+34',"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
        f"text='{subtitle}':fontcolor=#{fg}:fontsize=22:"
        f"x='w/2-text_w/2':y='h-64',"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text='TRIPPEDD NETWORK':fontcolor=white@0.75:fontsize=18:x=36:y=30,"
        f"format=yuv420p"
    )

filters = [seg(bg, fg, title, subtitle, i) for i, (title, subtitle, bg, fg) in enumerate(shows)]
filter_complex = ";".join(
    [f"{f}[v{i}]" for i, f in enumerate(filters)]
    + ["[v0][v1][v2][v3]concat=n=4:v=1:a=0[v]"]
)
audio = (
    "aevalsrc="
    "0.13*sin(2*PI*55*t)"
    "+0.07*sin(2*PI*(110+8*sin(2*PI*t/5))*t)"
    "+0.045*sin(2*PI*220*t)"
    "+0.025*sin(2*PI*440*t)"
    ":s=48000:d=20,"
    "highpass=f=35,lowpass=f=9000,volume=1.4"
)

cmd = [
    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
    "-f", "lavfi", "-i", audio,
    "-filter_complex", filter_complex,
    "-map", "[v]", "-map", "0:a:0", "-t", "20",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(OUT)
]
subprocess.run(cmd, check=True)
print(f"BUILT={OUT}")
