# Goodville House Exterior Pieces — South Park flat style

Built procedurally with Python PIL (`build_houses.py`). Flat colors, bold black
outlines (4–6px), transparent backgrounds, RGBA PNG. Construction-paper cutout look.

## Pieces (16)

| File | Size | Contents |
|---|---|---|
| house_body_blue.png | 800x600 | Blue walls + grey foundation |
| house_body_yellow.png | 800x600 | Yellow walls + grey foundation |
| house_body_red.png | 800x600 | Red walls + grey foundation |
| roof_brown.png | 900x420 | Brown triangle roof |
| roof_grey.png | 900x420 | Grey triangle roof |
| roof_red.png | 900x420 | Red triangle roof |
| door_closed_wood.png | 170x280 | Wood door, closed, gold knob |
| door_open_wood.png | 260x280 | Wood door swung open, dark interior |
| door_closed_white.png | 170x280 | White door, closed, gold knob |
| door_open_white.png | 260x280 | White door swung open, dark interior |
| window_lit.png | 170x150 | Warm yellow glow, white frame, cross mullion |
| window_unlit.png | 170x150 | Dark blue-grey, white frame, cross mullion |
| chimney_brick.png | 130x220 | Flat brick courses + cap |
| porch.png | 800x220 | Deck, railing, balusters, posts |
| garage_door_closed.png | 440x320 | White panel door, horizontal seams, handle |
| garage_door_open.png | 440x320 | Door rolled up 1/3, dark interior below |

## Alignment anchors (all coords = pixels from piece's own top-left)

House body canvas is the reference. Walls: x 60..740, y 120..500.
Foundation: x 40..760, y 500..560.

- **Roof -> body**: place roof at `(body_x - 50, body_y - 280)`. The roof eave
  line (y=380 in the roof canvas, x 20..880) then sits 20px *below* the body top
  edge (y=120), giving a 20px overlap so no gap shows. Roof canvas is 100px
  wider than the body canvas, centered.
- **Doors -> body**: place closed door so its bottom edge = body top + 500
  (foundation top), e.g. `(body_x + dx, body_y + 220)`. Open door interior
  occupies x 10..150; hinge side at x=150.
- **Windows -> body**: place anywhere on the wall area (y between 120 and ~360
  so the window sits fully on walls above the door line). Example:
  `(body_x + 90, body_y + 200)`.
- **Chimney -> roof**: chimney canvas 130x220, cap at top. Place so chimney
  bottom overlaps the roof slope, e.g. `(body_x + 610, body_y - 30)` — chimney
  must be composited AFTER the roof so it sits on top of the slope.
- **Porch -> body**: place at `(body_x, body_y + 300)` — porch canvas is
  800x220, deck bottom (y=214) then sits just below the foundation top
  (y=500). Porch is full body width; composite it in front of the body but
  offset doors/windows horizontally so they don't hide behind the railing.
- **Garage door**: standalone piece; composite against a body wall or use as
  its own structure. Bottom edge = ground/foundation line.

## Composite order (back to front)
1. Roof  2. Chimney  3. House body  4. Windows  5. Doors  6. Porch

(Door/garage interior-dark pieces go behind their own frame — they're
self-contained.)
