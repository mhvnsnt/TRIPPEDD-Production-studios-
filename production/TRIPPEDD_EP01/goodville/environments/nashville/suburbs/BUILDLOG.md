# NASHVILLE SUBURBS + TRAILER PARK + GOODVILLE ANCHOR — BUILD LOG
Worker 3 of 3 | 2026-10-12 | Output: `/tmp/nashville-build-suburbs/`

All assets hand-built with PIL in South Park flat style: bold black outlines (4-7px),
flat colors, simple geometric shapes, transparent PNG backgrounds.
Builder script: `build.py` (deterministic, rerunnable — edit and rebuild any piece).

## Style coordination
- Reused the existing `storefront.png` (trippedd-studio goodville/environments/store/) in
  `goodville_street.png` so the town center matches established store pieces.
- QC'd with the repo's Goodville style_hold scorer (`tools/brain/sensorium/goodville_style.py`):
  n_colors 35-92, edge_density 0.030-0.052, texture 414-3145 — all in cartoon bands.
- EVERY piece visually verified by the builder (frame reads, two text-overflow defects
  fixed: strip mall "LAUNDROMAT" sign, gas station pylon "GOODVILLE").

## Deliverables (32 PNGs, 684K total)

### Mobile homes (modular, transparent bg)
- `mobile_home_1.png` (940x560) — faded teal single-wide: white trim stripe, vented skirting,
  striped porch awning, screen door + cinder steps, window AC, satellite dish, rust spots, weeds, hitch tongue
- `mobile_home_2.png` (940x600) — tan double-wide, brown trim: deck with railing + rocking chair,
  blue awning, clothesline with laundry, window AC, rust spots
- `mobile_home_3.png` (940x560) — white single-wide: red shutters, flower boxes, red door,
  lattice deck, gray roof

### Full scenes (1600x900)
- `trailer_park_day.png` — gravel lot loop, 3 homes in a row, sun/clouds, hills, power poles +
  sagging wire, tire stack, tires, 2 lawn chairs, grill, rusty pickup, trash cans, mailbox,
  oak + pine trees, bushes, dirt patches
- `trailer_park_night.png` — same layout, night palette: moon + stars, tinted homes,
  ALL windows lit yellow (recorded per-home window rects), streetlamp with glow
- `goodville_street.png` — town center: existing corner store piece + BARBER shop (barber pole)
  + DINER, sidewalk, road with crosswalk + center dashes, 2 streetlamps, stop sign,
  fire hydrant, trash can, trees, hills

### Junkyard variant
- `junkyard.png` (1400x700) — chain-link fence, JUNKYARD sign, crushed-car stack,
  3 junkers (rust/blue/gray), 2 tire mountains, office trailer, scrap pile, oil stains

### Suburban houses (modular)
- `suburban_house_1.png` (1000x640) — brick ranch: mortar coursing, gray roof, garage,
  red door, shuttered windows, chimney, driveway, walkway, bushes
- `suburban_house_2.png` (1000x680) — two-story beige siding: column porch, shuttered
  windows, blue door, garage, chimney, driveway

### Commercial strip
- `strip_mall.png` (1400x560) — "GOODVILLE PLAZA": LIQUOR / PAWN SHOP / LAUNDROMAT / $ DOLLAR $,
  parapet roof, doors + windows per unit, sidewalk (sign text auto-fit so nothing overflows)
- `gas_station.png` (1100x620) — GOODVILLE GAS canopy, 2 pumps on islands, pylon sign with
  price 2.99, PAY kiosk, concrete pad

### Goodville anchor
- `goodville_sign.png` (820x640) — wooden town sign SP-style: "GOODVILLE",
  "POP. 2147 - ELEV 597 FT", "WELCOME, Y'ALL" board, bullet holes, grass tufts

### props/ (19 modular pieces)
tire, tire_stack, lawn_chair, grill, trash_can, mailbox, satellite_dish, rusty_pickup,
dumpster, propane_tank, shopping_cart, streetlamp, power_pole, stop_sign, fire_hydrant,
pine_tree, oak_tree, bush, tennessee_hill

## Notes for parent
- Night scene windows are lit from recorded window rects (HOME_WINDOWS in build.py) —
  if a home piece is edited, re-record its window rects or the night scene misfires.
- Junkyard is labeled "JUNKYARD" (no invented business name, per no-invented-canon).
- No git touched; parent collects from /tmp. If this should persist, commit to
  trippedd-studio under goodville/environments/ (branch -> PR -> merge per repo law).
