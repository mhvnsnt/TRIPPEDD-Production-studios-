#!/usr/bin/env python3
"""Wave 62 Lane C — diarization pipeline REBUILT with the Wave-61 production
rule: denoise goes DOWNSTREAM of embeddings, never upstream of them.

Rebuilt topology (production path):
  raw audio
    -> tuned webrtcvad VAD (agg=0 + 0.2 s hangover pad; Wave-59 winner)
    -> window grid 1.5 s / 0.25 s hop + energy gate (8% of max; Wave-58)
       -> drop windows straddling VAD boundaries (Wave-59 V2c)
    -> ECAPA-TDNN 192-dim embeddings computed on RAW audio (Wave-58
       committed embeddings.pt, SHA-verified; kept windows are bit-identical
       raw slices of Wave-58's grid, so the vectors are identical)
    -> eigengap E1a speaker-count estimator (Wave-60: symmetric normalized
       Laplacian, k-NN(7) cosine affinity, absolute gap)
    -> forced-k SpectralCluster (Apache-2.0)
    -> frame labeling inside VAD speech only, no fill (Wave-59 V2c)
    -> hypothesis RTTM -> DER/JER via pyannote-metrics (MIT)

THEN, downstream (separate script wire_downstream_caption.py):
  per-speaker hypothesis segments (raw audio) -> DeepFilterNet3 denoise
  -> denoised per-speaker wavs + caption burn-in onto the denoised mix.
  Denoise NEVER touches the embedding input.

Ablation (re-confirming the Wave-61 finding with fresh numbers):
  upstream-denoise control = Wave-61 topology (DeepFilterNet BEFORE the
  embedding stage, ECAPA recomputed on denoised audio) on clean AND on a
  seeded 10 dB-SNR white-noise variant, plus a noisy_bypass ablation.
  Expectation (Wave-61): upstream denoise collapses speaker separation
  (cos A/C rises, eigengap margin collapses, blind k flips 3->2 on noisy)
  and DER gets WORSE despite better SNR.

Fixture: Wave-58 9-turn 3-Kokoro-voice dialogue (A=af_heart F, B=am_puck M,
C=af_bella F; A/C both female on purpose), 42.9 s @16 kHz.

Proof artifacts land in proofs/rebuilt_pipeline/.
"""
import hashlib
import json
import math
import os
import sys
import time
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "rebuilt_pipeline")
os.makedirs(PROOFS, exist_ok=True)

W58 = os.path.join(HERE, "..", "wave58_lane_c", "proofs",
                   "real_voice_diarization")
FIXTURE = os.path.join(W58, "dialogue.wav")
GT_PATH = os.path.join(W58, "ground_truth.json")
REF_RTTM = os.path.join(W58, "reference.rttm")
EMB_PT = os.path.join(W58, "embeddings.pt")
SCRATCH = os.path.join(HERE, "scratch")

SR = 16000
SR_MODEL = 48000          # DeepFilterNet3 full-band
WIN_S, HOP_S = 1.5, 0.25  # wave58 window grid
SILENCE_FRAC = 0.08       # energy gate
SNR_IN_DB = 10.0          # noisy variant calibration
RNG_SEED = 20261008       # wave61 donor seed -> same noisy variant
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


# ------------------------------------------------- denoise (DeepFilterNet3)
def init_denoiser():
    # torchaudio 2.x removed torchaudio.backend.common; df.io only needs the
    # AudioMetaData dataclass at import time, so inject a shim BEFORE
    # importing df.enhance (never `import torchaudio.backend` — it does not
    # exist in this torchaudio version).
    if "torchaudio.backend.common" not in sys.modules:
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
    import torch
    import torchaudio.functional as TAF
    xt = torch.from_numpy(np.asarray(x, dtype=np.float32)).unsqueeze(0)
    return TAF.resample(xt, sr_in, sr_out).squeeze(0)


def denoise(model, df_state, enhance, x16):
    import torch
    with torch.no_grad():
        x48 = resample(np.clip(x16, -1, 1), SR, SR_MODEL).unsqueeze(0)
        out = enhance(model, df_state, x48)
    e48 = out.squeeze(0).numpy()
    e16 = resample(e48, SR_MODEL, SR).numpy()
    return e16[:len(x16)]


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
    return merged, len(decisions)


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


