# Wan 2.2 I2V (TI2V-5B) — GPU handoff runbook (Wave 6 Worker B)

**Status:** SPEC ONLY — nothing in this file was executed on a GPU in this sandbox.
Do not fabricate video.

**What it is:** Alibaba Tongyi Lab's open image-to-video workhorse — turn every
wizard key-art still into a shot. The TI2V-5B dense checkpoint (high-compression
4×16×16 VAE) is the practical consumer-GPU entry point: 5 s of 720p @24 fps
on a single consumer GPU with no special optimization (upstream README).
I2V-A14B (MoE, 27 B total / 14 B active) is the hero-shot upgrade — same runbook
shape, bigger card.

**License:** ✅ Apache-2.0 commercial-safe (code + weights) — verified Wave 5
from the GitHub API (`spdx_id: Apache-2.0`) and the HF model card frontmatter
(`license: apache-2.0`). README grants full rights over generated content.

**Upstream:** code https://github.com/Wan-Video/Wan2.2 ⚠️ org moved
`Wan-AI` → `Wan-Video` (old `Wan-AI` GitHub URLs 404 — HF weights stay under
`Wan-AI/`). Weights: `Wan-AI/Wan2.2-TI2V-5B` /
`Wan-AI/Wan2.2-TI2V-5B-Diffusers` (ungated, public).

**diffusers import path — PROVEN in this repo (Wave 2 wiring,
`tools/generative_stack/WAN22_WIRING.md`):** `diffusers==0.35.1` installed in
`~/venvs/whisperx` with a clean
`from diffusers import WanImageToVideoPipeline, WanPipeline,
WanVideoToVideoPipeline` (`WAN_PIPELINES_OK`, 2026-10-07). Pin 0.35.1 on the
GPU box too (newest diffusers needs `huggingface-hub>=1.32`, which breaks
whisperx's `hub<1.0`).

---

## Hardware floor

| Model | Minimum VRAM | Runtime (upstream) |
|---|---|---|
| **TI2V-5B** (test target) | **24 GB** (RTX 4090-class consumer GPU) | 5 s 720p @24 fps in **under 9 minutes**, single consumer GPU, no special optimization |
| I2V-A14B | 40–80 GB class (official single-GPU path with `--offload_model True --convert_model_dtype`); community runs on 24 GB via ComfyUI + FP8/quantized + offload | minutes per 5 s clip |
| Any 12 GB+ card | ComfyUI path (docs.comfy.org Wan2.2 tutorials) | community benchmarks vary |

**What stays blocked without a GPU:** all I2V inference (5B DiT, fp16/bf16
matmuls). The code path and imports are proven on a CPU box; generation needs
a CUDA card.

## Disk floor

**Budget ≥ 40 GB free** (weights + venv + cache; 45 GB safe):

| File(s) in `Wan-AI/Wan2.2-TI2V-5B` | Size (2026-10-07, HTTP HEAD) |
|---|---|
| `diffusion_pytorch_model-00001..3-of-00003.safetensors` | 9.83 + 10.0 + 0.18 = **19.99 GB** (re-measured 2026-10-07: shard-3 is only 178,558,176 B, not ~9.99 GB — the earlier per-shard figure was wrong; **the 34.2 GB total stands**) |
| `models_t5_umt5-xxl-enc-bf16.pth` | **11.36 GB** |
| `Wan2.2_VAE.pth` | 2.82 GB |
| config/json/misc | small |
| **Total** | **≈ 34.2 GB** (matches the catalog's 34 GB figure) |

## Exact download commands

```bash
# Code (correct org)
git clone https://github.com/Wan-Video/Wan2.2.git && cd Wan2.2
pip install -r requirements.txt   # torch >= 2.4.0 (CUDA wheel); flash_attn LAST if it fails

# diffusers path (pinned — proven in this repo)
pip install diffusers==0.35.1

# Weights (ungated — no HF login needed)
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B
# (for the diffusers-native variant instead: Wan-AI/Wan2.2-TI2V-5B-Diffusers)
```

## Test recipe — one wizard still → 2 s clip

**Input:** one wizard key-art still (PNG/JPG, 720p-ish; output aspect follows
the still). Prompt = motion + cinematography direction referencing the still's
content. Keep camera-motion words conservative ("slow dolly-in", "subtle") —
I2V hallucinates on aggressive moves.

```python
# diffusers path (proven imports, GPU box):
import torch
from diffusers import WanImageToVideoPipeline
from diffusers.utils import export_to_video

pipe = WanImageToVideoPipeline.from_pretrained(
    "Wan-AI/Wan2.2-TI2V-5B-Diffusers",
    torch_dtype=torch.bfloat16,
).to("cuda")

video = pipe(
    image="<wizard_still.png>",
    prompt=("The robed wizard turns slowly toward camera, neon alley signs "
            "flicker behind him, embers drift upward, subtle cinematic "
            "dolly-in, dark fantasy film still come alive."),
    height=720, width=1280,
    num_frames=49,          # 49 frames @ 24 fps ≈ 2 s — the smoke test
).frames[0]

export_to_video(video, "wan22_i2v_test.mp4", fps=24)
print("wrote wan22_i2v_test.mp4")
```

Upstream CLI alternative (same weights, official `generate.py`):

```bash
python generate.py --task ti2v-5B --size 1280*720 \
  --ckpt_dir ./Wan2.2-TI2V-5B --offload_model True --convert_model_dtype --t5_cpu \
  --image <wizard_still.png> \
  --prompt "The robed wizard turns slowly toward camera, neon alley signs flicker behind him, embers drift upward, subtle cinematic dolly-in."
```

## Expected artifacts

- `wan22_i2v_test.mp4` — **2 s, 720p, 24 fps, 49 frames**; motion present
  (turn, flicker, embers) but the wizard's character design unchanged from the
  input still.

## How the GPU worker verifies success

1. `ffprobe wan22_i2v_test.mp4` → 1280×720, 24 fps, **exactly 49 frames**
   (`nb_frames` or stream duration ≈ 2.04 s).
2. Extract frame 0 and frame 48 (`ffmpeg -i wan22_i2v_test.mp4 -vf
   "select='eq(n\,0)+eq(n\,48)'" -vsync vfr v_%d.png`) and **open both
   side-by-side with the input still**: identity/character design unchanged
   (no morphing into a different face, no invented logos/text), motion visible
   between frames.
3. Eyeball a mid-frame for anatomy: hands/face intact, no melting.
4. Report back: GPU model, `nvidia-smi` peak VRAM, wall-clock seconds for the
   49-frame clip, which path (diffusers vs `generate.py`), and the exact prompt.

## What stays blocked without a GPU (summary)

I2V generation entirely. Weight staging, the diffusers import proof, and prompt
design all work on a CPU box — the 5B DiT's diffusion sampling does not.
