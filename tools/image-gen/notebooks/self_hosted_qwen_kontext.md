# Qwen-Image-Edit / FLUX.1-Kontext on free GPUs — self-hosted reference-driven generation

Owner 2026-10-11: the "better than all of them" endgame. Our own unmetered model —
no queues (AI Horde), no quota walls (HF Spaces), no per-call billing.

## Option A: Kaggle (30 GPU-hours/week, already set up per memory)

1. New notebook, accelerator: **GPU T4 x2**.
2. Run:
```python
!pip install -q diffusers transformers accelerate gradio_client pillow
```
3. Qwen-Image-Edit quick serve:
```python
import torch
from diffusers import QwenImageEditPlusPipeline
pipe = QwenImageEditPlusPipeline.from_pretrained(
    "Qwen/Qwen-Image-Edit", torch_dtype=torch.bfloat16).to("cuda")
from PIL import Image
ref = Image.open("photo.jpg").convert("RGB")
out = pipe(image=ref,
    prompt="South Park cartoon version of this person, accurate to their likeness, "
           "South Park body proportions, clothing matching the photo",
    negative_prompt="photorealistic, blurry, watermark",
    num_inference_steps=40, true_cfg_scale=4.0).images[0]
out.save("out.png")
```
4. Keep the notebook: re-run per reference photo. 30 GPU-hrs/week = hundreds of generations.

## Option B: Google Colab (free T4)

Same code as above in a Colab cell. Free tier disconnects on idle — generate in
batches, download outputs each run.

## Option C: FLUX.1-Kontext (alternative model, instruction-tuned editing)

```python
!pip install -q diffusers transformers accelerate
from diffusers import FluxKontextPipeline
import torch
pipe = FluxKontextPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev", torch_dtype=torch.bfloat16).to("cuda")
```

## Wiring it back here
- Outputs land in `~/workspace/tpb-ai-base/` (or the task's folder), then get
  filed into the repo per the salvage law.
- Every output still runs through `gen.py`'s scoring (`--pick` accepts local
  files as candidates in a future pass) — self-hosted doesn't mean unverified.
- Prompt pattern (the ChatGPT method): reference photo + "South Park versions
  of themselves, accurate to likeness like SP does celebrities, South Park
  bodies, clothing from the photo."
