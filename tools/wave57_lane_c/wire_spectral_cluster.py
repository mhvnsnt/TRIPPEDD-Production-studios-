#!/usr/bin/env python3
"""Wave 57 Lane C — wire SpectralCluster + pyannote-metrics on REAL data.

Stage 3 of the measured diarization pipeline:
  embeddings (Wave 56, real SpeechBrain ECAPA 192-dim, 2-speaker fixture)
      -> SpectralCluster (Apache-2.0) clustering
      -> pyannote-metrics (MIT) DER / JER scoring against RTTM ground truth

Inputs (all from the committed Wave-56 run, re-verified by SHA-256):
  tools/wave56_lane_c/proofs/speechbrain_ecapa/embeddings.pt
    (4 x 192 tensor, segments A1, B1, A2, B2 — synthetic 2-speaker dialogue)
  Ground truth segment timing (from wire_speechbrain_ecapa.py: seg_dur=1.5s,
    gap_dur=0.2s, order A1 gap B1 gap A2 gap B2, SR=16000):
    A1 [0.0, 1.5) spk A | B1 [1.7, 3.2) spk B | A2 [3.4, 4.9) spk A | B2 [5.1, 6.6) spk B

Outputs (proofs/spectral_cluster/):
  reference.rttm, hypothesis.rttm, result.json

pyannote.audio (gated HF model terms) is explicitly NOT used — permissive-only
rule. Only pyannote-metrics (MIT, pure metrics library) is wired here.
"""
import hashlib
import json
import os
import time

import numpy as np
import torch
from pyannote.core import Annotation, Segment
from pyannote.metrics.diarization import DiarizationErrorRate, JaccardErrorRate
from scipy.optimize import linear_sum_assignment
from sklearn.metrics.cluster import contingency_matrix

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EMB_PATH = os.path.join(REPO, "tools", "wave56_lane_c", "proofs",
                        "speechbrain_ecapa", "embeddings.pt")
EMB_SHA_W56 = ("79eff78da81791da8e5fc20b6cb0c26505b3196a58bddeab1f7c0fa8863d86e4")
PROOFS = os.path.join(HERE, "proofs", "spectral_cluster")
os.makedirs(PROOFS, exist_ok=True)

URI = "wave56_fixture_2spk"
# (start, end, speaker) — from Wave-56 fixture layout, seg_dur=1.5, gap=0.2
REF_SEGS = [(0.0, 1.5, "A"), (1.7, 3.2, "B"), (3.4, 4.9, "A"), (5.1, 6.6, "B")]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_rttm(path, segs):
    with open(path, "w") as f:
        for start, end, spk in segs:
            f.write(f"SPEAKER {URI} 1 {start:.2f} {end - start:.2f} "
                    f"<NA> <NA> {spk} <NA> <NA>\n")


def rttm_to_annotation(path):
    ann = Annotation(uri=URI)
    with open(path) as f:
        for line in f:
            parts = line.split()
            if not parts or parts[0] != "SPEAKER":
                continue
            start, dur, spk = float(parts[3]), float(parts[4]), parts[7]
            ann[Segment(start, start + dur)] = spk
    return ann


