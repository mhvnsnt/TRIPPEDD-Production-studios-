"""
CONTACT SHEET — every pose, every view, one image, with its numbers on it.

A folder of thirty PNGs is not evidence anyone will actually look at. A sheet
is, and putting the MEASUREMENT on the frame it came from is what stops a
number and a picture drifting apart — which is how "the mouth opens" survived
three passes while the renders showed a plug.

  .trippedd_venv/bin/python tools/character/contact_sheet.py [--view mouth]
"""
import json, os, sys, glob

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
SRC = os.path.abspath(opt("--src", "renders/_mouth_proof"))
VIEW = opt("--view", "front")
OUT = os.path.abspath(opt("--out", os.path.join(SRC, "CONTACT_%s.png" % VIEW)))
COLS = int(opt("--cols", "5"))
CELL = int(opt("--cell", "460"))

from PIL import Image, ImageDraw, ImageFont

proof = {}
pj = os.path.join(SRC, "mouth_proof.json")
if os.path.exists(pj):
    proof = {r["pose"]: r for r in json.load(open(pj))["poses"]}

frames = sorted(glob.glob(os.path.join(SRC, "*_%s.png" % VIEW)))
if not frames:
    sys.exit("no %s frames in %s" % (VIEW, SRC))

def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

BAR = 62
rows = (len(frames) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * CELL, rows * (CELL + BAR)), (14, 14, 18))
d = ImageDraw.Draw(sheet)
f_title, f_num = font(19), font(14)

for i, path in enumerate(frames):
    name = os.path.basename(path).rsplit("_%s.png" % VIEW, 1)[0]
    im = Image.open(path).convert("RGB").resize((CELL, CELL), Image.LANCZOS)
    x, y = (i % COLS) * CELL, (i // COLS) * (CELL + BAR)
    sheet.paste(im, (x, y))
    d.rectangle([x, y + CELL, x + CELL, y + CELL + BAR], fill=(22, 22, 28))
    d.text((x + 10, y + CELL + 6), name.replace("_", " "), font=f_title, fill=(235, 235, 245))
    r = proof.get(name)
    if r:
        v = r["visible"]
        d.text((x + 10, y + CELL + 30),
               "jaw %.0f°  gap %.1f%%HH" % (r["jawDeg"], r["lipGapPercentOfHeadHeight"]),
               font=f_num, fill=(150, 200, 255))
        d.text((x + 200, y + CELL + 30),
               "teeth %.1f  tongue %.1f  cavity %.1f" % (v["teeth"], v["tongue"], v["cavity"]),
               font=f_num, fill=(255, 200, 150))
    d.rectangle([x, y, x + CELL - 1, y + CELL + BAR - 1], outline=(45, 45, 55))

sheet.save(OUT)
print("%s  %d frames  %dx%d" % (OUT, len(frames), sheet.size[0], sheet.size[1]))
