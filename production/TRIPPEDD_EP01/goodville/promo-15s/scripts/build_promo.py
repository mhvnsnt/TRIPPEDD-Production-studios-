#!/usr/bin/env python3
"""Goodville Cartoon 15s promo — hand-built South Park-esque cutout animation.
No AI-generated visuals. PIL cutout compositing (the digital paper-cutout method),
stepped animation, flat colors, orthographic look.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os, subprocess

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

keyart = Image.open('/home/hatch/workspace/trippedd-studio/assets/references/ep01/source/Goodville - Not South Park.png').convert('RGB')
oldhead = Image.open(os.path.join(ASSETS, 'oldhead_body.png'))   # 275x369 head
amos_head = Image.open(os.path.join(ASSETS, 'amosjr_head.png'))  # 250x250

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
d.rectangle([0, 180, 260, 470], outline=None)
d.rectangle([40, 230, 220, 300], fill=(60, 50, 70))         # sign board
d.rectangle([300, 150, 620, 470], fill=(150, 150, 160))     # motel-ish
d.rectangle([340, 200, 580, 270], fill=(200, 60, 60))       # red sign
d.rectangle([660, 170, 980, 470], fill=(170, 140, 100))     # taco-ish
d.rectangle([700, 220, 940, 290], fill=(60, 50, 70))
d.rectangle([1020, 190, 1280, 470], fill=(140, 120, 130))    # right building
d.rectangle([0, 470, W, 540], fill=SIDEWALK)                 # sidewalk
d.rectangle([0, 540, W, H], fill=ROAD)                      # road
for x in range(60, W, 160):                                  # lane dashes
    d.rectangle([x, 622, x+80, 634], fill=(230, 200, 60))
# signs text
f_s = font(44)
d.text((52, 238), "BAR", font=f_s, fill=(255, 255, 255))
d.text((352, 208), "MOTEL", font=f_s, fill=(255, 255, 255))
d.text((712, 228), "TACOS", font=f_s, fill=(255, 255, 255))

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
    return Image.blend(im, Image.composite(im, g, g), 0.0) if False else \
        Image.fromarray(((np.asarray(im).astype(float)*0.94 + np.asarray(g).astype(float)*0.06)).astype(np.uint8))

def shadow(im, x, y, w):
    d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse([x-w//2, y-14, x+w//2, y+14], fill=(0, 0, 0, 70))

# ---------- old head assembly (shots 1-2) ----------
def oldhead_frame(scale, bob, mouth):
    """mouth: 0 closed, 1 small, 2 med, 3 wide. Head front-center like the key art."""
    im = bg_sign.copy()
    hw, hh = int(250*scale), int(369*scale)
    head = oldhead.resize((hw, hh), Image.LANCZOS)
    hx, hy = 640 - hw//2, 30 + bob
    # jacket: black trapezoid behind head
    d = ImageDraw.Draw(im)
    d.polygon([(hx-40, hy+hh-120), (hx+hw+40, hy+hh-120),
               (hx+hw+90, H), (hx-90, H)], fill=BLACK)
    im.paste(head, (hx, hy), head)
    # mouth shapes (relative to head box; actual mouth ~62% down, 60% across)
    mx, my = hx + int(hw*0.54), hy + int(hh*0.42)  # measured in extraction
    d = ImageDraw.Draw(im)
    ms = int(30*scale)
    if mouth == 0:
        d.line([mx-ms, my, mx+ms, my], fill=MOUTH_C, width=max(3, int(5*scale)))
    else:
        wdt = [0.5, 0.8, 1.1][mouth-1] * ms
        d.ellipse([mx-wdt, my-wdt*0.8, mx+wdt, my+wdt*0.8], fill=MOUTH_C)
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

# ---------- Amos Jr. assembly ----------
def amosjr(lunge, punch):
    """punch 0 = windup, 1 = extended"""
    im = Image.new('RGBA', (420, 560), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # torso: white tank
    d.polygon([(130, 200), (290, 200), (310, 480), (110, 480)], fill=WHITE)
    d.polygon([(130, 200), (290, 200), (270, 250), (150, 250)], fill=(225, 225, 225))
    # legs: blue jeans rects (simple)
    d.rectangle([140, 480, 200, 560], fill=(70, 90, 140))
    d.rectangle([220, 480, 280, 560], fill=(70, 90, 140))
    # head
    im.paste(amos_head, (85, 0), amos_head)
    # right arm down (holds can) — simple
    d.ellipse([60, 230, 130, 430], fill=SKIN)
    d.ellipse([70, 400, 140, 470], fill=SKIN)          # fist w/ can
    d.rectangle([78, 380, 132, 440], fill=(30, 80, 160))  # beer can hint
    # left arm: punch
    if punch == 0:
        d.ellipse([290, 230, 350, 330], fill=SKIN)     # cocked back
        d.ellipse([295, 290, 355, 350], fill=SKIN_DK)  # fist
    else:
        d.rectangle([290, 250, 420, 300], fill=SKIN)  # extended
        d.ellipse([380, 235, 440, 315], fill=SKIN_DK)  # fist
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
            im = oldhead_frame(2.0, bob, mouth)
        elif f < 216:  # SHOT 2: old head push-in, line2a (3.3-10.7s)
            speaking = 79 <= f <= 257
            step = min(3, (f-72)//36)
            scale = 2.0 + step*0.05
            bob = -8 if speaking and (f//12) % 2 else 0
            mouth = mouth_cycle[(f//6) % len(mouth_cycle)] if speaking else 0
            im = oldhead_frame(scale, bob, mouth)
        elif f < 312:  # SHOT 3: reveal — Broadway, dino, Amos Jr. beating
            im = bg_street.copy()
            lf = f - 216  # 0..95
            # dino guy
            dx, dy = 480, 300
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
            # Amos Jr.: windup / punch cycle
            if lf < 32:
                am, ax = amosjr(0, 0), 760
            elif lf < 48:
                am, ax = amosjr(1, 1), 700   # punch 1, lunged
            elif lf < 64:
                am, ax = amosjr(0, 0), 760
            elif lf < 80:
                am, ax = amosjr(1, 1), 700   # punch 2
            else:
                am, ax = amosjr(0, 0), 780   # standing, done
            shadow(im, ax+210, 700, 260)
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
