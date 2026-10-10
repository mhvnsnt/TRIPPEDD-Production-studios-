#!/usr/bin/env python3
"""Wave 63 Lane C — VAD-coverage recovery on the Wave-62 rebuilt diarization
topology (denoise downstream of embeddings).

Context: the Wave-62 production topology (tuned webrtcvad VAD + dropped
boundary-straddling windows + frame labeling inside VAD speech only, NO fill)
measures DER 0.1158 / JER 0.1156 (miss 4.55 / FA 0.00 / conf 0.00) on the
Wave-58 9-turn 3-Kokoro-voice fixture. The Wave-60 baseline (same fixture,
full-window fill) measured DER 0.0941 / JER 0.0844 (miss 0.0 / FA 3.70 /
conf 0.0). The entire DER gap is a VAD-coverage trade-off: the Wave-58/60
fill step paints the 0.4 s inter-turn gaps (3.70 s FA), while V2c no-fill
leaves VAD-interior frames uncovered (4.55 s miss).

Experiment (only stage G — frame labeling — changes; windows, embeddings,
eigengap k, cluster labels are byte-identical across variants):

  F0  V2c no-fill (Wave-62 production verbatim) — control, must reproduce
      DER 0.1158 / JER 0.1156.
  F1  fill-within-VAD-speech (NEW): unlabeled frames whose center lies
      inside a VAD segment take the label of the temporally nearest labeled
      frame, where propagation is restricted to the same VAD segment (never
      across a VAD gap). VAD precision on this fixture is 1.0, so the fill
      should recover interior coverage without re-introducing gap FA.
  F2  Wave-58-style global fill: nearest labeled frame for EVERY frame
      (paints inter-turn gaps) — reproduces the miss->FA trade-off as the
      measured cost baseline.

Everything else is the Wave-62 main_clean pipeline reproduced verbatim
(torch-free: embeddings parsed raw float32 from the torch zip container,
same trick as Waves 59/60).

Licenses (wired path): webrtcvad MIT, SpectralCluster Apache-2.0,
pyannote-metrics MIT, scikit-learn/numpy/scipy BSD. Lane code original,
MIT. No new third-party tool is wired (all already WIRED - run-proven).
"""
import hashlib
import json
import math
import os
import time
import wave
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "coverage")
W58 = os.path.join(HERE, "..", "wave58_lane_c", "proofs",
                   "real_voice_diarization")
DIALOGUE = os.path.join(W58, "dialogue.wav")
GT_PATH = os.path.join(W58, "ground_truth.json")
REF_RTTM = os.path.join(W58, "reference.rttm")
EMB_PT = os.path.join(W58, "embeddings.pt")
SR = 16000
WIN_S, HOP_S = 1.5, 0.25
SILENCE_FRAC = 0.08  # wave58 energy gate
VAD_AGG, VAD_PAD = 0, 0.2  # wave59 tuned winner
K_MIN, K_MAX, KNN_K = 2, 6, 7

EXPECT_SHA = {
    "dialogue.wav":
        "666cc1b94bd72127375fe58416a15988434156746df0ed1bee61c91066ef0342",
    "ground_truth.json":
        "3bfbdbddb43ed4e4924256625c11bfd01c67fd19a575094a1ac952422a34c6cc",
    "embeddings.pt":
        "66d2d151aab053b61fcb9411aff5cc1ba7455ec87334b819a1312811e2bff4c9",
    "reference.rttm": "e759d68f3d9d6ad7169cc31584f4e2b258544d0e759d4f3e623cb25f399bc9ff",
}
EMB_SHAPE = (160, 192)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def load_fixture():
    for name, want in EXPECT_SHA.items():
        p = {"dialogue.wav": DIALOGUE, "ground_truth.json": GT_PATH,
             "embeddings.pt": EMB_PT, "reference.rttm": REF_RTTM}[name]
        got = sha256_file(p)
        assert got == want, f"{name} SHA mismatch: {got}"
    turns = json.load(open(GT_PATH))["turns"]
    with wave.open(DIALOGUE, "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        audio = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
                 .astype(np.float32) / 32768.0)
    z = zipfile.ZipFile(EMB_PT)
    raw = z.read("embeddings/data/0")
    assert len(raw) == EMB_SHAPE[0] * EMB_SHAPE[1] * 4, len(raw)
    emb = np.frombuffer(raw, dtype="<f4").reshape(EMB_SHAPE).astype(np.float64)
    assert np.all(np.isfinite(emb))
    return audio, turns, emb


