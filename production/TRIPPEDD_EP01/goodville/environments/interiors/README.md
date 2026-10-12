# Goodville Interior Props

South Park flat cutout style interior furniture for TRIPPEDD EP01 / Goodville.
All pieces: procedural Python PIL, FLAT colors (no gradients), bold black outlines (4-6px),
paper-cutout look, transparent PNG backgrounds.

Generator: `build_interiors.py` — re-run to regenerate all pieces.

## Living room

| File | Size (w x h) | Description |
|---|---|---|
| couch_blue.png | 560 x 340 | 3-seat couch, front view; separate rounded-rect cushions |
| couch_arm_detail.png | 240 x 280 | Armrest closeup piece |
| tv_off.png | 420 x 320 | Flat TV, dark screen, reflection stripe |
| tv_on.png | 420 x 320 | Same TV, colorful cartoon scene on screen |
| tv_stand.png | 460 x 260 | Wooden TV stand, two cabinet doors |
| coffee_table.png | 480 x 240 | Rectangular coffee table + lower shelf |
| lamp_floor.png | 200 x 580 | Floor lamp: trapezoid shade, pole, disc base |
| lamp_table.png | 220 x 400 | Table lamp, purple stem + lavender shade |
| bookshelf.png | 380 x 540 | Bookshelf, 4 shelves of colorful book spines + stacked bottom shelf |
| rug_oval.png | 540 x 340 | Oval rug, concentric rings + diamond band |
| wall_clock.png | 220 x 220 | Wall clock, 12 tick marks, 10:09 hands |

## Kitchen

| File | Size (w x h) | Description |
|---|---|---|
| fridge_closed.png | 340 x 580 | Fridge, closed; top freezer + bottom fridge doors, handles |
| fridge_open.png | 560 x 580 | Fridge with door swung open; shelves with food items, interior light |
| stove.png | 400 x 460 | Stove: 4 burners, control panel knobs, oven door + window |
| kitchen_table.png | 460 x 320 | Round wooden kitchen table |
| chair_wood.png | 240 x 480 | Wooden chair, front view; slatted back, crossbar |
| sink_counter.png | 560 x 340 | Counter with sink basin, faucet, soap bottle, cabinet doors |
| microwave.png | 360 x 260 | Microwave: window with food silhouette, green display, button grid |

## Usage notes

- All PNGs are RGBA; drop straight onto backgrounds in Blender/PIL compositing.
- Sizes are furniture-scale (~300-600px wide); scale down for distant shots, never up beyond 1.5x.
- Style lock: flat fills only, 4-6px outlines, no shading gradients — matches Goodville Cartoon locked key-art look.
