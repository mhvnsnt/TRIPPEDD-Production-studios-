#!/usr/bin/env python3
"""Wave 59 Lane C - VAD-boundary refinement of the real-voice diarization stage.

Baseline (Wave 58): 3 Kokoro voices (af_heart F / am_puck M / af_bella F),
ECAPA-TDNN 192-dim embeddings on 1.5 s / 0.25 s-hop windows, energy-gated
silence, SpectralCluster auto-k, pyannote-metrics scoring:
  DER 0.4084 / JER 0.5478 @collar 0.0 (miss 0.0 s, FA 3.7 s, confusion 12.35 s);
  DER 0.3556 @collar 0.25; forced k=3 -> DER 0.3359. Auto-k MERGED the two
  female voices (k=2 chosen); frame purity 0.6879.

This wave refines WINDOW/FRAME BOUNDARIES with a voice-activity detector
(Silero VAD, MIT license - verified live on PyPI + GitHub before wiring)
while changing nothing else:
  H_base - exact Wave-58 replication (energy gate, frame fill, auto k=3 range)
  H_vad  - identical pipeline, but:
             a) a window counts as speech only if >=50% of it overlaps a VAD
                speech interval (drops boundary-dominated windows);
             b) each 0.25 s frame is speech only if >=50% of it overlaps a VAD
                interval (VAD-hardened frame gate);
             c) hypothesis segment start/end snapped to the nearest VAD
                interval edge within +/-0.25 s.
  Diagnostics: both hypotheses also scored with forced k=3.

Hypothesis under test: most of the collar-0 gap vs collar-0.25 is boundary
slop (FA 3.7 s). VAD refinement should cut FA and confusion-at-boundaries;
it CANNOT fix the female-voice merge (a cluster-count failure, not a
boundary failure). A measured non-improvement is reported honestly.

Proof artifacts land in proofs/vad_boundary_refinement/:
  dialogue.wav, ground_truth.json (copied from Wave 58, SHA-256 verified),
  embeddings.pt, vad_timestamps.json, reference.rttm,
  hypothesis_base.rttm, hypothesis_vad.rttm (+ _k3 variants), result.json.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W58_PROOFS = os.path.join(HERE, os.pardir, "wave58_lane_c", "proofs",
                          "real_voice_diarization")
PROOFS = os.path.join(HERE, "proofs", "vad_boundary_refinement")
SAVEDIR = os.path.join(HERE, "scratch", "speechbrain_models")
SR_TTS = 24000
SR = 16000
WIN_S = 1.5
HOP_S = 0.25
GAP_S = 0.4
SILENCE_FRAC = 0.08
SNAP_TOL = 0.25        # boundary snap tolerance to nearest VAD edge
VAD_OVERLAP = 0.50     # window/frame speech = >=50% overlap with VAD speech
VAD_THRESHOLD = 0.5    # silero speech-probability threshold

TURNS = [
    ("A", "af_heart", "Alright, we're rolling. The street is quiet tonight, just the way we planned it."),
    ("B", "am_puck",  "Quiet is good. Last time the corner was crawling with onlookers before we even started."),
    ("C", "af_bella", "I brought the chalk. We can mark the lines before the crowd shows up."),
    ("A", "af_heart", "Mark them wide. Nobody should be guessing where the boundary is."),
    ("B", "am_puck",  "And the water table? Somebody has to keep the bottles on ice."),
    ("C", "af_bella", "I already filled the cooler. Ice, towels, and a spare roll of tape."),
    ("A", "af_heart", "Good. Now we just wait for the lights to come on over the alley."),
    ("B", "am_puck",  "When they do, we walk in steady. No rush, no noise."),
    ("C", "af_bella", "Steady wins. The ones who rush always trip on the first line."),
]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def resample(x, sr_in, sr_out):
    if sr_in == sr_out:
        return x
    n_out = int(round(len(x) * sr_out / sr_in))
    t_in = np.linspace(0, 1, len(x), endpoint=False)
    t_out = np.linspace(0, 1, n_out, endpoint=False)
    return np.interp(t_out, t_in, x).astype(np.float32)


def synthesize_dialogue():
    import torch
    from kokoro import KPipeline
    os.makedirs(PROOFS, exist_ok=True)
    pipeline = KPipeline(lang_code="a")
    turns_gt, audios = [], []
    t_cur = 0.0
    for idx, (spk, voice, text) in enumerate(TURNS):
        torch.manual_seed(1000 + idx)
        chunks = []
        for _gs, _ps, audio in pipeline(text, voice=voice):
            chunks.append(audio.numpy().astype(np.float32).ravel())
        line16 = resample(np.concatenate(chunks), SR_TTS, SR)
        dur = len(line16) / SR
        turns_gt.append({"index": idx, "speaker": spk, "voice": voice,
                         "text": text,
                         "start": round(t_cur, 4), "end": round(t_cur + dur, 4)})
        audios.append(line16)
        audios.append(np.zeros(int(GAP_S * SR), dtype=np.float32))
        t_cur += dur + GAP_S
    audio = np.concatenate(audios)
    return audio / max(1e-9, float(np.max(np.abs(audio)))) * 0.95, turns_gt


def embed_windows(audio, encoder, vad_gate=None):
    """Slide windows, gate silence (energy, Wave-58 rule), optionally require
    VAD speech overlap >= VAD_OVERLAP. Embed ONLY speech windows."""
    import torch
    win, hop = int(WIN_S * SR), int(HOP_S * SR)
    idxs = list(range(0, len(audio) - win + 1, hop))
    rms = np.array([float(np.sqrt(np.mean(audio[i:i + win] ** 2))) for i in idxs])
    thr = SILENCE_FRAC * float(np.max(rms))
    speech = np.array([bool(r >= thr) for r in rms])
    if vad_gate is not None:
        speech = speech & np.array([
            vad_gate((i / SR), (i + win) / SR) >= VAD_OVERLAP * WIN_S
            for i in idxs])
    spk_idx = [j for j, s in enumerate(speech) if s]
    batch = np.stack([audio[idxs[j]:idxs[j] + win] for j in spk_idx])
    embs = []
    with torch.no_grad():
        for b0 in range(0, len(batch), 32):
            wavs = torch.from_numpy(batch[b0:b0 + 32]).float()
            lens = torch.ones(len(wavs))
            e = encoder.encode_batch(wavs, lens).squeeze(1)
            embs.append(e.detach().cpu().numpy())
    return spk_idx, speech, np.concatenate(embs, axis=0), rms, thr, len(idxs)


def run_vad(audio, threshold=VAD_THRESHOLD, min_silence_ms=100,
            pad_ms=30, min_speech_ms=250):
    """Silero VAD -> [(start_s, end_s)] speech intervals + determinism probe."""
    import torch
    from silero_vad import load_silero_vad, get_speech_timestamps
    model = load_silero_vad()  # bundled torch JIT, MIT; no download needed
    wav = torch.from_numpy(audio.astype(np.float32)).unsqueeze(0)
    def stamps():
        return get_speech_timestamps(
            wav, model, threshold=threshold, sampling_rate=SR,
            min_silence_duration_ms=min_silence_ms, speech_pad_ms=pad_ms,
            min_speech_duration_ms=min_speech_ms, return_seconds=True)
    iv1, iv2 = stamps(), stamps()
    assert [(a["start"], a["end"]) for a in iv1] == \
           [(a["start"], a["end"]) for a in iv2], "VAD not deterministic!"
    return [(float(a["start"]), float(a["end"])) for a in iv1]


def make_vad_overlap_fn(intervals, dur_s):
    """Overlap (seconds) of [s, e) with the union of VAD speech intervals."""
    starts = np.array([a for a, _ in intervals])
    ends = np.array([b for _, b in intervals])
    def overlap(s, e):
        if e <= 0 or s >= dur_s:
            return 0.0
        return float(np.sum(np.maximum(0.0, np.minimum(ends, e) - np.maximum(starts, s))))
    return overlap


def cluster_labels(emb, k):
    from spectralcluster import SpectralClusterer
    if k is None:
        cl = SpectralClusterer(min_clusters=2, max_clusters=4, custom_dist="cosine")
    else:
        cl = SpectralClusterer(min_clusters=k, max_clusters=k, custom_dist="cosine")
    return np.asarray(cl.predict(emb), dtype=int)


def frames_from_windows(labels, spk_idx, n_frames, vad_gate=None):
    """Base (Wave-58) frame labeling; VAD variant additionally requires the
    frame itself to overlap VAD speech."""
    frames = np.full(n_frames, -1, dtype=int)
    center_off = int(round((WIN_S / 2) / HOP_S))
    win_label = {j: int(l) for j, l in zip(spk_idx, labels)}
    for i in range(n_frames):
        j = i - center_off
        if j not in win_label:
            continue
        if vad_gate is not None and \
           vad_gate(i * HOP_S, (i + 1) * HOP_S) < VAD_OVERLAP * HOP_S:
            continue
        frames[i] = win_label[j]
    # nearest-labeled-neighbor fill within one window radius (Wave-58 rule)
    for i in range(n_frames):
        if frames[i] != -1:
            continue
        if vad_gate is not None and \
           vad_gate(i * HOP_S, (i + 1) * HOP_S) < VAD_OVERLAP * HOP_S:
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


def snap_segments(segs, intervals):
    """Snap each segment edge to the nearest VAD interval edge within SNAP_TOL."""
    starts = sorted(a for a, _ in intervals)
    ends = sorted(b for _, b in intervals)
    def nearest(x, xs):
        return min(xs, key=lambda v: abs(v - x)) if xs else x
    out = []
    for s, e, c in segs:
        ns = nearest(s, starts)
        if abs(ns - s) > SNAP_TOL:
            ns = s
        ne = nearest(e, ends)
        if abs(ne - e) > SNAP_TOL:
            ne = e
        if ne <= ns:  # guard: never invert a segment
            ns, ne = s, e
        out.append((ns, ne, c))
    # merge same-label touch/overlap runs (never across the 0.4 s GT gaps)
    out.sort(key=lambda t: (t[0], t[1]))
    merged = []
    for s, e, c in out:
        if merged and merged[-1][2] == c and s <= merged[-1][1] + 1e-9:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e), c)
        else:
            merged.append((s, e, c))
    return merged


def frames_to_segments(frames, turns_gt, intervals=None):
    """Contiguous same-label runs -> segments; Hungarian cluster->speaker map;
    per-speaker frame purity; optional VAD edge snapping."""
    from scipy.optimize import linear_sum_assignment
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
    if intervals is not None:
        segs = snap_segments(segs, intervals)
    clus = sorted(set(c for _, _, c in segs))
    spks = sorted(set(t["speaker"] for t in turns_gt))
    cont = np.zeros((len(clus), len(spks)))
    ci = {c: k for k, c in enumerate(clus)}
    si = {s: k for k, s in enumerate(spks)}
    labeled = frames != -1
    agree = total = 0
    for i, f in enumerate(frames):
        if f == -1:
            continue
        t = (i + 0.5) * HOP_S
        spk = next((g["speaker"] for g in turns_gt if g["start"] <= t < g["end"]), None)
        if spk is None:
            continue
        total += 1
        cont[ci[f], si[spk]] += 1
    ri, cj = linear_sum_assignment(-cont)
    cmap = {int(clus[r]): spks[c] for r, c in zip(ri, cj)}
    for i, f in enumerate(frames):
        if f == -1:
            continue
        t = (i + 0.5) * HOP_S
        spk = next((g["speaker"] for g in turns_gt if g["start"] <= t < g["end"]), None)
        if spk is not None and cmap[f] == spk:
            agree += 1
    mapped = [(s, e, cmap[c]) for s, e, c in segs]
    return mapped, cmap, agree / max(1, total), total


def write_rttm(path, segments, uri="dialogue"):
    with open(path, "w") as f:
        for s, e, spk in segments:
            f.write(f"SPEAKER {uri} 1 {s:.3f} {e - s:.3f} <NA> <NA> {spk} <NA> <NA>\n")


def score(ref_path, hyp_path, collar):
    from pyannote.core import Annotation, Segment
    from pyannote.metrics.diarization import DiarizationErrorRate, JaccardErrorRate
    def load(p):
        ann = Annotation()
        with open(p) as f:
            for line in f:
                parts = line.split()
                on, dur, spk = float(parts[3]), float(parts[4]), parts[7]
                ann[Segment(on, on + dur)] = spk
        return ann
    ref, hyp = load(ref_path), load(hyp_path)
    der, jer = DiarizationErrorRate(collar=collar), JaccardErrorRate(collar=collar)
    det = der.compute_components(ref, hyp)
    return der(ref, hyp), jer(ref, hyp), det


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--vad-threshold", type=float, default=VAD_THRESHOLD)
    ap.add_argument("--vad-min-silence-ms", type=int, default=100)
    ap.add_argument("--vad-pad-ms", type=int, default=30)
    ap.add_argument("--vad-min-speech-ms", type=int, default=250)
    ap.add_argument("--tag", default="", help="output suffix for VAD-param sweeps")
    return ap.parse_args()


def main():
    args = parse_args()
    t0 = time.time()
    os.makedirs(PROOFS, exist_ok=True)
    checks = []
    results = {"checks": checks}
    resume = args.resume
    suf = f"_{args.tag}" if args.tag else ""
    wav_path = os.path.join(PROOFS, "dialogue.wav")
    gt_path = os.path.join(PROOFS, "ground_truth.json")

    # --- 1. fixture: resume artifacts after SHA-256 check ---
    if resume and os.path.exists(wav_path) and os.path.exists(gt_path):
        with open(gt_path) as f:
            g = json.load(f)
        turns_gt = g["turns"]
        assert g["wav_sha256"] == sha256_file(wav_path), "wav changed since GT!"
        with wave.open(wav_path, "rb") as w:
            assert w.getframerate() == SR and w.getnchannels() == 1
            audio = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
                     .astype(np.float32) / 32767.0)
        print("[resume] dialogue.wav SHA-256 matches ground_truth.json record", flush=True)
    else:
        audio, turns_gt = synthesize_dialogue()
        with wave.open(wav_path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((audio * 32767).astype(np.int16).tobytes())
    dur_s = len(audio) / SR
    n_frames = int(math.ceil(dur_s / HOP_S))
    checks.append({"name": "dialogue.wav resumed with SHA-256 match",
                   "pass": resume and os.path.exists(wav_path),
                   "measured": f"sha={sha256_file(wav_path)[:16]}... audio={dur_s:.2f}s"})
    checks.append({"name": "ground truth spans full audio (no orphan tail)",
                   "pass": abs((turns_gt[-1]["end"] + GAP_S) - dur_s) < 0.01,
                   "measured": f"audio={dur_s:.2f}s last_turn_end={turns_gt[-1]['end']:.2f}s"})

    # --- 2. VAD (Silero, MIT) ---
    t_vad = time.time()
    intervals = run_vad(audio, threshold=args.vad_threshold,
                        min_silence_ms=args.vad_min_silence_ms,
                        pad_ms=args.vad_pad_ms,
                        min_speech_ms=args.vad_min_speech_ms)
    vad_s = time.time() - t_vad
    vad_path = os.path.join(PROOFS, f"vad_timestamps{suf}.json")
    with open(vad_path, "w") as f:
        json.dump({"intervals_s": intervals, "n_intervals": len(intervals),
                   "threshold": args.vad_threshold,
                   "min_silence_duration_ms": args.vad_min_silence_ms,
                   "speech_pad_ms": args.vad_pad_ms,
                   "min_speech_duration_ms": args.vad_min_speech_ms}, f, indent=2)
    gt_speech = sum(t["end"] - t["start"] for t in turns_gt)
    vad_speech = sum(e - s for s, e in intervals)
    overlap_fn = make_vad_overlap_fn(intervals, dur_s)
    gt_cover = sum(overlap_fn(t["start"], t["end"]) for t in turns_gt) / gt_speech
    checks.append({"name": "VAD deterministic (two runs identical)",
                   "pass": True, "measured": f"{len(intervals)} intervals, {vad_s:.1f}s CPU"})
    checks.append({"name": "VAD covers GT speech (coverage >= 0.95)",
                   "pass": gt_cover >= 0.95,
                   "measured": f"coverage={gt_cover:.4f} vad_speech={vad_speech:.2f}s gt_speech={gt_speech:.2f}s"})

    # --- 3. embeddings ---
    import torch
    from speechbrain.inference import EncoderClassifier
    t1 = time.time()
    encoder = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", savedir=SAVEDIR)
    enc_load_s = time.time() - t1
    t2 = time.time()
    # base: Wave-58 energy gate only (replication)
    spk_idx_b, speech_b, emb_b, rms, thr, n_windows = embed_windows(audio, encoder)
    # VAD: energy gate + VAD overlap gate
    spk_idx_v, speech_v, emb_v, _, _, _ = embed_windows(
        audio, encoder, vad_gate=overlap_fn)
    embed_s = time.time() - t2
    torch.save(torch.from_numpy(emb_b), os.path.join(PROOFS, "embeddings_base.pt"))
    torch.save(torch.from_numpy(emb_v), os.path.join(PROOFS, f"embeddings_vad{suf}.pt"))
    checks.append({"name": "embedding shapes sane ((N,192))",
                   "pass": emb_b.shape[1] == 192 and emb_v.shape[1] == 192,
                   "measured": f"base={emb_b.shape} vad={emb_v.shape} windows={n_windows}"})
    checks.append({"name": "embeddings finite",
                   "pass": bool(np.all(np.isfinite(emb_b)) and np.all(np.isfinite(emb_v))),
                   "measured": "no NaN/Inf"})

    # --- 4. cluster + frames + segments ---
    t3 = time.time()
    out = {}
    for tag, spk_idx, emb, use_vad in [
            ("base", spk_idx_b, emb_b, False),
            ("vad", spk_idx_v, emb_v, True)]:
        for k, kname in [(None, "auto"), (3, "k3")]:
            labels = cluster_labels(emb, k)
            labels2 = cluster_labels(emb, k)  # determinism probe
            det_ok = bool(np.array_equal(labels, labels2))
            frames = frames_from_windows(labels, spk_idx, n_frames,
                                         vad_gate=overlap_fn if use_vad else None)
            mapped, cmap, purity, total_f = frames_to_segments(
                frames, turns_gt, intervals=intervals if use_vad else None)
            vadsuf = suf if use_vad else ""
            hyp = os.path.join(
                PROOFS, f"hypothesis_{tag}{vadsuf}{'' if k is None else '_k3'}.rttm")
            write_rttm(hyp, mapped)
            out[f"{tag}_{kname}"] = {"labels": labels, "det_ok": det_ok,
                                    "cmap": cmap, "purity": purity,
                                    "total_frames": total_f,
                                    "n_clusters": len(set(labels.tolist()))}
    cluster_s = time.time() - t3
    n_clus_base = out["base_auto"]["n_clusters"]
    checks.append({"name": "cluster count within [2,4] (base auto)",
                   "pass": 2 <= n_clus_base <= 4, "measured": f"{n_clus_base} clusters"})
    checks.append({"name": "clustering deterministic across runs (all 4 configs)",
                   "pass": all(v["det_ok"] for v in out.values()),
                   "measured": "all re-runs identical"})
    checks.append({"name": "Hungarian cluster->speaker map exists (base auto)",
                   "pass": len(out["base_auto"]["cmap"]) == n_clus_base,
                   "measured": f"map={out['base_auto']['cmap']}"})

    # --- 5. score ---
    ref_path = os.path.join(PROOFS, "reference.rttm")
    write_rttm(ref_path, [(t["start"], t["end"], t["speaker"]) for t in turns_gt])
    scores = {}
    for tag, kname in [("base", "auto"), ("vad", "auto"),
                       ("base", "k3"), ("vad", "k3")]:
        vadsuf = suf if tag == "vad" else ""
        hyp = os.path.join(
            PROOFS, f"hypothesis_{tag}{vadsuf}{'' if kname == 'auto' else '_k3'}.rttm")
        d0, j0, det0 = score(ref_path, hyp, collar=0.0)
        d25, j25, _ = score(ref_path, hyp, collar=0.25)
        scores[f"{tag}_{kname}"] = {
            "DER0": round(d0, 4), "JER0": round(j0, 4),
            "DER25": round(d25, 4), "JER25": round(j25, 4),
            "comp0": {k2: round(float(det0[k2]), 4) for k2 in
                      ["missed detection", "false alarm", "confusion", "total"]}}
    checks.append({"name": "baseline replication: DER0 within 1e-3 of Wave-58 (0.4084)",
                   "pass": abs(scores["base_auto"]["DER0"] - 0.4084) < 1e-3,
                   "measured": f"DER0={scores['base_auto']['DER0']}"})
    checks.append({"name": "VAD DER0 <= base DER0 (boundary refinement helps or not)",
                   "pass": scores["vad_auto"]["DER0"] <= scores["base_auto"]["DER0"],
                   "measured": f"base={scores['base_auto']['DER0']} vad={scores['vad_auto']['DER0']}"})

    results.update({
        "voices": sorted(set(v for _, v, _ in TURNS)),
        "speakers": sorted(set(s for s, _, _ in TURNS)),
        "dialogue_s": round(dur_s, 2),
        "vad": {"n_intervals": len(intervals), "speech_s": round(vad_speech, 2),
                "gt_coverage": round(gt_cover, 4), "threshold": args.vad_threshold,
                "min_silence_duration_ms": args.vad_min_silence_ms,
                "speech_pad_ms": args.vad_pad_ms,
                "min_speech_duration_ms": args.vad_min_speech_ms,
                "snap_tol_s": SNAP_TOL, "overlap_gate": VAD_OVERLAP},
        "windows": n_windows,
        "speech_windows": {k: int(np.sum(v)) for k, v in
                           [("base", speech_b), ("vad", speech_v)]},
        "configs": {k: {"clusters": v["n_clusters"], "cluster_map": v["cmap"],
                        "frame_purity": round(v["purity"], 4),
                        "speech_frames": v["total_frames"], **scores[k]}
                    for k, v in out.items()},
        "timings_s": {"ecapa_load": round(enc_load_s, 1),
                      "vad": round(vad_s, 1),
                      "embed": round(embed_s, 1), "cluster": round(cluster_s, 3),
                      "total": round(time.time() - t0, 1)},
    })
    n_pass = sum(1 for c in checks if c["pass"])
    results["pass_rate"] = f"{n_pass}/{len(checks)}"
    with open(os.path.join(PROOFS, f"result{suf}.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps({k: v for k, v in results.items() if k != "checks"}, indent=2))
    print(f"PASS {n_pass}/{len(checks)}")


if __name__ == "__main__":
    main()
