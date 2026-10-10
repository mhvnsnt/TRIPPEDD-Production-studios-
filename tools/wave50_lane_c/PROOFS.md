# Wave 50 Lane C — wire-up proofs (2026-10-08)

Two permissive-licensed tools wired with REAL runs. Both wire scripts are
original MIT-licensed code (this directory); external binaries/services are
invoked, never embedded.

Environment: Python 3.12.3 + numpy 1.26.4 (stdlib only otherwise),
ffmpeg 8.1.2 / ffprobe (Ubuntu build, `--enable-libass`), fontconfig with
1995 fonts (Noto family present). Network used only by tool 2 (archive.org).

## 1. ffmpeg ASS caption burn-in — production caption pipeline
- **Upstream:** ffmpeg (`ass` filter via libass 0.17.1) — invoked as an
  external binary, not embedded; this wire script itself is MIT.
- **License:** MIT (wire script). ffmpeg's own build flags include
  `--enable-gpl`; nothing is linked or embedded, the script only shells out,
  so no copyleft reaches the repo.
- **Script:** `wire_caption_burnin.py` — takes a clip + ASS, burns captions,
  verifies with ffprobe + frame-level pixel ground truth.
- **Proof (no network):** fully synthetic, deterministic static source.
  1. `testsrc` 10 s, 640x360@30fps + 440 Hz sine audio → `input_clip.mp4`.
  2. Authored `captions.ass`: 3 dialogue events (0.5–3.0 s, 3.5–6.0 s,
     6.5–9.0 s) with italic and `\c` color overrides, bottom-center style.
  3. Burn: `ffmpeg -vf ass=captions.ass` → `burned.mp4`. libass emitted
     zero error lines.
  - ffprobe: duration 10.008 s (expect 10 s), 640x360, audio stream present.
  - Pixel ground truth (rawvideo frames, subtitle band = lower third):
    - @1.5 s (caption ON): burned vs source mean|diff| = **7.03/255**
    - @9.5 s (caption OFF, last event ended 9.0 s): **0.51/255**
    - PASS rule: ON > 2.0 AND ON > 10x OFF, OFF < 1.0 → **PASS**
  - Frames eyeballed by the lane author: "BURN-IN PROOF LINE ONE" renders
    white-on-black-outline bottom-center @1.5 s; "Line three: red text"
    renders with red override text @7.5 s → **visual PASS**
- **Artifacts:** `proofs/caption_burnin/input_clip.mp4`,
  `proofs/caption_burnin/captions.ass`, `proofs/caption_burnin/burned.mp4`,
  `proofs/caption_burnin/frame_*.raw` (ground-truth frames),
  `proofs/caption_burnin/proof_frame_1_5s.png`,
  `proofs/caption_burnin/proof_frame_7_5s.png`,
  `proofs/caption_burnin/result.json`

## 2. pd_score_downloader — public-domain sheet-music fetch
- **Upstream:** Internet Archive advancedsearch + metadata + download APIs
  (open, no key). Wire script is original MIT code.
- **License:** MIT (wire script); the downloaded artifact is public domain.
- **Script:** `wire_pd_score.py` — searches archive.org, resolves metadata,
  downloads the score PDF, checks integrity, records provenance + SHA-256.
- **Proof (network):** one REAL PD score scan, identifier `carner_44_2181`:
  - Item: "Gladiolus Rag", Scott Joplin, published **1907** by
    Jos. W. Stern & Co. (archive.org metadata `date` field = 1907).
  - PD basis: US pre-1930 publication rule (published 1907); composer died
    1917, so life+70 also expired (1987). Provenance reasoning recorded for
    the catalog — not legal advice.
  - Download: `carner_44_2181.pdf`, **2,391,653 bytes** — byte-exact match
    with metadata-advertised size.
  - Integrity: magic `%PDF-1.5` OK; page count 6 (cross-checked with
    pdfinfo `Pages: 6` and the PDF `/Count 6`); SHA-256
    `1138be2ae94eb96548c686fa5ed9bb09d61bf5f5cbb3b629a3ae8baaa0d6ddfc`
    → **PASS**
- **Artifacts:** `proofs/pd_score/carner_44_2181.pdf` (2.3 MB),
  `proofs/pd_score/result.json`

### Honest corrections made during this lane (not failures)
- The page-count regex in `wire_pd_score.py` initially subtracted
  `/Type /Pages` matches from `/Type /Page\b` matches, but the page pattern
  never matches `/Pages`, so it reported 5 instead of 6. Fixed to a
  negative-lookahead pattern; pdfinfo and `/Count` both agree on 6.
- The libass stderr filter in `wire_caption_burnin.py` initially flagged
  informational libass API-version lines as "errors"; tightened to real
  error keywords (error/failed/cannot/unable). Clean run shows zero.

### Deferred (honest, not attempted to force)
- Broadcast-automation utility: no permissive candidate on the VM was both
  license-clear and runnable in this window; the two completed tools above
  satisfy the lane's 1–2 tool requirement. Candidates remain for a later lane.
