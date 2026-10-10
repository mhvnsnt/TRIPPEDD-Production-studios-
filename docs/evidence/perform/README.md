# THE PERFORMANCE TAKE — every channel he named, in one continuous shot

> *"we need to get the hair moving like hair and confirm in video the movement, blinking,
> mouth movement, hair sway, nose flare, etc, skip ears for now"* — the owner, 2026-09-13

`MARS_perform_ALL.mp4` is FRONT · THREE-QUARTER · SIDE side by side, 191 frames at 24 fps.
`perform_keyframes.png` is the same take as a contact sheet at each beat's own peak.
**A frame is not motion — watch the video.** (OWNER LAW #4)

## What each channel actually does, measured against the lines he drew

| beat | verts moved | max travel | from his own drawn feature | verdict |
|---|---:|---:|---:|---|
| HEAD TURN + HAIR SWAY | 23,830 | 159.72 mm | — | MOVED |
| **BLINK** | 420 | 15.53 mm | **3.8 mm** | **ON_TARGET** |
| **BLINK AGAIN** | 420 | 15.53 mm | **6.6 mm** | **ON_TARGET** |
| MOUTH / TALK | 4,938 | 29.39 mm | — | MOVED (jaw bone) |
| NOSE FLARE | 102 | 5.52 mm | **8.6 mm** | **MISPLACED** |
| BROW UP | 527 | 10.91 mm | **24.2 mm** | **MISPLACED** |
| HEAD NOD + SETTLE | 23,830 | 76.45 mm | — | MOVED |

Tolerance is 8.0 mm. **Nose flare misses it by 0.6 mm and the brow misses it by 16 mm.**
Both are recorded as failures rather than rounded down, and both need the same linework
rebuild the blink just had.

## The blink is driven by `blink_own_L/R`, built from his linework

`blink_L` / `blink_R` are still in the rig and are **deliberately not driven here**. They are
REGRESSION FIXTURES: measured, they travel **0.00** of the gap they must close and land
**68.5 / 65.8 mm** away, on his cheek. A rebuild that cannot tell itself apart from them is
not a rebuild. See `docs/evidence/blink_own/`.

## A statistic of mine that was wrong, and is recorded rather than quietly replaced

The first audit took the **centroid of every moved vertex**. A bilateral beat moves BOTH eyes,
and the centroid of two correct clusters is a point on neither: it scored the rebuilt blink
**33.9 mm** from "the eyelid" while the per-eye gate measured **4.5 mm** and PASSED. The table
above is the per-vertex median — each moved vertex's own distance to its nearest expected
point. `perform_take.json` carries the same note.

## The hair

Blender CLOTH on a separate `HAIR_SIM` object with **internal springs** (creep 87.52 → 1.14 mm),
a skin-only `HEAD_COLLIDER` cut back 6 mm from where the cap rests on the scalp, and a MASK
modifier so the face mesh does not draw the hair twice. `selfCollision` is **NOT_ATTEMPTED**
and is reported as itself.

## Reproduce

```bash
vendor/blender/blender -b -P tools/character/perform_take.py -- --res 420 --fps 24 --preroll 60
```
