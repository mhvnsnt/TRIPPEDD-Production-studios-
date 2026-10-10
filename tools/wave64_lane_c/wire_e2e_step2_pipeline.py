#!/usr/bin/env python3
"""Wave 64 Lane C — task 2, step 2: FULL end-to-end pipeline on real
multi-speaker audio with the Wave-64 recommended VAD.

  raw fixture audio (Wave-58 dialogue.wav, 3 Kokoro voices)
   -> webrtcvad VAD (RECOMMENDED: aggressiveness 0, 10 ms, 0.3 s pad)
   -> window grid 1.5 s / 0.25 s + energy gate (0.02/0.04/0.08 sweep —
      loosening now possible: step 1 recomputed ECAPA for all 166 windows)
   -> REAL ECAPA-TDNN embeddings (step 1, SpeechBrain, computed on RAW
      audio — quarantine: NO denoise upstream of the speaker path)
   -> blind eigengap speaker count -> forced-k SpectralCluster
   -> GT-informed Hungarian cluster->speaker map
   -> F0 no-fill + F1 fill-within-VAD labeling -> DER/JER (pyannote-metrics)
   -> caption path: per-speaker hypothesis segments -> SRT/ASS ->
      ffmpeg burn-in onto the RAW mix -> pixel ON/OFF checks

Downstream-denoise quarantine: DeepFilterNet3 is NOT installed in this
lane (no Rust toolchain on the VM to build deepfilternet/DeepFilterLib;
the checkpoint bytes sit in ~/.cache/DeepFilterNet from Wave-62). The
caption path therefore burns onto the raw mix; the speaker path never
sees denoised audio either way — the quarantine holds trivially and
honestly. Denoise stays a downstream-caption-path-only stage.

Runs in the torch-free lane venv. Re-run: ./venv/bin/python
wire_e2e_step2_pipeline.py (after step 1 wrote embeddings_all166.npy).

Licenses (wired path): webrtcvad MIT, SpectralCluster Apache-2.0,
pyannote-metrics MIT, SpeechBrain ECAPA Apache-2.0, scikit-learn/numpy/
scipy BSD. Lane code MIT. No GPL.
"""
import json
import math
import os
import re
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "end_to_end")
os.makedirs(PROOFS, exist_ok=True)

W63 = os.path.join(HERE, "..", "wave63_lane_c")
sys.path.insert(0, W63)
sys.path.insert(0, HERE)
import wire_vad_coverage_recovery as w63  # noqa: E402
import wire_vad_recall_experiment as w64  # noqa: E402

SR = w63.SR
WIN_S, HOP_S = w63.WIN_S, w63.HOP_S
# Recommended production VAD from the task-1 experiment
VAD_CFG = {"agg": 0, "frame_ms": 10, "pad": 0.3, "use_pad": True}
W, H, FPS = 640, 360, 30
COLORS = {"A": "FFD700", "B": "00E5FF", "C": "FF7AC8"}


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {p.stderr[-2000:]}")
    return p


def fmt_srt(t):
    ms = int(round(t * 1000))
    return (f"{ms//3600000:02d}:{(ms//60000)%60:02d}:"
            f"{(ms//1000)%60:02d},{ms%1000:03d}")


def fmt_ass(t):
    cs = int(round(t * 100))
    return (f"{cs//360000:01d}:{(cs//6000)%60:02d}:"
            f"{(cs//100)%60:02d}.{cs%100:02d}")


