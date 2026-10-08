#!/usr/bin/env python3
"""spritesheet_packer/packer.py — pack EP02 stills thumbnails into a sprite
sheet + JSON atlas. Shelf algorithm: sort thumbs by height desc, fill shelves
left-to-right at a fixed max sheet width, new shelf when a thumb won't fit.
Writes proofs/spritesheet.png, proofs/atlas.json, proofs/thumbs/*.png.
"""
import hashlib, json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PROOFS = os.path.join(HERE, "proofs")
THUMBS = os.path.join(PROOFS, "thumbs")
MAX_W, THUMB_W, PAD = 1024, 256, 4

SOURCES = [
    "production/WIZARD_GANG_EP01/ep02-stills/ep02-shot-10-1.png",
    "production/WIZARD_GANG_EP01/ep02-stills/ep02-shot-11-3.png",
    "production/WIZARD_GANG_EP01/ep02-stills/ep02-shot-12-1.png",
    "production/WIZARD_GANG_EP01/ep02-stills-review/ep02-stills-act1.jpg",
    "production/WIZARD_GANG_EP01/ep02-stills-review/ep02-full-lineup.jpg",
    "production/WIZARD_GANG_EP01/ep02-stills-review/ep02-title-card.png",
]

def main():
    os.makedirs(THUMBS, exist_ok=True)
    items = []
    for s in SOURCES:
        src = os.path.join(REPO, s)
        assert os.path.exists(src), f"missing source: {s}"
        im = Image.open(src).convert("RGB")
        w = THUMB_W
        h = round(im.height * THUMB_W / im.width)
        th = im.resize((w, h), Image.LANCZOS)
        name = os.path.splitext(os.path.basename(s))[0]
        tp = os.path.join(THUMBS, name + ".png")
        th.save(tp)
        items.append((name, w, h, tp))
    items.sort(key=lambda t: -t[2])  # tallest first -> better shelves
    shelves, cur, x, y = [], [], PAD, PAD
    shelf_h = 0
    for name, w, h, tp in items:
        if x + w + PAD > MAX_W and cur:
            shelves.append((cur, shelf_h)); cur, x, y = [], PAD, y + shelf_h + PAD
            shelf_h = 0
        cur.append((name, x, y, w, h, tp)); x += w + PAD
        shelf_h = max(shelf_h, h)
    if cur:
        shelves.append((cur, shelf_h))
    sheet_h = y + shelf_h + PAD
    sheet = Image.new("RGB", (MAX_W, sheet_h), (16, 16, 24))
    atlas = {}
    for shelf, _ in shelves:
        for name, sx, sy, w, h, tp in shelf:
            sheet.paste(Image.open(tp), (sx, sy))
            atlas[name] = {"x": sx, "y": sy, "w": w, "h": h}
    sp = os.path.join(PROOFS, "spritesheet.png")
    ap = os.path.join(PROOFS, "atlas.json")
    sheet.save(sp)
    json.dump({"sheet": "spritesheet.png", "width": MAX_W, "height": sheet_h,
               "frames": atlas}, open(ap, "w"), indent=2)
    print(f"packed {len(items)} thumbs -> {sp} ({MAX_W}x{sheet_h})")

if __name__ == "__main__":
    main()
