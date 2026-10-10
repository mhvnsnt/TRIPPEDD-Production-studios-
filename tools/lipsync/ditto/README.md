# TRIPPEDD lipsync — Ditto (realtime talking-head)

`Ditto: Motion-Space Diffusion for Controllable Realtime Talking Head
Synthesis` (ACM MM 2025, Ant Group). Audio-driven talking head: a diffusion
model generates 265-dim motion-space keypoints from audio features, then a
warp renderer animates the source portrait. Realtime-capable (30 FPS
streaming via the online pipeline).

- Code: `antgroup/ditto-talkinghead` (GitHub) — vendored under `upstream/`
  (`git clone --depth 1`, kept as reference; not committed — see note below)
- Weights: `digital-avatar/ditto-talkinghead` (Hugging Face)
- License: **Apache-2.0** — verified on the upstream repo (README "released
  under the Apache-2.0 license"; GitHub license badge Apache-2.0).
  Commercial-safe badge.

## Status

**PARTIAL → CPU proof of the audio→motion brain (real output, this
sandbox).** Full portrait rendering is GPU-handoff.

Proven in-sandbox (`proofs/`): `ditto_cpu_motion_proof.py` runs the REAL
upstream components on CPU via onnxruntime (no TensorRT, no CUDA):
`hubert.onnx` (audio→1024-dim features @25fps) +
`lmdm_v0.4_hubert.onnx` (motion-space diffusion, 50 DDIM steps) →
`(1, 80, 265)` motion keypoint sequence saved as `.npy`.

Honest caveats: `cond_frame` (source-face keypoint condition) and
emo/eye/sc conditioning are fixed to neutral constants — the full pipeline
derives them from the source portrait (motion extractor / face registration).
Lip/expression channels in the output are still audio-driven; the proof
asserts temporal variance of the motion sequence, not visual quality.

## Install recipe

```bash
# code
git clone --depth 1 https://github.com/antgroup/ditto-talkinghead.git

# python deps (CPU)
pip install onnxruntime librosa soundfile numpy scipy

# weights from HF (paths inside digital-avatar/ditto-talkinghead)
#   ditto_onnx/hubert.onnx                (~1.4 GB)
#   ditto_onnx/lmdm_v0.4_hubert.onnx      (motion diffusion)
#   ditto_onnx/{appearance_extractor,motion_extractor,warp_network,
#               stitch_network,decoder}.onnx   (renderer, GPU worker)
#   ditto_onnx/{blaze_face,face_mesh,insightface_det,landmark106,
#               landmark203}.onnx              (face registration)
#   ditto_cfg/v0.4_hubert_cfg_pytorch.pkl (reference config)
huggingface-cli download digital-avatar/ditto-talkinghead \
  --include "ditto_onnx/*" "ditto_cfg/*" --local-dir ./ditto_weights
```

NOTE (2026-10-07): `huggingface_hub`'s httpx breaks on this sandbox's
`no_proxy` (IPv6 literals `::1`/`[::1]`); strip entries containing `::`
from `no_proxy`/`NO_PROXY` before downloading (see TOOLS.md proxy quirk).

## Run the CPU proof

```bash
python ditto_cpu_motion_proof.py \
  --audio ../proofs/rhubarb_speech_3s.wav \
  --out   proofs/ditto_motion_3s.npy
```

Timing on this sandbox (7 GB RAM, CPU): hubert features for 3 s audio take
a few minutes; 50-step diffusion on the 80-frame window takes a few more.
`--steps 10` gives a quick smoke run.

## GPU-worker handoff spec (full portrait render)

- Follow the official `stream_pipeline_offline.py` / `inference.py` with the
  **PyTorch or TensorRT** checkpoints (`ditto_pytorch/*`), or convert the
  ONNX set with `scripts/cvt_onnx_to_trt.py`.
- VRAM: community deployments run realtime on RTX 3090/4090 (24 GB);
  8 GB minimum reported for the streaming pipeline.
- Full pipeline per frame-window: face registration (blaze_face/landmark203
  ONNX) → appearance/motion extractors → LMDM diffusion (this lane's proof)
  → warp_network + stitch_network + decoder → mp4 mux with the driving audio
  (`ffmpeg -i video -i audio -c:v copy -c:a aac out.mp4`, as in `inference.py`).
- Config reference: `ditto_cfg/v0.4_hubert_cfg_pytorch.pkl`
  (`audio_feat_dim=1103`, `motion_feat_dim=265`, `seq_frames=80`,
  `sampling_timesteps=50`, `overlap_v2=10`).

## TRIPPEDD fit

Ditto is the realtime/interactive pick: live avatar dialogue, NPC chatter,
cartoon dialogue shots where the portrait is already approved and only the
mouth/performance needs driving. Wan2.2-S2V is the offline cinematic pick.
OVRLipSync is the in-engine 3D-morph pick. Rhubarb stays the 2D-puppet pick.