# ------------------------------------------------- VAD (wave59 tuned winner)
def vad_segments(audio, sr=SR, agg=VAD_AGG, pad=VAD_PAD):
    import webrtcvad
    vad = webrtcvad.Vad(agg)
    frame_n = int(0.01 * sr)
    decisions = []
    for i in range(0, len(audio), frame_n):
        fr = audio[i:i + frame_n]
        if len(fr) < frame_n:
            fr = np.pad(fr, (0, frame_n - len(fr)))
        b = (np.clip(fr, -1, 1) * 32767).astype(np.int16).tobytes()
        decisions.append(vad.is_speech(b, sr))
    segs, s = [], None
    for i, d in enumerate(decisions):
        if d and s is None:
            s = i
        elif not d and s is not None:
            segs.append((s * 0.01, (i) * 0.01))
            s = None
    if s is not None:
        segs.append((s * 0.01, len(decisions) * 0.01))
    padded = [(max(0.0, a - pad), b + pad) for a, b in segs]
    merged = []
    for a, b in sorted(padded):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


def vad_quality(segs, turns, audio_len):
    frame = 0.01
    n = int(audio_len / SR / frame)
    gt = np.zeros(n, bool)
    va = np.zeros(n, bool)
    for t in turns:
        gt[int(t["start"] / frame):int(t["end"] / frame)] = True
    for a, b in segs:
        va[int(a / frame):int(b / frame)] = True
    tp = int((gt & va).sum())
    return (tp / max(1, int(gt.sum())), tp / max(1, int(va.sum())))


def inside_vad(t0, t1, segs, tol=0.001):
    return any(a - tol <= t0 and t1 <= b + tol for a, b in segs)


def rms(x):
    return float(np.sqrt(np.mean(np.square(x))))


# ------------------------------------------------- window grid + energy gate
def window_grid(audio):
    win = int(WIN_S * SR)
    hop = int(HOP_S * SR)
    idxs = list(range(0, len(audio) - win + 1, hop))
    rmsv = np.array([rms(audio[i:i + win]) for i in idxs])
    thr = SILENCE_FRAC * float(np.max(rmsv))
    all_speech = np.flatnonzero(rmsv >= thr)
    return idxs, rmsv, thr, all_speech