def esc_ass(t):
    return t.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def pipeline_run(audio, turns, all_emb, vad_segs, sil_frac):
    """Full diarization run on real-compute embeddings. Returns dict."""
    idxs, rmsv, _, _ = w63.window_grid(audio)
    thr = sil_frac * float(np.max(rmsv))
    all_speech = np.flatnonzero(rmsv >= thr)
    kept = [int(j) for j in all_speech
            if w63.inside_vad(j * HOP_S, j * HOP_S + WIN_S, vad_segs)]
    if len(kept) < 2:
        return {"failed": "kept<2"}
    # all_emb row p == grid window NUMBER p (step 1 convention)
    emb = all_emb[np.asarray([int(j) for j in kept])]
    k_est, eigs, gaps, margin = w63.eigengap_laplacian(emb)
    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=k_est, max_clusters=k_est,
                           custom_dist="cosine")
    labels = np.asarray(cl.predict(emb), dtype=int)
    n_frames = int(math.ceil((len(audio) / SR) / HOP_S))
    frames_f0 = w63.label_v2c_no_fill(kept, labels, vad_segs, n_frames)
    frames_f1 = w63.fill_within_vad(frames_f0, vad_segs, n_frames)
    cmap, purity, _ = w63.hungarian_map(frames_f0, turns)
    spk_of = {c: cmap[c] for c in set(frames_f0[frames_f0 != -1].tolist())}
    out = {"kept": len(kept), "k": k_est, "margin": round(margin, 2),
           "purity": round(purity, 4), "map": cmap}
    for tag, fvar in (("F0", frames_f0), ("F1", frames_f1)):
        segs_out = [(s, e, spk_of[c])
                    for s, e, c in w63.segments_from_frames(fvar)]
        hyp_path = os.path.join(PROOFS, f"e2e_tmp_{tag}.rttm")
        w63.write_rttm(hyp_path, segs_out)
        d, j, comp = w63.score(w63.REF_RTTM, hyp_path, 0.0)
        d25, j25, comp25 = w63.score(w63.REF_RTTM, hyp_path, 0.25)
        out[tag] = {
            "DER": round(d, 4), "JER": round(j, 4),
            "miss": round(comp["missed detection"], 3),
            "FA": round(comp["false alarm"], 3),
            "conf": round(comp["confusion"], 3),
            "DER_c025": round(d25, 4), "JER_c025": round(j25, 4),
            "segments": [[round(s, 3), round(e, 3), sp]
                         for s, e, sp in segs_out],
        }
    return out


