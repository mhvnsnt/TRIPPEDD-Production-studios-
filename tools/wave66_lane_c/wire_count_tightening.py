#!/usr/bin/env python3
"""Wave 66 Lane C — tighten the blind speaker-count decision.

Wave 65 ported the production diarization operating point (DER 0.0382 exact
repro on the fixture) but on REAL EP01 audio the blind eigengap speaker-count
margin is 1.02x — fragile. This script tests three count-tightening
approaches, measured honestly on the Wave-65 fixture (GT: 3 speakers) AND on
real EP01 episode audio (blind):

  (a) longer analysis windows for the count decision
  (b) VAD-gated energy clustering (log-RMS + delta, k-means BIC) as a count
      prior, combined with the eigengap by a transparent fallback rule
  (c) ASR-assisted speaker turns: faster-whisper (MIT) word timestamps ->
      inter-pause units (IPUs) -> per-IPU mean ECAPA embeddings -> count on
      turn-level embeddings instead of dense correlated windows

Quarantine (Wave-61 production rule): ECAPA embeddings are ALWAYS computed
on RAW audio. ASR is a *segmentation donor* — its word timestamps gate which
windows get averaged; no denoised/transformed audio ever feeds the speaker
path. DeepFilterNet is NOT wired (blocked: deepfilterlib has no cp312 wheel
and needs a Rust toolchain this VM lacks — recorded in PROOFS.md).

Donor-first: VAD/grid/eigengap/RTTM/scoring/fill come from the wave63/wave64
lane modules and the wave65 production wire (weight fetch, raw ECAPA
compute). This file adds only: parameterized grids, the three count
experiments, bootstrap stability, and the ASR stage.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W63 = os.path.join(HERE, "..", "wave63_lane_c")
W64 = os.path.join(HERE, "..", "wave64_lane_c")
W65 = os.path.join(HERE, "..", "wave65_lane_c")
sys.path.insert(0, W63)
sys.path.insert(0, W64)
sys.path.insert(0, W65)
import wire_vad_coverage_recovery as w63  # noqa: E402
import wire_vad_recall_experiment as w64  # noqa: E402
import wire_diarize_production as w65prod  # noqa: E402

SR = 16000
FRAME_HOP = 0.25  # scoring/labeling frame resolution (matches w63 HOP_S)
PROVEN_VAD = {"agg": 0, "frame_ms": 10, "pad": 0.3, "use_pad": True}
GATE_FRAC = 0.08
MARGIN_TRUST = 1.5  # (b) fallback threshold: trust eigengap iff margin >= this
_TORCH_THREADS_SET = False  # torch thread config is one-shot per process


# ------------------------------------------------------------- grid helpers
def grid(audio, win_s, hop_s):
    """Parameterized window grid: idxs (sample offsets), rms vector, energy
    gate threshold, speech window positions."""
    win, hop = int(win_s * SR), int(hop_s * SR)
    idxs = list(range(0, len(audio) - win + 1, hop))
    rmsv = np.array([w63.rms(audio[i:i + win]) for i in idxs])
    thr = GATE_FRAC * float(np.max(rmsv))
    speech = set(np.flatnonzero(rmsv >= thr).tolist())
    return idxs, rmsv, thr, speech


def kept_windows(audio, idxs, win_s, vad_segs, gate_frac=GATE_FRAC):
    """Energy gate + strict VAD inclusion (window fully inside a VAD seg)."""
    win = int(win_s * SR)
    rmsv = np.array([w63.rms(audio[i:i + win]) for i in idxs])
    thr = gate_frac * float(np.max(rmsv))
    kept = [j for j in range(len(idxs))
            if rmsv[j] >= thr
            and w63.inside_vad(idxs[j] / SR, (idxs[j] + win) / SR, vad_segs)]
    return kept, rmsv, thr


# ------------------------------------------------------------- ECAPA (raw)
def compute_embeddings(audio, idxs, win_s, scratch, tag):
    """Real ECAPA-TDNN on RAW audio (quarantine: no upstream denoise).
    Row p of the cache == grid window p. Reuses wave65's weight fetcher."""
    npy_path = os.path.join(scratch, f"emb_{tag}.npy")
    if (os.path.isfile(npy_path)
            and np.load(npy_path, mmap_mode="r").shape == (len(idxs), 192)):
        embs = np.load(npy_path).astype(np.float64)
        assert np.all(np.isfinite(embs))
        print(f"  [emb] cached {npy_path} {embs.shape}", flush=True)
        return embs
    import torch
    global _TORCH_THREADS_SET
    if not _TORCH_THREADS_SET:
        # one-shot per process: later calls raise RuntimeError
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
        _TORCH_THREADS_SET = True
    w65prod.fetch_weights(os.path.join(scratch, "ecapa_weights"))
    from speechbrain.inference import EncoderClassifier
    clf = EncoderClassifier.from_hparams(
        source=os.path.join(scratch, "ecapa_weights"),
        savedir=os.path.join(scratch, "ecapa_weights", "sb_tmp"),
        run_opts={"device": "cpu"})
    win = int(win_s * SR)
    embs, B = [], 8
    with torch.no_grad():
        for i in range(0, len(idxs), B):
            batch = np.stack([audio[j:j + win] for j in idxs[i:i + B]])
            wavs = torch.from_numpy(batch.astype(np.float32))
            e = clf.encode_batch(wavs)
            embs.append(e.squeeze(1).cpu().numpy())
            if (i // B) % 20 == 0:
                print(f"  [emb] {tag}: {min(i + B, len(idxs))}/{len(idxs)}",
                      flush=True)
    embs = np.concatenate(embs, axis=0).astype(np.float64)
    assert embs.shape == (len(idxs), 192) and np.all(np.isfinite(embs))
    np.save(npy_path, embs)
    print(f"  [emb] saved {npy_path} {embs.shape}", flush=True)
    return embs


# ------------------------------------------------------------- count helpers
def count_eigengap(emb, k_min, k_max, knn_k=7):
    """Blind eigengap with sample-count-adaptive guards."""
    n = emb.shape[0]
    k_max = min(k_max, n - 1)
    k_min = min(k_min, k_max)
    kk = min(knn_k, n - 2)  # w63 uses kth=knn_k+1 < n in argpartition
    kk = max(kk, 1)
    k_est, eigs, gaps, margin = w63.eigengap_laplacian(
        emb, k_min=k_min, k_max=k_max, knn_k=kk)
    return k_est, margin, {str(k): round(v, 5) for k, v in gaps.items()}


def bootstrap_stability(emb, k_min, k_max, B=20, seed=66):
    """P(count == modal count) over bootstrap resamples — the blind
    tightness metric for real audio (no GT). Deterministic seed."""
    rng = np.random.default_rng(seed)
    n = emb.shape[0]
    ks = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        k, _, _ = count_eigengap(emb[idx], k_min, k_max)
        ks.append(k)
    ks = np.array(ks)
    vals, cnts = np.unique(ks, return_counts=True)
    mode = int(vals[np.argmax(cnts)])
    return {"B": B, "ks": ks.tolist(),
            "mode": mode, "p_mode": float(cnts.max() / B),
            "dist": {str(int(v)): int(c) for v, c in zip(vals, cnts)}}


def cluster_forced(emb, k):
    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=k, max_clusters=k,
                           custom_dist="cosine")
    return np.asarray(cl.predict(emb), dtype=int)


