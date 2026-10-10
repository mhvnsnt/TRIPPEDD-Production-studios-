#!/usr/bin/env python3
# wire_audio_mastering.py — Wave 52 Lane C
# Voice-mastering chain for the cartoon VO pipeline:
#   Kokoro VO (Wave 51) -> noisereduce (MIT) -> pyloudnorm (MIT)
#       -> podcast master (-16 LUFS stereo) + broadcast master (-24 LUFS mono)
#
# License: MIT (this wire script). External libs invoked as deps, never embedded:
#   noisereduce  - MIT (github.com/timsainb/noisereduce, v3.0.3)
#   pyloudnorm   - MIT (github.com/csteinmetz1/pyloudnorm)
#   soundfile    - BSD-3-Clause (io dep)
# Loudness cross-check uses the ffmpeg `ebur128` filter (external binary, a
# second independent ITU-R BS.1770 implementation) purely as a measurement probe.
#
# Honest findings baked in as production rules:
#  * noisereduce stationary mode WITHOUT a noise profile treats program
#    material as noise (clean VO lost 70.6% RMS). Production rule: always
#    profile from silence/room tone; never run blind.
#  * Loudness gain must be computed on the FINAL channel layout (dual-mono
#    stereo reads +3 LU vs mono under BS.1770) — gain-after-upmix bug caught
#    and fixed during this wire-up.
#
# Run: tools/wave52_lane_c/venv/bin/python tools/wave52_lane_c/wire_audio_mastering.py
# Emits proofs into tools/wave52_lane_c/proofs/audio_mastering/.

import hashlib
import json
import math
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np
import soundfile as sf
from noisereduce import reduce_noise
import pyloudnorm as pyln

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IN_WAV = os.path.join(ROOT, "tools", "wave51_lane_c", "proofs", "kokoro_tts", "voice_line.wav")
OUT = os.path.join(HERE, "proofs", "audio_mastering")
os.makedirs(OUT, exist_ok=True)

PODCAST_TARGET = -16.0    # LUFS, stereo — podcast/platform delivery spec
BROADCAST_TARGET = -24.0  # LUFS, mono — broadcast spec
TRUE_PEAK_LIMIT = -1.0    # dBTP — safety ceiling on both masters
NOISE_DBFS = -40.0        # injected-noise level for the controlled denoise test

results = {"tool": "audio_mastering_chain", "wave": 52, "lane": "C",
           "utc": datetime.now(timezone.utc).isoformat(),
           "checks": [], "findings": [], "notes": []}


def check(name, ok, detail):
    results["checks"].append({"name": name, "pass": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + " — " + detail)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def ebur128(path):
    """Independent loudness measurement via ffmpeg's ebur128 filter."""
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path,
         "-filter_complex", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"],
        capture_output=True, text=True)
    txt = p.stderr
    m = {"raw_tail": txt[-400:] if txt else ""}
    for key, pat in (("integrated", r"I:\s+([-\d.]+)\s+LUFS"),
                     ("lra", r"LRA:\s+([-\d.]+)\s+LU"),
                     ("true_peak", r"Peak:\s+([-\d.]+)\s+dBFS")):
        mm = re.search(pat, txt)
        m[key] = float(mm.group(1)) if mm else None
    return m


def rms(x):
    return float(np.sqrt(np.mean(np.square(x))))


# ---------------------------------------------------------------- 1. load input
data, sr = sf.read(IN_WAV, dtype="float64")
n_frames = data.shape[0]
check("input_matches_wave51_vo",
      sr == 24000 and n_frames == 187800 and data.ndim == 1
      and abs(rms(data) - 0.0511) / 0.0511 < 0.05,
      "sr=%d frames=%d ch=1 rms=%.4f sha=%s"
      % (sr, n_frames, rms(data), sha256(IN_WAV)[:16]))
results["input"] = {"path": "tools/wave51_lane_c/proofs/kokoro_tts/voice_line.wav",
                    "sr": sr, "frames": n_frames, "rms": round(rms(data), 5),
                    "duration_s": round(n_frames / sr, 3)}

