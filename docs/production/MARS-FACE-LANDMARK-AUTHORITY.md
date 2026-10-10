# Mars Face Landmark Authority

## Why the old path is retired

The previous eye authority was a single orthographic render followed by pixel
raycasts. That is useful for coarse anatomy, but it is exactly the wrong
instrument at a fold where the brow ridge and upper lid project into nearly the
same pixels. A successful raycast only proved that a surface existed at the
pixel; it did not prove that the surface was the anatomical feature intended.

The eye rig therefore must not classify dark texture regions or use hand-tuned
distance thresholds to decide what is an eyelid.

## Open-source authority

The eye/eyebrow authority now uses **MVMP 1.4.2** (gfacchi-dev/mvmp, MIT).
MVMP supports GLB/GLTF meshes, renders five deterministic facial views, runs
MediaPipe, and back-projects the detected landmarks to the actual mesh while
returning the closest target vertex for every landmark.

MediaPipe's published topology defines the eye and eyebrow semantics. The
project's L/R names preserve the existing rig convention, but the membership
lists themselves are taken from MediaPipe's official face-landmark connection
sets.

The canonical 468-point MediaPipe face model remains the semantic reference:
the first 468 landmarks of the 478-point model follow that topology. We do not
invent a new eyelid curve.

## Hard gates

The authority generator refuses to publish when:

- fewer than 478 landmarks are returned;
- any semantic landmark maps outside the Mars mesh;
- an eye has zero measured width/opening;
- the upper-lid semantic set overlaps the eyebrow semantic set;
- the measured upper-lid/brow separation collapses below 8% of that eye's own
  measured width.

The last check is not a tuning knob for the blink. It is an identity/registration
sanity gate. If the registration collapses, the build stops.

## Blink rule

blink_L/R may deform only vertices selected from the measured upper-eyelid
authority band. The eyebrow authority set is a separate, immutable semantic
region. The blink validator must prove:

1. upper-lid vertices travel;
2. eyebrow vertices do not travel beyond the configured leakage ceiling;
3. the eye aperture closes against the actual eyeball;
4. the render agrees with the measurements.

A green metric with a bad render is a failure.

## Rebuild

Install mvmp==1.4.2, then:

    .trippedd_venv/bin/python tools/character/measure_face_mvmp.py \
      --debug renders/_rig_measure/mvmp_debug

The output is:

renders/_rig_measure/face_landmark_authority.json

It is derived evidence, not hand-authored anatomy.
