# Zonos (Zyphra) — zero-shot TTS wiring

- Upstream: https://github.com/Zyphra/Zonos
- License: **Apache-2.0 ✅ VERIFIED** from upstream repo (License: Apache License 2.0, root `LICENSE` file present; checked 2026-10-07) — commercial-safe.
- Model: `Zyphra/Zonos-v0.1-transformer` (also `Zyphra/Zonos-v0.1-hybrid`)
- What it is: 1.2B-param zero-shot TTS with speaker embeddings + fine-grained emotion/rate/pitch/quality conditioning; native 44 kHz output.
- **HARD CONSTRAINT (Wave 6, 2026-10-07): the CPU inference path is DEFINITIVELY INFEASIBLE — DO NOT RETRY.** Wave 5 documented a genuine attempt (`docs/GPU_HANDOFF_SPECS_WAVE5.md` § "Sandbox attempt"): transformer weights (3.25 GB) downloaded OK, but `Zonos.from_local` first materializes the backbone in fp32 (~3.25 GB) before casting to bf16 — transient fp32+bf16 coexistence + DAC/speaker-encoder overhead exceeded available RAM and the kernel OOM-killed the process (exit 137, SIGKILL) before any audio was generated. Hybrid has NO CPU path at all (mamba-ssm CUDA kernels). All real synthesis needs a CUDA card with 6 GB+ VRAM. See `ZONOS_GPU_RUNBOOK.md`.

## Install recipe

```bash
# system dep (phonemization)
sudo apt install -y espeak-ng          # Ubuntu
# brew install espeak-ng               # macOS

# NOTE (Wave 6): the stock `pip install git+https://github.com/Zyphra/Zonos.git`
# is BROKEN at upstream HEAD — upstream `pyproject.toml` `[tool.setuptools.packages.find]
# include = ["zonos"]` drops the `zonos/backbone/` subpackage (ModuleNotFoundError:
# No module named 'zonos.backbone'). Workaround: shallow-clone, patch the include to
# `["zonos", "zonos.*"]`, then `pip install --no-deps <clone>`. See `../PROOFS_WAVE4_TTS.md`.
# Real synthesis runs on the GPU box (recipe in ../ZONOS_GPU_RUNBOOK.md) —
# do NOT attempt on CPU (OOM-137, documented above).

python -m venv ~/venvs/zonos-gpu && source ~/venvs/zonos-gpu/bin/activate
```

## Model download (weights, ~3.25 GB transformer / ~3.3 GB hybrid)

```bash
# Preferred: huggingface-cli (ungated, no login) — download WITHOUT loading,
# so this step is safe on any box with ~4 GB free disk:
pip install "huggingface_hub[cli]"
huggingface-cli download Zyphra/Zonos-v0.1-transformer --local-dir ./Zonos-v0.1-transformer

# Do NOT do this on a CPU box (it loads the model and OOMs):
#   model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device="cpu")  # RETIRED — exit 137
```
# weights land in ./Zonos-v0.1-transformer
```

## Minimal run — RETIRED (CPU path infeasible)

The recipe below used `device="cpu"` and is **retired** — Wave 5 proved the
CPU load path OOMs (exit 137) before generating audio. Do not run it.
For the real test recipe, see `../ZONOS_GPU_RUNBOOK.md` (§ "Conditioning
recipe — one wizard voice: Static", `device="cuda"`).

```python
# (RETIRED — device="cpu" does not work; kept for reference only)
import torch, torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict

model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device="cpu")
wav, sr = torchaudio.load("assets/exampleaudio.mp3")   # any 10–30 s speaker sample
speaker = model.make_speaker_embedding(wav, sr)
cond = make_cond_dict(text="The block remembers.", speaker=speaker, language="en-us")
conditioning = model.prepare_conditioning(cond)
codes = model.generate(conditioning)
wavs = model.autoencoder.decode(codes).cpu()
torchaudio.save("proofs/zonos_block_remembers.wav", wavs[0], model.autoencoder.sampling_rate)
```

## Hardware (upstream + Wave 6 GPU verdict)

- GPU: 6 GB+ VRAM (hybrid additionally needs a 3000-series+ Nvidia GPU); ~2x real-time on RTX 4090.
- CPU: **NOT SUPPORTED — synthesis on CPU is definitively infeasible** (OOM-137 on transformer, Wave 5; no CPU kernel path for hybrid). Do not retry.
- Wave-4 sandbox result: see `../PROOFS_WAVE4_TTS.md`.

## Voice-cast relevance

Strongest zero-shot likeness engine of the three: speaker embedding from a
10–30 s reference clip + explicit emotion dials (happiness/anger/sadness/fear),
speaking rate, and pitch variation — the best documented fit for per-character
voice identity (Bill $aber-deep Narrator, Enzo-style Static, etc.). See
`../VOICE_CAST_MAPPING.md`.
