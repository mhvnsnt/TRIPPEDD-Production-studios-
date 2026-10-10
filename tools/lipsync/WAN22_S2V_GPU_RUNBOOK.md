# Wan2.2-S2V-14B — GPU handoff runbook (Wave 6 Worker B)

**Status:** SPEC ONLY — nothing in this file was executed on a GPU in this sandbox.
Sandbox reality (verified 2026-10-07): no `nvidia-smi`, no CUDA, ~7 GB RAM.
Do not treat these commands as verified working — they are copied from upstream docs.

**What it is:** Alibaba Tongyi Lab's audio-driven cinematic video generation —
reference portrait + driving audio (+ optional text prompt, + optional pose video)
→ lip-synced character performance (portrait, bust, or full-body), 480p/720p.
This is the talking-head / dialogue-scene engine for the Wizard Gang series.

**License:** ✅ Apache-2.0 commercial-safe (code + weights) — verified in Wave 5
from the GitHub API (`spdx_id: Apache-2.0`) and the HF model card frontmatter
(`license: apache-2.0`).

**Upstream:** code https://github.com/Wan-Video/Wan2.2 ⚠️ the org moved
`Wan-AI` → `Wan-Video`; `github.com/Wan-AI/Wan2.2-S2V` **404s** — do not use.
Weights: https://huggingface.co/Wan-AI/Wan2.2-S2V-14B (ungated, public).
Paper: arXiv:2508.18621 ("Wan-S2V: Audio-Driven Cinematic Video Generation").

---

## Hardware floor

| Path | Minimum | Notes |
|---|---|---|
| Official single-GPU CLI (`generate.py`) | **≥ 80 GB VRAM** | H100 80GB / A100 80GB, with `--offload_model True --convert_model_dtype` (upstream README: "This command can run on a GPU with at least 80GB VRAM") |
| Multi-GPU | 8× GPUs | `torchrun`, FSDP + DeepSpeed Ulysses (`--dit_fsdp --t5_fsdp --ulysses_size 8`) |
| Community ComfyUI path | **~32 GB peak** | kijai `ComfyUI-WanVideoWrapper` on RTX 5090: ~31.9 GB peak / 77-frame audio chunk; chunks chained via `WanSoundImageToVideoExtend`. Third-party report (glad-labs/poindexter, 2026-09) — expect chunk-boundary drift on long audio |

**diffusers entry point — honest correction (2026-10-07 web check):** upstream's
diffusers integrations cover **T2V-A14B, I2V-A14B, TI2V-5B** (Jul 28, 2025) and
**Wan2.2-Animate-14B** (Nov 13, 2025). **No S2V pipeline class in diffusers was
verified** — do NOT invent `from diffusers import WanS2VPipeline`. The supported
S2V entry points are the upstream `generate.py` CLI below (or the ComfyUI
wrapper). If a newer diffusers ships one, verify the class name in the
diffusers docs at runtime.

**What stays blocked without a GPU:** all S2V inference (14B DiT + wav2vec2
audio encoder). There is no smaller S2V checkpoint (no 1.3B/5B S2V) and no
upstream CPU path.

## Disk floor

**Budget 50 GB free for the weights** (verified 2026-10-07 via HTTP HEAD on the
HF file list — totals below; plus HF cache/venv overhead):

| File(s) | HEAD size | Required? |
|---|---|---|
| `diffusion_pytorch_model-00001..4-of-00004.safetensors` | 9.97 + 9.89 + 9.96 + 2.77 = **32.59 GB** | yes (the DiT) |
| `models_t5_umt5-xxl-enc-bf16.pth` | **11.36 GB** | yes (text prompt conditioning) |
| `Wan2.1_VAE.pth` | 0.51 GB | yes |
| `wav2vec2-large-xlsr-53-english/pytorch_model.bin` (ONE container) | 1.26 GB | yes (audio encoder) |
| `wav2vec2-large-xlsr-53-english/language_model/lm.binary` | 0.86 GB | optional (likely unused — encoder only) |
| `wav2vec2-large-xlsr-53-english/{flax_model.msgpack,model.safetensors}` | 2× 1.26 GB | **redundant** — same weights, other containers; skip to save ~2.5 GB |

