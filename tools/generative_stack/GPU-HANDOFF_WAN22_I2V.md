# GPU-HANDOFF — Wan 2.2 I2V / TI2V-5B image-to-video (Wave 7)

**Status: SPEC ONLY.** Nothing here has been executed on a GPU. This sandbox
has no CUDA card (`nvidia-smi` absent, no `/dev/nvidia*`) — the 5B DiT's
diffusion sampling cannot run here. Do not fabricate video. Full recipe:
`tools/generative_stack/WAN22_I2V_GPU_RUNBOOK.md`. Code/import path proven on
this box: `diffusers==0.35.1` in `~/venvs/whisperx`, `from diffusers import
WanImageToVideoPipeline` imports clean (re-verified 2026-10-07).

## GPU worker needs

| Item | Requirement |
|---|---|
| GPU | **24 GB VRAM** (RTX 4090-class) for TI2V-5B — 5 s 720p @24 fps in <9 min upstream, no special optimization; 40–80 GB class for I2V-A14B (official single-GPU path w/ `--offload_model True --convert_model_dtype`); 12 GB+ cards via the ComfyUI path only |
| Disk | **≥ 40 GB free** (TI2V-5B weights ≈ 34.2 GB: DiT safetensors 29.83 GB + UMT5 text encoder 11.36 GB + VAE 2.82 GB, HTTP HEAD-verified 2026-10-07) |
| Software | torch CUDA wheel, `diffusers==0.35.1` (pinned — newest diffusers needs `huggingface-hub>=1.32`, which breaks whisperx's `hub<1.0`; keep 0.35.1 on the GPU box too) |
| Network | huggingface.co reachable (ungated — no HF login needed) |

## Commands

```bash
pip install "huggingface_hub[cli]" diffusers==0.35.1
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B-Diffusers --local-dir ./Wan2.2-TI2V-5B-Diffusers
```

Test recipe (one wizard still → 2 s clip):

```python
import torch
from diffusers import WanImageToVideoPipeline
from diffusers.utils import export_to_video

pipe = WanImageToVideoPipeline.from_pretrained(
    "Wan-AI/Wan2.2-TI2V-5B-Diffusers", torch_dtype=torch.bfloat16).to("cuda")
video = pipe(
    image="<wizard_still.png>",
    prompt=("The robed wizard turns slowly toward camera, neon alley signs "
            "flicker behind him, embers drift upward, subtle cinematic "
            "dolly-in, dark fantasy film still come alive."),
    height=720, width=1280, num_frames=49,   # 49 frames @ 24 fps ≈ 2 s
).frames[0]
export_to_video(video, "wan22_i2v_test.mp4", fps=24)
```

## Expected outputs

- `wan22_i2v_test.mp4` — 2 s, 720p, 24 fps, **exactly 49 frames**; motion
  present (turn, flicker, embers); the wizard's character design unchanged from
  the input still.
- Verification: `ffprobe` → 1280×720, 24 fps, 49 frames / ≈2.04 s; open frame 0
  and frame 48 **side-by-side with the input still** — identity unchanged (no
  morphing, no invented logos/text); eyeball a mid-frame for anatomy
  (hands/face intact, no melting).

## Proof artifacts to report back

GPU model · `nvidia-smi` peak VRAM · wall-clock seconds for the 49-frame clip ·
diffusers-vs-`generate.py` path · exact prompt · the MP4's sha256.

## Licenses (verified 2026-10-07)

- Wan 2.2 code + weights: **Apache-2.0** (GitHub API `spdx_id` on `Wan-Video/Wan2.2`;
  HF cards `license: apache-2.0` on `Wan-AI/Wan2.2-TI2V-5B`,
  `Wan-AI/Wan2.2-TI2V-5B-Diffusers`, `Wan-AI/Wan2.2-S2V-14B`). README grants full
  rights over generated content.
- Upstream: code https://github.com/Wan-Video/Wan2.2 (org moved `Wan-AI` →
  `Wan-Video` — old `Wan-AI` GitHub URLs 404; HF weights stay under `Wan-AI/`).

## What stays blocked without a GPU

All I2V inference. Weight staging, the diffusers import proof, and prompt
design are the only CPU-side work possible. Pipeline slot: every wizard
storyboard still → shot; TI2V-5B for iteration, I2V-A14B for hero shots.
