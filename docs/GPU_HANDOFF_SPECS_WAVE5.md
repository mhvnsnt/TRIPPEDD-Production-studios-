# GPU Handoff Specs — Wave 5 (TRIPPEDD animated series)

**Date:** 2026-10-07 · **Author:** Wave 5 Worker B · **Status:** SPECS ONLY — nothing here was run on a GPU in this sandbox. Sandbox reality (verified 2026-10-07): no GPU (`nvidia-smi` absent), no CUDA, no torch preinstalled, ~7 GB RAM. Every license below was verified from the upstream LICENSE file or model card — never guessed. Every command is copied verbatim or paraphrased from upstream docs; where I only have third-party reports, that is labeled.

**Audience:** a GPU worker — the owner's machine or a rented GPU box — that will execute these handoffs.

---

## Spec 1 — Wan2.2-S2V talking-head test (audio-driven cinematic video)

### What it is
Wan2.2-S2V-14B (Alibaba Tongyi Lab) turns a **reference portrait + driving audio** (+ optional text prompt, + optional pose video) into a lip-synced cinematic character performance — portrait, bust, or full-body framing, 480p/720p. This is the talking-head / dialogue-scene engine for the Wizard Gang series.

### Upstream (verified 2026-10-07)
- **Code repo:** https://github.com/Wan-Video/Wan2.2 ⚠️ — the organization moved from `Wan-AI` to `Wan-Video`. `github.com/Wan-AI/Wan2.2-S2V` **does not exist (HTTP 404)** — do not clone that path.
- **Weights:** https://huggingface.co/Wan-AI/Wan2.2-S2V-14B (ungated, public)
- **Paper:** https://huggingface.co/papers/2508.18621 · **Project page:** https://humanaigc.github.io/wan-s2v-webpage
- **License:** ✅ **Apache-2.0 commercial-safe** — verified three ways: GitHub API reports `spdx_id: Apache-2.0` for `Wan-Video/Wan2.2`; the HF model card frontmatter says `license: apache-2.0`; the README usage section is the official Apache-2.0 release. Code + weights both Apache-2.0.
- **Release status:** FULLY RELEASED and usable. The upstream README todo list is all checked: inference code ✅, S2V-14B checkpoints ✅, ComfyUI integration ✅, Diffusers integration ✅ (2026-08-26 announcement). Free HF and ModelScope Gradio demos exist if the worker wants a zero-install smoke test first.

