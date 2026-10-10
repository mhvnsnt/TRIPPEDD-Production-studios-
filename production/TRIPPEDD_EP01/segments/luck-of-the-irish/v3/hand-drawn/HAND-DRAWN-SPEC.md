# Hand-Drawn Lane — Spec

The v3 pipeline is keyframe-agnostic: EbSynth propagates *any* painted
first frame, AI or human. This lane lets the owner's actual drawings drop
straight into the pipeline, replacing the AI-styled keyframes beat by beat.

## The deal

The quick transitional hits (eyes / ears / grin / tracksuit pops) can stay
AI-styled — they're on screen for a fraction of a second each. The **hero
frames** are where the audience actually studies the drawing, and those are
staged for hand-drawn replacement:

| Beat file              | What it is                              | Priority |
|------------------------|-----------------------------------------|----------|
| `hd-s5-jump80.png`     | 80%-leprechaun, mid-jump (the transformation peak) | HERO |
| `hd-freeze-mascot.png` | 100% mascot reveal (the freeze hold)    | HERO |
| `hd-s1-eyes.png`       | Eyes ignite green                       | optional |
| `hd-s2-ears.png`       | Elf ears pop                            | optional |
| `hd-s3-grin.png`       | Grin stretches cartoonish               | optional |
| `hd-s4-tracksuit.png`  | Clothes spin-morph to green tracksuit   | optional |

## Canvas spec

- **1920×1080 PNG.** Full frame, not a cutout.
- **Match the keyframe framing** in `v3/keys/`: same camera angle per
  beat. Reference frames: `keys/src-s1-t25.0.png`,
  `keys/src-s2-t27.0.png`, `keys/src-s4-t31.5.png`,
  `keys/src-freeze-t35.0.png` (the exact footage frames each keyframe was
  painted over). Draw the character at the same size/position in frame —
  EbSynth warps your drawing along the real motion, so framing match is
  what makes it sit correctly.
- Draw the *transformation state* for that beat (see table), not a
  generic portrait. The in-between motion is optical flow, not new
  drawing — one strong drawing per beat is the whole job.

## Acceptable inputs

- **Digital (preferred):** Krita / Procreate / anything — export
  1920×1080 PNG, no other constraints.
- **Phone photo of a paper drawing:** fine IF —
  - shot flat, straight-on, drawing fills the frame,
  - even lighting (no flash hotspot, no hard shadows),
  - 1920×1080 minimum resolution.
  - `use_hand_drawn.sh --photo` center-crops to 16:9 and resizes; pass
    `--corners "x1,y1,x2,y2,x3,y3,x4,y4"` (pixel coords of the drawing's
    four corners, clockwise from top-left) for a true perspective
    de-skew via ImageMagick. Below 1280×720 the script refuses — too
    soft for the pipeline.

## Drop-in procedure (one command)

```bash
cd production/TRIPPEDD_EP01/segments/luck-of-the-irish/v3
./use_hand_drawn.sh s5 /path/to/hd-s5-jump80.png
./use_hand_drawn.sh freeze --photo /path/to/IMG_1234.jpg
```

The script:
1. Backs up the AI keyframe it's replacing to
   `v3/hand-drawn/ai-backup/` (nothing is ever destroyed).
2. Processes the input (photo de-skew/crop if `--photo`; resize to the
   pipeline working size — 640×360 for s1–s5, full 1920×1080 for freeze).
3. Swaps the keyframe (or rebuilds `comp/mascot_reveal.mp4` for `freeze`).
4. Re-runs only the affected EbSynth segment(s).
5. Re-runs the full assembly (`assemble_v3.py` — now safe end to end;
   step 9 uses the sequential hits passes).

Then QC the beat by eye, re-upload, and push. The AI versions stay in
`ai-backup/` so any beat can be reverted with a file copy.
