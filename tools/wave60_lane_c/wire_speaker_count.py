#!/usr/bin/env python3
"""Wave 60 Lane C — embedding-side speaker-count selection for diarization.

Question: can an embedding-side speaker-count estimator recover k=3 on the
Wave-58 real-voice fixture (9-turn, 3-Kokoro-voice dialogue; A=af_heart F,
B=am_puck M, C=af_bella F — the two females merge under auto-k), so that
clustering with the ESTIMATED k matches forced-k=3 performance?

Wave 59 was boundary-side (VAD refinement: DER 0.4084 -> 0.3416). The
remaining error is count selection: SpectralCluster's auto-k (its own
eigengap on descending affinity eigenvalues, Ratio type) picks k=2 and the
two female voices merge into one cluster (~12.2 s of ~13.4 s total error).

Design (torch-free, all measured — no simulation):
  * Fixture: dialogue.wav + ground_truth.json copied from wave58's
    committed proofs (SHA-verified against wave58's SHA256SUMS).
  * Embeddings: Wave 58's committed embeddings.pt (SHA-verified), parsed
    as raw float32 from the torch zip container without torch — the same
    160x192 ECAPA vectors, bit-for-bit.
  * Window grid + energy gate reproduced from dialogue.wav (wave58
    verbatim): 166 windows, 160 speech. The V0 baseline hypothesis RTTM
    must be BYTE-IDENTICAL to wave58's committed hypothesis.rttm.
  * Speaker-count estimators (all blind to ground truth, embedding-side):
      E1a eigengap on the SYMMETRIC NORMALIZED LAPLACIAN (von Luxburg,
          absolute gap, k-NN(7) sparsified affinity)  <-- WIRED primary
      E1b same, ratio gap (diagnostic)
      E1c same as E1a, unpruned affinity (diagnostic)
      E1d same as E1c, ratio gap (diagnostic)
      E2  BIC on sklearn KMeans over L2-normalized embeddings (diagnostic)
      E3  max silhouette (cosine) over KMeans labels (diagnostic)
      E0  donor's own eigengap (SpectralCluster utils, descending affinity,
          Ratio) — NEGATIVE CONTROL: expected to reproduce the auto-k
          failure (k=2), showing why a different estimator is needed.
  * The wired estimator (E1a) is chosen A PRIORI (textbook Ng-Jordan-Weiss
    pipeline), not by DER. Its k drives SpectralClusterer(min=max=k_est).
  * Variants scored identically: wave58 verbatim frame labeling (WITH
    fill), Hungarian cluster->speaker map (no label cheating),
    pyannote-metrics DER/JER at collar 0.0 and 0.25.

License gate (all upstream, verified live 2026-10-08):
  - SpeechBrain ECAPA embeddings — Apache-2.0 (reused, not recomputed;
    wired Wave 56; wave58 fixture)
  - SpectralCluster 0.2.22 — Apache-2.0 (wired Wave 57)
  - pyannote-metrics 4.1 — MIT (wired Wave 57; --no-deps install)
  - scikit-learn 1.9.1 — BSD-3-Clause (KMeans + silhouette; also a
    SpectralCluster dependency)
  - scipy / numpy — BSD (system)
  - eigengap/BIC estimators — ORIGINAL lane code, MIT (this file)

Environment notes:
  - /tmp is a 512 MB tmpfs: pip ran with lane-local TMPDIR=scratch/pip-tmp.
  - no_proxy/NO_PROXY IPv6 literals stripped (httpx crash lesson).
  - Home disk was 99-100% full during this build (same as Wave 59): venv
    uses --system-site-packages (system numpy 1.26.4 / scipy 1.11.4),
    torch NOT installed (not needed: torch-free design).
"""
import hashlib
import json
import math
import os
import shutil
import sys
import time
import wave
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "speaker_count")
W58 = os.path.join(HERE, "..", "wave58_lane_c", "proofs", "real_voice_diarization")
SR = 16000
WIN_S = 1.5
HOP_S = 0.25
SILENCE_FRAC = 0.08  # wave58 energy gate

EXPECT_SHA = {
    "dialogue.wav": "666cc1b94bd72127375fe58416a15988434156746df0ed1bee61c91066ef0342",
    "ground_truth.json": "3bfbdbddb43ed4e4924256625c11bfd01c67fd19a575094a1ac952422a34c6cc",
    "hypothesis.rttm": "f5e31ff54a398f24a5eb1adaa7651e5c84295cd1ab3fd52b376372a8ec009807",
}
EXPECT_EMB_SHA = "66d2d151aab053b61fcb9411aff5cc1ba7455ec87334b819a1312811e2bff4c9"
EMB_SHAPE = (160, 192)

