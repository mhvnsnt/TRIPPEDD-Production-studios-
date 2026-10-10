#!/usr/bin/env python3
"""Wave 24 Lane B — wire webrtcvad (MIT wrapper + BSD WebRTC core).

Zero-dependency GMM voice activity detection: the cheapest VAD in the
captions lane (no model weights, no network). This demo synthesizes a
6 s / 16 kHz mono WAV with two speech-like bursts in silence, runs
webrtcvad over 30 ms frames, merges voiced frames into segments, and
checks the detected segments line up with the known burst regions.

Proof artifacts: tools/captions/proofs/wave24_lane_b/wave24_vad_proof.json
(+ wave24_synth.wav, the synthetic input).
"""
import json
import math
import os
import random
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
PROOF_DIR = os.path.join(HERE, "proofs", "wave24_lane_b")

SAMPLE_RATE = 16000
DURATION_S = 6.0
# Ground-truth speech bursts (seconds).
TRUTH = [(0.5, 2.0), (3.0, 4.5)]


def synth_wav(path):
    """Speech-like = sum of sines with syllabic amplitude modulation + noise."""
    random.seed(24)
    n = int(SAMPLE_RATE * DURATION_S)
    frames = []
    for i in range(n):
        t = i / SAMPLE_RATE
        in_speech = any(a <= t < b for a, b in TRUTH)
        if in_speech:
            # ~120 Hz "pitch" + harmonics, 4 Hz syllabic AM, plus noise.
            am = 0.55 + 0.45 * math.sin(2 * math.pi * 4 * t)
            s = (math.sin(2 * math.pi * 120 * t)
                 + 0.5 * math.sin(2 * math.pi * 240 * t)
                 + 0.25 * math.sin(2 * math.pi * 360 * t)) * am
            s += random.uniform(-0.08, 0.08)
            v = int(max(-1.0, min(1.0, s * 0.5)) * 32767)
        else:
            v = int(random.uniform(-30, 30))  # near-silence floor
        frames.append(v)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b"".join(v.to_bytes(2, "little", signed=True)
                               for v in frames))
    return path


def vad_segments(wav_path, aggressiveness=3, frame_ms=30, hangover_ms=200):
    import webrtcvad
    vad = webrtcvad.Vad(aggressiveness)
    with wave.open(wav_path, "rb") as w:
        assert w.getframerate() == SAMPLE_RATE and w.getnchannels() == 1 \
            and w.getsampwidth() == 2
        pcm = w.readframes(w.getnframes())
    frame_bytes = int(SAMPLE_RATE * frame_ms / 1000) * 2
    voiced = []
    for i in range(0, len(pcm) - frame_bytes + 1, frame_bytes):
        chunk = pcm[i:i + frame_bytes]
        voiced.append(vad.is_speech(chunk, SAMPLE_RATE))
    # Merge with hangover: bridge short silence gaps inside speech.
    hangover_frames = max(1, hangover_ms // frame_ms)
    segments, start, gap = [], None, 0
    for idx, v in enumerate(voiced):
        t = idx * frame_ms / 1000.0
        if v:
            if start is None:
                start = t
            gap = 0
        else:
            if start is not None:
                gap += 1
                if gap >= hangover_frames:
                    segments.append((start, t - gap * frame_ms / 1000.0))
                    start, gap = None, 0
    if start is not None:
        segments.append((start, len(voiced) * frame_ms / 1000.0))
    return segments, voiced


def overlap(a, b):
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def main():
    os.makedirs(PROOF_DIR, exist_ok=True)
    wav_path = os.path.join(PROOF_DIR, "wave24_synth.wav")
    synth_wav(wav_path)
    segments, voiced = vad_segments(wav_path)

    # Every truth burst must be substantially covered by detections...
    coverage = [max((overlap(seg, t) / (t[1] - t[0]) for seg in segments),
                    default=0.0) for t in TRUTH]
    # ...and every detected segment must substantially overlap some truth.
    purity = [max((overlap(seg, t) / (seg[1] - seg[0]) for t in TRUTH),
                  default=0.0) for seg in segments]

    assert len(segments) == len(TRUTH), \
        f"expected {len(TRUTH)} segments, got {len(segments)}: {segments}"
    assert all(c > 0.8 for c in coverage), f"poor coverage: {coverage}"
    assert all(p > 0.8 for p in purity), f"poor purity: {purity}"

    proof = {
        "tool": "webrtcvad (MIT wrapper, BSD WebRTC core) via webrtcvad-wheels",
        "input": wav_path,
        "sample_rate_hz": SAMPLE_RATE,
        "duration_s": DURATION_S,
        "ground_truth_speech_s": TRUTH,
        "vad_aggressiveness": 3,
        "frame_ms": 30,
        "detected_segments_s": [[round(a, 3), round(b, 3)] for a, b in segments],
        "coverage_per_burst": [round(c, 3) for c in coverage],
        "purity_per_segment": [round(p, 3) for p in purity],
        "voiced_frame_ratio": round(sum(voiced) / len(voiced), 3),
        "assertions": [
            "segment count == burst count (2)",
            "coverage per burst > 0.8",
            "purity per segment > 0.8",
        ],
    }
    proof_fn = os.path.join(PROOF_DIR, "wave24_vad_proof.json")
    with open(proof_fn, "w") as f:
        json.dump(proof, f, indent=2)
    print(f"segments: {proof['detected_segments_s']}")
    print(f"coverage: {proof['coverage_per_burst']} purity: {proof['purity_per_segment']}")
    print(f"proof -> {proof_fn}")


if __name__ == "__main__":
    main()
