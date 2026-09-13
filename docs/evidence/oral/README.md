# THE MOUTH IS SEALED. MEASURED, NOT INFERRED.

> *"you regressed the perfect mouth with teeth tongue gums and oral bridges, u reduce it
> to a small hole, it really bad when he opens his mouth it's stretching instead of
> opening."* — the owner

He is right, and here is the number:

| jaw angle | upper-teeth sample rays that reach the camera |
|---|---|
| 0° | **0 of 72** |
| 18° | **0 of 72** |
| 30° | **0 of 72** |

His teeth are enclosed in a closed head at every jaw angle. There is nothing for the
jaw to open, so it can only pull closed skin apart. That is the stretching.

## Which rig actually has the better mouth — measured, and it is not the obvious one

| part | `MARS_rigged.blend` | `MARS_FACE.blend` |
|---|---|---|
| teeth upper | 80 verts | **1,440 verts** (+ gum material) |
| teeth lower | 80 verts | **1,440 verts** (+ gum material) |
| tongue | 146 verts, 2 keys | **933 verts, 31 keys** |
| tongue bones | none | **tongue_root / tongue_mid / tongue_tip** |
| mouth sock | none | **406 verts** |
| shape keys | 9 | **88** |
| **mouth aperture** | **BOOLEAN + cutter** | **none** |

So nothing oral should move from `MARS_rigged` except the aperture. `MARS_FACE` is
already the better oral build in every other respect.

## Why bringing that cutter across does NOT work

`MARS_APERTURE_CUTTER` is a **1.3 mm flat plate** — bbox 44.3 × 46.5 × 1.3 mm. A
DIFFERENCE boolean against a flat plate cannot open a closed shell. Measured: it
changed the head by 61 vertices and left the boundary-edge count at **14 → 14**, i.e.
no hole at all.

Two further traps on the way, both recorded because they cost real time:
- **A library-linked object arrives at the origin.** Its centroid read 116.78 mm from
  the source's upper teeth — exactly |teeth centroid|, i.e. (0,0,0). Its placement came
  from a transform that does not survive the link. The cutter has to be dumped in
  **world space** and rebuilt.
- **`lips_outer` from the canonical fit is not his mouth.** It sits 23–36 mm from every
  oral part of the rig it describes (sock 29.89, teeth upper 26.49, teeth lower 23.00,
  tongue 35.56 mm). Same MediaPipe fit that put his eyelids on his cheeks. Anchor on
  his **teeth**, which are at his mouth by construction.

## Where the opening belongs is already in this rig

`MARS_MOUTH_SOCK` has a **58-edge open boundary** — a closed loop 41.3 × 7.4 mm sitting
1.27–6.46 mm from the head surface. That rim is his lip line, authored for this head.
`tools/character/open_the_mouth.py` walks it into an ordered loop and sweeps it into a
closed solid (0 non-manifold edges, signed volume +0.00018393) to subtract.

## STATUS: NOT SOLVED. 4 of 120.

The swept-rim boolean gets **4 of 120** upper-teeth rays through with the jaw closed and
**0–1 of 120** with it open, at every depth from 18 to 45 mm and with the cutter both
jaw-weighted and static. That is not a working mouth and is not banked as one — the
tool **refuses** rather than saving it, and `MARS_FACE.blend` is left untouched.

The remaining hypothesis, consistent with the head surface extending 30 mm further
forward than the rim: his lips are **modelled closed with real thickness**, so the
opening is not a surface cut but a volume that has to be removed between two lip
surfaces. That is the same shape of problem as the eyes — the region needs correct
geometry, not a modifier laid over the wrong geometry.

## THREE INSTRUMENT BUGS OF MINE, FOUND HERE

1. **"Did the ray hit the head" is not visibility.** A ray entering the mouth carries on
   and hits the back of the skull from inside, so it reports a hit whether the mouth is
   open or sealed — 0/120 at every jaw angle and every cutter depth, including depths
   that definitely broke through. Compare the first hit distance against the distance to
   the tooth.
2. **Tooth positions sampled once at rest.** Rotating the jaw then aims the rays at where
   the teeth used to be, and `MARS_TEETH_UPPER` carries an armature modifier. That
   reported teeth *disappearing* as the mouth opened.
3. **A jaw-weighted cutter can close the hole as the jaw rotates.** 4/120 closed against
   1/120 open — opening his mouth hid teeth. The head's own lower lip already rides the
   jaw and the boolean runs after it, so the aperture should be static.
