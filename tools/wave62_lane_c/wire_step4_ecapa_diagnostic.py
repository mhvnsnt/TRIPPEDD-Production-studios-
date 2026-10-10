#!/usr/bin/env python3
"""Wave 62 Lane C — step 4 standalone: GT-mean cosine diagnostic on the
downstream-denoised clean mix (fresh ECAPA pass). Runs in its own process so
no other model is in memory (the full stage-2 script was SIGKILLED twice when
this ran alongside DeepFilterNet3)."""
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
PROOFS = os.path.join(HERE, "proofs", "downstream")
W58 = os.path.join(HERE, "..", "wave58_lane_c", "proofs",
                   "real_voice_diarization")
GT_PATH = os.path.join(W58, "ground_truth.json")
SCRATCH = os.path.join(HERE, "scratch")
SR = 16000


def read_wav_mono(path):
    with wave.open(path, "rb") as w:
        n = w.getnframes()
        raw = w.readframes(n)
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


mix = read_wav_mono(os.path.join(PROOFS, "downstream_denoised_mix.wav"))
turns = json.load(open(GT_PATH))["turns"]

from speechbrain.inference import EncoderClassifier
embedder = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=os.path.join(SCRATCH, "speechbrain_models"))
import torch
torch.set_num_threads(1)
torch.set_num_interop_threads(1)

win, hop = int(1.5 * SR), int(0.25 * SR)
idxs = list(range(0, len(mix) - win + 1, hop))
batch = torch.stack([torch.from_numpy(mix[i:i + win]) for i in idxs])
with torch.no_grad():
    emb = embedder.encode_batch(batch).squeeze(1).numpy()
win_spk = [next((g["speaker"] for g in turns
                 if g["start"] <= i * 0.25 + 0.75 < g["end"]), None)
           for i in idxs]
means = {}
for s in ("A", "B", "C"):
    ix = [i for i, g in enumerate(win_spk) if g == s]
    m_ = emb[ix].mean(axis=0)
    means[s] = m_ / (np.linalg.norm(m_) + 1e-12)
cos = {f"{a}{b}": round(float(means[a] @ means[b]), 4)
       for a, b in (("A", "B"), ("A", "C"), ("B", "C"))}
print("diag_cos_downstream_denoised:", cos)
json.dump({"diag_cos_downstream_denoised": cos,
           "n_windows": len(idxs)},
          open(os.path.join(PROOFS, "step4_ecapa_diagnostic.json"), "w"),
          indent=2)
print("STEP4_DONE")
