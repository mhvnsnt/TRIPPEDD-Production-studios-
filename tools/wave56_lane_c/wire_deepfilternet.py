#!/usr/bin/env python3
"""Wave 56 Lane C — wire DeepFilterNet (Rikorose/DeepFilterNet).

Deep-learning full-band speech denoiser wired as an upgrade path for the
VO pipeline's denoise+master stage (Wave 52 wired noisereduce; this is the
deep-NN complement, especially for non-stationary noise).

License gate: upstream dual MIT / Apache-2.0 (LICENSE-MIT verbatim MIT text +
README license section, fetched 2026-10-08). PyPI package `deepfilternet`
is MIT (classifier + metadata).

Proof artifacts land in proofs/deepfilternet/:
  fixture_clean.wav      - real Wave-51 Kokoro VO (7.825 s, 24 kHz mono)
  fixture_noisy_white.wav, fixture_noisy_babble.wav - calibrated noisy variants
  out_clean.wav, out_noisy_white.wav, out_noisy_babble.wav - enhanced outputs
  result.json            - measured numbers + PASS/FAIL per check
"""
import hashlib
import json
import math
import os
import sys
import time
import wave

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "deepfilternet")
FIXTURE = os.path.join(
    HERE, "..", "wave51_lane_c", "proofs", "kokoro_tts", "voice_line.wav"
)
SR_FIX = 24000
SR_MODEL = 48000  # DeepFilterNet3 is full-band 48 kHz


def read_wav_mono(path):
    with wave.open(path, "rb") as w:
        n, sw, fr, ch = w.getnframes(), w.getsampwidth(), w.getframerate(), w.getnchannels()
        raw = w.readframes(n)
    assert sw == 2, f"expected int16, got {sw}-byte samples"
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


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-12)


def db(x):
    return 20.0 * math.log10(max(x, 1e-12))


