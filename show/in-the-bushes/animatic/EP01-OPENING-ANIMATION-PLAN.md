# In the Bushes — EP01 Opening Animation Plan

## Target

Build the first reproducible animation proof around the exact origin/title sequence. The spoken phrase **"IN THE BUSHES!"** happens before the title card, and Busch's look-away remains a separate comedic beat.

## Timing

24 fps. The current scene contract is 288 frames / 12 seconds.

| Shot | Frames | Action | Animation strategy |
|---|---:|---|---|
| S01 | 0–47 | Night ambience + teens panic | Mostly holds, silhouettes, head turns, camera drift |
| S02 | 48–83 | Teen shouts "IN THE BUSHES!" | Mouth swap + pose change + brief camera push |
| S03 | 84–119 | Six-pack/open cans thrown | Object translation, hand release, follow-through |
| S04 | 120–167 | Beer splash + Busch transformation | Splash layers, foliage shake, transform poses, impact frame |
| S05 | 168–203 | Busch wakes + looks away | Wake pose, eye/mouth swap, branch sway, deliberate look-away |
| S06 | 204–227 | Reaction hold | Minimal movement; timing does the joke |
| S07 | 228–275 | Title card | Clean title reveal; no extra gag over it |

## Reusable Busch Pose Library

1. `busch_idle` — neutral bush silhouette.
2. `busch_wake` — first conscious movement.
3. `busch_transform` — beer-triggered supernatural change.
4. `busch_confused` — trying to understand what happened.
5. `busch_drunk` — recurring intoxicated physicality without making every joke about drinking.
6. `busch_surprised` — sudden reaction.
7. `busch_look_away` — signature origin-scene beat.
8. `busch_reaction` — reusable deadpan reaction state.

## Layer Contract

Each Busch scene should be separable into:

- foliage/body silhouette
- branch/limb accents
- eyes
- mouth
- beer/splash FX
- foreground/background separation
- camera transform

This allows animation to be produced by swapping a small number of assets instead of redrawing the character for every frame.

## First Proof

The first render target is the 12-second opening contract, not a full episode. A successful proof must:

- render from the machine-readable scene data;
- preserve 24 fps timing;
- show the beer impact and transformation as distinct phases;
- preserve Busch's look-away before the title;
- produce a deterministic FFmpeg-deliverable master;
- retain source/provenance metadata.

## Tooling

OpenToonz is the primary traditional/cutout 2D animation backend. Blender Grease Pencil remains the secondary reusable/procedural option. FFmpeg is the deterministic media backend. The repository must describe these as capabilities, not claim that a local executable exists unless CI or a workstation verifies it.

## Next Engineering Pass

Create the actual reusable Busch vector/source layers and a deterministic scene assembly script. Then connect those source layers to the opening scene contract and render a proof artifact.
