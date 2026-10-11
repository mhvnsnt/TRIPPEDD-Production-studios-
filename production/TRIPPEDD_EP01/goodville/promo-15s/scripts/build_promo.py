#!/usr/bin/env python3
"""Goodville Cartoon 15s promo — hand-built South Park-esque cutout animation.
No AI-generated visuals. PIL cutout compositing (the digital paper-cutout method),
stepped animation, flat colors, orthographic look.

FIX PASS (parent-verified defects):
1. Removed the black-bar jacket polygon (shots 1-2) — asset's own shoulders used.
2. Old head scaled 2.0 -> 0.95 and lowered so the GOODVILLE sign stays readable.
3. Cigarette drawn explicitly after the mouth shapes (was getting covered).
4. Beer can redrawn as the key-art can (blue + red BEER label); the solid-blue
   "Pepsi-like" baked-in can cropped out of the head asset; the blue-rectangle
   placeholder ("beer can hint") replaced with a real can in the fist.
5. Amos Jr. head 250px -> 0.72 scale (was bobblehead); TACOS sign moved clear of
   Amos; punch arm re-posed to extend LEFT into the dino (was punching right,
   away from the target).
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS, FRAMES, AUDIO = (os.path.join(BASE, d) for d in ("assets", "frames", "audio"))
W, H, FPS, DUR = 1280, 720, 24, 15
NFRAMES = FPS * DUR  # 360

# ---------- palette (sampled from key art) ----------
SKY = (126, 200, 227)
ROAD = (110, 110, 112)
SIDEWALK = (150, 150, 152)
SKIN = (240, 200, 150)
SKIN_DK = (210, 170, 125)
BLACK = (20, 20, 22)
WHITE = (245, 245, 245)
YELLOW = (255, 216, 0)
DINO = (77, 166, 77)
DINO_LT = (143, 214, 143)
MOUTH_C = (42, 26, 18)
CAN_BLUE = (35, 90, 175)
CAN_RED = (185, 40, 40)

keyart = Image.open('/home/hatch/workspace/trippedd-studio/assets/references/ep01/source/Goodville - Not South Park.png').convert('RGB')

# FIX 1+4: trim extraction artifacts (non-destructive crops of the source assets)
# oldhead_body.png 250x369: bottom ~93px is a solid black extraction band -> cut it,
# the asset's own jacket/shoulders are the body (no drawn polygon needed).
oldhead = Image.open(os.path.join(ASSETS, 'oldhead_body.png')).crop((0, 0, 250, 276))
# amosjr_head.png 250x250: bottom region is a baked-in hand + Pepsi-like blue can
# (extraction grab) -> cut it; the real can is drawn separately in the fist.
amos_head = Image.open(os.path.join(ASSETS, 'amosjr_head.png')).crop((0, 0, 250, 188))

OH_W, OH_H = oldhead.size   # 250 x 276
AH_W, AH_H = amos_head.size  # 250 x 188

def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

# ---------- backgrounds ----------
# shots 1-2: town sign crop straight from key art (1280x720 region)
bg_sign = keyart.crop((250, 0, 1390, 540)).resize((1280, 720), Image.LANCZOS)

# shot 3: Broadway street, hand-drawn flat
bg_street = Image.new('RGB', (W, H), SKY)
d = ImageDraw.Draw(bg_street)
d.rectangle([0, 0, W, 300], fill=SKY)                       # sky
# buildings row
d.rectangle([0, 180, 260, 470], fill=(180, 120, 90))        # left building
d.rectangle([40, 230, 220, 300], fill=(60, 50, 70))         # sign board
d.rectangle([300, 150, 620, 470], fill=(150, 150, 160))    # motel-ish
d.rectangle([340, 200, 580, 270], fill=(200, 60, 60))       # red sign
d.rectangle([660, 170, 980, 470], fill=(170, 140, 100))     # taco-ish
# FIX 5: TACOS board shifted left + smaller text so Amos Jr. never covers it
d.rectangle([660, 220, 860, 290], fill=(60, 50, 70))
d.rectangle([1020, 190, 1280, 470], fill=(140, 120, 130))   # right building
d.rectangle([0, 470, W, 540], fill=SIDEWALK)                # sidewalk
d.rectangle([0, 540, W, H], fill=ROAD)                     # road
for x in range(60, W, 160):                                 # lane dashes
    d.rectangle([x, 622, x+80, 634], fill=(230, 200, 60))
# signs text
d.text((52, 238), "BAR", font=font(44), fill=(255, 255, 255))
d.text((352, 208), "MOTEL", font=font(44), fill=(255, 255, 255))
d.text((672, 232), "TACOS", font=font(36), fill=(255, 255, 255))

# shot 4: end card
bg_card = Image.new('RGB', (W, H), (8, 8, 10))
d = ImageDraw.Draw(bg_card)
f_big, f_mid = font(150), font(54)
for t, fnt, y, col in [("GOODVILLE", f_big, 180, YELLOW),
                       ("NOT SOUTH PARK.", f_mid, 400, WHITE),
                       ("JUST AS STUPID.", f_mid, 470, WHITE)]:
    bb = d.textbbox((0, 0), t, font=fnt)
    d.text(((W-(bb[2]-bb[0]))/2, y), t, font=fnt, fill=col)
# crown mark
cx, cy, s = W//2, 110, 46
pts = [(cx-1.4*s, cy), (cx-1.4*s, cy-0.9*s), (cx-0.7*s, cy-0.3*s), (cx, cy-1.2*s),
       (cx+0.7*s, cy-0.3*s), (cx+1.4*s, cy-0.9*s), (cx+1.4*s, cy), (cx-1.4*s, cy)]
d.polygon(pts, outline=(255, 255, 255), width=6)

# ---------- paper grain (static) ----------
rng = np.random.default_rng(7)
grain = Image.fromarray((rng.integers(0, 255, (H, W), dtype=np.uint8)), 'L')
grain = grain.point(lambda v: 235 + v//10)  # subtle

def apply_grain(im):
    g = Image.merge('RGB', (grain, grain, grain))
    return Image.fromarray(((np.asarray(im).astype(float)*0.94 + np.asarray(g).astype(float)*0.06)).astype(np.uint8))

def shadow(im, x, y, w):
    d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse([x-w//2, y-14, x+w//2, y+14], fill=(0, 0, 0, 70))

# ---------- FIX 4: key-art beer can, drawn flat (blue + red BEER label) ----------
def beer_can(scale=1.0):
    w, h = int(46*scale), int(66*scale)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 6, w-2, h-2], radius=int(7*scale), fill=CAN_BLUE)
    d.rectangle([2, 0, w-2, int(10*scale)], fill=(205, 205, 205))       # silver top rim
    d.ellipse([2, 0, w-2, int(10*scale)], fill=(225, 225, 225))
    d.rounded_rectangle([int(6*scale), int(20*scale), w-int(6*scale), h-int(12*scale)],
                        radius=int(4*scale), fill=CAN_RED)              # red label band
    fnt = font(max(8, int(13*scale)))
    t = "BEER"
    bb = d.textbbox((0, 0), t, font=fnt)
    d.text(((w-(bb[2]-bb[0]))/2, int(30*scale)), t, font=fnt, fill=(255, 255, 255))
    return im

BEER_CAN = beer_can(1.0)

# ---------- cigarette (drawn after the mouth so it is never covered) ----------
def cigarette(scale):
    """Small angled cigarette on its own layer; caller pastes at the mouth corner."""
    w, h = int(34*scale), int(14*scale)
    im = Image.new('RGBA', (w*2, h*3), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, y0 = w//2, h
    ln, wd = int(30*scale), max(3, int(7*scale))
    d.rectangle([x0, y0-wd//2, x0+ln, y0+wd//2], fill=(215, 185, 135))       # paper
    d.rectangle([x0, y0-wd//2, x0+int(8*scale), y0+wd//2], fill=(150, 110, 70))  # filter
    d.ellipse([x0+ln-3, y0-wd//2, x0+ln+3, y0+wd//2], fill=(255, 120, 40))    # ember
    return im.rotate(-12, resample=Image.BICUBIC, expand=True)

CIG = cigarette(1.0)

# ---------- old head assembly (shots 1-2) ----------
def oldhead_frame(scale, bob, mouth):
    """mouth: 0 closed, 1 small, 2 med, 3 wide. Medium close-up, framed right of
    center (echoing the key art where he stands at the right); GOODVILLE sign
    stays fully readable above/left of the head."""
    im = bg_sign.copy()
    hw, hh = int(OH_W*scale), int(OH_H*scale)
    head = oldhead.resize((hw, hh), Image.LANCZOS)
    # face center sits at asset-x ~125*scale; put the face at frame-x ~780
    hx, hy = 780 - int(125*scale), 427 + bob
    # FIX 1: no drawn jacket polygon (it read as a black bar). The asset's own
    # cropped shoulders are the body.
    im.paste(head, (hx, hy), head)
    # mouth shapes (measured: mouth center ~ (0.54, 0.56) of the cropped asset)
    mx, my = hx + int(hw*0.54), hy + int(hh*0.56)
    d = ImageDraw.Draw(im)
    ms = int(22*scale)
    if mouth == 0:
        d.line([mx-ms, my, mx+ms, my], fill=MOUTH_C, width=max(3, int(4*scale)))
    else:
        wdt = [0.5, 0.8, 1.1][mouth-1] * ms
        d.ellipse([mx-wdt, my-wdt*0.8, mx+wdt, my+wdt*0.8], fill=MOUTH_C)
    # FIX 3: cigarette drawn AFTER the mouth, at the mouth's right corner
    # (key-art position), so the animated mouth never covers it.
    cig = CIG.resize((int(CIG.width*scale), int(CIG.height*scale)), Image.LANCZOS)
    im.paste(cig, (int(mx + hw*0.10), int(my - cig.height*0.35)), cig)
    return im

# ---------- dino guy (hand-drawn, separate head layer) ----------
def dino_body():
    im = Image.new('RGBA', (240, 340), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(150, 300), (235, 250), (160, 230)], fill=DINO)          # tail
    d.rectangle([80, 200, 170, 320], fill=DINO)                          # torso
    d.ellipse([95, 220, 155, 300], fill=DINO_LT)                         # belly
    d.rectangle([95, 315, 125, 340], fill=DINO)                          # legs
    d.rectangle([140, 315, 170, 340], fill=DINO)
    d.ellipse([60, 230, 100, 270], fill=DINO)                            # arm nub
    return im

def dino_head():
    im = Image.new('RGBA', (200, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([30, 20, 170, 150], fill=DINO)                             # skull
    d.ellipse([90, 70, 190, 140], fill=DINO)                             # snout
    d.ellipse([55, 35, 105, 85], fill=WHITE)                             # eye L
    d.ellipse([105, 35, 155, 85], fill=WHITE)                            # eye R
    d.ellipse([72, 52, 88, 68], fill=BLACK)
    d.ellipse([122, 52, 138, 68], fill=BLACK)
    d.arc([100, 90, 180, 135], 10, 170, fill=WHITE, width=7)             # toothy grin
    return im

DINO_BODY, DINO_HEAD = dino_body(), dino_head()

# ---------- Amos Jr. assembly (FIX 5: redesigned proportions + punch) ----------
# Canvas 620x560. Head 0.72 scale (was full 250px -> bobblehead). Punch arm
# extends LEFT toward the dino (was drawn extending right, away from target).
AH_SCALE = 0.72

def amosjr(punch):
    """punch 0 = windup (cocked), 1 = extended LEFT into the dino."""
    im = Image.new('RGBA', (620, 560), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # torso: white tank
    d.polygon([(330, 120), (480, 120), (500, 470), (310, 470)], fill=WHITE)
    d.polygon([(330, 120), (480, 120), (465, 165), (345, 165)], fill=(225, 225, 225))
    # legs: blue jeans
    d.rectangle([350, 470, 410, 560], fill=(70, 90, 140))
    d.rectangle([430, 470, 490, 560], fill=(70, 90, 140))
    # head (can cropped out of the asset; real can goes in the fist)
    hw2, hh2 = int(AH_W*AH_SCALE), int(AH_H*AH_SCALE)
    im.paste(amos_head.resize((hw2, hh2), Image.LANCZOS), (315, 8),
             amos_head.resize((hw2, hh2), Image.LANCZOS))
    # arm tattoo (documented likeness item): small dark mark, viewer-left upper arm
    d.ellipse([298, 205, 322, 232], outline=(40, 60, 90), width=3)
    d.line([302, 218, 318, 218], fill=(40, 60, 90), width=2)
    # right arm (viewer-right): hangs down, fist grips the beer can
    d.ellipse([475, 200, 535, 390], fill=SKIN)          # arm
    d.ellipse([472, 372, 544, 442], fill=SKIN)         # fist (behind the can)
    # FIX 4: key-art beer can gripped in the fist (blue + red BEER label)
    im.paste(BEER_CAN, (484, 366), BEER_CAN)
    # finger lines over the can suggest the grip
    for fy in (392, 406, 420):
        d.line([484, fy, 528, fy], fill=SKIN_DK, width=3)
    # left arm: the punch
    if punch == 0:
        # windup: arm cocked, fist near chest
        d.polygon([(330, 190), (362, 218), (302, 302), (276, 276)], fill=SKIN)
        d.ellipse([268, 264, 332, 328], fill=SKIN_DK)   # cocked fist
    else:
        # extended: arm drives LEFT into the dino, fist leading
        d.polygon([(335, 185), (365, 235), (105, 285), (85, 225)], fill=SKIN)
        d.ellipse([40, 210, 115, 290], fill=SKIN_DK)    # fist
        # motion lines behind the fist
        for i in range(3):
            x0 = 135 + i*28
            d.line([x0, 232+i*16, x0+34, 242+i*16], fill=(255, 255, 255, 170), width=4)
    return im

# ---------- shot assembly ----------
mouth_cycle = [0, 1, 2, 1, 3, 2, 1, 0]

def render():
    os.makedirs(FRAMES, exist_ok=True)
    for f in range(NFRAMES):
        if f < 72:  # SHOT 1: old head, line1 (0.3-2.4s)
            speaking = 7 <= f <= 58
            bob = -8 if speaking and (f//12) % 2 else 0
            mouth = mouth_cycle[(f//6) % len(mouth_cycle)] if speaking else 0
            im = oldhead_frame(1.5, bob, mouth)
        elif f < 216:  # SHOT 2: old head push-in, line2a (3.3-10.7s)
            speaking = 79 <= f <= 257
            step = min(3, (f-72)//36)
            scale = 1.5 + step*0.023   # gentle push-in 1.50 -> 1.57
            bob = -8 if speaking and (f//12) % 2 else 0
            mouth = mouth_cycle[(f//6) % len(mouth_cycle)] if speaking else 0
            im = oldhead_frame(scale, bob, mouth)
        elif f < 312:  # SHOT 3: reveal — Broadway, dino, Amos Jr. beating
            im = bg_street.copy()
            lf = f - 216  # 0..95
            # dino guy
            dx, dy = 500, 300
            tilt = 0
            if 32 <= lf < 48 or 64 <= lf < 80:
                tilt = -12  # reeling from punches
            body = DINO_BODY.rotate(tilt, resample=Image.BICUBIC, expand=True)
            shadow(im, dx+120, dy+330, 200)
            im.paste(body, (dx, dy), body)
            # dino head: attached on torso top, then flies off at lf>=64
            hs = DINO_HEAD.resize((160, 136), Image.LANCZOS)
            head = None; hpos = None
            if lf < 64:
                hx, hy2 = dx+45, dy+55
                head = hs.rotate(tilt, resample=Image.BICUBIC, expand=True)
                hpos = (hx, hy2)
                im.paste(head, hpos, head)
            else:
                k = min(1.0, (lf-64)/14)
                hx = int(dx+45 + k*420)
                hy2 = int(dy+55 - k*260 + k*k*320)
                head = hs.rotate(int(-k*220), resample=Image.BICUBIC, expand=True)
                hpos = (hx, hy2)  # pasted AFTER Amos so it stays visible in flight
            # Amos Jr.: windup / punch cycle, lunging in on the punches.
            # Fist lands on the dino head: ax = dx + 48.
            if lf < 32:
                am, ax = amosjr(0), 608
            elif lf < 48:
                am, ax = amosjr(1), 548   # punch 1, lunged in
            elif lf < 64:
                am, ax = amosjr(0), 608
            elif lf < 80:
                am, ax = amosjr(1), 548   # punch 2
            else:
                am, ax = amosjr(0), 628   # standing, done
            shadow(im, ax+310, 700, 260)
            im.paste(am, (ax, 180), am)
            if head is not None and lf >= 64:
                im.paste(head, hpos, head)  # flying head stays in front
        else:  # SHOT 4: end card
            im = bg_card.copy()
        im = apply_grain(im)
        im.save(os.path.join(FRAMES, f"f{f:04d}.png"))
        if f % 60 == 0:
            print("frame", f, flush=True)

if __name__ == "__main__":
    render()
    print("DONE", NFRAMES, "frames")
