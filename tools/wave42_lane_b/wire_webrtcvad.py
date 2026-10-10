#!/usr/bin/env python3
"""Wire webrtcvad (MIT, github.com/wiseman/py-webrtcvad) — real VAD proof.

Production relevance: TRIPPEDD/God-Molecule captions + voice pipelines need
speech/silence segmentation (auto_caption.py, voiceover.py in tools/video_pipeline).
webrtcvad is the standard lightweight VAD: no model download, pure C extension.

Run: /home/hatch/.cache/w42b_venv/bin/python wire_webrtcvad.py
Outputs (all small, committed): fixture_vad.wav, vad_frames.txt,
vad_segments.json, vad_report.txt
"""
import json
import os
import struct
import wave

import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
SAMPLE_RATE = 16000
FRAME_MS = 30
AGGRESSIVENESS = 2


def voiced_burst(n, seed=7):
    """Deterministic speech-like signal: harmonic stack + syllabic AM + noise."""
    rng = np.random.default_rng(seed)
    t = np.arange(n) / SAMPLE_RATE
    f0 = 120.0
    sig = np.zeros(n)
    for k, amp in enumerate((1.0, 0.5, 0.3, 0.15, 0.08), start=1):
        sig += amp * np.sin(2 * np.pi * f0 * k * t)
    # syllabic amplitude modulation (~4 Hz) so it reads as speech, not a tone
    sig *= 0.55 + 0.45 * np.sin(2 * np.pi * 4.0 * t + 0.7)
    sig += 0.03 * rng.standard_normal(n)
    sig *= 0.5 / max(1e-9, np.abs(sig).max())
    return (sig * 30000).astype(np.int16)


def make_fixture(path):
    """7 s fixture: 1 s silence, 2 s voice, 1 s silence, 2 s voice, 1 s silence."""
    segs = [
        np.zeros(SAMPLE_RATE, dtype=np.int16),
        voiced_burst(2 * SAMPLE_RATE, seed=7),
        np.zeros(SAMPLE_RATE, dtype=np.int16),
        voiced_burst(2 * SAMPLE_RATE, seed=21),
        np.zeros(SAMPLE_RATE, dtype=np.int16),
    ]
    pcm = np.concatenate(segs)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())
    return pcm


def main():
    import webrtcvad

    print("webrtcvad module:", webrtcvad.__file__)
    wav_path = os.path.join(OUT, "fixture_vad.wav")
    make_fixture(wav_path)

    with wave.open(wav_path, "rb") as w:
        assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, 16000)
        pcm = w.readframes(w.getnframes())

    vad = webrtcvad.Vad(AGGRESSIVENESS)
    frame_bytes = SAMPLE_RATE * FRAME_MS // 1000 * 2
    n_frames = len(pcm) // frame_bytes
    decisions = []
    for i in range(n_frames):
        frame = pcm[i * frame_bytes:(i + 1) * frame_bytes]
        decisions.append(1 if vad.is_speech(frame, SAMPLE_RATE) else 0)

    with open(os.path.join(OUT, "vad_frames.txt"), "w") as f:
        f.write("".join(str(d) for d in decisions) + "\n")

    # merge voiced runs into segments (allow 3-frame bridging)
    segments, start = [], None
    gap = 0
    for i, d in enumerate(decisions):
        if d:
            if start is None:
                start = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap > 3:
                segments.append((start, i - gap))
                start, gap = None, 0
    if start is not None:
        segments.append((start, n_frames - 1))
    seg_s = [(round(a * FRAME_MS / 1000, 2), round((b + 1) * FRAME_MS / 1000, 2))
             for a, b in segments]

    voiced_ratio = sum(decisions) / len(decisions)
    truth = [(1.0, 3.0), (4.0, 6.0)]  # where the fixture actually has voice
    hits = sum(1 for (a, b) in seg_s
               for (ta, tb) in truth if a < tb - 0.25 and b > ta + 0.25)
    report = {
        "tool": "webrtcvad",
        "license": "MIT",
        "aggressiveness": AGGRESSIVENESS,
        "sample_rate": SAMPLE_RATE,
        "frame_ms": FRAME_MS,
        "n_frames": n_frames,
        "voiced_frames": sum(decisions),
        "voiced_ratio": round(voiced_ratio, 3),
        "segments_s": seg_s,
        "ground_truth_s": truth,
        "truth_segments_matched": hits,
        "verdict": "PASS" if hits == len(truth) and len(seg_s) <= 3 else "CHECK",
    }
    with open(os.path.join(OUT, "vad_segments.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(OUT, "vad_report.txt"), "w") as f:
        f.write(f"webrtcvad VAD proof\naggressiveness={AGGRESSIVENESS} "
                f"frames={n_frames} voiced={sum(decisions)} "
                f"ratio={voiced_ratio:.3f}\nsegments(s): {seg_s}\n"
                f"truth(s): {truth}\nverdict: {report['verdict']}\n")
    print(json.dumps(report, indent=2))
    assert report["verdict"] == "PASS", "VAD did not match ground truth"
    print("OK — real VAD proof written")


if __name__ == "__main__":
    main()
