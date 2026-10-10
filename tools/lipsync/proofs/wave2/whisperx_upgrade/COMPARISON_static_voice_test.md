# Rhubarb vs Whisper-align — side-by-side comparison

- Rhubarb timeline: `proofs/wave2/whisperx_upgrade/static_voice_test_rhubarb_timeline.json`
- Whisper-align timeline: `proofs/wave2/whisperx_upgrade/static_voice_test_whisper_timeline.json`

## Headline numbers

- Duration-weighted viseme agreement: **23.8%** (3.08s of 12.93s where whisper majority == Rhubarb viseme)
- Boundary MAE: Rhubarb boundary -> nearest whisper boundary = **54 ms** (n=72)

## Span counts

| metric | Rhubarb (acoustic) | Whisper-align (phone-derived) |
|---|---|---|
| timeline spans | 73 | 98 |
| non-rest moves | 66 | 89 |
| rest (X) coverage | 14.2% | 23.0% |
| longest single hold | 0.68s | 0.56s |
| mean hold | 0.18s | 0.13s |

## First 20 Rhubarb spans vs whisper majority

| start–end | Rhubarb | whisper majority | match |
|---|---|---|---|
| 0.00–0.03 | X | X | yes |
| 0.03–0.18 | D | A | NO |
| 0.18–0.25 | B | X | NO |
| 0.25–0.67 | X | X | yes |
| 0.67–0.81 | F | E | NO |
| 0.81–1.09 | E | X | NO |
| 1.09–1.30 | F | X | NO |
| 1.30–1.58 | X | X | yes |
| 1.58–2.26 | B | C | NO |
| 2.26–2.40 | D | A | NO |
| 2.40–2.54 | B | H | NO |
| 2.54–2.61 | G | A | NO |
| 2.61–2.96 | B | X | NO |
| 2.96–3.06 | C | C | yes |
| 3.06–3.47 | B | C | NO |
| 3.47–3.82 | F | C | NO |
| 3.82–3.89 | B | C | NO |
| 3.89–4.03 | C | C | yes |
| 4.03–4.38 | F | D | NO |
| 4.38–4.51 | A | X | NO |

## Reading the numbers

- Agreement <100% is expected: Rhubarb emits acoustic viseme boundaries while the whisper path emits word-anchored phone boundaries with proportional word-internal splits (documented approximation).
- Boundary MAE measures how far the two boundary sets sit from each other; sub-100ms MAE means the two engines broadly agree on *where* mouths change.
- The whisper path's value-add is not boundary precision but the attached words/phones (see `_meta.json`): animators can scrub by word, and the pipeline can re-target visemes per word without re-running audio.
