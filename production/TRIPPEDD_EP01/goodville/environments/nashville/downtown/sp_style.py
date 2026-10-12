"""Shared South Park flat-style helpers for the Nashville build.
Bold black outlines, flat colors, transparent PNG backgrounds.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BLACK = (10, 10, 12, 255)
WHITE = (245, 245, 242, 255)

def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

def poly(draw, pts, fill, outline=BLACK, width=8):
    draw.polygon(pts, fill=fill, outline=outline, width=width)

def rect(draw, box, fill, outline=BLACK, width=8):
    draw.rectangle(box, fill=fill, outline=outline, width=width)

def ellipse(draw, box, fill, outline=BLACK, width=8):
    draw.ellipse(box, fill=fill, outline=outline, width=width)

def line(draw, pts, fill=BLACK, width=8):
    draw.line(pts, fill=fill, width=width, joint="curve")

def window_grid(draw, x0, y0, cols, rows, ww, wh, gx, gy,
                glass_day=(38, 52, 74, 255), glass_night=(8, 10, 18, 255),
                lit=(255, 196, 84, 255), night=False, lit_ratio=0.45, seed=7,
                outline_w=5):
    """Draw a grid of windows. Returns nothing; draws on `draw`."""
    rng = random.Random(seed)
    for r in range(rows):
        for c in range(cols):
            x = x0 + c * (ww + gx)
            y = y0 + r * (wh + gy)
            if night:
                on = rng.random() < lit_ratio
                fill = lit if on else glass_night
            else:
                fill = glass_day
            draw.rectangle([x, y, x + ww, y + wh], fill=fill,
                           outline=BLACK, width=outline_w)

def neon_text(base_img, xy, text, size, color, glow_color=None, bold=True):
    """Draw neon tube text with glow onto base_img (RGBA). xy = top-left."""
    glow_color = glow_color or color
    f = font(size, bold)
    # glow layer: draw text blurred underneath
    glow = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for ox, oy in [(-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)]:
        gd.text((xy[0] + ox, xy[1] + oy), text, font=f, fill=glow_color)
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    base_img.alpha_composite(glow)
    d = ImageDraw.Draw(base_img)
    # tube: bright core
    d.text(xy, text, font=f, fill=(255, 255, 255, 255))
    # colored halo copy slightly offset for tube effect
    d2 = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(d2)
    dd.text(xy, text, font=f, fill=color)
    d2 = d2.filter(ImageFilter.GaussianBlur(2))
    base_img.alpha_composite(d2)
    return base_img

def neon_shape(base_img, draw_fn, color):
    """Draw a neon shape: draw_fn(draw) draws in white on temp layer; we add glow."""
    glow = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    draw_fn(gd, color)
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    base_img.alpha_composite(glow)
    d = ImageDraw.Draw(base_img)
    draw_fn(d, (255, 255, 255, 255))
    # tint pass so the tube carries its color like neon_text does
    tint = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(tint)
    draw_fn(td, color)
    tint = tint.filter(ImageFilter.GaussianBlur(2))
    base_img.alpha_composite(tint)
    return base_img

def text_center(draw, cx, y, text, size, fill, bold=True, stroke=0):
    f = font(size, bold)
    bb = draw.textbbox((0, 0), text, font=f)
    w = bb[2] - bb[0]
    if stroke:
        draw.text((cx - w / 2, y), text, font=f, fill=fill,
                  stroke_width=stroke, stroke_fill=BLACK)
    else:
        draw.text((cx - w / 2, y), text, font=f, fill=fill)