Full snapshot = **49.14 GB**; required unique set ≈ **46.6 GB**.

> ⚠️ Honest correction: earlier repo notes said "~28 GB" (and the HF API
> `safetensors.total` said 16.3 GB). Both are wrong — HTTP HEAD on every file
> in `Wan-AI/Wan2.2-S2V-14B` sums to ~49 GB. **Do not budget 28 GB.**

## Exact download commands

```bash
# Code (correct org)
git clone https://github.com/Wan-Video/Wan2.2.git && cd Wan2.2
pip install -r requirements.txt   # torch >= 2.4.0; install flash_attn LAST if it fails

# Weights (~49 GB; repo is ungated — no HF login needed)
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B

# Optional: skip the redundant wav2vec2 containers to save ~2.5 GB
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B \
  --exclude "wav2vec2-large-xlsr-53-english/flax_model.msgpack" \
  --exclude "wav2vec2-large-xlsr-53-english/model.safetensors"
```

## 5-second test recipe (series inputs)

**Input A — one wizard still:** any council-member key art, face toward camera,
unobstructed face (16:9 for episodes, 9:16 for vertical promos — output aspect
follows the input image).
**Input B — 5 s speech WAV:** 16-bit PCM, 16–44.1 kHz (e.g. a Static test line).

```bash
# 5-second talking-head test — official single-GPU command shape (verbatim
# from the upstream README, with a wizard still + wizard speech audio)
python generate.py --task s2v-14B --size 1024*704 \
  --ckpt_dir ./Wan2.2-S2V-14B/ \
  --offload_model True --convert_model_dtype \
  --prompt "Wizard Gang dialogue scene: the robed wizard speaks to camera, subtle head nods and hand motion, neon alley sign flickering behind him." \
  --image "<wizard_still.png>" \
  --audio "<5s_speech.wav>"
# Without --num_clip, output length auto-adapts to the audio length (≈5 s).
```

Zero-install smoke test first (optional): the free HF and ModelScope Gradio
demos upstream host can validate the input pairing before the 49 GB download.

## Expected artifacts

- `*.mp4` (480p or 720p), duration ≈ audio duration (≈5 s for the test).
- One video + one audio stream (audio muxed back at the end).
- Lip movement synced to the audio; identity, lighting, background stable.

## How the GPU worker verifies success

1. `ffprobe -v error -show_streams out.mp4` → exactly one video + one audio stream.
2. Duration within **±1 s** of the input audio duration.
3. Extract first / middle / last frames (`ffmpeg -i out.mp4 -vf
   "select='eq(n\,0)+eq(n\,120)+eq(n\,240)'" -vsync vfr check_%d.png`) and
   **open and look at each one**: same face/identity across frames, mouth
   actually moves (not a static image), no melting geometry on the face/hands.
4. First/last frame vs input still: character design unchanged.
5. Report back: GPU model, `nvidia-smi` peak VRAM, seconds of wall-clock per
   generated second, any drift notes, and whether `--offload_model` was needed.

## What stays blocked without a GPU (summary)

S2V inference entirely. The ~49 GB weights and the CLI wiring can be staged on
a CPU box, but generation itself needs an 80 GB-class card (or ~32 GB via the
community ComfyUI path). No CPU fallback exists upstream.

## Wave 10 re-verification (2026-10-07 — sandbox still GPU-less)

- Full snapshot re-verified via recursive HF file list: **49,148,820,007 B =
  49.15 GB** (unchanged from the 49.14 GB figure); the `wav2vec2` subfolder is
  present with identical sizes (`pytorch_model.bin` 1.26 GB, `lm.binary` 0.86 GB,
  both redundant 1.26 GB containers); required unique set still ≈ 46.6 GB.
- Upstream `generate.py` untouched since 2025-09-19; the Sep 2026 commit
  (TalkVerse community work) is README-only — the `--task s2v-14B` CLI shape
  in this runbook stands.
- diffusers at main (v0.41.0 released 2026-10-06) STILL ships no S2V pipeline
  class (`src/diffusers/pipelines/wan/` = t2v / i2v / v2v / animate / vace
  only) — the "do NOT invent `from diffusers import WanS2VPipeline`" warning
  stands.