### VRAM requirements (verified)
| Path | Requirement | Source |
|---|---|---|
| Official single-GPU `generate.py` (S2V-14B) | **≥ 80 GB VRAM** (e.g. H100 80GB, A100 80GB) with `--offload_model True --convert_model_dtype` | Upstream README, "💡 This command can run on a GPU with at least 80GB VRAM" |
| Multi-GPU | 8× GPUs via `torchrun`, FSDP + DeepSpeed Ulysses (`--dit_fsdp --t5_fsdp --ulysses_size 8`) | Upstream README |
| Community low-memory path (ComfyUI, kijai ComfyUI-WanVideoWrapper) | **~32 GB peak** on an RTX 5090 (32 GB): ~420 s and ~31.9 GB peak per 77-frame audio chunk, chunks chained with `WanSoundImageToVideoExtend` (previous chunk's latent = motion reference), full audio muxed back at the end | Third-party production report (glad-labs/poindexter commit `91bff0b`, 2026-09-14 spike): "renders a lip-synced presenter from a portrait plus narration on the 5090 (identity, light and background held for the whole chunk, photoreal and flat-vector alike)" |
| Cheap cards | Not viable for 14B. Consider Wan2.1 S2V alternatives or LTX-style pipelines instead (separate spec) | — |

> Honest note: there is **no smaller S2V checkpoint** (no 1.3B/5B S2V). If the worker only has a 24 GB card, the ComfyUI route with aggressive offload/quantization is the documented community path — but budget a full day for setup and expect chunk-boundary drift on long audio.

### Exact commands for the GPU worker
```bash
# 1. Clone (CORRECT org) and install
git clone https://github.com/Wan-Video/Wan2.2.git
cd Wan2.2
pip install -r requirements.txt   # torch >= 2.4.0; install flash_attn LAST if it fails

# 2. Download weights (~large — see §4 environment checklist for disk)
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B

# 3. Talking-head test (official single-GPU command, verbatim from upstream README)
python generate.py --task s2v-14B --size 1024*704 \
  --ckpt_dir ./Wan2.2-S2V-14B/ \
  --offload_model True --convert_model_dtype \
  --prompt "Summer beach vacation style, a white cat wearing sunglasses sits on a surfboard." \
  --image "examples/i2v_input.JPG" \
  --audio "examples/talk.wav"
# Without --num_clip, output length auto-adapts to the audio length.

# 4. Pose + audio driven variant (8-GPU example; --pose_video guides body motion)
torchrun --nproc_per_node=8 generate.py --task s2v-14B --size 1024*704 \
  --ckpt_dir ./Wan2.2-S2V-14B/ --dit_fsdp --t5_fsdp --ulysses_size 8 \
  --prompt "a person is singing" --image "examples/pose.png" \
  --audio "examples/sing.MP3" --pose_video "./examples/pose.mp4"
```

### Input contract (series use)
- `--image`: a **wizard character still** (PNG/JPG). Output aspect ratio **follows the input image** — use a 16:9 or 9:16 still depending on delivery format. Character should face the camera, unobstructed face.
- `--audio`: driving **WAV** (16-bit PCM, 16–44.1 kHz; the README example uses `talk.wav`). Length sets the output length; keep test clips **10–30 s** (longer runs accumulate visual drift per upstream/third-party notes).
- `--prompt`: scene/motion direction, e.g. `"Wizard Gang dialogue scene: Pablo leans on the alley wall, neon sign flickering behind him, subtle head nods as he speaks."`
- `--size`: pixel *area* (e.g. `1024*704`); aspect follows the image.
- `--num_clip`: optional clip-count cap for quick previews.

### Expected outputs
- MP4 (480p or 720p) with audio muxed, duration ≈ audio duration.
- Lip movement synced to the audio; identity, lighting, and background stable across the clip.

### How to verify the result (worker checklist)
1. File exists and plays: `ffprobe -v error -show_streams out.mp4` → shows one video + one audio stream.
2. Duration within ±1 s of the input audio duration.
3. Extract first/middle/last frames (`ffmpeg -i out.mp4 -vf "select='eq(n\,0)+eq(n\,150)+eq(n\,299)'" -vsync vfr check_%d.png`) and eyeball: same face/identity across frames, mouth actually moves (not a static image), no melting hands on close-ups.
4. Report back: GPU model, VRAM peak (from `nvidia-smi` log), seconds per generated second, any drift notes.

---

## Spec 2 — Real voice synthesis: Zonos / Dia / VibeVoice

Purpose: character dialogue VO for the series (wizard cast lines). All three licenses verified 2026-10-07 from upstream LICENSE files and model cards.

### 2a. Zonos (Zyphra) — ✅ Apache-2.0 commercial-safe

- **Upstream:** https://github.com/Zyphra/Zonos · **License:** Apache-2.0 — verified from the repo LICENSE file AND the HF model card (`license:apache-2.0`, ungated) for both checkpoints. Commercial use permitted.
- **Checkpoints:** `Zyphra/Zonos-v0.1-hybrid` (0.6B hybrid backbone — needs an Nvidia 3000-series or newer) and `Zyphra/Zonos-v0.1-transformer` (1B transformer). Native 44 kHz output. Zero-shot voice cloning from a 10–30 s speaker sample; emotion/speaking-rate/pitch controls; multilingual (en, ja, zh, fr, de).
- **VRAM (upstream README):** 6 GB+ VRAM on GPU. **CPU possible** "provided there is enough free RAM" (much slower, not interactive) — the only model in this spec with an honest CPU path.
- **System deps:** `espeak-ng` must be installed (`apt install espeak-ng`).
- **Worker commands (verbatim from upstream README):**
```bash
# install
pip install -e .            # from cloned repo, or
uv run gradio_interface.py  # recommended for repeated sampling (keeps model loaded)

# minimal python API (verbatim, choose ONE model line)
import torch, torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device

model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-hybrid", device=device)
# model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

wav, sampling_rate = torchaudio.load("assets/exampleaudio.mp3")
speaker = model.make_speaker_embedding(wav, sampling_rate)

cond_dict = make_cond_dict(text="Hello, world!", speaker=speaker, language="en-us")
conditioning = model.prepare_conditioning(cond_dict)
codes = model.generate(conditioning)
wavs = model.autoencoder.decode(codes).cpu()
torchaudio.save("sample.wav", wavs[0], model.autoencoder.sampling_rate)
```
- **Sample series prompts:** `make_cond_dict(text="They sealed the alley with their own shadows. Nobody walks out the same.", speaker=speaker, language="en-us")` — happy/angry/fearful variants via the emotion conditioning in the Gradio UI.
- **Upstream benchmark (cite):** real-time factor ~2× on RTX 4090 (README "Features").
- **Verify:** `ffprobe sample.wav` → 44.1 kHz PCM; listen to first 3 s; check the speaker sample's identity carries over; report RTF on the worker's card.

#### Sandbox attempt (honest result — pending)
Attempted in this sandbox: CPU-only synthesis of a ~3 s line with Zonos-v0.1-hybrid. Environment facts: no GPU; espeak-ng present (`/usr/bin/espeak-ng`, v1.51); PEP 668 blocked system pip so a venv was used; torch CPU wheel install in progress. ~7 GB total RAM, ~2 GB free — marginal for a 0.6B bf16 model (~1.2 GB weights + activations). Result recorded below when the run finishes. **If it OOMs or times out, that is the documented outcome — no audio artifact will be fabricated.**

### 2b. Dia (nari-labs) — ✅ Apache-2.0 commercial-safe

- **Upstream:** https://github.com/nari-labs/dia · **License:** Apache-2.0 — verified from the repo LICENSE file AND the `nari-labs/Dia-1.6B-0626` model card (`license:apache-2.0`). Commercial use permitted. ("To accelerate research, we are providing access to pretrained model checkpoints and inference code" — no non-commercial restriction in the license.)
- **Model:** Dia-1.6B-0626 (1.6 B) — **text-to-dialogue**: generates multi-speaker conversation from a transcript in one pass, with non-verbal tags `(laughs)`, `(coughs)`, etc. English only. This is the best fit for Wizard Gang **dialogue scenes** (two speakers, [S1]/[S2] tags).
- **VRAM (upstream benchmark table, RTX 4090):** ~4.4 GB (bfloat16/float16), ~7.9 GB (float32). Realtime factor ≈ 2.1× (bf16, compiled) / 1.5× (no compile).
- **Hard requirement:** "Dia has been tested on only GPUs (pytorch 2.0+, CUDA 12.6). **CPU support is to be added soon.**" → **CPU synthesis is NOT supported — do not attempt on CPU.**
- **Worker commands (verbatim from upstream README quickstart):**
```bash
# via transformers (install main branch first)
pip install git+https://github.com/huggingface/transformers.git
```
```python
from transformers import AutoProcessor, DiaForConditionalGeneration

torch_device = "cuda"
model_checkpoint = "nari-labs/Dia-1.6B-0626"

text = ["[S1] Dia is an open weights text to dialogue model. [S2] You get full control over scripts and voices. [S1] Wow. Amazing. (laughs) [S2] Try it now on Git hub or Hugging Face."]
processor = AutoProcessor.from_pretrained(model_checkpoint)
inputs = processor(text=text, padding=True, return_tensors="pt").to(torch_device)

model = DiaForConditionalGeneration.from_pretrained(model_checkpoint).to(torch_device)
outputs = model.generate(**inputs, max_new_tokens=3072, guidance_scale=3.0, temperature=1.8, top_p=0.90, top_k=45)
outputs = processor.batch_decode(outputs)
processor.save_audio(outputs, "example.mp3")
```
or `pip install git+https://github.com/nari-labs/dia.git` and use the repo directly.
- **Sample series prompt:** `"[S1] They sealed the alley with their own shadows. [S2] Then we unseal it. (laughs) [S1] Nobody walks out the same."`
- **Generation guidelines (upstream):** always start with `[S1]`; alternate `[S1]`/`[S2]` (never `[S1]`...`[S1]`); keep input 5–20 s of audio-equivalent; voice-clone prompts need a 5–10 s reference with a correct speaker-tagged transcript.
- **Verify:** duration sanity, both speakers audible and distinct, non-verbals present; report RTF and VRAM.

### 2c. VibeVoice (Microsoft) — 🚫 RESEARCH-ONLY per upstream terms (research lane only)

- **Upstream:** https://github.com/microsoft/VibeVoice · **Code license:** MIT — verified from the repo LICENSE file ("Copyright (c) 2025 Microsoft"). **This is NOT the whole story.**
- **Critical upstream facts (README, verified 2026-10-07):**
  1. 2025-09-05: **the VibeVoice-TTS code was REMOVED from the repository** ("We open-sourced VibeVoice-TTS… we have removed the VibeVoice-TTS code from this repository") after Microsoft "discovered instances where the tool was used in ways inconsistent with the stated intent." The long-form multi-speaker TTS variant (90-min, 4-speaker) **cannot be obtained from upstream anymore**.
  2. What remains: **VibeVoice-Realtime-0.5B** (streaming TTS) + VibeVoice-ASR models. HF: `microsoft/VibeVoice-Realtime-0.5B` (`license:mit`, ungated).
  3. The model card's **Responsible Usage** section states: "The VibeVoice-Realtime model is **limited to research purposes**"; "We do **not recommend using VibeVoice in commercial or real-world applications** without further testing and development… **intended for research and development purposes only**"; voice impersonation without explicit recorded consent is out-of-scope; every synthesized file gets an **audible AI disclaimer embedded** plus an imperceptible provenance watermark.
- **Verdict for the series:** 🚫 **research lane only — do NOT wire into shipping paths.** MIT code license does not override the research-only intended-use terms and the embedded audible disclaimer makes it unusable for finished episodes anyway. Catalog entry must carry the 🚫 badge.
- **If a research-lane test is still wanted:** follow the Colab (`demo/vibevoice_realtime_colab.ipynb`); expect the audible "generated by AI" disclaimer in output.

### 2d. Dia2 (nari-labs/dia2) — ✅ Apache-2.0 commercial-safe — NEW, catalogued in the Wave 5 appendix
- **Upstream:** https://github.com/nari-labs/dia2 · **License:** Apache-2.0 — verified from the repo LICENSE file (badge + text). Released 2025-11-19 per the Dia README update notice.
- **What:** streaming dialogue TTS (1B and 2B checkpoints: `nari-labs/Dia2-2B`) — starts generating as the first words arrive, conditionable on audio prefixes; up to 2 min English generation per run.
- **Worker quickstart (verbatim):** `uv sync`, then `uv run -m dia2.cli --hf nari-labs/Dia2-2B --input input.txt --cfg 6.0 --temperature 0.8 --cuda-graph --verbose output.wav` (CUDA 12.8+ drivers; CLI auto-selects CUDA else CPU, defaults bfloat16).

---

## Spec 3 — Wan 2.2 I2V (image-to-video) for wizard stills

### Upstream (verified 2026-10-07)
- **Code repo:** https://github.com/Wan-Video/Wan2.2 · **License:** ✅ **Apache-2.0 commercial-safe** (GitHub API `spdx_id: Apache-2.0`; HF frontmatter `license: apache-2.0`; Diffusers variants `-Diffusers`).
- **Checkpoints:** `Wan-AI/Wan2.2-I2V-A14B` (MoE: 27 B total, 14 B active per step) and `Wan-AI/Wan2.2-TI2V-5B` (dense 5 B, high-compression VAE 4×16×16). Also `Wan2.2-I2V-A14B-Diffusers` / `Wan2.2-TI2V-5B-Diffusers` for the diffusers path.
- **What changes vs Wan2.1:** MoE denoising experts, +83.2% more video training data, better motion + stylized-scene stability, reduced unrealistic camera movement (upstream README).

### VRAM tiers (verified)
| Model | Tier | VRAM / hardware | Runtime note | Source |
|---|---|---|---|---|
| I2V-A14B | datacenter / prosumer | Official single-GPU path uses `--offload_model True --convert_model_dtype`; expect **40–80 GB-class** cards for the stock command; community runs on 24 GB cards via ComfyUI + FP8/quantized + offload | minutes per 5 s clip; exact numbers are in the upstream `comp_effic.png` benchmark chart (image-only — read it in the README, do not trust third-party transcriptions) | Upstream README + community (kijai ComfyUI-WanVideoWrapper, DiffSynth-Studio "low-GPU-memory layer-by-layer offload, FP8 quantization") |
| TI2V-5B | consumer GPU | **RTX 4090-class (24 GB)** | **5 s 720p @24 fps in under 9 minutes** on a single consumer GPU (no special optimization) | Upstream README, verbatim |
| ComfyUI path | any 12 GB+ | Native ComfyUI integration (docs.comfy.org tutorials/video/wan/wan2_2) | community benchmarks vary | ComfyUI docs |

### Exact CLI for the GPU worker (verbatim from upstream README)
```bash
git clone https://github.com/Wan-Video/Wan2.2.git && cd Wan2.2
pip install -r requirements.txt   # torch >= 2.4.0; flash_attn LAST if it fails
huggingface-cli download Wan-AI/Wan2.2-I2V-A14B --local-dir ./Wan2.2-I2V-A14B
# or the 5B: huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B

# Image-to-video (official command, verbatim):
python generate.py --task i2v-A14B --size 1280*720 \
  --ckpt_dir ./Wan2.2-I2V-A14B --offload_model True --convert_model_dtype \
  --image examples/i2v_input.JPG \
  --prompt "Summer beach vacation style, a white cat wearing sunglasses sits on a surfboard. ..."

# 5B text+image-to-video variant:
python generate.py --task ti2v-5B --size 1280*720 \
  --ckpt_dir ./Wan2.2-TI2V-5B --offload_model True --convert_model_dtype --t5_cpu \
  --image <still> --prompt "<motion prompt>"
```

### Input contract (wizard stills)
- `--image`: the wizard **key-art still** (PNG/JPG, 720p-ish). Output aspect follows the still; deliver 1280×720 for episodes, 720×1280 crops for vertical promos.
- `--prompt`: motion + cinematography direction, referencing the still's content, e.g.: `"The robed wizard turns slowly toward camera, neon alley signs flicker behind him, embers drift upward, cinematic dolly-in, dark fantasy film still come alive."`
- `--size`: e.g. `1280*720` (area; aspect follows image).
- Keep camera-motion words conservative ("slow dolly-in", "subtle") — I2V hallucinates on aggressive moves.

### Expected output specs
- MP4, 480p or 720p, 24 fps, ~5 s default clips (chainable for longer).
- Verify: `ffprobe` stream check; first/last frame identity match against the input still (open both PNGs side by side — do not eyeball the video thumbnail alone); motion present but character design unchanged; report GPU/VRAM/seconds-per-clip.

---

## Spec 4 — GPU-worker environment checklist

### Base environment
| Item | Requirement | Why |
|---|---|---|
| OS | Ubuntu 22.04/24.04 (Linux) | Wan2.2 + Zonos READMEs; Zonos notes a community Windows fork exists but Linux is the tested path |
| Python | 3.10+ (venv or conda) | all four specs |
| CUDA | **12.6+** (Dia hard requirement); **12.8+** recommended (Dia2 quickstart); torch ≥ 2.4.0 | Wan2.2 README: "Ensure torch >= 2.4.0"; flash_attn install LAST if it fails |
| PyTorch | CUDA build matching the driver | `python -c "import torch; print(torch.cuda.is_available())"` must print True |
| System pkgs | `espeak-ng`, `ffmpeg`, `git-lfs` | Zonos phonemizer; muxing/probing |
| HF auth | `huggingface-cli login` only if hitting gated repos — all repos in this spec are **ungated** | verified via HF API (`gated: False`) 2026-10-07 |

### VRAM minimums per task
| Task | Minimum VRAM | Notes |
|---|---|---|
| Wan2.2-S2V-14B (official CLI) | **80 GB** | single H100/A100 80GB, or 8×GPU FSDP+Ulysses |
| Wan2.2-S2V-14B (ComfyUI chunked) | **~32 GB** | RTX 5090: ~31.9 GB peak / 77-frame chunk (third-party report) |
| Wan2.2 I2V-A14B (official CLI) | 40–80 GB class | with `--offload_model`; community 24 GB via ComfyUI+FP8/offload |
| Wan2.2 TI2V-5B | **24 GB** | RTX 4090-class, consumer path |
| Zonos hybrid 0.6B / transformer 1B | **6 GB+** | hybrid needs 3000-series+; CPU fallback possible with ample RAM |
| Dia 1.6B | **~5 GB** (bf16 ~4.4 GB measured) | CUDA-only; no CPU support |
| Dia2 2B | 8–12 GB est. | CUDA 12.8+; CPU fallback exists in CLI but untested upstream |
| VibeVoice-Realtime-0.5B | ~4 GB est. | research lane only — low priority |

### Disk space (model download sizes)
| Model | Approx. download | How known |
|---|---|---|
| Wan2.2-S2V-14B | **~16.3 GB safetensors** (HF metadata `safetensors.total` = 16,295,755,609 B) + VAE/audio-encoder files — budget ~20 GB | HF API, verified 2026-10-07 |
| Wan2.2-I2V-A14B | ~16–20 GB (same MoE family as S2V; exact figure not pulled — confirm with `du -sh` after download) | estimate, labeled |
| Wan2.2-TI2V-5B | ~10–12 GB (5 B dense + high-compression VAE; HF safetensors total not returned by API) | estimate, labeled |
| Zonos-v0.1-hybrid | **1.65 GB** (HF: 1,651,820,416 B) | HF API, verified 2026-10-07 |
| Zonos-v0.1-transformer | **1.62 GB** (HF: 1,624,411,136 B) | HF API, verified 2026-10-07 |
| Dia-1.6B-0626 | **1.61 GB** (HF: 1,611,160,576 B) + Descript Audio Codec (downloaded on first run) | HF API, verified 2026-10-07 |
| Dia2-2B | ~4 GB + Mimi tokenizer (2 B bf16; first CLI run downloads weights) | estimate from param count, labeled |
| VibeVoice-Realtime-0.5B | **1.02 GB** (HF: 1,017,626,722 B) | HF API, verified 2026-10-07 |
| **Recommended free disk** | **≥ 100 GB** for the full set + workspace | — |

### Install commands (copy-paste)
```bash
# system
sudo apt update && sudo apt install -y espeak-ng ffmpeg git-lfs
# python env
python3 -m venv gpu && source gpu/bin/activate
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu126
# (cu126 for Dia's CUDA 12.6 floor; use cu128 for Dia2)

# Wan2.2
git clone https://github.com/Wan-Video/Wan2.2.git && cd Wan2.2 && pip install -r requirements.txt
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B

# Zonos
git clone https://github.com/Zyphra/Zonos.git && cd Zonos && pip install -e .

# Dia
pip install git+https://github.com/nari-labs/dia.git
pip install git+https://github.com/huggingface/transformers.git   # main branch, for hf.py path

# Dia2 (uv)
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/nari-labs/dia2.git && cd dia2 && uv sync
```

### Estimated runtimes (upstream-cited — do not invent others)
| Task | Runtime | Source |
|---|---|---|
| S2V-14B, 77-frame chunk | ~420 s on RTX 5090 | glad-labs/poindexter commit 91bff0b (third-party, 2026-09-14) |
| TI2V-5B, 5 s 720p@24fps | < 9 min on single consumer GPU | Upstream README, verbatim |
| Zonos synthesis | ~2× real-time on RTX 4090 | Upstream README ("generates 2 seconds of audio per 1 second of compute") |
| Dia 1.6B | ~2.1× real-time (bf16+compile) on RTX 4090 | Upstream README benchmark table |
| I2V-A14B | see upstream `comp_effic.png` chart in the README | image-only upstream benchmark — read it on the GPU box |

### Worker acceptance checklist (per task)
1. Environment verified: `nvidia-smi` shows expected VRAM; torch CUDA available; espeak-ng present.
2. Model SHA / download completed without truncation (`huggingface-cli` resume-safe).
3. Test artifact produced: video (S2V/I2V) or wav (TTS) with `ffprobe`-verified streams.
4. Spot-check frames/audio opened and eyeballed — "rendered" is not "verified".
5. Report: GPU model, peak VRAM, wall-clock time, exact command, artifact path + SHA-256, anomalies (drift, identity slip, mis-sync).
