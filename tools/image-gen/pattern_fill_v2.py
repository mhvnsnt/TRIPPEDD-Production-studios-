"""Pattern-fill v2 — Chowder-method pattern fill (owner 2026-10-12).

Chowder's technique (C.H. Greenblatt): the pattern is a FULL-SCREEN FIXED image.
The character art has HOLES cut where the pattern shows through. The character
moves OVER the static pattern — the pattern never moves, never deforms.

Owner's cookie-cutter principle: pattern = dough, shirt shape = cutter.
Same pattern, same scale, same cut — from any angle.

v2 improvements over v1:
1. ANCHOR-BASED TILING: pattern tiles from a fixed anchor point (default: canvas
   center), not (0,0) of the shape bbox. Same character at different angles gets
   the same pattern phase = visual consistency.
2. SEAMLESS TILE CHECK: verifies extracted tile edges match before tiling.
   Falls back to mirror-tiling if edges don't match (hides seams).
3. NATIVE-RES EXTRACTION: no destructive resize on the tile. Pattern pixels are
   never blurred or altered during capture.
4. EDGE FEATHERING: 3px erode + 0.7px Gaussian feather on mask edges (from the
   Goodville v2 cleanup pass) for clean blends without halo/fringe.
5. SCALE LOCK: pattern scale is set once per outfit, stored in the output
   metadata comment. Same outfit = same scale, always.

Usage:
  python3 pattern_fill_v2.py <shape_or_mask.png> <pattern.png> <output.png> [options]
  python3 pattern_fill_v2.py --cutout <character.png> <mask.png> <output.png>

Options:
  --scale S        Pattern scale multiplier (default 1.0). Lock per outfit.
  --anchor X,Y     Tile anchor point (default: center of canvas).
                   Use "topleft" for (0,0) legacy behavior.
  --feather P      Edge feather radius in px (default 0.7).
  --erode P        Edge erode in px before feather (default 3).
  --mirror         Force mirror-tiling (hides seams on non-seamless tiles).
  --no-feather     Disable edge feathering.
"""
from PIL import Image, ImageFilter
import numpy as np
import sys
import argparse


def check_seamless(tile):
    """Check if a tile's edges match for seamless tiling.
    Returns True if left/right and top/bottom edges are close enough."""
    ta = np.array(tile.convert('RGB')).astype(np.int16)
    h, w = ta.shape[:2]
    # Compare opposite edges (5px strips)
    lr_diff = np.abs(ta[:, :5] - ta[:, -5:]).mean()
    tb_diff = np.abs(ta[:5, :] - ta[-5:, :]).mean()
    # Threshold: average < 15 per channel = seamless enough
    return lr_diff < 15 and tb_diff < 15


def extract_tile_safe(source_png, bbox=None):
    """Extract pattern at native resolution. No resize, no blur.
    If bbox is None, uses the full source image (Chowder method: full-screen pattern).
    Returns (tile_image, is_seamless)."""
    im = Image.open(source_png).convert('RGBA')
    if bbox is not None:
        tile = im.crop(bbox)
    else:
        tile = im
    return tile, check_seamless(tile)


