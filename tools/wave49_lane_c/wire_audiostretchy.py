#!/usr/bin/env python3
"""Wire-up + smoke proof: audiostretchy (BSD-3-Clause, TDHS C core).

Pitch-preserving time-stretch for the audio pipeline: fit AI voice lines /
music beds to animation beats without chipmunking; stretches silence
separately (gap_ratio).

Proof (no network): two synthetic 44.1 kHz mono WAVs:
  1. clean 440 Hz sine, 2.0 s  -> ratio=1.5 -> expect dur*1.5, dominant 440 Hz
     in every 1 s window (pure tone: single-peak FFT is a clean pitch metric).
  2. tone (2.5 s) + digital silence gap (0.5 s) + tone (0.5 s), 3.5 s total:
     - run A ratio=1.5          -> gap stretched with audio (~0.75 s)
     - run B ratio=1.5 gap_ratio=1.0 (silence mode) -> gap ~0.5 s, tones 1.5x
     Gap lengths are measured from the -40 dB RMS profile (50 ms bins).

KNOWN TOOL QUIRK (documented, not worked around): in silence mode,
audiostretchy pre-allocates the output buffer to output_capacity(nframes, ratio)
and save_wav writes the whole buffer, so silence-mode outputs are zero-padded
to the full-ratio duration. The proof trims trailing digital silence before
asserting the audio extent. Downstream users should do the same (or feed
ffmpeg silenceremove).

Usage: python3 wire_audiostretchy.py  (run from this script's directory)
"""

import contextlib
import json
import wave
from pathlib import Path

import numpy as np
from audiostretchy.stretch import stretch_audio

HERE = Path(__file__).resolve().parent
PROOF = HERE / "proofs" / "stretch"
INPUT_DIR = HERE / "proofs" / "input"
SR = 44100
F0 = 440.0


def write_wav(path: Path, audio: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    audio_i16 = (audio * 0.85 * 32767).astype(np.int16)
    with contextlib.closing(wave.open(str(path), "wb")) as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(audio_i16.tobytes())


def read_mono16(path: Path):
    with contextlib.closing(wave.open(str(path), "rb")) as w:
        sr, n = w.getframerate(), w.getnframes()
        pcm = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
    return pcm, sr


def dominant_freq(pcm: np.ndarray, sr: int) -> float:
    spec = np.abs(np.fft.rfft(pcm * np.hanning(len(pcm))))
    freqs = np.fft.rfftfreq(len(pcm), 1 / sr)
    return float(freqs[int(np.argmax(spec))])


def silent_runs(pcm: np.ndarray, sr: int, thresh_db: float = -40.0, bin_s: float = 0.05):
    """Return list of (start, end, dur) of contiguous below-threshold regions."""
    bs = int(bin_s * sr)
    rms = np.array([np.sqrt(np.mean(pcm[i:i + bs] ** 2))
                    for i in range(0, len(pcm) - bs + 1, bs)])
    db = 20 * np.log10(rms + 1e-12)
    sil = np.where(db < thresh_db)[0]
    runs, start, prev = [], None, None
    for b in sil:
        if prev is None or b == prev + 1:
            start = b if start is None else start
        else:
            runs.append((start, prev)); start = b
        prev = b
    if start is not None:
        runs.append((start, prev))
    return [(float(a * bin_s), float((b + 1) * bin_s), float((b - a + 1) * bin_s))
            for a, b in runs]


def trim_trailing_silence(pcm: np.ndarray, sr: int) -> np.ndarray:
    bs = int(0.05 * sr)
    for i in range(len(pcm), bs, -bs):
        seg = pcm[max(0, i - bs):i]
        if 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12) > -40:
            return pcm[:i]
    return pcm


