# Wave 12 Lane B — BG-plate wire-up proofs

Per the repo's **DONOR FIRST** law, the wire-ups reuse the existing
`pull_plate.py` donor (Wave 10 Lane A) unchanged — no new downloader was
hand-rolled. Both pulls were smoke-tested 2026-10-07; plates stay in
`<outdir>/plates/` (not committed); only proof JSON + contact-sheet PNG
are committed.

## 1. TubeBacks — abstract ripples loop

- **Run:** `python3 pull_plate.py --url "https://www.tubebacks.com/static/preview/stock-video-blue-glass-ripples-loop--video-hd-34588.mp4" --source "TubeBacks (tubebacks.com)" --title "Blue glass ripples loop (HD preview)" --license "Royalty-free" --license-proof "https://www.tubebacks.com/stock-video/blue-glass-ripples-loop-video-hd-34588.html" --outdir proofs/wave12_tubebacks`
- **Result:** `PLATE_PULL_OK`
- **Proof:** `proofs/wave12_tubebacks/plate_proof.json`
  - 8.0 s, 320x180 h264, 953,972 bytes, sha256 `d0dd3bb0998f9a74…`
- **Frames:** `proofs/wave12_tubebacks/plate_contact_sheet.png` — **visually
  verified** (abstract dark-blue glossy ripple loop, 4 frames, real motion).
- **Why it matters:** TubeBacks is the strongest new find of the lane —
  motion-background loops with direct MP4 preview URLs, no signup for
  previews, and a royalty-free license quoted verbatim on the license page.

## 2. Open Beelden — archival CC remix clip

- **Run:** `python3 pull_plate.py --url "https://www.openbeelden.nl/files/19/20004.19991.!.mp4" --source "Open Beelden (Netherlands Institute for Sound and Vision)" --title "Untitled SD clip (StrangerFestival 2009 remix)" --license "CC BY-SA 3.0 NL (per-item; commercial use allowed with attribution + share-alike)" --license-proof "https://openbeelden.nl/api.en" --outdir proofs/wave12_openbeelden`
- **Result:** `PLATE_PULL_OK`
- **Proof:** `proofs/wave12_openbeelden/plate_proof.json`
  - 81.16 s, 320x240 h264, 11,485,241 bytes, sha256 `420167fa8babc6f7…`
- **Frames:** `proofs/wave12_openbeelden/plate_contact_sheet.png` — **visually
  verified** (video remix with projected light on a person in a white
  T-shirt, 4 frames, real footage).
- **Why it matters:** Open Beelden is the strongest archival find — Dutch
  Sound-and-Vision archive, every item under a CC license or public domain,
  direct MP4/OGV download links, and an OAI-PMH API for batch harvesting.
  Per-item license must be checked (this clip: CC BY-SA 3.0 NL, so
  derivatives carry attribution + share-alike).
