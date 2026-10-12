# Goodville — Street Environment Pieces

South Park flat-construction set for Goodville streets. Simple geometric
shapes, bold black outlines (4-6px), flat colors, transparent PNG backgrounds,
paper-cutout look.

Built procedurally: `build_street.py` (`python3 build_street.py` regenerates all).

| File | Size | Description |
|---|---|---|
| `road_straight.png` | 600x220 | Road segment, grey with dashed center line — **tileable horizontally** |
| `sidewalk.png` | 600x180 | Sidewalk with expansion joints + curb strip — **tileable horizontally** |
| `streetlamp.png` | 260x680 | Street lamp: base, pole, arm, head with lit lens |
| `mailbox_blue.png` | 320x440 | USPS-style blue mailbox: domed top, U.S. MAIL label, slot, red flag, legs |
| `tree_pine.png` | 360x560 | Pine: 3 stacked green tiers on brown trunk |
| `tree_round.png` | 420x520 | Round leafy tree: 3 overlapping canopy circles on trunk |
| `bush.png` | 420x240 | Low bush: 3 overlapping green blobs |
| `fence_wood.png` | 600x300 | Wooden picket fence on 2 rails — **tileable horizontally** |
| `fire_hydrant.png` | 260x420 | Red hydrant: dome top, side + front caps, base flange |
| `stop_sign.png` | 340x340 | Red octagon, white border + STOP text, pole |

Tiling: `road_straight`, `sidewalk`, and `fence_wood` repeat seamlessly —
dashes, joints, and pickets land on even pixel periods of their widths.
