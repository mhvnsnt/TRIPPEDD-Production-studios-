# AGENTS: READ THIS BEFORE ANY FACIAL MEASUREMENT WORK ON MARS

The plates are HERE, as real bytes, in this directory. Do not report them missing.

```
mars_linework_front_close.png   1600x1600   THE AUTHORITATIVE ONE — invertible to 3D
mars_linework_front_full.png    1600x1600   whole head, reference only
LINEWORK_INDEX.json             sha256, camera, legend, tooling
```

## THE COLOUR LEGEND — and the distinction that matters

| colour | feature |
|--------|---------|
| **red** | eyebrow line |
| **yellow** | **UPPER** eyelid margin — and, lower on the face, the **nostril rims** |
| **green** | **LOWER** eyelid margin |

Upper vs lower is the whole point. "Eyelid contours" as one undifferentiated
bucket is what a blink cannot be built from.

Pure `#00FF00` in the border band is **not** a drawn mark — it is the
registration frame `annotation_base.py` burns in, and its presence is what
proves a returned plate was never cropped or rescaled.

## WHAT THESE PLATES PROVED — do not re-derive this, and do not undo it

**MediaPipe's FaceLandmarker misfits this particular face by one whole feature
vertically.** Measured by running it directly on the clean plate:

- its **eyebrow** ring lands on **his eyes**
- its **eyelid** rings land on **his cheeks**
- its **nose_alar** ring lands on **his upper lip**

See `docs/evidence/linework/mediapipe_misfit_proof.png` — the pixels, not a claim.

`renders/_rig_measure/canonical_fit.json` was BUILT from those landmarks, so it
carries the same error. It reports a **0.0000 mm residual** while being wrong by
up to **38.9 mm**, because a perfect thin-plate warp onto anchors that sit on the
wrong features is a perfect fit to the wrong question. A passing metric is not a
passing model.

**Therefore: for eyelid, eyebrow and nostril placement these owner-drawn plates
are the authority and `canonical_fit.json` is not.** OWNER LAW #5 — what he draws
is the observation; what the tool reports is a reading.

## HOW TO USE THEM

```bash
# read his marks back into ordered 2D polylines (+ an overlay proof)
./.trippedd_venv/bin/python tools/character/ingest_linework.py
#   -> renders/_rig_measure/linework.json
#   -> docs/evidence/linework/linework_extraction_proof.png

# render a fresh plate for him to mark (same camera, so marks stay comparable)
vendor/blender/blender -b -P tools/character/annotation_base.py --
```

The camera is not guesswork and is not duplicated: `tools/character/face_plate.py`
is the single definition of the plate's frame, framing and projection, imported by
both the renderer and the reader so they cannot drift apart.

## RELATED, ALREADY ON MAIN

`assets/donor/gnm_eyes/` · `assets/donor/gnm_face/` · `assets/donor/facs/` ·
`assets/rigs/MARS_face_state.json` · `assets/rigs/face_validation.json`
