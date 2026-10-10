# Dia (Nari Labs) — dialogue TTS wiring

- Upstream: https://github.com/nari-labs/dia
- License: **Apache-2.0 ✅ VERIFIED** from upstream repo (License: Apache License 2.0; README: "This project is licensed under the Apache License 2.0"; checked 2026-10-07) — commercial-safe by license.
- ⚠️ Upstream use disclaimer (README): "intended for research and educational use"; identity misuse, deceptive content, and illegal/malicious use are **strictly forbidden**. Respect it in the voice-cast lane.
- Model: `nari-labs/Dia-1.6B-0626` (1.6 B params; Dia2 also exists upstream)
- What it is: one-pass dialogue TTS — generates two-speaker `[S1]`/`[S2]` conversations with non-verbals ((laughs), (coughs), (sighs)…), audio-prompt voice cloning (5–10 s), emotion/tone conditioning. English-only.

## Install recipe

```bash
python -m venv ~/venvs/wave4-tts && source ~/venvs/wave4-tts/bin/activate

# CPU torch first so the dia install doesn't pull the CUDA wheel
pip install torch --index-url https://download.pytorch.org/whl/cpu

# the engine itself
pip install git+https://github.com/nari-labs/dia.git
```

## Model download (weights, ~3–6 GB)

```bash
python - <<'EOF'
from dia.model import Dia
model = Dia.from_pretrained("nari-labs/Dia-1.6B-0626", compute_dtype="float16")
print("loaded OK")
EOF
```

## Minimal run (short line)

```python
from dia.model import Dia
model = Dia.from_pretrained("nari-labs/Dia-1.6B-0626", compute_dtype="float16")
# Dialogue format: alternate [S1]/[S2]; start with [S1].
text = "[S1] The block remembers. [S2] Then let it speak. [S1]"
out = model.generate(text, use_torch_compile=False, verbose=False)
model.save_audio("proofs/dia_block_remembers.wav", out)
```

Or via HF transformers (`pip install git+https://github.com/huggingface/transformers.git`):

```python
from transformers import AutoProcessor, DiaForConditionalGeneration
proc = AutoProcessor.from_pretrained("nari-labs/Dia-1.6B-0626")
model = DiaForConditionalGeneration.from_pretrained("nari-labs/Dia-1.6B-0626")
outs = model.generate(**proc("[S1] The block remembers.", return_tensors="pt"),
                       max_new_tokens=1500, guidance_scale=3.0,
                       temperature=1.8, top_p=0.90, top_k=45)
proc.save_audio(proc.batch_decode(outs), "proofs/dia_block_remembers.wav")
```

## Hardware (upstream)

- Tested on GPUs only (PyTorch 2.0+, CUDA 12.6); **CPU support "to be added soon"** — expect CPU runs to fail or be unsupported upstream.
- Benchmarks (RTX 4090): ~4.4 GB VRAM @ bf16/float16, ~7.9 GB @ float32.
- Wave-4 sandbox result: see `../PROOFS_WAVE4_TTS.md`.

## Voice-cast relevance

The dialogue engine: two-speaker scenes (`[S1]`/`[S2]`) and non-verbals are a
natural fit for Wizard Gang banter (Static↔Cipher, Echo ad-libs). Voice cloning
via 5–10 s audio prompt can anchor recurring characters; the model is *not*
fine-tuned to a fixed voice, so fix the seed or reuse an audio prompt for
consistency. See `../VOICE_CAST_MAPPING.md`.
