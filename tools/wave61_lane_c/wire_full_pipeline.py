#!/usr/bin/env python3
"""Wave 61 Lane C — FULL voice pipeline END-TO-END on real multi-speaker audio.

Pipeline (all stages wired by prior waves, donors listed per stage):
  1. Denoise: DeepFilterNet3 (Rikorose/DeepFilterNet, dual MIT/Apache-2.0)
     — donor pattern from tools/wave56_lane_c/wire_deepfilternet.py
  2. VAD refinement: webrtcvad agg=0 + 0.2 s hangover pad (MIT)
     — winner config from tools/wave59_lane_c (V2c)
  3. Speaker-count selection: eigengap E1a (symmetric normalized Laplacian,
     k-NN(7)-sparsified cosine affinity, absolute gap; original lane code, MIT)
     — from tools/wave60_lane_c/wire_speaker_count.py
  4. forced-k SpectralCluster (Apache-2.0) clustering of ECAPA-TDNN 192-dim
     embeddings (Apache-2.0 speechbrain/spkrec-ecapa-voxceleb) — Wave 56/58
  5. Frame labeling inside VAD speech only, no fill (Wave 59 V2c) -> RTTM
  6. Score: DER/JER via pyannote-metrics (MIT) vs wave58 ground truth

Fixture: Wave-58 9-turn 3-Kokoro-voice dialogue (real neural VO, genuine GT)
  clean (16 kHz) AND a seeded 10 dB-SNR white-noise variant — the noisy path
  is the honest end-to-end: denoiser must earn its place.

Proof artifacts land in proofs/full_pipeline/.
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

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "full_pipeline")
os.makedirs(PROOFS, exist_ok=True)

W58 = os.path.join(HERE, "..", "wave58_lane_c", "proofs",
                   "real_voice_diarization")
FIXTURE = os.path.join(W58, "dialogue.wav")
GT_PATH = os.path.join(W58, "ground_truth.json")
REF_RTTM = os.path.join(W58, "reference.rttm")
SCRATCH = os.path.join(HERE, "scratch")

SR = 16000
SR_MODEL = 48000          # DeepFilterNet3 full-band
WIN_S, HOP_S = 1.5, 0.25  # wave58 window grid
SILENCE_FRAC = 0.08       # energy gate
SNR_IN_DB = 10.0          # noisy variant calibration
RNG_SEED = 20261008
K_MIN, K_MAX, KNN_K = 2, 6, 7
VAD_AGG, VAD_PAD = 0, 0.2  # wave59 tuned winner


def read_wav_mono(path):
    with wave.open(path, "rb") as w:
        n, sw, fr, ch = (w.getnframes(), w.getsampwidth(),
                         w.getframerate(), w.getnchannels())
        raw = w.readframes(n)
    assert sw == 2, f"expected int16, got {sw}-byte samples"
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x, fr


def write_wav_mono(path, x, sr):
    x = np.clip(x, -1.0, 1.0)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767.0).astype(np.int16).tobytes())


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-12)


def db(x):
    return 20.0 * math.log10(max(x, 1e-12))


# ------------------------------------------------- stage 1: denoise
def init_denoiser():
    # torchaudio 2.9+ compat shim (same as Wave 56 lane venv)
    import torchaudio.backend
    try:
        torchaudio.backend.common.AudioMetaData  # noqa
    except (AttributeError, ImportError):
        import types
        from dataclasses import dataclass
        mod = types.ModuleType("torchaudio.backend.common")

        @dataclass
        class AudioMetaData:
            sample_rate: int
            num_frames: int
            num_channels: int
            bits_per_sample: int
            encoding: str

        mod.AudioMetaData = AudioMetaData
        sys.modules["torchaudio.backend.common"] = mod
    from df.enhance import enhance, init_df
    model, df_state, _ = init_df(model_base_dir=None, post_filter=False)
    assert df_state.sr() == SR_MODEL
    return model, df_state, enhance


def resample(x, sr_in, sr_out):
    import torchaudio.functional as TAF
    xt = torch.from_numpy(np.asarray(x, dtype=np.float32)).unsqueeze(0)
    return TAF.resample(xt, sr_in, sr_out).squeeze(0)


def denoise(model, df_state, enhance, x16):
    with torch.no_grad():
        x48 = resample(np.clip(x16, -1, 1), SR, SR_MODEL).unsqueeze(0)
        out = enhance(model, df_state, x48)
    e48 = out.squeeze(0).numpy()
    e16 = resample(e48, SR_MODEL, SR).numpy()
    return e16[:len(x16)]


# ------------------------------------------------- stage 2: VAD
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
    # frame runs -> segments, then hangover pad
    segs, s = [], None
    for i, d in enumerate(decisions):
        if d and s is None:
            s = i
        elif not d and s is not None:
            segs.append((s * 0.01, (i) * 0.01))
            s = None
    if s is not None:
        segs.append((s * 0.01, len(decisions) * 0.01))
    # pad both ends, merge overlaps
    padded = [(max(0.0, a - pad), b + pad) for a, b in segs]
    merged = []
    for a, b in sorted(padded):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged, len(decisions)


def vad_quality(segs, turns, audio_len):
    """Recall/precision of VAD segments vs GT turn spans (10 ms frame basis)."""
    frame = 0.01
    n = int(audio_len / SR / frame)
    gt = np.zeros(n, bool)
    va = np.zeros(n, bool)
    for t in turns:
        gt[int(t["start"] / frame):int(t["end"] / frame)] = True
    for a, b in segs:
        va[int(a / frame):int(b / frame)] = True
    tp = int((gt & va).sum())
    return (tp / max(1, int(gt.sum())), tp / max(1, int(va.sum())), int(gt.sum()))


def inside_vad(t0, t1, segs, tol=0.001):
    return any(a - tol <= t0 and t1 <= b + tol for a, b in segs)


# ------------------------------------------------- stage 5: count estimator
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


# ------------------------------------------------- pipeline
def run_pipeline(tag, audio16, model, df_state, enhance, turns, ref_rttm,
                 res, embedder, skip_denoise=False):
    print(f"\n===== variant: {tag} =====")
    v = {"tag": tag, "snr_gain_db": None}

    # stage 1: denoise (skip_denoise=True -> honest no-denoiser ablation)
    t = time.time()
    e = audio16.copy() if skip_denoise else denoise(model, df_state, enhance,
                                                   audio16)
    v["denoise_s"] = round(time.time() - t, 1)
    v["denoised"] = not skip_denoise
    write_wav_mono(os.path.join(PROOFS, f"out_{tag}_denoised.wav"), e, SR)
    v["denoised_sha256"] = sha256(os.path.join(PROOFS, f"out_{tag}_denoised.wav"))

    # stage 2: tuned VAD on the DENOISED audio
    segs, ndec = vad_segments(e)
    v["vad_nseg"] = len(segs)
    v["vad_segments"] = [[round(a, 3), round(b, 3)] for a, b in segs]
    rec, prec, _ = vad_quality(segs, turns, len(e))
    v["vad_recall"], v["vad_precision"] = round(rec, 4), round(prec, 4)
    print(f"  VAD: {len(segs)} segments, recall={rec:.4f} prec={prec:.4f}")

    # stage 2b: window grid + energy gate + VAD-boundary refinement (V2c)
    win = int(WIN_S * SR)
    hop = int(HOP_S * SR)
    idxs = list(range(0, len(e) - win + 1, hop))
    rmsv = np.array([rms(e[i:i + win]) for i in idxs])
    thr = SILENCE_FRAC * float(np.max(rmsv))
    all_speech = np.flatnonzero(rmsv >= thr)
    kept = [j for j in all_speech
            if inside_vad(j * HOP_S, j * HOP_S + WIN_S, segs)]
    v["windows_grid"] = len(idxs)
    v["windows_speech_energy"] = int(len(all_speech))
    v["windows_kept_vad"] = len(kept)
    print(f"  windows: grid={len(idxs)} energy-speech={len(all_speech)} "
          f"kept(VAD)={len(kept)}")

    # stage 4: ECAPA embeddings on denoised kept windows
    batch = torch.stack([torch.from_numpy(e[j * hop:j * hop + win])
                         for j in kept])
    t = time.time()
    with torch.no_grad():
        emb = embedder.encode_batch(batch).squeeze(1).numpy()
    v["embed_s"] = round(time.time() - t, 1)
    v["embed_shape"] = list(emb.shape)
    v["embed_finite"] = bool(np.all(np.isfinite(emb)))
    assert emb.shape == (len(kept), 192)
    print(f"  ECAPA: shape={emb.shape}, finite={v['embed_finite']}")

    # stage 3: eigengap count (blind to GT)
    k_est, eigs, gaps, margin = eigengap_laplacian(emb)
    v["eigengap_k"] = k_est
    v["eigengap_eigenvalues"] = [round(x, 4) for x in eigs]
    v["eigengap_gaps"] = {str(k): round(g, 4) for k, g in gaps.items()}
    v["eigengap_margin"] = round(margin, 2)
    print(f"  eigengap: k={k_est}, margin={margin:.1f}x")

    # stage 4b: forced-k SpectralCluster
    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=k_est, max_clusters=k_est,
                           custom_dist="cosine")
    labels = np.asarray(cl.predict(emb), dtype=int)
    v["n_clusters_found"] = len(set(labels.tolist()))

    # diagnostic (GT-informed, NOT part of the blind pipeline): how separable
    # are the two female voices in THIS variant's embedding space?
    gt_spk = [gt_at(turns, j * HOP_S + WIN_S / 2) for j in kept]
    means = {}
    for s in ("A", "B", "C"):
        idx = [i for i, g in enumerate(gt_spk) if g == s]
        if idx:
            m = emb[idx].mean(axis=0)
            means[s] = m / (np.linalg.norm(m) + 1e-12)
    v["diag_cos"] = {f"{a}{b}": round(float(means[a] @ means[b]), 4)
                     for a, b in (("A", "B"), ("A", "C"), ("B", "C"))
                     if a in means and b in means}
    print(f"  GT-mean cosine: {v['diag_cos']}")

    # stage 5: frame labeling inside VAD speech only, no fill.
    # Each kept window (span: frames j..j+5) labels the frames it covers;
    # a frame takes the label of the covering kept window whose center is
    # nearest. Frames outside VAD speech, or covered by no kept window,
    # stay -1 (no nearest-neighbour fill — the Wave-58 fill discipline).
    n_frames = int(math.ceil((len(e) / SR) / HOP_S))
    frames = np.full(n_frames, -1, dtype=int)
    best_d = np.full(n_frames, np.inf)
    center_off = int(round((WIN_S / 2) / HOP_S))
    win_frames = int(round(WIN_S / HOP_S))  # 6 frames per 1.5 s window
    for j, lab in zip(kept, labels):
        for f in range(j, min(j + win_frames, n_frames)):
            t_center = (f + 0.5) * HOP_S
            if not any(a <= t_center < b for a, b in segs):
                continue
            d = abs(f - (j + center_off))
            if d < best_d[f]:
                best_d[f] = d
                frames[f] = int(lab)
    v["frames_labeled"] = int((frames != -1).sum())
    v["frames_total"] = n_frames

    cmap, purity, nfrm = hungarian_map(frames, turns)
    v["cluster_to_speaker"] = {str(k): s for k, s in cmap.items()}
    v["frame_purity"] = round(purity, 4)
    mapped = set(cmap.values())
    v["speakers_mapped"] = sorted(mapped)
    print(f"  map={v['cluster_to_speaker']} purity={purity:.4f}")

    spk_of = {c: cmap[c] for c in set(frames[frames != -1].tolist())}
    segs_out = [(s, e_, spk_of[c]) for s, e_, c in segments_from_frames(frames)]
    v["n_hyp_segments"] = len(segs_out)
    hyp_path = os.path.join(PROOFS, f"hypothesis_{tag}.rttm")
    write_rttm(hyp_path, segs_out)


    for collar in (0.0, 0.25):
        d, j, comp = score(ref_rttm, hyp_path, collar)
        key = str(collar)
        v[f"DER_c{key}"] = round(d, 4)
        v[f"JER_c{key}"] = round(j, 4)
        v[f"components_c{key}"] = {k: round(x, 3) for k, x in comp.items()}
        print(f"  collar={collar}: DER={d:.4f} JER={j:.4f} "
              f"(miss={comp['missed detection']:.2f} "
              f"FA={comp['false alarm']:.2f} conf={comp['confusion']:.2f} "
              f"total={comp['total']:.2f})")
    return v


# ------------------------------------------------- main
def main():
    t_all = time.time()
    res = {"checks": [], "variants": {}}

    def check(name, ok, detail):
        res["checks"].append({"name": name, "status": "PASS" if ok else "FAIL",
                              "detail": detail})
        print(("PASS" if ok else "FAIL"), name, "-", detail)

    ok_f = sha256(FIXTURE) == "666cc1b94bd72127375fe58416a15988434156746df0ed1bee61c91066ef0342"
    ok_g = sha256(GT_PATH) == "3bfbdbddb43ed4e4924256625c11bfd01c67fd19a575094a1ac952422a34c6cc"
    ok_r = sha256(REF_RTTM) == "e759d68f3d9d6ad7169cc31584f4e2b258544d0e759d4f3e623cb25f399bc9ff"
    check("fixture_sha", ok_f, f"dialogue.wav {sha256(FIXTURE)[:12]}")
    check("gt_sha", ok_g, f"ground_truth.json {sha256(GT_PATH)[:12]}")
    check("ref_rttm_sha", ok_r, f"reference.rttm {sha256(REF_RTTM)[:12]}")

    clean, sr = read_wav_mono(FIXTURE)
    assert sr == SR
    turns = json.load(open(GT_PATH))["turns"]
    write_wav_mono(os.path.join(PROOFS, "fixture_clean.wav"), clean, SR)
    check("fixture_duration", abs(len(clean) / SR - 42.9) < 0.5,
          f"{len(clean)/SR:.2f} s, 9 turns, 3 voices")

    rng = np.random.default_rng(RNG_SEED)
    speech_rms = rms(clean)
    noise = rng.standard_normal(clean.shape).astype(np.float32)
    noise *= speech_rms / (rms(noise) * 10 ** (SNR_IN_DB / 20))
    snr_in = db(speech_rms / rms(noise))
    noisy = clean + noise
    write_wav_mono(os.path.join(PROOFS, "fixture_noisy_white.wav"),
                   np.clip(noisy, -1, 1), SR)
    check("noise_calibration", abs(snr_in - SNR_IN_DB) < 0.3,
          f"input SNR {snr_in:.1f} dB (target {SNR_IN_DB})")

    model, df_state, enhance = init_denoiser()
    from speechbrain.inference import EncoderClassifier
    embedder = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=os.path.join(SCRATCH, "speechbrain_models"))

    res["variants"]["clean"] = run_pipeline(
        "clean", clean, model, df_state, enhance, turns, REF_RTTM, res, embedder)
    res["variants"]["noisy"] = run_pipeline(
        "noisy", np.clip(noisy, -1, 1), model, df_state, enhance, turns,
        REF_RTTM, res, embedder)
    res["variants"]["noisy_bypass"] = run_pipeline(
        "noisy_bypass", np.clip(noisy, -1, 1), model, df_state, enhance,
        turns, REF_RTTM, res, embedder, skip_denoise=True)

    nc, nn = res["variants"]["clean"], res["variants"]["noisy"]
    nb = res["variants"]["noisy_bypass"]

    # SNR gain of the denoiser on the noisy variant (noise is known exactly)
    e_n1, _ = read_wav_mono(os.path.join(PROOFS, "out_noisy_denoised.wav"))
    resid = e_n1 - clean
    snr_out = db(rms(clean) / rms(resid))
    gain = snr_out - snr_in
    nn["snr_out_db"], nn["snr_gain_db"] = round(snr_out, 2), round(gain, 2)
    print(f"  denoise SNR: {snr_in:.1f} -> {snr_out:.1f} dB (Δ {gain:+.1f} dB)")
    check("denoise_snr_gain_noisy", gain > 3.0,
          f"10 dB input -> {gain:+.1f} dB gain")

    e_clean, _ = read_wav_mono(os.path.join(PROOFS, "out_clean_denoised.wav"))
    rdelta = abs(rms(e_clean) - rms(clean)) / rms(clean)
    corr = float(np.corrcoef(clean, e_clean)[0, 1])
    check("denoise_clean_noop_rms", rdelta < 0.05,
          f"clean RMS delta {rdelta*100:.2f}% (< 5%)")
    check("denoise_clean_noop_corr", corr > 0.99,
          f"corr(clean, enhanced) = {corr:.5f}")

    e_n2 = denoise(model, df_state, enhance, np.clip(noisy, -1, 1))
    maxdiff = float(np.max(np.abs(e_n1 - e_n2)))
    check("denoise_deterministic", maxdiff < 1e-4,
          f"re-run max|diff| = {maxdiff:.2e} (wav-quantized read vs fresh)")

    check("vad_recall_noisy", nn["vad_recall"] >= 0.90,
          f"tuned VAD recall {nn['vad_recall']:.4f} (>= 0.90)")
    check("vad_precision_noisy", nn["vad_precision"] >= 0.99,
          f"tuned VAD precision {nn['vad_precision']:.4f} (>= 0.99)")
    check("eigengap_k_noisy", nn["eigengap_k"] == 3,
          f"E1a selects k={nn['eigengap_k']} (margin {nn['eigengap_margin']}x)")
    check("eigengap_k_clean", nc["eigengap_k"] == 3,
          f"clean-path E1a selects k={nc['eigengap_k']}")
    check("all_speakers_mapped_noisy", set(nn["speakers_mapped"]) == {"A", "B", "C"},
          f"mapped {nn['speakers_mapped']}")
    check("der_finite_noisy", np.isfinite(nn["DER_c0.0"]),
          f"noisy-path DER={nn['DER_c0.0']:.4f} JER={nn['JER_c0.0']:.4f}")
    check("der_finite_clean", np.isfinite(nc["DER_c0.0"]),
          f"clean-path DER={nc['DER_c0.0']:.4f} JER={nc['JER_c0.0']:.4f}")
    check("der_finite_bypass", np.isfinite(nb["DER_c0.0"]),
          f"bypass DER={nb['DER_c0.0']:.4f} JER={nb['JER_c0.0']:.4f}")
    check("est_k_matches_forced",
          nn["eigengap_k"] == 3 and nn["n_clusters_found"] == 3,
          "estimator k == forced-k clusters == 3")
    check("denoise_helps_diarization", nn["DER_c0.0"] < nb["DER_c0.0"],
          f"noisy+denoise DER {nn['DER_c0.0']:.4f} vs "
          f"noisy-bypass DER {nb['DER_c0.0']:.4f}")
    check("bypass_worse_than_clean", nb["DER_c0.0"] > nc["DER_c0.0"],
          f"sanity: noisy-bypass DER {nb['DER_c0.0']:.4f} > "
          f"clean DER {nc['DER_c0.0']:.4f}")
    res["honest_findings"] = [
        "noisy-path eigengap k is reported as measured (expected 3; "
        "residual noise collapses the gap margin)",
        "caption words come from Wave-58 GT turn texts; the pipeline "
        "supplies speaker identity + timing only (no ASR stage wired)",
    ]

    res["total_s"] = round(time.time() - t_all, 1)
    res["passed"] = sum(1 for c in res["checks"] if c["status"] == "PASS")
    res["failed"] = sum(1 for c in res["checks"] if c["status"] == "FAIL")
    with open(os.path.join(PROOFS, "full_pipeline_result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"{res['passed']}/{len(res['checks'])} checks PASS "
          f"in {res['total_s']} s")
    return 0 if res["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
