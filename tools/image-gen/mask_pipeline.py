"""Owner mask pipeline (owner 2026-10-11).
When the assistant's auto-cut is wrong, the owner hand-edits a mask and shares it.
This pipeline applies owner masks + pattern fills cleanly.

Usage:
  python3 mask_pipeline.py <character.png> <mask.png> <tile.png> <output.png>
  python3 mask_pipeline.py <character.png> <mask.png> --cutout <output.png>

Mask convention: white = keep/fill, black = remove/skip.
"""
from PIL import Image
import numpy as np
import sys

def apply_mask_pattern(character_path, mask_path, tile_path, output_path):
    """Fill mask area with pattern tile."""
    char = Image.open(character_path).convert('RGBA')
    mask_img = Image.open(mask_path).convert('L')
    if mask_img.size != char.size:
        mask_img = mask_img.resize(char.size, Image.LANCZOS)
    mask = np.array(mask_img) > 128
    tile = Image.open(tile_path).convert('RGBA')
    sw, sh = char.size
    tiled = Image.new('RGBA', (sw, sh), (0,0,0,0))
    for y in range(0, sh, tile.height):
        for x in range(0, sw, tile.width):
            tiled.paste(tile, (x, y))
    shape = Image.new('RGBA', char.size, (0,0,0,0))
    sa = np.array(shape)
    sa[mask] = [255,255,255,255]
    shape = Image.fromarray(sa)
    filled = Image.new('RGBA', char.size, (0,0,0,0))
    filled.paste(tiled, (0,0), shape)
    result = char.copy()
    result.paste(filled, (0,0), filled)
    result.save(output_path)
    print(f'pattern applied -> {output_path}')
    return output_path

def apply_mask_cutout(character_path, mask_path, output_path):
    """Cut character to mask shape (transparent outside)."""
    char = Image.open(character_path).convert('RGBA')
    mask_img = Image.open(mask_path).convert('L')
    if mask_img.size != char.size:
        mask_img = mask_img.resize(char.size, Image.LANCZOS)
    mask = np.array(mask_img) > 128
    ca = np.array(char)
    out = np.zeros_like(ca)
    out[mask] = ca[mask]
    Image.fromarray(out).save(output_path)
    print(f'cutout -> {output_path}')
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    if sys.argv[3] == '--cutout':
        apply_mask_cutout(sys.argv[1], sys.argv[2], sys.argv[4])
    else:
        apply_mask_pattern(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
