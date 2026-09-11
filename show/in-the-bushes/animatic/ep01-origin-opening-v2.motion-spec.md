# In the Bushes — EP01 Origin Opening v2 Motion Spec

**Sequence:** `EP01-origin-opening-v2`  
**Runtime:** 29.5s  
**Frame rate:** 24fps  
**Canvas:** 1920×1080  
**Style:** limited 2D / cutout-friendly, expressive timing, reusable poses

## Motion goal

This version should feel like a tiny scene rather than a title sting. The camera and characters should create forward momentum before the supernatural beat. Movement stays economical: strong key poses, holds, object arcs, small secondary motion, and deliberate reaction timing.

## Shot blocking

| Shot | Frames | Motion |
|---|---:|---|
| S01 | 0–71 | Slow camera push. Bush leaves move subtly on an irregular loop; distant light flicker and tiny insect movement establish the location. |
| S02 | 72–143 | Three teen silhouettes run in from frame-left, decelerate, duck, then pop up just enough to look back. Six-pack nearly slips; hand catches it. Bush remains completely normal. |
| S03 | 144–203 | Medium push-in. One teen checks the pack, one steadies a rattling can, third teen points toward off-screen trouble then toward bush. Short holds let the whispered argument breathe. |
| S04 | 204–251 | Quick head turn / point into bush. On the shouted **“IN THE BUSHES!”**, hold the pose for a fraction before cutting into the throw. |
| S05 | 252–323 | Six-pack travels on a readable arc with slight rotation. One loose can clips a branch and changes trajectory. Another bounces. Open can lands against foliage and spills. Add a brief impact shake. |
| S06 | 324–419 | Teens exit first. Bush does nothing for a beat. Beer drips downward. Leaf twitch #1. Hold. Leaf twitch #2. Hold. Then a deeper foliage shudder travels from low center outward. |
| S07 | 420–491 | Transformation is restrained: foliage lifts, eyes read, body rises a little. Add a tiny delayed branch-arm movement after the main rise so Busch feels newly conscious rather than mechanically animated. |
| S08 | 492–551 | Busch scans left → right → down. Eye direction leads head movement. He notices fleeing teens late. One short pause sells confusion. |
| S09 | 552–611 | Busch turns toward the chaos, stops, then deliberately looks away. The look-away is held longer than comfortable. No title transition yet. |
| S10 | 612–659 | Almost still. One blink, tiny body sway, one leaf settling. Let night ambience dominate. |
| S11 | 660–707 | Hard cut to title. No dissolve. Title holds for clean readability. Busch remains a subtle silhouette behind/around the lettering. |

## Reusable motion presets

- `teen_run_stop`
- `teen_duck_peek`
- `teen_look_back`
- `pack_hand_catch`
- `can_rattle`
- `point_and_hold`
- `throw_arc_spin`
- `branch_clip_recoil`
- `liquid_drip_loop`
- `foliage_twitch`
- `foliage_shudder`
- `busch_wake_rise`
- `busch_eye_scan`
- `busch_look_away`
- `reaction_blink_sway`
- `camera_slow_push`
- `impact_micro_shake`

## Timing rules

1. The spoken phrase **“IN THE BUSHES!”** must be heard before the beer is thrown.
2. The teens flee before Busch visibly wakes; the audience gets a short suspense gap.
3. The transformation should escalate in stages instead of one instant glow effect.
4. Busch's look-away remains a separate comedy beat.
5. The reaction hold remains separate from the title card.
6. Avoid constant zooming. Camera movement is used to establish, reveal, and punctuate—not to fill empty animation.

## Asset requirements

Use existing Busch model/wake/look-away/reaction assets. Add reusable original teen silhouettes, generic beer-pack/can props, and a generic spill/impact FX layer. No beverage-company logo, label artwork, or distinctive branded packaging is required for the story beat.

## Render target

Master: 1920×1080, 24fps, 708 frames.  
Preview: same timing, reduced resolution permitted.  
Primary 2D backend: OpenToonz.  
Deterministic media/QC: FFmpeg + FFprobe.
