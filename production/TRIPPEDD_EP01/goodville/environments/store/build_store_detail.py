#!/usr/bin/env python3
"""Goodville store DETAIL pieces — South Park flat cutout style.
Product labels, price tags, posters, floor tiles, ceiling lights,
window display items. Transparent PNGs."""
from PIL import Image, ImageDraw
import os, random

OUT = os.path.dirname(os.path.abspath(__file__))
BLK = (0, 0, 0, 255)
random.seed(31)

def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# ------------------------------------------------ product labels (shelf items)
def product_jar(color, label, name, w=90, h=130):
    img = canvas(w+20, h+20)
    d = ImageDraw.Draw(img)
    # jar body
    d.rectangle([15, 35, w+5, h+10], fill=(240, 240, 235, 255), outline=BLK, width=4)
    # lid
    d.rectangle([20, 12, w, 38], fill=(180, 60, 60, 255), outline=BLK, width=4)
    # label
    d.rectangle([22, 60, w-2, h-8], fill=color, outline=BLK, width=2)
    d.text(((w+20)//2, (h+52)//2), label, fill=(255,255,255,255), anchor="mm")
    img.save(f"{OUT}/{name}")

product_jar((200, 120, 40, 255), "BEANS", "product_beans.png")
product_jar((80, 150, 80, 255), "PEAS", "product_peas.png")
product_jar((200, 60, 60, 255), "SOUP", "product_soup.png")

def product_box(color, label, name, w=110, h=140):
    img = canvas(w+20, h+20)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, w+10, h+10], fill=color, outline=BLK, width=4)
    d.rectangle([22, 30, w-2, 80], fill=(255,255,255,255), outline=BLK, width=2)
    d.text(((w+20)//2, 110), label, fill=(255,255,255,255), anchor="mm")
    img.save(f"{OUT}/{name}")

product_box((60, 120, 200, 255), "FLAKES", "product_cereal.png")
product_box((230, 150, 50, 255), "CHIPS", "product_chips.png")

def product_bottle(color, label, name):
    img = canvas(80, 170)
    d = ImageDraw.Draw(img)
    # neck
    d.rectangle([30, 10, 50, 50], fill=color, outline=BLK, width=3)
    d.rectangle([26, 5, 54, 18], fill=(150, 150, 150, 255), outline=BLK, width=3)
    # body
    d.rounded_rectangle([12, 48, 68, 160], radius=12, fill=color, outline=BLK, width=4)
    d.rectangle([18, 90, 62, 125], fill=(255,255,255,255), outline=BLK, width=2)
    d.text((40, 107), label, fill=(30,30,30,255), anchor="mm")
    img.save(f"{OUT}/{name}")

product_bottle((200, 60, 50, 255), "POP", "product_soda.png")
product_bottle((70, 140, 80, 255), "JUICE", "product_juice.png")

# ------------------------------------------------ price tags
def price_tag(price, name):
    img = canvas(130, 80)
    d = ImageDraw.Draw(img)
    d.polygon([(10, 10), (100, 10), (120, 40), (100, 70), (10, 70)],
              fill=(255, 240, 150, 255), outline=BLK, width=4)
    d.ellipse([14, 32, 26, 48], fill=(255,255,255,255), outline=BLK, width=2)
    d.text((65, 40), price, fill=(200, 40, 40, 255), anchor="mm")
    img.save(f"{OUT}/{name}")

price_tag("$1.99", "price_199.png")
price_tag("$0.99", "price_099.png")
price_tag("SALE", "price_sale.png")

# ------------------------------------------------ posters (3)
def poster(bg, name, draw_fn):
    img = canvas(220, 300)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 210, 290], fill=bg, outline=BLK, width=5)
    draw_fn(d)
    img.save(f"{OUT}/{name}")

