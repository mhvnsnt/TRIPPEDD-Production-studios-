#!/usr/bin/env python3
"""Wire imageio-ffmpeg (BSD-2-Clause, github.com/imageio/imageio-ffmpeg).

Provides a static ffmpeg binary via pip — no system install needed.
Production relevance: TRIPPEDD/God-Molecule video pipeline
(tools/video_pipeline, tools/video): test-pattern generation, probing,
frame extraction, downscale transcode — the primitives every promo/entrance
render pass needs. The bundled ffmpeg binary is used as a standalone tool
(via subprocess), never linked — the quarantine doctrine's standalone-tool
pattern; the imageio-ffmpeg package itself is BSD-2-Clause.

Run: /home/hatch/.cache/w43b_venv/bin/python wire_imageio_ffmpeg.py

Outputs (all small, committed): ffmpeg_test.mp4, ffmpeg_frame.png,
ffmpeg_probe.json, ff_report.txt
"""
import json
import os
import re
import struct
import subprocess

import imageio_ffmpeg

OUT = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
MP4 = os.path.join(OUT, "ffmpeg_test.mp4")
SMALL = os.path.join(OUT, "ffmpeg_test_360p.mp4")
FRAME = os.path.join(OUT, "ffmpeg_frame.png")
PROBE = os.path.join(OUT, "ffmpeg_probe.json")
REPORT = os.path.join(OUT, "ff_report.txt")


def run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    print("imageio-ffmpeg version:", imageio_ffmpeg.__version__)
    print("ffmpeg exe:", FF, os.path.getsize(FF), "bytes")
    rc, out, err = run([FF, "-version"])
    assert rc == 0, "ffmpeg -version failed"
    ver = out.splitlines()[0]
    print(ver)

    # 1. generate a 2 s 640x360 30 fps test pattern (small: crf 30)
    rc, out, err = run([FF, "-y", "-f", "lavfi",
                        "-i", "testsrc=size=640x360:rate=30:duration=2",
                        "-c:v", "libx264", "-crf", "30", "-pix_fmt", "yuv420p",
                        MP4])
    assert rc == 0 and os.path.exists(MP4), f"testsrc encode failed: {err[-500:]}"
    print(f"encoded: {MP4} ({os.path.getsize(MP4)} bytes)")

    # 2. probe it (parse ffmpeg -i stderr)
    rc, out, err = run([FF, "-i", MP4])
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    m2 = re.search(r"Video: [^\n]*?(\d{2,5}x\d{2,5})", err)
    res = m2.group(1)
    m3 = re.search(r"(\d+(?:\.\d+)?) fps", err)
    fps = m3.group(1)
    print(f"probe: duration={dur:.2f}s res={res} fps={fps}")

    # 3. extract the frame at t=1.0 s as PNG, verify PNG IHDR dims by hand
    rc, out, err = run([FF, "-y", "-ss", "1.0", "-i", MP4, "-frames:v", "1",
                        FRAME])
    assert rc == 0 and os.path.exists(FRAME), f"frame extract failed: {err[-500:]}"
    with open(FRAME, "rb") as f:
        data = f.read(33)
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", data[16:24])
    print(f"frame: {FRAME} ({os.path.getsize(FRAME)} bytes) IHDR {w}x{h}")
    assert (w, h) == (640, 360), f"unexpected frame dims {w}x{h}"

    # 4. downscale transcode 640x360 -> 320x180 (real pipeline primitive)
    rc, out, err = run([FF, "-y", "-i", MP4, "-vf", "scale=320:180",
                        "-c:v", "libx264", "-crf", "30", "-pix_fmt", "yuv420p",
                        SMALL])
    assert rc == 0 and os.path.exists(SMALL), f"transcode failed: {err[-500:]}"
    print(f"transcoded: {SMALL} ({os.path.getsize(SMALL)} bytes)")

    with open(PROBE, "w") as f:
        json.dump({"ffmpeg_version": ver, "ffmpeg_exe_bytes": os.path.getsize(FF),
                   "src": {"file": "ffmpeg_test.mp4",
                           "bytes": os.path.getsize(MP4),
                           "duration_s": round(dur, 2),
                           "resolution": res, "fps": fps},
                   "frame_png": {"file": "ffmpeg_frame.png",
                                 "bytes": os.path.getsize(FRAME),
                                 "ihdr": [w, h]},
                   "transcode_180p": {"file": "ffmpeg_test_360p.mp4",
                                      "bytes": os.path.getsize(SMALL)}},
                  f, indent=2)
    with open(REPORT, "w") as f:
        f.write("imageio-ffmpeg wire report (Wave 43 Lane B)\n")
        f.write(f"imageio-ffmpeg: {imageio_ffmpeg.__version__} (BSD-2-Clause)\n")
        f.write(f"{ver}\n")
        f.write(f"ffmpeg exe: {os.path.getsize(FF)} bytes (static, pip-bundled)\n")
        f.write(f"1. testsrc encode 640x360@30fps 2s -> ffmpeg_test.mp4 "
                f"({os.path.getsize(MP4)} bytes)\n")
        f.write(f"2. probe: duration {dur:.2f}s, {res}, {fps} fps\n")
        f.write(f"3. frame @1.0s -> ffmpeg_frame.png ({os.path.getsize(FRAME)} bytes), "
                f"IHDR {w}x{h} verified\n")
        f.write(f"4. scale 320x180 transcode -> ffmpeg_test_360p.mp4 "
                f"({os.path.getsize(SMALL)} bytes)\n")
        f.write("verdict: PASS — real encode/probe/extract/transcode, no stub\n")
    print("verdict: PASS")
    print("wrote", PROBE, REPORT)


if __name__ == "__main__":
    main()
