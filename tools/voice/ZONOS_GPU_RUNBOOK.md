# Zonos (Zyphra) — GPU handoff runbook (Wave 6 Worker B)

**Status:** SPEC ONLY — nothing in this file was executed on a GPU in this sandbox.
First real synthesis is the GPU worker's job. Do not fabricate audio.

**What it is:** Zyphra's 1.2B-param zero-shot TTS — speaker embedding from a
10–30 s reference clip + fine-grained conditioning (emotion, speaking rate,
pitch variation, audio quality). Native 44 kHz output. Primary casting engine
for the Wizard Gang cast (per `tools/voice/VOICE_CAST_MAPPING.md`).

**License:** ✅ Apache-2.0 commercial-safe (verified Wave 5 from upstream LICENSE
file and both HF model cards). Full legal read — Worker D, Wave 5:
`docs/VOICE_COMMERCIAL_USE_WAVE5.md` §1. **Caveat (process, not license):**
phonemization runs through eSpeak-NG (GPL-3.0, quarantine row 7) — invoke the
`espeak-ng` *binary* as a standalone tool, never link the library into shipping
paths. Note: Zyphra's follow-up model **ZONOS2** is a separate MIT model —
evaluate it separately, do not conflate it with v0.1.

**Upstream:** code https://github.com/Zyphra/Zonos · weights
`Zyphra/Zonos-v0.1-transformer` / `Zyphra/Zonos-v0.1-hybrid` (ungated, public).

---

## Hardware floor

| Item | Floor | Notes |
|---|---|---|
| GPU (VRAM) | **6 GB+ VRAM** (upstream README) | ~2× real-time on RTX 4090 per upstream |
| GPU (backbone) | **transformer = any CUDA card; hybrid = Nvidia 3000-series or newer ONLY** | hybrid uses mamba-ssm, whose selective-scan kernels are CUDA-only — **no CPU inference path for hybrid** (code-level blocker, not a resource one) |
| CPU synthesis | **DEFINITIVELY INFEASIBLE — DO NOT RETRY** | See § "CPU attempt history" below |

**CPU attempt history (why you must not retry):** Wave 5 documented a genuine
attempt — transformer weights downloaded (`curl -C -`, size-verified
3,248,848,864 B). `Zonos.from_local` loads the backbone as bf16 (~1.6 GB) but
**first materializes it in fp32 (~3.25 GB) then casts** — the transient
fp32+bf16 coexistence plus DAC/speaker-encoder overhead exceeded available RAM
and the kernel OOM-killed the process (**exit 137, SIGKILL**) during
`from_local`, before any audio was generated. Details:
`docs/GPU_HANDOFF_SPECS_WAVE5.md` § "Sandbox attempt" (spec 2a). CPU retry on
any RAM-constrained CPU-only machine will end the same way.

## Disk floor

Weights are small — **budget ~6 GB** (weights + HF cache + venv):

| Checkpoint | Size (corrected) | Method |
|---|---|---|
| `Zyphra/Zonos-v0.1-transformer` | **~3.25 GB** (3,248,848,864 B) | HTTP HEAD on the resolve URL, Wave 5 |
| `Zyphra/Zonos-v0.1-hybrid` | **~3.3 GB** (3,303,692,816 B) | HTTP HEAD, Wave 5 |

> ⚠️ Honest correction: the HF API `safetensors.total` figures (1.62 / 1.65 GB)
> were **~2× wrong**; the catalog was corrected in Wave 5. Do not budget 1.7 GB.

## Exact download commands

```bash
# System dep (phonemization — binary only per the GPL quarantine doctrine)
sudo apt install -y espeak-ng ffmpeg

# Env + install (GPU box: CUDA torch, not CPU torch)
python -m venv ~/venvs/zonos-gpu && source ~/venvs/zonos-gpu/bin/activate
pip install torch torchaudio          # CUDA wheel matching your driver
pip install git+https://github.com/Zyphra/Zonos.git

# Weights (ungated — no HF login needed)
python - <<'EOF'
from zonos.model import Zonos
# transformer = any CUDA card; hybrid needs a 3000-series+
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device="cuda")
print("loaded OK")
EOF
# weights land in ~/.cache/huggingface/hub/models--Zyphra--Zonos-v0.1-transformer
```

