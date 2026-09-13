# THE SKIN FILLING THE CENTRE OF HIS MOUTH IS GONE (2026-09-13)

> *"there's still a lot of skin stretch ... it looks like a gooey skin-textured paste of
> the blue skin and gums and teeth, but, like, stretched inside of the mouth cavity"*
> — the owner

| frame | |
|---|---|
| `01_BEFORE_rest.png` · `03_AFTER_rest_still_closed.png` | his mouth still closes — **identical** |
| `02_BEFORE_open_skin_fills_the_mouth.png` | what he was looking at |
| `04_AFTER_open_tongue_teeth_gums.png` | tongue, teeth, gums, cavity |
| `06_FALSECOLOUR_before.png` · `07_FALSECOLOUR_after.png` | the same two frames, coloured by MATERIAL |
| **`08_mouth_open_AB.gif`** | **watch it move — before and after, same 18 frames, side by side** |
| `09_mouth_open_AFTER.gif` | the fixed mouth alone, closed → open → closed |

**OWNER LAW #4: a mouth opening is MOTION.** A still cannot show whether his lips part or
his skin stretches into the cavity; the sequence can, so the sequence is what ships.

## THE CAUSE: THERE WAS NOTHING TO SPLIT

The lip seam is welded, so the jaw drags one continuous sheet of his skin into the cavity.
Splitting it opened the CORNERS and left the centre welded — at 44 crossing edges and
again at 98. That was never a tuning problem:

| | |
|---|---|
| edges crossing the crease in the lip zone | **44** |
| **faces STRADDLING the crease** | **36** |
| their area, median / max | **13.0 / 52.7 mm²** |
| their longest edge, median / max | **8.7 / 22.5 mm** |
| whole-head median face area | **0.59 mm²** |
| widest stretch of his mouth with **no crossing edge at all** | **7.9 mm** |

**A single face 22× the median area spans from his upper lip to his lower lip.** Across
7.9 mm of his mouth there is no edge for `split_edges` to act on. That face is what the
jaw pulls inward, and it is the blue skin filling the centre of his open mouth.

## SO THE FACES ARE CUT FIRST, THEN THE SEAM IS SPLIT

`tools/character/split_lip_seam.py`, and the cut is Blender's own `bisect_plane`, not
hand-rolled geometry. Measured on `assets/rigs/MARS_FACE.blend`:

    faces straddling his crease            36 -> 23   (36 cut, one pass)
    seam edges (upper face meets lower)    82, spanning 36.8 mm of his 50.0 mm mouth
    verts                                  27,721 -> 27,865
    original vertices' rest drift          0.000000 mm
    shape keys still moving                88 of 88

    seam aperture, how far his lips travel apart
      rest                                  0.00 mm
      jaw 18                               25.66 mm mean
      jaw 30                               42.45 mm mean
      jaw 30 + lips + funnel               44.36 mm mean / 46.68 max

    teeth the camera can see                5 -> 72 of 240

## AND IN PIXELS, WHICH IS THE AUTHORITY

False-colour by MATERIAL, whole frame, at jaw 30° + `lip_lower_depress` +
`lip_upper_raise` + `mouth_funnel`:

| | his skin | cavity | teeth | gums | tongue | sock | **oral total** |
|---|---|---|---|---|---|---|---|
| before | 83.41% | 3.64% | 1.06% | 1.01% | 0.09% | 1.78% | **7.58%** |
| after | **75.75%** | 4.56% | **2.45%** | 1.40% | **2.77%** | 4.08% | **15.24%** |
| **rest, before AND after** | 84.81% | 0.05% | 0.04% | 0.00% | 0.03% | 0.53% | **0.64%** |

**Oral anatomy doubles and his tongue goes from 0.09% to 2.77%, while REST is identical to
the pixel** — the counter-check that matters, because a mouth that no longer closes is not
a fixed mouth.

## FOUR OF MY OWN ERRORS ON THE WAY, ALL CAUGHT BY MEASUREMENT

