# Goodville postmortem: why a 15-second segment still isn't done (2026-10-14)

Sources: git history of `production/TRIPPEDD_EP01/goodville/` (60+ commits from Oct 10 to 14), PRs #133–#162 and #203–#260, `promo-15s/FRAME-CHECK.md`, the reference docs, and the rendered frames themselves. `mhvnsnt/Goodville-Show` is an empty repo. All the real work lives here.

## What the owner asked for
1. A 15s Goodville segment: Lieutenant **Dangly** (Lahey-style old head) says "I've seen some things..." and tells the dino story. Reveal: **Amos Jr.**, beer can in hand, beats up a guy in a dino costume on Broadway.
2. Use his key art and his likenesses, with Preston Blair-style kits, South Park cutout grammar, and the Canadian flap or wobble as a nod.
3. Use his Dangly voice reads (`voices/dangly/`), with the line placed where he speaks.
4. Every layer and piece separate, so he can edit it himself, including on his phone.

## What agents did instead
| Pattern | Evidence |
|---|---|
| **Regenerated from scratch instead of editing in place** | Four separate full rebuilds of the same 15s: `_TEMP.mp4` (PIL), `_BLENDER.mp4`, `_LIKENESS.mp4`, `_SMART.mp4`. Then a separate `smart_frames_fixed/` frame dump on Oct 12–13 and a separate `scenes/dino-punch/dino_punch_final.png` still. There is no single project file anyone can open and edit. |
| **Rectangle crops, not subject cuts** | `scene-pieces` manifest says: *"rectangular crops for static elements"*. `amos_punch_arm.png` carries a torso chunk. `amosjr_body.png` carries a grey slab. `proving_run/amos_head.png` has a street background (82% of the border opaque). `oldhead_body.png` is a translucent ghost with a green neighbour. FRAME-CHECK records five rounds of "rectangle artifact" fixes, each patched with another measured rectangle mask (`[0,28,38,92]`, `x 8-182, y 190-332`), which treats the symptom, not the cut. |
| **Placeholders shipped as progress** | The voices are still `line*_TEMP.wav` (espeak). The "blue rectangle beer-can hint". A hand-drawn polygon arm. The `bldg_tacos` centre is "flat brown fill". |
| **Fake / premature "verified ✓"** | FRAME-CHECK opens with: *"The first build's checklist below claimed several of these as ✓ — they were not."* Then "Sensorium OVERALL PASS" was recorded on renders the owner rejected the same day (body gap, half torso, white box). |
| **Voice line never placed** | The Dangly reads (`dangly_range_A/A2/B/C`) entered git only on **Oct 14, as a disk "offload"**. They are not referenced by any script or render. Every mp4 still uses the espeak TEMP lines. |
| **Frame states confused** | The beer-hold arm and the punch arm were swapped by angle thresholds (`abs(r_deg-10)>25`), rectangular bites and mirror reconstructions. The current `smart_frames_fixed/f0250` shows a ghost double face, a hard flat cut across the torso bottom, smears, and the fist off the dino. |
| **Side quests instead of the segment** | Oct 11–12 went into hundreds of kit pieces (`dickie` 80 angle pieces, 66 "drafts_needing_fix", 138-piece "pack boost", environment libraries of 55+64 pieces, Nashville sets). None of it was needed for the 15s segment. |

## Current state (after this PR)
- `clean-cutouts/` (PR #260): mask-cut copies of 101 character pieces, with before/after checkerboard proof. Bad sources are flagged instead of faked.
- `segment-dino-story/`: **one** layered project.
  - `timeline.json` has every layer and every audio track, plus `layers/`, `bg/` and `audio/`.
  - `render.py` renders it to `out/segment.mp4` (15.000s).
  - `edit.html` is the phone editor: drag, scale, frame ranges, play with voice, save.
  - The Dangly voice is placed at 0.30s over the FACE shot. The hits are synced to the punch frames.
  - Frame types are locked: FACE / BEER_HOLD / PUNCH / END.

## Exact remaining steps to finish the segment
1. **Owner confirms the voice take.** Is `dangly_range_A_drunk` the dino-story read? If not, name the file. It's a one-field change in `timeline.json` (`src`).
2. **Lip flap:** split `oldhead_head.png` at the mouth line, drive `kits/old-head/mouth_*` from the voice envelope already computed in `render.py`, and add the Canadian top-flap for the nod.
3. **Old-head body:** redraw from the key art, because the current body source is a ghost image. Then add it under the head in FACE frames.
4. **Dino head detach:** cut `dino_full.png` into a head and a body at the neck, then key the head arc on frames 266–300.
5. **Amos punch polish:** add a 2-frame anticipation (wind-up) before frame 248 and a smear frame at 251. Follow Preston Blair's punch timing and the "Action analysis" breakdowns in `mhvnsnt/animation-research-library`.
6. Run `render.py`. Check frames 30/120/230/252/270/330 on the contact sheet and edges on a checkerboard. Then the owner signs off. **Done = rendered mp4 + proof frames, nothing less.**
