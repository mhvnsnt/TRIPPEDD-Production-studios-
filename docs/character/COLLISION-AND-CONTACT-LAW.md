# MARS Baseline Collision & Contact Law

## Purpose

Baseline character animation must be physically coherent before stylized exaggeration is allowed. Hair must not pass through the head/face, the tongue must not pass through cheeks or lips, and independently simulated or deformed regions must not silently interpenetrate anatomy.

This is a **contact/QC authority**, not a demand that every creative shot look physically realistic. Exaggeration, cartoon motion, deliberate clipping, and impossible poses are allowed only when the shot explicitly opts into them.

## Baseline law

> **No unapproved interpenetration.** Every collision-sensitive pair has a declared relationship: `BLOCK`, `ALLOW`, or `STYLE_OVERRIDE`.

`BLOCK` means penetration beyond the declared tolerance is a gate failure.

`ALLOW` means the pair is intentionally non-colliding and must be documented; it is not an accidental omission.

`STYLE_OVERRIDE` means a shot may intentionally violate baseline contact for an explicitly authored effect. The override must be recorded with the shot/evidence manifest so a deliberate glitch cannot be mistaken for a broken baseline.

## Collision layers

Collision should be layered rather than making every vertex collide with every other vertex:

1. **ANATOMY_PROXY** — stable low-complexity collision surfaces for head, face, mouth cavity, tongue, teeth and other anatomical regions.
2. **DEFORMED_SURFACE** — the render surface whose measured deformation is authoritative for final contact checks.
3. **SIMULATION** — hair/cloth or other simulated regions that need collision against anatomy.
4. **SELF_CONTACT** — optional self-collision for hair/cloth where inter-locking or fold-through is possible.
5. **CREATIVE_OVERRIDE** — explicit shot-level exceptions for intentional exaggeration.

The proxy is an acceleration/collision surface, never a replacement for the supplied render mesh. Final gates must measure against the appropriate authoritative surface.

## Required baseline contact pairs

| Pair | Baseline | Gate |
|---|---|---|
| Hair → scalp/head | BLOCK | No hair vertex may cross the head collision surface beyond tolerance |
| Hair → face/ears | BLOCK | No face-through on approved contact regions |
| Hair → hair | BLOCK where self-collision is enabled | No unresolved self-interlock/penetration |
| Tongue → cheeks | BLOCK | No tongue vertices inside cheek collision volume |
| Tongue → lips/teeth | BLOCK with authored contact exceptions | Contact may touch/slide; penetration beyond tolerance fails |
| Teeth → tongue | BLOCK | No unexplained deep intersection |
| Teeth → cheeks | BLOCK | No cheek-through |
| Eyes/lids → eyeball/socket | BLOCK | Preserve eye seating while animating |
| Facial soft tissue → teeth/mouth cavity | BLOCK where anatomy is closed | No accidental oral breakthrough |

The exact tolerance is **not guessed**. Each lane must publish its measured tolerance, source/scene hash, frame range and QC result.

## Measurement contract

A collision gate must report, at minimum:

- source scene/asset hash;
- collision proxy hash and construction method;
- render-surface hash where applicable;
- frame range and sampling rate;
- collision pair;
- minimum signed separation or penetration depth;
- p50/p90/p99/max penetration (or equivalent distance distribution);
- count of violating vertices/contact samples;
- maximum allowed tolerance;
- whether self-collision was attempted;
- visual evidence reference;
- exact command used to reproduce the measurement.

`UNKNOWN` when any required measurement or evidence is missing. `PASS` only when the measured gate passes and the required visual evidence agrees.

## Hair baseline

Hair is the first simulation lane because the current MARS hair test demonstrated that a raw secondary-motion number can be dominated by rigid drift/creep. Do not accept a large motion value as proof of healthy sway.

For hair, measure rigid head motion separately from true secondary motion. A baseline proof should use a pre-roll long enough to establish equilibrium, then measure a controlled turn. Native Blender Cloth/XPBD collision should be preferred over a custom collision solver when it can provide reproducible contact behavior.

Required hair checks:

- roots remain attached within the published root-give tolerance;
- hair does not penetrate the head/face collision surface;
- secondary motion is measured after rigid-transform removal;
- pre-roll is sufficient to distinguish settling/creep from sway;
- self-collision is explicitly `PASS`, `FAIL`, or `NOT_ATTEMPTED`;
- a multi-frame visual sequence is published.

## Mouth/tongue baseline

Tongue, teeth, lips and cheek collision should use dedicated anatomical proxies or volumes derived from the authoritative model. Do not use arbitrary image-space pixel tests as the collision authority.

The normal expressive system can drive extreme shapes, but the baseline lane must first prove that ordinary speech, blink, jaw, tongue and expression ranges do not create accidental face-through.

## Stylization and deliberate bugs

Creative modes are first-class, but they must be explicit:

- `BASELINE_PHYSICAL` — collision gates enforced.
- `EXAGGERATED` — authored deformation ranges may exceed baseline, but collision remains enforced unless the shot declares an override.
- `CARTOON_GLITCH` — deliberate violations permitted only through `STYLE_OVERRIDE` records.

This keeps the character capable of impossible animation without making accidental clipping indistinguishable from intentional style.

## Implementation order

1. Build/verify anatomy collision proxies from the existing authoritative MARS geometry.
2. Add a reusable pairwise contact measurement utility.
3. Wire hair → head/face collision into the native Blender Cloth/XPBD proof.
4. Prove tongue → cheek/lip/teeth contacts on the oral rig.
5. Add eye/lid/socket contact checks to the existing eye-linework proof.
6. Publish per-lane evidence manifests and rendered sequences.
7. Add shot-level style overrides only after baseline gates are green.

No global remesh is permitted as a shortcut. Collision proxies are derived working artifacts; MARS_source.glb remains the render-surface authority.
