#!/usr/bin/env python3
"""Wave 64 Lane C — VAD-recall experiment (the only remaining coverage lever
from Wave-63 Lane C's findings).

Wave-63 closed the labeling side: fill-within-VAD-speech (F1) reached DER
0.0712 / JER 0.0700 (miss 2.67 / FA 0.12 / conf 0.00) on the Wave-58 fixture
(42.9 s @16 kHz, 9 turns, 3 Kokoro voices). The residual 2.67 s miss equals
the VAD's own recall ceiling (webrtcvad aggressiveness 0, 10 ms frames,
0.2 s hangover pad: recall 0.9351 x 39.3 s GT speech ~= 2.55 s). No
labeling policy can recover speech the VAD never marked — so this wave
systematically tunes the VAD itself:

  Phase A: VAD-quality grid — webrtcvad aggressiveness 0..3 x frame size
           10/20/30 ms x hangover-pad 0.0/0.1/0.2/0.25/0.3/0.35/0.4/0.5 s.
           Frame-level recall/precision/F1 vs ground truth. The extended
           pad range maps the FA cliff (inter-turn gaps are 0.4 s).
  Phase B: hangover/merge tuning on the Phase-A winner — explicit
           trigger/hangover logic (T_on x T_off) x gap-merge window.
  Phase C: full diarization pipeline (windows -> energy gate -> VAD-kept
           windows -> fixture ECAPA embeddings -> eigengap count ->
           forced-k SpectralCluster -> GT-informed Hungarian map ->
           F0 no-fill + F1 fill-within-VAD labeling -> DER/JER/miss/FA/conf
           via pyannote-metrics) on the top-K VAD configs + the Wave-63
           baseline as control.
  Phase D: energy-gate threshold x window-inclusion criterion sensitivity
           on the Phase-C winner.

Goal: recover missed speech without letting false alarms explode.
Two outputs: (1) min-DER config (the measured optimum), (2) the
recommended PRODUCTION operating point = min DER subject to FA <= 0.5 s
(the knee: beyond it, FA explodes for marginal DER gains).

Torch-free: embeddings parsed raw float32 from the torch zip container
(the Waves 59/60 trick); denoise stays quarantined OFF the speaker path
entirely (no DeepFilterNet anywhere in this script).

Licenses (wired path): webrtcvad MIT, SpectralCluster Apache-2.0,
pyannote-metrics MIT, scikit-learn/numpy/scipy BSD. Lane code original,
MIT. No new third-party tool is wired.
"""
import itertools
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "vad_recall")
os.makedirs(PROOFS, exist_ok=True)

# Reuse Wave-63's proven fixture/scoring/labeling code (don't rewrite).
W63 = os.path.join(HERE, "..", "wave63_lane_c")
sys.path.insert(0, W63)
import wire_vad_coverage_recovery as w63  # noqa: E402

SR = w63.SR
WIN_S, HOP_S = w63.WIN_S, w63.HOP_S
FRAME_EVAL = 0.01  # VAD quality evaluated at 10 ms frames (wave63 convention)


# ------------------------------------------------- generalized VAD
def vad_decisions(audio, sr=SR, agg=0, frame_ms=10):
    """Raw webrtcvad speech decisions, one per frame_ms frame."""
    import webrtcvad
    assert frame_ms in (10, 20, 30)
    vad = webrtcvad.Vad(agg)
    frame_n = int(frame_ms / 1000 * sr)
    frame_s = frame_ms / 1000.0
    decisions = []
    for i in range(0, len(audio), frame_n):
        fr = audio[i:i + frame_n]
        if len(fr) < frame_n:
            fr = np.pad(fr, (0, frame_n - len(fr)))
        b = (np.clip(fr, -1, 1) * 32767).astype(np.int16).tobytes()
        decisions.append(bool(vad.is_speech(b, sr)))
    return decisions, frame_s