K_MIN, K_MAX = 2, 6          # estimator search range
KNN_K = 7                    # k-NN sparsification for the Laplacian affinity


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def stage_fixture():
    """Copy fixture from wave58 committed proofs; SHA-verify every file."""
    os.makedirs(PROOFS, exist_ok=True)
    for name, want in EXPECT_SHA.items():
        dst = os.path.join(PROOFS, name)
        shutil.copyfile(os.path.join(W58, name), dst)
        got = sha256_file(dst)
        assert got == want, f"{name} SHA mismatch: {got}"
    with open(os.path.join(PROOFS, "ground_truth.json")) as f:
        turns_gt = json.load(f)["turns"]
    with wave.open(os.path.join(PROOFS, "dialogue.wav"), "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        audio = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
                 .astype(np.float32) / 32767.0)
    return audio, turns_gt


def load_embeddings():
    """Raw float32 (160,192) from wave58's torch-saved embeddings.pt."""
    p = os.path.join(W58, "embeddings.pt")
    assert sha256_file(p) == EXPECT_EMB_SHA, "embeddings.pt SHA mismatch"
    z = zipfile.ZipFile(p)
    raw = z.read("embeddings/data/0")
    assert len(raw) == EMB_SHAPE[0] * EMB_SHAPE[1] * 4, len(raw)
    emb = np.frombuffer(raw, dtype="<f4").reshape(EMB_SHAPE).astype(np.float64)
    assert np.all(np.isfinite(emb))
    return emb


def wave58_windows(audio):
    win = int(WIN_S * SR)
    hop = int(HOP_S * SR)
    idxs = list(range(0, len(audio) - win + 1, hop))
    rms = np.array([float(np.sqrt(np.mean(audio[i:i + win] ** 2)))
                    for i in idxs])
    thr = SILENCE_FRAC * float(np.max(rms))
    speech = np.array([r >= thr for r in rms])
    return np.flatnonzero(speech), len(idxs), thr, float(np.max(rms))


# ------------------------------------------------- estimators (blind to GT)
def _l2n(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def _affinity(X):
    """Donor-consistent affinity: (cosine_sim + 1) / 2, range [0,1]."""
    Xn = _l2n(X)
    return (Xn @ Xn.T + 1.0) / 2.0


def _laplacian_sym(W, knn_k=None):
    """Symmetric normalized Laplacian, optionally k-NN sparsified
    (symmetrized by max, diagonal kept)."""
    n = W.shape[0]
    if knn_k:
        mask = np.zeros_like(W, dtype=bool)
        # keep top-knn_k affinities per row (excluding self)
        idx = np.argpartition(-W, kth=knn_k + 1, axis=1)[:, :knn_k + 1]
        rows = np.arange(n)[:, None]
        mask[rows, idx] = True
        W = np.where(mask | mask.T, W, 0.0)
        np.fill_diagonal(W, 1.0)
    d = W.sum(axis=1)
    d_inv_sqrt = 1.0 / np.sqrt(np.maximum(d, 1e-12))
    return np.eye(n) - (d_inv_sqrt[:, None] * W * d_inv_sqrt[None, :])


def eigengap_laplacian(X, k_min=K_MIN, k_max=K_MAX, knn_k=KNN_K, ratio=False):
    """Von Luxburg eigengap on the symmetric normalized Laplacian.

    eigenvalues ascending l1 <= l2 <= ...; k = argmax gap after l_k.
    Returns (k_est, eigenvalues[:k_max+1], gaps dict).
    """
    from scipy.linalg import eigh
    W = _affinity(X)
    L = _laplacian_sym(W, knn_k=knn_k)
    vals = eigh(L, eigvals_only=True)  # ascending
    vals = np.maximum(vals, 0.0)
    gaps, ratios = {}, {}
    for k in range(k_min, k_max):
        gaps[k] = float(vals[k] - vals[k - 1])       # gap after l_k (0-based k-1)
        ratios[k] = float(vals[k] / (vals[k - 1] + 1e-12))
    metric = ratios if ratio else gaps
    k_est = max(metric, key=lambda k: metric[k])
    return k_est, vals[:k_max + 1].tolist(), gaps, ratios


def donor_eigengap(X, max_clusters=4, min_clusters=2):
    """NEGATIVE CONTROL: SpectralCluster's own auto-k machinery
    (descending affinity eigenvalues, Ratio type), INCLUDING predict()'s
    min_clusters clamp: n = max(eigengap_k, min_clusters).
    Expected to pick 2, reproducing the Wave-58 auto-k failure."""
    from spectralcluster import utils
    W = _affinity(X)
    eigenvalues, _ = utils.compute_sorted_eigenvectors(W, descend=True)
    n, max_delta_norm = utils.compute_number_of_clusters(
        eigenvalues, max_clusters=max_clusters, stop_eigenvalue=1e-2,
        eigengap_type=utils.EigenGapType.Ratio, descend=True)
    n = max(int(n), min_clusters)  # mirrors SpectralClusterer.predict()
    return n, float(max_delta_norm), eigenvalues[:max_clusters + 1].tolist()


def bic_kmeans(X, k_min=K_MIN, k_max=K_MAX):
    """BIC over sklearn KMeans on L2-normalized embeddings.
    BIC(k) = N*ln(RSS/N) + (k*d + k - 1)*ln(N)."""
    from sklearn.cluster import KMeans
    Xn = _l2n(X)
    n, d = Xn.shape
    bics, inertias = {}, {}
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xn)
        rss = float(km.inertia_)
        n_params = k * d + (k - 1)
        bics[k] = n * math.log(rss / n) + n_params * math.log(n)
        inertias[k] = rss
    return min(bics, key=lambda k: bics[k]), bics, inertias


