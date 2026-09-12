# In the Bushes — EP01 Origin Opening v3 Animation Build

## Goal

Turn `EP01-origin-opening-v3-alley-police` into a reproducible 37-second animation proof without falling back to a slideshow treatment.

The current build has a procedural teen-performance layer in addition to the scene motion data. The teens are constructed from reusable character parts so the render can change pose, lean, arm swing, leg placement, head direction, clothing silhouette and facial expression over time.

## Layer stack

1. `BG_NIGHT` — original alley environment, puddles, fire escape, dumpster and distant street.
2. `BG_ATMOS` — police-light sweep, headlights, subtle environment movement.
3. `TEENS` — procedural reusable character rig with pose-to-pose performance.
4. `PROPS` — generic six-pack, loose cans, spill and impact.
5. `BUSCH` — wake / reaction / look-away poses.
6. `FX` — spill, branch recoil, foliage twitch/shudder and supernatural pulse.
7. `TITLE` — isolated title card.

## Character-performance pass

The teen group must not be treated as one large SVG that only translates across the frame.

The current character system is intentionally **more developed than stick figures** while remaining economical to animate. Each performer has a readable head treatment, torso/clothing silhouette, hands, articulated legs, shoes and individual acting language.

Reusable performance vocabulary currently includes:

- hang / talk
- turn / stare
- freeze / panic
- grab / turn toward exit
- run with alternating limbs
- duck / hide / peek
- crouch / breathe
- look at beer / look toward bush
- ask / group glance
- point / commit
- throw
- flee / flee faster

The rig uses independent body-part geometry and asynchronous movement between the three teens. Each numeric body/head/limb value is interpolated between pose extremes rather than snapping from one pose to another. Performer-specific delay and tempo values stagger the shared action arc, so the three characters do not react as synchronized puppets.

Current provisional performance identities remain:

- Teen 01 — impulsive: commits first and farther.
- Teen 02 — cautious: reacts later and stays more guarded.
- Teen 03 — deadpan: reacts latest and with less movement.

These are performance placeholders, not final locked names or immutable character canon.

## Build order

### Pass A — staging

- Place the three teens on a common baseline.
- Establish believable hanging-out positions inside the alley.
- Keep the alley exit and bush readable throughout the opening.

### Pass B — character/object motion

- Use the procedural teen performance layer rather than whole-sheet translation.
- Apply `can_handoff` and `grab_beer` as object/hand interaction beats.
- Apply `teen_run_out`, `duck_hide`, `peek_back`, and `catch_breath` with visible pose changes.
- Add `can_rattle` before the decision line.
- Stage `point_bush` directly into the spoken **IN THE BUSHES!** beat.
- Apply `run_out_of_alley`, then `throw_arc_spin`, `can_bounce`, `liquid_spill`, and `branch_recoil`.

### Pass C — supernatural timing

- Let the teens flee before Busch visibly wakes.
- Use separate foliage twitch and shudder stages with holds between them.
- Build the larger supernatural pulse only after the physical spill/twitch beats.
- Bring Busch up using `busch_wake_rise` with delayed branch-arm movement.

### Pass D — comedy timing

- Let Busch scan the scene before looking down at the cans.
- Give Busch a readable pause after noticing what happened.
- Keep `busch_look_away` completely separate from the title transition.
- Hold the awkward reaction.
- Hard cut to title.

## Regression checks

`tools/test_teen_performance.py` is a stdlib-only regression test for the character rig. It verifies:

- a mid-transition contains interpolated body values rather than simply matching an endpoint;
- the three performers occupy different acting states during the shared panic beat;
- throw timing is staggered by performer delay/tempo;
- the cast retains three distinct character-design languages rather than regressing to a generic stick-figure construction.

`tools/validate_origin_opening.py` verifies the authored 13-shot causal sequence before rendering.

`tools/render_preflight.py` verifies source assets and required render dependencies before attempting a full render.

## Open-source/tooling decision

Blender Grease Pencil is documented as a secondary animation backend for shots that need true point/stroke interpolation, deformation, inherited/parented motion, or hand-drawn breakdowns. Blender 4.5 LTS supports traditional 2D and cut-out animation and provides an `Interpolate Sequence` tool for generating in-between keyframes.

OpenToonz remains the primary traditional/cutout 2D backend for production-quality manual animation passes. The project is open source and its official repository documents the Modified BSD licensing boundaries; bundled third-party components must be handled according to their own licenses.

For this low-fi deterministic opening, the procedural Python rig remains the fast/reproducible default. Blender and OpenToonz are escalation backends when a shot's deformation, timing, cleanup or compositing requirements exceed the procedural SVG layer.

## Render acceptance checks

- 888 frames exactly.
- 1920x1080 at 24fps.
- Spoken phrase occurs before the throw.
- Teens physically run out of the alley before the beer is thrown.
- Teen pose/performance changes are visible; no whole-sheet-only translation as the primary teen animation.
- Legs, arms and body lean change during running/panic beats.
- Mid-pose interpolation is used instead of endpoint snapping.
- Teen reactions are staggered rather than synchronized.
- At least two distinct foliage reaction stages occur.
- Busch wake has visible weight and delayed secondary motion.
- Look-away is visibly readable as its own action.
- Title does not begin during the look-away.
- Camera movement is not the primary source of perceived motion.
- No third-party beverage logos or distinctive branded packaging appear in source art.
- Final media is inspected with FFprobe before being called verified.

## Engineering entry points

- `tools/build_origin_opening.py` — deterministic compositor/render backend.
- `tools/teen_performance.py` — reusable procedural teen performance rig.
- `tools/build_origin_opening_character.py` — character-performance entry point that reuses the deterministic builder while injecting the procedural teen layer.
- `tools/test_teen_performance.py` — regression checks for interpolation, asynchronous acting and character-design richness.
- `tools/validate_origin_opening.py` — story/timing continuity validator.
- `tools/render_preflight.py` — fail-fast environment/source preflight.
- `animatic/ep01-origin-opening-v2.motion-blocks.json` — authored timing and major action source of truth.

The next pass should extend the same component-level principle to Busch: independent foliage/body deformation, branch-arm timing, eye direction and mouth swaps, followed by a verified preview render and frame-level QC.