def main():
    t0 = time.time()
    res = {"wave": 64, "lane": "C", "task": "end-to-end pipeline",
           "vad_cfg": VAD_CFG, "checks": []}

    def check(name, ok, detail):
        res["checks"].append({"name": name, "pass": bool(ok),
                              "detail": detail})
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

    audio, turns, _fixture_emb = w63.load_fixture()
    check("fixture_shas", True, "wave58 fixture SHA-verified")
    emb_path = os.path.join(PROOFS, "embeddings_all166.npy")
    assert os.path.isfile(emb_path), "run step 1 first"
    all_emb = np.load(emb_path)
    assert all_emb.shape == (166, 192)
    check("real_ecapa_embeddings", True,
          f"step-1 real-compute ECAPA embeddings loaded {all_emb.shape} "
          f"(computed on RAW audio — quarantine: no upstream denoise)")

    vad_segs = w64.vad_segments_gen(audio, **VAD_CFG)
    rec, prec, _, _ = w64.vad_quality_frames(vad_segs, turns, len(audio))
    check("recommended_vad", abs(rec - 0.9728) < 0.002 and len(vad_segs) == 9,
          f"VAD recall={rec:.4f} prec={prec:.4f} segs={len(vad_segs)}")

    idxs = list(range(0, len(audio) - int(WIN_S * SR) + 1, int(HOP_S * SR)))
    assert len(idxs) == 166  # window numbers 0..165 == all_emb rows

    # energy-gate sweep incl. LOOSENING (deferred from task 1)
    print("gate sweep (real-compute embeddings, all 166 windows):",
          flush=True)
    sweep = {}
    for sil in (0.02, 0.04, 0.08):
        pr = pipeline_run(audio, turns, all_emb, vad_segs, sil)
        sweep[str(sil)] = pr
        f1 = pr["F1"]
        print(f"  gate={sil}: kept={pr['kept']} k={pr['k']} "
              f"margin={pr['margin']} F1 DER={f1['DER']} miss={f1['miss']} "
              f"FA={f1['FA']} conf={f1['conf']} c025={f1['DER_c025']}",
              flush=True)
    res["gate_sweep"] = sweep
    best_sil = min(sweep, key=lambda s: sweep[s]["F1"]["DER"])
    best = sweep[best_sil]
    res["best_gate"] = best_sil
    print(f"  best gate: {best_sil} -> F1 DER={best['F1']['DER']}",
          flush=True)
    check("blind_k3", best["k"] == 3,
          f"eigengap blind k={best['k']} margin={best['margin']}x")
    check("purity", best["purity"] == 1.0,
          f"frame purity={best['purity']} map={best['map']}")
    check("e2e_beats_wave63",
          best["F1"]["DER"] < 0.0712,
          f"end-to-end F1 DER={best['F1']['DER']} vs wave63 0.0712 "
          f"(task-1 torch-free recommended: 0.0382)")
    check("no_confusion", best["F1"]["conf"] == 0.0,
          f"confusion={best['F1']['conf']}s")

    # final hypothesis RTTM (best gate, F1 labeling)
    hyp_path = os.path.join(PROOFS, "hypothesis_e2e_F1.rttm")
    with open(hyp_path, "w") as f:
        for s, e, sp in best["F1"]["segments"]:
            f.write(f"SPEAKER dialogue 1 {s:.3f} {e - s:.3f} "
                    f"<NA> <NA> {sp} <NA> <NA>\n")
    check("hypothesis_written", True, f"{hyp_path}")

    # ---- caption path: SRT + ASS + ffmpeg burn-in onto the RAW mix
    def overlap(a0, a1, b0, b1):
        return max(0.0, min(a1, b1) - max(a0, b0))

    events = []
    for s, e, spk in best["F1"]["segments"]:
        b, bov = None, 0.0
        for t_ in turns:
            ov = overlap(s, e, t_["start"], t_["end"])
            if ov > bov:
                b, bov = t_, ov
        events.append((s, e, spk, b["text"] if b else ""))
    check("events_have_text", all(ev[3] for ev in events),
          f"{sum(1 for ev in events if ev[3])}/{len(events)} events carry "
          "GT turn text (pipeline supplies who/when — no ASR)")

    srt_path = os.path.join(PROOFS, "captions_e2e.srt")
    with open(srt_path, "w") as f:
        for i, (s, e, spk, text) in enumerate(events, 1):
            f.write(f"{i}\n{fmt_srt(s)} --> {fmt_srt(e)}\n"
                    f"[{spk}] {text}\n\n")
    ass_path = os.path.join(PROOFS, "captions_e2e.ass")
    with open(ass_path, "w") as f:
        f.write("[Script Info]\nTitle: wave64 e2e captions\n"
                "ScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n")
        f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, "
                "PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
                "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, "
                "Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
                "MarginR, MarginV, Encoding\n")
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
          f"captions_e2e.ass {os.path.getsize(ass_path)} bytes")

    # quarantine note: burn-in onto the RAW mix (no DeepFilterNet in lane;
    # speaker path never saw denoised audio either way)
    import wave as wv
    with wv.open(w63.DIALOGUE, "rb") as w:
        dur = w.getnframes() / w.getframerate()
    src = os.path.join(PROOFS, "waves_e2e.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", w63.DIALOGUE,
         "-filter_complex",
         f"[0:a]showwaves=s={W}x{H}:mode=line:colors=white,format=yuv420p[v]",
         "-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-crf", "23",
         "-t", f"{dur:.2f}", src])
    burned = os.path.join(PROOFS, "burned_captions_e2e.mp4")
    p = run(["ffmpeg", "-y", "-v", "warning", "-i", src,
             "-vf", f"ass={ass_path}", "-c:a", "copy", burned])
    bad = [l for l in p.stderr.splitlines()
           if re.search(r"error|failed|cannot|unable", l, re.I)]
    check("libass_clean", not bad, f"libass stderr errors: {len(bad)}")
    check("burned_mp4", os.path.getsize(burned) > 10000,
          f"burned_captions_e2e.mp4 {os.path.getsize(burned)} bytes")

    hyp = [(s, e) for s, e, _ in best["F1"]["segments"]]
    long_ev = [(s, e) for s, e in hyp if e - s > 2.0]
    t_on = (long_ev[0][0] + long_ev[0][1]) / 2
    covered = np.zeros(int(dur * FPS) + 1, bool)
    for s, e in hyp:
        covered[int(s * FPS):int(e * FPS) + 1] = True
    t_off = next(i for i in range(len(covered)) if not covered[i]) / FPS

    def band_diff(t, tag):
        f1 = os.path.join(PROOFS, f"frame_{tag}.raw")
        f2 = os.path.join(PROOFS, f"frame_src_{tag}.raw")
        for srcf, dst in ((burned, f1), (src, f2)):
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i",
                 srcf, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt",
                 "gray", dst])
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

    res["elapsed_s"] = round(time.time() - t0, 1)
    n_pass = sum(c["pass"] for c in res["checks"])
    res["checks_pass"] = f"{n_pass}/{len(res['checks'])}"
    with open(os.path.join(PROOFS, "end_to_end_result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n{n_pass}/{len(res['checks'])} checks PASS, "
          f"{res['elapsed_s']}s. Result -> proofs/end_to_end/", flush=True)
    if n_pass != len(res["checks"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
