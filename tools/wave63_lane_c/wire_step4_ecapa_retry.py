#!/usr/bin/env python3
"""Wave 63 Lane C — step-4 ECAPA downstream-mix diagnostic, RETRY.

Wave-62 §7.1: the ECAPA process was SIGKILLed (OOM killer) 4 times on the
shared VM — twice inside the full stage-2 script (alongside DeepFilterNet3),
twice as a standalone low-thread process. The VM was memory-constrained
during those runs; the diagnostic was omitted rather than simulated.

This retry runs ECAPA-TDNN (SpeechBrain spkrec-ecapa-voxceleb, Apache-2.0)
in its OWN process with threads pinned to 1 and windows batched (32 at a
time) to keep peak RSS low, on the quieter VM.

Diagnostic ("quarantined effect" check): GT-mean cosine similarity between
the three speaker means computed on (a) the downstream-denoised clean mix
(Wave-62 `downstream_denoised_mix.wav` — denoise applied ONLY after
diarization, per-speaker segments cut on hypothesis boundaries) and (b) the
RAW fixture audio (dialogue.wav) as a matched control, same model, same
windowing (1.5 s / 0.25 s). If downstream denoise pushed the two female
means together the way UPSTREAM denoise did in Wave-61 (cos A/C 0.5905 ->
0.7438 on noisy), it shows here. Denoise placement is downstream-only in
production, so the speaker path never sees this audio — this is a
GT-informed bonus diagnostic, not part of the blind pipeline.
"""
import json
import os
import sys
import wave

import numpy as np

import os as _os
_os.environ.setdefault("OMP_NUM_THREADS", "1")
_os.environ.setdefault("MKL_NUM_THREADS", "1")
_os.environ.setdefault("MALLOC_ARENA_MAX", "2")

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "step4")
W58 = os.path.join(HERE, "..", "wave58_lane_c", "proofs",
                   "real_voice_diarization")
W62 = os.path.join(HERE, "..", "wave62_lane_c", "proofs", "downstream")
GT_PATH = os.path.join(W58, "ground_truth.json")
SCRATCH = os.path.join(HERE, "scratch", "step4")
SR = 16000
BATCH = 32


def read_wav_mono(path):
    with wave.open(path, "rb") as w:
        n = w.getnframes()
        raw = w.readframes(n)
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def gt_mean_cosines(embedder, torch, mix, turns):
    win, hop = int(1.5 * SR), int(0.25 * SR)
    idxs = list(range(0, len(mix) - win + 1, hop))
    embs = []
    for s in range(0, len(idxs), BATCH):
        chunk = idxs[s:s + BATCH]
        batch = torch.stack([torch.from_numpy(mix[i:i + win]) for i in chunk])
        with torch.no_grad():
            e = embedder.encode_batch(batch).squeeze(1).numpy()
        embs.append(e)
    emb = np.concatenate(embs, axis=0)
    win_spk = [next((g["speaker"] for g in turns
                     if g["start"] <= i * 0.25 + 0.75 < g["end"]), None)
               for i in idxs]
    means = {}
    for spk in ("A", "B", "C"):
        ix = [i for i, g in enumerate(win_spk) if g == spk]
        m_ = emb[ix].mean(axis=0)
        means[spk] = m_ / (np.linalg.norm(m_) + 1e-12)
    cos = {f"{a}{b}": round(float(means[a] @ means[b]), 4)
           for a, b in (("A", "B"), ("A", "C"), ("B", "C"))}
    return cos, len(idxs)


def main():
    os.makedirs(PROOFS, exist_ok=True)
    os.makedirs(SCRATCH, exist_ok=True)
    mix_dn = read_wav_mono(os.path.join(W62, "downstream_denoised_mix.wav"))
    mix_raw = read_wav_mono(os.path.join(W58, "dialogue.wav"))
    turns = json.load(open(GT_PATH))["turns"]

    from speechbrain.inference import EncoderClassifier
    embedder = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=os.path.join(SCRATCH, "speechbrain_models"))
    import torch
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)

    cos_dn, n_dn = gt_mean_cosines(embedder, torch, mix_dn, turns)
    print("diag_cos_downstream_denoised:", cos_dn)
    cos_raw, n_raw = gt_mean_cosines(embedder, torch, mix_raw, turns)
    print("diag_cos_raw_control:", cos_raw)

    out = {"diag_cos_downstream_denoised": cos_dn,
           "n_windows_denoised": n_dn,
           "diag_cos_raw_control": cos_raw,
           "n_windows_raw": n_raw,
           "model": "speechbrain/spkrec-ecapa-voxceleb",
           "batch": BATCH,
           "note": "GT-informed bonus diagnostic; production speaker path "
                   "never sees denoised audio (Wave-61 law: denoise "
                   "downstream of embeddings only)"}
    with open(os.path.join(PROOFS, "step4_ecapa_retry.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("STEP4_RETRY_DONE")


if __name__ == "__main__":
    main()
