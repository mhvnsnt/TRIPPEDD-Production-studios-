# MARS mouth sock surgical repair

## Finding

The open-mouth roof/tongue volume survey found `MARS_MOUTH_SOCK` was the
frontmost surface across the oral opening instead of behaving as a thin
vestibular lining behind the lips and cheeks.

Measured evidence supplied by the production investigation:

- z -8..-4 mm: sock first at depth +14.8 mm on 82% of sampled rays
- z -4..0 mm: sock first at +10.5 mm on 59%
- z +14..+20 mm: sock first at +21.1 mm on 49% (roof)
- z -14..-8 mm: sock first at +38.4 mm on 56% (over tongue)
- center-ray tracing also found the sock back wall at about +50..+57 mm,
  approximately 25 mm in front of the cavity wall at +79..+84 mm

Isolation separately identified a `MARS_MESH` skin bridge spanning the open
aperture. That defect was repaired separately (16 membranes removed; bridging
faces 38 -> 22; vertex drift 0.000000 mm; one visible closed-face loss).

## Surgical operation

`tools/character/repair_mars_mouth_sock.py` samples the measured mouth volume
with first-hit rays. It records which `MARS_MOUTH_SOCK` faces are actually the
frontmost surface, then, only with `--apply`, removes those faces using BMesh
`FACES_ONLY` deletion. It does not move vertices and does not touch
`MARS_MESH`, teeth, tongue, gums/palate, or the actual cavity wall.

Blender's BMesh/delete semantics support face-only deletion without deleting
the retained boundary vertices/edges. The important production rule is that
this is a surgical candidate, not a promotion: the resulting blend must be
rendered from the same open-mouth camera and pass pixel truth, reopen/SHA, and
mouth proof before promotion.

## Execution

Dry measurement:

```bash
vendor/blender/blender -b assets/rigs/MARS_FACE.blend \
  --python tools/character/repair_mars_mouth_sock.py -- \
  --report-only
```

Surgical candidate:

```bash
vendor/blender/blender -b assets/rigs/MARS_FACE.blend \
  --python tools/character/repair_mars_mouth_sock.py -- \
  --apply \
  --out assets/variants/MARS_MOUTH_SOCK_SURGICAL_CANDIDATE.blend
```

Then render the exact established open-mouth frame. Do not promote from the
ray report alone. Pixels veto geometry.
