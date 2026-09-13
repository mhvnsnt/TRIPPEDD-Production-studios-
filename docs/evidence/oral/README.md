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

---

# THE CAVITY WAS NEVER MISSING. THE LIP SEAM DOES NOT PART. (2026-09-13)

Owner: *"probably cause ur doing it by hand instead of the rule and law of using open
source tools and things we have like Google GNM."* He was right. `tools/character/
oral_cavity.py`, `build_gnm_oral_donor.py`, `build_mars_oral_bridge.py`,
`survey_oral_aperture.py` and `run_mars_oral_repair.sh` were already in the repo, with
the **Google GNM (Apache-2.0)** oral donor sitting in `assets/donor/gnm_oral/` — mouth
sock, upper and lower teeth-and-gums, tongue and tongue expressions. I hand-built a
swept cutter instead of running them. OWNER LAW #3.

## Running the real tool

`oral_cavity.py` carves the cavity as a **void cut out of the head**, lofted from his
measured aperture curve, and it works:

```
WELD  47,021 verts -> 23,373 · boundary edges 68,237 -> 8 · non-manifold 20
      every surviving vertex position identical to the scan (0 moved)
cutter solid: 394 verts · boundary 0 · non-manifold 0 · signed volume +0.004146
cavity solid: 7 rings x 56 pts · depth 0.3182 (1.65 x mouth width)
carved: 23,830 verts, 47,174 faces, materials [tripo_mat..., MARS_ORAL_MAT]
rays landing on CAVITY WALL:  seam 41/41 · upper lip 0/41 · lower lip 0/41
oral-material vertices in front of the lip surface: 0
```

**That also explains why my boundary-edge test found nothing.** The cavity is a carved
VOID — the head stays a closed shell and its walls are the head's own surface turned
inward. Looking for new boundary edges near the lips was the wrong question entirely.

**And it carries a finding that matters for the eye slivers too:** the scan arrived as
loose triangles — 68,237 of 104,281 edges shared with nothing, because glTF splits a
vertex for every corner whose normal or UV differs. Welding at 1e-6 (one part in 840,000
of head height) gives 8 boundary edges and moves no vertex. *"That is why edge-splitting
tore the face into shards: the mesh was already shards."*

## So what is actually wrong: the lips are sealed and nothing parts them

| control | upper + lower teeth rays reaching the camera |
|---|---|
| rest | **0 / 240** |
| jaw 18° | 7 / 240 |
| jaw 30° | 6 / 240 |
| jaw 18° + `lip_lower_depress` | 6 / 240 |
| jaw 18° + `lip_lower_depress` + `lip_upper_raise` | 8 / 240 |
| jaw 30° + both lip keys | 7 / 240 |
| jaw 30° + both + `mouth_funnel` | **9 / 240** |
| `facs_jawOpen` 1.0 | 1 / 240 |
| `facs_jawOpen` + jaw 30° + lips + funnel | 6 / 240 |

**Nine of 240 at the very best.** That is the "small hole" he described, measured. The
cavity is there, the GNM teeth (1,440 verts each, 738 teeth + 702 gum), gums and tongue
(933 verts, 31 keys) are there — but the **upper and lower lip surfaces do not separate
at the seam**, so the jaw can only stretch them.

**NEXT, AND IT IS NOT ANOTHER BOOLEAN:** the lip seam needs to be a real split so the two
lip surfaces can part, and the jaw needs to carry the lower one. `oral_cavity.py` already
locates that seam (`seam_at(x)`, and the 41/41 seam probe). That is the lane.
