# ---- background ----
def paint_background():
    img = Image.fromarray(vgrad(W, H, SKY_TOP, SKY_BOT)).convert("RGBA")
    d = ImageDraw.Draw(img)

    # clouds — soft white blobs
    for (x, y, r) in [(300, 150, 130), (420, 180, 100), (1500, 130, 140),
                      (1640, 170, 90), (950, 90, 110), (1100, 120, 80)]:
        soft_blob(img, x, y, r, (255, 255, 255), alpha=0.85, blur=28)

    # far mountains (lighter, hazier)
    far = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    df = ImageDraw.Draw(far)
    df.polygon([(0, 620), (260, 300), (520, 620)], fill=(70, 130, 138, 255))
    df.polygon([(380, 620), (700, 260), (1020, 620)], fill=(64, 124, 132, 255))
    df.polygon([(900, 620), (1250, 280), (1600, 620)], fill=(70, 130, 138, 255))
    df.polygon([(1400, 620), (1720, 320), (1920, 620)], fill=(64, 124, 132, 255))
    far = far.filter(ImageFilter.GaussianBlur(6))
    img.alpha_composite(far)

    # near mountains — rich green with soft shadow modelling
    mtn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dm = ImageDraw.Draw(mtn)
    dm.polygon([(0, 700), (330, 330), (660, 700)], fill=(22, 110, 82, 255))
    dm.polygon([(520, 700), (940, 300), (1360, 700)], fill=(22, 110, 82, 255))
    dm.polygon([(1220, 700), (1600, 340), (1920, 700)], fill=(22, 110, 82, 255))
    mtn = mtn.filter(ImageFilter.GaussianBlur(1))
    img.alpha_composite(mtn)
    # soft darker modelling on mountain faces (tighter, less wash)
    for (x, y, r) in [(250, 540, 110), (830, 520, 120), (1500, 560, 100)]:
        soft_blob(img, x, y, r, MTN_DK, alpha=0.40, blur=30)
    # snow caps — white with soft blue-gray shadow edge
    snow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(snow)
    for (cx, cy, wdt) in [(330, 330, 260), (940, 300, 300), (1600, 340, 240)]:
        ds.polygon([(cx - wdt // 2, cy + 70), (cx, cy - 8),
                    (cx + wdt // 2, cy + 70),
                    (cx + wdt // 2 - 36, cy + 100), (cx, cy + 52),
                    (cx - wdt // 2 + 36, cy + 100)], fill=SNOW + (255,))
    snow = snow.filter(ImageFilter.GaussianBlur(3))
    img.alpha_composite(snow)
    for (x, y, r) in [(380, 380, 90), (1000, 360, 100), (1650, 390, 80)]:
        soft_blob(img, x, y, r, SNOW_SH, alpha=0.5, blur=22)

    # hills band
    hills = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dh = ImageDraw.Draw(hills)
    dh.polygon([(0, 1080), (0, 700), (500, 640), (1000, 700), (1500, 650),
                (1920, 700), (1920, 1080)], fill=(64, 140, 88, 255))
    hills = hills.filter(ImageFilter.GaussianBlur(4))
    img.alpha_composite(hills)
    soft_blob(img, 500, 700, 260, (48, 112, 70), alpha=0.5, blur=50)
    soft_blob(img, 1450, 700, 260, (48, 112, 70), alpha=0.5, blur=50)

    # pine trees with snow
    def pine(x, y, s):
        t = Image.new("RGBA", (s * 2, s * 3), (0, 0, 0, 0))
        td = ImageDraw.Draw(t)
        for i, (ww, yy) in enumerate([(s * 1.5, s * 2.2), (s * 1.2, s * 1.5),
                                      (s * 0.9, s * 0.8)]):
            td.polygon([(s, yy - s * 0.9), (s - ww / 2, yy), (s + ww / 2, yy)],
                       fill=PINE + (255,))
        # snow blobs
        for (sx, sy, sr) in [(s * 0.7, s * 1.9, s * 0.28),
                             (s * 1.25, s * 1.3, s * 0.24),
                             (s, s * 0.65, s * 0.2)]:
            td.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                       fill=SNOW + (255,))
        t = t.filter(ImageFilter.GaussianBlur(1.5))
        img.alpha_composite(t, (int(x - s), int(y - s * 3)))
    for (x, y, s) in [(120, 760, 55), (230, 780, 40), (1700, 770, 50),
                      (1800, 790, 38), (60, 800, 34), (1560, 800, 32)]:
        pine(x, y, s)

    # road
    rd = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    drd = ImageDraw.Draw(rd)
    drd.rectangle([0, 880, W, H], fill=ROAD + (255,))
    drd.rectangle([0, 880, W, 892], fill=ROAD_DK + (255,))
    rd = rd.filter(ImageFilter.GaussianBlur(1))
    img.alpha_composite(rd)
    # subtle road texture
    for _ in range(300):
        x, y = random.randint(0, W - 1), random.randint(895, H - 1)
        c = random.choice([ROAD_DK, (150, 152, 155)])
        ImageDraw.Draw(img).point((x, y), fill=c + (255,))
    # yellow dashes
    dd = ImageDraw.Draw(img)
    for x in range(40, W, 190):
        dd.rectangle([x, 975, x + 110, 990], fill=(242, 196, 60, 255))

    # ---- buildings ----
    def building(x, y, wdt, hgt, wall, roof_c, sign_text):
        b = Image.new("RGBA", (wdt + 60, hgt + 120), (0, 0, 0, 0))
        bd = ImageDraw.Draw(b)
        ox, oy = 30, 70
        # wall with plank lines
        bd.rectangle([ox, oy, ox + wdt, oy + hgt], fill=wall + (255,))
        for px in range(ox + 18, ox + wdt, 26):
            bd.line([px, oy, px, oy + hgt], fill=WOOD_DK + (255,), width=2)
        # soft wall shading
        # windows
        for wx in [ox + 30, ox + wdt - 90]:
            bd.rectangle([wx, oy + 45, wx + 60, oy + 105],
                         fill=(38, 52, 66, 255), outline=(30, 24, 20, 255),
                         width=3)
            bd.line([wx + 8, oy + 52, wx + 28, oy + 98],
                    fill=(150, 190, 220, 255), width=5)
        # door
        bd.rectangle([ox + wdt // 2 - 32, oy + hgt - 110, ox + wdt // 2 + 32,
                      oy + hgt], fill=WOOD_DK + (255,),
                     outline=(30, 24, 20, 255), width=3)
        # roof + snow
        bd.polygon([(ox - 18, oy + 6), (ox + wdt // 2, oy - 58),
                    (ox + wdt + 18, oy + 6), (ox + wdt + 6, oy + 22),
                    (ox - 6, oy + 22)], fill=roof_c + (255,))
        bd.polygon([(ox - 14, oy + 2), (ox + wdt // 2, oy - 50),
                    (ox + wdt + 14, oy + 2), (ox + wdt // 2, oy - 12)],
                   fill=SNOW + (255,))
        b = b.filter(ImageFilter.GaussianBlur(1))
        img.alpha_composite(b, (x - 30, y - 70))
        # sign board — shrink font until text fits
        fnt_size = 30
        fnt = ImageFont.truetype(FONT_BOLD, fnt_size)
        _m = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        while _m.textlength(sign_text, font=fnt) > wdt - 24 and fnt_size > 10:
            fnt_size -= 2
            fnt = ImageFont.truetype(FONT_BOLD, fnt_size)
        sb = Image.new("RGBA", (wdt, 54), (0, 0, 0, 0))
        sbd = ImageDraw.Draw(sb)
        sbd.rectangle([0, 0, wdt, 54], fill=(24, 24, 28, 255))
        text_stroke(sbd, (wdt // 2, 27), sign_text, fnt, (240, 230, 200),
                    (0, 0, 0), 1)
        img.alpha_composite(sb, (x, y + 18))

    building(8, 620, 400, 210, (96, 128, 118), (70, 60, 52),
             "GENERAL STORE")
    building(1540, 630, 380, 200, (150, 140, 150), (80, 70, 76), "MOTEL")

    # ---- GOODVILLE town sign ----
    sg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sg)
    # posts
    for px in [700, 1180]:
        sd.rectangle([px, 300, px + 44, 780], fill=WOOD + (255,))
        for i in range(6):
            gx = px + 6 + i * 7
            sd.line([gx, 310, gx, 770], fill=WOOD_DK + (255,), width=2)
    # board
    bx1, by1, bx2, by2 = 600, 120, 1280, 330
    sd.rounded_rectangle([bx1, by1, bx2, by2], radius=26, fill=WOOD + (255,),
                         outline=WOOD_DK + (255,), width=6)
    for px in range(bx1 + 40, bx2, 64):
        sd.line([px, by1 + 12, px, by2 - 12], fill=WOOD_DK + (255,), width=2)
    # snow on top of board
    sd.rounded_rectangle([bx1 - 8, by1 - 26, bx2 + 8, by1 + 26], radius=20,
                         fill=SNOW + (255,))
    sg = sg.filter(ImageFilter.GaussianBlur(1))
    img.alpha_composite(sg)
    # letters
    fnt_big = ImageFont.truetype(FONT_BOLD, 118)
    d2 = ImageDraw.Draw(img)
    text_stroke(d2, (940, 228), "GOODVILLE", fnt_big, SIGN_YEL, (20, 14, 10),
                5)
    return img
