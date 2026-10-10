#!/usr/bin/env python3
"""verify_atlas.py — prove the atlas is exact:
  1. atlas.json parses; every frame rect is inside the sheet bounds.
  2. No two rects overlap (pairwise intersection, padding-aware).
  3. Cropping the sheet at each rect reproduces the thumbnail bytes exactly.
  4. Every thumbnail file on disk is claimed by exactly one atlas entry.
Writes proofs/PROOFS.md with SHA-256 of sources, thumbs, sheet, atlas.
"""
import hashlib, json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PROOFS = os.path.join(HERE, "proofs")
THUMBS = os.path.join(PROOFS, "thumbs")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def overlap(a, b):
    return not (a["x"] + a["w"] <= b["x"] or b["x"] + b["w"] <= a["x"] or
                a["y"] + a["h"] <= b["y"] or b["y"] + b["h"] <= a["y"])

def main():
    atlas = json.load(open(os.path.join(PROOFS, "atlas.json")))
    sheet = Image.open(os.path.join(PROOFS, "spritesheet.png"))
    W, H = sheet.size
    assert (W, H) == (atlas["width"], atlas["height"]), "atlas/sheet size mismatch"
    frames = atlas["frames"]
    names = sorted(frames)
    in_bounds = all(f["x"] >= 0 and f["y"] >= 0 and f["x"] + f["w"] <= W
                    and f["y"] + f["h"] <= H for f in frames.values())
    no_overlap = True
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if overlap(frames[names[i]], frames[names[j]]):
                no_overlap = False
    exact, mismatched = 0, []
    for n in names:
        f = frames[n]
        crop = sheet.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
        thumb = Image.open(os.path.join(THUMBS, n + ".png"))
        if list(crop.getdata()) == list(thumb.getdata()):
            exact += 1
        else:
            mismatched.append(n)
    thumbs_on_disk = sorted(os.path.splitext(p)[0] for p in os.listdir(THUMBS)
                            if p.endswith(".png"))
    coverage_ok = thumbs_on_disk == names
    checks = {
        "frames": len(names), "sheet_size": [W, H],
        "all_rects_in_bounds": bool(in_bounds),
        "no_rect_overlaps": bool(no_overlap),
        "pixel_exact_crops": exact, "mismatched_crops": mismatched,
        "thumb_coverage_1to1": bool(coverage_ok),
    }
    artifacts = {"proofs/spritesheet.png": os.path.join(PROOFS, "spritesheet.png"),
                 "proofs/atlas.json": os.path.join(PROOFS, "atlas.json")}
    for s in ["production/WIZARD_GANG_EP01/ep02-stills/ep02-shot-10-1.png",
              "production/WIZARD_GANG_EP01/ep02-stills/ep02-shot-11-3.png",
              "production/WIZARD_GANG_EP01/ep02-stills/ep02-shot-12-1.png",
              "production/WIZARD_GANG_EP01/ep02-stills-review/ep02-stills-act1.jpg",
              "production/WIZARD_GANG_EP01/ep02-stills-review/ep02-full-lineup.jpg",
              "production/WIZARD_GANG_EP01/ep02-stills-review/ep02-title-card.png"]:
        artifacts[s] = os.path.join(REPO, s)
    for n in names:
        artifacts[f"proofs/thumbs/{n}.png"] = os.path.join(THUMBS, n + ".png")
    hashes = {k: sha256(v) for k, v in sorted(artifacts.items())}
    lines = ["# PROOFS — spritesheet_packer (6 EP02 stills thumbnails)", "",
             "## Verification", "```json", json.dumps(checks, indent=2), "```",
             "", "## SHA-256", ""]
    for k, v in hashes.items():
        lines.append(f"- `{k}`: `{v}`")
    open(os.path.join(PROOFS, "PROOFS.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps(checks, indent=2))
    ok = in_bounds and no_overlap and exact == len(names) and coverage_ok and not mismatched
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
