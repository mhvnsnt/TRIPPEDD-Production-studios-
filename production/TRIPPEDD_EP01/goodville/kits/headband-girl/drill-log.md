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
