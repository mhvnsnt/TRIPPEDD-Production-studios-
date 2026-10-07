#!/usr/bin/env python3
"""auditok_vad_srt.py — VAD caption-cue scaffolding with auditok (MIT).

Pipeline role: before any ASR runs, split episode audio into speech-active
regions. The regions become (a) the only spans worth transcribing and
(b) natural caption-cue boundaries.

This proof:
  1. synthesizes a speech-like test signal (3 amplitude-modulated tone
     bursts with silence gaps + low noise, 16 kHz mono WAV),
  2. runs auditok's energy-based VAD over it,
  3. emits an SRT scaffold — one cue per detected speech region.

auditok: https://github.com/amsehili/auditok (MIT, verified 2026-10-07).

Usage:
    python3 auditok_vad_srt.py --out-dir proofs/wave17_auditok
"""
import argparse
import os
import wave

import numpy as np


def synth_speech_like(path: str, sr: int = 16000) -> None:
    rng = np.random.default_rng(7)
    # (start_s, dur_s, base_freq_hz) — three "utterances"
    bursts = [(0.5, 1.2, 180.0), (2.4, 0.9, 240.0), (4.0, 1.4, 150.0)]
    total = 6.0
    n = int(total * sr)
    sig = np.zeros(n, dtype=np.float64)
    t = np.arange(n) / sr
    for start, dur, f in bursts:
        i0, i1 = int(start * sr), int((start + dur) * sr)
        tt = t[i0:i1] - start
        # syllable-ish amplitude modulation at ~4 Hz over a voiced tone
        env = (0.55 + 0.45 * np.sin(2 * np.pi * 4.0 * tt)) ** 2
        # fade in/out 50 ms to avoid clicks
        fade = int(0.05 * sr)
        env[:fade] *= np.linspace(0, 1, fade)
        env[-fade:] *= np.linspace(1, 0, fade)
        sig[i0:i1] = env * np.sin(2 * np.pi * f * tt)
    sig += 0.01 * rng.standard_normal(n)  # low room noise
    sig = np.clip(sig, -1, 1)
    pcm = (sig * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def srt_ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="auditok VAD -> SRT scaffold proof.")
    ap.add_argument("--out-dir", required=True, help="Proof output directory.")
    args = ap.parse_args()

    import auditok

    os.makedirs(args.out_dir, exist_ok=True)
    wav_path = os.path.join(args.out_dir, "wave17_synth_speech.wav")
    srt_path = os.path.join(args.out_dir, "wave17_auditok_vad.srt")

    synth_speech_like(wav_path)

    regions = auditok.split(
        wav_path,
        min_dur=0.2,       # ignore blips shorter than 200 ms
        max_dur=4.0,       # split very long regions
        max_silence=0.3,   # merge across short pauses
        energy_threshold=60,
    )
    regions = list(regions)

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, reg in enumerate(regions, 1):
            f.write(
                f"{i}\n{srt_ts(reg.start)} --> {srt_ts(reg.end)}\n"
                f"[speech region {i}]\n\n"
            )

    print(f"input : {wav_path}")
    print(f"output: {srt_path}")
    print(f"detected {len(regions)} speech region(s):")
    for reg in regions:
        print(f"  {reg.start:.2f}s -> {reg.end:.2f}s")

    # Proof gate: the synthetic signal has exactly 3 bursts; VAD must find
    # all three (no misses, no phantom regions).
    assert len(regions) == 3, f"expected 3 regions, got {len(regions)}"
    for reg, (start, dur, _f) in zip(
        regions, [(0.5, 1.2, 0), (2.4, 0.9, 0), (4.0, 1.4, 0)]
    ):
        assert abs(reg.start - start) < 0.35, "region start drifted"
        assert abs(reg.end - (start + dur)) < 0.35, "region end drifted"
    print("PROOF OK: 3/3 synthetic speech regions recovered as SRT cues.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
