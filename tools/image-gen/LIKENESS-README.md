# likeness_gen — FREE likeness-holding image generation

Owner priority 2026-10-11: our free gen stack (AI Horde img2img, HF Qwen with
prompt-rewriting) destroyed likeness 3+ times. Root cause: those pipelines
generate from TEXT describing the image — the image-to-text indirection loses
everything. This tool conditions DIRECTLY on the input image pixels.

## Architecture: image-conditioned, never text-mediated

```
input image ──→ FLUX.1-Kontext-dev ──→ output image
                     │
              edit instruction (owner's exact words, verbatim)
```

Kontext takes the IMAGE as context and applies the instruction as an edit.
The character's visual identity flows through the image channel, not through
a text description. This is the same principle as the USE THE IMAGE LAW:
the image is the material, not a reference for a description.

## Laws enforced in code

1. **IMAGE-CONDITIONED**: no backend converts the image to words. `likeness_backends.py`
   contains only image-in backends. The old `backend_hf_qwen` (rewrite_prompt=True)
   is NOT used here — it violates the verbatim law.
2. **VERBATIM PROMPT LAW**: `--instruction` is passed byte-for-byte to the model.
   No rewriting, no prompt-engineering, no template wrapping. Default = pass-through.
   `--craft` records agent-crafted provenance when the owner explicitly says
   "figure out the prompt" — the text still goes to the model untouched.

## Backends (preference order)

1. **kontext** — `black-forest-labs/FLUX.1-Kontext-Dev` HF Space (free, gradio_client).
   Image editing model; character consistency is its design goal. Primary.
2. **qwen** — `Qwen/Qwen-Image-Edit` HF Space with `rewrite_prompt=False`.
   Fallback. (Quota exhausts fast.)
3. **horde** — Stable Horde img2img at LOW denoise (0.40). Last resort; cannot
   do real angle changes without drifting.

## Usage

```bash
# Owner's exact words, passed through verbatim:
likeness_gen.py --ref head.png \
  --instruction "turn to three-quarter view facing left, keep the same face" \
  --output out.png

# Owner said "figure out the prompt" — record agent-crafted provenance:
likeness_gen.py --ref head.png --instruction "..." --output out.png --craft

# Pin a backend:
likeness_gen.py --ref head.png --instruction "..." --output out.png --backend qwen
```

Exit: 0 = PASS (likeness gate), 2 = FAIL (output written for inspection),
1 = all backends failed.

## Verification

Every output runs through `verify_likeness` (face-ROI drift vs reference +
sensorium style_hold). Note: the face_drift pixel metric is meaningful for
composition-preserving edits; for ANGLE CHANGES the pixels must move, so
human eye verification is the gate. Both are reported.

## Proof (2026-10-11)

- Dickie `head_sep.png` → 3/4 view via Kontext: eyes PASS (same hair, goatee,
  eyes, brows, skin, shirt, SP style). face_drift N/A for rotation (pixels move
  by design).
- Dickie `head_sep.png` → background change via Kontext: face_drift + style_hold
  gate.

## Self-hosted endgame (unmetered)

For batch work without Space queues/quotas, run FLUX.1-Kontext-dev or
Qwen-Image-Edit on the owner's free GPUs — see
`notebooks/self_hosted_qwen_kontext.md` (Kaggle 30 GPU-hrs/wk, Colab free T4).
Same image-conditioned architecture, no queues.
