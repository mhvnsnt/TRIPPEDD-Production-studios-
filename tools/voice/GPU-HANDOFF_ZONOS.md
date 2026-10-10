# GPU-HANDOFF — Zonos zero-shot TTS synthesis (Wave 7)

**Status: SPEC ONLY.** Nothing here has been executed on a GPU. This sandbox
has no CUDA card (`nvidia-smi` absent, no `/dev/nvidia*`), 7.9 GB RAM, and
4.8 GB free disk — Zonos synthesis is impossible on this box. Do not fabricate
audio. The CPU path is **definitively infeasible — DO NOT RETRY** (Wave 5:
OOM-137 / SIGKILL in `from_local`, before any audio; hybrid has no CPU kernels
at all — mamba-ssm is CUDA-only). Full recipe: `tools/voice/ZONOS_GPU_RUNBOOK.md`.

## GPU worker needs

| Item | Requirement |
|---|---|
| GPU | Any CUDA card, **6 GB+ VRAM** (transformer); hybrid needs Nvidia **3000-series+** |
| OS/packages | Linux, `espeak-ng` + `ffmpeg` via apt (phonemization — invoke the *binary* only; eSpeak-NG is GPL-3.0, never link the library into shipping paths) |
| Disk | **≥ 6 GB free** (weights ~3.25 GB transformer / ~3.3 GB hybrid, HTTP HEAD-verified 2026-10-07) |
| Network | huggingface.co reachable (repos are ungated — no HF login needed) |

## Commands

```bash
sudo apt install -y espeak-ng ffmpeg
python -m venv ~/venvs/zonos-gpu && source ~/venvs/zonos-gpu/bin/activate
pip install torch torchaudio          # CUDA wheel matching your driver — NOT the CPU wheel
# packaging note: stock pip install of Zyphra/Zonos is broken at upstream HEAD
# (setuptools include drops zonos/backbone/); shallow-clone, patch the include
# to ["zonos", "zonos.*"], then pip install --no-deps <clone>. See runbook.
huggingface-cli download Zyphra/Zonos-v0.1-transformer --local-dir ./Zonos-v0.1-transformer
```

Then run the Static test recipe in `ZONOS_GPU_RUNBOOK.md` (speaker embedding
from a 10–30 s **owner-supplied / consented** reference clip — never scraped
real-person audio; `make_cond_dict` with speaking_rate≈20, pitch_std≈45, hot
emotion dials; `generate` → DAC decode → `static_line01.wav`).

## Expected outputs

- `static_line01.wav` — **44.1 kHz PCM**, ~4–6 s for the test line.
- Verification: `ffprobe` → 44100 Hz, duration >2 s; **listen**: real intelligible
  speech, fast/lively energy, voice matches the reference speaker's register;
  `torchaudio.save` rate == `model.autoencoder.sampling_rate` (no silent resample).

## Proof artifacts to report back

GPU model · `nvidia-smi` peak VRAM · seconds-per-generated-second (upstream
claims ~2× real-time on a 4090 — report measured) · exact `make_cond_dict`
settings · the WAV's sha256.

## Licenses (verified 2026-10-07)

- Zyphra/Zonos code + weights: **Apache-2.0** (GitHub API `spdx_id`; HF cards
  `license: apache-2.0` on both `Zonos-v0.1-transformer` and `Zonos-v0.1-hybrid`).
- eSpeak-NG (phonemizer): GPL-3.0 — binary-only use; quarantine row stands.
- Upstream: https://github.com/Zyphra/Zonos · weights `Zyphra/Zonos-v0.1-transformer` /
  `Zyphra/Zonos-v0.1-hybrid`. ZONOS2 is a separate MIT model — evaluate separately.

## What unblocks after the smoke test

Wizard-cast voice casting lane (per `tools/voice/VOICE_CAST_MAPPING.md`):
Static, Cipher, Echo, Hollow, Sombra Negra, Kiko, Narrator, Theory, Onyx —
all still need owner-supplied/consented reference audio per character first.
No character lines are synthesized until the owner approves scripts.
