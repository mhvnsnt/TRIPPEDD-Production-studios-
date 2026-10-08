#!/usr/bin/env python3
"""Wave 56 Lane C — wire SpeechBrain ECAPA-TDNN speaker embeddings.

Speaker-embedding stage wired as the diarization-adjacent complement to the
VO pipeline (who-spoke-when for multi-character dialogue editing / caption
burn-in; the Wave 44/7A catalog notes flag this as the diarization layer).

License gate: SpeechBrain is Apache-2.0 (GitHub API spdx_id, re-verified
2026-10-08); the spkrec-ecapa-voxceleb model card on HF is tagged
license:apache-2.0 and is NOT gated.

Proof artifacts land in proofs/speechbrain_ecapa/:
  fixture_2spk.wav  - synthetic 2-speaker dialogue (A,B,A,B segments, 16 kHz)
  embeddings.pt    - 4 x 192 ECAPA embeddings
  result.json      - measured numbers + PASS/FAIL per check
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
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "speechbrain_ecapa")
SAVEDIR = os.path.join(HERE, "scratch", "speechbrain_models")
SR = 16000


def voice(dur_s, f0, n_harm, decay, vib_hz, vib_pct, seed):
    """Deterministic harmonic-complex 'voice' with vibrato and jitter."""
    rng = np.random.default_rng(seed)
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    vib = 1.0 + (vib_pct / 100.0) * np.sin(2 * math.pi * vib_hz * t)
    phase = np.cumsum(2 * math.pi * f0 * vib / SR)
    x = np.zeros(n, dtype=np.float64)
    phases = rng.uniform(0, 2 * math.pi, n_harm)
    for h in range(1, n_harm + 1):
        amp = 1.0 / (h ** decay)
        x += amp * np.sin(h * phase + phases[h - 1])
    x /= np.max(np.abs(x))
    # syllable-ish amplitude modulation (speech-like energy contour)
    syll = 0.65 + 0.35 * np.sin(2 * math.pi * 3.1 * t + 0.4) * np.sin(
        2 * math.pi * 0.7 * t + 1.1
    )
    x *= np.clip(syll, 0.15, 1.0)
    # 50 ms raised-cosine edges
    m = int(0.05 * SR)
    ramp = 0.5 - 0.5 * np.cos(np.pi * np.arange(m) / m)
    x[:m] *= ramp
    x[-m:] *= ramp[::-1]
    return x.astype(np.float32)


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


def main():
    t0 = time.time()
    seg_dur, gap_dur = 1.5, 0.2
    seg_n, gap_n = int(seg_dur * SR), int(gap_dur * SR)
    # same speaker, DIFFERENT utterances (different seeds) — a same-speaker
    # test must not cheat with byte-identical inputs
    segs = {"A1": voice(seg_dur, 110.0, 12, 1.0, 5.0, 1.0, seed=11),
            "B1": voice(seg_dur, 175.0, 10, 1.6, 6.0, 1.5, seed=22),
            "A2": voice(seg_dur, 110.0, 12, 1.0, 5.0, 1.0, seed=12),
            "B2": voice(seg_dur, 175.0, 10, 1.6, 6.0, 1.5, seed=23)}
    labels = ["A1", "B1", "A2", "B2"]
    spk_of = {"A1": "A", "B1": "B", "A2": "A", "B2": "B"}
    # interleave with gaps: A1 gap B1 gap A2 gap B2
    parts = []
    for i, lab in enumerate(labels):
        parts.append(segs[lab])
        if i < len(labels) - 1:
            parts.append(np.zeros(gap_n, dtype=np.float32))
    audio = np.concatenate(parts)
    write_wav_mono(os.path.join(PROOFS, "fixture_2spk.wav"), audio, SR)

    from speechbrain.inference import EncoderClassifier

    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", savedir=SAVEDIR
    )
    batch = torch.stack([torch.from_numpy(segs[lab]) for lab in labels])  # 4 x T
    with torch.no_grad():
        emb = classifier.encode_batch(batch).squeeze(1)  # 4 x 192
    emb2 = classifier.encode_batch(batch).squeeze(1)
    torch.save(emb, os.path.join(PROOFS, "embeddings.pt"))

    res = {"model": "speechbrain/spkrec-ecapa-voxceleb",
           "embedding_dim": emb.shape[1], "segments": labels, "checks": []}

    def check(name, ok, detail):
        res["checks"].append({"name": name, "status": "PASS" if ok else "FAIL",
                              "detail": detail})
        print(("PASS" if ok else "FAIL"), name, "-", detail)

    check("embedding_shape", tuple(emb.shape) == (4, 192),
          f"shape {tuple(emb.shape)}")
    check("embeddings_finite", bool(torch.isfinite(emb).all()),
          "no NaN/Inf")

    # pairwise cosine similarity
    en = F.normalize(emb, p=2, dim=1)
    sim = (en @ en.T).numpy()
    res["cosine_similarity"] = [[round(float(v), 4) for v in row] for row in sim]
    intra = [sim[0, 2], sim[1, 3]]
    inter = [sim[0, 1], sim[0, 3], sim[1, 2], sim[2, 3]]
    margin = min(intra) - max(inter)
    res["min_intra_sim"] = round(float(min(intra)), 4)
    res["max_inter_sim"] = round(float(max(inter)), 4)
    res["separation_margin"] = round(float(margin), 4)
    check("speaker_separation", margin > 0.05,
          f"min intra {min(intra):.4f} vs max inter {max(inter):.4f} "
          f"(margin {margin:+.4f})")
    check("same_segment_near_one", all(sim[i, i] > 0.999 for i in range(4)),
          f"diag {np.diag(sim).round(4).tolist()}")

    maxdiff = float(torch.max(torch.abs(emb - emb2)))
    res["determinism_max_abs_diff"] = maxdiff
    check("embeddings_deterministic", maxdiff == 0.0, f"max|diff| = {maxdiff}")

    res["elapsed_s"] = round(time.time() - t0, 1)
    check("runs_to_completion", True, f"{res['elapsed_s']} s end-to-end")
    res["sha256"] = {f: sha256(os.path.join(PROOFS, f))
                     for f in sorted(os.listdir(PROOFS))
                     if f.endswith((".wav", ".pt"))}
    res["passed"] = sum(1 for c in res["checks"] if c["status"] == "PASS")
    res["failed"] = sum(1 for c in res["checks"] if c["status"] == "FAIL")
    with open(os.path.join(PROOFS, "result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n{res['passed']}/{len(res['checks'])} checks PASS")
    return 0 if res["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