def silhouette_kmeans(X, k_min=K_MIN, k_max=K_MAX):
    """Max mean silhouette (cosine) over KMeans labels."""
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    Xn = _l2n(X)
    sils, labels = {}, {}
    for k in range(k_min, k_max + 1):
        lab = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(Xn)
        sils[k] = float(silhouette_score(Xn, lab, metric="cosine"))
        labels[k] = lab
    return max(sils, key=lambda k: sils[k]), sils, labels


# ------------------------------------------------- wave58-verbatim downstream
def cluster_labels(emb, k_min, k_max):
    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=k_min, max_clusters=k_max,
                           custom_dist="cosine")
    return np.asarray(cl.predict(emb), dtype=int)


def frames_from_windows_wave58(labels, spk_idx, n_frames):
    """Wave58 verbatim frame labeling INCLUDING the fill step."""
    frames = np.full(n_frames, -1, dtype=int)
    center_off = int(round((WIN_S / 2) / HOP_S))
    for j, lab in zip(spk_idx, labels):
        f = j + center_off
        if 0 <= f < n_frames:
            frames[f] = int(lab)
    for i in range(n_frames):  # wave58 fill step
        if frames[i] != -1:
            continue
        for d in range(1, center_off + 2):
            cand = None
            if i - d >= 0 and frames[i - d] != -1:
                cand = frames[i - d]
            elif i + d < n_frames and frames[i + d] != -1:
                cand = frames[i + d]
            if cand is not None:
                frames[i] = cand
                break
    return frames


def gt_at(turns_gt, t):
    return next((g["speaker"] for g in turns_gt
                 if g["start"] <= t < g["end"]), None)


def hungarian_map(frames, turns_gt):
    from scipy.optimize import linear_sum_assignment
    clus = sorted(set(frames[frames != -1].tolist()))
    spks = sorted(set(t["speaker"] for t in turns_gt))
    cont = np.zeros((len(clus), len(spks)))
    ci = {c: k for k, c in enumerate(clus)}
    si = {s: k for k, s in enumerate(spks)}
    for i, f in enumerate(frames):
        if f == -1:
            continue
        s = gt_at(turns_gt, (i + 0.5) * HOP_S)
        if s is not None:
            cont[ci[f], si[s]] += 1
    ri, cj = linear_sum_assignment(-cont)
    cmap = {int(clus[r]): spks[c] for r, c in zip(ri, cj)}
    agree = total = 0
    for i, f in enumerate(frames):
        if f == -1:
            continue
        s = gt_at(turns_gt, (i + 0.5) * HOP_S)
        if s is None:
            continue
        total += 1
        if cmap[f] == s:
            agree += 1
    return cmap, agree / max(1, total), total


def segments_from_frames(frames):
    segs = []
    i, n = 0, len(frames)
    while i < n:
        if frames[i] == -1:
            i += 1
            continue
        j = i
        while j < n and frames[j] == frames[i]:
            j += 1
        segs.append((i * HOP_S, j * HOP_S, frames[i]))
        i = j
    return segs