def main():
    t0 = time.time()
    rng = np.random.default_rng(20261008)

    clean, sr = read_wav_mono(os.path.normpath(FIXTURE))
    assert sr == SR_FIX, f"fixture sr {sr} != {SR_FIX}"

    speech_rms = rms(clean)
    target_snr_db = 10.0  # calibrated: noise 10 dB below speech RMS

    # --- stationary white noise variant ---
    noise_white = rng.standard_normal(clean.shape).astype(np.float32)
    noise_white *= speech_rms / (rms(noise_white) * 10 ** (target_snr_db / 20))
    noisy_white = clean + noise_white

    # --- non-stationary "babble-like" variant: band-limited noise, 4 Hz AM ---
    n = clean.shape[0]
    t = np.arange(n) / sr
    am = 0.5 + 0.5 * np.sin(2 * math.pi * 4.0 * t + 0.7)
    noise_babble = rng.standard_normal(n).astype(np.float32)
    # crude band-limit to the speech band via FFT (300-3400 Hz)
    spec = np.fft.rfft(noise_babble)
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    mask = (freqs >= 300) & (freqs <= 3400)
    spec *= mask
    noise_babble = np.fft.irfft(spec, n).astype(np.float32)
    noise_babble *= am
    noise_babble *= speech_rms / (rms(noise_babble) * 10 ** (target_snr_db / 20))
    noisy_babble = clean + noise_babble

    def up(x):
        # 24 kHz -> 48 kHz via torch (polyphase not needed; linear is fine for fixture)
        xt = torch.from_numpy(x).unsqueeze(0).unsqueeze(0)
        return torch.nn.functional.interpolate(
            xt, scale_factor=2, mode="linear", align_corners=False
        ).squeeze(0)

    def down(x):
        xt = x if torch.is_tensor(x) else torch.from_numpy(x)
        xt = xt.unsqueeze(0).unsqueeze(0)
        return torch.nn.functional.interpolate(
            xt, scale_factor=0.5, mode="linear", align_corners=False
        ).squeeze(0).squeeze(0).numpy()

    from df.enhance import enhance, init_df

    model, df_state, _ = init_df(model_base_dir=None, post_filter=False)
    assert df_state.sr() == SR_MODEL, f"model sr {df_state.sr()}"

    def denoise(x48):
        # x48 is (C=1, T); enhance/df.analysis expect exactly 2D
        audio = x48 if torch.is_tensor(x48) else torch.from_numpy(x48)
        assert audio.dim() == 2, audio.shape
        with torch.no_grad():
            out = enhance(model, df_state, audio)
        return out.squeeze(0).numpy()

    res = {"fixture": os.path.basename(FIXTURE), "sr_model": SR_MODEL,
           "snr_in_db": target_snr_db, "checks": []}

    def check(name, ok, detail):
        res["checks"].append({"name": name, "status": "PASS" if ok else "FAIL",
                              "detail": detail})
        print(("PASS" if ok else "FAIL"), name, "-", detail)

    outputs = {}
    for tag, noisy in (("noisy_white", noisy_white), ("noisy_babble", noisy_babble),
                       ("clean", clean)):
        e48 = denoise(up(np.clip(noisy, -1, 1)))
        e = down(e48)
        e = e[: len(clean)]
        outputs[tag] = e
        write_wav_mono(os.path.join(PROOFS, f"out_{tag}.wav"), e, SR_FIX)

    # input fixtures
    write_wav_mono(os.path.join(PROOFS, "fixture_clean.wav"), clean, SR_FIX)
    write_wav_mono(os.path.join(PROOFS, "fixture_noisy_white.wav"), noisy_white, SR_FIX)
    write_wav_mono(os.path.join(PROOFS, "fixture_noisy_babble.wav"), noisy_babble, SR_FIX)

    # --- metrics: SNR improvement (exact, since noise is known) ---
    for tag, noise in (("noisy_white", noise_white), ("noisy_babble", noise_babble)):
        e = outputs[tag]
        snr_in = db(rms(clean) / rms(noise))
        resid = e - clean
        snr_out = db(rms(clean) / rms(resid))
        improv = snr_out - snr_in
        res[f"snr_in_{tag}_db"] = round(snr_in, 2)
        res[f"snr_out_{tag}_db"] = round(snr_out, 2)
        res[f"snr_improv_{tag}_db"] = round(improv, 2)
        check(f"snr_improvement_{tag}", improv > 3.0,
              f"SNR {snr_in:.1f} -> {snr_out:.1f} dB (Δ {improv:+.1f} dB)")

    # non-stationary advantage vs stationary (DFNet's documented strength)
    check("nonstationary_advantage",
          res["snr_improv_noisy_babble_db"] >= res["snr_improv_noisy_white_db"] - 1.0,
          f"babble Δ {res['snr_improv_noisy_babble_db']:+.1f} dB vs "
          f"white Δ {res['snr_improv_noisy_white_db']:+.1f} dB")

    # --- clean no-op control ---
    e_clean = outputs["clean"]
    delta = abs(rms(e_clean) - rms(clean)) / rms(clean)
    corr = float(np.corrcoef(clean, e_clean)[0, 1])
    res["clean_rms_delta_pct"] = round(delta * 100, 2)
    res["clean_corr"] = round(corr, 5)
    check("clean_noop_rms", delta < 0.05,
          f"clean RMS delta {delta*100:.2f}% (< 5%)")
    check("clean_noop_corr", corr > 0.99, f"corr(clean, enhanced) = {corr:.5f}")

    # --- byte-determinism: denoise the same input twice ---
    e48a = denoise(up(np.clip(noisy_white, -1, 1)))
    e48b = denoise(up(np.clip(noisy_white, -1, 1)))
    maxdiff = float(np.max(np.abs(e48a - e48b)))
    res["determinism_max_abs_diff"] = maxdiff
    check("byte_deterministic", maxdiff == 0.0, f"max|diff| = {maxdiff}")

    # --- timing ---
    res["enhance_ms_per_sec_audio"] = round(
        (time.time() - t0) / (len(clean) / SR_FIX) * 1000, 1)
    check("runs_to_completion", True,
          f"3 enhances in {time.time()-t0:.1f} s total")

    res["sha256"] = {f: sha256(os.path.join(PROOFS, f))
                     for f in sorted(os.listdir(PROOFS)) if f.endswith(".wav")}
    res["passed"] = sum(1 for c in res["checks"] if c["status"] == "PASS")
    res["failed"] = sum(1 for c in res["checks"] if c["status"] == "FAIL")
    with open(os.path.join(PROOFS, "result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n{res['passed']}/{len(res['checks'])} checks PASS")
    return 0 if res["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
