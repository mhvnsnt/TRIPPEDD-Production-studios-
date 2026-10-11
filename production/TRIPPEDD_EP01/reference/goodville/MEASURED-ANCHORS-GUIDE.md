# MEASURED ANCHORS — the Goodville 2D construction guide

**Status:** Standing method. Owner directive 2026-10-11 (the key-art five incident):
four characters came out clean, five came out terrible — same task, different
quality. That inconsistency was the defect. This guide makes the method
systematic, not luck. It is the practical companion to the MEASURED-ANCHOR LAW
in `~/AGENTS.md` and the kit contract in `kits/KIT-SPEC.md`.

**Scope:** every 2D character sheet, every rig, every cutout animation in every
show — anywhere a character gets put together from pieces. If the anchors
aren't measured, the sheet isn't started.

---

## 1. The idea in one paragraph

Every character gets an **anchor map**: a set of named points measured in
pixel coordinates on the character's own `head_blank` (the clean base head).
Every furniture piece — eyes, brows, pupils, mouths — is composited ONTO those
points, never eyeballed. Every limb piece gets a **pivot** placed at its real
joint. Outlines are single clean lines. The result: pieces that fit together
into a character instead of a collage, and the same quality no matter which
worker builds it.

This is not invented. It is the same method, three ways:

- **Preston Blair** (the master our kits are named for): "THE PARTS OF THE
  CHARACTER FIT TOGETHER AT SOCKET POINTS." He builds every head on an
  egg/ball with a center guide line and an eye-level guide line, then draws
  features over that framework in perspective. Crucially: the eyes' and ears'
  **bases stay fixed** while flexible features (mouth, cheeks) move around
  them. The fixed bases ARE the anchors.
- **South Park's actual rig** (Game Informer, from the studio): each character
  is ~10,000 pieces of geometry; every rig carries four or more views
  (front/back/left/right); special poses are replacement pieces toggled by a
  slider — one piece of geometry off, another on. Twelve different hands exist
  separately per view. Every one of those pieces registers to the same
  underlying construction, or the character falls apart.
- **Cutout rigging practice** (open-source, pulled in — see §8): a piece's
  region boundary runs along a line the drawing already has (collar, cuff,
  hairline — never across an open face); the pivot sits at the real joint
  (neck, shoulder, wrist); child pieces that shrink (blinking eyes) get an
  `under` fill so no hole opens behind them.

---

## 2. The anchor map

### 2.1 Coordinate system