def segments_from_runs(decisions, frame_s, t_on=1, t_off=1):
    """Trigger/hangover segmentation: open after t_on consecutive speech
    frames; close after t_off consecutive non-speech frames. The segment
    spans the first speech frame through the LAST speech frame (hangover
    silence bridges runs but does not extend the trailing edge — matching
    wave63's close-at-first-silence-frame behavior when t_off=1)."""
    segs = []
    run_start, n_speech, sil, last_speech = None, 0, 0, -1
    for i, d in enumerate(decisions):
        if d:
            if run_start is None:
                run_start, n_speech = i, 0
            n_speech += 1
            last_speech = i
            sil = 0
        else:
            sil += 1
            if run_start is not None:
                if n_speech >= t_on and sil >= t_off:
                    segs.append((run_start * frame_s,
                                 (last_speech + 1) * frame_s))
                    run_start, n_speech, sil = None, 0, 0
                elif n_speech < t_on:
                    # never triggered: discard the run
                    run_start, n_speech, sil = None, 0, 0
    if run_start is not None and n_speech >= t_on:
        segs.append((run_start * frame_s, (last_speech + 1) * frame_s))
    return segs


def merge_gaps(segs, merge_gap):
    merged = []
    for a, b in sorted(segs):
        if merged and a <= merged[-1][1] + merge_gap:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


def pad_merge(segs, pad):
    padded = [(max(0.0, a - pad), b + pad) for a, b in segs]
    return merge_gaps(padded, 0.0)


def vad_segments_gen(audio, agg=0, frame_ms=10, pad=0.2,
                     t_on=1, t_off=1, merge_gap=0.0, use_pad=True):
    """Generalized VAD segmentation. With (frame_ms=10, pad=0.2,
    use_pad=True) this is bit-equivalent to wave63.vad_segments."""
    decisions, frame_s = vad_decisions(audio, SR, agg, frame_ms)
    segs = segments_from_runs(decisions, frame_s, t_on=t_on, t_off=t_off)
    if use_pad:
        return pad_merge(segs, pad)
    return merge_gaps(segs, merge_gap)


def vad_quality_frames(segs, turns, audio_len):
    """Frame-level recall/precision/F1 of VAD segments vs GT speech."""
    n = int(audio_len / SR / FRAME_EVAL)
    gt = np.zeros(n, bool)
    va = np.zeros(n, bool)
    for t in turns:
        gt[int(t["start"] / FRAME_EVAL):int(t["end"] / FRAME_EVAL)] = True
    for a, b in segs:
        va[int(a / FRAME_EVAL):int(b / FRAME_EVAL)] = True
    tp = int((gt & va).sum())
    rec = tp / max(1, int(gt.sum()))
    prec = tp / max(1, int(va.sum()))
    f1 = 2 * rec * prec / max(1e-12, rec + prec)
    return rec, prec, f1, int(gt.sum()) * FRAME_EVAL


# Canonical Wave-58 embedding-row map: fixture embeddings.pt holds the 160
# grid windows that pass the 0.08 energy gate (Wave-58's choice). Loosening
# the gate admits windows with NO embedding rows — that needs a real ECAPA
# recompute (torch; deferred to the task-2 venv), so Phase D only tightens.
_CANON_ROW = None


def canon_row(audio):
    global _CANON_ROW
    if _CANON_ROW is None:
        _, rmsv, _, _ = w63.window_grid(audio)
        thr08 = w63.SILENCE_FRAC * float(np.max(rmsv))
        a08 = np.flatnonzero(rmsv >= thr08)
        assert len(a08) == 160, len(a08)
        _CANON_ROW = {int(j): i for i, j in enumerate(a08)}
    return _CANON_ROW


