# Wan 2.2 TI2V-5B — REAL I2V test lane (Wave 3 Worker C)

Date: 2026-10-07. Sandbox truth report. **No artifacts faked — this is the documented partial.**

## GPU state
**No GPU.** `nvidia-smi` not present; CPU-only box, 7.8 GB RAM, 7.0 GB free disk
(`/home/hatch` at 94%).

## Weight sizes (from live HuggingFace API, `Wan-AI/Wan2.2-TI2V-5B`, 2026-10-07)
| file | bytes |
|---|---|
| `diffusion_pytorch_model-00001-of-00003.safetensors` | 9,825,014,472 |
| `diffusion_pytorch_model-00002-of-00003.safetensors` | 9,995,661,736 |
| `diffusion_pytorch_model-00003-of-00003.safetensors` | 178,558,176 |
| `Wan2.2_VAE.pth` | 2,818,839,170 |
| `models_t5_umt5-xxl-enc-bf16.pth` | ~11,000,000,000 (umt5-xxl class) |
| **total** | **≈ 34 GB** |

Free disk: 7.0 GB. **Download is physically impossible on this box** — not
attempted beyond this accounting, because any shard alone exceeds free space.

## License (re-verified 2026-10-07, evidence in this dir)
- HF model card metadata: `license:apache-2.0` (fetched from the live API today).
- `README.md` (15,935 bytes, fetched): contains `apache-2.0`.
- `LICENSE.txt` (11,357 bytes, fetched from github.com/Wan-Video/Wan2.2): Apache-2.0.
- **✅ Apache-2.0 on code AND weights** — commercial-safe, no revenue cap.

## Inference path (code-level, no weights needed)
Re-verified in the pinned Wave 2 venv `~/venvs/whisperx`, 2026-10-07:
- `diffusers==0.35.1`, `from diffusers import WanImageToVideoPipeline` → **OK**
  (proves the TI2V-5B pipeline class is available; weights are the missing piece).

## GPU-box runbook (this is what runs on a CUDA box with ≥40 GB disk)
```python
from diffusers import WanImageToVideoPipeline
import torch
pipe = WanImageToVideoPipeline.from_pretrained(
    "Wan-AI/Wan2.2-I2V-A14B-Diffusers", torch_dtype=torch.bfloat16).to("cuda")
frames = pipe(image=still_image, prompt="...").frames[0]  # few-frames test first
```
TI2V-5B (~34 GB full set, ~20 GB diffusion) is the iteration model;
I2V-A14B is the hero-shot model.

## Verdict
**BLOCKED-HONEST:** weights verified available + licensed, but this sandbox
cannot hold or run them (no CUDA, 7 GB free disk, 7.8 GB RAM). No fake
"proof frames" generated. A real few-frame I2V test belongs on a GPU worker —
this file plus `tools/generative_stack/WAN22_WIRING.md` is the complete handoff.

## Evidence files (this directory)
- `README.md` — model card as served by HF today
- `config.json` — Ti2V-5B model config (dim 3072, 30 layers, 24 heads)
- `diffusion_index.json` — safetensors shard index (proves 3-shard layout)
- `license_text.txt` — Apache-2.0 license text from upstream repo
