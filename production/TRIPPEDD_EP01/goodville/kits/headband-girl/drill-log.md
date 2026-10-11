# Likeness drill log — headband-girl (purple headband)

## vs Tier A promo art (key art)
- Matches: purple headband with darker center mark; big black puffs + side hair;
  gold hoops; eyelashes on outer eye corners; thin arched brows; small pinkish lips;
  purple spaghetti-strap top with straps; brown skin #A06335.
- Off: head_base is flat (key art has soft modeling). Hair puffs are solid black —
  key art has subtle strand texture the flat fill removes (SP style). The headband
  mark is subtle in key art; reproduced as a slightly darker purple shape.

## Iterations
- 2026-10-11: head.png extraction was good. hair_L/hair_R tight crops came back
  dark/muddy — abandoned in favor of key-art isolation.
- 2026-10-11: Hair isolated by luminance key caught the BROWN background post.
  Fixed with neutral-dark key (spread<30) + extraction-alpha silhouette constraint +
  manual post exclusion. Clean.
- 2026-10-11: head_base first build had STEN's hat + crown's beanie intruding (crop too
  wide) and box-fill artifacts. Rebuilt from key art with skin-color key, tighter crop
  (435,505)-(625,810), flattened to #A06335, alpha maxed. Clean.
- 2026-10-11: prop_earring_R came back EMPTY (gold key too strict on occluded hoop).
  Re-isolated both hoops from key art with gold key — both present.
- 2026-10-11: eyes_scheming boxy lids → redrawn curved.

## Still off
- Legs/feet below black bar (not visible). Generic dark pants + shoes, color invented,
  marked in manifest.
- Nose: key art shows at most a faint nose line; omitted (spec: optional for adults,
  and it's not a clear anchor).
- The headband's center mark is very subtle in key art; the kit's mark is an
  interpretation of the dark squiggle.

## Attempt 3 rebuild (2026-10-11)
- Head stack rebuilt from key-art rembg cut (445,590)-(650,810): head_base (skin 150,94,54 + hair), headband.png (purple 141,97,140), donor eyes_open/pupils/brows_neutral/mouth_closed.
- Expression variants rescaled to donor anchors (eyes 78,140 / mouth 105,190 / brows 100,106). Pupil direction variants from donor shift.
- Angles: head_34L/34R (feature-shift), head_profile_R (from 34R + nose).
- Torso: torso_34 (squeeze), torso_back (purple 107,70,103 constructed). preview_sheet.png added.

## Defect repair (2026-10-11) — white rectangles on cheeks
- Root cause: head_base/34L/34R/profile_R had rectangular transparent HOLES in the
  lower cheek (leftover mouth-socket cut, oversized vs the actual mouth).
- Fix: filled interior transparent regions in lower face (y>0.6h) with flat skin
  #9A6034 (sampled). Eye sockets (upper face) preserved. Mouths composite on top
  of the now-solid head. All 4 head angles verified clean.

## v2 measured-anchor rebuild (2026-10-11, Sten's method)
Donor: old full composite (head_base + brows_neutral + eyes_open + pupils + mouth_closed + headband), 205x220. Saved as v2/donor_reference.png.

MEASURED ANCHORS (pixel coords, written down per MEASURED-ANCHOR LAW):
- skin_rgb: (154,96,52) — cheek samples (45,155)/(100,205)
- eye whites bbox: x31-125 y116-164 (from eyes_open.png alpha)
- pupil centroids: L(63.5,138.0) R(92.7,135.0) (dark-dot connected components, pupils.png)
- brow_L clean stroke: x46-65 y100-104; brow_R inner bit: x86-99 y98-99
- mouth_closed content: x86-124 y181-199
All saved in v2/anchors.json.

DEFECTS FOUND IN DONOR PIECES (fixed in v2):
1. brows_neutral.png: big dark HAIR BLOB on right (x~135-160) baked into the piece.
   v2: clean left stroke mirrored about x=77.5 for right brow; blob removed.
2. mouth_closed.png: big SKIN BOX (x86-124 y181-199) with lips painted at bottom.
   v2: tight 13x14 crop of lip-reddish pixels only.
3. pupils.png: eyelash-flick junk (x144-155 y116-152) + stray dots (x150-153).
   v2: two dots only at measured centroids.
4. head_base.png: transparent eye SOCKETS + brown BOX-FILL band in eye zone + painted
   brows/mouth baked in.
   v2/head_blank: zones feather-filled with sampled skin; hair (dark px) and gold
   hoops protected from fill; sockets opaque; headband composited on top.
5. Lid lines: old donor's lid line was the socket edge (vanishes on head_blank).
   v2/eyes_open: 1px black arcs drawn hugging the top edge of each white oval +
   2 short lash flicks at R-eye outer corner, matching key art.
6. head_34L/34R: old ones had ghosted/doubled outlines from bad warps — NOT reused.
   v2: single-pass PIL AFFINE squeeze 0.85, BICUBIC, anchored at far edge.

VERIFICATION:
- head_blank + tight furniture @ recorded offsets (v2/furniture_offsets.json)
  reconstructs donor: 343 px differ (>60/765) out of 22351 — all in the fixed zones.
- Zoomed vs key art: lid lines thin and hugging (key art has thin black upper lid
  line); lash flicks short at R outer corner; brows thin arches; pupils cross-eyed
  toward center like key art; small pinkish lips; purple headband with center mark;
  gold hoops; big black loc puffs. Identity held.
- preview_sheet.png rebuilt: assembled character (v2 head + earrings + torso + arms),
  head angles, tight furniture grid, head_blank panel — character put together,
  not scattered parts.