# ------------------------------------------------- full pipeline for one config
def run_pipeline(audio, turns, fixture_emb, vad_segs, sil_frac,
                 inclusion="strict"):
    """One full diarization run. Returns dict with DER/JER/components for
    F0 (no-fill) and F1 (fill-within-VAD) labelings, eigengap, purity."""
    idxs, rmsv, _, _ = w63.window_grid(audio)
    # energy gate threshold override (tightening only: rows must exist)
    thr = sil_frac * float(np.max(rmsv))
    assert sil_frac >= w63.SILENCE_FRAC, \
        f"gate {sil_frac} < 0.08 needs ECAPA recompute (no embedding rows)"
    all_speech = np.flatnonzero(rmsv >= thr)

    def keep(j):
        t0, t1 = j * HOP_S, j * HOP_S + WIN_S
        if inclusion == "strict":
            return w63.inside_vad(t0, t1, vad_segs)
        tc = (t0 + t1) / 2
        if inclusion == "center":
            return any(a <= tc < b for a, b in vad_segs)
        if inclusion == "overlap50":
            ov = sum(max(0.0, min(t1, b) - max(t0, a))
                     for a, b in vad_segs)
            return ov >= 0.5 * WIN_S
        raise ValueError(inclusion)

    kept = [int(j) for j in all_speech if keep(j)]
    row = canon_row(audio)
    assert all(int(j) in row for j in kept), "kept window lacks embedding row"
    if len(kept) < 2:
        return {"failed": "kept_windows<2", "kept": len(kept)}
    emb = fixture_emb[np.asarray([row[int(j)] for j in kept])]
    k_est, eigs, gaps, margin = w63.eigengap_laplacian(emb)

    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=k_est, max_clusters=k_est,
                           custom_dist="cosine")
    labels = np.asarray(cl.predict(emb), dtype=int)

    n_frames = int(math.ceil((len(audio) / SR) / HOP_S))
    frames_f0 = w63.label_v2c_no_fill(kept, labels, vad_segs, n_frames)
    frames_f1 = w63.fill_within_vad(frames_f0, vad_segs, n_frames)
    cmap, purity, _ = w63.hungarian_map(frames_f0, turns)
    spk_of = {c: cmap[c] for c in set(frames_f0[frames_f0 != -1].tolist())}

    out = {"failed": None, "kept": len(kept), "k": k_est,
           "margin": round(margin, 2), "purity": round(purity, 4),
           "grid": len(idxs), "energy_speech": int(len(all_speech))}
    for tag, fvar in (("F0", frames_f0), ("F1", frames_f1)):
        segs_out = [(s, e, spk_of[c])
                    for s, e, c in w63.segments_from_frames(fvar)]
        hyp_path = os.path.join(PROOFS, f"tmp_{tag}.rttm")
        w63.write_rttm(hyp_path, segs_out)
        d, j, comp = w63.score(w63.REF_RTTM, hyp_path, 0.0)
        d25, j25, comp25 = w63.score(w63.REF_RTTM, hyp_path, 0.25)
        out[tag] = {
            "DER": round(d, 4), "JER": round(j, 4),
            "miss": round(comp["missed detection"], 3),
            "FA": round(comp["false alarm"], 3),
            "conf": round(comp["confusion"], 3),
            "DER_c025": round(d25, 4), "JER_c025": round(j25, 4),
            "miss_c025": round(comp25["missed detection"], 3),
            "FA_c025": round(comp25["false alarm"], 3),
        }
    return out


