# ---- character painters ----
def face_base(r):
    s = r * 2 + 60
    c = s // 2
    arr = np.full((s, s, 3), SKIN, np.uint8).astype(float)
    yy, xx = np.mgrid[0:s, 0:s]
    d = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / r
    edge = np.clip((d - 0.60) / 0.40, 0, 1)[..., None]
    arr = arr * (1 - edge * 0.38) + np.array(SKIN_DK) * edge * 0.38
    lx, ly = c - r * 0.38, c - r * 0.42
    ld = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2) / (r * 1.15)
    li = np.clip(1 - ld, 0, 1)[..., None]
    arr = arr * (1 - li * 0.30) + np.array(SKIN_LT) * li * 0.30
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    mask = d <= 1.0
    img = Image.fromarray(np.dstack([arr, (mask * 255).astype(np.uint8)]))
    d2 = ImageDraw.Draw(img)
    d2.ellipse([c - r, c - r, c + r, c + r], outline=OUTLINE + (255,), width=4)
    # blush
    soft_blob(img, c - r * 0.52, c + r * 0.28, r * 0.30, BLUSH, 0.35, 18)
    soft_blob(img, c + r * 0.52, c + r * 0.28, r * 0.30, BLUSH, 0.35, 18)
    return img, c

def paint_eyes(layer, cx, cy, r, style="normal"):
    d = ImageDraw.Draw(layer)
    ex, ey, ew, eh = cx, cy, r * 0.52, r * 0.62
    for sgn in (-1, 1):
        x = cx + sgn * r * 0.30
        # white with soft top shading
        d.ellipse([x - ew / 2, cy - eh / 2, x + ew / 2, cy + eh / 2],
                  fill=(250, 250, 250, 255), outline=OUTLINE + (255,), width=3)
    layer2 = layer.filter(ImageFilter.GaussianBlur(0))  # noop keep
    # top shade on eyes
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    for sgn in (-1, 1):
        x = cx + sgn * r * 0.30
        ds.ellipse([x - ew / 2, cy - eh / 2, x + ew / 2, cy + eh / 2],
                   fill=(190, 200, 210, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    # mask to eye interiors roughly
    layer.alpha_composite(sh)
    d = ImageDraw.Draw(layer)
    for sgn in (-1, 1):
        x = cx + sgn * r * 0.30
        px = x + (r * 0.06 if style == "side" else 0)
        d.ellipse([px - 9, cy - 9, px + 9, cy + 9], fill=(18, 16, 16, 255))
        d.ellipse([px - 3, cy - 6, px + 3, cy], fill=(255, 255, 255, 255))

def paint_mouth(layer, cx, cy, r, style="smile"):
    d = ImageDraw.Draw(layer)
    if style == "smile":
        d.arc([cx - r * 0.28, cy + r * 0.10, cx + r * 0.28, cy + r * 0.52],
              start=15, end=165, fill=OUTLINE + (255,), width=5)
    elif style == "smirk":
        d.arc([cx - r * 0.22, cy + r * 0.08, cx + r * 0.30, cy + r * 0.50],
              start=20, end=150, fill=OUTLINE + (255,), width=5)
    elif style == "flat":
        d.line([cx - r * 0.20, cy + r * 0.32, cx + r * 0.20, cy + r * 0.32],
               fill=OUTLINE + (255,), width=5)

def hair_strands(layer, cx, cy, r, n, c_dark, c_mid, c_lt, top=True):
    """Shaggy hair mass: base blob + strand strokes."""
    d = ImageDraw.Draw(layer)
    # base mass
    d.ellipse([cx - r * 1.02, cy - r * 1.05, cx + r * 1.02, cy + r * 0.35],
              fill=c_mid + (255,))
    for _ in range(n):
        a = random.uniform(math.pi * 1.05, math.pi * 1.95) if top else \
            random.uniform(0, math.pi * 2)
        r0 = r * random.uniform(0.55, 0.95)
        x0 = cx + math.cos(a) * r0
        y0 = cy + math.sin(a) * r0 * 0.9 - r * 0.1
        ang = a + random.uniform(-0.5, 0.5)
        leng = r * random.uniform(0.25, 0.55)
        x2 = x0 + math.cos(ang) * leng
        y2 = y0 + math.sin(ang) * leng + r * 0.12
        xm = (x0 + x2) / 2 + random.uniform(-14, 14)
        ym = (y0 + y2) / 2 + random.uniform(-14, 14)
        col = random.choice([c_dark, c_dark, c_mid, c_lt])
        tapered_curve(d, [(x0, y0), (xm, ym), (x2, y2)],
                      random.uniform(5, 8), random.uniform(1.5, 3), col + (255,))
    # soft outline on hair mass
    layer2 = layer.copy()
    return layer

def capsule(d, x1, y1, x2, y2, w, fill, outline_w=3):
    d.line([x1, y1, x2, y2], fill=fill + (255,), width=int(w))
    d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=fill + (255,))
    d.ellipse([x2 - w / 2, y2 - w / 2, x2 + w / 2, y2 + w / 2], fill=fill + (255,))

def cloth_shade(layer, box, base, dark, n_folds=4):
    """Soft fold shadows on clothing."""
    x1, y1, x2, y2 = box
    for _ in range(n_folds):
        fx = random.uniform(x1 + 15, x2 - 15)
        fy0 = random.uniform(y1 + 10, y1 + (y2 - y1) * 0.4)
        fl = random.uniform((y2 - y1) * 0.3, (y2 - y1) * 0.6)
        tmp = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        tapered_curve(td, [(fx, fy0), (fx + random.uniform(-18, 18), fy0 + fl / 2),
                           (fx + random.uniform(-26, 26), fy0 + fl)],
                      16, 5, dark + (255,))
        tmp = tmp.filter(ImageFilter.GaussianBlur(9))
        # apply at low alpha
        arr = np.array(tmp).astype(float)
        arr[..., 3] *= 0.35
        layer.alpha_composite(Image.fromarray(arr.astype(np.uint8)))
    # top highlight
    soft_blob(layer, (x1 + x2) / 2 - 20, y1 + 26, (x2 - x1) * 0.4,
              (255, 255, 255), 0.14, 22)
