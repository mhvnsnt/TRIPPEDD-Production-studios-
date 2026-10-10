# Luck of the Irish v3 — METHODS

Honest provenance record for the v3 commercial pipeline. Written 2026-10-10.
No marketing language: what follows is what was actually done, including
what was *not* done.

## 0. What v3 is

A 56.5s commercial. A→B→C edit of the owner's real phone footage with
production audio, then a part-by-part cartoon transformation (eyes → ears →
grin → tracksuit → 80%-leprechaun at the jump), a freeze frame completing to
100% mascot, green iris, 2D swap card, title card, slogan card, one
disclaimer, end button. The transformation is the only AI-assisted section;
everything else is footage, cards, and authored effects.

## 1. Transformation keyframes — AI image-edit, NOT hand-drawn

The five transformation stages (`v3/keys/s1-eyes.png` … `s5-jump80.png`,
plus `s0-clean.png`) were made with the `media.generate_image` AI image-EDIT
model. Each was prompted as an edit of a real frame of the owner's footage
("edit this photo into a hand-drawn cartoon transformation stage"), keeping
his pose, body position, and the motel background.

**Plain truth:** they are AI-generated images *in a hand-drawn cartoon
style*. They are not literally hand-drawn. The raw model outputs are
preserved next to the finals (`keys/media-generation-v3-*.webp` with their
`.json` generation records), so anyone can see exactly what the model
produced.

**Correction of the record:** the build brief called for a hand-correction
pass on each keyframe (hands, face, proportions). Pixel-diffing the finals
against downscaled raw outputs shows s1–s4 are unchanged apart from resize
to 640×360 (mean abs diff < 1.1/255 — resampling noise only). The
"correction" that actually happened was *selection*: several generations
were made per stage (see the superseded `k1/k2/k3` three-stage attempts in
`keys/`) and the best take was kept. `s5-jump80.png` has no preserved raw
source — its generation record was not saved. That is a provenance gap.

## 2. Motion propagation — EbSynth (non-generative)

EbSynth is a real open-source tool. It is optical-flow based and
non-generative: it warps the painted keyframe's pixels along the motion it
measures in the source video. No diffusion, no morphing, no invented frames.

`v3/ebs/run_all_ebsynth.sh` runs five segments (`segA`–`segE`), one per
transformation stage, at 640×360 / 8 fps via
`~/workspace/video-fix-tools/ebsynth/run_ebsynth.py`:

| seg | timeline    | keyframes              |
|-----|-------------|------------------------|
| A   | t22.9→25.0  | clean → S1 eyes        |
| B   | t25.0→27.0  | S1 → S2 ears           |
| C   | t27.0→29.0  | S2 → S3 grin           |
| D   | t29.0→31.5  | S3 → S4 tracksuit      |
| E   | t31.5→t33.5 | S4 → S5 jump (80%)     |

CPU-bound, ~45s/frame. Styled frames kept in `segX/styled-frames/`.
This is why the transformation follows his real movement: the motion is
his, from the footage; only the painted look is transferred.

## 3. Cartoon FX — authored vs generated, per asset

- **Flash frames** (`v3/fx/flash_white.png`, `flash_green.png`): flat
  full-frame color plates, faded in/out in ffmpeg. Authored.
- **Speedlines** (`v3/fx/speedlines.png`): static plate, overlaid during
  the jump hold. Authored.
- **Starburst / poof pop clips**: the 15-frame scale-up animations were
  built procedurally in PIL from `fx/starburst.png` / `fx/poof.png`
  (`assemble_v3.py` step 3). The plates themselves came from earlier build
  stages (exact origin not recorded — gap). The *animation* is authored;
  the plates' origin is not fully documented.
- **Pop-clip encoding fix:** the h264 `yuva420p` clips lost their alpha
  (decoders rendered black boxes), so they were re-encoded as qtrle `.mov`
  and overlaid as RGBA. Verified clean by eye.
- **Freeze poof:** the first version whited out the frame at 1.7× scale.
  It was hand-redrawn in PIL as a clean white cartoon smoke puff, capped
  at 1.1× scale with a 4-frame fade-out. Literally hand-made pixels.
- **100% mascot reveal** (`comp/mascot_reveal.mp4`): the reveal frame is
  an AI image-edit output (`keys/media-generation-v3-freeze-mascot-*.webp`,
  same hand-drawn-style prompting as §1). Its assembly into the reveal clip
  (poof burst → mascot hold) was done ad-hoc; the build command was not
  preserved in the scripts — gap.
- **Cards** (title, slogan, disclaimer, end button): typography on black,
  built with PIL/ffmpeg. Authored. The disclaimer card renderer
  (`v3/build_disclaimer_card.py`) is reusable for the rotation.

## 4. Assembly — `v3/assemble_v3.py` (11 steps)

1. Base 0→22.9s lifted from the v1 final (untouched footage + audio).
2. Beat clips built from clean frame ranges; part-beat timeline computed
   (`comp/v3-hittimes.txt` is the source of truth for hit times).