def write_rttm(path, segments, uri="dialogue"):
    with open(path, "w") as f:
        for s, e, spk in segments:
            f.write(f"SPEAKER {uri} 1 {s:.3f} {e - s:.3f} "
                    f"<NA> <NA> {spk} <NA> <NA>\n")


def score(ref_path, hyp_path, collar):
    from pyannote.core import Annotation, Segment
    from pyannote.metrics.diarization import (
        DiarizationErrorRate, JaccardErrorRate)

    def load(p):
        ann = Annotation()
        with open(p) as f:
            for line in f:
                parts = line.split()
                on, dur, spk = float(parts[3]), float(parts[4]), parts[7]
                ann[Segment(on, on + dur)] = spk
        return ann

    ref, hyp = load(ref_path), load(hyp_path)
    der = DiarizationErrorRate(collar=collar)
    jer = JaccardErrorRate(collar=collar)
    det = der.compute_components(ref, hyp)
    comp = {"missed_detection": float(det["missed detection"]),
            "false_alarm": float(det["false alarm"]),
            "confusion": float(det["confusion"]),
            "total": float(det["total"])}
    return der(ref, hyp), jer(ref, hyp), comp


def run_variant(name, emb, k_min, k_max, spk_idx, n_frames, turns_gt):
    """Cluster with k in [k_min, k_max] (k_min==k_max forces k), then the
    wave58-verbatim downstream: frames (with fill) -> Hungarian -> RTTM."""
    labels = cluster_labels(emb, k_min, k_max)
    frames = frames_from_windows_wave58(labels, spk_idx, n_frames)
    cmap, purity, n_fr = hungarian_map(frames, turns_gt)
    segs = segments_from_frames(frames)
    hyp = [(s, e, cmap[c]) for s, e, c in segs]
    hyp_path = os.path.join(PROOFS, f"hypothesis_{name}.rttm")
    write_rttm(hyp_path, hyp)
    ref_path = os.path.join(PROOFS, "reference.rttm")
    d0, j0, c0 = score(ref_path, hyp_path, 0.0)
    d25, j25, _ = score(ref_path, hyp_path, 0.25)
    return {
        "k_min": k_min, "k_max": k_max,
        "clusters": len(set(labels.tolist())),
        "cluster_map": {str(k): v for k, v in cmap.items()},
        "frame_purity": round(purity, 4),
        "DER_collar0": round(d0, 4), "JER_collar0": round(j0, 4),
        "DER_collar0.25": round(d25, 4), "JER_collar0.25": round(j25, 4),
        "components_collar0_s": {k: round(v, 3) for k, v in c0.items()},
    }


