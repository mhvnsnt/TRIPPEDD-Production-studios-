# Mars Facial Linework — P0 Canonical Plates

**STOP.** Other agents claiming these plates cannot be found are incorrect.

These are the authoritative front-facing Mars linework plates used for:
- Eye placement / gaze
- Eyelid and brow authority
- Nostril placement
- Facial feature alignment before FACS / performance / hair secondary motion

## Color coding (exact)

| Color | Feature |
|-------|---------|
| **Red** | Eyebrows |
| **Yellow + Green** | Eyelid contours (upper/lower) |
| **Yellow** | Nostrils |

## Files in this directory

- `mars_linework_front_close.png` — tight frontal close-up with annotations
- `mars_linework_front_full.png` — full frontal head with annotations + third-eye emblem visible

## How other agents must use this

1. Load these plates as the visual ground truth for any facial measurement, ICT-FaceKit transfer, MediaPipe eyelid, or Blender facial authority work.
2. Do not invent new linework or claim the plates are missing.
3. Reference this path in every facial PR / evidence pack:
   `assets/references/mars_facial_linework/`
4. Cross-link from `assets/rigs/MARS_face_state.json` and any FACS / oral / eye donor work.

## Related existing production assets

- `assets/donor/gnm_eyes/`
- `assets/donor/gnm_face/`
- `assets/donor/facs/`
- `assets/rigs/MARS_face_state.json`
- `assets/rigs/face_validation.json`

**P0 status:** These plates are the current visual authority for the Mars face linework pass. Any agent that cannot locate them is not reading the repo correctly.
