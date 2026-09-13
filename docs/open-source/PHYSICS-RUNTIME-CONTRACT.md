# Physics Runtime Contract

The production physics lane is layered under the same evidence boundary as facial animation and depth/fracture.

## Pinned whole repositories

- RigFlex — secondary motion / soft rig: `ddce51fc70011d29188a8a387ea6bfdfc2a39f25`
- SimuSama — MPM / soft-body research: `4545bfe7a7a96dec5b2ffcdec45c1ec33f3ac1fd`
- JiggleArmature — secondary-motion bones: `2e2119994c63879ea5e55aca8651eed3b89c8b87`

## Authority

These systems generate **derived simulation or derived rig output**. They do not own canonical `MARS_source.glb` geometry. Canonical mutation is forbidden by the runtime manifest.

A physics result is not promoted from a numeric simulation alone. Promotion requires exact upstream pinning, reproducible output, collision/contact evidence, and actual-pixel visual evidence. `UNKNOWN` never passes.

Native Blender physics remains the production baseline where it covers the task; these projects are alternate lanes that must prove themselves against the canonical character.