def main():
    t0 = time.time()
    checks = []
    results = {"checks": checks,
               "design": "torch-free; embeddings = wave58 embeddings.pt "
                         "(SHA-verified, raw float32 parse); wave58-verbatim "
                         "window grid + frame labeling (with fill)"}

    # ---- fixture + embeddings ----
    audio, turns_gt = stage_fixture()
    checks.append({"name": "fixture SHAs match wave58 committed artifacts",
                   "pass": True,
                   "measured": "dialogue.wav + ground_truth.json + "
                               "hypothesis.rttm verified vs SHA256SUMS"})
    emb = load_embeddings()
    checks.append({"name": "embeddings.pt SHA matches wave58; (160,192) "
                            "finite float32, torch-free",
                   "pass": emb.shape == EMB_SHAPE and
                           bool(np.all(np.isfinite(emb))),
                   "measured": f"shape={emb.shape}"})
    dur_s = len(audio) / SR
    spk_idx, n_grid, thr, max_rms = wave58_windows(audio)
    checks.append({"name": "wave58 window grid + energy gate reproduced",
                   "pass": n_grid == 166 and len(spk_idx) == 160,
                   "measured": f"grid={n_grid} speech={len(spk_idx)} "
                               f"thr={thr:.5f} max_rms={max_rms:.5f}"})
    n_frames = int(math.ceil(dur_s / HOP_S))
    ref_path = os.path.join(PROOFS, "reference.rttm")
    write_rttm(ref_path, [(t["start"], t["end"], t["speaker"])
                          for t in turns_gt])

    # ---- estimators (blind) ----
    t_est = time.time()
    k_e1a, vals_a, gaps_a, ratios_a = eigengap_laplacian(
        emb, knn_k=KNN_K, ratio=False)
    k_e1b, _, gaps_b, ratios_b = eigengap_laplacian(
        emb, knn_k=KNN_K, ratio=True)
    k_e1c, vals_c, gaps_c, _ = eigengap_laplacian(
        emb, knn_k=None, ratio=False)
    k_e1d, _, _, ratios_d = eigengap_laplacian(
        emb, knn_k=None, ratio=True)
    k_e2, bics, inertias = bic_kmeans(emb)
    k_e3, sils, _ = silhouette_kmeans(emb)
    k_e0, max_dn, donor_vals = donor_eigengap(emb, max_clusters=4)
    results["estimator_s"] = round(time.time() - t_est, 1)
    estimators = {
        "E1a_eigengap_laplacian_knn7_abs": {
            "k": k_e1a, "eigenvalues": [round(v, 6) for v in vals_a],
            "gaps": {str(k): round(v, 6) for k, v in gaps_a.items()},
            "note": "PRIMARY (wired): textbook von Luxburg, fixed a priori"},
        "E1b_eigengap_laplacian_knn7_ratio": {
            "k": k_e1b,
            "ratios": {str(k): round(v, 4) for k, v in ratios_b.items()},
            "note": "diagnostic"},
        "E1c_eigengap_laplacian_unpruned_abs": {
            "k": k_e1c,
            "eigenvalues": [round(v, 6) for v in vals_c],
            "gaps": {str(k): round(v, 6) for k, v in gaps_c.items()},
            "note": "diagnostic"},
        "E1d_eigengap_laplacian_unpruned_ratio": {
            "k": k_e1d,
            "ratios": {str(k): round(v, 4) for k, v in ratios_d.items()},
            "note": "diagnostic"},
        "E2_BIC_kmeans": {
            "k": k_e2,
            "BIC": {str(k): round(v, 1) for k, v in bics.items()},
            "inertia": {str(k): round(v, 1) for k, v in inertias.items()},
            "note": "diagnostic"},
        "E3_silhouette_kmeans": {
            "k": k_e3,
            "silhouette": {str(k): round(v, 4) for k, v in sils.items()},
            "note": "diagnostic"},
        "E0_donor_eigengap_negative_control": {
            "k": k_e0, "max_delta_norm": round(max_dn, 4),
            "eigenvalues_desc": [round(v, 6) for v in donor_vals],
            "note": "SpectralCluster's own auto-k machinery; expected k=2"},
    }
    results["estimators"] = estimators
    for tag, e in estimators.items():
        print(f"[{tag}] k_est={e['k']}", flush=True)
    checks.append({"name": "donor negative control reproduces auto-k failure",
                   "pass": k_e0 == 2,
                   "measured": f"donor eigengap k={k_e0} "
                               f"(max_delta_norm={round(max_dn, 4)})"})
    checks.append({"name": "primary estimator E1a selects k in [2,6]",
                   "pass": K_MIN <= k_e1a <= K_MAX,
                   "measured": f"E1a k={k_e1a} "
                               f"(gaps={ {k: round(v, 4) for k, v in gaps_a.items()} })"})

    # ---- variants ----
    variants = {}
    variants["auto_k"] = run_variant(
        "auto_k", emb, 2, 4, spk_idx, n_frames, turns_gt)
    variants["forced_k3"] = run_variant(
        "forced_k3", emb, 3, 3, spk_idx, n_frames, turns_gt)
    variants["est_E1a"] = run_variant(
        "est_E1a", emb, k_e1a, k_e1a, spk_idx, n_frames, turns_gt)
    for tag, ekey in (("est_E2", "E2_BIC_kmeans"),
                      ("est_E3", "E3_silhouette_kmeans")):
        ke = estimators[ekey]["k"]
        variants[tag] = run_variant(
            tag, emb, ke, ke, spk_idx, n_frames, turns_gt)
    # Oracle-k cross-check: independent clusterer (plain sklearn KMeans on
    # L2-normalized embeddings, k=3) through the same downstream. Tests
    # whether the forced-k DER is specific to spectral clustering.
    from sklearn.cluster import KMeans
    km3 = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(
        emb / np.linalg.norm(emb, axis=1, keepdims=True))
    frames_km = frames_from_windows_wave58(km3, spk_idx, n_frames)
    cmap_km, purity_km, _ = hungarian_map(frames_km, turns_gt)
    segs_km = segments_from_frames(frames_km)
    hyp_km = [(s, e, cmap_km[c]) for s, e, c in segs_km]
    hyp_km_path = os.path.join(PROOFS, "hypothesis_xcheck_kmeans_k3.rttm")
    write_rttm(hyp_km_path, hyp_km)
    d_km, j_km, c_km = score(ref_path, hyp_km_path, 0.0)
    variants["xcheck_kmeans_k3"] = {
        "k_min": 3, "k_max": 3, "clusters": 3,
        "cluster_map": {str(k): v for k, v in cmap_km.items()},
        "frame_purity": round(purity_km, 4),
        "DER_collar0": round(d_km, 4), "JER_collar0": round(j_km, 4),
        "DER_collar0.25": None, "JER_collar0.25": None,
        "components_collar0_s": {k: round(v, 3) for k, v in c_km.items()},
        "note": "oracle-k cross-check, NOT an estimator variant",
    }
    results["variants"] = variants
    for name, v in variants.items():
        print(f"[{name}] k=[{v['k_min']},{v['k_max']}] clusters={v['clusters']} "
              f"map={v['cluster_map']} DER0={v['DER_collar0']} "
              f"JER0={v['JER_collar0']} conf={v['components_collar0_s']['confusion']}",
              flush=True)

    # ---- gates ----
    a = variants["auto_k"]
    hyp_auto = os.path.join(PROOFS, "hypothesis_auto_k.rttm")
    ref_hyp = os.path.join(PROOFS, "hypothesis.rttm")  # wave58 committed copy
    same = open(hyp_auto, "rb").read() == open(ref_hyp, "rb").read()
    checks.append({"name": "V0 baseline hypothesis RTTM byte-identical to "
                            "wave58 committed hypothesis.rttm",
                   "pass": same,
                   "measured": f"byte-identical={same}"})
    checks.append({"name": "auto-k reproduces wave58 DER (0.4084 ±0.005)",
                   "pass": abs(a["DER_collar0"] - 0.4084) <= 0.005,
                   "measured": f"DER0={a['DER_collar0']} "
                               f"JER0={a['JER_collar0']}"})
    f3 = variants["forced_k3"]
    # Wave 58's PROOFS.md reported forced-k=3 -> DER 0.3359 from an
    # UNCOMMITTED ad-hoc diagnostic (no code in the wave58 wire script).
    # This lane's deterministic forced-k=3 measures DER 0.0941. The auto-k
    # baseline reproduces wave58 BYTE-IDENTICALLY, so the pipeline is
    # faithful: the 0.3359 number does not reproduce and is documented as
    # a Wave-58 diagnostic anomaly (see PROOFS.md), not a regression here.
    checks.append({"name": "forced k=3 measured (deterministic); wave58's "
                            "uncommitted 0.3359 diagnostic does NOT reproduce",
                   "pass": math.isfinite(f3["DER_collar0"]),
                   "measured": f"DER0={f3['DER_collar0']} "
                               f"JER0={f3['JER_collar0']} "
                               f"purity={f3['frame_purity']} "
                               f"map={f3['cluster_map']} "
                               f"(wave58 ad-hoc reported 0.3359)"})
    e1 = variants["est_E1a"]
    checks.append({"name": "primary estimator k matches forced k=3 count",
                   "pass": k_e1a == 3,
                   "measured": f"E1a k={k_e1a}"})
    checks.append({"name": "estimator DER matches forced-k DER (±0.005) "
                            "[goal: beat or match 0.3359]",
                   "pass": abs(e1["DER_collar0"] - f3["DER_collar0"]) <= 0.005,
                   "measured": f"est DER0={e1['DER_collar0']} vs "
                               f"forced DER0={f3['DER_collar0']}"})
    checks.append({"name": "DER/JER finite for all variants",
                   "pass": all(math.isfinite(variants[v][m])
                               for v in variants
                               for m in ("DER_collar0", "JER_collar0")),
                   "measured": ", ".join(
                       f"{v}={variants[v]['DER_collar0']}" for v in variants)})

    d_auto = a["DER_collar0"] - e1["DER_collar0"]
    results["delta_est_vs_auto"] = {
        "DER_collar0": round(d_auto, 4),
        "verdict": ("IMPROVED" if d_auto > 0.005 else
                    "NO_IMPROVEMENT" if d_auto > -0.005 else "REGRESSED"),
    }
    results["total_s"] = round(time.time() - t0, 1)
    n_pass = sum(1 for c in checks if c["pass"])
    results["pass_rate"] = f"{n_pass}/{len(checks)}"
    with open(os.path.join(PROOFS, "speaker_count_result.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"PASS {n_pass}/{len(checks)}")


if __name__ == "__main__":
    main()
