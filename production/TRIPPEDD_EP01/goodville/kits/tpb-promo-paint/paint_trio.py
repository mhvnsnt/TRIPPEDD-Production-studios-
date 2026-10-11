#!/usr/bin/env python3
"""TPB trio promo — hand-painted in the AI key-art style. PIL/OpenCV only, zero AI imagery."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

random.seed(7)
W, H = 1920, 1080

# ---- palette sampled from the key art ----
SKIN      = (232, 194, 157)
SKIN_DK   = (198, 142, 102)
SKIN_LT   = (248, 221, 190)
BLUSH     = (232, 155, 122)
HAIR_DK   = (72, 45, 26)
HAIR_MID  = (110, 74, 44)
HAIR_LT   = (166, 124, 78)
SKY_TOP   = (74, 158, 208)
SKY_BOT   = (184, 224, 240)
MTN       = (28, 104, 78)
MTN_DK    = (18, 74, 56)
SNOW      = (244, 248, 250)
SNOW_SH   = (200, 221, 232)
WOOD      = (84, 49, 33)
WOOD_DK   = (62, 36, 23)
SIGN_YEL  = (249, 201, 43)
ROAD      = (138, 141, 144)
ROAD_DK   = (110, 113, 116)
PINE      = (30, 74, 58)
OUTLINE   = (58, 36, 24)
TOQUE     = (32, 44, 88)
SHIRT_RED = (148, 44, 48)
PANTS_BLUE= (52, 84, 150)
STRIPE_NV = (36, 52, 110)
STRIPE_CR = (232, 228, 214)
TEE_BLACK = (34, 32, 34)
KHAKI     = (150, 134, 104)
KITTY     = (232, 150, 80)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def vgrad(w, h, top, bottom):
    t = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(top, dtype=float) * (1 - t) + np.array(bottom, dtype=float) * t
    return np.repeat(arr, w, axis=1).astype(np.uint8)

def radial_mask(w, h, cx, cy, r0, r1):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    m = np.clip((d - r0) / max(1, (r1 - r0)), 0, 1)
    return m  # 0 inside r0, 1 outside r1

def soft_blob(base, x, y, r, color, alpha=0.5, blur=30):
    """Paint a soft radial blob onto RGBA base."""
    s = int(r * 2 + blur * 4)
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([blur * 2, blur * 2, s - blur * 2, s - blur * 2],
              fill=color + (int(255 * alpha),))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(lay, (int(x - s / 2), int(y - s / 2)))

def tapered_curve(draw, pts, w0, w1, color):
    """Draw a tapered curve as stamped circles along a quadratic bezier."""
    (x0, y0), (x1, y1), (x2, y2) = pts
    n = 24
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t ** 2 * x2
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t ** 2 * y2
        w = w0 + (w1 - w0) * t
        draw.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=color)

def grain(base, amount=6):
    arr = np.array(base.convert("RGB")).astype(int)
    n = np.random.randint(-amount, amount + 1, arr.shape)
    arr = np.clip(arr + n, 0, 255).astype(np.uint8)
    return Image.fromarray(arr).convert("RGBA")

def text_stroke(draw, xy, s, font, fill, stroke, sw):
    draw.text(xy, s, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke,
             anchor="mm")
