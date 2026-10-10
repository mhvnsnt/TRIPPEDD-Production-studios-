#!/usr/bin/env python3
"""Wave 66 Lane C — supplementary: blind speaker count on REAL single-speaker
voice (cipher-refs clips, concatenated). The EP01 episode audio
(audio-orig.m4a) contains no speech (ASR: 10 words / 300 s), so this is the
real-voice sanity check: a single-speaker recording should count k=1.

Compares baseline (1.5 s / 0.25 s) vs the winning (2.5 s / 0.5 s) grids.
ECAPA on RAW audio (quarantine holds). No GT -> blind: margin + stability.
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # reuse the lane wire as a library
import wire_count_tightening as W

os.environ.setdefault("HF_HUB_OFFLINE", "1")
CLIPS = [
    "../../production/WIZARD_GANG_EP01/cipher-refs/audio/"
    "cipher-voice-backstage-manic.mp3",
    "../../production/WIZARD_GANG_EP01/cipher-refs/audio/"
    "cipher-voice-interview-loop.mp3",
    "../../production/WIZARD_GANG_EP01/cipher-refs/audio/"
    "cipher-voice-ring-taunt.mp3",
]


def main():
    scratch = os.path.join(HERE, "scratch")
    out = os.path.join(HERE, "proofs")
    # 1. build concatenated 16 kHz mono wav (1 s silence gaps), read-only src
    cat = os.path.join(scratch, "cipher_voice_concat.wav")
    if not os.path.isfile(cat):
        parts = []
        for c in CLIPS:
            p = os.path.join(HERE, c)
            assert os.path.isfile(p), p
            parts += ["-i", p]
        # concat with 1 s anullsrc gaps between clips
        W.w65prod.run(["ffmpeg", "-y", "-v", "error",
                       "-i", os.path.join(HERE, CLIPS[0]),
                       "-f", "lavfi", "-t", "1", "-i", "anullsrc=r=16000:cl=mono",
                       "-i", os.path.join(HERE, CLIPS[1]),
                       "-f", "lavfi", "-t", "1", "-i", "anullsrc=r=16000:cl=mono",
                       "-i", os.path.join(HERE, CLIPS[2]),
                       "-filter_complex",
                       "[0:a][1:a][2:a][3:a][4:a]concat=n=5:v=0:a=1,"
                       "aresample=16000,pan=mono|c0=c0[a]",
                       "-map", "[a]", "-c:a", "pcm_s16le", cat])
    audio, dur, _ = W.w65prod.load_audio_any(cat, scratch)
    print(f"concat cipher voice: {dur:.1f}s", flush=True)
    vad_segs = W.w64.vad_segments_gen(audio, **W.PROVEN_VAD)
    speech_s = sum(b - x for x, b in vad_segs)
    print(f"VAD: {len(vad_segs)} segs, {speech_s:.1f}s speech", flush=True)

    res = {"audio": "cipher-refs concat (real single-speaker voice)",
           "dur_s": round(dur, 1),
           "vad_speech_s": round(speech_s, 1)}
    for win_s, hop_s in [(1.5, 0.25), (2.5, 0.5)]:
        tag = f"cipher_win{str(win_s).replace('.', 'p')}_hop{str(hop_s).replace('.', 'p')}"
        idxs, _, _, _ = W.grid(audio, win_s, hop_s)
        emb_all = W.compute_embeddings(audio, idxs, win_s, scratch, tag)
        kept, _, _ = W.kept_windows(audio, idxs, win_s, vad_segs)
        emb = emb_all[np.asarray(kept)]
        k, margin, gaps = W.count_eigengap(emb, 1, 6)
        stab = W.bootstrap_stability(emb, 1, 6)
        r = {"k": k, "margin": round(margin, 3), "kept": f"{len(kept)}/{len(idxs)}",
             "stability": stab["p_mode"], "stab_dist": stab["dist"]}
        print(f"  {win_s}s/{hop_s}s: k={k} margin={margin:.2f}x "
              f"stable={stab['p_mode']:.2f} kept={len(kept)}/{len(idxs)}",
              flush=True)
        res[tag] = r
    import json
    with open(os.path.join(out, "w66_cipher_voice_count.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("-> proofs/w66_cipher_voice_count.json", flush=True)


if __name__ == "__main__":
    main()