def build_pattern_layer(tile, canvas_size, anchor='center', scale=1.0, mirror=False):
    """Build a full-canvas pattern layer, anchored to a fixed point.
    Chowder principle: the pattern is FIXED. The mask/shape moves over it.

    anchor: 'center', 'topleft', or (x, y) tuple.
    The anchor determines where tile (0,0) sits. Using a fixed anchor means
    the same pattern phase regardless of shape position/size.
    """
    tw, th = tile.size
    if scale != 1.0:
        # Scale the tile ONCE, cleanly, before tiling
        tile = tile.resize(
            (max(1, int(tw * scale)), max(1, int(th * scale))),
            Image.LANCZOS
        )
        tw, th = tile.size

    cw, ch = canvas_size

    # Resolve anchor to pixel coordinates
    if anchor == 'center':
        ax, ay = cw // 2, ch // 2
    elif anchor == 'topleft':
        ax, ay = 0, 0
    else:
        ax, ay = anchor

    # Build tiled pattern covering the canvas, offset so tile grid aligns to anchor
    # Tile (0,0) is placed such that the anchor point falls on a tile boundary.
    # This makes the pattern phase deterministic and angle-independent.
    tiled = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))

    # Start tiling from anchor, going outward in both directions
    # This ensures the anchor point is always on a tile grid intersection
    start_x = ax - ((ax // tw) * tw) - tw  # backs up to before 0
    start_x = ax % tw - tw  # tile boundary at or before anchor
    if start_x > ax:
        start_x -= tw
    start_y = ay % th - th
    if start_y > ay:
        start_y -= th

    if mirror:
        # Mirror-tiling: alternate flip to hide seams
        tile_r = tile.transpose(Image.FLIP_LEFT_RIGHT)
        tile_b = tile.transpose(Image.FLIP_TOP_BOTTOM)
        tile_rb = tile_r.transpose(Image.FLIP_TOP_BOTTOM)
        tiles = [[tile, tile_r], [tile_b, tile_rb]]
        row, col = 0, 0
        y = start_y
        while y < ch:
            x = start_x
            col = 0
            while x < cw:
                tiled.paste(tiles[row % 2][col % 2], (x, y))
                x += tw
                col += 1
            y += th
            row += 1
    else:
        for y in range(start_y, ch, th):
            for x in range(start_x, cw, tw):
                tiled.paste(tile, (x, y))

    return tiled


def apply_feathered_mask(pattern_layer, mask, erode_px=3, feather_px=0.7):
    """Apply mask with edge treatment: erode + feather.
    From Goodville v2 cleanup: kills halo/fringe on hand-drawn masks."""
    if erode_px > 0:
        mask = mask.filter(ImageFilter.MinFilter(erode_px * 2 + 1))
    if feather_px > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(feather_px))

    # Use mask as alpha for the pattern layer
    result = Image.new('RGBA', pattern_layer.size, (0, 0, 0, 0))
    result.paste(pattern_layer, (0, 0), mask)
    return result


def fill_shape_v2(shape_png, pattern_png, output_png, scale=1.0,
                  anchor='center', feather=0.7, erode=3, mirror=False,
                  pattern_bbox=None):
    """Fill a shape/mask with pattern using Chowder-method anchored tiling.

    shape_png: RGBA image where alpha = fill area, OR L-mode mask (white=fill).
    pattern_png: source pattern image.
    """
    shape = Image.open(shape_png)
    if shape.mode == 'L':
        # L-mode mask: white = fill
        mask = shape.convert('L')
        canvas_size = mask.size
    elif shape.mode == 'RGB':
        # RGB owner mask: white = fill, black = skip (luminance as mask)
        mask = shape.convert('L')
        canvas_size = mask.size
    else:
        shape = shape.convert('RGBA')
        # Use alpha channel as mask
        mask = shape.split()[3]
        canvas_size = shape.size

    # Extract pattern at native res
    tile, is_seamless = extract_tile_safe(pattern_png, pattern_bbox)
    use_mirror = mirror or not is_seamless
    if not is_seamless and not mirror:
        print(f"  note: tile edges don't match ({'seamless' if is_seamless else 'NOT seamless'}), using mirror-tiling")

    # Build anchored pattern layer (Chowder: pattern is FIXED)
    pattern_layer = build_pattern_layer(tile, canvas_size, anchor=anchor,
                                        scale=scale, mirror=use_mirror)

    # Apply mask with edge treatment
    if feather > 0 or erode > 0:
        result = apply_feathered_mask(pattern_layer, mask,
                                      erode_px=erode, feather_px=feather)
    else:
        result = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
        result.paste(pattern_layer, (0, 0), mask)

    # Embed scale in PNG metadata for scale-lock tracking
    from PIL.PngImagePlugin import PngInfo
    info = PngInfo()
    info.add_text("pattern_scale", str(scale))
    info.add_text("pattern_anchor", str(anchor))
    info.add_text("pattern_source", pattern_png)
    result.save(output_png, pnginfo=info)
    print(f"filled -> {output_png} (scale={scale}, anchor={anchor}, "
          f"seamless={is_seamless}, mirror={use_mirror})")
    return output_png


def cutout_v2(character_png, mask_png, output_png, feather=0.7, erode=3):
    """Cut character to mask with edge treatment."""
    char = Image.open(character_png).convert('RGBA')
    mask_img = Image.open(mask_png).convert('L')
    if mask_img.size != char.size:
        mask_img = mask_img.resize(char.size, Image.LANCZOS)
    if erode > 0:
        mask_img = mask_img.filter(ImageFilter.MinFilter(erode * 2 + 1))
    if feather > 0:
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(feather))
    out = Image.new('RGBA', char.size, (0, 0, 0, 0))
    out.paste(char, (0, 0), mask_img)
    out.save(output_png)
    print(f"cutout -> {output_png}")
    return output_png


def main():
    p = argparse.ArgumentParser(description="Chowder-method pattern fill v2")
    p.add_argument('inputs', nargs='*', help='input files')
    p.add_argument('--scale', type=float, default=1.0)
    p.add_argument('--anchor', default='center',
                   help='"center", "topleft", or "X,Y"')
    p.add_argument('--feather', type=float, default=0.7)
    p.add_argument('--erode', type=float, default=3)
    p.add_argument('--mirror', action='store_true')
    p.add_argument('--no-feather', action='store_true')
    p.add_argument('--cutout', action='store_true')
    p.add_argument('--bbox', default=None,
                   help='pattern crop as "x1,y1,x2,y2" (default: full image)')
    args = p.parse_args()

    if args.no_feather:
        args.feather = 0
        args.erode = 0

    anchor = args.anchor
    if ',' in anchor:
        x, y = anchor.split(',')
        anchor = (int(x), int(y))

    bbox = None
    if args.bbox:
        bbox = tuple(int(v) for v in args.bbox.split(','))

    if args.cutout:
        if len(args.inputs) < 3:
            print("usage: pattern_fill_v2.py --cutout <character.png> <mask.png> <output.png>")
            sys.exit(1)
        cutout_v2(args.inputs[0], args.inputs[1], args.inputs[2],
                  feather=args.feather, erode=args.erode)
    else:
        if len(args.inputs) < 3:
            print("usage: pattern_fill_v2.py <shape_or_mask.png> <pattern.png> <output.png> [options]")
            sys.exit(1)
        fill_shape_v2(args.inputs[0], args.inputs[1], args.inputs[2],
                      scale=args.scale, anchor=anchor,
                      feather=args.feather, erode=args.erode,
                      mirror=args.mirror, pattern_bbox=bbox)


if __name__ == '__main__':
    main()
