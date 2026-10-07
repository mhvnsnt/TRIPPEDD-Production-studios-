#!/usr/bin/env python3
"""Ditto CPU micro-proof (ONNX, TensorRT-free, GPU-free).

Runs the REAL Ditto audio->motion brain on CPU with onnxruntime:
  WAV (16 kHz) -> hubert.onnx (audio features, 25 fps x 1024)
              -> cond assembly (aud + neutral emo/eye/sc = 1103-dim)
              -> lmdm_v0.4_hubert.onnx (motion-space diffusion, 50 DDIM steps)
              -> (1, 80, 265) motion keypoint sequence saved as .npy

Weights: digital-avatar/ditto-talkinghead on Hugging Face (Apache-2.0).
Code: antgroup/ditto-talkinghead (Apache-2.0), vendored under upstream/.

Caveats (honest, not hidden):
 - cond_frame (source-face keypoint condition) is a NEUTRAL (zeros) vector;
   the full pipeline derives it from the source portrait via the motion
   extractor. Lip/expression channels are still audio-driven.
 - emo/eye/sc conditioning is fixed to neutral constants (same reason).
 - This proves the audio-driven motion generator; the warp renderer
   (appearance/warp/stitch/decoder ONNX) is documented but NOT run here
   (needs the face-registered source image; GPU-worker handoff in README).

Usage:
  python ditto_cpu_motion_proof.py --audio <wav> --out <npy>
"""
import argparse, math, os, sys, time
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--hubert", default=os.path.join(os.path.dirname(__file__), "weights", "ditto_onnx_hubert.onnx"))
    ap.add_argument("--lmdm", default=os.path.join(os.path.dirname(__file__), "weights", "ditto_onnx_lmdm_v0.4_hubert.onnx"))
    ap.add_argument("--steps", type=int, default=50)
    args = ap.parse_args()

    import librosa, onnxruntime as ort

    print("[1/4] loading audio:", args.audio, flush=True)
    audio, sr = librosa.load(args.audio, sr=16000, mono=True)
    audio = audio.astype(np.float32)
    num_f = math.ceil(len(audio) / 16000 * 25)
    print("      samples:", len(audio), "-> video frames @25fps:", num_f, flush=True)

    print("[2/4] hubert.onnx -> audio features", flush=True)
    t0 = time.time()
    hub = ort.InferenceSession(args.hubert, providers=["CPUExecutionProvider"])
    inp = hub.get_inputs()[0]
    print("      hubert input:", inp.name, inp.shape, "| output:", hub.get_outputs()[0].name, flush=True)
    chunksize = (3, 5, 2)
    split_len = int(sum(chunksize) * 0.04 * 16000) + 80  # 6480
    speech_pad = np.concatenate([
        np.zeros((split_len - int(sum(chunksize[1:]) * 0.04 * 16000),), dtype=np.float32),
        audio,
        np.zeros((split_len,), dtype=np.float32),
    ], 0)
    res = []
    i = 0
    while i < num_f:
        sss = int(i * 0.04 * 16000)
        chunk = speech_pad[sss:sss + split_len].reshape(1, -1)
        enc = hub.run(None, {"input_values": chunk})[0]          # [1, T, 1024]
        valid = enc[0][-sum(chunksize[1:]) * 2: -chunksize[2] * 2]
        valid_feat = valid.reshape(chunksize[1], 2, 1024).mean(1)  # [5, 1024]
        res.append(valid_feat)
        i += chunksize[1]
    aud_feat = np.concatenate(res, 0)[:num_f]                     # [num_f, 1024]
    print("      aud_feat:", aud_feat.shape, "in %.1fs" % (time.time() - t0), flush=True)

    print("[3/4] assembling cond (aud 1024 + emo 8 + eye_open 2 + eye_ball 6 + sc 63 = 1103)", flush=True)
    # neutral emo softmax like upstream _get_emo_avg(4) = 'Neutral'
    emo = np.zeros(8, dtype=np.float32); emo[4] = 8.0
    emo = np.exp(emo) / np.exp(emo).sum()
    eye_open = np.array([1.0, 1.0], dtype=np.float32)   # fully open
    eye_ball = np.zeros(6, dtype=np.float32)
    sc = np.zeros(63, dtype=np.float32)                  # identity-neutral shape code
    cond = np.concatenate([
        aud_feat,
        np.tile(emo, (num_f, 1)),
        np.tile(eye_open, (num_f, 1)),
        np.tile(eye_ball, (num_f, 1)),
        np.tile(sc, (num_f, 1)),
    ], -1).astype(np.float32)
    print("      cond:", cond.shape, flush=True)

    print("[4/4] lmdm diffusion sampling (%d steps, 80-frame window)" % args.steps, flush=True)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "upstream"))
    from core.models.lmdm import LMDM
    lmdm = LMDM(model_path=args.lmdm, device="cpu",
                motion_feat_dim=265, audio_feat_dim=1103, seq_frames=80)
    lmdm.setup(args.steps)
    seq_frames = 80
    aud = cond[None, :seq_frames]
    if aud.shape[1] < seq_frames:                        # pad short clips
        aud = np.concatenate([aud, np.tile(aud[:, -1:], (1, seq_frames - aud.shape[1], 1))], 1)
    kp_cond = np.zeros((1, 265), dtype=np.float32)       # neutral source-face condition
    t0 = time.time()
    motion = lmdm(kp_cond, aud.astype(np.float32), args.steps)   # (1, 80, 265)
    print("      diffusion done in %.1fs" % (time.time() - t0), flush=True)

    np.save(args.out, motion)
    print("saved:", args.out, motion.shape, motion.dtype, flush=True)
    # sanity: motion must vary across frames and differ from pure noise
    std_t = motion[0].std(0)
    print("per-dim temporal std: min %.4f  mean %.4f  max %.4f" % (std_t.min(), std_t.mean(), std_t.max()))
    print("motion[0,0,:5] =", motion[0, 0, :5])

if __name__ == "__main__":
    main()