# ------------------------------------------------- eigengap E1a (wave60)
def _l2n(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def eigengap_laplacian(X, k_min=K_MIN, k_max=K_MAX, knn_k=KNN_K):
    from scipy.linalg import eigh
    W = (_l2n(X) @ _l2n(X).T + 1.0) / 2.0
    n = W.shape[0]
    mask = np.zeros_like(W, dtype=bool)
    idx = np.argpartition(-W, kth=knn_k + 1, axis=1)[:, :knn_k + 1]
    rows = np.arange(n)[:, None]
    mask[rows, idx] = True
    W = np.where(mask | mask.T, W, 0.0)
    np.fill_diagonal(W, 1.0)
    d = W.sum(axis=1)
    di = 1.0 / np.sqrt(np.maximum(d, 1e-12))
    L = np.eye(n) - (di[:, None] * W * di[None, :])
    vals = np.maximum(eigh(L, eigvals_only=True), 0.0)
    gaps = {k: float(vals[k] - vals[k - 1]) for k in range(k_min, k_max)}
    k_est = max(gaps, key=lambda k: gaps[k])
    margin = gaps[k_est] / max(v for k, v in gaps.items() if k != k_est)
    return k_est, vals[:k_max + 1].tolist(), gaps, margin


# ------------------------------------------------- frames / scoring
def gt_at(turns, t):
    return next((g["speaker"] for g in turns
                 if g["start"] <= t < g["end"]), None)


def hungarian_map(frames, turns):
    from scipy.optimize import linear_sum_assignment
    clus = sorted(set(frames[frames != -1].tolist()))
    spks = sorted(set(t["speaker"] for t in turns))
    cont = np.zeros((len(clus), len(spks)))
    ci = {c: k for k, c in enumerate(clus)}
    si = {s: k for k, s in enumerate(spks)}
    for i, f in enumerate(frames):
        if f == -1:
            continue
        s = gt_at(turns, (i + 0.5) * HOP_S)
        if s is not None:
            cont[ci[f], si[s]] += 1
    ri, cj = linear_sum_assignment(-cont)
    cmap = {int(clus[r]): spks[c] for r, c in zip(ri, cj)}
    agree = total = 0
    for i, f in enumerate(frames):
        if f == -1:
            continue
        s = gt_at(turns, (i + 0.5) * HOP_S)
        if s is None:
            continue
        total += 1
        if cmap[f] == s:
            agree += 1
    return cmap, agree / max(1, total), total


def segments_from_frames(frames):
    segs, i, n = [], 0, len(frames)
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
    comp = {k: float(det[k]) for k in
            ("missed detection", "false alarm", "confusion", "total")}
    return der(ref, hyp), jer(ref, hyp), comp


# ------------------------------------------------- frame labeling variants
def label_v2c_no_fill(kept, labels, segs, n_frames):
    """Wave-62 production labeling verbatim: frames covered by a kept window
    whose center is inside VAD speech; nearest-to-window-center wins."""
    frames = np.full(n_frames, -1, dtype=int)
    best_d = np.full(n_frames, np.inf)
    center_off = int(round((WIN_S / 2) / HOP_S))
    win_frames = int(round(WIN_S / HOP_S))
    for j, lab in zip(kept, labels):
        for f in range(j, min(j + win_frames, n_frames)):
            t_center = (f + 0.5) * HOP_S
            if not any(a <= t_center < b for a, b in segs):
                continue
            d = abs(f - (j + center_off))
            if d < best_d[f]:
                best_d[f] = d
                frames[f] = int(lab)
    return frames


def fill_within_vad(frames_base, segs, n_frames):
    """F1: for unlabeled frames whose center is inside a VAD segment, take
    the label of the temporally nearest labeled frame, restricted to the
    same VAD segment (never propagate across a VAD gap). Ties -> earlier."""
    filled = frames_base.copy()
    labeled_idx = np.flatnonzero(frames_base != -1)
    labeled_lab = frames_base[labeled_idx]
    if len(labeled_idx) == 0:
        return filled
    # VAD segment index per frame center
    seg_of = np.full(n_frames, -1, dtype=int)
    for i in range(n_frames):
        tc = (i + 0.5) * HOP_S
        for si, (a, b) in enumerate(segs):
            if a <= tc < b:
                seg_of[i] = si
                break
    for f in range(n_frames):
        if filled[f] != -1 or seg_of[f] == -1:
            continue
        # nearest labeled frame inside the same VAD segment
        cand = labeled_idx[seg_of[labeled_idx] == seg_of[f]]
        if len(cand) == 0:
            continue  # no labeled anchor in this VAD segment: stay unlabeled
        d = np.abs(cand - f)
        filled[f] = int(labeled_lab[seg_of[labeled_idx] == seg_of[f]][
            np.argmin(d)])
    return filled


def fill_global(frames_base):
    """F2 (Wave-58-style): nearest labeled frame for EVERY frame, including
    inter-turn gaps. Measures the miss->FA trade-off cost."""
    filled = frames_base.copy()
    labeled_idx = np.flatnonzero(frames_base != -1)
    labeled_lab = frames_base[labeled_idx]
    unl = np.flatnonzero(filled == -1)
    for f in unl:
        d = np.abs(labeled_idx - f)
        filled[f] = int(labeled_lab[np.argmin(d)])
    return filled


def main():
    t0 = time.time()
    res = {"wave": 63, "lane": "C",
           "question": "VAD-coverage recovery: close the miss/FA gap vs "
                       "Wave-60 (V2c no-fill vs fill trade-off)"}
    checks = []

    def check(name, ok, detail):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    audio, turns, fixture_emb = load_fixture()
    check("fixture_shas",
          True, "dialogue.wav + ground_truth.json + embeddings.pt + "
                 "reference.rttm SHA-verified vs wave58 manifest")

    # stage B: tuned VAD on raw audio (identical to wave62 main_clean)
    segs = vad_segments(audio)
    rec, prec = vad_quality(segs, turns, len(audio))
    res["vad_segments"] = [[round(a, 3), round(b, 3)] for a, b in segs]
    res["vad_recall"], res["vad_precision"] = round(rec, 4), round(prec, 4)
    check("vad_reproduces_wave62", abs(rec - 0.9351) < 0.002 and prec == 1.0,
          f"recall={rec:.4f} (wave62 0.9351) prec={prec:.4f} "
          f"segments={len(segs)}")
    print(f"  VAD: {len(segs)} segments, recall={rec:.4f} prec={prec:.4f}")

    # stage C: window grid + energy gate + VAD-boundary refinement (V2c)
    idxs, rmsv, thr, all_speech = window_grid(audio)
    kept = [int(j) for j in all_speech
            if inside_vad(j * HOP_S, j * HOP_S + WIN_S, segs)]
    check("windows_reproduce_wave62",
          len(idxs) == 166 and len(all_speech) == 160 and len(kept) == 94,
          f"grid={len(idxs)} energy-speech={len(all_speech)} kept={len(kept)}")
    print(f"  windows: grid={len(idxs)} energy-speech={len(all_speech)} "
          f"kept(VAD)={len(kept)}")

    # stage D: fixture embeddings (raw slices; NO denoise upstream)
    row = {int(j): i for i, j in enumerate(all_speech)}
    emb = fixture_emb[np.asarray([row[int(j)] for j in kept])]
    assert emb.shape == (len(kept), 192)

    # stage E: eigengap speaker-count selection (blind to GT)
    k_est, eigs, gaps, margin = eigengap_laplacian(emb)
    res["eigengap_k"], res["eigengap_margin"] = k_est, round(margin, 2)
    check("eigengap_blind_k3", k_est == 3,
          f"k={k_est} margin={margin:.2f}x (wave62 2.11x)")
    print(f"  eigengap: k={k_est}, margin={margin:.1f}x")

    # stage F: forced-k SpectralCluster
    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=k_est, max_clusters=k_est,
                           custom_dist="cosine")
    labels = np.asarray(cl.predict(emb), dtype=int)

    n_frames = int(math.ceil((len(audio) / SR) / HOP_S))

    # stage G variants
    frames_f0 = label_v2c_no_fill(kept, labels, segs, n_frames)
    frames_f1 = fill_within_vad(frames_f0, segs, n_frames)
    frames_f2 = fill_global(frames_f0)

    # cluster->speaker map from the production (no-fill) labeling; the fill
    # variants only change coverage, never identity (purity is 1.0).
    cmap, purity, nfrm = hungarian_map(frames_f0, turns)
    res["cluster_to_speaker"] = {str(k): s for k, s in cmap.items()}
    res["frame_purity"] = round(purity, 4)
    check("purity_and_map", purity == 1.0 and
          sorted(cmap.values()) == ["A", "B", "C"],
          f"map={cmap} purity={purity:.4f}")
    for tag, fvar in (("F1", frames_f1), ("F2", frames_f2)):
        cm, pu, _ = hungarian_map(fvar, turns)
        check(f"map_agrees_{tag}", cm == cmap and pu == 1.0,
              f"{tag} map identical to F0, purity={pu:.4f}")

    spk_of = {c: cmap[c] for c in set(frames_f0[frames_f0 != -1].tolist())}
    variants = {}
    for tag, fvar in (("F0_nofill", frames_f0), ("F1_fill_within_vad", frames_f1),
                      ("F2_fill_global", frames_f2)):
        labeled = int((fvar != -1).sum())
        # newly labeled frames introduced by the fill step
        new = int(((fvar != -1) & (frames_f0 == -1)).sum())
        segs_out = [(s, e, spk_of[c])
                    for s, e, c in segments_from_frames(fvar)]
        hyp_path = os.path.join(PROOFS, f"hypothesis_{tag}.rttm")
        write_rttm(hyp_path, segs_out)
        v = {"frames_labeled": labeled, "frames_filled_new": new,
             "n_hyp_segments": len(segs_out)}
        for collar in (0.0, 0.25):
            d, j, comp = score(REF_RTTM, hyp_path, collar)
            key = str(collar)
            v[f"DER_c{key}"] = round(d, 4)
            v[f"JER_c{key}"] = round(j, 4)
            v[f"components_c{key}"] = {k: round(x, 3)
                                      for k, x in comp.items()}
            print(f"  {tag} collar={collar}: DER={d:.4f} JER={j:.4f} "
                  f"(miss={comp['missed detection']:.2f} "
                  f"FA={comp['false alarm']:.2f} "
                  f"conf={comp['confusion']:.2f})")
        variants[tag] = v
    res["variants"] = variants

    f0, f1, f2 = (variants["F0_nofill"], variants["F1_fill_within_vad"],
                  variants["F2_fill_global"])
    # F0 must reproduce Wave-62 main_clean before any claim is made
    check("f0_reproduces_wave62",
          abs(f0["DER_c0.0"] - 0.1158) < 0.002 and
          abs(f0["JER_c0.0"] - 0.1156) < 0.002 and
          f0["components_c0.0"]["missed detection"] == 4.55 and
          f0["components_c0.0"]["false alarm"] == 0.0,
          f"DER={f0['DER_c0.0']} JER={f0['JER_c0.0']} "
          f"(wave62: 0.1158/0.1156)")
    check("f1_miss_recovered",
          f1["components_c0.0"]["missed detection"] <
          f0["components_c0.0"]["missed detection"],
          f"F1 miss={f1['components_c0.0']['missed detection']}s vs "
          f"F0 miss={f0['components_c0.0']['missed detection']}s")
    check("f1_beats_wave62_der",
          f1["DER_c0.0"] < f0["DER_c0.0"],
          f"F1 DER={f1['DER_c0.0']} vs F0 DER={f0['DER_c0.0']}")
    check("f1_beats_wave60_der",
          f1["DER_c0.0"] < 0.0941,
          f"F1 DER={f1['DER_c0.0']} vs wave60 fill DER=0.0941")
    check("f2_measures_fill_cost",
          f2["components_c0.0"]["false alarm"] > 0.0,
          f"F2 FA={f2['components_c0.0']['false alarm']}s "
          f"(wave60 fill FA=3.70s)")

    res["checks"] = checks
    res["elapsed_s"] = round(time.time() - t0, 1)
    n_pass = sum(c["pass"] for c in checks)
    res["checks_pass"] = f"{n_pass}/{len(checks)}"
    with open(os.path.join(PROOFS, "vad_coverage_result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n{n_pass}/{len(checks)} checks PASS, "
          f"{res['elapsed_s']}s. Result -> proofs/coverage/")
    if n_pass != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