def frames_from_window_labels(kept, labels, idxs, win_s, vad_segs, audio_len):
    """0.25 s frames: nearest kept-window-center wins (frame center must be
    inside VAD). Generalizes w63.label_v2c_no_fill to arbitrary grids."""
    n_frames = int(math.ceil((audio_len / SR) / FRAME_HOP))
    frames = np.full(n_frames, -1, dtype=int)
    best_d = np.full(n_frames, np.inf)
    for j, lab in zip(kept, labels):
        t0, t1 = idxs[j] / SR, idxs[j] / SR + win_s
        wcenter = (t0 + t1) / 2.0
        f0 = max(0, int(math.floor(t0 / FRAME_HOP)))
        f1 = min(n_frames, int(math.ceil(t1 / FRAME_HOP)))
        for f in range(f0, f1):
            tc = (f + 0.5) * FRAME_HOP
            if not any(a <= tc < b for a, b in vad_segs):
                continue
            d = abs(tc - wcenter)
            if d < best_d[f]:
                best_d[f] = d
                frames[f] = int(lab)
    return frames


def score_frames(frames, ref_rttm, out_dir, tag, uri):
    """Frames -> RTTM -> DER/JER (collar 0 and 0.25)."""
    segs = [(s, e, f"SPK{int(c):02d}")
            for s, e, c in w63.segments_from_frames(frames)]
    hyp = os.path.join(out_dir, f"hyp_{tag}.rttm")
    w63.write_rttm(hyp, segs, uri=uri)
    d, j, comp = w63.score(ref_rttm, hyp, 0.0)
    d25, j25, _ = w63.score(ref_rttm, hyp, 0.25)
    return {"DER": round(d, 4), "JER": round(j, 4),
            "DER_c025": round(d25, 4), "JER_c025": round(j25, 4),
            "miss": round(comp["missed detection"], 3),
            "FA": round(comp["false alarm"], 3),
            "conf": round(comp["confusion"], 3),
            "n_segs": len(segs), "hyp_rttm": hyp}