def _p_beer(d):
    d.text((110, 60), "COLD", fill=(255,255,255,255), anchor="mm")
    d.text((110, 100), "BEER", fill=(255,255,255,255), anchor="mm")
    d.rectangle([70, 140, 150, 240], fill=(220, 170, 60, 255), outline=BLK, width=4)
    d.rectangle([70, 140, 150, 165], fill=(255,255,255,255), outline=BLK, width=3)
def _p_missing(d):
    d.text((110, 50), "MISSING", fill=(200, 40, 40, 255), anchor="mm")
    d.ellipse([70, 90, 150, 170], fill=(240, 210, 170, 255), outline=BLK, width=3)
    d.text((110, 210), "HAVE YOU", fill=(30,30,30,255), anchor="mm")
    d.text((110, 240), "SEEN ME?", fill=(30,30,30,255), anchor="mm")
def _p_sale(d):
    d.text((110, 80), "BIG", fill=(255,255,255,255), anchor="mm")
    d.text((110, 140), "SALE", fill=(255, 230, 80, 255), anchor="mm")
    d.text((110, 210), "50% OFF", fill=(255,255,255,255), anchor="mm")

poster((40, 80, 160, 255), "poster_beer.png", _p_beer)
poster((245, 245, 240, 255), "poster_missing.png", _p_missing)
poster((200, 50, 50, 255), "poster_sale.png", _p_sale)

# ------------------------------------------------ floor tile (tileable)
def floor_tile(name, size=240):
    img = canvas(size, size)
    d = ImageDraw.Draw(img)
    ts = 80
    for y in range(0, size, ts):
        for x in range(0, size, ts):
            c = (225, 225, 220, 255) if ((x+y)//ts) % 2 == 0 else (200, 200, 195, 255)
            d.rectangle([x, y, x+ts, y+ts], fill=c, outline=(170, 170, 165, 255), width=2)
    img.save(f"{OUT}/{name}")

floor_tile("floor_tile.png")

# ------------------------------------------------ ceiling lights (2)
def ceiling_light(name, on=True):
    img = canvas(200, 120)
    d = ImageDraw.Draw(img)
    d.rectangle([85, 0, 115, 30], fill=(120, 120, 120, 255), outline=BLK, width=3)
    fill = (255, 250, 220, 255) if on else (200, 200, 195, 255)
    d.pieslice([40, 20, 160, 120], start=0, end=180, fill=fill, outline=BLK, width=4)
    if on:
        for r in (70, 85):
            d.arc([100-r, 60-r, 100+r, 60+r], start=200, end=340,
                  fill=(255, 230, 150, 180), width=6)
    img.save(f"{OUT}/{name}")

ceiling_light("ceiling_light_on.png", True)
ceiling_light("ceiling_light_off.png", False)

# ------------------------------------------------ window display items
def display_pyramid(name):
    img = canvas(260, 200)
    d = ImageDraw.Draw(img)
    # pyramid of cans
    for row, n in enumerate([(3), (2), (1)]):
        y = 150 - row*42
        for i in range(n):
            x = 130 + (i - (n-1)/2)*52
            d.rectangle([x-22, y-38, x+22, y], fill=(220, 70, 70, 255), outline=BLK, width=3)
            d.rectangle([x-22, y-38, x+22, y-24], fill=(240, 240, 240, 255), outline=BLK, width=2)
    # base
    d.rectangle([30, 150, 230, 185], fill=(150, 150, 150, 255), outline=BLK, width=4)
    img.save(f"{OUT}/{name}")

display_pyramid("window_display_cans.png")

def sale_banner(name):
    img = canvas(500, 100)
    d = ImageDraw.Draw(img)
    d.polygon([(10, 10), (490, 10), (470, 90), (30, 90)], fill=(230, 50, 50, 255), outline=BLK, width=5)
    d.text((250, 50), "GRAND OPENING", fill=(255, 255, 255, 255), anchor="mm")
    img.save(f"{OUT}/{name}")

sale_banner("sale_banner.png")

print("store detail done")
