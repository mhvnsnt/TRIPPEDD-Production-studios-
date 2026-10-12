"""Pattern-fill for repeating-pattern garments (owner 2026-10-11).
Method: extract pattern tile from good angle -> fill shirt silhouette at any angle.
Pattern doesn't need to be pixel-exact, just the same pattern in the same cut/shape.
Like a cookie cutter: pattern = dough, shirt shape = cutter.
"""
from PIL import Image
import numpy as np

def extract_tile(source_png, bbox):
    """Extract a pattern tile from a good donor piece."""
    im = Image.open(source_png).convert('RGBA')
    return im.crop(bbox)

def fill_shape(shape_png, tile_png, output_png, tile_scale=1.0):
    """Fill a shirt silhouette with the pattern tile."""
    shape = Image.open(shape_png).convert('RGBA')
    tile = Image.open(tile_png).convert('RGBA')
    if tile_scale != 1.0:
        tile = tile.resize((int(tile.width*tile_scale), int(tile.height*tile_scale)), Image.LANCZOS)
    # tile the pattern to cover the shape
    sw, sh = shape.size
    tiled = Image.new('RGBA', (sw, sh), (0,0,0,0))
    for y in range(0, sh, tile.height):
        for x in range(0, sw, tile.width):
            tiled.paste(tile, (x, y))
    # mask by shape alpha
    result = Image.new('RGBA', (sw, sh), (0,0,0,0))
    result.paste(tiled, (0,0), shape)
    result.save(output_png)
    return output_png

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print("usage: pattern_fill.py <shape.png> <tile.png> <output.png> [scale]")
        sys.exit(1)
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    fill_shape(sys.argv[1], sys.argv[2], sys.argv[3], scale)
    print(f"filled -> {sys.argv[3]}")
