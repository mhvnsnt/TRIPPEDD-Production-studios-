#!/usr/bin/env python3
"""Wire-up + smoke proof: webrtcvad (WebRTC GMM VAD, MIT wrapper + BSD core).

Silence/speech detection for the audio pipeline: gates caption chunking,
silence-trim, and speech-gated resync. No model weights, no network at runtime.

Proof strategy (no network, no mic): synthesize a known-ground-truth 16 kHz
mono 16-bit WAV with labeled silence/voiced regions, run webrtcvad in 30 ms
frames (aggressiveness=2), then apply the canonical ring-buffer collector to
emit speech segments. The proof asserts the collector finds exactly the two
voiced regions within a tolerance and reports per-region speech-frame rates.

Usage: python3 wire_webrtcvad.py  (run from this script's directory)
"""

import collections
import contextlib
import json
import wave
from pathlib import Path

import numpy as np
import webrtcvad

HERE = Path(__file__).resolve().parent
PROOF = HERE / "proofs" / "vad"
INPUT_DIR = HERE / "proofs" / "input"
SR = 16000  # webrtcvad only accepts 8/16/32/48 kHz
FRAME_MS = 30
AGGRESSIVENESS = 2

# Ground truth timeline (seconds): (start, end, label)
GT = [
    (0.0, 1.0, "silence"),
    (1.0, 2.5, "voiced"),
    (2.5, 3.5, "silence"),
    (3.5, 5.0, "voiced"),
]


def synth_vowel(dur_s: float, f0: float, sr: int, seed: int) -> np.ndarray:
    """Harmonic buzz with syllabic amplitude modulation -> pseudo-vowel."""
    rng = np.random.default_rng(seed)
    t = np.arange(int(dur_s * sr)) / sr
    sig = np.zeros_like(t)
    for h in range(1, 9):  # harmonic series, 1/h rolloff
        sig += np.sin(2 * np.pi * f0 * h * t + rng.uniform(0, 2 * np.pi)) / h
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 4.0 * t)  # ~4 Hz syllable rate
    sig *= am
    # 10 ms raised-cosine fade at both ends to avoid clicks
    fade = int(0.01 * sr)
    win = 0.5 * (1 - np.cos(np.linspace(0, np.pi, fade)))
    sig[:fade] *= win
    sig[-fade:] *= win[::-1]
    return sig / np.max(np.abs(sig))


def build_test_wav(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    parts = []
    for start, end, label in GT:
        dur = end - start
        if label == "silence":
            parts.append(np.zeros(int(dur * SR)))
        else:
            f0 = 120.0 if start < 2.0 else 165.0
            parts.append(synth_vowel(dur, f0, SR, seed=int(start * 10)))
    audio = np.concatenate(parts)
    audio_i16 = (audio * 0.85 * 32767).astype(np.int16)
    with contextlib.closing(wave.open(str(path), "wb")) as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(audio_i16.tobytes())
    print(f"wrote test wav: {path} ({len(audio_i16) / SR:.2f}s @ {SR}Hz mono16)")


def read_frames(wav_path: Path):
    with contextlib.closing(wave.open(str(wav_path), "rb")) as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2
        assert w.getframerate() == SR
        pcm = w.readframes(w.getnframes())
    frame_len = SR * FRAME_MS // 1000
    for i in range(0, len(pcm) - frame_len * 2 + 1, frame_len * 2):
        yield pcm[i : i + frame_len * 2]


def collect_segments(frames, vad, padding_ms=300, ratio=0.75):
    """Canonical ring-buffer segmenter from the webrtcvad example."""
    num_padding = padding_ms // FRAME_MS
    ring = collections.deque(maxlen=num_padding)
    triggered = False
    voiced_frames = []
    segments = []
    total_ms = 0
    for frame in frames:
        is_speech = vad.is_speech(frame, SR)
        if not triggered:
            ring.append((frame, is_speech))
            if len(ring) == num_padding and sum(1 for _, s in ring if s) > ratio * num_padding:
                triggered = True
                voiced_frames.extend(f for f, s in ring)
                ring.clear()
        else:
            voiced_frames.append(frame)
            ring.append((frame, is_speech))
            if len(ring) == num_padding and sum(1 for _, s in ring if not s) > ratio * num_padding:
                end_ms = total_ms
                triggered = False
                yield bytes(b"".join(voiced_frames)), (end_ms - len(voiced_frames) * FRAME_MS) / 1000.0, end_ms / 1000.0
                ring.clear()
                voiced_frames = []
        total_ms += FRAME_MS
    if voiced_frames:
        end_ms = total_ms
        yield bytes(b"".join(voiced_frames)), (end_ms - len(voiced_frames) * FRAME_MS) / 1000.0, end_ms / 1000.0


def main():
    PROOF.mkdir(parents=True, exist_ok=True)
    wav_path = INPUT_DIR / "vad_test.wav"
    build_test_wav(wav_path)

    vad = webrtcvad.Vad(AGGRESSIVENESS)
    frames = list(read_frames(wav_path))
    flags = [vad.is_speech(f, SR) for f in frames]
    frame_times = [(i * FRAME_MS / 1000.0, (i + 1) * FRAME_MS / 1000.0) for i in range(len(frames))]

    # Per-region speech-frame rates vs ground truth
    region_stats = []
    for start, end, label in GT:
        in_region = [i for i, (a, b) in enumerate(frame_times) if b > start and a < end]
        rate = sum(flags[i] for i in in_region) / max(len(in_region), 1)
        region_stats.append({"start": start, "end": end, "label": label,
                             "speech_frame_rate": round(rate, 3),
                             "frames": len(in_region)})
        print(f"  GT {label:8s} [{start:4.1f}-{end:4.1f}s]: {rate:6.1%} frames flagged speech")

    segments = []
    for _seg_bytes, seg_start, seg_end in collect_segments(iter(frames), vad):
        segments.append({"start_s": round(seg_start, 3), "end_s": round(seg_end, 3),
                         "dur_s": round(seg_end - seg_start, 3)})
    for s in segments:
        print(f"  detected segment: {s['start_s']:.3f}s -> {s['end_s']:.3f}s (dur {s['dur_s']:.3f}s)")

    # Assertions: exactly 2 segments, aligned to the voiced ground truth (tol 0.4s incl. padding)
    voiced_gt = [(s, e) for s, e, l in GT if l == "voiced"]
    ok = len(segments) == 2 and all(
        abs(seg["start_s"] - gs) <= 0.4 and abs(seg["end_s"] - ge) <= 0.4
        for seg, (gs, ge) in zip(segments, voiced_gt)
    )
    result = {
        "tool": "webrtcvad",
        "license": "MIT (Python wrapper, wiseman/py-webrtcvad) + BSD (WebRTC VAD core)",
        "input": str(wav_path),
        "sample_rate_hz": SR,
        "frame_ms": FRAME_MS,
        "aggressiveness": AGGRESSIVENESS,
        "total_frames": len(frames),
        "region_stats": region_stats,
        "segments": segments,
        "expected_segments": 2,
        "pass": bool(ok),
    }
    out = PROOF / "result.json"
    out.write_text(json.dumps(result, indent=2))
    print(f"result: {'PASS' if ok else 'FAIL'} -> {out}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