def main():
    PROOF.mkdir(parents=True, exist_ok=True)

    # ---- Signal 1: pure 440 Hz sine -> pitch-preservation probe ----
    sine_src = INPUT_DIR / "sine440.wav"
    t = np.arange(int(2.0 * SR)) / SR
    write_wav(sine_src, np.sin(2 * np.pi * F0 * t))
    sine_out = PROOF / "sine440_stretched_1.5x.wav"
    stretch_audio(str(sine_src), str(sine_out), ratio=1.5)
    pcm, sr = read_mono16(sine_out)
    sine_dur = len(pcm) / sr
    win_freqs = [dominant_freq(pcm[int(off * sr):int(off * sr) + sr], sr)
                 for off in (0.0, 1.0, 2.0)]
    sine_ok = abs(sine_dur - 3.0) / 3.0 <= 0.05 and all(abs(f - F0) <= 1.0 for f in win_freqs)
    print(f"pitch probe: dur {sine_dur:.3f}s (expect 3.000s); "
          f"dominant freq per 1s window {[f'{f:.1f}' for f in win_freqs]} Hz (expect 440.0)")

    # ---- Signal 2: tone + silence gap + tone -> silence-separate probe ----
    def tone(dur, seed):
        rng = np.random.default_rng(seed)
        tt = np.arange(int(dur * SR)) / SR
        sig = sum(np.sin(2 * np.pi * F0 * h * tt + rng.uniform(0, 2 * np.pi)) / h
                  for h in (1, 2, 3))
        return sig / np.max(np.abs(sig))

    gap_src = INPUT_DIR / "tone_gap_tone.wav"
    write_wav(gap_src, np.concatenate([tone(2.5, 7), np.zeros(int(0.5 * SR)), tone(0.5, 9)]))

    runs = []
    for name, params, exp_gap, exp_extent in [
        ("full_1.5x", {"ratio": 1.5}, 0.75, 5.25),
        ("silence_separate", {"ratio": 1.5, "gap_ratio": 1.0}, 0.50, 5.00),
    ]:
        out = PROOF / f"gap_{name}.wav"
        stretch_audio(str(gap_src), str(out), **params)
        pcm, sr = read_mono16(out)
        trimmed = trim_trailing_silence(pcm, sr)
        extent = float(len(trimmed) / sr)
        gaps = silent_runs(trimmed, sr)
        # the interior gap is the longest silent run strictly inside the audio
        interior = [g for g in gaps if g[0] > 1.0 and g[1] < extent - 0.2]
        gap_dur = float(max((g[2] for g in interior), default=0.0))
        gap_ok = bool(abs(gap_dur - exp_gap) <= 0.15)
        extent_ok = bool(abs(extent - exp_extent) / exp_extent <= 0.05)
        print(f"  {name}: extent {extent:.3f}s (expect ~{exp_extent:.2f}s, "
              f"trailing pad trimmed) {'OK' if extent_ok else 'OFF'}; "
              f"gap {gap_dur:.2f}s (expect ~{exp_gap:.2f}s) {'OK' if gap_ok else 'OFF'}")
        runs.append({"name": name, "params": params, "output": out.name,
                     "audio_extent_s": round(extent, 3), "expected_extent_s": exp_extent,
                     "extent_within_5pct": extent_ok,
                     "interior_gap_s": round(gap_dur, 2), "expected_gap_s": exp_gap,
                     "gap_within_150ms": gap_ok})

    ok = sine_ok and all(r["extent_within_5pct"] and r["gap_within_150ms"] for r in runs)
    result = {
        "tool": "audiostretchy",
        "license": "BSD-3-Clause (verified via GitHub API spdx_id 2026-10-08)",
        "pitch_probe": {"input": str(sine_src), "output": str(sine_out.name),
                        "output_dur_s": round(sine_dur, 3), "expected_dur_s": 3.0,
                        "dominant_freq_per_1s_window_hz": [round(f, 1) for f in win_freqs],
                        "pass": bool(sine_ok)},
        "silence_mode_probe": {"input": str(gap_src), "runs": runs},
        "quirk": "silence-mode outputs are zero-padded to the full-ratio buffer "
                 "(save_wav writes the whole pre-allocated buffer); trim trailing "
                 "digital silence downstream — done in this proof.",
        "pass": bool(ok),
    }
    out_json = PROOF / "result.json"
    out_json.write_text(json.dumps(result, indent=2))
    print(f"result: {'PASS' if ok else 'FAIL'} -> {out_json}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
