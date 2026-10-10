# GPU-HANDOFF — Wan 2.2-S2V-14B talking-head / dialogue scenes (Wave 7)

**Status: SPEC ONLY.** Nothing here has been executed on a GPU. This sandbox
has no CUDA card (`nvidia-smi` absent, no `/dev/nvidia*`) — the 14B DiT +
wav2vec2 audio encoder cannot run here. Do not fabricate video. Full recipe:
`tools/lipsync/WAN22_S2V_GPU_RUNBOOK.md`. There is **no diffusers S2V pipeline
class** (upstream diffusers covers T2V-A14B / I2V-A14B / TI2V-5B / Animate-14B
only) — do NOT invent `from diffusers import WanS2VPipeline`; the entry points
are the upstream `generate.py` CLI or the ComfyUI wrapper.

## GPU worker needs

| Item | Requirement |
|---|---|
| GPU | **≥ 80 GB VRAM** (H100 80GB / A100 80GB) for the official single-GPU CLI with `--offload_model True --convert_model_dtype` (upstream: "This command can run on a GPU with at least 80GB VRAM"); 8× GPUs for the multi-GPU FSDP path; **~32 GB peak** via the community ComfyUI path (`ComfyUI-WanVideoWrapper` on RTX 5090: ~31.9 GB peak / 77-frame audio chunk, third-party report) |
| Disk | **≥ 50 GB free** (weights: DiT safetensors 32.59 GB + UMT5 text encoder 11.36 GB + Wan2.1 VAE 0.51 GB + wav2vec2 english encoder 1.26 GB ≈ **46.6 GB unique**; full snapshot 49.14 GB. HTTP HEAD-verified 2026-10-07 — do not budget the stale "~28 GB" figure) |
| Software | torch ≥ 2.4.0 (CUDA wheel), flash_attn LAST if it fails |
| Network | huggingface.co reachable (ungated — no HF login needed) |

## Commands

```bash
git clone https://github.com/Wan-Video/Wan2.2.git && cd Wan2.2   # correct org — Wan-AI GitHub URLs 404
pip install -r requirements.txt
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B
# optional: skip redundant wav2vec2 containers (~2.5 GB saved)
#   --exclude "wav2vec2-large-xlsr-53-english/flax_model.msgpack" \
#   --exclude "wav2vec2-large-xlsr-53-english/model.safetensors"
```

5-second talking-head test (wizard still + wizard speech WAV; command shape
verified verbatim against the current upstream README, 2026-10-07):

```bash
python generate.py --task s2v-14B --size 1024*704 \
  --ckpt_dir ./Wan2.2-S2V-14B/ \
  --offload_model True --convert_model_dtype \
  --prompt "Wizard Gang dialogue scene: the robed wizard speaks to camera, subtle head nods and hand motion, neon alley sign flickering behind him." \
  --image "<wizard_still.png>" \
  --audio "<5s_speech.wav>"
# Without --num_clip, output length auto-adapts to the audio length (≈5 s).
```

Zero-install pre-check (optional): upstream's free HF/ModelScope Gradio demos
can validate the still+audio pairing before the ~49 GB download.

## Expected outputs

- `*.mp4` (480p or 720p), duration ≈ input audio duration (±1 s); one video +
  one audio stream (audio muxed back at the end).
- Lip movement synced to the audio; identity, lighting, background stable.
- Verification: `ffprobe -show_streams` → exactly 1 video + 1 audio stream;
  extract first/middle/last frames and **open and look at each one** — same
  face across frames, mouth actually moves (not a static image), no melting
  face/hands; first/last frame vs input still: character design unchanged.

## Proof artifacts to report back

GPU model · `nvidia-smi` peak VRAM · wall-clock seconds per generated second ·
whether `--offload_model` was needed · chunk-boundary drift notes (ComfyUI
path) · the MP4's sha256.

## Licenses (verified 2026-10-07)

- Wan2.2-S2V code + weights: **Apache-2.0** (GitHub API `spdx_id`; HF card
  `license: apache-2.0` on `Wan-AI/Wan2.2-S2V-14B`). Paper: arXiv:2508.18621.
- Upstream: code https://github.com/Wan-Video/Wan2.2 · weights
  https://huggingface.co/Wan-AI/Wan2.2-S2V-14B (ungated, public).

## What stays blocked without a GPU

All S2V inference. Weight staging and CLI wiring can be pre-staged on a CPU
box; generation needs an 80 GB-class card (or ~32 GB via ComfyUI). No smaller
S2V checkpoint exists (no 1.3B/5B S2V) and no upstream CPU path. This is the
talking-head / dialogue-scene engine for the Wizard Gang series: reference
portrait + driving audio (+ optional pose video) → lip-synced performance.