def main():
    t0 = time.time()
    res = {"wave": 64, "lane": "C",
           "question": "VAD-recall experiment: tune the VAD to recover "
                       "missed speech without FA exploding"}
    checks = []

    def check(name, ok, detail):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}",
              flush=True)

    audio, turns, fixture_emb = w63.load_fixture()
    check("fixture_shas", True,
          "wave58 fixture SHA-verified (dialogue.wav, ground_truth.json, "
          "embeddings.pt, reference.rttm)")

    # --- cross-check: generalized VAD == wave63 VAD at baseline settings
    base_segs = vad_segments_gen(audio, agg=0, frame_ms=10, pad=0.2)
    w63_segs = w63.vad_segments(audio)
    same = (len(base_segs) == len(w63_segs) and
            all(abs(a - c) < 1e-9 and abs(b - d) < 1e-9
                for (a, b), (c, d) in zip(base_segs, w63_segs)))
    rec, prec, f1, gt_s = vad_quality_frames(base_segs, turns, len(audio))
    check("vad_generalized_matches_wave63", same,
          f"baseline segments identical to wave63: {same} "
          f"(n={len(base_segs)})")
    check("vad_baseline_reproduces_wave63",
          abs(rec - 0.9351) < 0.002 and prec == 1.0,
          f"recall={rec:.4f} (wave63 0.9351) prec={prec:.4f}")
    print(f"  baseline: {len(base_segs)} segs, rec={rec:.4f} "
          f"prec={prec:.4f} f1={f1:.4f}, GT speech={gt_s:.1f}s", flush=True)

    # --- Phase A: VAD-quality grid
    print("Phase A: aggressiveness x frame-size x pad grid ...", flush=True)
    phaseA = []
    for agg, fms, pad in itertools.product((0, 1, 2, 3), (10, 20, 30),
                                          (0.0, 0.1, 0.2, 0.25,
                                           0.3, 0.35, 0.4, 0.5)):
        segs = vad_segments_gen(audio, agg=agg, frame_ms=fms, pad=pad)
        r, p, f, _ = vad_quality_frames(segs, turns, len(audio))
        phaseA.append({"agg": agg, "frame_ms": fms, "pad": pad,
                       "n_seg": len(segs), "recall": round(r, 4),
                       "precision": round(p, 4), "f1": round(f, 4)})
    phaseA.sort(key=lambda d: -d["f1"])
    res["phaseA"] = phaseA
    print("  top-8 Phase A by F1:", flush=True)
    for d in phaseA[:8]:
        print(f"    agg={d['agg']} fms={d['frame_ms']} pad={d['pad']}: "
              f"rec={d['recall']} prec={d['precision']} f1={d['f1']} "
              f"n={d['n_seg']}", flush=True)
    baseA = next(d for d in phaseA
                 if (d["agg"], d["frame_ms"], d["pad"]) == (0, 10, 0.2))
    print(f"  baseline rank: "
          f"{phaseA.index(baseA)+1}/48 (f1={baseA['f1']})", flush=True)

    # --- Phase B: hangover/merge tuning on the Phase-A winner
    wA = phaseA[0]
    print(f"Phase B: hangover/merge tuning on agg={wA['agg']} "
          f"fms={wA['frame_ms']} ...", flush=True)
    phaseB = []
    for t_on, t_off, mg in itertools.product(
            (1, 2, 3), (3, 5, 10, 20), (0.15, 0.25, 0.4)):
        segs = vad_segments_gen(audio, agg=wA["agg"], frame_ms=wA["frame_ms"],
                                t_on=t_on, t_off=t_off, merge_gap=mg,
                                use_pad=False)
        r, p, f, _ = vad_quality_frames(segs, turns, len(audio))
        phaseB.append({"agg": wA["agg"], "frame_ms": wA["frame_ms"],
                       "t_on": t_on, "t_off": t_off, "merge_gap": mg,
                       "n_seg": len(segs), "recall": round(r, 4),
                       "precision": round(p, 4), "f1": round(f, 4)})
    phaseB.sort(key=lambda d: -d["f1"])
    res["phaseB"] = phaseB
    print("  top-8 Phase B by F1:", flush=True)
    for d in phaseB[:8]:
        print(f"    t_on={d['t_on']} t_off={d['t_off']} mg={d['merge_gap']}: "
              f"rec={d['recall']} prec={d['precision']} f1={d['f1']} "
              f"n={d['n_seg']}", flush=True)

    # --- Phase C: full pipeline on top-K VAD configs + baseline control
    cand_cfgs = []
    seen = set()
    for src, lst, topk in (("A", phaseA, 6), ("B", phaseB, 4)):
        for d in lst[:topk]:
            if src == "A":
                cfg = {"agg": d["agg"], "frame_ms": d["frame_ms"],
                       "pad": d["pad"], "use_pad": True}
            else:
                cfg = {"agg": d["agg"], "frame_ms": d["frame_ms"],
                       "t_on": d["t_on"], "t_off": d["t_off"],
                       "merge_gap": d["merge_gap"], "use_pad": False}
            key = json.dumps(cfg, sort_keys=True)
            if key not in seen:
                seen.add(key)
                cand_cfgs.append((src, cfg))
    cand_cfgs.append(("baseline",
                      {"agg": 0, "frame_ms": 10, "pad": 0.2,
                       "use_pad": True}))
    print(f"Phase C: full pipeline on {len(cand_cfgs)} configs ...",
          flush=True)
    phaseC = []
    for src, cfg in cand_cfgs:
        kw = dict(cfg)
        kw.pop("use_pad", None)
        segs = vad_segments_gen(audio, use_pad=cfg.get("use_pad", True),
                                **kw)
        pr = run_pipeline(audio, turns, fixture_emb, segs,
                          sil_frac=w63.SILENCE_FRAC, inclusion="strict")
        entry = {"src": src, "cfg": cfg,
                 "vad_recall": None, "vad_precision": None,
                 "n_vad_seg": len(segs)}
        r, p, _, _ = vad_quality_frames(segs, turns, len(audio))
        entry["vad_recall"], entry["vad_precision"] = round(r, 4), round(p, 4)
        entry.update({k: v for k, v in pr.items() if k != "failed"})
        entry["failed"] = pr.get("failed")
        phaseC.append(entry)
        f1r = pr.get("F1", {})
        print(f"    [{src}] {cfg}: kept={pr.get('kept')} k={pr.get('k')} "
              f"margin={pr.get('margin')} F1: DER={f1r.get('DER')} "
              f"miss={f1r.get('miss')} FA={f1r.get('FA')} "
              f"conf={f1r.get('conf')} | c025 DER={f1r.get('DER_c025')}",
              flush=True)
    okC = [e for e in phaseC if not e["failed"]]
    okC.sort(key=lambda e: e["F1"]["DER"])
    res["phaseC"] = phaseC
    winner_min_der = okC[0]
    # Recommended production operating point: min DER with FA <= 0.5 s
    # (the knee — beyond it FA explodes for marginal DER gains).
    feas = [e for e in okC if e["F1"]["FA"] <= 0.5]
    recommended = min(feas, key=lambda e: e["F1"]["DER"])
    print(f"  Phase-C min-DER: [{winner_min_der['src']}] "
          f"{winner_min_der['cfg']} F1 DER={winner_min_der['F1']['DER']} "
          f"(miss={winner_min_der['F1']['miss']} "
          f"FA={winner_min_der['F1']['FA']})", flush=True)
    print(f"  Phase-C recommended (FA<=0.5): [{recommended['src']}] "
          f"{recommended['cfg']} F1 DER={recommended['F1']['DER']} "
          f"(miss={recommended['F1']['miss']} "
          f"FA={recommended['F1']['FA']})", flush=True)

    baseC = next(e for e in phaseC if e["src"] == "baseline")
    check("baseline_pipeline_reproduces_wave63",
          abs(baseC["F1"]["DER"] - 0.0712) < 0.002 and
          abs(baseC["F0"]["DER"] - 0.1158) < 0.002,
          f"baseline F1 DER={baseC['F1']['DER']} (wave63 0.0712), "
          f"F0 DER={baseC['F0']['DER']} (wave63 0.1158)")
    check("mindER_k3", winner_min_der["k"] == 3,
          f"min-DER eigengap k={winner_min_der['k']} "
          f"margin={winner_min_der['margin']}x")
    check("mindER_purity", winner_min_der.get("purity") == 1.0,
          f"min-DER frame purity={winner_min_der.get('purity')}")
    check("mindER_beats_wave63",
          winner_min_der["F1"]["DER"] < baseC["F1"]["DER"] - 1e-9,
          f"min-DER F1 DER={winner_min_der['F1']['DER']} vs wave63 "
          f"{baseC['F1']['DER']}")
    check("recommended_beats_wave63",
          recommended["F1"]["DER"] < baseC["F1"]["DER"] - 1e-9,
          f"recommended F1 DER={recommended['F1']['DER']} vs wave63 "
          f"{baseC['F1']['DER']} (FA={recommended['F1']['FA']}<=0.5)")
    check("recommended_k3_pure",
          recommended["k"] == 3 and recommended.get("purity") == 1.0,
          f"recommended k={recommended['k']} "
          f"purity={recommended.get('purity')}")

    # --- Phase D: energy-gate x inclusion sensitivity on the recommended
    wcfg = dict(recommended["cfg"])
    kw = dict(wcfg)
    kw.pop("use_pad", None)
    wsegs = vad_segments_gen(audio, use_pad=wcfg.get("use_pad", True), **kw)
    print("Phase D: energy-gate x inclusion sensitivity ...", flush=True)
    phaseD = []
    for sil, inc in itertools.product((0.08, 0.10, 0.12, 0.16),
                                      ("strict", "center", "overlap50")):
        pr = run_pipeline(audio, turns, fixture_emb, wsegs, sil_frac=sil,
                          inclusion=inc)
        entry = {"sil_frac": sil, "inclusion": inc,
                 "failed": pr.get("failed")}
        entry.update({k: v for k, v in pr.items() if k != "failed"})
        phaseD.append(entry)
        f1r = pr.get("F1", {})
        print(f"    gate={sil} incl={inc}: kept={pr.get('kept')} "
              f"k={pr.get('k')} F1 DER={f1r.get('DER')} "
              f"miss={f1r.get('miss')} FA={f1r.get('FA')}", flush=True)
    okD = [e for e in phaseD if not e["failed"]]
    okD.sort(key=lambda e: e["F1"]["DER"])
    res["phaseD"] = phaseD
    bestD = okD[0]
    print(f"  Phase-D best: gate={bestD['sil_frac']} "
          f"incl={bestD['inclusion']} F1 DER={bestD['F1']['DER']} "
          f"(miss={bestD['F1']['miss']} FA={bestD['F1']['FA']})", flush=True)
    res["winner"] = {
        "min_der": {"src": winner_min_der["src"],
                    "cfg": winner_min_der["cfg"],
                    "F1": winner_min_der["F1"]},
        "recommended": {"src": recommended["src"], "cfg": recommended["cfg"],
                        "F1": recommended["F1"],
                        "rule": "min DER subject to FA <= 0.5 s"},
        "phaseD": {"sil_frac": bestD["sil_frac"],
                   "inclusion": bestD["inclusion"],
                   "F1": bestD["F1"]}}
    check("phaseD_best_at_least_recommended",
          bestD["F1"]["DER"] <= recommended["F1"]["DER"] + 1e-9,
          f"D-best DER={bestD['F1']['DER']} vs recommended "
          f"{recommended['F1']['DER']}")

    # --- write hypothesis RTTMs (F0 + F1) for min-DER and recommended
    def write_winner_rttms(tag_prefix, cfg, sil_frac, inclusion):
        kw = dict(cfg)
        kw.pop("use_pad", None)
        vsegs = vad_segments_gen(audio, use_pad=cfg.get("use_pad", True),
                                 **kw)
        pr = run_pipeline(audio, turns, fixture_emb, vsegs,
                          sil_frac=sil_frac, inclusion=inclusion)
        idxs, rmsv, _, _ = w63.window_grid(audio)
        thr = sil_frac * float(np.max(rmsv))
        all_speech = np.flatnonzero(rmsv >= thr)

        def keep(j):
            t0, t1 = j * HOP_S, j * HOP_S + WIN_S
            if inclusion == "strict":
                return w63.inside_vad(t0, t1, vsegs)
            tc = (t0 + t1) / 2
            if inclusion == "center":
                return any(a <= tc < b for a, b in vsegs)
            ov = sum(max(0.0, min(t1, b) - max(t0, a)) for a, b in vsegs)
            return ov >= 0.5 * WIN_S

        kept = [int(j) for j in all_speech if keep(j)]
        row = canon_row(audio)
        assert all(int(j) in row for j in kept)
        emb = fixture_emb[np.asarray([row[int(j)] for j in kept])]
        from spectralcluster import SpectralClusterer
        cl = SpectralClusterer(min_clusters=pr["k"], max_clusters=pr["k"],
                               custom_dist="cosine")
        labels = np.asarray(cl.predict(emb), dtype=int)
        n_frames = int(math.ceil((len(audio) / SR) / HOP_S))
        frames_f0 = w63.label_v2c_no_fill(kept, labels, vsegs, n_frames)
        frames_f1 = w63.fill_within_vad(frames_f0, vsegs, n_frames)
        cmap, _, _ = w63.hungarian_map(frames_f0, turns)
        spk_of = {c: cmap[c]
                  for c in set(frames_f0[frames_f0 != -1].tolist())}
        for tag, fvar in (("F0", frames_f0), ("F1", frames_f1)):
            segs_out = [(s, e, spk_of[c])
                        for s, e, c in w63.segments_from_frames(fvar)]
            w63.write_rttm(
                os.path.join(PROOFS,
                             f"hypothesis_{tag_prefix}_{tag}.rttm"),
                segs_out)

    write_winner_rttms("minder", winner_min_der["cfg"],
                       w63.SILENCE_FRAC, "strict")
    write_winner_rttms("recommended", recommended["cfg"],
                       bestD["sil_frac"], bestD["inclusion"])
    check("winner_rttms_written", True,
          "hypothesis_minder/recommended_F0/F1.rttm in proofs/vad_recall/")

    res["checks"] = checks
    res["elapsed_s"] = round(time.time() - t0, 1)
    n_pass = sum(c["pass"] for c in checks)
    res["checks_pass"] = f"{n_pass}/{len(checks)}"
    with open(os.path.join(PROOFS, "vad_recall_result.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n{n_pass}/{len(checks)} checks PASS, "
          f"{res['elapsed_s']}s. Result -> proofs/vad_recall/")
    if n_pass != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
