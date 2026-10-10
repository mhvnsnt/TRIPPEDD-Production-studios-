# PROOFS.md — cartoon_sfx_kit (Wave 12 Lane A wire-up)

## What this tool is
`batch_sfx_kit.py` — batch orchestration + verification layer on top of the
repo's existing clean-room SFX donor (`tools/video_pipeline/sfx.py`:
numpy, public-domain algorithms). Per the repo AGENTS.md DONOR FIRST law,
no new synthesis code was hand-rolled — the donor recipes are used, not
duplicated. This tool renders the kit, re-reads every WAV, and fails loudly
on any format/content problem. No GPL/AGPL code anywhere in the chain.

## Proof of run (2026-10-07, this VM)
Command: `python3 batch_sfx_kit.py` → exit 0, "all WAVs verified"

- 12 WAVs rendered into `out/` — 820,786 bytes total
- Every file verified: 44100 Hz, mono, 16-bit, nonzero frames, audible peak
- `manifest.json` written with per-file SHA-256, duration, peak dBFS

| file | duration | peak |
|---|---|---|
| bell.wav | 0.800 s | −0.00 dBFS |
| blip.wav | 0.120 s | −0.01 dBFS |
| crowd.wav | 2.500 s | −0.92 dBFS |
| explode.wav | 1.100 s | −0.00 dBFS |
| fall.wav | 1.000 s | −0.11 dBFS |
| gunshot.wav | 0.300 s | −0.00 dBFS |
| hit.wav | 0.250 s | −0.00 dBFS |
| ko.wav | 0.900 s | −0.00 dBFS |
| pickup.wav | 0.180 s | −0.00 dBFS |
| riser.wav | 1.200 s | −0.28 dBFS |
| thud.wav | 0.350 s | −0.09 dBFS |
| whoosh.wav | 0.600 s | −0.00 dBFS |

## Honest notes
- The donor's `--all` renders 12 recipes (includes `ko.wav` beyond the 11
  named in its docstring); all 12 passed verification.
- WAVs are tool-generated (synthesized), so there is no third-party license
  to clear — output belongs to the pipeline per the tool-use doctrine.
- First smoke-test attempt failed (wrong repo-root depth in the script);
  fixed and re-run clean — the failure was in this wrapper, not the donor.