3. Starburst/poof pop clips (PIL, §3).
4. K3 hero hold: 1.5s zoompan punch-in on EbSynth segE's last styled frame.
5. Freeze: 0.3s hold of the same frame.
6. Poof: 0.4s hand-redrawn poof over the freeze.
7. Iris: mascot reveal → 2D swap card (`xfade circlecrop`, the clean
   geometric iris — no AI involved).
8. Base concat of all segments.
9. **HITS pass:** flashes, starbursts, poof, speedlines, and the
   tracksuit spin-morph gag at the computed hit times. The monolithic
   11-overlay ffmpeg graph was SIGKILLed by the sandbox (~10s, no OOM log),
   so it was rebuilt as **5 sequential passes** (`v3/run_hits_seq.py`),
   one hit per ffmpeg invocation (~2.5 min/pass, stable).
10. Audio (`v3/build_audio_v3.py`, 91 lines): production bed from v1's
    audio kept through the footage; synthesized riser 22.9→35s; numpy-built
    impact hits at each part-beat, poof burst, and reveal sting; cards
    near-silent; peak-normalized, no clipping. The `tmp-*.wav` files in
    `v3/` are the synthesized components.
11. Final mux: h264 + aac, `+faststart`.

**Disclaimer fix (post-build, same branch):** the 13-disclaimers-on-one-card
was replaced by a single large disclaimer per the owner's note. The new
card was spliced in with a stream-copy cut at the exact keyframe boundaries
(44.433333 / 52.433333) — transformation, audio, and all other cards are
bit-identical to the graded cut. Rotation state lives in
`v3/disclaimer-rotation.json` (v3 aired index 0; `next_index: 1`).

## 5. What "no AI slop" means for this cut

**Used — and allowed again:**
- AI *image edit* of the owner's own photographed body, as rotoscope
  plates in a cartoon style. Still images only, never video.
- EbSynth optical-flow propagation (non-generative by construction).
- Procedural/authored animation (PIL frame sequences, ffmpeg filters).
- Synthesized audio components from numpy + the production bed.

**Banned — the v2 failure modes, absent here:**
- AI face/body morph frames (no generative interpolation of his face or
  body at any point).
- Video-to-video generative passes over his performance.
- Generative fill or "AI transition" effects.
- A screen effect (the v2 green overlay) standing in for animation.

**The standard, in one sentence:** AI may paint the keyframes, but only
rotoscopy, optical flow, and hand/authored animation may move them —
nothing about his body is ever generated in motion.

## 6. Known gaps

- s5-jump80.png: raw generation source not preserved.
- fx/starburst.png, fx/poof.png: plate origins not recorded (their
  animation is authored; the plates' provenance is not).
- mascot_reveal.mp4: build command not preserved in scripts.
- The planned per-keyframe hand-correction pass did not happen on s1–s4
  (verified by pixel diff); selection was the actual QC.

## End-button rebuild (Porky-style sign-off) — 2026-10-10
- Replaced the t52.5→end "THAT'S THE IRISH, FOLKS." text card with a Looney-Tunes-ending-style gag:
  - **Rings plate**: drawn in PIL (build_endbutton.py) — concentric red/gold bullseye circles on near-black, 1920×1080. Drawn shapes, not lifted frames.
  - **Pop-up**: the 100% mascot sticker (rebuilt from fx/sticker/mascot-cutout-raw.png + 7px white die-cut border) scales 0→1 with easeOutBack overshoot bounce while rising 160px, over 15 frames.
  - **Timing** (121 frames @30fps = 4.033s): rings 0.8s → pop 0.5s → line 2.07s → hold 0.57s → hard cut to black (3 frames).
  - **Line**: "Th-th-that's the Irish, folks!" — **TEMP VOICE, PLACEHOLDER**: ElevenLabs "Callum - Husky Trickster" (characters_animation), eleven_v3 model, peak-normalized to -1.5dB. Raw take saved as endbutton-line-temp.mp3. SWAPPABLE for the owner's own voice — re-run the audio build step in build_endbutton.py with the new line file.
  - Splice: A=[0,44.466667) (video stream copy, 1334 frames exact; audio atrim+re-encoded AAC 128k to hit the exact boundary — transparent, higher bitrate than source) + W=[44.466667,56.533333) re-encoded (new disclaimer 241f + endseg 121f). Total 56.556s.
- **AI vs manual, precisely**: rings drawn by hand-authored code (PIL shapes); mascot pop animation is keyframed scaling of the AI-image-edit keyframe cutout (same provenance as the other keyframes); the VOICE is AI TTS (ElevenLabs) and is explicitly TEMP.

## Disclaimer-leak fix — 2026-10-10
- The earlier disclaimer splice left 5 frames (44.4667–44.6333s) of the OLD 13-disclaimers card flashing before the new single disclaimer. Found by dense frame extraction + white-pixel classification + own-eyes verification.
- Fixed by dragging the new single-disclaimer card backwards: the [44.466667, 52.5) window is now 100% the new card (241 frames from disclaimer-card-idx0.mp4 + 1-frame hold), hard-cut from the slogan card. Frame-by-frame QC confirms zero old-card frames.