1. **A SPLIT PAIR CANNOT BE TOLD APART BY ITS POSITION.** The whole point of the split is
   that the two halves sit on top of one another, so "is this vertex above the crease"
   answers the same for both, they get the same weights and they travel together.
   **Measured: seam gap 0.00 mm at every pose.** Classified by which FACES a vertex
   belongs to instead: 0.00 → 21.64 mm. That alone is the difference between a split that
   does nothing and one that works.
2. **A VERTEX LYING EXACTLY ON THE CUT IS ON NEITHER SIDE.** `z > seam_z` calls it "below",
   so every freshly bisected face read as *still straddling* and the count went 103 → 117
   on a pass that had cut every one of them correctly. The cut was working; my detector
   was not.
3. **AFTER A BISECT THERE ARE NO CROSSING EDGES LEFT TO SPLIT.** The crease becomes a chain
   of vertices sitting ON it, shared above and below. What has to be split is that chain —
   every edge whose two faces lie on opposite sides — and classifying the FACE by its
   centroid is what makes it epsilon-free, because a centroid is never on the crease.
4. **A SECOND CUT PASS MEASURED WORSE: 36 → 23 → 28.** Once a wide face is cut at its
   centroid's crease height, the fragments that still straddle are the ends of a curve, and
   a plane through THEIR centroids cuts them somewhere worse than not at all. One pass.

Also measured and reversed: deriving the seam from the mesh's own crease valley **wanders**
— 94 faces straddling against the measured contour's 36, and the split built on it recovered
*less* of his mouth (oral 3.92% vs 5.02%). It is kept only as the independent check on where
his crease is (mean 3.48 mm, max 6.93 mm from the contour); the contour is what is cut along.

## STALE AFTER THIS — THE VERTEX COUNT CHANGED

27,721 → 27,865. Everything indexed by vertex id on `MARS_MESH` is now stale, and is named
here rather than left to break two tools later:

    docs/evidence/hair/_valley_CAGE.npy  ->  _hairzones.npy  ->  every hair tool

Regenerate in that order: `valley_discriminator.py`, then `hair_zones.py`.

## STILL OPEN

- **23 faces still span his crease** and render as pale shards across the mouth. They are
  the ends of faces too wide for one plane; they need real topology, not another cut.
- **The mouth region has almost no geometry** — 261 faces fill his entire mouth. Densifying
  it is the same remedy as *THE LID CANNOT BE BUILT OUT OF THREE VERTICES*.
- The seam spans **36.8 mm of his 50.0 mm mouth**; the corners are not cut through.

---

## TWO THINGS THAT DID NOT WORK, MEASURED, AND LEFT OFF BY DEFAULT

The 23 faces still spanning his crease are not a cutting problem. **14 of them are visible
from outside at jaw 30°, with 1,008 rays landing on them — they ARE the pale shards.** They
are fragments of **17–23 mm²** on a head whose median face is **0.59 mm²**. Both attempts to
cut them away were measured and both failed:

| | oral anatomy in frame | note |
|---|---|---|
| the plain cut — **promoted** | **15.24%** | 23 faces still straddle |
| `--residual-rounds 3` (narrow the fragments, re-cut) | 15.11% | 23 → **26** straddlers |
| `--densify-passes 2` (subdivide the whole crease band) | 14.22% | costs **2,804** vertices |

The straddler count goes *up* while the pixels stay flat. No amount of plane-cutting gives
that region the topology it does not have — **261 faces fill his entire mouth**. Both code
paths are kept and both default to off, because the measurement is the point.

**THE NEXT OPERATION IS RETOPOLOGY OF THE MOUTH REGION, NOT ANOTHER CUT.** That is the
lane ChatGPT already named (Remi: mesh repair + Instant Meshes retopology + UV validation
without modifying the source mesh), and it is the same remedy as *THE LID CANNOT BE BUILT
OUT OF THREE VERTICES*.
