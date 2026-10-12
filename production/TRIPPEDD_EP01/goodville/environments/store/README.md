# Goodville — Store Environment Pieces

South Park flat-construction set for the corner store in gag #5 ("The Serious
Guys"). Simple geometric shapes, bold black outlines (4-6px), flat colors,
transparent PNG backgrounds, paper-cutout look.

Built procedurally: `build_store.py` (`python3 build_store.py` regenerates all).

| File | Size | Description |
|---|---|---|
| `storefront.png` | 1200x820 | Store exterior front: sign band, striped awning, glass door, two big windows with product silhouettes |
| `store_sign_blank.png` | 1000x160 | Blank red sign band with white inner border — overlay text on it later |
| `store_door_closed.png` | 300x560 | Glass door, closed: frame, push bar, kick plate |
| `store_door_open.png` | 300x560 | Glass door, open: dark interior gap, angled door panel, handle |
| `store_window.png` | 520x420 | Storefront window: mullions, product display, SALE poster |
| `shelf_empty.png` | 520x620 | Shelf unit, empty: 4 wood shelves on 2 uprights |
| `shelf_stocked.png` | 520x620 | Same shelf stocked: colorful boxes (top/bottom rows) and cans |
| `counter.png` | 640x320 | Checkout counter: top slab, front panel, kick strip |
| `cash_register.png` | 360x380 | Register: display showing $0.00, key grid, drawer |
| `cooler_door.png` | 420x680 | Beverage cooler: DRINKS header, glass door, 3 shelves of drinks, handle bar |
| `store_interior_backwall.png` | 1600x720 | Wide back wall: top band + 3 stocked shelf bays |

Notes:
- `storefront.png` carries a generic "STORE" sign; swap in `store_sign_blank.png`
  with composited text for the final gag-specific signage.
- Keep text overlays in the same flat bold style (DejaVu Sans Bold used here).
