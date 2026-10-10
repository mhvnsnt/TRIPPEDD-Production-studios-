# Wave 55 Lane C — audiomentations (MIT) degradation-stress stage wiring.
#
# ORIGINAL MIT-licensed wire code for the TRIPPEDD pipeline. External libs
# (audiomentations, numpy, soundfile, librosa) are pip-installed, never
# embedded. License verified 2026-10-08 via GitHub API:
# iver56/audiomentations spdx_id = MIT. No GPL/LGPL/NC in the wire path.
# No model weights, no network.
#
# Pipeline fit (per catalog): "stress-testing restoration chains against
# degraded variants". Stage: mastered VO (Wave 52) -> SEEDED DEGRADED
# VARIANTS (this stage) -> denoise (Wave 52 noisereduce) -> measure recovery.
# Also doubles as a VO take-variation generator (take2 takes) via seeded
# pitch/gain shifts.
#
# Proof runs on REAL data:
#   tools/wave52_lane_c/proofs/audio_mastering/vo_denoised_clean.wav
#   (real Wave-52 noisereduce output, 7.825 s, 24 kHz mono, 16-bit).
import json
import math
import os
import random
import sys

import numpy as np
import soundfile as sf
from audiomentations import (AddGaussianNoise, AirAbsorption, Compose,
                             Gain, HighPassFilter, PitchShift)

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "audiomentations")
os.makedirs(PROOFS, exist_ok=True)

REPO = os.path.dirname(os.path.dirname(HERE))
SRC_MONO = os.path.join(REPO, "tools", "wave52_lane_c", "proofs",
                        "audio_mastering", "vo_denoised_clean.wav")
SR = 24000

checks = []
results = {}


def check(name, ok, detail):
    checks.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print(("PASS" if ok else "FAIL"), name, "-", detail)


def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x, dtype=np.float64) ** 2)))


def dom_freq(x, sr):
    n = len(x)
    win = x * np.hanning(n)
    spec = np.abs(np.fft.rfft(win))
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    return float(freqs[int(np.argmax(spec))])


# ---------------------------------------------------------------- source load
y, sr = sf.read(SRC_MONO, dtype="float32")
check("source_load", y.ndim == 1 and sr == SR and len(y) == 187800,
      f"frames={len(y)} sr={sr}")
src_rms = rms(y)
results["source"] = {"frames": len(y), "sr": sr, "rms": src_rms}

# ------------------------------------------------- 1) Gain -6 dB (exact gain)
gain_aug = Compose([Gain(min_gain_db=-6.0, max_gain_db=-6.0, p=1.0)])
y_g = gain_aug(samples=y, sample_rate=SR)
ratio = rms(y_g) / src_rms
expect = 10 ** (-6.0 / 20.0)  # 0.501187
check("gain_minus6db", abs(ratio - expect) < 1e-4,
      f"RMS ratio={ratio:.6f} expect={expect:.6f} (real dB gain applied)")
results["gain_ratio"] = float(ratio)
results["gain_expected"] = expect

# ------------------------------------------------- 2) seeded Gaussian noise
# Seeded RNG -> the degraded variant is reproducible; noise RMS must match
# the requested amplitude (uniform(-a, a) has RMS = a/sqrt(3)).
noise_aug = Compose([AddGaussianNoise(min_amplitude=0.005, max_amplitude=0.005,
                                      p=1.0)],
                    shuffle=False)
np.random.seed(1234)
y_n1 = noise_aug(samples=y, sample_rate=SR)
np.random.seed(1234)
y_n2 = noise_aug(samples=y, sample_rate=SR)
noise1 = y_n1.astype(np.float64) - y.astype(np.float64)
noise2 = y_n2.astype(np.float64) - y.astype(np.float64)
check("noise_reproducible", np.array_equal(y_n1, y_n2),
      "same seed -> bit-identical degraded variant")
# Seeded RNG -> the degraded variant is reproducible. Upstream implementation
# (verified in installed source): noise = amplitude * randn(...) — Gaussian
# with std = amplitude, so expected noise RMS = amplitude exactly.
exp_noise_rms = 0.005
got_noise_rms = rms(noise1)
check("noise_amplitude", abs(got_noise_rms - exp_noise_rms) / exp_noise_rms < 0.02,
      f"added-noise RMS={got_noise_rms:.6f} expect={exp_noise_rms:.6f} "
      f"(Gaussian std=amplitude per upstream source)")
