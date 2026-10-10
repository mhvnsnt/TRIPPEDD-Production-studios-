# EP02 Video Build — Visual Cut (2026-10-08)

**Output (Drive-canonical, NOT in git):** `Wizard Gang EP02 THE SUMMIT (visual cut, no dialogue).mp4`
Drive: https://drive.google.com/file/d/1U_uApZlItPoz7iEwEG1j0milOgrOyjBN/view?usp=drivesdk
Local: `production/WIZARD_GANG_EP01/wizard-gang-ep02-16x9.mp4` (122,519,627 bytes)

## Method
- **Image-to-video FROM the 29 approved stills** (`ep02-stills/ep02-shot-*.png`) — never fresh prompts.
- Motion: ffmpeg zoompan Ken Burns — slow push-in / pull-out / lateral drift, alternating per shot.
  Subtle Adult Swim grammar. **Zero likeness-drift risk** (no AI regeneration; stills are the frames).
- Shot durations per `EP02_SHOT_LIST.md`. 5s fog-wipe transition (26-1 → 27-1) per storyboard S26
  ("fog wipe → fireworks over the rooftop") fills the 4:05–4:10 gap.
- Assembly: 50s pilot cold open (`wizard-gang-pilot-16x9-v2.mp4`) UNCHANGED + 250s new show = **300.0s**.
- Full re-encode (libx264 medium, CRF 19, yuv420p), 1920x1080 30fps, AAC stereo, faststart (moov first).
- **NO dialogue/SFX/music** — owner approves all voices first. New-show portion carries silent audio;
  pilot keeps its original audio.

## Verification
- Duration 300.025s; full decode clean (exit 0, no errors); faststart confirmed (moov @36 < mdat).
- 16 spot-check frames across the timeline eyes-on verified: correct shot order, likeness intact.
- Segment durations all match shot list (29/29 + 5s transition).

## Notes
- One corrupt leftover segment from the dead coordinator (`seg-13-2.mp4`) was regenerated.
- `production/WIZARD_GANG_SHORT_01/` was missing from this checkout's working tree (removed by a
  concurrent process); pilot restored from the wave30 checkout (byte-identical, 23,991,008 bytes).
- Next: dialogue/voice sync pass AFTER owner approves all voices (Cipher, Bill $aber, Sombra pending).
