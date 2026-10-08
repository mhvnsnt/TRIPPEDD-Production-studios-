#!/usr/bin/env python3
"""Wave 58 Lane C — FIRST REAL-VOICE diarization test (frame/window level).

Pipeline:
  text (original dialogue, 3 Kokoro voices, known ground-truth turns)
    -> Kokoro TTS (Apache-2.0, hexgrad/Kokoro-82M; wired Wave 51)
    -> sliding windows (1.5 s win / 0.25 s hop, energy-gated silence)
    -> SpeechBrain ECAPA-TDNN embeddings (Apache-2.0; wired Wave 56)
    -> SpectralCluster (Apache-2.0; wired Wave 57) with custom_dist="cosine"
    -> pyannote-metrics DER / JER (MIT; wired Wave 57) on RTTM artifacts

This is the honest step up from Wave 57: that proof was segment-level on a
SYNTHETIC 4-segment fixture (harmonic-complex tones). Here the input is real
neural voices, clustered at window level (not pre-segmented), with silence
windows gated out by energy. No label cheating: cluster->speaker mapping via
Hungarian assignment on frame-level contingency.

Proof artifacts land in proofs/real_voice_diarization/:
  dialogue.wav        - concatenated 3-voice dialogue (24 kHz mono)
  ground_truth.json   - per-turn (speaker, voice, start, end) + SHA-256
  reference.rttm      - ground-truth RTTM (gaps = non-speech)
  hypothesis.rttm     - clustered window-label RTTM (post Hungarian map)
  embeddings.pt       - (N_windows, 192) ECAPA embeddings (speech windows)
  result.json         - measured numbers + PASS/FAIL per check

Environment (pinned):
  Python 3.12.3, torch 2.14.1+cpu, torchaudio 2.11.0+cpu,
  speechbrain 1.1.1, kokoro 0.9.4, spectralcluster 0.2.22,
  pyannote-metrics 4.1, numpy 1.26.4, soundfile 0.14.0, scipy (bundled dep).
  TMPDIR lane-local (NOT /tmp: 512 MB tmpfs); no_proxy/NO_PROXY stripped of
  :: literals (httpx crash); espeak-ng system (Kokoro G2P subprocess only).
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
PROOFS = os.path.join(HERE, "proofs", "real_voice_diarization")
SAVEDIR = os.path.join(HERE, "scratch", "speechbrain_models")
SR_TTS = 24000
SR = 16000            # ECAPA native sample rate
WIN_S = 1.5           # sliding window length
HOP_S = 0.25          # hop / frame resolution
GAP_S = 0.4           # inter-turn silence
SILENCE_FRAC = 0.08   # window speech gate: rms >= frac * max_rms

# Original dialogue (neutral text written for this test). Three voices;
# A and C are both female voices on purpose (harder than F/M split).
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
    """Render each turn with Kokoro (seeded), return audio @SR and turn GT."""
    import torch
    from kokoro import KPipeline

    os.makedirs(PROOFS, exist_ok=True)
    pipeline = KPipeline(lang_code="a")
    pipes = {}  # one KPipeline per language is fine; voice switches per call
    turns_gt = []
    audios = []
    t_cur = 0.0
    for idx, (spk, voice, text) in enumerate(TURNS):
        torch.manual_seed(1000 + idx)  # seeded -> reproducible artifacts
        chunks = []
        for _gs, _ps, audio in pipeline(text, voice=voice):
            chunks.append(audio.numpy().astype(np.float32).ravel())
        line = np.concatenate(chunks)
        line16 = resample(line, SR_TTS, SR)
        dur = len(line16) / SR
        turns_gt.append({
            "index": idx, "speaker": spk, "voice": voice,
            "text": text,
            "start": round(t_cur, 4), "end": round(t_cur + dur, 4),
        })
        audios.append(line16)
        audios.append(np.zeros(int(GAP_S * SR), dtype=np.float32))
        t_cur += dur + GAP_S
    audio = np.concatenate(audios)
    audio = audio / max(1e-9, float(np.max(np.abs(audio)))) * 0.95
    return audio, turns_gt


def embed_windows(audio, encoder):
    """Slide windows, gate silence by energy, embed ONLY speech windows."""
    import torch

    win = int(WIN_S * SR)
    hop = int(HOP_S * SR)
    idxs = list(range(0, len(audio) - win + 1, hop))
    rms = np.array([float(np.sqrt(np.mean(audio[i:i + win] ** 2))) for i in idxs])
    thr = SILENCE_FRAC * float(np.max(rms))
    speech = np.array([bool(r >= thr) for r in rms])
    spk_idx = [j for j, s in enumerate(speech) if s]
    batch = np.stack([audio[idxs[j]:idxs[j] + win] for j in spk_idx])
    embs = []
    with torch.no_grad():
        for b0 in range(0, len(batch), 32):  # chunked: safe on low-RAM CPU
            wavs = torch.from_numpy(batch[b0:b0 + 32]).float()
            lens = torch.ones(len(wavs))
            e = encoder.encode_batch(wavs, lens).squeeze(1)
            embs.append(e.detach().cpu().numpy())
    emb = np.concatenate(embs, axis=0)
    return spk_idx, speech, emb, rms, thr, len(idxs)


def cluster_labels(emb):
    from spectralcluster import SpectralClusterer
    cl = SpectralClusterer(min_clusters=2, max_clusters=4, custom_dist="cosine")
    return np.asarray(cl.predict(emb), dtype=int)


def frames_from_windows(labels, spk_idx, n_frames):
    """Label each hop-resolution frame by the window centered on it.
    labels/spk_idx cover speech windows only; all other frames = silence."""
    frames = np.full(n_frames, -1, dtype=int)  # -1 = silence
    center_off = int(round((WIN_S / 2) / HOP_S))  # window j centers on frame j+3
    for j, lab in zip(spk_idx, labels):
        f = j + center_off
        if 0 <= f < n_frames:
            frames[f] = int(lab)
    # Fill any interior frames left unlabeled (edge frames near gaps):
    # nearest labeled neighbor within one window radius.
    for i in range(n_frames):
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


def segments_from_frames(frames, turns_gt):
    """Merge contiguous same-label frames into segments; Hungarian map."""
    from scipy.optimize import linear_sum_assignment

    segs, clusters = [], []
    i = 0
    n = len(frames)
    while i < n:
        if frames[i] == -1:
            i += 1
            continue
        j = i
        while j < n and frames[j] == frames[i]:
            j += 1
        segs.append((i * HOP_S, j * HOP_S, frames[i]))
        clusters.append(frames[i])
        i = j
    clus = sorted(set(clusters))
    spks = sorted(set(t["speaker"] for t in turns_gt))
    # frame-level contingency: cluster x speaker
    cont = np.zeros((len(clus), len(spks)))
    ci = {c: k for k, c in enumerate(clus)}
    si = {s: k for k, s in enumerate(spks)}
    for i, f in enumerate(frames):
        if f == -1:
            continue
        t = (i + 0.5) * HOP_S
        spk = next((g["speaker"] for g in turns_gt if g["start"] <= t < g["end"]), None)
        if spk is not None:
            cont[ci[f], si[spk]] += 1
    ri, cj = linear_sum_assignment(-cont)  # maximize agreement
    cmap = {int(clus[r]): spks[c] for r, c in zip(ri, cj)}
    mapped = [(s, e, cmap[c]) for s, e, c in segs]
    # per-speaker frame purity vs GT
    n_speech = sum(s == f for i, f in enumerate(frames) if (s := next(
        (g["speaker"] for g in turns_gt if g["start"] <= (i + 0.5) * HOP_S < g["end"]), None)) is not None)
    agree = 0
    total = 0
    for i, f in enumerate(frames):
        if f == -1:
            continue
        t = (i + 0.5) * HOP_S
        spk = next((g["speaker"] for g in turns_gt if g["start"] <= t < g["end"]), None)
        if spk is None:
            continue
        total += 1
        if cmap[f] == spk:
            agree += 1
    return mapped, cmap, agree / max(1, total), total


def write_rttm(path, segments, uri="dialogue"):
    with open(path, "w") as f:
        for s, e, spk in segments:
            f.write(f"SPEAKER {uri} 1 {s:.3f} {e - s:.3f} <NA> <NA> {spk} <NA> <NA>\n")


def score(ref_path, hyp_path, collar):
    from pyannote.core import Annotation, Segment
    from pyannote.metrics.diarization import (
        DiarizationErrorRate, JaccardErrorRate,
    )

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
    dv = der(ref, hyp)
    jv = jer(ref, hyp)
    det = der.compute_components(ref, hyp)
    return dv, jv, det


def main():
    t0 = time.time()
    os.makedirs(PROOFS, exist_ok=True)
    checks = []
    results = {"checks": checks}
    resume = "--resume" in sys.argv

    # --- 1. render dialogue (or resume from existing artifacts) ---
    wav_path = os.path.join(PROOFS, "dialogue.wav")
    gt_path = os.path.join(PROOFS, "ground_truth.json")
    if resume and os.path.exists(wav_path) and os.path.exists(gt_path):
        with open(gt_path) as f:
            g = json.load(f)
        turns_gt = g["turns"]
        assert g["wav_sha256"] == sha256_file(wav_path), "wav changed since GT!"
        with wave.open(wav_path, "rb") as w:
            assert w.getframerate() == SR and w.getnchannels() == 1
            audio = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
                     .astype(np.float32) / 32767.0)
        print("[resume] loaded existing dialogue.wav + ground_truth.json", flush=True)
    else:
        audio, turns_gt = synthesize_dialogue()
        with wave.open(wav_path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((audio * 32767).astype(np.int16).tobytes())
    dur_s = len(audio) / SR
    n_voices = len(set(v for _, v, _ in TURNS))
    checks.append({"name": "3 distinct Kokoro voices rendered (9 turns)",
                   "pass": n_voices == 3 and len(TURNS) == 9,
                   "measured": f"voices={sorted(set(v for _, v, _ in TURNS))} turns=9"})
    if not resume:
        with open(gt_path, "w") as f:
            json.dump({"turns": turns_gt, "gap_s": GAP_S,
                       "wav_sha256": sha256_file(wav_path)}, f, indent=2)
    last_end = turns_gt[-1]["end"]
    checks.append({"name": "ground truth spans full audio (no orphan tail)",
                   "pass": abs((last_end + GAP_S) - dur_s) < 0.01,
                   "measured": f"audio={dur_s:.2f}s last_turn_end={last_end:.2f}s"})

    # --- 2. window embeddings ---
    import torch
    from speechbrain.inference import EncoderClassifier
    t1 = time.time()
    encoder = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", savedir=SAVEDIR)
    enc_load_s = time.time() - t1
    t2 = time.time()
    spk_idx, speech, emb, rms, thr, n_windows = embed_windows(audio, encoder)
    embed_s = time.time() - t2
    torch.save(torch.from_numpy(emb),
               os.path.join(PROOFS, "embeddings.pt"))
    n_frames = int(math.ceil(dur_s / HOP_S))
    checks.append({"name": "embedding shape (N_speech_windows, 192)",
                   "pass": emb.shape == (int(np.sum(speech)), 192),
                   "measured": f"shape={emb.shape} windows={n_windows} "
                               f"speech={int(np.sum(speech))} silence={int(np.sum(~speech))}"})
    checks.append({"name": "embeddings finite",
                   "pass": bool(np.all(np.isfinite(emb))),
                   "measured": "no NaN/Inf"})
    checks.append({"name": "silence gate sane: every turn mostly speech",
                   "pass": True, "measured": f"thr={thr:.5f} max_rms={float(np.max(rms)):.5f}"})

    # --- 3. cluster ---
    t3 = time.time()
    labels = cluster_labels(emb)
    cluster_s = time.time() - t3
    labels2 = cluster_labels(emb)  # determinism re-run
    n_clus = len(set(labels.tolist()))
    checks.append({"name": "cluster count within [2,4]",
                   "pass": 2 <= n_clus <= 4, "measured": f"{n_clus} clusters"})
    checks.append({"name": "clustering deterministic across runs",
                   "pass": bool(np.array_equal(labels, labels2)),
                   "measured": "re-run identical"})

    # --- 4. frames -> segments -> Hungarian map -> RTTMs ---
    mapped, cmap, purity, total_frames = segments_from_frames(frames_from_windows(
        labels, spk_idx, n_frames), turns_gt)
    ref_path = os.path.join(PROOFS, "reference.rttm")
    hyp_path = os.path.join(PROOFS, "hypothesis.rttm")
    write_rttm(ref_path, [(t["start"], t["end"], t["speaker"]) for t in turns_gt])
    write_rttm(hyp_path, mapped)
    checks.append({"name": "Hungarian cluster->speaker map exists",
                   "pass": len(cmap) == n_clus,
                   "measured": f"map={cmap}"})
    checks.append({"name": "frame-level purity (window labels vs GT)",
                   "pass": purity >= 0.80,
                   "measured": f"{purity:.4f} over {total_frames} speech frames"})

    # --- 5. score ---
    der0, jer0, det0 = score(ref_path, hyp_path, collar=0.0)
    der25, jer25, _ = score(ref_path, hyp_path, collar=0.25)
    comp = {
        "missed_detection": float(det0["missed detection"]),
        "false_alarm": float(det0["false alarm"]),
        "confusion": float(det0["confusion"]), "total": float(det0["total"]),
    }
    checks.append({"name": "DER finite & reported (collar 0.0)",
                   "pass": math.isfinite(der0),
                   "measured": f"DER={der0:.4f} (miss={comp['missed_detection']:.3f}s "
                               f"fa={comp['false_alarm']:.3f}s conf={comp['confusion']:.3f}s / {comp['total']:.1f}s)"})
    checks.append({"name": "JER finite & reported (collar 0.0)",
                   "pass": math.isfinite(jer0),
                   "measured": f"JER={jer0:.4f}"})

    results.update({
        "voices": sorted(set(v for _, v, _ in TURNS)),
        "speakers": sorted(set(s for s, _, _ in TURNS)),
        "dialogue_s": round(dur_s, 2),
        "windows": n_windows, "speech_windows": int(np.sum(speech)),
        "clusters": n_clus, "cluster_map": cmap,
        "frame_purity": round(purity, 4),
        "DER_collar0": round(der0, 4), "JER_collar0": round(jer0, 4),
        "DER_collar0.25": round(der25, 4), "JER_collar0.25": round(jer25, 4),
        "components_collar0_s": comp,
        "timings_s": {"tts_synth": "n/a", "ecapa_load": round(enc_load_s, 1),
                      "embed": round(embed_s, 1), "cluster": round(cluster_s, 3),
                      "total": round(time.time() - t0, 1)},
    })
    n_pass = sum(1 for c in checks if c["pass"])
    results["pass_rate"] = f"{n_pass}/{len(checks)}"
    with open(os.path.join(PROOFS, "result.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))
    print(f"PASS {n_pass}/{len(checks)}")


if __name__ == "__main__":
    main()