pred_snr = 20 * math.log10(src_rms / exp_noise_rms)
snr_noisy = 20 * math.log10(src_rms / got_noise_rms)
check("noise_snr_matches_params", abs(snr_noisy - pred_snr) < 0.5,
      f"degraded SNR={snr_noisy:.2f} dB, predicted from params={pred_snr:.2f} dB")
results["degraded_snr_db"] = snr_noisy
results["degraded_snr_predicted_db"] = pred_snr

# ------------------------------------------------- 3) PitchShift +2 semitones
# Measurable on a synthetic 440 Hz tone: expect 440 * 2^(2/12) = 493.88 Hz.
tone = (0.9 * np.sin(2 * np.pi * 440.0 *
                     np.arange(SR * 2, dtype=np.float64) / SR)).astype(np.float32)
pitch_aug = Compose([PitchShift(min_semitones=2.0, max_semitones=2.0, p=1.0)])
y_p = pitch_aug(samples=tone, sample_rate=SR)
f0 = dom_freq(y_p, SR)
expect_f = 440.0 * 2 ** (2.0 / 12.0)
check("pitch_shift_2st", abs(f0 - expect_f) < 3.0,
      f"dominant freq={f0:.2f} Hz expect={expect_f:.2f} Hz (real resampling pitch)")
results["pitch_measured_hz"] = f0
results["pitch_expected_hz"] = expect_f

# ------------------------------------------------- 4) full degradation chain
degrade = Compose([
    AddGaussianNoise(min_amplitude=0.008, max_amplitude=0.008, p=1.0),
    AirAbsorption(min_temperature=10.0, max_temperature=10.0,
                  min_humidity=30.0, max_humidity=30.0,
                  min_distance=50.0, max_distance=50.0, p=1.0),
    HighPassFilter(min_cutoff_freq=100.0, max_cutoff_freq=100.0, p=1.0),
    Gain(min_gain_db=-3.0, max_gain_db=-3.0, p=1.0),
], shuffle=False)
y_d = degrade(samples=y, sample_rate=SR)
check("degrade_chain", len(y_d) == len(y) and np.all(np.isfinite(y_d)),
      f"frames preserved={len(y_d)}, finite, RMS {src_rms:.4f}->{rms(y_d):.4f}")
out_deg = os.path.join(PROOFS, "vo_degraded_variant_seed1234.wav")
sf.write(out_deg, np.clip(y_d, -1, 1).astype(np.float32), SR, subtype="PCM_16")
check("degrade_written", os.path.getsize(out_deg) > 300000,
      f"{os.path.getsize(out_deg)} bytes")
# Determinism of the whole chain. FINDING: audiomentations draws from BOTH
# np.random and Python's random module (HighPassFilter consumes `random`
# even with a fixed cutoff range — measured). Seeding only one leaves the
# chain non-deterministic. Seeding both -> bit-identical.
np.random.seed(99); random.seed(99)
a = degrade(samples=y, sample_rate=SR)
np.random.seed(99); random.seed(99)
b = degrade(samples=y, sample_rate=SR)
check("chain_deterministic", np.array_equal(a, b),
      "np.random.seed + random.seed -> bit-identical degraded WAV")
results["dual_rng_note"] = ("HighPassFilter consumes Python's random module; "
                            "both RNGs must be seeded for reproducibility")
results["degraded_rms"] = rms(y_d)

# ------------------------------------------------- 5) a genuinely different take
vary = Compose([PitchShift(min_semitones=-1.5, max_semitones=-1.5, p=1.0),
                Gain(min_gain_db=1.5, max_gain_db=1.5, p=1.0)], shuffle=False)
y_v = vary(samples=y, sample_rate=SR)
check("take_variation", len(y_v) == len(y) and not np.array_equal(y_v, y),
      f"take2 variant: pitch -1.5 st, gain +1.5 dB, frames={len(y_v)}")
out_var = os.path.join(PROOFS, "vo_take2_variant.wav")
sf.write(out_var, np.clip(y_v, -1, 1).astype(np.float32), SR, subtype="PCM_16")

results["checks"] = checks
results["upstream"] = {"repo": "iver56/audiomentations", "license": "MIT",
                       "verified": "2026-10-08 via GitHub API spdx_id"}
with open(os.path.join(PROOFS, "result.json"), "w") as f:
    json.dump(results, f, indent=2, default=float)

failed = [c for c in checks if not c["ok"]]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks PASS")
sys.exit(1 if failed else 0)
