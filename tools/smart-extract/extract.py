#!/usr/bin/env python3
"""Smart Extraction Pipeline — vision-guided character part extraction.

"sense → loop → trace → cut → verify"

Replaces dumb flood-fill masking with:
  1. SENSE: vision pass (muse.visual_grounding) locates each part -> bboxes in spec JSON
  2. TRACE + CUT: rembg (isnet-anime for cartoon art) for the base cutout
  3. VERIFY: automated checks + mandatory eye verification loop
  4. POSITION: part placement from measured key-art anchors, never eyeballed

BANNED: flood-fill masking, manual eyeballed crops, blurred-edge cutouts,
"good enough" extractions. (SMART-WAY LAW, owner 2026-10-11.)

Usage:
  extract.py --image key_art.png --spec parts_spec.json --character amos_jr --outdir out/

Spec format (parts_spec.json):
  {
    "image": "path/to/key_art.png",
    "image_size": [1536, 1024],
    "parts": [
      {"name": "head", "bbox": [x0, y0, x1, y1], "pad": 30,
       "notes": "shaggy brown hair, mustache+goatee"},
      ...
    ]
  }
  bbox in PIXELS (convert from 0-1000 normalized visual-grounding output).

Output:
  out/<character>/<part>.png          RGBA cutouts, clean edges
  out/<character>/manifest.json       part anchors, bboxes, verify scores
"""
import argparse, json, os, sys, time

# rembg venv (persistent, ~/workspace — never /tmp)
REMBG_PY = "/home/hatch/workspace/.venvs/rembg/bin/python"


def run_rembg_crop(crop_path, out_path, models=("isnet-anime", "isnet-general-use")):
    """Model ladder: try each model in order, return (model_used, verify_dict).
    The VERIFY loop picks the winner."""
    import subprocess
    last_err = None
    for model in models:
        code = (
            "import sys\n"
            "from rembg import new_session, remove\n"
            "from PIL import Image\n"
            f"sess = new_session({model!r})\n"
            f"im = Image.open({crop_path!r})\n"
            "out = remove(im, session=sess)\n"
            f"out.save({out_path!r})\n"
            "print('rembg-ok')\n"
        )
        r = subprocess.run([REMBG_PY, "-c", code], capture_output=True,
                           text=True, timeout=300)
        if "rembg-ok" in r.stdout:
            return model
        last_err = r.stderr[-300:]
    raise RuntimeError(f"all rembg models failed: {last_err}")


def alpha_cleanup(png_path, despeckle_min_area=25):
    """Remove small disconnected alpha specks (detached chunks). Keeps the
    largest connected component + any component >= despeckle_min_area."""
    from PIL import Image
    import numpy as np
    try:
        from scipy import ndimage
    except ImportError:
        return  # scipy optional; skip if unavailable
    im = Image.open(png_path).convert("RGBA")
    a = np.array(im)[:, :, 3]
    mask = a > 12
    if not mask.any():
        return
    labeled, n = ndimage.label(mask)
    if n <= 1:
        return
    sizes = ndimage.sum(mask, labeled, range(1, n + 1))
    keep = {i + 1 for i, s in enumerate(sizes) if s >= despeckle_min_area}
    # always keep the largest component
    keep.add(int(np.argmax(sizes)) + 1)
    kill = ~np.isin(labeled, list(keep))
    arr = np.array(im)
    arr[kill, 3] = 0
    Image.fromarray(arr).save(png_path)


