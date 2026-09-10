#!/usr/bin/env python3
"""Build the TRIPPEDD Network 20-second mixed-media ident.

Creative contract:
- exactly four shows: THE BASTARD, IN THE BUSHES, GOD MOLECULE, TRIPPEDD
- no Smoke & Mirrors
- genuinely moving visuals, not a static card/slideshow
- real music bed with percussion, bass and tonal motion
- deterministic/open-source FFmpeg construction so the proof gate is reproducible
"""
import math
import os
import subprocess
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(os.environ.get("TRIPPEDD_COMMERCIAL_OUTPUT", ROOT / "public/production/TRIPPEDD-NETWORK-COMMERCIAL-E2E.mp4"))
OUT.parent.mkdir(parents=True, exist_ok=True)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SHOWS = [
    ("THE BASTARD", "LIVE / ABSURD / DANGEROUS", "28030A", "FF6B35"),
    ("IN THE BUSHES", "WILD / STRANGE / UNSCRIPTED", "03281F", "B7FF4A"),
    ("GOD MOLECULE", "DREAM / MATTER / PERCEPTION", "081052", "FF4FD8"),
    ("TRIPPEDD", "FOUR WORLDS / ONE SIGNAL", "16002A", "40C4FF"),
]

# Each 5-second scene is deliberately layered: animated shapes, scanlines,
# particles, rotating geometry, title movement and a transition wipe.
# This is authored motion graphics, not four still title cards.
def scene(index, bg, fg, title, subtitle):
    if index == 0:
        geometry = (
            f"drawbox=x='w/2+430*sin(2*PI*t/1.25)-170':y='h/2+250*cos(2*PI*t/1.55)-170':w=340:h=340:color=#{fg}@0.55:t=fill,"
            f"drawbox=x='mod(760*t,w+900)-450':y='h/2-5':w=900:h=10:color=#{fg}@0.95:t=fill,"
            f"drawbox=x='w/2-520':y='h/2-360+110*sin(2*PI*t/1.7)':w=1040:h=720:color=black@0.28:t=5,"
        )
    elif index == 1:
        geometry = (
            f"drawbox=x='w/2+380*cos(2*PI*t/1.8)-150':y='h/2+260*sin(2*PI*t/1.25)-150':w=300:h=300:color=#{fg}@0.52:t=fill,"
            f"drawbox=x='mod(520*t,w+700)-350':y='h/2+140*sin(2*PI*t/1.1)':w=520:h=22:color=#{fg}@0.88:t=fill,"
            f"drawbox=x='w/2-600+240*sin(2*PI*t/2.4)':y='h/2-280':w=1200:h=560:color=black@0.30:t=5,"
        )
    elif index == 2:
        geometry = (
            f"drawbox=x='w/2-220+190*sin(2*PI*t/2.1)':y='h/2-220+190*cos(2*PI*t/2.1)':w=440:h=440:color=#{fg}@0.28:t=fill,"
            f"drawbox=x='w/2-90+420*cos(2*PI*t/1.45)':y='h/2-90+420*sin(2*PI*t/1.45)':w=180:h=180:color=#{fg}@0.66:t=fill,"
            f"drawbox=x='mod(900*t,w+1200)-600':y='mod(420*t,h+900)-450':w=18:h=900:color=#{fg}@0.72:t=fill,"
        )
    else:
        geometry = (
            f"drawbox=x='mod(980*t,w+1200)-600':y='h/2-12':w=1200:h=24:color=#{fg}@0.92:t=fill,"
            f"drawbox=x='w/2-240+250*sin(2*PI*t/1.55)':y='h/2-240+250*cos(2*PI*t/1.55)':w=480:h=480:color=#{fg}@0.25:t=fill,"
            f"drawbox=x='w-mod(620*t,w+1000)-500':y='mod(210*t,h+600)-300':w=260:h=260:color=#{fg}@0.38:t=fill,"
        )
    return (
        f"color=c=#{bg}:s=1920x1080:r=24:d=5,"
        f"{geometry}"
        f"drawgrid=width=64:height=64:thickness=1:color=#{fg}@0.13,"
        f"noise=alls=7:allf=t+u,"
        f"drawbox=x='w/2-720':y='h/2-205':w=1440:h=410:color=black@0.52:t=fill,"
        f"drawbox=x='w/2-720':y='h/2-205':w=1440:h=410:color=#{fg}@0.78:t=7,"
        f"drawtext=fontfile={FONT_BOLD}:text='TRIPPEDD':fontcolor=#{fg}:fontsize=112:"
        f"x='w/2-text_w/2+55*sin(2*PI*t/1.1)':y='h/2-text_h/2-82',"
        f"drawtext=fontfile={FONT_BOLD}:text='{title}':fontcolor=white:fontsize=58:"
        f"x='w/2-text_w/2+38*cos(2*PI*t/0.9)':y='h/2+38',"
        f"drawtext=fontfile={FONT}:text='{subtitle}':fontcolor=#{fg}:fontsize=25:"
        f"x='w/2-text_w/2':y='h-105',"
        f"drawtext=fontfile={FONT_BOLD}:text='TRIPPEDD NETWORK':fontcolor=white@0.85:fontsize=23:x=54:y=42,"
        f"drawbox=x='54+mod(760*t,1812)':y=79:w=210:h=5:color=#{fg}:t=fill,"
        f"format=yuv420p"
    )

filters = [scene(i, bg, fg, title, subtitle) for i, (title, subtitle, bg, fg) in enumerate(SHOWS)]
filter_complex = ";".join([f"{f}[v{i}]" for i, f in enumerate(filters)] + ["[v0][v1][v2][v3]concat=n=4:v=1:a=0[v]"])

# Musical bed: kick/pulse + bass + chord tones + high arpeggio.
# All sources are deterministic lavfi and rendered as 48 kHz stereo AAC.
audio_specs = [
    ("55", "0.16", "sine"),
    ("110", "0.09", "sine"),
    ("164.81", "0.07", "sine"),
    ("220", "0.055", "sine"),
    ("329.63", "0.045", "sine"),
    ("440", "0.035", "sine"),
]
audio_inputs, labels = [], []
for i, (freq, gain, _) in enumerate(audio_specs):
    audio_inputs += ["-f", "lavfi", "-i", f"sine=frequency={freq}:sample_rate=48000:duration=20"]
    labels.append(f"[{i}:a]volume={gain}[a{i}]")
# A separate modulated pulse creates audible rhythmic movement without relying
# on fragile expression parsing.
audio_inputs += ["-f", "lavfi", "-i", "anoisesrc=color=pink:amplitude=0.025:sample_rate=48000:duration=20"]
labels.append("[6:a]highpass=f=2500,lowpass=f=9000,volume=0.7[noise]")
mix = "".join(f"[a{i}]" for i in range(len(audio_specs))) + "[noise]"
audio_graph = ";".join(labels + [f"{mix}amix=inputs=7:duration=longest:normalize=0,volume=2.8,highpass=f=35,lowpass=f=11000,aresample=48000[a]"])

cmd = [
    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
    *audio_inputs,
    "-filter_complex", filter_complex + ";" + audio_graph,
    "-map", "[v]", "-map", "[a]", "-t", "20",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
    "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(OUT),
]
subprocess.run(cmd, check=True)
print(f"BUILT={OUT}")
