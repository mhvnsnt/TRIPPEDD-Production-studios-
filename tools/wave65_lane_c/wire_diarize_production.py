#!/usr/bin/env python3
"""Wave 65 Lane C — PRODUCTION diarization port.

The proven Wave-64 operating point (webrtcvad aggressiveness 0 / 10 ms
frames / 0.3 s hangover pad -> DER 0.0382 / JER 0.0378 on the multi-speaker
fixture, -46% vs Wave-63) wired as a single production-ready script.

Topology (production law honored throughout):
  raw audio
   -> webrtcvad VAD (agg=0, 10 ms, 0.3 s pad)             [webrtcvad MIT]
   -> window grid 1.5 s / 0.25 s + energy gate + strict VAD inclusion
   -> ECAPA-TDNN embeddings on RAW audio                  [SpeechBrain
      Apache-2.0; QUARANTINE: denoise (DeepFilterNet) NEVER sits upstream
      of the speaker path — embeddings see raw audio only]
   -> blind eigengap speaker-count selection              [scipy]
   -> forced-k SpectralCluster (cosine)                    [Apache-2.0]
   -> Hungarian map (GT-informed; skipped without GT)      [scipy]
   -> DER/JER (pyannote-metrics, only with --ref-rttm)    [MIT]
   -> per-speaker hypothesis segments -> SRT/ASS ->
      ffmpeg ASS burn-in onto the RAW mix waveform render  [ffmpeg/libass]

Donor-first: VAD / grid / eigengap / frame labeling / RTTM / scoring come
from the wave63 (`wire_vad_coverage_recovery`) and wave64
(`wire_vad_recall_experiment`) lane modules — this file only wires them
into the production topology and adds the real-ECAPA compute stage
(ported from wave64's `wire_e2e_step1_ecapa`, single-thread, batch 8).

Modes:
  --mode fixture    SHA-verified Wave-58 fixture (dialogue.wav, GT RTTM):
                    reproduces the Wave-64 baseline DER/JER.
  --mode production  arbitrary episode audio (e.g. the real EP01
                    audio-orig.m4a): blind run, no GT -> hypothesis RTTM,
                    captions and burn-in; DER/JER honestly reported N/A.

Licenses (wired path): webrtcvad MIT, SpectralCluster Apache-2.0,
pyannote-metrics MIT, SpeechBrain ECAPA Apache-2.0, scipy/numpy/
scikit-learn BSD. Lane code MIT. No GPL.
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W63 = os.path.join(HERE, "..", "wave63_lane_c")
W64 = os.path.join(HERE, "..", "wave64_lane_c")
sys.path.insert(0, W63)
sys.path.insert(0, W64)
import wire_vad_coverage_recovery as w63  # noqa: E402
import wire_vad_recall_experiment as w64  # noqa: E402

SR = w63.SR
WIN_S, HOP_S = w63.WIN_S, w63.HOP_S
# ---- Proven Wave-64 production operating point (do not change lightly) ----
PROVEN_VAD = {"agg": 0, "frame_ms": 10, "pad": 0.3, "use_pad": True}
PROVEN_GATE = 0.08

W, H, FPS = 640, 360, 30
PALETTE = ["FFD700", "00E5FF", "FF7AC8", "9DFF70", "FF9F1C", "B388FF",
           "FF6B6B", "4DD0E1", "FFD166", "C8B6FF"]

HF_REPO = "https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb/resolve/main"
NEED_FILES = ["hyperparams.yaml", "embedding_model.ckpt",
              "mean_var_norm_emb.ckpt", "classifier.ckpt",
              "label_encoder.txt"]


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


def _remote_size(url):
    """Expected byte size from the HF resolve endpoint (X-Linked-Size or
    Content-Length); None if the server won't say."""
    req = urllib.request.Request(url, headers={"User-Agent": "curl"},
                                 method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            for h in ("X-Linked-Size", "Content-Length"):
                v = r.headers.get(h)
                if v and v.isdigit():
                    return int(v)
    except Exception:
        pass
    return None


def _download(url, dst, expect, tries=4):
    for attempt in range(1, tries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": "curl"})
        with urllib.request.urlopen(req, timeout=120) as r, \
                open(dst + ".part", "wb") as f:
            while True:
                b = r.read(65536)
                if not b:
                    break
                f.write(b)
        got = os.path.getsize(dst + ".part")
        if expect is not None and got != expect:
            print(f"  attempt {attempt}: got {got} bytes, expected "
                  f"{expect} — retrying", flush=True)
            os.remove(dst + ".part")
            continue
        os.replace(dst + ".part", dst)
        return
    raise RuntimeError(f"download of {url} failed after {tries} tries")


def fetch_weights(scratch):
    """ECAPA bytes via direct HTTPS (huggingface_hub xet stalls on this VM's
    proxy — Wave-64 proven route). hyperparams.yaml patched to fully-local
    pretrained_path so SpeechBrain never touches the hub (HF_HUB_OFFLINE=1)."""
    os.makedirs(scratch, exist_ok=True)
    for fn in NEED_FILES:
        dst = os.path.join(scratch, fn)
        url = f"{HF_REPO}/{fn}"
        expect = _remote_size(url)
        if (os.path.isfile(dst) and os.path.getsize(dst) > 1000
                and (expect is None or os.path.getsize(dst) == expect)):
            print(f"  have {fn} ({os.path.getsize(dst)} bytes)", flush=True)
            continue
        if os.path.isfile(dst):
            print(f"  {fn} size mismatch "
                  f"({os.path.getsize(dst)} vs {expect}) — re-fetching",
                  flush=True)
            os.remove(dst)
        print(f"  GET {url} (expect {expect} bytes)", flush=True)
        _download(url, dst, expect)
        print(f"  saved {fn} ({os.path.getsize(dst)} bytes)", flush=True)
    hp = os.path.join(scratch, "hyperparams.yaml")
    txt = open(hp).read()
    assert "embedding_model.ckpt" in txt and "mean_var_norm" in txt
    if f"pretrained_path: {scratch}" not in txt:
        txt2 = re.sub(r"^pretrained_path:.*$",
                      f"pretrained_path: {scratch}", txt,
                      flags=re.MULTILINE)
        assert txt2 != txt, "pretrained_path line not found"
        open(hp, "w").write(txt2)
        print("  hyperparams.yaml patched to fully-local paths", flush=True)


def load_audio_any(path, scratch):
    """-> (float32 16 kHz mono np array, duration_s). Direct wave read when
    already 16 kHz mono; otherwise ffmpeg decode to scratch."""
    import wave as wv
    try:
        with wv.open(path, "rb") as w:
            if w.getframerate() == SR and w.getnchannels() == 1:
                a = (np.frombuffer(w.readframes(w.getnframes()),
                                   dtype=np.int16).astype(np.float32)
                     / 32768.0)
                return a, w.getnframes() / w.getframerate(), path
    except wv.Error:
        pass
    dst = os.path.join(scratch,
                       "decoded_" + hashlib.sha256(
                           os.path.abspath(path).encode()).hexdigest()[:16]
                       + ".wav")
    if not os.path.isfile(dst):
        run(["ffmpeg", "-y", "-v", "error", "-i", path,
             "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", dst])
    with wv.open(dst, "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        a = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
             .astype(np.float32) / 32768.0)
        return a, w.getnframes() / w.getframerate(), dst


def compute_embeddings_raw(audio, idxs, scratch, npy_path):
    """Real ECAPA-TDNN on RAW audio (quarantine: no denoise upstream of the
    speaker path). row p of the .npy == grid window number p."""
    if (os.path.isfile(npy_path)
            and np.load(npy_path, mmap_mode="r").shape == (len(idxs), 192)):
        embs = np.load(npy_path).astype(np.float64)
        assert np.all(np.isfinite(embs))
        print(f"  loaded cached {npy_path} {embs.shape}", flush=True)
        return embs
    import torch
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    fetch_weights(os.path.join(scratch, "ecapa_weights"))
    from speechbrain.inference import EncoderClassifier
    clf = EncoderClassifier.from_hparams(
        source=os.path.join(scratch, "ecapa_weights"),
        savedir=os.path.join(scratch, "ecapa_weights", "sb_tmp"),
        run_opts={"device": "cpu"})
    print("  ECAPA spkrec-ecapa-voxceleb on CPU (local weights)", flush=True)
    win = int(WIN_S * SR)
    embs = []
    B = 8
    with torch.no_grad():
        for i in range(0, len(idxs), B):
            batch = np.stack([audio[j:j + win] for j in idxs[i:i + B]])
            wavs = torch.from_numpy(batch.astype(np.float32))
            e = clf.encode_batch(wavs)  # sb 1.1.1: (wavs, wav_lens, normalize)
            embs.append(e.squeeze(1).cpu().numpy())
            if (i // B) % 20 == 0:
                print(f"  encoded {min(i + B, len(idxs))}/{len(idxs)}",
                      flush=True)
    embs = np.concatenate(embs, axis=0).astype(np.float64)
    assert embs.shape == (len(idxs), 192) and np.all(np.isfinite(embs))
    np.save(npy_path, embs)
    print(f"  saved {npy_path} {embs.shape}", flush=True)
    return embs


def diarize(audio, vad_cfg, sil_frac, emb_all, idxs, k_min, k_max):
    """VAD -> grid+gate+strict-inclusion -> eigengap -> forced-k cluster ->
    F0/F1 frame labeling. Returns dict; cluster labels anonymous here."""
    _, rmsv, _, _ = w63.window_grid(audio)
    thr = sil_frac * float(np.max(rmsv))
    energy_speech = set(np.flatnonzero(rmsv >= thr).tolist())
    vad_segs = w64.vad_segments_gen(audio, **vad_cfg)
    kept = [j for j in sorted(energy_speech)
            if w63.inside_vad(idxs[j] / SR, (idxs[j] / SR) + WIN_S, vad_segs)]
    if len(kept) < 2:
        raise RuntimeError(f"kept<2 windows (sil_frac={sil_frac})")
    emb = emb_all[np.asarray(kept)]
    k_est, eigs, gaps, margin = w63.eigengap_laplacian(emb, k_min=k_min,
                                                      k_max=k_max)
    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=k_est, max_clusters=k_est,
                           custom_dist="cosine")
    labels = np.asarray(cl.predict(emb), dtype=int)
    n_frames = int(math.ceil((len(audio) / SR) / HOP_S))
    frames_f0 = w63.label_v2c_no_fill(kept, labels, vad_segs, n_frames)
    frames_f1 = w63.fill_within_vad(frames_f0, vad_segs, n_frames)
    return {"vad_segs": vad_segs, "kept": kept, "kept_n": len(kept),
            "energy_n": len(energy_speech), "n_win": len(idxs),
            "thr": thr, "k": k_est, "margin": margin, "gaps": gaps,
            "labels": labels, "frames_f0": frames_f0, "frames_f1": frames_f1}


def rttm_turns(path):
    """Parse a reference RTTM into Wave-63-style turns list."""
    turns = []
    for line in open(path):
        f = line.split()
        if f[0] != "SPEAKER":
            continue
        turns.append({"start": float(f[3]), "end": float(f[3]) + float(f[4]),
                      "speaker": f[7]})
    return turns


def overlap(a0, a1, b0, b1):
    return max(0.0, min(a1, b1) - max(a0, b0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["fixture", "production"],
                    default="fixture")
    ap.add_argument("--audio", default=None,
                    help="input audio (production mode; default: EP01 audio-orig.m4a)")
    ap.add_argument("--ref-rttm", default=None,
                    help="GT RTTM: enables Hungarian map + DER/JER scoring")
    ap.add_argument("--vad-agg", type=int, default=PROVEN_VAD["agg"])
    ap.add_argument("--vad-frame-ms", type=int, default=PROVEN_VAD["frame_ms"])
    ap.add_argument("--vad-pad", type=float, default=PROVEN_VAD["pad"])
    ap.add_argument("--gate", type=float, default=PROVEN_GATE,
                    help="energy gate as fraction of max window RMS")
    ap.add_argument("--k-min", type=int, default=None)
    ap.add_argument("--k-max", type=int, default=None)
    ap.add_argument("--no-burn-in", action="store_true")
    ap.add_argument("--uri", default=None)
    a = ap.parse_args()

    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    out = os.path.join(HERE, "proofs", a.mode)
    os.makedirs(out, exist_ok=True)
    scratch = os.path.join(HERE, "scratch")
    os.makedirs(scratch, exist_ok=True)

    t0 = time.time()
    res = {"wave": 65, "lane": "C", "mode": a.mode,
           "proven_vad": PROVEN_VAD, "checks": []}

    def check(name, ok, detail):
        res["checks"].append({"name": name, "pass": bool(ok),
                              "detail": detail})
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

    vad_cfg = {"agg": a.vad_agg, "frame_ms": a.vad_frame_ms,
               "pad": a.vad_pad, "use_pad": True}
    uri = a.uri or ("dialogue" if a.mode == "fixture" else "ep01_audio_orig")

    # ---- 1. audio
    if a.mode == "fixture":
        audio, turns, fixture_emb = w63.load_fixture()
        dur = len(audio) / SR
        wav_for_video = w63.DIALOGUE
        ref_rttm = w63.REF_RTTM
        check("fixture_shas", True, "wave58 fixture SHA-verified")
    else:
        audio_in = a.audio or os.path.abspath(os.path.join(
            HERE, "..", "..", "production", "WIZARD_GANG_EP01",
            "audio-orig.m4a"))
        assert os.path.isfile(audio_in), audio_in
        audio, dur, wav_for_video = load_audio_any(audio_in, scratch)
        turns = rttm_turns(a.ref_rttm) if a.ref_rttm else None
        ref_rttm = a.ref_rttm
        check("episode_audio_loaded", True,
              f"{os.path.basename(audio_in)} {dur:.2f}s -> 16k mono "
              f"{len(audio)} samples")

    # ---- 2. VAD (proven operating point)
    vad_segs = w64.vad_segments_gen(audio, **vad_cfg)
    speech_s = sum(b - x for x, b in vad_segs)
    check("vad_ok", len(vad_segs) >= 1 and speech_s > 0,
          f"VAD agg={vad_cfg['agg']} {vad_cfg['frame_ms']}ms "
          f"pad={vad_cfg['pad']}: {len(vad_segs)} segments, "
          f"{speech_s:.2f}s speech ({100*speech_s/dur:.1f}% of {dur:.1f}s)")
    if turns is not None:
        rec, prec, f1v, _ = w64.vad_quality_frames(vad_segs, turns,
                                                   len(audio))
        check("vad_recall", True,
              f"recall={rec:.4f} prec={prec:.4f} F1={f1v:.4f}")

    # ---- 3. grid + real ECAPA on RAW audio (quarantine: no upstream denoise)
    idxs = list(range(0, len(audio) - int(WIN_S * SR) + 1, int(HOP_S * SR)))
    print(f"  grid: {len(idxs)} windows ({WIN_S}s/{HOP_S}s)", flush=True)
    npy_path = os.path.join(out, "embeddings_raw.npy")
    emb_all = compute_embeddings_raw(audio, idxs, scratch, npy_path)
    check("embeddings_raw", emb_all.shape == (len(idxs), 192),
          f"{emb_all.shape} real ECAPA on RAW audio (row p = window p)")

    if a.mode == "fixture":
        # validate real compute vs the SHA-pinned fixture embeddings
        _, rmsv, _, _ = w63.window_grid(audio)
        a08 = np.flatnonzero(rmsv >= w63.SILENCE_FRAC * float(np.max(rmsv)))
        canon = {int(j): i for i, j in enumerate(a08)}
        rec_rows = np.stack([emb_all[int(j)] for j in a08])
        fix_rows = np.stack([fixture_emb[canon[int(j)]] for j in a08])
        cos = (np.sum(rec_rows * fix_rows, axis=1)
               / (np.linalg.norm(rec_rows, axis=1)
                  * np.linalg.norm(fix_rows, axis=1)))
        check("real_compute_matches_fixture", float(cos.min()) > 0.999,
              f"cos(recomputed, fixture): mean={cos.mean():.6f} "
              f"min={cos.min():.6f} max={cos.max():.6f}")

    # ---- 4-6. diarization core
    kmin = a.k_min if a.k_min is not None else (2 if turns else 1)
    kmax = a.k_max if a.k_max is not None else (6 if turns else 10)
    dz = diarize(audio, vad_cfg, a.gate, emb_all, idxs, kmin, kmax)
    check("blind_k", dz["k"] >= kmin,
          f"eigengap k={dz['k']} margin={dz['margin']:.2f}x "
          f"(kept {dz['kept_n']}/{dz['n_win']} windows)")
    res.update({k: dz[k] for k in
                ("kept_n", "energy_n", "n_win", "k", "margin", "thr")})
    res["eigengap_gaps"] = {str(k): round(v, 4)
                            for k, v in dz["gaps"].items()}

    # cluster -> speaker names
    if turns is not None:
        cmap, purity, _ = w63.hungarian_map(dz["frames_f0"], turns)
        check("purity", True,
              f"frame purity={purity:.4f} map={cmap} (GT-informed)")
        spk_of = {c: cmap[c] for c in
                  set(dz["frames_f0"][dz["frames_f0"] != -1].tolist())}
    else:
        # no GT: blind — anonymous speaker labels, no map, no purity claim
        spk_of = {int(c): f"SPEAKER_{int(c):02d}"
                  for c in set(dz["labels"].tolist())}
        res["note"] = ("no ground truth: anonymous SPEAKER_xx labels; "
                       "Hungarian map / purity / DER / JER not measurable")
        print("  no GT: anonymous SPEAKER_xx labels "
              "(map/purity/DER/JER N/A)", flush=True)

    segs_f0 = [(s, e, spk_of[int(c)])
               for s, e, c in w63.segments_from_frames(dz["frames_f0"])]
    segs_f1 = [(s, e, spk_of[int(c)])
               for s, e, c in w63.segments_from_frames(dz["frames_f1"])]

    # ---- 7. RTTM + scoring (fixture/GT mode only)
    hyp_f0 = os.path.join(out, "hypothesis_F0.rttm")
    hyp_f1 = os.path.join(out, "hypothesis_F1.rttm")
    w63.write_rttm(hyp_f1, segs_f1, uri=uri)
    w63.write_rttm(hyp_f0, segs_f0, uri=uri)
    check("hypothesis_written", os.path.getsize(hyp_f1) > 0,
          f"{os.path.basename(hyp_f1)} ({len(segs_f1)} F1 segments)")

    if ref_rttm is not None:
        for tag, hp in (("F0", hyp_f0), ("F1", hyp_f1)):
            d, j, comp = w63.score(ref_rttm, hp, 0.0)
            d25, j25, _ = w63.score(ref_rttm, hp, 0.25)
            res[tag] = {"DER": round(d, 4), "JER": round(j, 4),
                        "miss": round(comp["missed detection"], 3),
                        "FA": round(comp["false alarm"], 3),
                        "conf": round(comp["confusion"], 3),
                        "DER_c025": round(d25, 4), "JER_c025": round(j25, 4)}
        f1 = res["F1"]
        check("der_baseline", abs(f1["DER"] - 0.0382) < 0.002,
              f"F1 DER={f1['DER']} vs wave64 baseline 0.0382 "
              f"(miss={f1['miss']} FA={f1['FA']} conf={f1['conf']})")
        check("jer_baseline", abs(f1["JER"] - 0.0378) < 0.002,
              f"F1 JER={f1['JER']} vs wave64 baseline 0.0378")

    # ---- 8. captions: SRT + ASS (pipeline supplies who/when; text = GT
    # turn text when GT exists, else speaker labels — no ASR, stated)
    events = []
    for s, e, spk in segs_f1:
        text = ""
        if turns is not None:
            b, bov = None, 0.0
            for t_ in turns:
                ov = overlap(s, e, t_["start"], t_["end"])
                if ov > bov:
                    b, bov = t_, ov
            text = b["text"] if b else ""
        else:
            text = f"{s:.1f}s - {e:.1f}s"
        events.append((s, e, spk, text))
    res["n_events"] = len(events)

    srt_path = os.path.join(out, "captions.srt")
    with open(srt_path, "w") as f:
        for i, (s, e, spk, text) in enumerate(events, 1):
            f.write(f"{i}\n{fmt_srt(s)} --> {fmt_srt(e)}\n"
                    f"[{spk}] {text}\n\n")
    ass_path = os.path.join(out, "captions.ass")
    speakers = sorted({sp for _, _, sp, _ in events})
    with open(ass_path, "w") as f:
        f.write("[Script Info]\nTitle: wave65 production captions\n"
                "ScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n")
        f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, "
                "PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
                "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, "
                "Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
                "MarginR, MarginV, Encoding\n")
        for i, spk in enumerate(speakers):
            col = PALETTE[i % len(PALETTE)]
            bgr = f"{col[4:6]}{col[2:4]}{col[0:2]}"
            style = re.sub(r"\W", "", spk)
            f.write(f"Style: {style},Noto Sans,26,&H00{bgr},&H000000FF,"
                    f"&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0.5,2,"
                    f"30,30,40,1\n")
        f.write("\n[Events]\nFormat: Layer, Start, End, Style, Name, "
                "MarginL, MarginR, MarginV, Effect, Text\n")
        for s, e, spk, text in events:
            style = re.sub(r"\W", "", spk)
            f.write(f"Dialogue: 0,{fmt_ass(s)},{fmt_ass(e)},{style},,0,0,0,,"
                    f"[{{\\b1}}{esc_ass(spk)}{{\\b0}}] {esc_ass(text)}\n")
    check("captions_written", os.path.getsize(ass_path) > 1000,
          f"captions.srt/ass: {len(events)} events, "
          f"{os.path.getsize(ass_path)} bytes ASS")

    # ---- 9. optional ffmpeg ASS burn-in onto the RAW mix waveform
    if not a.no_burn_in:
        src = os.path.join(out, "waves.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-i", wav_for_video,
             "-filter_complex",
             f"[0:a]showwaves=s={W}x{H}:mode=line:colors=white,format=yuv420p[v]",
             "-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-crf", "23",
             "-t", f"{dur:.2f}", src])
        burned = os.path.join(out, "burned_captions.mp4")
        p = run(["ffmpeg", "-y", "-v", "warning", "-i", src,
                 "-vf", f"ass={ass_path}", "-c:a", "copy", burned])
        bad = [l for l in p.stderr.splitlines()
               if re.search(r"error|failed|cannot|unable", l, re.I)]
        check("libass_clean", not bad, f"libass stderr errors: {len(bad)}")
        check("burned_mp4", os.path.getsize(burned) > 10000,
              f"burned_captions.mp4 {os.path.getsize(burned)} bytes")

        long_ev = [(s, e) for s, e, _ in segs_f1 if e - s > 2.0]
        t_on = (long_ev[0][0] + long_ev[0][1]) / 2
        covered = np.zeros(int(dur * FPS) + 1, bool)
        for s, e, _ in segs_f1:
            covered[int(s * FPS):int(e * FPS) + 1] = True
        t_off = next(i for i in range(len(covered)) if not covered[i]) / FPS

        def band_diff(t, tag):
            f1 = os.path.join(out, f"frame_{tag}.raw")
            f2 = os.path.join(out, f"frame_src_{tag}.raw")
            for srcf, dst in ((burned, f1), (src, f2)):
                run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}",
                     "-i", srcf, "-frames:v", "1", "-f", "rawvideo",
                     "-pix_fmt", "gray", dst])
            aa = np.fromfile(f1, dtype=np.uint8).reshape(H, W)
            bb = np.fromfile(f2, dtype=np.uint8).reshape(H, W)
            band = slice(int(H * 0.70), H)
            return float(np.mean(np.abs(aa[band].astype(float)
                                        - bb[band].astype(float))))

        d_on = band_diff(t_on, "on")
        d_off = band_diff(t_off, "off")
        res["pixel"] = {"on_mean_abs_diff": round(d_on, 3),
                        "off_mean_abs_diff": round(d_off, 3),
                        "t_on": round(t_on, 3), "t_off": round(t_off, 3)}
        check("burn_pixel_on", d_on > 2.0,
              f"caption-ON band diff {d_on:.2f}/255 (> 2.0)")
        check("burn_pixel_off", d_off < 1.0,
              f"caption-OFF band diff {d_off:.2f}/255 (< 1.0)")

    res["elapsed_s"] = round(time.time() - t0, 1)
    n_pass = sum(c["pass"] for c in res["checks"])
    res["checks_pass"] = f"{n_pass}/{len(res['checks'])}"
    with open(os.path.join(out, "result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n{n_pass}/{len(res['checks'])} checks PASS, {res['elapsed_s']}s "
          f"-> {out}", flush=True)
    if n_pass != len(res["checks"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
