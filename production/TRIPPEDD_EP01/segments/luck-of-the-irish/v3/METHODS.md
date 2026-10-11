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

## Score upgrade + sign-off v2 — 2026-10-10 (owner direction, voice-transcribed)
Owner watched with sound and asked for: (1) a suspenseful horror-movie-style score
behind his dialogue and the buildup, (2) a Looney-Tunes/upbeat commercial bed after
the freeze frame, (3) a new sign-off read at 53s — "a leprechaun from the hood mixed
with the Lucky Charms leprechaun and Porky's voice." All music 100% original
numpy synthesis (build_v3_score.py) — zero samples, zero library music, safe for YouTube.

- **Suspense bed (0 → 34.5s)**: layered 55/55.7/82.4 Hz drone with slow LFO,
  dissonant minor-2nd string-ish swells (110/116.54/164.81/233.08 Hz additive,
  3s attack) at 4/12/20/28s, 48 BPM heartbeat pulse, and a 29.5→34.5s riser
  (150→1200 Hz sweep + rising noise) that HARD-CUTS to near-silence at the freeze
  frame (classic horror beat). Ducked under his dialogue: full duck (0.22 gain)
  wherever the production bed exceeds ~0.015 RMS, full bed in the gaps — dialogue
  stays on top, measured +10.4 dB over the bed in the 5–20s dialogue zone.
- **Upbeat bed (34.8 → 56.5s)**: original 132 BPM C-major cartoon/commercial groove —
  bouncy kick (1, 2&, 3, 4&), snare on 2/4, swung hats, I–V–vi–IV bass bounce,
  plucky triangle-ish original melody (2-bar call/response), offbeat chord stabs,
  ascending-run + big C-major tag with sparkle at the end. Fills the previously
  dead-silent 37–53.5s cards region. Ducked to 0.35 gain under the sign-off voice.
- **Sign-off voice**: the temp ElevenLabs read is PRESERVED as
  `audio/leprechaun-line-v1.wav` (clean vocal, converted from endbutton-line-temp.mp3 —
  verified byte-identical to the 53.96s placement in the pre-score cut). The new cut
  uses **v2**: `audio/leprechaun-line-v2.wav` = Piper `en_US-ryan-medium` (local neural
  TTS, free) reading "Th-th-th-that's the Irish, folks!" (stutter authored in text),
  pitch-shifted +3 semitones via rubberband for the cartoon lift, placed at 53.0s to
  land on the mascot pop-up (cross-correlation verified). v1 is never deleted —
  it stays on the branch so he can swap it back in.
- **Voice provenance note**: Chatterbox was the first choice but is not installed on
  this box and disk is at 86% (torch install not viable); Piper was the best local
  TTS available. The v2 read is a directed placeholder — still SWAPPABLE for the
  owner's own performance or a real voice-clone pass later.
- **Mix**: production audio untouched except the old temp-voice region (53.4→end)
  zeroed; peak-normalized to −1 dBFS, true peak −0.3 dBFS (no clipping). Video
  stream-copied, duration unchanged (56.53s).

## Mix rev2 — owner notes 2026-10-10 ~22:07 CDT (build_v3_score_rev2.py)
Rebuilt from the PRE-SCORE cut (git 402b1e42) — not layered on the scored cut.
1. **Base muted 17.0→20.0s** (camera person's "alright" removed); 100ms
   raised-cosine fades on mute edges, no clicks. Suspense bed continues under.
2. **Base boosted ×2.5 on 32.0→34.0s** ("luck of the Irish!" punches);
   100ms gain-envelope fades; peak in window 0.316→0.791 pre-norm.
3. **Suspense bed DOUBLED** (×2.0 mix gain). Duck floor lowered 0.10→0.05 in
   dialogue regions so the doubled bed never buries his voice (dialogue still
   clearly on top: measured +9.6 dB in the 10–12s zone). Riser (29.5→34.5) still
   rides at full gain EXCEPT a 0.6 dip under his 32–34s line (owner's own
   condition: "if 2x buries the 32-34s line, back the bed off slightly") —
   voice now +6.8 dB over the bed there (was −1.6 dB). Compromise noted.
4. **Upbeat bed UNCHANGED** (owner: "good where it is volume wise").
5. **v1 voice back in the cut** (owner: "v1 was better than v2 1000 percent").
   v1 sits at its natural ~53.27s spot in the base — nothing re-placed, nothing
   zeroed. v2 is OUT of the cut (verified ncorr 0.068 ≈ absent; v1 ncorr 0.871).
- **Mix**: peak-normalized to −1 dBFS, true peak −1.10 dBFS (no clipping).
  Video stream-copied (MD5-identical to pre-score), duration 56.555s unchanged.

## Standalone score-bed assets (owner asset-save add 2026-10-10)
- `audio/suspense-score-track-1.wav` — suspense bed at its FINAL doubled level
  (0→34.5s, clean, no dialogue/voice). "Track 1" numbering: more may come.
- `audio/luck_of_the_irish_commercial_track_music_score_jingle.wav` — upbeat bed
  (34.8→56.5s, clean). Owner's display name: **"luck of the Irish commercial
  track music score jingle"**.
Both exported at the final mix normalization level; reusable across the show.

## Voice asset admin
- `audio/leprechaun-line-v1.wav` — the ORIGINAL temp ElevenLabs read. IN THE CUT.
- `audio/leprechaun-line-v2.wav` — the Piper +3st directed read (former v2).
  Preserved; NOT in the cut.
- `audio/robot-porky-voice.wav` — byte copy of v2, per owner's naming
  ("save v2 voice as robot porky voice in the files"). Asset only.

## 2026-10-10 ~23:45 CDT — V-dip on suspense bed under "luck of the Irish!" (owner)
- For the exact 32-34s line duration: bed fades to -72dBFS at 33s (midpoint),
  back up to -24dBFS at 34s, release to natural by 34.4s. Voice untouched.
- Implemented in build_v3_score_dip.py (deterministic; absolute dB targets
  computed against the bed's own smoothed level to handle the riser crescendo).
- Verified on pure bed stem: drone hits -72dB @33s, -24dB @34s.
- Final: true peak -0.99dBFS, no clipping. Video stream untouched.
