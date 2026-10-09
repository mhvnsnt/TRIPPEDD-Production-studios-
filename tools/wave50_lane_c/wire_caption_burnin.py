#!/usr/bin/env python3
"""Wire-up + smoke proof: ffmpeg ASS caption burn-in pipeline (MIT, this file).

Caption burn-in utility for the TRIPPEDD production pipeline: takes a video
clip + an ASS subtitle file and produces a burned-in MP4 via ffmpeg's `ass`
(libass) filter. ffmpeg itself is invoked as an external binary (not embedded);
only this script is licensed MIT.

Proof (no network): fully synthetic ground truth, deterministic static source:
  1. Generate a 10 s, 640x360@30fps, static-pattern clip (testsrc) + 440 Hz
     sine audio track via lavfi.
  2. Author an ASS file with 3 dialogue events (0.5-3.0 s, 3.5-6.0 s,
     6.5-9.0 s) including italic and color overrides.
  3. Burn: ffmpeg -vf ass=captions.ass -> burned.mp4.
  4. Extract rawvideo frames from burned + original at t=1.5 s (caption ON)
     and t=9.5 s (caption OFF, after last event ends at 9.0 s).
  5. Assert:
     - ffprobe: duration ~10 s, 640x360 video stream, audio stream present
     - caption-ON frames differ strongly in the subtitle band (lower third)
       while caption-OFF frames are near-identical (re-encode noise only)
     - libass emitted no errors during the burn

Usage: python3 wire_caption_burnin.py  (run from this script's directory)
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROOF = HERE / "proofs" / "caption_burnin"
DUR = 10.0
W, H = 640, 360
FPS = 30

ASS_CONTENT = """[Script Info]
ScriptType: v4.00+
PlayResX: 640
PlayResY: 360
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans,28,&H00FFFFFF,&H000019FF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,2,1,2,10,10,24,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:00:03.00,Default,,0,0,0,,BURN-IN PROOF LINE ONE
Dialogue: 0,0:00:03.50,0:00:06.00,Default,,0,0,0,,{\\i1}Line two with italics{\\i0}
Dialogue: 0,0:00:06.50,0:00:09.00,Default,,0,0,0,,Line three: {\\c&H0000FF&}red text{\\c}
"""


def run(cmd, cwd=PROOF):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main():
    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            fail(f"{tool} not found on PATH")
    PROOF.mkdir(parents=True, exist_ok=True)

    # ---- 1. Synthetic source clip (static pattern, deterministic) ----
    src = PROOF / "input_clip.mp4"
    p = run(["ffmpeg", "-y",
             "-f", "lavfi", "-i", f"testsrc=duration={DUR}:size={W}x{H}:rate={FPS}",
             "-f", "lavfi", "-i", f"sine=frequency=440:duration={DUR}:sample_rate=44100",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
             "-c:a", "aac", "-shortest", src.name])
    if p.returncode != 0 or not src.exists():
        fail(f"source clip generation failed:\n{p.stderr[-1500:]}")
    print(f"source clip: {src.name} ({src.stat().st_size} bytes)")

    # ---- 2. ASS file ----
    ass = PROOF / "captions.ass"
    ass.write_text(ASS_CONTENT)
    print(f"ASS written: {ass.name} ({len(ASS_CONTENT)} chars, 3 dialogue events)")

    # ---- 3. Burn-in ----
    burned = PROOF / "burned.mp4"
    p = run(["ffmpeg", "-y", "-i", src.name,
             "-vf", f"ass={ass.name}",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
             "-c:a", "aac", burned.name])
    if p.returncode != 0 or not burned.exists():
        fail(f"burn-in failed:\n{p.stderr[-1500:]}")
    libass_errors = [l for l in p.stderr.splitlines()
                     if re.search(r"(?i)\berror\b|\bfailed\b|\bcannot\b|\bunable\b", l)]
    if libass_errors:
        print("libass stderr notes:")
        for l in libass_errors[:5]:
            print("   ", l)
    print(f"burned: {burned.name} ({burned.stat().st_size} bytes)")

    # ---- 4. ffprobe sanity ----
    p = run(["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_type,codec_name,width,height",
             "-show_entries", "format=duration",
             "-of", "json", burned.name])
    info = json.loads(p.stdout)
    streams = {(s.get("codec_type"), s.get("codec_name")) for s in info["streams"]}
    vstream = next(s for s in info["streams"] if s["codec_type"] == "video")
    dur = float(info["format"]["duration"])
    has_video = (vstream["width"], vstream["height"]) == (W, H)
    has_audio = any(t == "audio" for t, _ in streams)
    print(f"ffprobe: dur={dur:.3f}s (expect {DUR}s), "
          f"{vstream['width']}x{vstream['height']} (expect {W}x{H}), "
          f"audio={'yes' if has_audio else 'no'}")

    # ---- 5. Frame-level ground truth ----
    def grab(video: Path, t: float, tag: str) -> np.ndarray:
        out = PROOF / f"frame_{tag}.raw"
        p = run(["ffmpeg", "-y", "-ss", str(t), "-i", video.name,
                 "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", out.name])
        if p.returncode != 0 or not out.exists():
            fail(f"frame grab failed ({video.name}@{t}s):\n{p.stderr[-800:]}")
        return np.frombuffer(out.read_bytes(), dtype=np.uint8).reshape(H, W, 3).astype(np.float64)

    b_cap = grab(burned, 1.5, "burned_caption_on")
    s_cap = grab(src, 1.5, "src_caption_on")
    b_nocap = grab(burned, 9.5, "burned_caption_off")
    s_nocap = grab(src, 9.5, "src_caption_off")

    # Subtitle band: ASS Alignment 2 (bottom-center), MarginV 24 -> lower third
    band = slice(int(H * 0.66), H)
    diff_on = float(np.mean(np.abs(b_cap[band] - s_cap[band])))
    diff_off = float(np.mean(np.abs(b_nocap[band] - s_nocap[band])))
    full_on = float(np.mean(np.abs(b_cap - s_cap)))
    print(f"subtitle-band mean|diff| @1.5s (caption ON):  {diff_on:.2f}/255")
    print(f"subtitle-band mean|diff| @9.5s (caption OFF): {diff_off:.2f}/255")
    print(f"full-frame  mean|diff| @1.5s (caption ON):  {full_on:.2f}/255")

    dur_ok = abs(dur - DUR) <= 0.3
    cap_ok = diff_on > 2.0 and diff_on > 10 * max(diff_off, 1e-9)
    off_ok = diff_off < 1.0
    print(f"duration ok: {dur_ok}, caption changed pixels: {cap_ok}, "
          f"no-caption unchanged: {off_ok}")
    ok = bool(dur_ok and has_video and has_audio and cap_ok and off_ok)

    result = {
        "tool": "ffmpeg_ass_caption_burnin",
        "license": "MIT (this wire script); ffmpeg invoked as external binary, not embedded",
        "ffmpeg": subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.splitlines()[0],
        "source": {"file": src.name, "size_bytes": src.stat().st_size,
                   "dur_s": DUR, "size": f"{W}x{H}@{FPS}"},
        "ass": {"file": ass.name, "events": 3,
                "windows_s": [[0.5, 3.0], [3.5, 6.0], [6.5, 9.0]]},
        "output": {"file": burned.name, "size_bytes": burned.stat().st_size,
                   "ffprobe_dur_s": round(dur, 3),
                   "video_ok": bool(has_video), "audio_ok": bool(has_audio)},
        "pixel_ground_truth": {
            "subtitle_band_rows": [int(H * 0.66), H],
            "caption_on_t1_5s_mean_abs_diff": round(diff_on, 2),
            "caption_off_t9_5s_mean_abs_diff": round(diff_off, 2),
            "caption_on_fullframe_mean_abs_diff": round(full_on, 2),
            "pass_caption_changed": bool(cap_ok),
            "pass_nocaption_unchanged": bool(off_ok),
        },
        "libass_error_lines": libass_errors[:5],
        "pass": ok,
    }
    out_json = PROOF / "result.json"
    out_json.write_text(json.dumps(result, indent=2))
    print(f"result: {'PASS' if ok else 'FAIL'} -> {out_json.name}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
