# proofs/ — Wave 4 TTS

## dac_roundtrip_COMPONENT_ONLY__NOT_TTS.wav (112,684 bytes, 1.28 s, 44.1 kHz)

**This is NOT a Zonos / Dia / VibeVoice generation. Do not present it as one.**

What it is: espeak-ng formant synthesis of "The block remembers." passed
through the Descript Audio Codec (`dac` 1.0.0, `44khz` model) — the neural
vocoder both Dia and Zonos use as their audio codec — encode → decode on CPU.

What it proves: the codec stage of the Dia/Zonos pipeline runs on this box's
CPU (2 cores). The transformer/diffusion stages could not run here (weights
exceed free disk and RAM — see `../PROOFS_WAVE4_TTS.md`).

Produced 2026-10-07 by `~/venvs/wave4-tts`. Re-verified on re-read: 1.28 s,
peak 0.905, has signal.