meter = pyln.Meter(sr)
pre_lufs = meter.integrated_loudness(data)
pre_eb = ebur128(IN_WAV)
check("pyloudnorm_agrees_with_ffmpeg_ebur128",
      pre_eb["integrated"] is not None and abs(pre_lufs - pre_eb["integrated"]) <= 1.0,
      "pyloudnorm=%.2f LUFS ebur128=%.2f LUFS (pre-normalization)"
      % (pre_lufs, pre_eb["integrated"] or float("nan")))
results["input"]["integrated_lufs_pyloudnorm"] = round(pre_lufs, 2)
results["input"]["integrated_lufs_ebur128"] = pre_eb["integrated"]

# Silence-region map of the clean VO (20 ms frames) — noise-profile source.
F = int(sr * 0.02)
nfr = (len(data) // F) * F
dtrim = data[:nfr]
frame_e = np.sqrt((dtrim.reshape(-1, F) ** 2).mean(1))
sil_frames = np.where(frame_e < np.percentile(frame_e, 10))[0]
noise_profile = np.concatenate([dtrim[i * F:(i + 1) * F] for i in sil_frames])
results["notes"].append(
    "silence profile: %d frames (%.2f s), rms %.6f — used as the stationary "
    "noise reference" % (len(sil_frames), len(noise_profile) / sr, rms(noise_profile)))

# ------------------------------------------------- 2. noisereduce (MIT)
# 2a. NEGATIVE CONTROL (documented misuse): stationary mode with NO noise
#     profile. Expected to damage program material — proves the profile rule.
blind = reduce_noise(y=data, sr=sr, stationary=True).astype(np.float64)
blind_delta = (rms(data) - rms(blind)) / rms(data)
results["findings"].append(
    "NEGATIVE CONTROL: stationary noisereduce with no y_noise profile on the "
    "clean VO removed %.1f%% of signal RMS (%.4f -> %.4f) — the gate treats "
    "program material as noise. Production rule: never run blind; always "
    "supply a silence/room-tone profile." % (blind_delta * 100, rms(data), rms(blind)))

# 2b. CORRECT USAGE on clean VO: profile from the file's own silence.
clean_dn = reduce_noise(y=data, sr=sr, stationary=True,
                        y_noise=noise_profile).astype(np.float64)
clean_delta = abs(rms(clean_dn) - rms(data)) / rms(data)
clean_corr = float(np.corrcoef(data, clean_dn)[0, 1])
check("noisereduce_clean_with_profile_safe",
      clean_delta < 0.05 and clean_corr > 0.999,
      "clean VO rms %.4f -> %.4f (delta %+.1f%%), corr %.5f — safe no-op pass"
      % (rms(data), rms(clean_dn), (rms(clean_dn) - rms(data)) / rms(data) * 100,
         clean_corr))

# 2c. CONTROLLED PROOF: inject calibrated -40 dBFS white noise, denoise with
#     the true noise reference; measure silence-region floor suppression and
#     speech-region fidelity separately (global SNR-vs-pristine is the wrong
#     metric — it penalizes the gate for doing its job).
rng = np.random.default_rng(52)
noise = rng.standard_normal(data.shape)
noise *= 10 ** (NOISE_DBFS / 20) / rms(noise)
noisy = data + noise
noisy_dn = reduce_noise(y=noisy, sr=sr, stationary=True,
                        y_noise=noise).astype(np.float64)
nn, dd, dnn = noisy[:nfr], dtrim, noisy_dn[:nfr]
sil = np.repeat(frame_e < np.percentile(frame_e, 15), F)
sp = np.repeat(frame_e > np.percentile(frame_e, 60), F)
floor_before, floor_after = rms(nn[sil]), rms(dnn[sil])
suppression = 20 * math.log10(floor_after / floor_before)
sp_corr = float(np.corrcoef(dnn[sp], dd[sp])[0, 1])
check("noisereduce_silence_floor_suppression",
      suppression <= -15.0,
      "silence-region noise floor %.5f -> %.5f (%+.1f dB, -40 dBFS white noise)"
      % (floor_before, floor_after, suppression))
check("noisereduce_speech_fidelity",
      sp_corr >= 0.95,
      "speech-region corr(denoised, clean)=%.4f (honest: musical-gate artifacts "
      "remain — error RMS %.4f vs speech RMS %.4f)"
      % (sp_corr, rms((dnn - dd)[sp]), rms(dd[sp])))
results["noisereduce"] = {
    "blind_no_profile_rms_loss_pct": round(blind_delta * 100, 1),
    "clean_with_profile_rms_delta_pct": round((rms(clean_dn) - rms(data)) / rms(data) * 100, 2),
    "clean_with_profile_corr": round(clean_corr, 5),
    "silence_floor_suppression_db": round(suppression, 1),
    "speech_region_corr": round(sp_corr, 4)}

sf.write(os.path.join(OUT, "vo_noisy_40db.wav"), noisy, sr, subtype="PCM_16")
sf.write(os.path.join(OUT, "vo_denoised_clean.wav"), clean_dn, sr, subtype="PCM_16")
sf.write(os.path.join(OUT, "vo_denoised_noisy.wav"), noisy_dn, sr, subtype="PCM_16")

# ---------------------------------------------- 3. pyloudnorm (MIT)
def master(y_mono, target_lufs, stereo, name):
    """Dual-pass master.
    Pass 1: pyloudnorm ITU-R BS.1770 gain to target, computed on the FINAL
    channel layout (dual-mono stereo reads +3 LU vs mono — gain-after-upmix
    bug caught during this wire-up), written as FLOAT32 so hot peaks are
    never clipped at the PCM16 rail before limiting.
    Pass 2 (only if needed): ffmpeg `alimiter` true-peak limiter to -1.0 dBTP
    (external binary; the repo's already-wired FFmpeg, no code linked).
    Linear attenuation was tried first and REJECTED: it cannot un-clip
    samples already flattened at the PCM16 rail."""
    m = np.stack([y_mono, y_mono], axis=1) if stereo else y_mono
    loud = meter.integrated_loudness(m)
    m = (m * 10 ** ((target_lufs - loud) / 20)).astype(np.float64)
    tmp_f32 = os.path.join(OUT, "_tmp_" + name + "_f32.wav")
    out_path = os.path.join(OUT, name + ".wav")
    sf.write(tmp_f32, m, sr, subtype="FLOAT")
    meas = ebur128(tmp_f32)
    tp = meas["true_peak"]
    peak_limited = False
    if tp is not None and tp > TRUE_PEAK_LIMIT:
        peak_limited = True
        lim = 10 ** (TRUE_PEAK_LIMIT / 20)
        tmp_lim = os.path.join(OUT, "_tmp_" + name + "_lim.wav")
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-i", tmp_f32, "-af",
             "alimiter=limit=%f:attack=7:release=100:level_in=1"
             ":level_out=%f:level=disabled" % (lim, lim),
             "-c:a", "pcm_s16le", tmp_lim], check=True)
        os.replace(tmp_lim, out_path)
        meas = ebur128(out_path)
    else:
        sf.write(out_path, m, sr, subtype="PCM_16")
        meas = ebur128(out_path)
    if meas["integrated"] is None or meas["true_peak"] is None:
        results["notes"].append("ebur128 parse failure on %s: %s"
                                % (name, meas["raw_tail"]))
    os.remove(tmp_f32)
    return out_path, meas, peak_limited


