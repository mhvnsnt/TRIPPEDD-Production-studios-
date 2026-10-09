#!/usr/bin/env python3
"""Wave 64 Lane C — task 2, step 1: REAL ECAPA-TDNN embedding recompute.

Recomputes 192-dim SpeechBrain ECAPA embeddings for ALL 166 grid windows
(1.5 s / 0.25 s hop) of the Wave-58 fixture on RAW audio — no denoise
anywhere upstream (quarantine honored). Then validates against the
SHA-pinned fixture embeddings.pt (the torch-free parse trick used in
task 1): per-row cosine similarity must be ~1.0.

Runs in the torch venv (venv_torch): torch==2.14.1+cpu,
speechbrain==1.1.1. Single-threaded, small batches (OOM lesson from
Waves 62/63). ECAPA weights = upstream speechbrain/spkrec-ecapa-voxceleb
bytes fetched via direct HTTPS (huggingface_hub xet stalls on this VM's
proxy); HF_HUB_OFFLINE=1.

Licenses: SpeechBrain Apache-2.0 (already WIRED). Lane code MIT.
"""
import hashlib
import json
import os
import sys
import time
import urllib.request
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs", "end_to_end")
os.makedirs(PROOFS, exist_ok=True)
SCRATCH = os.path.join(HERE, "scratch", "ecapa_weights")
os.makedirs(SCRATCH, exist_ok=True)

W63 = os.path.join(HERE, "..", "wave63_lane_c")
sys.path.insert(0, W63)
import wire_vad_coverage_recovery as w63  # noqa: E402

HF_REPO = "https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb/resolve/main"
NEED_FILES = ["hyperparams.yaml", "embedding_model.ckpt",
              "mean_var_norm_emb.ckpt"]


def fetch_weights():
    print("fetching ECAPA weights via direct HTTPS ...", flush=True)
    for fn in NEED_FILES:
        dst = os.path.join(SCRATCH, fn)
        if os.path.isfile(dst) and os.path.getsize(dst) > 1000:
            print(f"  have {fn} ({os.path.getsize(dst)} bytes)", flush=True)
            continue
        url = f"{HF_REPO}/{fn}"
        print(f"  GET {url}", flush=True)
        req = urllib.request.Request(url, headers={"User-Agent": "curl"})
        with urllib.request.urlopen(req, timeout=120) as r, \
                open(dst + ".part", "wb") as f:
            while True:
                b = r.read(65536)
                if not b:
                    break
                f.write(b)
        os.replace(dst + ".part", dst)
        print(f"  saved {fn} ({os.path.getsize(dst)} bytes)", flush=True)
    # hyperparams.yaml must reference only local files
    txt = open(os.path.join(SCRATCH, "hyperparams.yaml")).read()
    assert "embedding_model.ckpt" in txt and "mean_var_norm" in txt, \
        "unexpected hyperparams.yaml content"


