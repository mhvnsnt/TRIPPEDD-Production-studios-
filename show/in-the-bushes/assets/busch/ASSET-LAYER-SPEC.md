# Busch — Reusable Animation Asset Layer Spec

## Purpose

Define the minimum reusable source layers needed to animate Busch without redrawing the character for every shot.

## Layer stack

1. `foliage_body` — primary bush silhouette and branch mass.
2. `head_turn` — optional grouped deformation/turn layer for the look-away beat.
3. `eyes_neutral` / `eyes_open` / `eyes_transform` / `eyes_confused` / `eyes_drunk` / `eyes_wide` / `eyes_side` — expression swaps.
4. `mouth_neutral` / `mouth_wake` / `mouth_transform` / `mouth_small` / `mouth_drunk` / `mouth_open` — dialogue/reaction swaps.
5. `subtle_sway` — reusable low-amplitude drunk movement.
6. `beer_impact` — beer splash/contact layer, isolated from character art.
7. `energy_fx` — transformation effect layer, isolated so the effect can be reused or removed.

## Animation rules

- Keep Busch readable as a bush first; facial features should feel embedded in the foliage rather than pasted on.
- Favor held poses, swaps, small translations, branch movement, and camera motion over frame-by-frame redraws.
- The look-away is a dedicated performance beat and must not be collapsed into the transformation.
- Beer impact and transformation effects must remain independent layers for timing and editorial control.
- Any new layer must include a reason, reuse target, and provenance note.

## First source-art deliverable

Create a clean neutral Busch turnaround/source sheet containing:

- front idle
- slight left/right turn
- eyes neutral/open/side/wide
- mouth neutral/open/small/drunk
- branch silhouette variants
- beer-contact silhouette

The source sheet is original production artwork for In the Bushes. Open-source software may be used to create it, but third-party character artwork is not imported as creative source material.
