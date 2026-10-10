# Wave 55 Lane C — resampy (ISC) sample-rate-conversion stage wiring.
#
# ORIGINAL MIT-licensed wire code for the TRIPPEDD pipeline. External libs
# (resampy, numpy, scipy, soundfile) are pip-installed, never embedded.
# License verified 2026-10-08 via GitHub API: bmcfee/resampy spdx_id = ISC.
# No GPL/LGPL/NC anywhere in the wire path. No model weights, no network.
#
# Pipeline fit: text->VO (Kokoro, 24 kHz) -> ... -> mastering (Wave 52) ->
# SAMPLE-RATE CONVERSION (this stage) -> 48 kHz video deliverables / archive.
# The stage standardizes archive audio sample rates before any restoration
# chain runs (per catalog notes).
#
# Proof run on REAL data:
#   tools/wave52_lane_c/proofs/audio_mastering/vo_denoised_clean.wav
#   (real Wave-52 noisereduce output, 7.825 s, 24 kHz mono, 16-bit).
import json
import math
import os
import sys

import numpy as np
import soundfile as sf

import resampy

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "resampy")
os.makedirs(PROOFS, exist_ok=True)

REPO = os.path.dirname(os.path.dirname(HERE))
SRC_MONO = os.path.join(REPO, "tools", "wave52_lane_c", "proofs",
                        "audio_mastering", "vo_denoised_clean.wav")
SRC_STEREO = os.path.join(REPO, "tools", "wave52_lane_c", "proofs",
                          "audio_mastering", "master_podcast_16lufs_stereo.wav")

checks = []
results = {}


def check(name, ok, detail):
    checks.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print(("PASS" if ok else "FAIL"), name, "-", detail)


def db(x):
    return 20.0 * math.log10(max(float(x), 1e-30))


# ---------------------------------------------------------------- source load
y, sr = sf.read(SRC_MONO, dtype="float32")
check("source_load", y.ndim == 1 and sr == 24000 and len(y) == 187800,
      f"mono frames={len(y)} sr={sr} dur={len(y)/sr:.6f}s")
results["source"] = {"frames": len(y), "sr": sr, "channels": 1}

# ------------------------------------------------------- 1) synthetic THD/SNR
# A 1 kHz sine at 24 kHz resampled to 48 kHz: measure SNR of the resampled
# tone against the ideal 1 kHz sine at 48 kHz (same phase/amplitude).
t48 = np.arange(187800 * 2, dtype=np.float64) / 48000.0
tone24 = np.sin(2 * np.pi * 1000.0 * np.arange(187800, dtype=np.float64) / 24000.0).astype(np.float64)
tone48_rs = resampy.resample(tone24, 24000, 48000, filter="kaiser_best")
ideal48 = np.sin(2 * np.pi * 1000.0 * t48)
# resampy is a linear-phase FIR; allow a fixed alignment lag: find best lag.
best, best_err = 0, np.inf
for lag in range(0, 400):
    err = np.mean((tone48_rs[lag:lag + len(ideal48) - 400] -
                   ideal48[:len(ideal48) - 400]) ** 2)
    if err < best_err:
        best, best_err = lag, err
tone48_al = tone48_rs[best:best + len(ideal48) - 400]
sig = np.mean(ideal48[:len(tone48_al)] ** 2)
noise = np.mean((tone48_al - ideal48[:len(tone48_al)]) ** 2)
snr_db = 10 * math.log10(sig / max(noise, 1e-30))
check("tone_snr_24k_to_48k", snr_db > 80.0,
      f"SNR={snr_db:.2f} dB (lag={best}) — real sinc SRC, not a copy")
results["tone_snr_db"] = snr_db
results["tone_align_lag"] = int(best)

# ------------------------------------------------------- 2) real VO -> 48 kHz
y48 = resampy.resample(y.astype(np.float64), 24000, 48000, filter="kaiser_best")
check("vo_up_24k_48k", len(y48) == 375600,
      f"frames 187800 -> {len(y48)} (expect 375600), dur={len(y48)/48000:.6f}s")
check("vo_up_finite", np.all(np.isfinite(y48)),
      f"min={y48.min():.6f} max={y48.max():.6f}")

# ------------------------------------------------------- 3) 48k -> 24k round-trip
# HONEST FINDING (measured 2026-10-08): resampy's 48k->24k kaiser_best
# anti-alias filter is NOT transparent to output Nyquist. Tone sweep:
# 10.0 kHz -> 0.00 dB, 10.5 kHz -> -0.26 dB, 10.75 kHz -> -1.67 dB,
# 11.0 kHz -> -5.82 dB, 11.5 kHz -> -29.46 dB => -3 dB point ~10.83 kHz.
# The real VO has energy up there, so a naive 24->48->24 round-trip only
# reaches ~24 dB SNR. Pipeline consequence: UPSAMPLE 24k->48k for video
# deliverables is safe; keep the 24k master as archive source of truth,
# never round-trip back. The checks below document the real behavior.
from scipy.signal import butter, filtfilt

y_rt = resampy.resample(y48, 48000, 24000, filter="kaiser_best")
y64 = y.astype(np.float64)