def verify_part(png_path, spec_part):
    """Automated verification. Returns dict of checks. The agent's own eyes
    are the final gate — these catch what eyes might miss at speed."""
    from PIL import Image
    import numpy as np
    im = Image.open(png_path).convert("RGBA")
    arr = np.array(im)
    a = arr[:, :, 3]
    checks = {}
    # 1. non-empty
    opaque = (a > 12).sum()
    checks["non_empty"] = bool(opaque > 100)
    checks["opaque_px"] = int(opaque)
    # 2. detached chunks: count connected components, flag small ones
    try:
        from scipy import ndimage
        labeled, n = ndimage.label(a > 12)
        sizes = sorted(ndimage.sum(a > 12, labeled, range(1, n + 1)),
                       reverse=True) if n else []
        checks["components"] = int(n)
        checks["small_components"] = int(sum(1 for s in sizes[1:] if s < 25))
        checks["detached_chunks"] = checks["small_components"] > 0
    except ImportError:
        checks["components"] = -1
    # 3. edge fringe: mean alpha in the semi-transparent band.
    #    Normal anti-aliased edges have SOME semi pixels; a true halo/blur
    #    has a WIDE band. Flag only when the band is disproportionate.
    edge = ((a > 12) & (a < 245)).sum()
    checks["semi_px"] = int(edge)
    checks["fringe_ratio"] = float(edge / max(opaque, 1))
    checks["fringe_flag"] = bool(checks["fringe_ratio"] > 0.60)
    # 4. bbox sanity: tight bbox of output vs spec crop
    ys, xs = np.where(a > 12)
    if len(xs):
        checks["tight_bbox"] = [int(xs.min()), int(ys.min()),
                                int(xs.max()), int(ys.max())]
    src_mean = spec_part.get("src_mean_rgb")
    if src_mean:
        out_mean = arr[:, :, :3][a > 12].mean(axis=0)
        import math
        dist = math.dist(out_mean, src_mean)
        checks["color_dist"] = round(float(dist), 1)
        checks["color_flag"] = bool(dist > 90)
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--character", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--model", default="isnet-anime",
                    choices=["isnet-anime", "isnet-general-use", "u2net"])
    ap.add_argument("--pad-default", type=int, default=30)
    a = ap.parse_args()

    from PIL import Image
    spec = json.load(open(a.spec))
    img = Image.open(spec.get("image", a.image)).convert("RGB")
    W, H = img.size

    # group parts by character (per-part "character" overrides --character)
    from collections import defaultdict
    groups = defaultdict(list)
    for part in spec["parts"]:
        groups[part.get("character", a.character)].append(part)

    all_manifests = {}
    for character, parts in groups.items():
        char_dir = os.path.join(a.outdir, character)
        os.makedirs(char_dir, exist_ok=True)
        manifest = {"character": character,
                    "image": spec.get("image", a.image),
                    "image_size": [W, H], "model": a.model,
                    "parts": [], "banned_methods_note":
                    "flood-fill masking banned per SMART-WAY LAW (owner 2026-10-11)"}

        for part in parts:
            name = part["name"]
            x0, y0, x1, y1 = part["bbox"]
            pad = part.get("pad", a.pad_default)
            cx0 = max(0, x0 - pad); cy0 = max(0, y0 - pad)
            cx1 = min(W, x1 + pad); cy1 = min(H, y1 + pad)
            crop = img.crop((cx0, cy0, cx1, cy1))
            crop_path = os.path.join(char_dir, f"_{name}_crop.png")
            out_path = os.path.join(char_dir, f"{name}.png")
            crop.save(crop_path)
            models = part.get("models", ["isnet-anime", "isnet-general-use"])
            print(f"[{name}] crop {crop.size} -> rembg ladder {models}...",
                  flush=True)
            t0 = time.time()
            # model ladder: try each, keep the winner by verify score
            best, best_checks, best_model = None, None, None
            import shutil
            for mi, model in enumerate(models):
                tmp = out_path + f".m{mi}.png"
                try:
                    run_rembg_crop(crop_path, tmp, [model])
                except RuntimeError as e:
                    print(f"[{name}] {model} failed: {e}")
                    continue
                alpha_cleanup(tmp)
                import numpy as _np
                _crop_arr = _np.array(crop)
                part["src_mean_rgb"] = [float(x) for x in
                                        _crop_arr.reshape(-1, 3).mean(axis=0)]
                c = verify_part(tmp, part)
                score = (c["opaque_px"]
                         - 500 * c.get("small_components", 0)
                         - 2000 * c["fringe_ratio"]
                         - 500 * c.get("color_dist", 0))
                if best is None or score > best[0]:
                    if best is not None and os.path.exists(best[1]):
                        os.remove(best[1])
                    best = (score, tmp)
                    best_checks, best_model = c, model
                elif os.path.exists(tmp):
                    os.remove(tmp)
            if best is None:
                raise RuntimeError(f"[{name}] all models failed")
            shutil.move(best[1], out_path)
            checks = best_checks
            checks["model_used"] = best_model
            dt = time.time() - t0
            os.remove(crop_path)  # keep only the cutout
            entry = {"name": name, "file": f"{name}.png",
                     "spec_bbox": [x0, y0, x1, y1],
                     "crop_bbox": [cx0, cy0, cx1, cy1],
                     "notes": part.get("notes", ""),
                     "rembg_seconds": round(dt, 1),
                     "verify": checks}
            manifest["parts"].append(entry)
            flag = "  <-- VERIFY" if (checks.get("detached_chunks") or
                                      checks.get("fringe_flag") or
                                      checks.get("color_flag") or
                                      not checks.get("non_empty")) else ""
            print(f"[{name}] done in {dt:.1f}s model={checks.get('model_used')} "
                  f"opaque={checks['opaque_px']} comps={checks['components']} "
                  f"fringe={checks['fringe_ratio']:.2f} "
                  f"color_dist={checks.get('color_dist', '-')}{flag}")

        mp = os.path.join(char_dir, "manifest.json")
        json.dump(manifest, open(mp, "w"), indent=1)
        print(f"\n[{character}] manifest: {mp}")
        all_manifests[character] = mp
    print("\nNEXT: read every output PNG with your own eyes. "
          "Automated checks catch specks; eyes catch likeness.")


if __name__ == "__main__":
    main()
