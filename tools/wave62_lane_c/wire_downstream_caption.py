#!/usr/bin/env python3
"""Wave 62 Lane C — DOWNSTREAM denoise (the production-rule-compliant path).

DeepFilterNet3 is applied ONLY to the per-speaker output segments AFTER
clustering/diarization — never to the embedding input. This script:

  1. Loads the MAIN (production-topology) hypothesis RTTM
     (hypothesis_main_clean.rttm — speaker identity + timing from the
     denoise-free speaker path).
  2. Cuts per-speaker audio from RAW fixture audio on those boundaries,
     denoises each speaker channel with DeepFilterNet3, saves
     denoised_spk_<A|B|C>.wav, and mixes down to downstream_denoised_mix.wav.
  3. Diagnostics (GT-informed, labeled as such): SNR/no-op stats on clean,
     and SNR gain of downstream denoise on a seeded 10 dB-noise-injected
     copy of the per-speaker segments (the caption-path value case);
     GT-mean cosine separation on a fresh ECAPA pass over the
     downstream-denoised mix (shows the denoise effect is real but
     quarantined downstream — diarization already happened upstream).
  4. Caption burn-in (Wave-61 donor pattern): hypothesis RTTM timing +
     speaker, GT turn TEXTS (words; no ASR stage wired — documented),
     SRT + per-speaker-color ASS burned onto a waveform render of the
     DOWNSTREAM-DENOISED MIX, pixel ON/OFF verified (Wave-50 method).

Nothing here touches the embedding input. The speaker path is unaffected.
"""
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "proofs", "rebuilt_pipeline")
PROOFS = os.path.join(HERE, "proofs", "downstream")
os.makedirs(PROOFS, exist_ok=True)

W58 = os.path.join(HERE, "..", "wave58_lane_c", "proofs",
                   "real_voice_diarization")
FIXTURE = os.path.join(W58, "dialogue.wav")
GT_PATH = os.path.join(W58, "ground_truth.json")
HYP_RTTM = os.path.join(PIPE, "hypothesis_main_clean.rttm")
SCRATCH = os.path.join(HERE, "scratch")

SR = 16000
SR_MODEL = 48000
SNR_IN_DB = 10.0
RNG_SEED = 20261008
W, H, FPS = 640, 360, 30
COLORS = {"A": "FFD700", "B": "00E5FF", "C": "FF7AC8"}


def read_wav_mono(path):
    with wave.open(path, "rb") as w:
        n, sw, fr, ch = (w.getnframes(), w.getsampwidth(),
                         w.getframerate(), w.getnchannels())
        raw = w.readframes(n)
    assert sw == 2
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x, fr


def write_wav_mono(path, x, sr):
    x = np.clip(x, -1.0, 1.0)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767.0).astype(np.int16).tobytes())


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-12)


def db(x):
    return 20.0 * math.log10(max(x, 1e-12))


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\n{p.stderr[-2000:]}")
    return p


def init_denoiser():
    # torchaudio 2.x removed torchaudio.backend.common; df.io only needs the
    # AudioMetaData dataclass at import time, so inject a shim BEFORE
    # importing df.enhance (never `import torchaudio.backend` — it does not
    # exist in this torchaudio version).
    if "torchaudio.backend.common" not in sys.modules:
        import types
        from dataclasses import dataclass
        mod = types.ModuleType("torchaudio.backend.common")

        @dataclass
        class AudioMetaData:
            sample_rate: int
            num_frames: int
            num_channels: int
            bits_per_sample: int
            encoding: str

        mod.AudioMetaData = AudioMetaData
        sys.modules["torchaudio.backend.common"] = mod
    from df.enhance import enhance, init_df
    model, df_state, _ = init_df(model_base_dir=None, post_filter=False)
    assert df_state.sr() == SR_MODEL
    return model, df_state, enhance


def resample(x, sr_in, sr_out):
    import torch
    import torchaudio.functional as TAF
    xt = torch.from_numpy(np.asarray(x, dtype=np.float32)).unsqueeze(0)
    return TAF.resample(xt, sr_in, sr_out).squeeze(0)


