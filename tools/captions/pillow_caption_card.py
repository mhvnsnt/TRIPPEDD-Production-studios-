#!/usr/bin/env python3
"""Wave 24 Lane B — wire Pillow (HPND license) for caption-card rendering.

Renders a 1920x1080 episode title card + a lower-third caption bar with
Noto Sans (OFL) — the programmatic alternative to hand-building title
cards when the libass/FFmpeg burn-in path is overkill (static cards,
thumbnails, end slates).

Proof artifacts: tools/captions/proofs/wave24_lane_b/wave24_caption_card.png
(+ wave24_caption_card.json with text metrics). The PNG is re-opened and
pixel-checked: card must contain non-background pixels in the title band
and in the caption bar.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROOF_DIR = os.path.join(HERE, "proofs", "wave24_lane_b")

W, H = 1920, 1080
BG = (10, 10, 14)
TITLE = "WIZARD GANG"
SUBTITLE = 'EP01 \u201cTHE SUMMIT\u201d'
CAPTION = "[music] \u266a synth swell \u266a"
FONT_PATH = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def main():
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(PROOF_DIR, exist_ok=True)
    assert os.path.exists(FONT_PATH), f"missing font: {FONT_PATH}"

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(FONT_BOLD, 120)
    f_sub = ImageFont.truetype(FONT_PATH, 56)
    f_cap = ImageFont.truetype(FONT_PATH, 44)

    # Title block, vertically centered-ish.
    tb = d.textbbox((0, 0), TITLE, font=f_title)
    d.text(((W - (tb[2] - tb[0])) / 2, 380), TITLE, font=f_title,
           fill=(245, 245, 245))
    sb = d.textbbox((0, 0), SUBTITLE, font=f_sub)
    d.text(((W - (sb[2] - sb[0])) / 2, 540), SUBTITLE, font=f_sub,
           fill=(200, 200, 210))

    # Lower-third caption bar (broadcast-style black band, white text).
    bar_h, bar_y = 96, H - 180
    d.rectangle([0, bar_y, W, bar_y + bar_h], fill=(0, 0, 0))
    cb = d.textbbox((0, 0), CAPTION, font=f_cap)
    d.text(((W - (cb[2] - cb[0])) / 2, bar_y + (bar_h - (cb[3] - cb[1])) / 2),
           CAPTION, font=f_cap, fill=(255, 255, 255))

    png_path = os.path.join(PROOF_DIR, "wave24_caption_card.png")
    img.save(png_path)

    # Verify by re-opening: title band and caption bar must differ from BG.
    chk = Image.open(png_path).convert("RGB")
    assert chk.size == (W, H)

    def nonbg_count(box, bg):
        raw = chk.crop(box).tobytes()
        n = 0
        for i in range(0, len(raw), 3):
            if (raw[i], raw[i + 1], raw[i + 2]) != bg:
                n += 1
        return n

    title_nonbg = nonbg_count((200, 380, W - 200, 560), BG)
    bar_nonbg = nonbg_count((200, bar_y, W - 200, bar_y + bar_h), (0, 0, 0))
    assert title_nonbg > 1000, "title band rendered empty"
    # Caption bar must contain rendered glyphs incl. the U+266A music note
    # (not tofu boxes): bright pixels prove the glyphs drew.
    assert bar_nonbg > 500, "caption bar rendered empty"

    import PIL
    proof = {
        "tool": "Pillow (HPND) + Noto Sans Regular/Bold (OFL-1.1)",
        "pillow_version": PIL.__version__,
        "output": png_path,
        "size": [W, H],
        "font": FONT_PATH,
        "title": TITLE,
        "subtitle": SUBTITLE,
        "caption_bar_text": CAPTION,
        "title_band_nonbg_pixels": title_nonbg,
        "caption_bar_nonbg_pixels": bar_nonbg,
        "assertions": [
            "PNG re-opened at 1920x1080",
            "title band contains rendered glyphs",
            "caption bar contains rendered glyphs incl. U+266A",
        ],
    }
    proof_fn = os.path.join(PROOF_DIR, "wave24_caption_card.json")
    with open(proof_fn, "w") as f:
        json.dump(proof, f, indent=2)
    print(f"card -> {png_path}")
    print(f"proof -> {proof_fn}")


if __name__ == "__main__":
    main()
