# THE MOUTH: WHAT IS ACTUALLY WRONG, IN PIXELS (2026-09-13)

> *"the literal mouth was perfect yesterday ... It had the perfect tongue, teeth, gums,
> and mouth going. It had no stretch."* — the owner
>
> *"it looks like a gooey skin-textured paste of, you know, the blue skin and gums and
> teeth, but, like, stretched inside of the mouth cavity"*

He is right on both counts, and both are now measured rather than argued.

| frame | what it is |
|---|---|
| `00_TARGET_the_mouth_that_worked.png` | the mouth from 2026-09-12. Clean dark cavity, white teeth, pink gums, tongue, **no stretch.** This is the target. |
| `01_TODAY_oral_parts_hidden.png` | what `assets/rigs/MARS_FACE.blend` renders today |
| `02_TODAY_oral_parts_unhidden.png` | the same rig with the oral objects' `hide_render` turned off |
| `03_MY_CAVITY_PAINT_made_it_worse.png` | my attempt to repaint the cavity walls. **It is worse.** Kept as the receipt. |
| `04_FALSECOLOUR_by_material.png` | the same frame, false-coloured BY MATERIAL — this is what proves it |
| `05_MARS_rigged_cavity_protrudes.png` | `MARS_rigged.blend`, whose cavity bowl bulges out through his closed lips |

## 1. HIS TEETH, GUMS, TONGUE AND MOUTH INTERIOR WERE SWITCHED OFF

Measured on the canonical rig:

    MARS_MOUTH_SOCK    hide_render = True
    MARS_TEETH_UPPER   hide_render = True
    MARS_TEETH_LOWER   hide_render = True
    MARS_TONGUE        hide_render = True

Every render of this face has been of a mouth with the anatomy disabled.

**AND THAT IS WHY EVERY RAY-BASED INSTRUMENT DISAGREED WITH THE PICTURE.**
`scene.ray_cast` walks the depsgraph and **ignores `hide_render` entirely**, so the
aperture survey happily reported `MOUTH_SOCK 9.9%` and `TEETH_LOWER 2.2%` of a frame in
which *not one pixel* of either was drawn. A false-colour render with the skin hidden
came back **100% background** — the control that settles it. Same family as every other
entry in this file: **ask whether the metric can even express the failure.**

## 2. THE "OPEN MOUTH" IS 100% HIS OWN SKIN

False-colour by object, at jaw 30° + `lip_lower_depress` + `lip_upper_raise` +
`mouth_funnel`, counted per pixel:

    skin 90.99%   background 9.01%   teeth 0%   tongue 0%   sock 0%

With the parts unhidden it becomes `teeth_lower 2.06% · sock 1.81% · teeth_upper 0% ·
tongue 0%` — **3.87% of the frame.** The target frame scores `teeth 4.8% · tongue 7.8% ·
cavity 28.3%`. So what he is looking at is his own face texture smeared across the inside
of his mouth. That is the "gooey skin-textured paste", exactly.

## 3. THE LIP SEAM IS WELDED — AND A SPLIT PAIR CANNOT BE TOLD APART BY ITS POSITION

`tools/character/split_lip_seam.py` cuts it, and one finding is worth keeping:

    classified by POSITION   seam gap 0.00 mm at every pose
    classified by FACES      seam gap 0.00 -> 21.64 mm mean / 44.64 mm max at jaw 30

The entire point of the split is that the two halves sit **on top of one another**, so
"is this vertex above the crease" returns the same answer for both, they receive the same
weights and they travel together. What tells them apart is which SURFACE they belong to.
Shape keys and vertex groups ride through as bmesh layers — all 88 keys still move, no
original vertex shifts by more than 0.000000 mm.

Splitting is necessary and **nowhere near sufficient**: oral anatomy went 3.87% → 5.02%
of the frame. It does not fix the stretch.

## 4. REPAINTING THE CAVITY MADE IT WORSE. THAT IS WHY THE FALSE-COLOUR IS HERE.

1,589 of the 1,852 faces inside his mouth still carried the head's own texture, so I
assigned `MARS_ORAL_MAT` to the 131 faces the camera can see inside his open mouth (his
visible lip faces excluded by measurement, not by eye). `04_FALSECOLOUR_by_material.png`
shows the result: **orange is that material**, and it covers enormous slabs reaching up
past his nose and out over his cheeks.

The owner: *"you got pink wedges busting out of the cheeks and stuff ... it looks like a
bunch of just pink rims and stuff floating around."* Correct. **Not promoted, and the
canonical rig was never written.**

But it exposes the real defect: **261 faces fill his entire mouth.** Over 5,000 rays at
0.5 mm spacing land on 261 distinct faces — each one roughly 5 mm² against a head whose
median face edge is 2.02 mm. The mouth region has almost no topology, so anything mapped
across it smears. This is the same defect as *THE LID CANNOT BE BUILT OUT OF THREE
VERTICES*, in his mouth.

## 5. NEITHER EXISTING RIG IS THE GOOD ONE

    MARS_FACE.blend    88 FACS keys, eyes, linework blinks -- no aperture, anatomy hidden
    MARS_rigged.blend  BOOLEAN + MARS_APERTURE_CUTTER + MARS_CAVITY + separate gums
                       -- and its cavity bowl protrudes THROUGH his closed lips (frame 05)

The target frame was produced by `tools/character/run_mouth_pipeline.sh`, whose stage 3
(`rig_face.py`) writes **straight to `assets/rigs/MARS_FACE.blend`**. The eye, blink,
densify and eyeball work landed in that same file afterwards. That is how the mouth was
lost, and it is why it cannot simply be re-run: it would take the eyes with it.

**THE ROUTE IS THE ONE HE ALREADY GAVE:** rebuild the good mouth into a SEPARATE rig and
bring the aperture, cavity and gums across onto the rig that has the eyes and the nose —
*"find a way to merge those files so we have all of the right parts and working parts"* —
never by re-running a stage that overwrites the canonical rig in place.
