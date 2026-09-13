# Face linework → measured rig contract

The supplied face drawings/line overlays are treated as **measurement evidence**, not as a texture to eyeball against.

## Required semantic lines

- left/right brow arcs;
- upper and lower eyelid lines for each eye;
- inner and outer eye corners;
- nostril wings and nostril openings;
- nose bridge and tip;
- upper/lower lip boundaries and mouth corners;
- visible oral-cavity boundary;
- ear outline/root when side or rear evidence exposes it.

## Mapping rule

Each line is converted into points in the source image coordinate system and then registered to the measured 3D face using the existing face-anatomy landmark frame. The resulting 3D targets become constraints for the rig. They do **not** directly move vertices by a screen-space offset.

The hierarchy is:

`source linework → semantic 2D landmarks → 3D anatomical landmarks → geometry/shape fit → motion proof`

A line that cannot be registered with sufficient evidence is recorded as `UNRESOLVED`; it is never silently guessed.

## Face order

1. eyeball center/socket and eye-line;
2. upper/lower eyelid surfaces;
3. brows;
4. nostrils/nose;
5. mouth/oral cavity;
6. ears and ear-root controls;
7. named FACS expressions;
8. hair dynamics;
9. full performance clips.

## Ear policy

Ear motion is intentionally subtle. The new `tools/character/ear_motion_map.py` pass measures candidate ear regions and possible hair occlusion before any ear bones are created. If the source does not expose enough geometry, the tool returns `NEEDS_SOURCE_GEOMETRY` rather than inventing an ear.

## Visual gate

A structural landmark fit is not a visual PASS. The final gate must show the actual model with the target lines/anchors overlaid and must survive frame-by-frame motion proof. The project should retain both the overlay and the rendered result as artifacts.