def aligned_snr(a, b, maxlag=500):
    best, be = 0, np.inf
    for lag in range(0, maxlag + 1):
        m = min(len(a) - 500, len(b) - lag)
        mse = np.mean((b[lag:lag + m] - a[:m]) ** 2)
        if mse < be:
            best, be = lag, mse
    m = min(len(a) - 500, len(b) - best)
    err = b[best:best + m] - a[:m]
    snr = 20 * math.log10(float(np.sqrt(np.mean(a[:m] ** 2))) /
                          max(float(np.sqrt(np.mean(err ** 2))), 1e-30))
    return snr, best, float(np.abs(err).max())


# 3a) roll-off characterization: -3 dB point of the 48->24 filter
def tone_att(f0):
    t = np.arange(96000, dtype=np.float64) / 48000.0
    out = resampy.resample(np.sin(2 * np.pi * f0 * t), 48000, 24000,
                           filter="kaiser_best")
    seg = out[500:-500]
    return 20 * math.log10(float(np.sqrt(np.mean(seg ** 2))) / 0.70710678)


att_lo, att_hi = tone_att(10750.0), tone_att(11000.0)
f3db = 10750.0 + 250.0 * (-3.0 - att_lo) / (att_hi - att_lo)  # linear interp
check("rolloff_3db_point", 10500.0 < f3db < 11500.0,
      f"-3 dB at ~{f3db:.0f} Hz (10.75k:{att_lo:.2f}dB, 11k:{att_hi:.2f}dB)")
results["downsample_3db_hz"] = float(f3db)

# 3b) round-trip IS transparent below the roll-off: 10 kHz lowpassed VO
b, a = butter(8, 10000.0 / 12000.0, btype="low")
y_lp = filtfilt(b, a, y64)
y48_lp = resampy.resample(y_lp, 24000, 48000, filter="kaiser_best")
y_rt_lp = resampy.resample(y48_lp, 48000, 24000, filter="kaiser_best")
snr_lp, lag_lp, maxe_lp = aligned_snr(y_lp, y_rt_lp)
check("roundtrip_below_10k", snr_lp > 60.0,
      f"lag={lag_lp}: 10k-lowpassed round-trip SNR={snr_lp:.2f} dB, "
      f"max abs err={maxe_lp:.2e}")
results["roundtrip_10k_lowpass_snr_db"] = snr_lp
results["roundtrip_10k_lowpass_max_abs_err"] = maxe_lp

# 3c) naive full-band round-trip, documented as lossy above ~10.8 kHz
snr_full, lag_full, maxe_full = aligned_snr(y64, y_rt)
check("roundtrip_fullband_documented", snr_full < 40.0,
      f"lag={lag_full}: full-band round-trip SNR={snr_full:.2f} dB "
      f"(max err {maxe_full:.2e}) — expected lossy above ~10.8 kHz, "
      f"this is the documented filter behavior, not a wire defect")
results["roundtrip_fullband_snr_db"] = snr_full
results["roundtrip_fullband_max_abs_err"] = maxe_full

# ------------------------------------------------------- 4) exact-rate sanity
y_same = resampy.resample(y.astype(np.float64), 24000, 24000)
check("same_rate_identity", len(y_same) == len(y) and
      np.max(np.abs(y_same - y.astype(np.float64))) < 1e-9,
      f"max diff={np.max(np.abs(y_same - y.astype(np.float64))):.2e}")

# ------------------------------------------------------- 5) stereo master SRC
ys, srs = sf.read(SRC_STEREO, dtype="float32")
ys48 = np.stack([resampy.resample(ys[:, c].astype(np.float64), 24000, 48000,
                                 filter="kaiser_best")
                 for c in range(ys.shape[1])], axis=1)
check("stereo_up", ys48.shape == (375600, 2),
      f"shape {ys.shape} -> {ys48.shape}, channels preserved")
out_stereo = os.path.join(PROOFS, "master_podcast_16lufs_48k.wav")
sf.write(out_stereo, np.clip(ys48, -1, 1).astype(np.float32), 48000,
         subtype="PCM_16")

# ------------------------------------------------------- 6) proof artifacts
out_vo48 = os.path.join(PROOFS, "vo_denoised_clean_48k.wav")
sf.write(out_vo48, np.clip(y48, -1, 1).astype(np.float32), 48000,
         subtype="PCM_16")

# ------------------------------------------------------- 7) determinism
y48_b = resampy.resample(y.astype(np.float64), 24000, 48000, filter="kaiser_best")
check("determinism", np.array_equal(np.clip(y48, -1, 1).astype(np.float32),
                                   np.clip(y48_b, -1, 1).astype(np.float32)),
      "two full 24k->48k runs -> bit-identical float32")

# ------------------------------------------------------- 8) filter comparison
y48_fast = resampy.resample(y.astype(np.float64), 24000, 48000, filter="kaiser_fast")
check("filter_variant_differs", not np.array_equal(y48_fast, y48),
      "kaiser_fast output differs from kaiser_best (both real ops)")

results["checks"] = checks
results["upstream"] = {"repo": "bmcfee/resampy", "license": "ISC",
                       "verified": "2026-10-08 via GitHub API spdx_id"}
with open(os.path.join(PROOFS, "result.json"), "w") as f:
    json.dump(results, f, indent=2, default=float)

failed = [c for c in checks if not c["ok"]]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks PASS")
sys.exit(1 if failed else 0)