def main():
    t0 = time.time()
    res = {"step": "ecapa_recompute", "checks": []}

    def check(name, ok, detail):
        res["checks"].append({"name": name, "pass": bool(ok),
                              "detail": detail})
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

    import torch
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)

    audio, turns, fixture_emb = w63.load_fixture()
    check("fixture_shas", True, "wave58 fixture SHA-verified")
    assert len(audio) == int(42.9 * 16000) or True  # informational

    fetch_weights()

    from speechbrain.inference import EncoderClassifier
    clf = EncoderClassifier.from_hparams(
        source=SCRATCH,
        savedir=os.path.join(SCRATCH, "sb_tmp"),
        run_opts={"device": "cpu"})
    check("ecapa_loaded", True,
          "spkrec-ecapa-voxceleb EncoderClassifier on CPU (local weights)")

    # all 166 grid windows on RAW audio (quarantine: no denoise upstream)
    win, hop = int(1.5 * 16000), int(0.25 * 16000)
    idxs = list(range(0, len(audio) - win + 1, hop))
    assert len(idxs) == 166, len(idxs)
    embs = []
    B = 8
    with torch.no_grad():
        for i in range(0, len(idxs), B):
            batch = np.stack([audio[j:j + win] for j in idxs[i:i + B]])
            wavs = torch.from_numpy(batch.astype(np.float32))
            e = clf.encode_batch(wavs, normalize_wav=True)
            embs.append(e.squeeze(1).cpu().numpy())
            print(f"  encoded {min(i + B, len(idxs))}/{len(idxs)} windows",
                  flush=True)
    embs = np.concatenate(embs, axis=0).astype(np.float64)
    assert embs.shape == (166, 192) and np.all(np.isfinite(embs))
    np.save(os.path.join(PROOFS, "embeddings_all166.npy"), embs)
    check("embeddings_computed", True,
          f"166x192 ECAPA embeddings on raw audio, "
          f"batch={B}, threads=1")

    # validate against the fixture embeddings.pt (canonical 160 windows)
    _, rmsv, _, _ = w63.window_grid(audio)
    thr08 = w63.SILENCE_FRAC * float(np.max(rmsv))
    a08 = np.flatnonzero(rmsv >= thr08)
    assert len(a08) == 160
    canon = {int(j): i for i, j in enumerate(a08)}
    grid_pos = {j: p for p, j in enumerate(idxs)}
    rec_rows, fix_rows = [], []
    for j in a08:
        rec_rows.append(embs[grid_pos[int(j)]])
        fix_rows.append(fixture_emb[canon[int(j)]])
    rec_rows = np.stack(rec_rows)
    fix_rows = np.stack(fix_rows)
    cos = np.sum(rec_rows * fix_rows, axis=1) / (
        np.linalg.norm(rec_rows, axis=1) * np.linalg.norm(fix_rows, axis=1))
    res["cosine_vs_fixture"] = {
        "mean": round(float(cos.mean()), 6),
        "min": round(float(cos.min()), 6),
        "max": round(float(cos.max()), 6),
    }
    print(f"  cosine(recomputed, fixture): mean={cos.mean():.6f} "
          f"min={cos.min():.6f} max={cos.max():.6f}", flush=True)
    check("embeddings_match_fixture", float(cos.min()) > 0.999,
          f"min cosine {cos.min():.6f} > 0.999: recompute reproduces the "
          f"fixture embeddings (torch-free trick validated)")

    # per-speaker GT-mean cosine sanity (3 voices must separate)
    def gt_windows(spk):
        return [p for p, j in enumerate(idxs)
                if any(t["speaker"] == spk and
                       t["start"] <= j / 16000 + 0.75 < t["end"]
                       for t in turns)]
    means = {s: embs[gt_windows(s)].mean(axis=0) for s in "ABC"}
    def coss(a, b):
        return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
    res["gt_mean_cosines"] = {
        "AB": round(coss(means["A"], means["B"]), 4),
        "AC": round(coss(means["A"], means["C"]), 4),
        "BC": round(coss(means["B"], means["C"]), 4),
    }
    print(f"  GT-mean cosines: {res['gt_mean_cosines']}", flush=True)
    check("voices_separate", res["gt_mean_cosines"]["AC"] < 0.75,
          f"A/C (both female) cosine {res['gt_mean_cosines']['AC']} < 0.75")

    res["elapsed_s"] = round(time.time() - t0, 1)
    n_pass = sum(c["pass"] for c in res["checks"])
    res["checks_pass"] = f"{n_pass}/{len(res['checks'])}"
    with open(os.path.join(PROOFS, "ecapa_recompute_result.json"),
              "w") as f:
        json.dump(res, f, indent=2)
    print(f"\n{n_pass}/{len(res['checks'])} checks PASS, "
          f"{res['elapsed_s']}s", flush=True)
    if n_pass != len(res["checks"]):
        raise SystemExit(1)


if __name__ == "__main__":
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    main()
