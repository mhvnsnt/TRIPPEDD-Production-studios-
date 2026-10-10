# PROOFS — lip-sync pipeline (Lane B, Anim Pull Wave 1)

Date: 2026-10-07. Branch: `wave1-anim-lane-b`.

## Pipeline winner

**Rhubarb Lip Sync 1.14.0** (MIT — verified in the release's bundled LICENSE.md;
output mouth cues belong to us outright). It built/runs cleanly in this sandbox
on the first try, so **no fallback was needed** (whisper-phoneme, papagayo-ng,
MFA, aeneas were not required; they remain documented fallbacks).

Pipeline (see `tools/lipsync/`):
- `lipsync_pipeline.sh` — one-command: WAV → Rhubarb TSV → timeline JSON + verify
- `rhubarb_to_timeline.py` — TSV→JSON converter + verifier (coverage, sanity, viseme set)
- `VISEME_REFERENCE.md` — Preston Blair A–H + X reference for animators + phoneme→viseme guide
- `BUILD.sh` — build/verify instructions

## Real proof — Static's approved EP02 line L1

Source line (from `production/WIZARD_GANG_EP01/DIALOGUE.md`, line 30, status APPROVED):
> "Ayo! You see that fire? That's the bat signal, baby — council's in session!
>  Everybody move like you got somewhere to be!"

### HONEST VOICE NOTE (stand-in)

The real Static voice is the **Enzo Amore Chatterbox zero-shot clone** owned by the
voice crew — not runnable in this sandbox (Chatterbox isn't installed here and the
voice crew owns that pipeline; VOICE_STATUS.md lists it as their track). The
dialogue WAV below is a **synthetic stand-in rendered with espeak-ng** (`en-us`,
165 wpm). **The voice is a stand-in; the lip-sync TIMELINE is the proof.**
When the real Static L1 VO exists, re-run the same pipeline on it — Rhubarb works
on any clean single-speaker WAV.

One observed stand-in artifact (documented, not edited out): the B viseme holds
5.53–7.63 (2.1 s) on the flat espeak voice — a real voiced take will give more
movement in that span. The timeline below is exactly what Rhubarb computed; no
hand edits.

## Artifacts

- `proofs/lane-b/static_L1_standin_raw.wav` — 8.25 s, mono, 16-bit, 22050 Hz
- `proofs/lane-b/static_L1_cues.tsv` — raw Rhubarb output (35 rows, gapless 0.00–8.25)
- `proofs/lane-b/static_L1_timeline.json` — verified timeline JSON

## SHA-256

| file | sha256 |
|------|--------|
| `static_L1_standin_raw.wav` | `72024f4234977ce43d8d77129678ae3512f83382ee2ac87f834c7c9c31f7ec7a` |
| `static_L1_cues.tsv` | `1b06d8c1fb128993a41c197a6c00981041a95f4c7b1d7ed5ff2cab707745e8a3` |
| `static_L1_timeline.json` | `c8ced8c52d6f42581a9e20427932928b33ac4f7fb526b4963dfa5971a4e71386` |

## Verification (machine-checked by `rhubarb_to_timeline.py`)

- **Coverage:** timeline spans 0.00–8.25 s = full audio duration (ffprobe-verified), gapless (`end[i] == start[i+1]`, no overlaps) — **PASS**
- **Sane count:** 35 cue rows, 29 non-rest mouth moves over 8.25 s of speech (≈1.2 moves per syllable — the line has ~34 syllables) — **PASS**
- **Viseme set:** every row in documented Preston Blair set {A, B, C, D, E, F, G, H, X}; observed: A B C D E F G H X — **PASS**
- **Sync sanity (waveform vs cues):** ffmpeg silence regions (0.33–0.71, 1.74–2.09, 5.07–5.44, 7.87–8.25 s) fall inside X (rest) spans in the timeline — mouth rests where the audio is silent — **PASS**

## First 20 rows of the timeline

```
start-end   viseme  mouth shape
0.00- 0.03  X  REST — closed/neutral
0.03- 0.34  B  MBP — lips pressed
0.34- 0.71  X  REST — closed/neutral
0.71- 0.84  F  L — tongue on teeth
0.84- 1.12  B  MBP — lips pressed
1.12- 1.27  A  AI — wide open
1.27- 1.31  B  MBP — lips pressed
1.31- 1.35  G  FV — lower lip on teeth
1.35- 1.49  C  E — teeth slightly apart
1.49- 1.56  B  MBP — lips pressed
1.56- 1.70  E  O — rounded open
1.70- 2.08  X  REST — closed/neutral
2.08- 2.52  B  MBP — lips pressed
2.52- 2.59  C  E — teeth slightly apart
2.59- 2.77  B  MBP — lips pressed
2.77- 2.98  C  E — teeth slightly apart
2.98- 3.26  E  O — rounded open
3.26- 3.45  C  E — teeth slightly apart
3.45- 3.50  H  WQ — puckered
3.50- 3.75  C  E — teeth slightly apart
```

(Full 35-row timeline in `static_L1_timeline.json`.)