# Chain of record: denoise (correct usage) -> master.
pod_path, pod_meas, pod_lim = master(
    clean_dn, PODCAST_TARGET, stereo=True, name="master_podcast_16lufs_stereo")
brc_path, brc_meas, brc_lim = master(
    clean_dn, BROADCAST_TARGET, stereo=False, name="master_broadcast_24lufs_mono")

for label, path, meas, target, peak_limited, expect_ch in (
        ("podcast_-16lufs", pod_path, pod_meas, PODCAST_TARGET, pod_lim, 2),
        ("broadcast_-24lufs", brc_path, brc_meas, BROADCAST_TARGET, brc_lim, 1)):
    tol = 1.0 if peak_limited else 0.5
    lufs_ok = meas["integrated"] is not None and abs(meas["integrated"] - target) <= tol
    tp_ok = meas["true_peak"] is not None and meas["true_peak"] <= TRUE_PEAK_LIMIT
    info = sf.info(path)
    layout_ok = (abs(info.frames / info.samplerate - n_frames / sr) < 0.010
                 and info.channels == expect_ch)
    check("master_%s_lufs" % label, lufs_ok,
          "ebur128 %.2f LUFS vs target %.1f (tol %.1f, peak_limited=%s)"
          % (meas["integrated"] if meas["integrated"] is not None else float("nan"),
             target, tol, peak_limited))
    check("master_%s_true_peak" % label, tp_ok,
          "true peak %.2f dBFS <= -1.0 dBTP ceiling"
          % (meas["true_peak"] if meas["true_peak"] is not None else float("nan")))
    check("master_%s_layout" % label, layout_ok,
          "ch=%d (expect %d), duration %.3fs, LRA %.2f LU"
          % (info.channels, expect_ch, info.frames / info.samplerate,
             meas["lra"] if meas["lra"] is not None else float("nan")))
    results[label] = {"path": os.path.relpath(path, ROOT), "target_lufs": target,
                      "measured_lufs": meas["integrated"], "lra_lu": meas["lra"],
                      "true_peak_dbtp": meas["true_peak"], "peak_limited": peak_limited,
                      "channels": info.channels, "bytes": os.path.getsize(path)}

