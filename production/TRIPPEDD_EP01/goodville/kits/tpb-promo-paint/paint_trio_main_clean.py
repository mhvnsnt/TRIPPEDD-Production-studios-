# ---- bodies ----
def paint_body(cx, head_cy, r, shirt, pants, stripes=None):
    """Returns RGBA layer with torso, arms, legs, shoes. Feet at y~955."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    neck_y = head_cy + r * 0.80
    hip_y = 730
    # legs
    leg_w = 56
    for sgn in (-1, 1):
        lx = cx + sgn * 52
        d.rectangle([lx - leg_w / 2, hip_y - 20, lx + leg_w / 2, 920],
                    fill=pants + (255,))
    # leg shading
    for sgn in (-1, 1):
        lx = cx + sgn * 52
        soft_blob(lay, lx + 14, 830, 26, (0, 0, 0), 0.18, 14)
    # shoes
    for sgn in (-1, 1):
        lx = cx + sgn * 52
        d.rounded_rectangle([lx - 38, 912, lx + 38, 962], radius=16,
                            fill=(40, 36, 38, 255), outline=OUTLINE + (255,),
                            width=3)
    # torso
    tx1, tx2 = cx - 118, cx + 118
    d.rounded_rectangle([tx1, neck_y - 10, tx2, hip_y + 10], radius=46,
                        fill=shirt + (255,))
    if stripes:
        c1, c2 = stripes
        sy = neck_y - 10
        i = 0
        while sy < hip_y + 10:
            sh = 34
            # clip stripes to torso rounded rect via mask
            d.rectangle([tx1, sy, tx2, min(sy + sh, hip_y + 10)],
                        fill=(c1 if i % 2 == 0 else c2) + (255,))
            sy += sh
            i += 1
        # re-mask: redraw rounded rect outline over stripes
        d.rounded_rectangle([tx1, neck_y - 10, tx2, hip_y + 10], radius=46,
                            outline=OUTLINE + (255,), width=4)
    cloth_shade(lay, (tx1, neck_y, tx2, hip_y), shirt, tuple(
        max(0, c - 55) for c in shirt), n_folds=5)
    if not stripes:
        d.rounded_rectangle([tx1, neck_y - 10, tx2, hip_y + 10], radius=46,
                            outline=OUTLINE + (255,), width=4)
    # arms — tapered capsules with mitten hands
    for sgn in (-1, 1):
        sx, sy = cx + sgn * 108, neck_y + 40
        ex, ey = cx + sgn * 128, neck_y + 200
        # sleeve shading
        capsule(d, sx, sy, ex, ey, 64, shirt)
        soft_blob(lay, sx + sgn * 8, sy + 60, 26, (0, 0, 0), 0.16, 12)
        # hand
        d.ellipse([ex - 30, ey - 6, ex + 30, ey + 54], fill=SKIN + (255,),
                  outline=OUTLINE + (255,), width=3)
        soft_blob(lay, ex - 10, ey + 18, 20, SKIN_DK, 0.30, 10)
    return lay

def paint_bubbles():
    cx, cy, r = 380, 430, 130
    lay = paint_body(cx, cy, r, SHIRT_RED, PANTS_BLUE)
    d = ImageDraw.Draw(lay)
    # head
    face, c = face_base(r)
    lay.alpha_composite(face, (cx - c, cy - c))
    # toque — navy cap with ribbing
    tq = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tqd = ImageDraw.Draw(tq)
    tqd.ellipse([cx - r * 1.0, cy - r * 1.55, cx + r * 1.0, cy - r * 0.30],
                fill=TOQUE + (255,))
    for i in range(-4, 5):
        gx = cx + i * 26
        tqd.line([gx, cy - r * 1.5, gx, cy - r * 0.42],
                 fill=(20, 30, 66, 255), width=4)
    # toque shading + brim
    tqd.ellipse([cx - r * 1.0, cy - r * 0.72, cx + r * 1.0, cy - r * 0.30],
                fill=(44, 58, 108, 255), outline=OUTLINE + (255,), width=4)
    tq = tq.filter(ImageFilter.GaussianBlur(1))
    lay.alpha_composite(tq)
    # big round glasses + eyes behind
    paint_eyes(lay, cx, cy + 10, r)
    for sgn in (-1, 1):
        gx = cx + sgn * r * 0.30
        d.ellipse([gx - 58, cy + 10 - 58, gx + 58, cy + 10 + 58],
                  outline=(22, 20, 22, 255), width=9)
    d.line([cx - r * 0.30 + 52, cy + 4, cx + r * 0.30 - 52, cy + 4],
           fill=(22, 20, 22, 255), width=8)
    # glass shine
    soft_blob(lay, cx - r * 0.30 - 18, cy - 12, 20, (255, 255, 255), 0.35, 8)
    paint_mouth(lay, cx, cy + 10, r, "smile")
    # kitty at feet
    kx, ky = cx - 170, 900
    d.ellipse([kx - 52, ky - 60, kx + 52, ky + 44], fill=KITTY + (255,),
              outline=OUTLINE + (255,), width=4)
    soft_blob(lay, kx - 16, ky - 10, 30, (214, 120, 62), 0.4, 12)
    for sgn in (-1, 1):  # ears
        ex = kx + sgn * 34
        d.polygon([(ex - 16, ky - 52), (ex + 16, ky - 52), (ex, ky - 88)],
                  fill=KITTY + (255,), outline=OUTLINE + (255,))
    # kitty face
    for sgn in (-1, 1):
        ex = kx + sgn * 20
        d.ellipse([ex - 8, ky - 30, ex + 8, ky - 14], fill=(20, 18, 18, 255))
    d.arc([kx - 16, ky - 18, kx + 16, ky + 6], start=20, end=160,
          fill=OUTLINE + (255,), width=4)
    d.line([kx + 44, ky + 20, kx + 92, ky - 8], fill=KITTY + (255,), width=16)
    return lay

def paint_ricky():
    cx, cy, r = 960, 450, 135
    lay = paint_body(cx, cy, r, STRIPE_CR, KHAKI, stripes=(STRIPE_NV, STRIPE_CR))
    d = ImageDraw.Draw(lay)
    # hair mass BEHIND face — shaggy, follows head contour
    hm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hm)
    hd.ellipse([cx - r * 1.12, cy - r * 1.18, cx + r * 1.12, cy + r * 0.75],
               fill=(58, 38, 24, 255))
    # dense top mass
    for _ in range(60):
        a = random.uniform(math.pi * 1.02, math.pi * 1.98)
        rr = r * random.uniform(0.70, 1.02)
        x0 = cx + math.cos(a) * rr
        y0 = cy + math.sin(a) * rr * 0.95 - r * 0.08
        x2 = x0 + math.cos(a) * r * random.uniform(0.10, 0.28)
        y2 = y0 + r * random.uniform(0.18, 0.42)
        xm = (x0 + x2) / 2 + random.uniform(-8, 8)
        ym = (y0 + y2) / 2
        col = random.choice([(46, 30, 20), (58, 38, 24), HAIR_MID, HAIR_LT])
        tapered_curve(hd, [(x0, y0), (xm, ym), (x2, y2)], 7, 2.5,
                      col + (255,))
    for _ in range(46):
        a = random.uniform(math.pi * 0.95, math.pi * 2.05)
        rr = r * random.uniform(0.85, 1.08)
        x0 = cx + math.cos(a) * rr
        y0 = cy + math.sin(a) * rr * 0.95 - r * 0.08
        # strands flow downward-outward, hugging the head
        x2 = x0 + math.cos(a) * r * random.uniform(0.15, 0.35)
        y2 = y0 + r * random.uniform(0.25, 0.5)
        xm = (x0 + x2) / 2 + random.uniform(-10, 10)
        ym = (y0 + y2) / 2
        col = random.choice([(46, 30, 20), (46, 30, 20), HAIR_MID, HAIR_LT])
        tapered_curve(hd, [(x0, y0), (xm, ym), (x2, y2)], 6, 2, col + (255,))
    # side locks past chin
    for sgn in (-1, 1):
        lx = cx + sgn * r * 1.0
        for _ in range(10):
            x0 = lx + random.uniform(-10, 10)
            tapered_curve(hd, [(x0, cy - r * 0.1),
                               (x0 + random.uniform(-8, 8), cy + r * 0.5),
                               (x0 + random.uniform(-10, 10), cy + r * 0.9)],
                          6, 2, random.choice(
                              [(46, 30, 20), HAIR_MID]) + (255,))
    hm = hm.filter(ImageFilter.GaussianBlur(1))
    lay.alpha_composite(hm)
    # head
    face, c = face_base(r)
    lay.alpha_composite(face, (cx - c, cy - c))
    # greasy shine on top (after face, clipped to hair region)
    soft_blob(lay, cx - r * 0.3, cy - r * 0.85, r * 0.5, (210, 180, 140),
              0.20, 20)
    # (hair painted behind face — see below)
    paint_eyes(lay, cx, cy + 8, r)
    # heavy-lidded: dark upper lid line
    for sgn in (-1, 1):
        gx = cx + sgn * r * 0.30
        d.arc([gx - r * 0.28, cy + 8 - r * 0.36, gx + r * 0.28, cy + 8 + r * 0.1],
              start=180, end=360, fill=OUTLINE + (255,), width=6)
    # goatee: filled chin patch with strand texture
    d.rounded_rectangle([cx - r * 0.30, cy + r * 0.42, cx + r * 0.30,
                         cy + r * 0.78], radius=18, fill=(52, 34, 22, 255),
                        outline=OUTLINE + (255,), width=3)
    # mustache
    d.rounded_rectangle([int(cx - r * 0.34), int(cy + r * 0.30),
                         int(cx + r * 0.34), int(cy + r * 0.46)], radius=8,
                        fill=(52, 34, 22, 255))
    for _ in range(16):
        gx = cx + random.uniform(-r * 0.26, r * 0.26)
        gy = cy + r * 0.50 + random.uniform(-6, 20)
        tapered_curve(d, [(gx, gy - 10), (gx + random.uniform(-4, 4), gy),
                          (gx + random.uniform(-5, 5), gy + 10)],
                      4, 1.5, random.choice(
                          [(70, 46, 28), (90, 62, 38)]) + (255,))
    paint_mouth(lay, cx, cy + 8, r, "flat")
    # cigarette in right hand
    hx, hy = cx + 128, cy + r * 0.80 + 200 - 40
    # (hand pos from paint_body: ex=cx+128, ey=neck_y+200)
    ex, ey = cx + 128, (cy + r * 0.80) + 200
    d.rectangle([ex + 6, ey + 8, ex + 52, ey + 20], fill=(245, 245, 240, 255),
                outline=OUTLINE + (255,), width=2)
    d.ellipse([ex + 48, ey + 6, ex + 60, ey + 22], fill=(250, 120, 40, 255))
    soft_blob(lay, ex + 54, ey + 14, 14, (250, 150, 60), 0.5, 8)
    # smoke wisp
    for i, (sx, sy) in enumerate([(ex + 54, ey - 10), (ex + 66, ey - 46),
                                  (ex + 52, ey - 82)]):
        soft_blob(lay, sx, sy, 16 - i * 3, (230, 230, 235), 0.35, 10)
    return lay

def paint_julian():
    cx, cy, r = 1480, 430, 125
    lay = paint_body(cx, cy, r, TEE_BLACK, (38, 44, 72))
    d = ImageDraw.Draw(lay)
    # head
    face, c = face_base(r)
    lay.alpha_composite(face, (cx - c, cy - c))
    # slicked-back hair with comb lines
    hk = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hkd = ImageDraw.Draw(hk)
    hkd.ellipse([cx - r * 1.0, cy - r * 1.5, cx + r * 1.0, cy - r * 0.28],
                fill=(26, 22, 24, 255))
    for i in range(-4, 5):
        gx = cx + i * 24
        hkd.line([gx, cy - r * 1.38, gx + random.uniform(-6, 6), cy - r * 0.45],
                 fill=(58, 50, 48, 255), width=2)
    soft_blob(hk, cx - r * 0.3, cy - r * 1.0, r * 0.45, (120, 110, 105),
              0.25, 16)
    hk = hk.filter(ImageFilter.GaussianBlur(1))
    lay.alpha_composite(hk)
    # sideburns
    for sgn in (-1, 1):
        d.rectangle([cx + sgn * r * 0.88 - 10, cy - r * 0.2,
                     cx + sgn * r * 0.88 + 10, cy + r * 0.25],
                    fill=(26, 22, 24, 255))
    paint_eyes(lay, cx, cy + 8, r, style="side")
    # confident brows
    for sgn in (-1, 1):
        bx = cx + sgn * r * 0.30
        d.line([bx - 26, cy - r * 0.42, bx + 26, cy - r * 0.36],
               fill=OUTLINE + (255,), width=7)
    paint_mouth(lay, cx, cy + 8, r, "smirk")
    # tumbler with amber liquid in left hand
    ex, ey = cx - 128, (cy + r * 0.80) + 200
    # glass
    d.rounded_rectangle([ex - 26, ey - 6, ex + 26, ey + 62], radius=8,
                        fill=(200, 220, 230, 90), outline=OUTLINE + (255,),
                        width=3)
    d.rectangle([ex - 20, ey + 18, ex + 20, ey + 56],
                fill=(196, 128, 44, 220))
    # ice cubes
    for (ix, iy) in [(ex - 8, ey + 30), (ex + 8, ey + 40)]:
        d.rectangle([ix - 8, iy - 8, ix + 8, iy + 8],
                    fill=(225, 240, 248, 200), outline=(160, 190, 210, 255),
                    width=2)
    soft_blob(lay, ex, ey + 28, 22, (255, 200, 120), 0.25, 10)
    return lay

