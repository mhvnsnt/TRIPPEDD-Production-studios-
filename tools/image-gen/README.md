# tools/image-gen — FREE reference-driven image generation

Owner 2026-10-11: beat ChatGPT/Gemini/Grok at OUR job — generate elsewhere, bring it back here.

## The method (learned from the owner's ChatGPT session)
ChatGPT wins with **reference-driven generation**: upload a photo, prompt
"South Park versions of themselves, accurate to likeness like SP does
celebrities, South Park bodies, clothing from the photo." gpt-image-1 embeds
reference images in the same token space as text, so likeness + clothing hold
through the style transfer. This tool replicates that on free backends.

## Usage
```bash
# reference-driven (the ChatGPT method):
python3 gen.py --ref photo.jpg \
  --prompt "South Park version, hold likeness and clothing" \
  --output out.png

# stronger re-render:
python3 gen.py --ref photo.jpg --prompt "..." --output out.png --denoise 0.85

# generate-and-pick: 2+ backends in parallel, best-scored wins
python3 gen.py --ref photo.jpg --prompt "..." --output out.png --pick

# text-only fallback (no reference):
python3 gen.py --no-ref --prompt "..." --output out.png
```
Exit codes: 0 = PASS, 2 = verification FAIL (output still written), 1 = backends dead.

## Backends (all free) — see backends_free.py
| backend | mode | verdict 2026-10-11 |
|---|---|---|
| ai_horde | img2img, denoise 0.55–0.85 | THE workhorse. Free, ~90s–3min typical. Holds composition; likeness gated by verification. |
| hf_qwen | Qwen-Image-Edit Space | Best quality when free GPU quota is up; quota exhausts fast, fails fast. |
| pollinations | text-to-image only | Last resort. Free flux ignores image input; may watermark. Anime drift observed. |

## The differentiator
`--pick` scores every candidate with sensorium `style_hold` + face-ROI
likeness-vs-reference, returns the best. Combined + self-judging. The face
check FAILs drifted outputs — commercial tools hand those back as "done."

## Heavy-duty path
`notebooks/self_hosted_qwen_kontext.md` — run Qwen-Image-Edit / FLUX.1-Kontext
on free Kaggle/Colab GPUs. Unmetered, no queues.

## Sharing
Backend + verification code adapted from `tools/image-edit/ai_edit.py`
(PR #172, free-ai-edit). When both land, converge on `backends_free.py`.