# Determinism: identical re-runs must be byte-identical (same dual-pass path).
def rerun(y_mono, target_lufs, stereo):
    m = np.stack([y_mono, y_mono], axis=1) if stereo else y_mono
    m = (m * 10 ** ((target_lufs - meter.integrated_loudness(m)) / 20)).astype(np.float64)
    p = os.path.join(OUT, "_det.wav")
    sf.write(p, m, sr, subtype="FLOAT")
    eb = ebur128(p)
    if eb["true_peak"] is not None and eb["true_peak"] > TRUE_PEAK_LIMIT:
        lim = 10 ** (TRUE_PEAK_LIMIT / 20)
        q = os.path.join(OUT, "_det2.wav")
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", p,
             "-af", "alimiter=limit=%f:attack=7:release=100:level_in=1"
             ":level_out=%f:level=disabled" % (lim, lim),
             "-c:a", "pcm_s16le", q], check=True)
        os.replace(q, p)
    return sha256(p)

det = [rerun(clean_dn, PODCAST_TARGET, True) for _ in range(2)]
check("mastering_byte_deterministic", det[0] == det[1],
      "two identical runs -> sha %s" % det[0][:16])
os.remove(os.path.join(OUT, "_det.wav"))

# noisereduce determinism
dn2 = reduce_noise(y=data, sr=sr, stationary=True,
                   y_noise=noise_profile).astype(np.float64)
p2 = os.path.join(OUT, "_det2.wav")
sf.write(p2, dn2, sr, subtype="PCM_16")
check("denoise_byte_deterministic",
      sha256(p2) == sha256(os.path.join(OUT, "vo_denoised_clean.wav")),
      "repeat denoise -> identical bytes")
os.remove(p2)

results["environment"] = {
    "python": sys.version.split()[0],
    "numpy": np.__version__,
    "noisereduce": __import__("importlib.metadata", fromlist=["x"]).version("noisereduce"),
    "pyloudnorm": "csteinmetz1/pyloudnorm (MIT)",
    "ffmpeg": subprocess.run(["ffmpeg", "-version"],
                             capture_output=True, text=True).stdout.splitlines()[0],
    "license_policy": "permissive only (MIT/Apache-2.0/BSD/ISC)"}
results["summary_pass"] = all(c["pass"] for c in results["checks"])
results["summary"] = "%d/%d checks PASS" % (
    sum(c["pass"] for c in results["checks"]), len(results["checks"]))

with open(os.path.join(OUT, "result.json"), "w") as f:
    json.dump(results, f, indent=2)
print("\n" + results["summary"])
sys.exit(0 if results["summary_pass"] else 1)
