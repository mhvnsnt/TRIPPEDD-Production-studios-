# TRIPPEDD lipsync — Wan2.2-S2V (speech-to-video)

Alibaba Wan-AI speech-to-video: animates a still reference image from a driving
audio track (+ optional text prompt / pose video). Outputs 480p/720p cinematic
video at 24fps, length follows the audio. NOT just a talking-head lip-sync
tool — it does face, expression, body motion, camera and staging.

- Upstream: `Wan-Video/Wan2.2` (GitHub), weights `Wan-AI/Wan2.2-S2V-14B` (HF)
- License: **Apache-2.0** — verified in the upstream repo's `LICENSE.txt`
  (vendored excerpt under `upstream/`) AND on the HF model card
  (`cardData.license: apache-2.0` via HF API, 2026-10-07). Commercial-safe badge.
- Paper: `arXiv:2508.18621` — "Wan-S2V: Audio-Driven Cinematic Video Generation"

## Status

**BLOCKED-HONEST (sandbox: no GPU).** 14B-parameter model; the first-party
command targets **≥80 GB VRAM** single-GPU. Community VRAM-optimised forks
exist (e.g. `ighoshsubho/Wan2.2_S2V_Vram_optims`, Apache-2.0) for lower-VRAM
rigs. No fake generation attempted in this sandbox.

Verified in-sandbox: repo layout, `LICENSE.txt` (Apache-2.0), S2V CLI surface
in `generate.py`, `requirements_s2v.txt`, upstream HF model id + license,
official GPU compute table (`upstream/assets/comp_effic.png`).

## Install recipe (GPU worker)

```bash
# code
git clone https://github.com/Wan-Video/Wan2.2.git && cd Wan2.2
pip install -r requirements.txt
pip install -r requirements_s2v.txt
pip install "huggingface_hub[cli]"

# weights (~28 GB for bf16 14B; disk needed ~60 GB with cache)
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B
```

For TTS-generated driving audio the repo also integrates CosyVoice
(`requirements_s2v.txt` covers it) — that path adds a second license/rights
review (TTS voice identity), so prefer our own recorded/TTS-pipeline audio.

## Run (GPU worker)

```bash
python generate.py --task s2v-14B \
  --ckpt_dir ./Wan2.2-S2V-14B \
  --image <reference_portrait.jpg> \
  --audio  <dialogue.wav> \
  --prompt "<staging prompt, e.g. 'Summer beach vacation style...'>" \
  --size 720p --sample_steps 40
# output -> < Wan2.2 repo root >/s2v-14B_*.mp4  (length follows the audio)
```

## GPU-worker handoff spec

- VRAM: ≥80 GB single GPU (first-party command, e.g. H100/H20 80GB);
  multi-GPU via FSDP + DeepSpeed-Ulysses (`--ulysses_size 4/8 --dit_fsdp --t5_fsdp`).
- Reference points from the official compute table (A14B T2V/I2V, 81f @24fps):
  H100 480p ≈ 327s / 41 GB peak; 720p ≈ 1050s / 60 GB peak (single GPU).
  Expect S2V-14B in the same band (it shares the 14B backbone + wav2vec2
  audio encoder). Community forks claim reduced-VRAM S2V runs — re-measure on
  target hardware before quoting numbers.
- Weights: `Wan-AI/Wan2.2-S2V-14B` (~28 GB bf16); VAE is the Wan2.1-style VAE
  (`Wan2.1_VAE.pth` ships inside the repo).
- Audio: 16 kHz mono WAV works; any length (video follows audio; use
  `--num_clip` to cap clip count).
- Consent rule: the model can make a real person appear to speak — explicit
  consent + provenance review required before shipping generated likeness work.

## TRIPPEDD fit

Candidate for cinematic dialogue cutscenes / cartoon dialogue shots where a
full generated performance beats viseme-only puppetry. Heavier than Ditto;
use Ditto for realtime/interactive, Wan2.2-S2V for offline cinematic shots.
