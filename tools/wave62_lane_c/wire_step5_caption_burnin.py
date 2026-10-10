#!/usr/bin/env python3
"""Wave 62 Lane C — step 5 standalone: caption burn-in onto the
downstream-denoised mix. Extracted from wire_downstream_caption.py (step 5
only) so it runs in a torch-free process — the full stage-2 script was
SIGKILLED twice by the OOM killer when ECAPA and DeepFilterNet3 shared a
process. Inputs: hypothesis_main_clean.rttm + downstream_denoised_mix.wav
(both already on disk)."""
import json
import os
import re
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "proofs", "rebuilt_pipeline")
PROOFS = os.path.join(HERE, "proofs", "downstream")
os.makedirs(PROOFS, exist_ok=True)

W58 = os.path.join(HERE, "..", "wave58_lane_c", "proofs",
                   "real_voice_diarization")
GT_PATH = os.path.join(W58, "ground_truth.json")
HYP_RTTM = os.path.join(PIPE, "hypothesis_main_clean.rttm")

W, H, FPS = 640, 360, 30
COLORS = {"A": "FFD700", "B": "00E5FF", "C": "FF7AC8"}


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {p.stderr[-2000:]}")
    return p


def load_rttm(p):
    segs = []
    with open(p) as f:
        for line in f:
            parts = line.split()
            segs.append((float(parts[3]), float(parts[3]) + float(parts[4]),
                         parts[7]))
    return segs


def overlap(a0, a1, b0, b1):
    return max(0.0, min(a1, b1) - max(a0, b0))


def esc_ass(t):
    return t.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def fmt_srt(t):
    ms = int(round(t * 1000))
    return (f"{ms//3600000:02d}:{(ms//60000)%60:02d}:"
            f"{(ms//1000)%60:02d},{ms%1000:03d}")


def fmt_ass(t):
    cs = int(round(t * 100))
    return (f"{cs//360000:01d}:{(cs//6000)%60:02d}:"
            f"{(cs//100)%60:02d}.{cs%100:02d}")


def main():
    t_all = time.time()
    res = {"checks": []}

    def check(name, ok, detail):
        res["checks"].append({"name": name, "status": "PASS" if ok else "FAIL",
                              "detail": detail})
        print(("PASS" if ok else "FAIL"), name, "-", detail)

    turns = json.load(open(GT_PATH))["turns"]
    hyp = load_rttm(HYP_RTTM)
    den_wav = os.path.join(PROOFS, "downstream_denoised_mix.wav")
    assert os.path.isfile(den_wav), "run the denoise stages first"

    events = []
    for s, e, spk in hyp:
        best, best_ov = None, 0.0
        for t_ in turns:
            ov = overlap(s, e, t_["start"], t_["end"])
            if ov > best_ov:
                best, best_ov = t_, ov
        events.append((s, e, spk, best["text"] if best else ""))
    check("events_have_text", all(ev[3] for ev in events),
          f"{sum(1 for ev in events if ev[3])}/{len(events)} events carry "
          "GT turn text (words; pipeline supplies who/when — no ASR)")

    srt_path = os.path.join(PROOFS, "captions.srt")
    with open(srt_path, "w") as f:
        for i, (s, e, spk, text) in enumerate(events, 1):
            f.write(f"{i}\n{fmt_srt(s)} --> {fmt_srt(e)}\n"
                    f"[{spk}] {text}\n\n")
    ass_path = os.path.join(PROOFS, "captions.ass")
    with open(ass_path, "w") as f:
        f.write("[Script Info]\nTitle: wave62 downstream captions\n"
                "ScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n")
        f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour,"
                " SecondaryColour, OutlineColour, BackColour, Bold, Italic,"
                " Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
                " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR,"
                " MarginV, Encoding\n")
        for spk, col in COLORS.items():
            bgr = f"{col[4:6]}{col[2:4]}{col[0:2]}"
            f.write(f"Style: Spk{spk},Noto Sans,26,&H00{bgr},&H000000FF,"
                    f"&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0.5,2,"
                    f"30,30,40,1\n")
        f.write("\n[Events]\nFormat: Layer, Start, End, Style, Name, "
                "MarginL, MarginR, MarginV, Effect, Text\n")
        for s, e, spk, text in events:
            f.write(f"Dialogue: 0,{fmt_ass(s)},{fmt_ass(e)},Spk{spk},,0,0,0,,"
                    f"[{{\\b1}}{spk}{{\\b0}}] {esc_ass(text)}\n")
    check("ass_written", os.path.getsize(ass_path) > 1000,
          f"captions.ass {os.path.getsize(ass_path)} bytes")

    dur = 42.9
    src = os.path.join(PROOFS, "waves.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", den_wav,
         "-filter_complex",
         f"[0:a]showwaves=s={W}x{H}:mode=line:colors=white,format=yuv420p[v]",
         "-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-crf", "23",
         "-t", f"{dur:.2f}", src])
    burned = os.path.join(PROOFS, "burned_captions.mp4")
    p = run(["ffmpeg", "-y", "-v", "warning", "-i", src,
             "-vf", f"ass={ass_path}", "-c:a", "copy", burned])
    bad = [l for l in p.stderr.splitlines()
           if re.search(r"error|failed|cannot|unable", l, re.I)]
    check("libass_clean", not bad, f"libass stderr errors: {len(bad)}")

    long_ev = [ev for ev in hyp if ev[1] - ev[0] > 2.0]
    t_on = (long_ev[0][0] + long_ev[0][1]) / 2
    covered = np.zeros(int(dur * FPS) + 1, bool)
    for s, e, _ in hyp:
        covered[int(s * FPS):int(e * FPS) + 1] = True
    t_off = next(i for i in range(len(covered)) if not covered[i]) / FPS
    res["on_off_times"] = {"on": round(t_on, 3), "off": round(t_off, 3)}

    def band_diff(t, tag):
        f1 = os.path.join(PROOFS, f"frame_{tag}.raw")
        f2 = os.path.join(PROOFS, f"frame_src_{tag}.raw")
        for srcf, dst in ((burned, f1), (src, f2)):
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", srcf,
                 "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", dst])
        a = np.fromfile(f1, dtype=np.uint8).reshape(H, W)
        b = np.fromfile(f2, dtype=np.uint8).reshape(H, W)
        band = slice(int(H * 0.70), H)
        return float(np.mean(np.abs(a[band].astype(float) -
                                    b[band].astype(float))))

    d_on = band_diff(t_on, "on")
    d_off = band_diff(t_off, "off")
    res["pixel"] = {"on_mean_abs_diff": round(d_on, 3),
                    "off_mean_abs_diff": round(d_off, 3)}
    check("burn_pixel_on", d_on > 2.0,
          f"caption-ON band diff {d_on:.2f}/255 (> 2.0)")
    check("burn_pixel_off", d_off < 1.0,
          f"caption-OFF band diff {d_off:.2f}/255 (< 1.0)")

    res["passed"] = sum(1 for c in res["checks"] if c["status"] == "PASS")
    res["failed"] = sum(1 for c in res["checks"] if c["status"] == "FAIL")
    res["total_s"] = round(time.time() - t_all, 1)
    json.dump(res, open(os.path.join(PROOFS, "caption_result.json"), "w"),
              indent=2)
    print(f"\n{res['passed']}/{len(res['checks'])} checks PASS "
          f"in {res['total_s']} s")
    return 0 if res["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
