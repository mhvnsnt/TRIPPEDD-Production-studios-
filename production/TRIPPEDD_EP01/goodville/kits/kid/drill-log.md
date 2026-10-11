# Likeness drill log — kid (blue/red bobble hat)

## vs Tier A promo art (key art)
- Matches: blue hat dome + red brim + red pom silhouette; blonde side tuft color (#F2C04E);
  brown jacket + blue shirt collar; cigarette white stick + ember; dark chin patch;
  big white oval eyes touching at center; pupils looking up-right.
- Off: head_base is a clean flat peach oval — the key art has soft shading the flat
  fill removes (intentional SP flattening). The blonde tuft extraction is thinner than
  the key-art tuft (partial alpha ate the edges). Chin patch is hand-drawn, slightly
  more regular than the key-art's organic shape.

## Iterations
- 2026-10-11: First extraction round — head included hand + girl's hair (bbox too wide);
  hat included forehead/eyes (rembg kept whole head blob); torso grabbed Amos's arm +
  girl's arm (wrong subject). Re-extracted with tighter bboxes.
- 2026-10-11: round2 kid_head extraction came back DARK (rembg partial alpha, RGB
  (134,106,84) at 54% alpha vs key-art (248,195,155)). Re-extracted with larger crop
  (kid_head_fix) — clean.
- 2026-10-11: Blonde tuft isolated by blue-channel key caught SKIN (big tan blob).
  Re-isolated from key art with blonde key (r>200&g>150&b<130) in tuft region — correct.
- 2026-10-11: head_base had visible box-fill artifacts (filled feature regions read as
  boxes against shaded skin). Fixed by flattening entire head to flat #F7C39B and
  maxing alpha to 255.
- 2026-10-11: eyes_scheming had boxy skin lids. Redrew as curved skin ellipses + lid arcs.

## Still off
- Legs/feet are below the black bar in the key art (not visible). Built as generic dark
  pants + dark shoes — color is invented, marked in manifest. Owner should confirm
  or provide reference.
- The cigarette grip hand is hand-built (not extracted); the key-art hand is small
  (~20px) and partially occluded.
- No neutral brows in key art (kid has none visible); brows only on angry/sad per SP kid grammar.
