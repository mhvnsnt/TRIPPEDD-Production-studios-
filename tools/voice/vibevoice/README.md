# VibeVoice (Microsoft) — long-form TTS wiring

- Upstream: https://github.com/microsoft/VibeVoice
- License: **MIT ✅ VERIFIED** from upstream repo (License: MIT License; checked 2026-10-07).
- ⚠️ **Upstream intent caveat (README, 2025-09-05):** "we have removed the VibeVoice-TTS code from this repository" after misuse was discovered; "We do not recommend using VibeVoice in commercial or real-world applications without further testing and development. This model is intended for **research and development purposes only**." MIT is commercial-safe by license, but wire per upstream's stated intent: **research/scratch use, badge clearly, never load-bearing**.
- Models: `microsoft/VibeVoice-1.5B` (long-form multi-speaker TTS — up to 90 min, up to 4 speakers), `microsoft/VibeVoice-Realtime-0.5B` (streaming, ~300 ms first-audio latency, ~10 min robust generation), `microsoft/VibeVoice-ASR-7B` (ASR, not TTS)
- What it is: next-token diffusion over continuous speech latents @ 7.5 Hz frame rate; LLM understands script/dialogue flow, diffusion head renders acoustic detail. Multi-lingual (EN/ZH+).

## Install recipe

```bash
python -m venv ~/venvs/wave4-tts && source ~/venvs/wave4-tts/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
git clone https://github.com/microsoft/VibeVoice.git
cd VibeVoice && pip install -e .    # NOTE: upstream removed the TTS inference
                                    # code — this gives you docs/ASR; see below
```

## Model download (weights)

```bash
# TTS weights are still published on Hugging Face even though the repo's
# TTS inference code was removed upstream:
huggingface-cli download microsoft/VibeVoice-1.5B        # ~3 GB
huggingface-cli download microsoft/VibeVoice-Realtime-0.5B  # ~1 GB
```

## Minimal run

⚠️ No official in-repo TTS inference script remains upstream (removed
2025-09-05). Community paths: third-party integrations (e.g. Esperanto's
`vibevoice` provider) or the HF demo/Colab. Wave-4 attempt documented in
`../PROOFS_WAVE4_TTS.md` — exact state of what runs from a clean clone.

```python
# Intended shape once an inference path is available (see upstream demo):
#   text in  ->  up-to-4-speaker long-form dialogue out
#   "[S1] The block remembers. [S2] Then let it speak."
```

## Hardware (upstream)

- GPU recommended for real-time; ASR-BitNet variant runs real-time on CPU
  (3+ threads) — TTS has no official CPU story.
- Wave-4 sandbox result: see `../PROOFS_WAVE4_TTS.md`.

## Voice-cast relevance

Built for long multi-speaker scripts (episodes, not lines): up-to-4 distinct
speakers with turn-taking and consistency across a script is the closest
documented match for full Wizard Gang ensemble scenes. Treat as
**research-only pending upstream intent change**; final VO must come from a
production-cleared engine. See `../VOICE_CAST_MAPPING.md`.
