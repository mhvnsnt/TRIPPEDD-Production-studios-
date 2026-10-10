# Wan 2.2 — open image-to-video workhorse (Wave 2 wiring)

Date: 2026-10-07. Repo: both (trippedd production + god-molecule creative).

## License (verified 2026-10-07)
**Apache-2.0 on code AND weights** — confirmed at `github.com/Wan-Video/Wan2.2`
(LICENSE.txt) and the HuggingFace model card ("models in this repository are
licensed under the Apache 2.0 License"). No revenue cap, no territory
restriction. Fully commercial-safe — the open I2V workhorse.

## Wiring status
**WIRED — inference path proven (no weight download).** The 14B weights are
GPU-box downloads; what matters for the pipeline is the code path:
- `diffusers==0.35.1` installed in `~/venvs/whisperx` (pinned: newest
  diffusers needs huggingface-hub>=1.32 which breaks whisperx's hub<1.0 —
  0.35.1 satisfies both).
- `from diffusers import WanImageToVideoPipeline, WanPipeline, WanVideoToVideoPipeline`
  — imports clean (`WAN_PIPELINES_OK`, 2026-10-07).

## Inference path (GPU box)
```python
from diffusers import WanImageToVideoPipeline
import torch
pipe = WanImageToVideoPipeline.from_pretrained(
    "Wan-AI/Wan2.2-I2V-A14B-Diffusers", torch_dtype=torch.bfloat16).to("cuda")
# TI2V-5B is the practical GPU-poor entry point
video = pipe(image=still, prompt="...").frames[0]
```

## Pipeline slot
Animate the show's generated stills: every storyboard still becomes a shot
via I2V. TI2V-5B for iteration, I2V-A14B for hero shots.
