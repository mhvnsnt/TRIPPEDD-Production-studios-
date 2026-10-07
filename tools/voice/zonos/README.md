# Zonos (Zyphra) — zero-shot TTS wiring

- Upstream: https://github.com/Zyphra/Zonos
- License: **Apache-2.0 ✅ VERIFIED** from upstream repo (License: Apache License 2.0, root `LICENSE` file present; checked 2026-10-07) — commercial-safe.
- Model: `Zyphra/Zonos-v0.1-transformer` (also `Zyphra/Zonos-v0.1-hybrid`)
- What it is: 1.2B-param zero-shot TTS with speaker embeddings + fine-grained emotion/rate/pitch/quality conditioning; native 44 kHz output.

## Install recipe

```bash
# system dep (phonemization)
sudo apt install -y espeak-ng          # Ubuntu
# brew install espeak-ng               # macOS

python -m venv ~/venvs/wave4-tts && source ~/venvs/wave4-tts/bin/activate

# CPU torch (this box has no GPU; CPU inference is slow but supported
# upstream "provided there is enough free RAM")
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# the engine itself (pulls transformers, etc.)
pip install git+https://github.com/Zyphra/Zonos.git
```

## Model download (weights, ~3–4 GB)

```bash
python - <<'EOF'
from zonos.model import Zonos
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device="cpu")
print("loaded OK")
EOF
# weights land in ~/.cache/huggingface/hub/models--Zyphra--Zonos-v0.1-transformer
```

## Minimal run (CPU, short line)

```python
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

## Hardware (upstream)

- GPU: 6 GB+ VRAM (hybrid additionally needs a 3000-series+ Nvidia GPU); ~2x real-time on RTX 4090.
- CPU: supported with enough free RAM, "a lot slower ... likely won't be sufficient for interactive use".
- Wave-4 sandbox result: see `../PROOFS_WAVE4_TTS.md`.

## Voice-cast relevance

Strongest zero-shot likeness engine of the three: speaker embedding from a
10–30 s reference clip + explicit emotion dials (happiness/anger/sadness/fear),
speaking rate, and pitch variation — the best documented fit for per-character
voice identity (Bill $aber-deep Narrator, Enzo-style Static, etc.). See
`../VOICE_CAST_MAPPING.md`.
