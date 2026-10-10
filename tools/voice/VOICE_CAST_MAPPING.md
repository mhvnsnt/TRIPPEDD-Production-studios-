# VOICE CAST MAPPING — Wave 4 TTS engines × Wizard Gang 9-character cast

Date: 2026-10-07. Worker A, TRIPPEDD Resource Pull Program Wave 4.

> Basis: each engine's **documented** capabilities only (emotion control,
> speaker similarity, dialogue support, long-form). No likeness claims from
> untested synthesis. Character voice targets are the owner's stated
> likenesses; nothing invented.

## Engine capability summary (documented)

| Capability | Zonos (Zyphra, Apache-2.0) | Dia (Nari Labs, Apache-2.0) | VibeVoice (Microsoft, MIT) |
|---|---|---|---|
| Speaker similarity | ✅ Zero-shot cloning from 10–30 s reference; speaker embeddings | ✅ Audio-prompt cloning (5–10 s); **not** fine-tuned to a fixed voice — fix seed or reuse audio prompt for consistency | ⚠️ Multi-speaker (up to 4) with consistency across a script; preset voice embeddings (Realtime) |
| Emotion / style control | ✅ Explicit dials: happiness, anger, sadness, fear + speaking rate, pitch variation, audio quality; audio-prefix inputs (can elicit whispering) | ✅ Emotion/tone via audio conditioning; non-verbals: (laughs) (coughs) (sighs) (gasps) (screams) + 15 more | ✅ Expressive conversational dynamics, emotional nuance (documented, less granular than Zonos) |
| Dialogue support | Single-speaker utterances | ✅ **Two-speaker** `[S1]`/`[S2]` one-pass dialogue | ✅ **Up-to-4-speaker** conversations, natural turn-taking |
| Long-form | Line-level | ~5–20 s per generation (guideline) | ✅ **Up to 90 min** single pass (1.5B); ~10 min robust (Realtime-0.5B) |
| Output | 44 kHz native | 44.1 kHz (DAC) | 24 kHz class (codec @ 7.5 Hz frame rate) |
| Language | EN/JA/ZH/FR/DE | **English-only** | EN/ZH+ |
| Caveats | 6 GB+ VRAM rec.; CPU slow | GPU-only upstream; research-use disclaimer (no identity misuse) | **Research-only per upstream** — never load-bearing |

## Per-character assessment

### 1. Ashes / Narrator → Bill $aber deep narrator
- **Primary: Zonos.** The narrator needs one consistent deep voice across episodes; Zonos's speaker-embedding cloning from a 10–30 s Bill $aber-style reference + emotion dials (gravity, menace) is the strongest documented fit for a *fixed character identity*.
- **Secondary: VibeVoice-1.5B** for long narration passages (90-min single pass keeps narrator consistency) — research-only caveat applies; final VO must come from a production-cleared engine.

### 2. Static → Enzo Amore fast Jersey braggadocio
- **Primary: Zonos.** Fast braggadocio = speaking-rate control + high-energy emotion settings on a cloned reference. Rate/pitch dials are documented Zonos strengths.
- **Secondary: Dia** for banter scenes — non-verbals ((laughs), (scoffs)) suit Static's mouth.

### 3. Cipher → Lio Rush high-energy
- **Primary: Zonos** (energy via rate + pitch variation on a cloned reference).
- **Secondary: Dia** for Cipher↔Static two-speaker exchanges (`[S1]`/`[S2]`).

### 4. Echo → Shotzi Blackheart raspy punk
- **Primary: Zonos** (clone the rasp from a reference; emotion dials for punk attitude).
- **Secondary: Dia** — non-verbals are a natural fit for punk ad-libs ((laughs), (coughs), (screams)); audio-prompt cloning keeps her consistent within a scene.

### 5. Hollow → Super Dragon
- **Primary: Zonos** (straight cloning task; few special delivery demands documented).

### 6. Sombra Negra → Damian Priest deep menace
- **Primary: Zonos.** Deep menace = low pitch + anger/fear emotion settings; the **audio-prefix** input is documented to elicit whispering — a direct tool for menacing delivery.
- Note: Sombra Negra is male (canon-law binding) — reference audio must match.

### 7. Kiko → Keiji Mutoh theatrical
- **Primary: Zonos** (theatrical delivery via emotion + pitch-variation dials on a cloned reference).
- **Secondary: Dia** for theatrical non-verbals.

### 8. Theory → Black 20yo NY woman
- **Primary: Zonos** (clone from an approved reference; no invented voice — owner supplies or approves the reference).
- Note: Dia's "different voice every run" behavior makes it a poor primary for a fixed character unless seed/audio-prompt discipline is enforced.

### 9. Onyx → TBD
- **Unassigned.** Once the voice target is defined, **Zonos zero-shot** is the flexible default (no retraining; 10–30 s reference is enough to prototype).

## Scene-level routing (all three engines have a role)

- **Single lines / character-defining delivery → Zonos** (identity + emotion control).
- **Two-character banter, arguments, ad-libs → Dia** (`[S1]`/`[S2]` + non-verbals; keep one audio prompt per character per scene for consistency).
- **Ensemble scenes (3–4 speakers), episode-length scripts → VibeVoice-1.5B** (turn-taking + long-form coherence) — **research-only**; treat outputs as scratch until upstream intent changes or a production-cleared engine takes over.

## What this lane does NOT do

- No voice has been synthesized on this box (weights exceed sandbox disk/RAM — see `PROOFS_WAVE4_TTS.md`); this mapping is capability-based routing, not casting results.
- No real-person voice is cloned without permission — Dia's upstream disclaimer (no identity misuse) and the owner's canon law both bind here. Reference audio must be licensed/approved.
- Final shipped VO lines come from production-cleared engines (sherpa-tts lane is the current working offline path); Wave-4 engines graduate from scratch/research to shipping only after a real GPU-box smoke test.