All anchors live in the coordinate system of the character's **`head_blank`**
PNG — the clean base head with furniture zones filled in (the Dickie/Julio v2
pattern: brow/eye/mouth zones filled via skin-tone sampling from the
character's own face, so furniture composites onto flat skin, not holes).

- Origin: top-left of `head_blank.png`, x right, y down, pixels.
- The anchor map is per character, per head angle. The front-view map is
  measured by hand; 3/4 and profile maps derive from it (see §3.4).

### 2.2 The points (measure all of these)

| Anchor | What it is | How to measure |
|---|---|---|
| `eye_L`, `eye_R` | Center of each eye socket (the white oval's center) | Center of the donor's eye whites on `head_blank` |
| `brow_L`, `brow_R` | Brow line: inner end of each brow | Where the donor's brow starts, above the inner eye corner |
| `pupil_rest` | Pupil rest position | Center of the donor's pupil in the neutral gaze |
| `nose_tip` | Nose position (adults) | Tip of the donor's nose bump |
| `mouth_center` | Mouth slot center | Center of the donor's closed mouth line |
| `mouth_width` | Mouth slot width | End to end of the closed mouth line |
| `chin` | Chin bottom | Lowest skin pixel on the centerline |
| `head_cx` | Head horizontal center | Midpoint between the ears/side edges at eye level |
| `neck` | Neck join | Where the head meets the collar/torso |

Write them down. In the manifest, in a file, on paper — but written, not
remembered. The manifest format is in §2.3.

### 2.3 Anchor map format (goes in `manifest.json`)

```json
"anchor_map": {
  "head_blank": "head_blank.png",
  "head_blank_size": [520, 640],
  "points": {
    "eye_L": [198, 302],
    "eye_R": [322, 302],
    "brow_L": [172, 252],
    "brow_R": [348, 252],
    "pupil_rest": [198, 302],
    "nose_tip": [260, 348],
    "mouth_center": [260, 402],
    "mouth_width": 64,
    "chin": [260, 478],
    "head_cx": 260,
    "neck": [260, 478]
  },
  "measured_from": "donor head_sep.png, key art bbox (x0,y0,x1,y1)",
  "measured_date": "2026-10-11"
}
```

The existing per-piece `anchor` bbox field in the manifest stays (it records
where each piece was cut from). The `anchor_map` is the shared registration
all pieces composite against.

---

## 3. Measuring: exact steps

### 3.1 Prep

1. Build `head_blank.png` FIRST. Take the donor head extraction, fill the
   brow/eye/mouth zones with skin sampled from the character's own cheek
   (gradient clone, not flat fill — the Dickie v2 method). No holes, no
   baked-in expressions. This is the foundation everything registers to.
2. Open `head_blank.png` at 200%+ zoom. You are measuring, not guessing.

### 3.2 Measure

3. Mark `eye_L` / `eye_R`: the center of each eye white in the donor. For
   South Park-style characters the eyes are two white ovals side by side;
   the socket center is the oval's center whether or not the white is
   currently visible.
4. Mark `brow_L` / `brow_R`: the inner end of each brow, on the brow line.
   Adults always have visible brows; they sit above the inner eye corner.
5. Mark `pupil_rest`, `nose_tip`, `mouth_center`, `mouth_width`, `chin`,
   `head_cx`, `neck` per the table in §2.2.
6. Sanity check: `eye_L` and `eye_R` should be roughly symmetric about
   `head_cx`. If they're not, the donor head may be a 3/4 view — note it
   and measure the visible geometry honestly instead of forcing symmetry.
   (SYMMETRY GATE: mirror only verified-symmetric parts.)

### 3.3 Composite furniture onto the anchors

7. Every eye variant centers on (`eye_L`, `eye_R`). Every brow variant's
   inner end lands on (`brow_L`, `brow_R`). Every pupil variant centers on
   `pupil_rest` (look-directions offset from rest by a fixed, recorded
   number of pixels — e.g. `pupil_left = pupil_rest + (-14, 0)`).
8. Every mouth variant centers on `mouth_center` and stays within
   `mouth_width` (open/yell mouths may extend downward from center, never
   sideways past the slot — the slot is the registration).
9. Composite each variant onto `head_blank` and read it at 200% zoom. The
   furniture must sit IN the face, not on top of it. If it looks pasted,
   the anchor is wrong — re-measure, don't nudge blindly.

### 3.4 Angles (3/4, profile)

10. Front-view anchors are measured by hand. For 3/4 views, derive by the
    same transform applied to the head (the smooth-displacement method that
    held likeness on Dickie/Julio): transform the ANCHOR POINTS with the
    head, don't re-measure from scratch.
11. Profiles are the most interpreted piece — build from the front geometry
    (nose bump, brow ridge, chin) and record the derived anchors honestly
    in the manifest as `derived`, not `measured`.

---

## 4. Pivots for rigging and animation

When a piece moves, it rotates around its pivot. The pivot is almost never
the piece's center — it goes at the real joint. (Pulled in from cutout
rigging practice, §8.)

| Piece | Pivot placement |
|---|---|
| Head (whole) | The neck — where the head disappears into the collar |
| Eyes | Their own middle — eyes squash and swap, they don't swing |
| Pupils | Their own center — look-direction is translation, not rotation |
| Mouths | The mouth slot center (`mouth_center`) — replacement pieces, no rotation |
| Brows | Inner end (`brow_L`/`brow_R`) — they pivot from the inner corner on anger/surprise |
| Arm | The shoulder joint |
| Hand / held object | The wrist — not the object's own center |
| Torso | The waist — so breathing/leaning lifts upward from the hips |
| Leg | The hip joint |
| Whole body | Between the feet, at the bottom edge (for sway) |

Rules:

- **Region boundaries run along lines the drawing already has** — collar,
  cuff, hairline, hat rim, sleeve edge. NEVER cut across an open smooth area
  (middle of a cheek, flat expanse of shirt). A seam across open artwork is
  a scar.
- **Cut generously, overlap the join.** A head region reaches down past the
  jaw into the collar; pieces overlap instead of leaving hairline gaps.
- **Draw order is back to front.** The piece with the ugliest cut goes
  behind the piece that covers it.
- **Small rotations.** Cutout motion lives at small angles — past a few
  degrees the cut lines open up. Big moves get replacement pieces (South
  Park's slider method), not bigger rotations.
- **Eyes that blink need backing.** A blink scales the eye to nothing; if
  the eye was cut out of the head, a hole opens behind it. Fill the socket
  on `head_blank` (the `under` principle) so blinking never punches a hole
  in the face.

---

## 5. Outlines

- **One clean line** following the piece edge. Flat South Park cutout style
  uses minimal outlines on bodies (per the study, bodies are solid fills;
  faces carry the detail) — but where a line exists, there is exactly one.
- **NO white halos.** The pale fringe around a piece is the PNG's alpha
  fringe from extraction, not a style choice. Kill it at cut time (tighter
  alpha cutoff in the extraction), not after.
- **NO doubled or fringed edges.** If the outline looks doubled, the piece
  was composited twice or the extraction left a rim — re-cut, don't paint
  over.
- **NO outlines floating off the piece.** The line follows the edge. If it
  drifts, the outline was drawn from a different silhouette than the piece
  — re-derive it from the actual piece edge.
- **NO SQUARE CUTS** (KIT-SPEC law 8): every joining edge is shaped/rounded,
  never straight.

---

## 6. Per-character checklist

Before any sheet ships, every box gets checked with eyes on the actual
pixels at 200% zoom:

- [ ] `head_blank.png` exists — clean, no holes, no baked expressions
- [ ] Anchor map measured and written into `manifest.json` (§2.3)
- [ ] Every eye variant centers on `eye_L`/`eye_R`
- [ ] Every brow variant lands on `brow_L`/`brow_R`
- [ ] Every pupil variant offsets from `pupil_rest` by recorded pixels
- [ ] Every mouth variant centers on `mouth_center`, within `mouth_width`
- [ ] Every variant composited on `head_blank` and read zoomed — sits IN
      the face, not pasted on
- [ ] Angles' anchors derived from the front map, recorded as derived
- [ ] Outlines: single, clean, no halos, no doubling, no floaters
- [ ] No square cuts on joining edges
- [ ] Pivots recorded per §4 (needed for rigging/animation)
- [ ] Full composite (head + furniture + body + hands) reads as the
      character, not a collage — verified against the donor likeness
- [ ] `drill-log.md` updated with what was measured and what was derived

---

## 7. Defect catalog — what you see, what it is, what caused it

| What you see | What it is | Cause |
|---|---|---|
| Pale outline/halo around a piece | Alpha fringe from extraction | Loose alpha cutoff at cut time; re-cut tighter |
| Doubled or fringed edge | Piece composited twice, or extraction rim left on | Re-cut the piece; check for duplicate layers |
| Outline floating off the piece edge | Outline drawn from a different silhouette | Re-derive outline from the actual piece edge |
| Eyes look pasted on | Furniture eyeballed, not anchored | Measure the sockets; composite onto `eye_L`/`eye_R` |
| Blank white eyes (no pupils) | Pupils never composited into the head | Composite pupil layer onto every head angle |
| White rectangles on the face | Transparent holes in the head (oversized mouth/eye sockets) | Fill zones on `head_blank`; furniture goes on top |
| Mouth drifts between variants | No shared mouth slot | Center every mouth on `mouth_center` |
| Piece swings out of its socket in animation | Pivot in the wrong place | Move pivot to the real joint (§4) |
| Straight seam across the drawing | Cut runs through open artwork | Move the boundary to a collar/cuff/hairline |
| Hairline gap along a cut | Pieces butted edge-to-edge | Overlap the join; cut generously |
| Hole opens when eyes blink | Eye cut out of head with nothing behind | Fill the socket on `head_blank` (`under` fill) |
| Wedge of nothing when a limb rotates | No overlap at the joint | Overlap the join; rotate less; use replacement pieces |
| Parts don't fit — collage look | No shared anchor map | Stop. Measure anchors (§3). Rebuild on them. |

The last row is the one that sank the key-art five. Everything above it is
fixable per-piece; the collage look means the foundation was skipped.

---

## 8. Pulled in (2026-10-11, PULL-IN DIRECTIVE)

Actual usable material, wired into the pipeline — not just referenced.

### 8.1 png-to-animated-svg rig system (gerard-castell, GitHub)

- **Location:** `~/workspace/tools/png-to-animated-svg-src/`
- **What it is:** A complete skill for turning a flat PNG into a rigged,
  animatable SVG: `grid.py` (measure pieces on a labelled coordinate grid),
  `rig.py` (trace pieces, build named groups with pivots), `preview.py`
  (drag-test every pivot in a browser before animating).
- **Why it's here:** Its `rig.json` format (per-piece `region`, `pivot`,
  `joint`, `children`, `under`) is the measured-anchor method implemented
  as a tool. The pivot table in §4 and the defect catalog in §7 are drawn
  directly from its `reference/rigging.md`, which was written from the same
  failures we hit (halos = alpha fringe, holes on blink = missing `under`,
  swinging pieces = wrong pivot).
- **Wiring:** The `grid.py` measure-first workflow maps 1:1 onto §3
  (measure anchors before compositing). The `preview.py` pivot drag-test is
  the verification step for §4. Wire into Pocket Studio + kit tooling per
  the wiring law — parent's call on priority.
- **License:** open-source GitHub repo (check license file in repo before
  shipping anything built with it).

### 8.2 ChibiRigKit (milkc0de, GitHub)

- **Location:** `~/workspace/tools/chibirigkit/`
- **What it is:** Open-source pipeline that turns a single character PNG
  into an animated 2D rig: auto-prepares face pieces (sclera, iris,
  eyelashes, closed eyes, closed mouth, reconstructed face background),
  supports blinking, gaze movement, head yaw/pitch/roll, mic-driven lip
  sync, motion recording, WebM export, OBS sync.
- **Why it's here:** Its piece-preparation list (face background
  reconstruction behind the features = our `head_blank`; separate sclera /
  iris / closed-eye pieces = our furniture set) validates the kit
  architecture independently. Its face-background reconstruction is a
  reference implementation for the `head_blank` fill in §3.1.
- **License:** open-source GitHub repo (check license file in repo before
  shipping anything built with it).

### 8.3 Methods referenced (not cloned — documented here)

- **Preston Blair, _Cartoon Animation_:** socket points (parts fit together
  at sockets); egg-head model with center + eye-level guide lines; fixed
  bases for eyes/ears, flexible mouth/cheeks; model sheets as animator
  guides; draw the figure first, clothes over it.
- **South Park studio rig** (via Game Informer): ~10,000 geometry pieces per
  character; 4+ views per rig; replacement-piece sliders for special poses;
  12+ hands per view. Our kit's per-view, per-pose piece inventory follows
  the same logic at our scale.
- **Stop-motion/cutout lip sync practice:** body and eyes stay locked while
  only the mouth piece swaps — which is why the mouth slot anchor
  (`mouth_center`) must be shared across all mouth variants.

---

## 9. The rule, restated

Measure first. Write it down. Composite onto the numbers. One clean outline.
Parts that fit. Verify zoomed. Every character, every time — sheets, rigs,
animation. If the anchors aren't measured, the sheet isn't started.