Alternative for repeated sampling (keeps the model loaded): `uv run gradio_interface.py`
from the cloned repo.

## Conditioning recipe — one wizard voice: Static

Static = Enzo Amore-style fast Jersey braggadocio. Zonos's documented strengths
are exactly Static's demands: speaking-rate control, pitch variation, and
high-energy emotion dials on top of a cloned speaker identity.

**Identity guard (non-negotiable):** the 10–30 s reference clip must be
**owner-supplied / explicitly consented audio** (owner, collaborator, or the
owner's own voice-talent performance). **Do NOT scrape Enzo Amore audio from
the internet** — identity-misuse laws apply regardless of the Apache-2.0
license, and the legal read (`docs/VOICE_COMMERCIAL_USE_WAVE5.md`) assumes
owned/consented reference audio for all casting.

```python
import torch, torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device   # cuda on the GPU box

model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

# 1. Speaker identity: 10-30 s CONSENTED reference clip
wav, sr = torchaudio.load("static_reference.wav")   # owner-supplied
speaker = model.make_speaker_embedding(wav, sr)

# 2. Static's conditioning: fast braggadocio = rate up, pitch lively, hot emotion
cond = make_cond_dict(
    text="You want the smoke? Come get it. Static's on the corner and the block remembers.",
    speaker=speaker,
    language="en-us",
    speaking_rate=20.0,          # > default (~15): fast Jersey delivery
    pitch_std=45.0,              # wide pitch swings for braggadocio energy
    emotion={"happiness": 0.8, "anger": 0.4, "sadness": 0.05,
             "disgust": 0.1, "fear": 0.05, "other": 0.2, "surprise": 0.3},
    vqscore_8=[0.78] * 8,        # audio-quality dials: keep high
    ctc_loss_weight=0.0,         # leave at default unless intelligibility drops
)
conditioning = model.prepare_conditioning(cond)

# 3. Generate + decode
codes = model.generate(conditioning)
wavs = model.autoencoder.decode(codes).cpu()
torchaudio.save("static_line01.wav", wavs[0], model.autoencoder.sampling_rate)
print("wrote static_line01.wav @", model.autoencoder.sampling_rate, "Hz")
```

Tune from there: `speaking_rate` 15–25, `pitch_std` 25–60, happiness/anger for
hotter reads; `make_cond_dict` exposes every dial — keep a log of the settings
per character in `tools/voice/zonos/` so takes are reproducible.

## Expected artifacts

- `static_line01.wav` — **44.1 kHz PCM** (Zonos's native output rate), duration
  roughly matching the text length at the chosen speaking rate (~4–6 s for the
  test line above).

## How the GPU worker verifies success

1. `ffprobe static_line01.wav` → 44100 Hz PCM; duration sane (>2 s, no truncation).
2. Listen to the full line: speech (not noise/music), intelligible, energy matches
   the conditioning (fast, lively — not flat narration).
3. Identity check: voice sounds like the reference speaker (same register/timbre
   family). If it sounds like a different person entirely, the embedding pipeline
   is broken — re-check the reference clip format.
4. `torchaudio.save` rate matches `model.autoencoder.sampling_rate` — no silent
   resampling mismatch.
5. Report back: GPU model, VRAM peak, seconds-per-generated-second (upstream
   claims ~2× real-time on a 4090 — report the measured number), and the exact
   `make_cond_dict` settings used.

## What stays blocked without a GPU (summary)

**Everything past weight download.** Transformer = RAM-blocked on CPU (exit 137,
documented); hybrid = CUDA-kernel-blocked (mamba-ssm has no CPU path).
Import/install wiring on a CPU box is proven; synthesis needs a CUDA card with
6 GB+ VRAM.
