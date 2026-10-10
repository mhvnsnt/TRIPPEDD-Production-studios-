#!/usr/bin/env python3
"""Permissive-license speaker diarization for the Wave44 Lane C pull program.

Pipeline (all components MIT/BSD/ISC/Apache-2.0, no gated models):
  1. VAD: webrtcvad (MIT) on 30ms frames -> voiced segments.
  2. Features: librosa (ISC) MFCC mean+std per segment.
  3. Clustering: scikit-learn (BSD-3) AgglomerativeClustering -> speaker labels.

Design decision documented in PROOFS.md: pyannote.audio's models require
accepting HuggingFace gated-community terms for the segmentation/embedding
checkpoints, so it is deferred in favor of this fully permissive stack.
"""
import sys
import wave
import numpy as np
import webrtcvad
import librosa
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler


def read_mono_16k(path):
    with wave.open(path, "rb") as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == 16000, \
            f"need 16kHz mono 16-bit WAV, got {w.getnchannels()}ch/{w.getsampwidth()*8}bit/{w.getframerate()}Hz"
        n = w.getnframes()
        raw = w.readframes(n)
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def vad_segments(audio, sr=16000, frame_ms=30, aggressiveness=2, max_gap_s=0.3, min_seg_s=0.2):
    vad = webrtcvad.Vad(aggressiveness)
    frame_len = int(sr * frame_ms / 1000)
    voiced = []
    for i in range(0, len(audio) - frame_len + 1, frame_len):
        frame = audio[i:i + frame_len]
        pcm = (np.clip(frame, -1, 1) * 32767).astype(np.int16).tobytes()
        voiced.append(vad.is_speech(pcm, sr))
    segments, start = [], None
    for i, v in enumerate(voiced):
        t = i * frame_ms / 1000.0
        if v and start is None:
            start = t
        elif not v and start is not None:
            segments.append((start, t))
            start = None
    if start is not None:
        segments.append((start, len(voiced) * frame_ms / 1000.0))
    # merge close segments
    merged = []
    for s, e in segments:
        if merged and s - merged[-1][1] <= max_gap_s:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return [(s, e) for s, e in merged if e - s >= min_seg_s]


def segment_features(audio, sr, segments, n_mfcc=20):
    feats = []
    for s, e in segments:
        y = audio[int(s * sr):int(e * sr)]
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        delta = librosa.feature.delta(mfcc)
        vec = np.concatenate([mfcc.mean(axis=1), mfcc.std(axis=1),
                              delta.mean(axis=1)])
        # F0 statistics: pitch is the dominant cue separating our two voices
        f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz("C2"),
                                fmax=librosa.note_to_hz("C7"), sr=sr)
        voiced_f0 = f0[~np.isnan(f0)]
        if len(voiced_f0) > 0:
            logf0 = np.log(voiced_f0)
            vec = np.concatenate([vec, [logf0.mean(), logf0.std(),
                                        np.log(np.median(voiced_f0))]])
        else:
            vec = np.concatenate([vec, [0.0, 0.0, 0.0]])
        feats.append(vec)
    return np.stack(feats)


def diarize(path, n_speakers=2):
    sr = 16000
    audio = read_mono_16k(path)
    segments = vad_segments(audio, sr)
    if len(segments) < n_speakers:
        raise RuntimeError(f"only {len(segments)} voiced segments, need >= {n_speakers}")
    X = StandardScaler().fit_transform(segment_features(audio, sr, segments))
    # Pitch is a primary speaker cue, but the MFCC block (60 dims) outnumbers
    # the F0 block (3 dims) 20:1, so equal-per-dim scaling buries it. Weight the
    # F0 dims after scaling so voice-pitch differences actually move the metric.
    X[:, -3:] *= 8.0
    labels = AgglomerativeClustering(n_clusters=n_speakers).fit_predict(X)
    return [(s, e, int(l)) for (s, e), l in zip(segments, labels)]


def main():
    path = sys.argv[1]
    n_speakers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    turns = diarize(path, n_speakers)
    print(f"file: {path}")
    print(f"voiced segments: {len(turns)}, speakers requested: {n_speakers}")
    print(f"{'start':>8} {'end':>8} {'dur':>6}  speaker")
    for s, e, l in turns:
        print(f"{s:8.2f} {e:8.2f} {e-s:6.2f}  SPEAKER_{l:02d}")


if __name__ == "__main__":
    main()
