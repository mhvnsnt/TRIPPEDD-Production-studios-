# Rhubarb vs Whisper-align — side-by-side comparison

- Rhubarb timeline: `proofs/lane-b/static_L1_timeline.json`
- Whisper-align timeline: `proofs/wave2/whisperx_upgrade/static_L1_whisper_timeline.json`

## Headline numbers

- Duration-weighted viseme agreement: **21.3%** (1.76s of 8.25s where whisper majority == Rhubarb viseme)
- Boundary MAE: Rhubarb boundary -> nearest whisper boundary = **56 ms** (n=34)

## Span counts

| metric | Rhubarb (acoustic) | Whisper-align (phone-derived) |
|---|---|---|
| timeline spans | 35 | 62 |
| non-rest moves | 29 | 56 |
| rest (X) coverage | 18.9% | 26.5% |
| longest single hold | 2.10s | 0.49s |
| mean hold | 0.24s | 0.13s |

## First 20 Rhubarb spans vs whisper majority

| start–end | Rhubarb | whisper majority | match |
|---|---|---|---|
| 0.00–0.03 | X | A | NO |
| 0.03–0.34 | B | A | NO |
| 0.34–0.71 | X | X | yes |
| 0.71–0.84 | F | D | NO |
| 0.84–1.12 | B | A | NO |
| 1.12–1.27 | A | C | NO |
| 1.27–1.31 | B | G | NO |
| 1.31–1.35 | G | G | yes |
| 1.35–1.49 | C | A | NO |
| 1.49–1.56 | B | C | NO |
| 1.56–1.70 | E | C | NO |
| 1.70–2.08 | X | X | yes |
| 2.08–2.52 | B | C | NO |
| 2.52–2.59 | C | B | NO |
| 2.59–2.77 | B | C | NO |
| 2.77–2.98 | C | A | NO |
| 2.98–3.26 | E | C | NO |
| 3.26–3.45 | C | X | NO |
| 3.45–3.50 | H | B | NO |
| 3.50–3.75 | C | A | NO |

## Reading the numbers

- Agreement <100% is expected: Rhubarb emits acoustic viseme boundaries while the whisper path emits word-anchored phone boundaries with proportional word-internal splits (documented approximation).
- Boundary MAE measures how far the two boundary sets sit from each other; sub-100ms MAE means the two engines broadly agree on *where* mouths change.
- The whisper path's value-add is not boundary precision but the attached words/phones (see `_meta.json`): animators can scrub by word, and the pipeline can re-target visemes per word without re-running audio.
