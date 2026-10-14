# Segment: Dangly's dino story (15s) — layered, editable, voice synced

This is ONE project. Edit it in place. Do not rebuild it from scratch.

```
segment-dino-story/
  timeline.json   ← the whole edit: video layers (piece, frames, x/y/scale/rot) + audio tracks
  layers/         ← mask-cut character pieces (from ../clean-cutouts), one PNG per piece
  bg/             ← background plates
  audio/          ← Dangly voice (range A drunk, 16-bit copy of voices/dangly/dangly_range_A_drunk.wav)
  render.py       ← timeline.json → out/segment.mp4 (python3 + Pillow + ffmpeg)
  edit.html       ← phone-friendly editor: scrub frames, drag layers with a finger, change scale/frame ranges, play with voice, save timeline.json
  out/segment.mp4 ← current render (15.000s, 1280×720, 24fps, voice + 2 hits)
```

**On mobile:** open `edit.html` from GitHub Pages / any static host, or run `python3 -m http.server` in this folder on the box and open it on the phone. Save → upload `timeline.json` with the GitHub app → `python3 render.py`.

## Frame types (fixes "the frames were never right")
| Type | Frames | Pieces |
|---|---|---|
| FACE | 0–215 | `oldhead_head.png` over the GOODVILLE sign. The head wobbles on the voice (South Park Canadian nod) with a stepped push-in. |
| BEER_HOLD | 216–247, 281–311 | `amos-jr/body_full.png` (the folded arm holds the BEER can in front of the torso). No punch arm is on screen. |
| PUNCH | 248–280 | `torso_no_arm.png` + head patch from `body_full.png` (kills the ghost double-eyes) + `arm_punch.png` flipped, attached at the viewer-left shoulder, fist + can into the dino head. The dino gets knocked back on frame 252. |
| END | 312–359 | end card |

Only one arm state is ever on screen, so the beer-hold arm and the punch arm never double up.

## Voice
`voice_dangly` starts at 0.30s and runs about 6.9s across the FACE shot. To recast (Tyneshia's read, or range B or C), drop the file in `audio/`, change `src`, and keep `start_s`. The hits are at 10.42s and 11.08s, on the punch frames.

## Proof
- `proof_contact_sheet.png`: frames 30, 120, 230, 252, 270 and 330 from the render.
- `proof_BEFORE_old_punch_frames.png`: the old smart_frames_fixed f0250 and dino_punch_final. Look for the hard torso cut, the ghost face and the smears.
- `proof_punch_attached.png`: the punch arm attached at the shoulder.

## Known gaps (honest)
- No lip flap yet. The kit has `old-head/mouth_*`, but the head is one piece. The next step is a jaw split on `oldhead_head.png`.
- The voice line text in `dangly_range_A_drunk.wav` was not machine-verified. Transcription failed on this box, so the owner needs to confirm it's the dino-story read.
- The old-head BODY source is a ghost image, so only the head is used. It needs a redraw from the key art.
- The dino is the flat scene piece. Its head does not detach yet.
