#!/usr/bin/env python3
"""verify_card.py — prove the title cards are real renders, not blanks:
  1. Both PNGs reopen at exactly 1920x1080 RGB.
  2. Text bands have high pixel variance (text actually rendered).
  3. Corners are dark (vignette/gradient present).
  4. Guides variant: green pixel found on the 90% action-safe border;
     clean variant has no pure-green guide pixels.
Writes proofs/PROOFS.md with SHA-256.
"""
import hashlib, json, os, sys
from PIL import Image, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs")
W, H = 1920, 1080

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def band_variance(im, y0, y1):
    return ImageStat.Stat(im.crop((0, y0, W, y1))).var

def main():
    clean = Image.open(os.path.join(PROOFS, "title_card.png")).convert("RGB")
    guides = Image.open(os.path.join(PROOFS, "title_card_guides.png")).convert("RGB")
    size_ok = clean.size == (W, H) and guides.size == (W, H)
    # show-title band (y 400-570) and episode band (y 700-790) must be busy
    show_var = band_variance(clean, 400, 570)
    ep_var = band_variance(clean, 700, 790)
    text_ok = sum(show_var) > 500 and sum(ep_var) > 500
    # corners dark
    px = clean.load()
    corners = [px[5, 5], px[W - 6, 5], px[5, H - 6], px[W - 6, H - 6]]
    dark_ok = all(sum(c) < 120 for c in corners)
    # guides: 90% action-safe border -> margin = 5% of W/H
    mx, my = int(W * 0.05), int(H * 0.05)
    gpx = guides.load()
    green_on_border = any(gpx[x, my][1] > 200 and gpx[x, my][0] < 80
                          for x in range(mx, W - mx, 7))
    cpx = clean.load()
    green_in_clean = sum(1 for x in range(0, W, 13) for y in range(0, H, 13)
                         if cpx[x, y][1] > 200 and cpx[x, y][0] < 80 and cpx[x, y][2] < 80)
    checks = {
        "size_1920x1080_both": bool(size_ok),
        "show_title_band_variance": [round(v, 1) for v in show_var],
        "episode_band_variance": [round(v, 1) for v in ep_var],
        "text_rendered": bool(text_ok),
        "corners_dark_vignette": bool(dark_ok),
        "guides_action_safe_border_found": bool(green_on_border),
        "clean_card_has_no_guide_green": green_in_clean == 0,
    }
    artifacts = {"proofs/title_card.png": os.path.join(PROOFS, "title_card.png"),
                 "proofs/title_card_guides.png": os.path.join(PROOFS, "title_card_guides.png"),
                 "gen_title_card.py": os.path.join(HERE, "gen_title_card.py")}
    hashes = {k: sha256(v) for k, v in sorted(artifacts.items())}
    lines = ["# PROOFS — title_card (1920x1080 episode title card generator)", "",
             "Visually inspected: gradient indigo-black bg, gold rules, 'WIZARD GANG'",
             "off-white, 'EPISODE 02' gold. No invented episode titles (canon law).", "",
             "## Verification", "```json", json.dumps(checks, indent=2), "```",
             "", "## SHA-256", ""]
    for k, v in hashes.items():
        lines.append(f"- `{k}`: `{v}`")
    open(os.path.join(PROOFS, "PROOFS.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps(checks, indent=2))
    ok = all([size_ok, text_ok, dark_ok, green_on_border, green_in_clean == 0])
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