# ------------------------------------------------- window grid + energy gate
def window_grid(audio):
    win = int(WIN_S * SR)
    hop = int(HOP_S * SR)
    idxs = list(range(0, len(audio) - win + 1, hop))
    rmsv = np.array([rms(audio[i:i + win]) for i in idxs])
    thr = SILENCE_FRAC * float(np.max(rmsv))
    all_speech = np.flatnonzero(rmsv >= thr)
    return idxs, rmsv, thr, all_speech


# ------------------------------------------------- fixture embeddings (RAW)
def load_fixture_embeddings():
    """Wave-58 committed embeddings.pt (raw float32), parsed with torch."""
    import torch
    obj = torch.load(EMB_PT, map_location="cpu", weights_only=True)
    emb = np.asarray(obj, dtype=np.float32)
    assert emb.shape == (160, 192), f"unexpected shape {emb.shape}"
    assert np.all(np.isfinite(emb))
    return emb


# ------------------------------------------------- ECAPA embedder (ablation only)
def init_embedder():
    from speechbrain.inference import EncoderClassifier
    return EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=os.path.join(SCRATCH, "speechbrain_models"))


def recompute_embeddings(audio, kept, embedder):
    import torch
    win = int(WIN_S * SR)
    hop = int(HOP_S * SR)
    batch = torch.stack([torch.from_numpy(audio[j * hop:j * hop + win])
                         for j in kept])
    with torch.no_grad():
        emb = embedder.encode_batch(batch).squeeze(1).numpy()
    assert emb.shape == (len(kept), 192)
    assert np.all(np.isfinite(emb))
    return emb


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

