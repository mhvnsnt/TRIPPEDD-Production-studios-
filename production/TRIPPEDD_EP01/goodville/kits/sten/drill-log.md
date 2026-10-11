# Likeness drill log — STEN (blue/red bobble hat)

NAME LOCKED 2026-10-11: STEN. Adult. Stan-based (the only SP-based key-art figure per owner).

OWNER CORRECTION 2026-10-11: ADULT, not a STEN. STEN (Stan hat colors + blonde hair). Name TBD (Sten proposed).

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
- 2026-10-11: round2 STEN_head extraction came back DARK (rembg partial alpha, RGB
  (134,106,84) at 54% alpha vs key-art (248,195,155)). Re-extracted with larger crop
  (STEN_head_fix) — clean.
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
- No neutral brows in key art (adult grammar correction 2026-10-11: adults have visible brows; brows_neutral added — the old "SP STEN grammar" note was wrong, he is an adult).

## Attempt 3 rebuild (2026-10-11)
- head_base.png + torso_base.png were BROKEN (opaque peach blob / crude geometric) — rebuilt from key art.
- New: rembg u2net head cut (250,555)-(490,800) incl. pom; artifact cleaned; flat skin #F5C098 fill; jaw trimmed at y188.
- hat_full.png (blue/red + pom), hair_full.png (yellow side tuft) extracted by color key.
- Donor furniture: eyes_open (whites), pupils (measured dots), mouth_open_donor from cut; all expression variants rescaled/repositioned to donor anchors (eyes center 134,122 / mouth 135,145 / brows y94).
- Angles: head_34L/34R via feature-shift on fixed silhouette; head_profile_R via 0.72x compress + nose bump; torso_34/torso_back.
- Torso constructed from sampled colors (jacket 87,62,57 / navy 40,47,89) — key-art torso 90% occluded, documented.
- preview_sheet.png + head_neutral_full.png added. Every piece verified zoomed vs key art.
