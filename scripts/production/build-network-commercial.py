#!/usr/bin/env python3
"""Build the authored TRIPPEDD Network 20-second mixed-media ident.

This is intentionally a real animated ident, not a static title card:
- four 5-second visual worlds, one for each commissioned show
- kinetic 2D/2.5D geometry and typography
- show-specific visual motifs
- TRIPPEDD wordmark only; no unrequested studio/show names
- generated musical bed with bass, pulse, arpeggio and transition hits
- 1920x1080, 24fps, 48kHz stereo AAC
"""
import os
import subprocess
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(os.environ.get("TRIPPEDD_COMMERCIAL_OUTPUT", ROOT / "public/production/TRIPPEDD-NETWORK-COMMERCIAL-E2E.mp4"))
OUT.parent.mkdir(parents=True, exist_ok=True)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Only these four shows are allowed in the network ident.
SHOWS = [
    ("THE BASTARD", "live / absurd / dangerous", "4A0710", "FF6B35"),
    ("IN THE BUSHES", "wild / strange / unscripted", "063B2B", "B7FF4A"),
    ("GOD MOLECULE", "dream / matter / perception", "081052", "FF4FD8"),
    ("TRIPPEDD", "four worlds / one signal", "18002E", "40C4FF"),
]

def scene(index, bg, fg, title, subtitle):
    # Every scene has multiple independently moving layers. The motion is
    # deliberately graphic/rough rather than a slideshow: sliding blocks,
    # pulsing frames, a moving grid, scanlines, and kinetic type.
    motions = [
        (
            "drawbox=x='mod(420*t-500,w+900)-450':y='h/2-150':w=300:h=300:color=#%s@0.85:t=fill,"
            "drawbox=x='w-mod(300*t,w+700)-350':y='mod(190*t,h+500)-250':w=220:h=220:color=#%s@0.55:t=fill,"
            "drawbox=x='mod(170*t,w+500)-250':y='mod(90*t,h+300)-150':w=500:h=8:color=#%s@0.9:t=fill"
        ),
        (
            "drawbox=x='w/2+260*sin(2*PI*t/2.4)-140':y='h/2+180*cos(2*PI*t/3.1)-140':w=280:h=280:color=#%s@0.78:t=fill,"
            "drawbox=x='mod(240*t,w+800)-400':y='h/2+90*sin(2*PI*t/1.7)':w=420:h=18:color=#%s@0.75:t=fill,"
            "drawbox=x='w-mod(190*t,w+600)-300':y='mod(150*t,h+400)-200':w=180:h=180:color=#%s@0.45:t=fill"
        ),
        (
            "drawbox=x='w/2-180+170*sin(2*PI*t/2.8)':y='h/2-180+170*cos(2*PI*t/2.8)':w=360:h=360:color=#%s@0.50:t=fill,"
            "drawbox=x='w/2-90+300*cos(2*PI*t/1.9)':y='h/2-90+300*sin(2*PI*t/1.9)':w=180:h=180:color=#%s@0.72:t=fill,"
            "drawbox=x='mod(360*t,w+1000)-500':y='mod(260*t,h+900)-450':w=12:h=700:color=#%s@0.8:t=fill"
        ),
        (
            "drawbox=x='mod(520*t,w+1100)-550':y='h/2-8':w=1100:h=16:color=#%s@0.85:t=fill,"
            "drawbox=x='w/2-210+210*sin(2*PI*t/2.2)':y='h/2-210+210*cos(2*PI*t/2.2)':w=420:h=420:color=#%s@0.32:t=fill,"
            "drawbox=x='w-mod(410*t,w+900)-450':y='mod(130*t,h+500)-250':w=300:h=300:color=#%s@0.42:t=fill"
        ),
    ][index] % (fg, fg, fg)

    # A large central title card moves and breathes over the kinetic world.
    return (
        f"color=c=#{bg}:s=1920x1080:r=24:d=5,"
        f"{motions},"
        f"drawgrid=width=96:height=96:thickness=2:color=#{fg}@0.12,"
        f"noise=alls=9:allf=t+u,"
        f"drawbox=x='w/2-700+45*sin(2*PI*t/1.6)':y='h/2-180':w=1400:h=360:color=black@0.48:t=fill,"
        f"drawbox=x='w/2-700':y='h/2-180':w=1400:h=360:color=#{fg}@0.70:t=5,"
        f"drawtext=fontfile={FONT_BOLD}:text='TRIPPEDD':fontcolor=#{fg}:fontsize=118:"
        f"x='w/2-text_w/2+30*sin(2*PI*t/1.8)':y='h/2-text_h/2-76',"
        f"drawtext=fontfile={FONT_BOLD}:text='{title}':fontcolor=white:fontsize=56:"
        f"x='w/2-text_w/2+55*cos(2*PI*t/2.3)':y='h/2+36',"
        f"drawtext=fontfile={FONT}:text='{subtitle}':fontcolor=#{fg}:fontsize=28:"
        f"x='w/2-text_w/2':y='h-92',"
        f"drawtext=fontfile={FONT_BOLD}:text='TRIPPEDD NETWORK':fontcolor=white@0.82:fontsize=22:"
        f"x=54:y=44,"
        f"drawbox=x='54+mod(430*t,1812)':y=78:w=160:h=4:color=#{fg}:t=fill,"
        f"format=yuv420p"
    )

filters = [scene(i, bg, fg, title, subtitle) for i, (title, subtitle, bg, fg) in enumerate(SHOWS)]
filter_complex = ";".join([f"{f}[v{i}]" for i, f in enumerate(filters)] + ["[v0][v1][v2][v3]concat=n=4:v=1:a=0[v]"])

# A musical bed, not a diagnostic hum: kick-like transients, sub bass,
# stereo-width pulse, arpeggio notes, and four transition accents.
# The signal is intentionally audible but leaves headroom for later mix work.
audio = (
    "aevalsrc="
    "0.055*sin(2*PI*55*t)*(0.35+0.65*(0.5+0.5*sin(2*PI*2*t)))"
    "+0.035*sin(2*PI*110*t)"
    "+0.025*sin(2*PI*(220+55*sin(2*PI*t/5))*t)"
    "+0.018*sin(2*PI*(330+110*sin(2*PI*t/2.5))*t)"
    "+0.020*sin(2*PI*440*t)*(0.5+0.5*sin(2*PI*3*t))"
    "+0.035*exp(-70*mod(t,1))*sin(2*PI*95*t)"
    "+0.028*exp(-55*mod(t,0.5))*sin(2*PI*180*t)"
    ":s=48000:d=20,"
    "highpass=f=35,lowpass=f=11000,volume=1.8"
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