# ------------------------------------------------------------- experiment (a)
def exp_long_windows(audio, vad_segs, scratch, out_dir, kmin, kmax,
                     ref_rttm, uri, turns):
    """(a) Longer analysis windows for the count decision. Baseline
    (1.5 s / 0.25 s) reproduces the wave65 operating point; longer windows
    give each embedding more phonetic content but blur turn boundaries."""
    res = {}
    for win_s, hop_s in [(1.5, 0.25), (2.0, 0.5), (2.5, 0.5), (3.0, 0.5),
                         (2.5, 0.25)]:
        tag = f"a_win{win_s}_hop{hop_s}".replace(".", "p")
        print(f"  [a] grid {win_s}s/{hop_s}s", flush=True)
        idxs, _, _, _ = grid(audio, win_s, hop_s)
        emb_all = compute_embeddings(audio, idxs, win_s, scratch, tag)
        kept, rmsv, thr = kept_windows(audio, idxs, win_s, vad_segs)
        emb = emb_all[np.asarray(kept)]
        k, margin, gaps = count_eigengap(emb, kmin, kmax)
        stab = bootstrap_stability(emb, kmin, kmax)
        labels = cluster_forced(emb, k)
        f0 = frames_from_window_labels(kept, labels, idxs, win_s, vad_segs,
                                       len(audio))
        f1 = w63.fill_within_vad(f0, vad_segs,
                                 int(math.ceil((len(audio) / SR) / FRAME_HOP)))
        r = {"win_s": win_s, "hop_s": hop_s, "n_win": len(idxs),
             "kept_n": len(kept), "k": k, "margin": round(margin, 3),
             "gaps": gaps, "stability": stab}
        if turns is not None:
            cmap, purity, _ = w63.hungarian_map(f0, turns)
            r["purity"] = round(purity, 4)
            r["map"] = {str(a): b for a, b in cmap.items()}
            r.update(score_frames(f1, ref_rttm, out_dir, tag, uri))
        print(f"    k={k} margin={margin:.2f}x stable={stab['p_mode']:.2f} "
              f"kept={len(kept)}/{len(idxs)}"
              + (f" DER={r.get('DER')}" if turns else ""), flush=True)
        res[tag] = r
    return res


