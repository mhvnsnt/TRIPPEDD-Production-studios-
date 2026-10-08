# Viseme → mouth-shape reference (for animators)

Pipeline output visemes are **Preston Blair** mouth shapes — the same set
Rhubarb Lip Sync emits (A–H + X rest). Map each code to your character's
mouth sprite / blendshape pose.

| Code | Mouth shape | Description | Example sounds |
|------|-------------|-------------|----------------|
| A | AI | Jaw dropped, mouth wide open | *fire*, *see* |
| B | MBP | Lips pressed together | *baby*, *move* |
| C | E | Teeth slightly apart, relaxed | *everybody*, *session* |
| D | U | Lips rounded, small opening | *you*, *council* |
| E | O | Lips rounded, open | *or*, *more* |
| F | L | Tongue tip on upper teeth | *like*, *signal* |
| G | FV | Lower lip tucked under upper teeth | *fire*, *five* |
| H | WQ | Lips puckered / flat-ish | *bat*, *was* |
| X | REST | Closed, neutral | silence / pauses |

## Phoneme → viseme guide (syllables & vowels)

The pipeline emits **visemes directly** (mouth shapes), not phonemes — the
mouth-shape timeline is the proof artifact. For dialogue prep and spot-checking
("getting syllables and vowels for the mouths right"), this is the mapping
Rhubarb's Preston Blair set applies:

| Phoneme (IPA / Arpabet) | Viseme |
|--------------------------|--------|
| iː, ɪ (IY) | A |
| eɪ (EY), ɛ (EH), æ (AE) | C |
| aɪ (AY), ɔɪ (OY), aʊ (AW) | A (start) |
| ɑː (AA), ʌ (AH) | C |
| oʊ (OW), ɔː (AO) | E |
| uː (UW), ʊ (UH) | D |
| w (W), k (K), g (G), ʤ (JH), tʃ (CH) | H |
| m (M), b (B), p (P) | B |
| f (F), v (V) | G |
| θ (TH), ð (DH) | F |
| l (L), n (N), t (T), d (D), s (S), z (Z) | C |
| r (R) | D |
| y (Y) | C |
| h (HH) | X/H |

## Wave 2 extensions (whisper-align pipeline)

CMUdict emits four Arpabet phones the Wave 1 table did not list; the Wave 2
pipeline maps them into the same mouth classes (documented in
`whisper_align_to_timeline.py`):

| Phoneme | Viseme | Rationale |
|---------|--------|-----------|
| IH (ɪ) | A | same vowel class as the Wave 1 IY row |
| ER (ɝː) | C | mid-open relaxed, same class as EH/AE row |
| NG | C | nasal, same class as N |
| SH, ZH | C | sibilant fricatives, same class as S/Z |

## Notes for the episode pipeline

- Timeline JSON rows are gapless: `end[i] == start[i+1]`, first row starts at
  0.00 and the last row ends at the audio duration — drive the mouth sprite
  with the viseme whose `[start, end)` contains the current time.
- `X` = rest. Hold the neutral mouth sprite; don't animate through X.
- Long holds (>0.5s on one viseme) usually mean flat/robotic input audio
  (e.g. a TTS stand-in) — real voiced dialogue gives more movement. The
  timeline is still honest; prefer re-recording the VO over editing the cues.
- Sync check: overlay the JSON on the waveform — spoken words must fall
  inside non-X viseme spans; X spans must fall inside silence (see PROOFS).
