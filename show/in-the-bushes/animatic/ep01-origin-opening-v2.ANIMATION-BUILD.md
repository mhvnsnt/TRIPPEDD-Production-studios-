# In the Bushes — EP01 Origin Opening v2 Animation Build

## Goal

Turn `EP01-origin-opening-v2` into a reproducible 29.5-second animation proof without falling back to a slideshow treatment.

## Layer stack

1. `BG_NIGHT` — original nighttime environment.
2. `BG_ATMOS` — insects, distant light movement, subtle leaf motion.
3. `TEENS` — reusable silhouettes and pose swaps.
4. `PROPS` — generic six-pack and loose cans.
5. `BUSCH` — wake / reaction / look-away poses.
6. `FX` — spill, branch recoil, foliage twitch/shudder, impact.
7. `TITLE` — isolated title card.

## Build order

### Pass A — staging

- Place the three teen silhouettes on a common baseline.
- Establish left-to-right entrance and a believable stopping point near the bush.
- Keep the bush visible enough that the audience remembers it before anything supernatural happens.

### Pass B — character/object motion

- Apply `teen_run_stop`.
- Apply `teen_duck_peek` and `pack_hand_catch`.
- Add `can_rattle` before the decision line.
- Stage `point_and_hold` directly into the spoken **IN THE BUSHES!** beat.
- Apply `throw_arc_spin`, then `branch_clip_recoil`, `can_bounce`, and `liquid_spill`.

### Pass C — supernatural timing

- Let the teens leave before the bush reacts.
- Use two separate foliage twitches with visible holds.
- Build the larger shudder only after the audience has had time to wonder whether anything happened.
- Bring Busch up using `busch_wake_rise` with a delayed branch-arm movement.

### Pass D — comedy timing

- Scan left, right, then down.
- Give Busch a readable pause after noticing the spilled cans.
- Keep `busch_look_away` completely separate from the title transition.
- Hold the awkward silence.
- Hard cut to title.

## Render acceptance checks

- 708 frames exactly.
- 1920x1080 at 24fps.
- Spoken phrase occurs before throw.
- Teens are gone before Busch visibly wakes.
- At least two distinct foliage reaction stages occur.
- Look-away is visibly readable as its own action.
- Title does not begin during the look-away.
- Camera movement is not the primary source of perceived motion.
- No third-party beverage logos or distinctive branded packaging appear in source art.

## Next implementation target

The next engineering step is a deterministic frame builder/preview path that consumes the scene JSON plus `motion-blocks.json`, composites the SVG layers, and produces a frame sequence that can be validated by FFprobe/FFmpeg before full-resolution export.