# ------------------------------------------------------------- experiment (b)
def exp_energy_prior(audio, vad_segs, out_dir, kmin, kmax, ref_rttm, uri,
                     turns, emb_baseline, kept_baseline):
    """(b) VAD-gated energy clustering as a count prior.

    Independent evidence family (prosodic energy vs spectral embeddings):
    k-means on [log RMS, delta log RMS] over VAD-gated 0.25 s frames,
    k chosen by BIC. Combination rule (transparent): trust the eigengap
    when its margin >= MARGIN_TRUST, else fall back to the energy prior.
    The prior is VALIDATED on the fixture (GT k=3) before any adoption."""
    from sklearn.cluster import KMeans
    res = {}
    # fine-grid frame features, VAD-gated + energy-gated
    hop = int(FRAME_HOP * SR)
    n_fr = int(math.ceil(len(audio) / hop))
    lrms = np.array([math.log(w63.rms(audio[i * hop:(i + 1) * hop]) + 1e-9)
                     for i in range(n_fr)])
    inside = np.array([any(a <= (i + 0.5) * FRAME_HOP < b
                           for a, b in vad_segs) for i in range(n_fr)])
    thr = GATE_FRAC * float(np.max(np.exp(lrms)))
    gated = inside & (np.exp(lrms) >= thr)
    d = np.gradient(lrms)
    X = np.stack([lrms[gated], d[gated]], axis=1)
    n = X.shape[0]
    print(f"  [b] VAD-gated energy frames: {n}/{n_fr}", flush=True)

    bic, rss = {}, {}
    kmax_e = min(10, n - 1)
    for k in range(1, kmax_e + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
        r = float(np.sum((X - km.cluster_centers_[km.labels_]) ** 2))
        rss[k] = r
        p = k * 2 + (k - 1)  # means + mixture weights
        bic[k] = n * math.log(max(r, 1e-12) / n) + p * math.log(n)
    k_e = min(bic, key=lambda k: bic[k])
    res["energy"] = {"n_frames": n, "k_bic": k_e,
                     "bic": {str(k): round(v, 1) for k, v in bic.items()}}
    print(f"    energy-BIC k={k_e}", flush=True)

    # baseline eigengap on the same audio (dense-window embeddings)
    k_g, margin_g, gaps_g = count_eigengap(emb_baseline, kmin, kmax)
    res["eigengap"] = {"k": k_g, "margin": round(margin_g, 3), "gaps": gaps_g}

    # combination rule
    if margin_g >= MARGIN_TRUST:
        k_final, source = k_g, "eigengap(margin>=trust)"
    else:
        k_final, source = int(k_e), "energy-prior(fallback)"
    res["combined"] = {"k_final": k_final, "source": source,
                       "trust_thr": MARGIN_TRUST}
    print(f"    combined k={k_final} via {source}", flush=True)

    # fixture validation: does the prior agree with GT?
    gt_k = len(set(t["speaker"] for t in turns)) if turns else None
    res["fixture_validation"] = {
        "gt_k": gt_k,
        "prior_agrees_with_gt": (k_e == gt_k) if gt_k else None,
        "adopted": (margin_g >= MARGIN_TRUST) or (k_e == gt_k) if gt_k
                   else "blind: fallback used"}
    if turns is not None and k_final != k_g:
        # recluster at the prior count and score (honest: may be worse)
        labels = cluster_forced(emb_baseline, k_final)
        kept = kept_baseline
        idxs = kept_baseline["idxs"]
        f0 = frames_from_window_labels(kept["kept"], labels, idxs, 1.5,
                                       vad_segs, len(audio))
        f1 = w63.fill_within_vad(f0, vad_segs, int(math.ceil(
            (len(audio) / SR) / FRAME_HOP)))
        res["combined"].update(score_frames(f1, ref_rttm, out_dir,
                                            "b_combined", uri))
    return res


# ------------------------------------------------------------- experiment (c)
def _sanitize_proxy_env():
    """TOOLS.md quirk: httpx (used by huggingface_hub for the model
    download) crashes parsing IPv6 literals in no_proxy/NO_PROXY
    (`Invalid port: ':1]'`). Strip any entry containing '::'; the egress
    proxy itself (http_proxy/https_proxy) stays set."""
    for var in ("no_proxy", "NO_PROXY"):
        v = os.environ.get(var)
        if v and "::" in v:
            os.environ[var] = ",".join(p for p in v.split(",")
                                       if "::" not in p)


def asr_words(audio, scratch):
    """faster-whisper (MIT) word timestamps on RAW audio. The words are a
    *segmentation donor* for turn boundaries; audio fed to ASR is the raw
    mix — no denoise anywhere near the speaker path."""
    from faster_whisper import WhisperModel
    _sanitize_proxy_env()
    # main() sets HF_HUB_OFFLINE=1 for the local ECAPA weights; the
    # faster-whisper model download needs the hub — scope the override.
    _old_offline = os.environ.get("HF_HUB_OFFLINE")
    os.environ["HF_HUB_OFFLINE"] = "0"
    try:
        model = WhisperModel("base.en", device="cpu", compute_type="int8",
                             download_root=os.path.join(scratch, "fw_models"))
    finally:
        if _old_offline is None:
            os.environ.pop("HF_HUB_OFFLINE", None)
        else:
            os.environ["HF_HUB_OFFLINE"] = _old_offline
    t0 = time.time()
    segments, info = model.transcribe(audio, language="en",
                                      word_timestamps=True,
                                      vad_filter=False)
    words = []
    for seg in segments:
        for w in (seg.words or []):
            words.append({"start": float(w.start), "end": float(w.end),
                          "word": w.word, "prob": float(w.probability)})
    dt = time.time() - t0
    print(f"  [c] ASR: {len(words)} words, lang_prob={info.language_probability:.2f}, "
          f"{dt:.0f}s", flush=True)
    return words, dt


def ipus_from_words(words, vad_segs, gap_s=0.5):
    """Inter-pause units: split the word stream where the inter-word gap
    exceeds gap_s; drop words outside VAD."""
    vw = [w for w in words
          if any(w65prod.overlap(w["start"], w["end"], a, b) > 0
                 for a, b in vad_segs)]
    ipus, cur = [], []
    prev_end = None
    for w in sorted(vw, key=lambda x: x["start"]):
        if cur and prev_end is not None and w["start"] - prev_end > gap_s:
            ipus.append({"start": cur[0]["start"], "end": cur[-1]["end"],
                         "words": cur})
            cur = []
        cur.append(w)
        prev_end = w["end"]
    if cur:
        ipus.append({"start": cur[0]["start"], "end": cur[-1]["end"],
                     "words": cur})
    return ipus


def exp_asr_turns(audio, vad_segs, scratch, out_dir, kmin, kmax,
                  ref_rttm, uri, turns, emb_fine, kept_fine, idxs_fine,
                  ipu_gap_s=0.5):
    """(c) Count on turn-level (IPU) embeddings: average the fine-grid
    window embeddings inside each ASR-derived IPU, then eigengap on the
    ~independent turn samples instead of dense correlated windows."""
    res = {}
    words, asr_s = asr_words(audio, scratch)
    res["asr"] = {"n_words": len(words), "seconds": round(asr_s, 1),
                  "model": "base.en-int8-cpu"}
    ipus = ipus_from_words(words, vad_segs, gap_s=ipu_gap_s)
    res["asr"]["ipu_gap_s"] = ipu_gap_s
    res["asr"]["n_ipus_raw"] = len(ipus)
    res["asr"]["mean_ipu_s"] = round(float(np.mean(
        [u["end"] - u["start"] for u in ipus])) if ipus else 0, 2)
    print(f"  [c] {len(ipus)} IPUs", flush=True)

    # per-IPU mean embedding from fine-grid windows whose center in IPU
    centers = np.array([idxs_fine[j] / SR + 0.75 for j in kept_fine])
    E = emb_fine[np.asarray(kept_fine)]
    ipu_emb, ipu_spans = [], []
    for u in ipus:
        m = (centers >= u["start"] - 0.25) & (centers <= u["end"] + 0.25)
        if m.sum() == 0:
            continue
        ipu_emb.append(E[m].mean(axis=0))
        ipu_spans.append((u["start"], u["end"]))
    ipu_emb = np.stack(ipu_emb) if ipu_emb else np.zeros((0, 192))
    res["asr"]["n_ipus_embedded"] = int(ipu_emb.shape[0])
    print(f"  [c] {ipu_emb.shape[0]} IPUs with embeddings", flush=True)
    if ipu_emb.shape[0] < kmin + 1:
        res["count"] = {"status": "insufficient_turns",
                        "n": int(ipu_emb.shape[0])}
        return res

    k, margin, gaps = count_eigengap(ipu_emb, kmin, kmax)
    stab = bootstrap_stability(ipu_emb, kmin, kmax)
    res["count"] = {"k": k, "margin": round(margin, 3), "gaps": gaps,
                    "stability": stab}
    print(f"    IPU eigengap k={k} margin={margin:.2f}x "
          f"stable={stab['p_mode']:.2f}", flush=True)

    labels = cluster_forced(ipu_emb, k)
    # propagate IPU labels to 0.25 s frames
    n_frames = int(math.ceil((len(audio) / SR) / FRAME_HOP))
    f0 = np.full(n_frames, -1, dtype=int)
    for (s, e), lab in zip(ipu_spans, labels):
        f0[int(s / FRAME_HOP):int(math.ceil(e / FRAME_HOP))] = int(lab)
    f1 = w63.fill_within_vad(f0, vad_segs, n_frames)
    if turns is not None:
        cmap, purity, _ = w63.hungarian_map(f0, turns)
        res["purity"] = round(purity, 4)
        res["map"] = {str(a): b for a, b in cmap.items()}
        res.update(score_frames(f1, ref_rttm, out_dir, "c_ipu", uri))
        print(f"    DER={res.get('DER')} JER={res.get('JER')}", flush=True)
    return res


# ------------------------------------------------------------- deepfilternet
def deepfilternet_status():
    """Wave-61 rule: denoise must never sit upstream of ECAPA. This probe
    only establishes whether a cp312-compatible DeepFilterNet exists."""
    st = {"expected_role": "downstream-of-embeddings only (caption/ASR path)",
          "df3_checkpoint_cache": os.path.expanduser(
              "~/.cache/DeepFilterNet/DeepFilterNet3")}
    st["checkpoint_bytes_present"] = os.path.isdir(
        st["df3_checkpoint_cache"])
    try:
        import deepfilternet  # noqa
        st["import"] = "ok"
    except Exception as e:
        st["import"] = f"failed: {type(e).__name__}: {e}"
    try:
        import deepfilterlib  # noqa
        st["deepfilterlib"] = "ok"
    except Exception as e:
        st["deepfilterlib"] = (f"missing: deepfilterlib has no cp312 wheel "
                               f"on PyPI and needs a Rust toolchain "
                               f"({type(e).__name__})")
    st["wired"] = False
    return st

# ------------------------------------------------------------- baseline
def run_baseline(audio, vad_segs, scratch, out_dir, kmin, kmax, ref_rttm,
                 uri, turns, w65_proofs_dir):
    """Wave-65 operating point reproduction: 1.5 s / 0.25 s grid on RAW
    audio. Reuses wave65's cached raw embeddings when the grid matches
    exactly (shape-checked), plus a fresh 8-window ECAPA spot-check proving
    the reuse chain."""
    tag = "a_win1p5_hop0p25"
    idxs, _, _, _ = grid(audio, 1.5, 0.25)
    cached = os.path.join(w65_proofs_dir, "embeddings_raw.npy")
    emb_all, reuse = None, "recomputed"
    if os.path.isfile(cached):
        c = np.load(cached)
        if c.shape == (len(idxs), 192) and np.all(np.isfinite(c)):
            emb_all = c.astype(np.float64)
            reuse = "wave65-cache"
            # mirror into this lane's scratch cache so exp (a) hits it
            np.save(os.path.join(scratch, f"emb_{tag}.npy"), emb_all)
            print(f"  [base] reusing wave65 embeddings {c.shape}", flush=True)
    if emb_all is None:
        emb_all = compute_embeddings(audio, idxs, 1.5, scratch, tag)
    kept, rmsv, thr = kept_windows(audio, idxs, 1.5, vad_segs)
    emb = emb_all[np.asarray(kept)]
    k, margin, gaps = count_eigengap(emb, kmin, kmax)
    stab = bootstrap_stability(emb, kmin, kmax)
    labels = cluster_forced(emb, k)
    f0 = frames_from_window_labels(kept, labels, idxs, 1.5, vad_segs,
                                   len(audio))
    n_fr = int(math.ceil((len(audio) / SR) / FRAME_HOP))
    f1 = w63.fill_within_vad(f0, vad_segs, n_fr)
    r = {"grid": "1.5s/0.25s", "embedding_source": reuse,
         "n_win": len(idxs), "kept_n": len(kept), "thr": round(float(thr), 5),
         "k": k, "margin": round(margin, 3), "gaps": gaps,
         "stability": stab}
    if turns is not None:
        cmap, purity, _ = w63.hungarian_map(f0, turns)
        r["purity"] = round(purity, 4)
        r["map"] = {str(a): b for a, b in cmap.items()}
        r.update(score_frames(f1, ref_rttm, out_dir, "base", uri))
    return r, {"emb": emb, "emb_all": emb_all, "kept": kept, "idxs": idxs}


def spotcheck_embeddings(audio, idxs, emb_cached, scratch):
    """Fresh ECAPA encode of 8 spread windows vs the reused cache rows —
    proves the reuse chain end-to-end (model + audio path)."""
    import torch
    global _TORCH_THREADS_SET
    if not _TORCH_THREADS_SET:
        torch.set_num_threads(1)
        _TORCH_THREADS_SET = True
    w65prod.fetch_weights(os.path.join(scratch, "ecapa_weights"))
    from speechbrain.inference import EncoderClassifier
    clf = EncoderClassifier.from_hparams(
        source=os.path.join(scratch, "ecapa_weights"),
        savedir=os.path.join(scratch, "ecapa_weights", "sb_tmp"),
        run_opts={"device": "cpu"})
    picks = np.linspace(0, len(idxs) - 1, 8).astype(int)
    win = int(1.5 * SR)
    with torch.no_grad():
        batch = np.stack([audio[idxs[p]:idxs[p] + win] for p in picks])
        e = clf.encode_batch(torch.from_numpy(
            batch.astype(np.float32))).squeeze(1).cpu().numpy()
    a, b = e.astype(np.float64), emb_cached[picks].astype(np.float64)
    cos = np.sum(a * b, axis=1) / (np.linalg.norm(a, axis=1)
                                   * np.linalg.norm(b, axis=1))
    return {"n": 8, "cos_min": round(float(cos.min()), 6),
            "cos_mean": round(float(cos.mean()), 6)}


# ------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["fixture", "production", "both"],
                    default="both")
    ap.add_argument("--exp", choices=["a", "b", "c", "all"], default="all")
    ap.add_argument("--skip-asr", action="store_true",
                    help="skip experiment (c) ASR stage")
    ap.add_argument("--ipu-gap", type=float, default=0.5,
                    help="inter-word gap (s) that splits ASR IPUs")
    a = ap.parse_args()
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    out = os.path.join(HERE, "proofs")
    os.makedirs(out, exist_ok=True)
    scratch = os.path.join(HERE, "scratch")
    os.makedirs(scratch, exist_ok=True)
    t0 = time.time()
    res = {"wave": 66, "lane": "C",
           "goal": "tighten blind speaker-count decision",
           "quarantine": "ECAPA always on RAW audio; no denoise upstream"}

    modes = []
    if a.only in ("fixture", "both"):
        modes.append("fixture")
    if a.only in ("production", "both"):
        modes.append("production")

    for mode in modes:
        print(f"\n=== {mode} ===", flush=True)
        mr = {}
        if mode == "fixture":
            audio, turns, _ = w63.load_fixture()
            uri, ref_rttm = "dialogue", w63.REF_RTTM
            kmin, kmax = 2, 6
            print("  fixture SHA-verified (dialogue.wav, 9 turns, 3 voices)",
                  flush=True)
        else:
            audio_in = os.path.abspath(os.path.join(
                HERE, "..", "..", "production", "WIZARD_GANG_EP01",
                "audio-orig.m4a"))
            assert os.path.isfile(audio_in), audio_in
            audio, dur, _ = w65prod.load_audio_any(audio_in, scratch)
            turns, ref_rttm, uri = None, None, "ep01_audio_orig"
            kmin, kmax = 1, 10
            print(f"  real EP01 audio: {dur:.1f}s (read-only)", flush=True)

        vad_segs = w64.vad_segments_gen(audio, **PROVEN_VAD)
        speech_s = sum(b - x for x, b in vad_segs)
        mr["vad"] = {"n_segs": len(vad_segs),
                     "speech_s": round(speech_s, 2),
                     "frac": round(speech_s / (len(audio) / SR), 4)}

        w65_proofs = os.path.join(W65, "proofs", mode)
        base, ctx = run_baseline(audio, vad_segs, scratch, out, kmin, kmax,
                                 ref_rttm, uri, turns, w65_proofs)
        mr["baseline"] = base
        print(f"  [base] k={base['k']} margin={base['margin']}x "
              f"stable={base['stability']['p_mode']:.2f} "
              f"kept={base['kept_n']}/{base['n_win']}"
              + (f" DER={base.get('DER')} JER={base.get('JER')}"
                 if turns else ""), flush=True)
        if turns is not None and base["embedding_source"] == "wave65-cache":
            sc = spotcheck_embeddings(audio, ctx["idxs"], ctx["emb_all"],
                                      scratch)
            mr["baseline"]["spotcheck"] = sc
            print(f"  [base] spot-check cos min/mean: "
                  f"{sc['cos_min']}/{sc['cos_mean']}", flush=True)

        # (a) long windows — baseline entry already measured; run the rest
        if a.exp in ("a", "all"):
            ar = exp_long_windows(audio, vad_segs, scratch, out, kmin, kmax,
                                  ref_rttm, uri, turns)
            # the (1.5,0.25) entry recomputes from cache: drop in favor of
            # the instrumented baseline above (identical inputs)
            ar["a_win1p5_hop0p25"] = base
            mr["exp_a_long_windows"] = ar

        # (b) energy prior
        if a.exp in ("b", "all"):
            mr["exp_b_energy_prior"] = exp_energy_prior(
                audio, vad_segs, out, kmin, kmax, ref_rttm, uri, turns,
                ctx["emb"], {"kept": ctx["kept"], "idxs": ctx["idxs"]})

        # (c) ASR turns
        if a.exp in ("c", "all") and not a.skip_asr:
            mr["exp_c_asr_turns"] = exp_asr_turns(
                audio, vad_segs, scratch, out, kmin, kmax, ref_rttm, uri,
                turns, ctx["emb_all"], ctx["kept"], ctx["idxs"],
                ipu_gap_s=a.ipu_gap)

        res[mode] = mr
        # incremental write: a restart kills the process, not the evidence
        with open(os.path.join(out, "w66_results.json"), "w") as f:
            json.dump(res, f, indent=2)
        print(f"  [ckpt] mode {mode} written", flush=True)

    res["deepfilternet"] = deepfilternet_status()
    res["elapsed_s"] = round(time.time() - t0, 1)
    with open(os.path.join(out, "w66_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\nresults -> {out}/w66_results.json ({res['elapsed_s']}s)",
          flush=True)


if __name__ == "__main__":
    main()