def main():
    t0 = time.time()
    checks = []

    def check(name, ok, detail):
        checks.append({"name": name, "status": "PASS" if ok else "FAIL",
                       "detail": detail})
        print(("PASS" if ok else "FAIL"), name, "—", detail)

    # 1. Re-verify the Wave-56 input artifact (same bytes, not re-generated)
    emb_sha = sha256(EMB_PATH)
    check("embeddings_pt_sha256_matches_wave56",
          emb_sha == EMB_SHA_W56,
          f"sha256={emb_sha[:16]}… {'matches' if emb_sha == EMB_SHA_W56 else 'MISMATCH'}")

    emb = torch.load(EMB_PATH, map_location="cpu", weights_only=True).float()
    X = emb.numpy()
    check("embedding_shape", tuple(X.shape) == (4, 192), f"shape {tuple(X.shape)}")
    check("embeddings_finite", bool(np.isfinite(X).all()), "no NaN/Inf")

    # 2. SpectralCluster — embeddings in, speaker labels out
    from spectralcluster import SpectralClusterer
    clusterer = SpectralClusterer(min_clusters=2, max_clusters=4,
                                  custom_dist="cosine")
    labels = clusterer.predict(X)
    labels2 = clusterer.predict(X)  # determinism re-run
    n_clusters = int(np.max(labels) + 1)
    check("cluster_count_is_2", n_clusters == 2,
          f"{n_clusters} clusters: {labels.tolist()}")
    check("cluster_deterministic", bool(np.array_equal(labels, labels2)),
          f"re-run identical: {labels2.tolist()}")

    # 3. Optimal cluster-id -> speaker-id mapping (Hungarian on contingency)
    ref_labels = [spk for _, _, spk in REF_SEGS]
    cont = contingency_matrix(ref_labels, labels)
    row, col = linear_sum_assignment(-cont)
    mapping = {int(col[i]): row[i] for i in range(len(row))}  # cluster -> ref idx
    spk_of_row = sorted(set(ref_labels))
    hyp_segs = [(s, e, spk_of_row[mapping[int(labels[i])]])
                for i, (s, e, _) in enumerate(REF_SEGS)]

    # label purity: A1/A2 same cluster, B1/B2 same cluster, A!=B
    purity_ok = (labels[0] == labels[2] and labels[1] == labels[3]
                 and labels[0] != labels[1])
    check("speaker_purity", bool(purity_ok),
          f"A1/A2->c{int(labels[0])}, B1/B2->c{int(labels[1])}, "
          f"map { {int(k): spk_of_row[v] for k, v in mapping.items()} }")

    # 4. RTTM round-trip (artifacts on disk), then pyannote-metrics scoring
    ref_path = os.path.join(PROOFS, "reference.rttm")
    hyp_path = os.path.join(PROOFS, "hypothesis.rttm")
    write_rttm(ref_path, REF_SEGS)
    write_rttm(hyp_path, hyp_segs)
    ref_ann = rttm_to_annotation(ref_path)
    hyp_ann = rttm_to_annotation(hyp_path)

    der_metric = DiarizationErrorRate()
    jer_metric = JaccardErrorRate()
    der = float(der_metric(ref_ann, hyp_ann))
    jer = float(jer_metric(ref_ann, hyp_ann))
    # decompose DER from this pair (pure recomputation on the same inputs)
    detail = der_metric.compute_components(ref_ann, hyp_ann)
    check("der_is_zero", der == 0.0, f"DER={der:.4f} (4/4 segments correct)")
    check("jer_is_zero", jer == 0.0, f"JER={jer:.4f} (per-speaker perfect)")

    elapsed = time.time() - t0
    check("runs_to_completion", True, f"{elapsed:.1f} s end-to-end")

    result = {
        "input_embeddings": EMB_PATH.replace(REPO + "/", ""),
        "input_sha256": emb_sha,
        "reference_segments": [
            {"start": s, "end": e, "speaker": spk} for s, e, spk in REF_SEGS],
        "cluster_labels": [int(x) for x in labels],
        "cluster_to_speaker": {str(k): spk_of_row[v]
                               for k, v in mapping.items()},
        "hypothesis_segments": [
            {"start": s, "end": e, "speaker": spk} for s, e, spk in hyp_segs],
        "DER": der,
        "JER": jer,
        "DER_breakdown": {k: float(detail.get(k, 0.0))
                          for k in ("miss", "false_alarm", "confusion", "total")},
        "elapsed_s": round(elapsed, 1),
        "checks": checks,
        "sha256": {os.path.basename(ref_path): sha256(ref_path),
                   os.path.basename(hyp_path): sha256(hyp_path)},
        "passed": sum(1 for c in checks if c["status"] == "PASS"),
        "failed": sum(1 for c in checks if c["status"] == "FAIL"),
    }
    res_path = os.path.join(PROOFS, "result.json")
    with open(res_path, "w") as f:
        json.dump(result, f, indent=2)
    result["sha256"]["result.json"] = sha256(res_path)
    with open(res_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n{result['passed']}/{len(checks)} PASS — wrote {res_path}")


if __name__ == "__main__":
    main()