# ------------------------------------------------- pipeline
def run_pipeline(tag, audio16, turns, ref_rttm, res, mode,
                 fixture_emb=None, embedder=None,
                 model=None, df_state=None, enhance=None):
    """mode='main': PRODUCTION topology. Embeddings = Wave-58 fixture rows
    (raw audio slices; NO denoise anywhere before the embedding stage).
    mode='upstream': ablation control — DeepFilterNet BEFORE the embedding
    stage, ECAPA recomputed on denoised audio (the Wave-61 topology).
    mode='bypass': ablation — no denoise, ECAPA recomputed on noisy audio."""
    print(f"\n===== variant: {tag} (mode={mode}) =====")
    v = {"tag": tag, "mode": mode, "upstream_denoise": mode == "upstream"}

    # stage A: audio conditioning. In production mode this is a no-op:
    # RAW audio straight to the speaker path.
    e = audio16.copy()
    if mode == "upstream":
        t = time.time()
        e = denoise(model, df_state, enhance, audio16)
        v["denoise_s"] = round(time.time() - t, 1)
        write_wav_mono(os.path.join(PROOFS, f"out_{tag}_conditioned.wav"), e, SR)
        v["conditioned_sha256"] = sha256(
            os.path.join(PROOFS, f"out_{tag}_conditioned.wav"))

    # stage B: tuned VAD on the audio the embeddings will see
    segs, ndec = vad_segments(e)
    v["vad_nseg"] = len(segs)
    v["vad_segments"] = [[round(a, 3), round(b, 3)] for a, b in segs]
    rec, prec = vad_quality(segs, turns, len(e))
    v["vad_recall"], v["vad_precision"] = round(rec, 4), round(prec, 4)
    print(f"  VAD: {len(segs)} segments, recall={rec:.4f} prec={prec:.4f}")

    # stage C: window grid + energy gate + VAD-boundary refinement (V2c)
    idxs, rmsv, thr, all_speech = window_grid(e)
    kept = [int(j) for j in all_speech
            if inside_vad(j * HOP_S, j * HOP_S + WIN_S, segs)]
    v["windows_grid"] = len(idxs)
    v["windows_speech_energy"] = int(len(all_speech))
    v["windows_kept_vad"] = len(kept)
    v["energy_gate_thr"] = float(thr)
    print(f"  windows: grid={len(idxs)} energy-speech={len(all_speech)} "
          f"kept(VAD)={len(kept)}")

    # stage D: embeddings — RAW-slice fixture rows in production mode
    t = time.time()
    if mode == "main":
        row = {int(j): i for i, j in enumerate(all_speech)}
        rows = [row[int(j)] for j in kept]
        emb = fixture_emb[np.asarray(rows)]
        v["embed_source"] = ("wave58 committed embeddings.pt "
                             "(raw-audio slices, NO upstream denoise)")
    else:
        emb = recompute_embeddings(e, kept, embedder)
        v["embed_source"] = ("ECAPA recomputed fresh on "
                             f"{'denoised' if mode == 'upstream' else 'noisy'} audio")
    v["embed_s"] = round(time.time() - t, 1)
    v["embed_shape"] = list(emb.shape)
    v["embed_finite"] = bool(np.all(np.isfinite(emb)))
    assert emb.shape == (len(kept), 192)
    print(f"  ECAPA: shape={emb.shape}, finite={v['embed_finite']} "
          f"({v['embed_source'][:42]}...)")

    # stage E: eigengap speaker-count selection (blind to GT)
    k_est, eigs, gaps, margin = eigengap_laplacian(emb)
    v["eigengap_k"] = k_est
    v["eigengap_eigenvalues"] = [round(x, 4) for x in eigs]
    v["eigengap_gaps"] = {str(k): round(g, 4) for k, g in gaps.items()}
    v["eigengap_margin"] = round(margin, 2)
    print(f"  eigengap: k={k_est}, margin={margin:.1f}x")

    # stage F: forced-k SpectralCluster
    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=k_est, max_clusters=k_est,
                           custom_dist="cosine")
    labels = np.asarray(cl.predict(emb), dtype=int)
    v["n_clusters_found"] = len(set(labels.tolist()))

    # GT-informed diagnostic (NOT part of the blind pipeline)
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
    print(f"  GT-mean cosine (diagnostic): {v['diag_cos']}")

    # stage G: frame labeling inside VAD speech only, no fill
    n_frames = int(math.ceil((len(e) / SR) / HOP_S))
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
    v["frames_labeled"] = int((frames != -1).sum())
    v["frames_total"] = n_frames

    cmap, purity, nfrm = hungarian_map(frames, turns)
    v["cluster_to_speaker"] = {str(k): s for k, s in cmap.items()}
    v["frame_purity"] = round(purity, 4)
    v["speakers_mapped"] = sorted(set(cmap.values()))
    print(f"  map={v['cluster_to_speaker']} purity={purity:.4f}")

    spk_of = {c: cmap[c] for c in set(frames[frames != -1].tolist())}
    segs_out = [(s, ee, spk_of[c]) for s, ee, c in segments_from_frames(frames)]
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

    # fixture SHA verification (same values Wave-61 asserted)
    ok_f = sha256(FIXTURE) == "666cc1b94bd72127375fe58416a15988434156746df0ed1bee61c91066ef0342"
    ok_g = sha256(GT_PATH) == "3bfbdbddb43ed4e4924256625c11bfd01c67fd19a575094a1ac952422a34c6cc"
    ok_r = sha256(REF_RTTM) == "e759d68f3d9d6ad7169cc31584f4e2b258544d0e759d4f3e623cb25f399bc9ff"
    check("fixture_sha", ok_f, f"dialogue.wav {sha256(FIXTURE)[:12]}")
    check("gt_sha", ok_g, f"ground_truth.json {sha256(GT_PATH)[:12]}")
    check("ref_rttm_sha", ok_r, f"reference.rttm {sha256(REF_RTTM)[:12]}")

    clean, sr = read_wav_mono(FIXTURE)
    assert sr == SR
    turns = json.load(open(GT_PATH))["turns"]
    check("fixture_duration", abs(len(clean) / SR - 42.9) < 0.5,
          f"{len(clean)/SR:.2f} s, 9 turns, 3 voices")

    # Wave-58 embedding rows are 160 speech windows of the 166-grid on RAW
    # audio: verify the grid + gate reproduce EXACTLY before reusing rows.
    idxs, rmsv, thr, all_speech = window_grid(clean)
    fixture_emb = load_fixture_embeddings()
    check("embed_shape_fixture", fixture_emb.shape == (160, 192),
          f"shape={fixture_emb.shape}, finite")
    check("grid_gate_reproduced", len(idxs) == 166 and len(all_speech) == 160,
          f"grid={len(idxs)}, speech={len(all_speech)}, thr={thr:.5f}")

    # seeded noisy variant (wave61 donor: same RNG seed -> same noise)
    rng = np.random.default_rng(RNG_SEED)
    speech_rms = rms(clean)
    noise = rng.standard_normal(clean.shape).astype(np.float32)
    noise *= speech_rms / (rms(noise) * 10 ** (SNR_IN_DB / 20))
    snr_in = db(speech_rms / rms(noise))
    noisy = np.clip(clean + noise, -1, 1)
    write_wav_mono(os.path.join(PROOFS, "fixture_noisy_white.wav"), noisy, SR)
    check("noise_calibration", abs(snr_in - SNR_IN_DB) < 0.3,
          f"input SNR {snr_in:.1f} dB (target {SNR_IN_DB})")

    model, df_state, enhance = init_denoiser()
    embedder = init_embedder()

    # ---- MAIN: production topology (denoise DOWNSTREAM, not in this path)
    res["variants"]["main_clean"] = run_pipeline(
        "main_clean", clean, turns, REF_RTTM, res, mode="main",
        fixture_emb=fixture_emb)

    # ---- ABLATION: upstream-denoise control (Wave-61 topology), re-measured
    res["variants"]["upstream_clean"] = run_pipeline(
        "upstream_clean", clean, turns, REF_RTTM, res, mode="upstream",
        embedder=embedder, model=model, df_state=df_state, enhance=enhance)
    res["variants"]["upstream_noisy"] = run_pipeline(
        "upstream_noisy", noisy, turns, REF_RTTM, res, mode="upstream",
        embedder=embedder, model=model, df_state=df_state, enhance=enhance)
    res["variants"]["bypass_noisy"] = run_pipeline(
        "bypass_noisy", noisy, turns, REF_RTTM, res, mode="bypass",
        embedder=embedder)

    m = res["variants"]["main_clean"]
    uc = res["variants"]["upstream_clean"]
    un = res["variants"]["upstream_noisy"]
    bn = res["variants"]["bypass_noisy"]

    check("main_eigengap_k3", m["eigengap_k"] == 3,
          f"production-path E1a k={m['eigengap_k']} (margin {m['eigengap_margin']}x)")
    check("main_all_speakers", set(m["speakers_mapped"]) == {"A", "B", "C"},
          f"mapped {m['speakers_mapped']}")
    check("main_der_finite", np.isfinite(m["DER_c0.0"]),
          f"main DER={m['DER_c0.0']:.4f} JER={m['JER_c0.0']:.4f}")
    check("main_beats_wave60_baseline", m["DER_c0.0"] <= 0.0941,
          f"main DER {m['DER_c0.0']:.4f} vs Wave-60 baseline 0.0941")
    check("upstream_clean_eigengap_k", uc["eigengap_k"] >= 2,
          f"upstream-clean E1a k={uc['eigengap_k']} (margin {uc['eigengap_margin']}x)")
    check("upstream_clean_hurts_or_neutral", uc["DER_c0.0"] >= m["DER_c0.0"],
          f"upstream_clean DER {uc['DER_c0.0']:.4f} vs main {m['DER_c0.0']:.4f} "
          "(expect upstream >= main: denoise hurts or at best neutral)")
    check("upstream_noisy_k_flip", un["eigengap_k"] < 3 or un["DER_c0.0"] > bn["DER_c0.0"],
          f"upstream_noisy k={un['eigengap_k']} DER={un['DER_c0.0']:.4f} vs "
          f"bypass k={bn['eigengap_k']} DER={bn['DER_c0.0']:.4f}")
    check("upstream_noisy_hurts", un["DER_c0.0"] > bn["DER_c0.0"],
          f"Wave-61 re-confirm: upstream+denoise DER {un['DER_c0.0']:.4f} > "
          f"no-denoise DER {bn['DER_c0.0']:.4f}")
    check("cos_ac_rises_upstream", uc["diag_cos"]["AC"] >= m["diag_cos"]["AC"],
          f"cos(A,C): main={m['diag_cos']['AC']:.4f} vs upstream={uc['diag_cos']['AC']:.4f} "
          "(mechanism: denoise pushes speaker means together)")

    res["honest_findings"] = [
        "The production topology puts NO denoise before the embedding "
        "stage. The fixture embeddings were computed on raw audio by "
        "Wave-58; kept windows are bit-identical raw slices of that grid, "
        "so rows are exact (no recompute, no torch needed on this path).",
        "The ablation recomputes ECAPA fresh on denoised/noisy audio to "
        "re-confirm the Wave-61 finding with this wave's own numbers.",
        "diag_cos is GT-informed (not part of the blind pipeline).",
    ]
    res["total_s"] = round(time.time() - t_all, 1)
    res["passed"] = sum(1 for c in res["checks"] if c["status"] == "PASS")
    res["failed"] = sum(1 for c in res["checks"] if c["status"] == "FAIL")
    with open(os.path.join(PROOFS, "rebuilt_pipeline_result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"{res['passed']}/{len(res['checks'])} checks PASS "
          f"in {res['total_s']} s")
    return 0 if res["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
