#!/usr/bin/env python3
"""Generate a minimal but valid Blu-ray PGS (.sup) file with one caption.

Two display sets:
  DS1 @ PTS 1.0s: PCS(normal, 1 object) + WDS + PDS + ODS(RLE text bitmap) + END
  DS2 @ PTS 4.0s: PCS(normal, 0 objects) + END  (clears the caption)

Bitmap is rendered with PIL/DejaVuSans (system font) — fully synthetic,
license-clean input for the BDSup2Sub smoke test.
"""
import struct, sys
from PIL import Image, ImageDraw, ImageFont

VIDEO_W, VIDEO_H = 1920, 1080
WIN_X, WIN_Y, WIN_W, WIN_H = 560, 880, 800, 140
TEXT = "WIZARD GANG"
SUBTEXT = "PGS caption smoke test"

def render_bitmap():
    img = Image.new("L", (WIN_W, WIN_H), 0)
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    d.text((WIN_W // 2, 18), TEXT, font=f1, anchor="ma", fill=255)
    d.text((WIN_W // 2, 92), SUBTEXT, font=f2, anchor="ma", fill=255)
    # 3-level palette: 0 = transparent, 1 = white text, 2 = black edge
    px = img.load()
    out = bytearray(WIN_W * WIN_H)
    for y in range(WIN_H):
        for x in range(WIN_W):
            v = px[x, y]
            out[y * WIN_W + x] = 1 if v > 128 else 0
    # crude 1px black outline around text (dilate inverse)
    edge = bytearray(out)
    for y in range(1, WIN_H - 1):
        for x in range(1, WIN_W - 1):
            i = y * WIN_W + x
            if out[i] == 0 and any(out[i + dy * WIN_W + dx] == 1
                                   for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                edge[i] = 2
    return bytes(edge)

def rle_encode(bitmap, w, h):
    """BDSup2Sub's RLE dialect (see SupBD.java decodeBitmap):
       00 00 = EOL; 00 01..3F = short zero run; 00 40..7F yy = long zero run
       (((b-0x40)<<8)+yy); 00 80..BF c = short color run (b-0x80 of c);
       00 C0..FF yy c = long color run (((b-0xC0)<<8)+yy of c)."""
    out = bytearray()
    for y in range(h):
        row = bitmap[y * w:(y + 1) * w]
        x = 0
        while x < w:
            c = row[x]
            n = 1
            while x + n < w and row[x + n] == c and n < 16383:
                n += 1
            if n == 1 and c != 0:
                out.append(c)
            elif c == 0:
                if n < 0x40:
                    out += bytes([0x00, n])
                else:
                    out += bytes([0x00, 0x40 | (n >> 8), n & 0xFF])
            else:
                if n < 0x80:
                    out += bytes([0x00, 0x80 | n, c])
                else:
                    out += bytes([0x00, 0xC0 | (n >> 8), n & 0xFF, c])
            x += n
        out += bytes([0x00, 0x00])  # end of line
    return bytes(out)

def seg(segtype, pts, payload):
    return (b"PG" + struct.pack(">II", pts, 0) + bytes([segtype]) +
            struct.pack(">H", len(payload)) + payload)

def pcs(pts, comp_num, n_objects, obj_pos=None, state=0x00):
    p = struct.pack(">HHB", VIDEO_W, VIDEO_H, 0x10)  # 16 fps-ish rate byte
    p += struct.pack(">HBB", comp_num, state, 0x00)  # state, no pal update
    p += struct.pack(">BB", 0x00, n_objects)         # palette id, n objects
    if n_objects:
        ox, oy = obj_pos
        p += struct.pack(">HBB", 0x0000, 0x00, 0x00)  # obj id, window id, cropped=0
        p += struct.pack(">HH", ox, oy)
    return seg(0x16, pts, p)

def wds(pts):
    p = struct.pack(">B", 1)
    p += struct.pack(">BHHHH", 0x00, WIN_X, WIN_Y, WIN_W, WIN_H)
    return seg(0x17, pts, p)

def pds(pts):
    p = struct.pack(">BB", 0x00, 0x01)  # palette id, version
    # entry: id, Y, Cr, Cb, Alpha
    p += bytes([0, 16, 128, 128, 0])      # 0: transparent
    p += bytes([1, 235, 128, 128, 255])    # 1: white
    p += bytes([2, 16, 128, 128, 255])     # 2: black edge
    return seg(0x14, pts, p)

def ods(pts, rle):
    obj_data = struct.pack(">HH", WIN_W, WIN_H) + rle
    p = struct.pack(">HBB", 0x0000, 0x00, 0xC0)  # obj id, ver, last-in-seq
    p += len(obj_data).to_bytes(3, "big") + obj_data
    return seg(0x15, pts, p)

def end(pts):
    return seg(0x80, pts, b"")

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "smoke.sup"
    bitmap = render_bitmap()
    rle = rle_encode(bitmap, WIN_W, WIN_H)
    data = bytearray()
    data += pcs(90000, 0, 1, (WIN_X, WIN_Y), state=0x80)  # epoch start
    data += wds(90000)
    data += pds(90000)
    data += ods(90000, rle)
    data += end(90000)
    data += pcs(360000, 1, 0)
    data += end(360000)
    open(path, "wb").write(bytes(data))
    nonzero = sum(1 for b in bitmap if b)
    print(f"wrote {path} ({len(data)} bytes, 2 display sets, bitmap {WIN_W}x{WIN_H}, "
          f"{nonzero} opaque px, RLE {len(rle)} bytes)")

if __name__ == "__main__":
    main()