def denoise(model, df_state, enhance, x16):
    import torch
    with torch.no_grad():
        x48 = resample(np.clip(x16, -1, 1), SR, SR_MODEL).unsqueeze(0)
        out = enhance(model, df_state, x48)
    e48 = out.squeeze(0).numpy()
    e16 = resample(e48, SR_MODEL, SR).numpy()
    return e16[:len(x16)]


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

    raw, sr = read_wav_mono(FIXTURE)
    assert sr == SR
    turns = json.load(open(GT_PATH))["turns"]
    hyp = load_rttm(HYP_RTTM)
    check("hypothesis_present", len(hyp) >= 9,
          f"{len(hyp)} hypothesis events in main_clean RTTM")
    check("hyp_speakers", {s for _, _, s in hyp} == {"A", "B", "C"},
          f"hypothesis covers speakers {sorted({s for _, _, s in hyp})}")

    # ---- 1. per-speaker channels from RAW audio on hypothesis boundaries ----
    t = time.time()
    channels = {}
    for s, e, spk in hyp:
        seg = raw[int(s * SR):int(e * SR)]
        channels.setdefault(spk, []).append(seg)
    raw_ch = {spk: np.concatenate(chs) for spk, chs in channels.items()}
    res["per_speaker_raw_s"] = {k: round(len(vv) / SR, 2)
                                for k, vv in raw_ch.items()}
    print(f"  per-speaker raw durations: {res['per_speaker_raw_s']}")

    # ---- 2. downstream denoise: each speaker channel separately ----
    # --resume: reuse the denoised wavs from the earlier (SIGKILLED) run so
    # the DeepFilterNet3 model is never loaded alongside SpeechBrain ECAPA.
    RESUME = "--resume" in sys.argv
    RESUME_WAVS = [os.path.join(PROOFS, f"denoised_spk_{s}.wav")
                   for s in ("A", "B", "C")] + [
        os.path.join(PROOFS, "downstream_denoised_mix.wav"),
        os.path.join(PROOFS, "downstream_denoised_noisy_mix.wav")]
    if RESUME and all(os.path.isfile(p) and os.path.getsize(p) > 0
                      for p in RESUME_WAVS):
        print("  --resume: reusing denoised wavs from disk (no DF model)")
        den_ch = {s: read_wav_mono(os.path.join(
            PROOFS, f"denoised_spk_{s}.wav"))[0] for s in ("A", "B", "C")}
        mix = read_wav_mono(os.path.join(
            PROOFS, "downstream_denoised_mix.wav"))[0]
        mix_n = read_wav_mono(os.path.join(
            PROOFS, "downstream_denoised_noisy_mix.wav"))[0]
        res["denoise_s"] = "reused-from-disk"
    else:
        model, df_state, enhance = init_denoiser()
        den_ch = {}
        for spk in sorted(raw_ch):
            d = denoise(model, df_state, enhance, raw_ch[spk])
            den_ch[spk] = d
            write_wav_mono(os.path.join(PROOFS, f"denoised_spk_{spk}.wav"),
                           d, SR)
        res["denoise_s"] = round(time.time() - t, 1)

        # mix-down for the caption path (same event layout as hypothesis)
        mix = np.zeros(len(raw), dtype=np.float32)
        for s, e, spk in hyp:
            seg_len = int(e * SR) - int(s * SR)
            den_seg = denoise(model, df_state, enhance,
                              raw[int(s * SR):int(e * SR)])
            mix[int(s * SR):int(s * SR) + seg_len] += den_seg[:seg_len]
        write_wav_mono(os.path.join(PROOFS, "downstream_denoised_mix.wav"),
                       mix, SR)
    res["mix_sha256"] = sha256(os.path.join(
        PROOFS, "downstream_denoised_mix.wav"))

    # clean no-op stats (diagnostic; denoise should be ~transparent on clean)
    rdelta = abs(rms(mix) - rms(raw)) / rms(raw)
    corr = float(np.corrcoef(raw, mix)[0, 1])
    res["clean_noop_rms_delta_pct"] = round(rdelta * 100, 3)
    res["clean_noop_corr"] = round(corr, 5)
    check("downstream_clean_noop_rms", rdelta < 0.05,
          f"RMS delta {rdelta*100:.2f}% (< 5%)")
    check("downstream_clean_noop_corr", corr > 0.99,
          f"corr(raw, downstream-denoised mix) = {corr:.5f}")

    # ---- 3. value case: 10 dB noise injected, denoise on OUTPUT path ----
    rng = np.random.default_rng(RNG_SEED)
    speech_rms = rms(raw)
    noise = rng.standard_normal(raw.shape).astype(np.float32)
    noise *= speech_rms / (rms(noise) * 10 ** (SNR_IN_DB / 20))
    noisy_raw = np.clip(raw + noise, -1, 1)
    # per-speaker noisy segments on hypothesis boundaries, denoise each
    if not (RESUME and os.path.isfile(os.path.join(
            PROOFS, "downstream_denoised_noisy_mix.wav"))):
        mix_n = np.zeros(len(raw), dtype=np.float32)
        for s, e, spk in hyp:
            seg_len = int(e * SR) - int(s * SR)
            dseg = denoise(model, df_state, enhance,
                           noisy_raw[int(s * SR):int(e * SR)])
            mix_n[int(s * SR):int(s * SR) + seg_len] += dseg[:seg_len]
        write_wav_mono(os.path.join(
            PROOFS, "downstream_denoised_noisy_mix.wav"), mix_n, SR)
    snr_before = db(rms(raw) / rms(noisy_raw - raw))
    snr_after = db(rms(raw) / rms(mix_n - raw))
    gain = snr_after - snr_before
    res["noisy_downstream_snr"] = {"before_db": round(snr_before, 2),
                                  "after_db": round(snr_after, 2),
                                  "gain_db": round(gain, 2)}
    check("downstream_snr_gain", gain > 3.0,
          f"10 dB noisy -> downstream denoise {snr_before:.1f} -> "
          f"{snr_after:.1f} dB (Δ {gain:+.1f} dB) — value WITHOUT touching "
          "the speaker path")

    # ---- 4. quarantined-effect diagnostic: GT-mean cosine on a fresh ECAPA
    # pass over the downstream-denoised clean mix (GT-informed; diarization
    # already happened upstream, so any collapse is harmless).
    from speechbrain.inference import EncoderClassifier
    embedder = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=os.path.join(SCRATCH, "speechbrain_models"))
    import torch
    win = int(1.5 * SR)
    hop = int(0.25 * SR)
    idxs = list(range(0, len(mix) - win + 1, hop))
    batch = torch.stack([torch.from_numpy(mix[i:i + win]) for i in idxs])
    with torch.no_grad():
        emb = embedder.encode_batch(batch).squeeze(1).numpy()
    win_spk = [next((g["speaker"] for g in turns
                     if g["start"] <= i * 0.25 + 0.75 < g["end"]), None)
               for i in idxs]
    means = {}
    for s in ("A", "B", "C"):
        ix = [i for i, g in enumerate(win_spk) if g == s]
        m_ = emb[ix].mean(axis=0)
        means[s] = m_ / (np.linalg.norm(m_) + 1e-12)
    res["diag_cos_downstream_denoised"] = {
        f"{a}{b}": round(float(means[a] @ means[b]), 4)
        for a, b in (("A", "B"), ("A", "C"), ("B", "C"))}
    print(f"  downstream-denoised GT-mean cosine (diagnostic): "
          f"{res['diag_cos_downstream_denoised']}")

    # ---- 5. caption burn-in onto the downstream-denoised mix ----
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

    dur = len(mix) / SR
    den_wav = os.path.join(PROOFS, "downstream_denoised_mix.wav")
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
    json.dump(res, open(os.path.join(PROOFS, "result.json"), "w"), indent=2)
    print(f"\n{res['passed']}/{len(res['checks'])} checks PASS "
          f"in {res['total_s']} s")
    return 0 if res["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
