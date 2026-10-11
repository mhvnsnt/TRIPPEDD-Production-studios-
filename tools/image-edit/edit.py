#!/usr/bin/env python3
"""one-turn: one command = one finished image-edit job.

Gemini does cutout/outline/SVG-trace/magic-select/recolor/eyedropper/fill/
restore in a single prompt. This CLI does the same in a single call with
chainable ops, self-verifying each step (SMART-WAY LAW: see -> verify loop).

Ops (applied left to right, state flows through):
  cutout      subject extraction via the rembg isnet ladder (NEVER flood-fill)
  outline     clean edge outline of the subject -> PNG
  svg         raster -> SVG (vtracer color; potrace fallback for silhouettes)
  select      mask a region: --subject TEXT (agent: pass bbox from visual
              grounding via --bbox), --bbox X1,Y1,X2,Y2 (pixels), or magic
              --at X,Y --tol N
  recolor     HSV-shift the masked region to --color (edges preserved)
  eyedropper  report color at --at / --region (hex + nearest name)
  fill        fill the current mask with --color
  restore     denoise + unsharp sharpen (cheap)
  ai_edit     FREE one-turn AI image edit: --prompt "..." -> AI Horde img2img
              (HF Qwen fallback), auto style_hold + face-likeness verification.
              THE differentiator: FAILs the edit if the face drifted.

Usage:
  edit.py INPUT -o OUTDIR --ops cutout,svg [--subject ...] [--bbox ...] [OP-OPTIONS]

Examples:
  edit.py keyart.png -o out/ --ops cutout,svg --subject "Amos Jr" --bbox 900,280,1330,900
  edit.py photo.png -o out/ --ops select,recolor --at 400,300 --tol 24 --color "#ff0000"
  edit.py photo.png -o out/ --ops eyedropper --at 100,100
  edit.py photo.png -o out/ --ops restore --denoise --sharpen

One-turn agent pattern: run visual grounding ONCE for the subject bbox, then a
single edit.py call. JSON report of everything done -> OUTDIR/report.json.
$0 free tools only. Never generates new imagery - only transforms input pixels.
"""
import argparse, json, os, shutil, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SMART_EXTRACT = REPO / "tools" / "smart-extract"
REMBG_PY = "/home/hatch/workspace/.venvs/rembg/bin/python"

sys.path.insert(0, str(HERE))

# ---------------------------------------------------------------- donors
def run_rembg_crop(crop_path, out_path, models=("isnet-anime", "isnet-general-use")):
    """Donor: tools/smart-extract/extract.py run_rembg_crop (subprocess).

    SMART-WAY improvement: run EVERY model in the ladder and keep the one with
    the most foreground kept (max alpha coverage). The old first-success-wins
    picked isnet-anime even when it ate white-on-light regions.
    """
    import cv2
    from PIL import Image
    best, best_cov, best_model = None, -1, None
    for model in models:
        code = (
            "import sys\n"
            "from rembg import new_session, remove\n"
            "from PIL import Image\n"
            f"im = Image.open(r'''{crop_path}''').convert('RGB')\n"
            f"session = new_session('{model}')\n"
            "out = remove(im, session=session)\n"
            f"out.save(r'''{crop_path}.{model}.png''')\n"
            "print('rembg-ok')\n"
        )
        r = subprocess.run([REMBG_PY, "-c", code], capture_output=True, text=True,
                           timeout=600)
        cand = Path(f"{crop_path}.{model}.png")
        if "rembg-ok" in r.stdout and cand.exists():
            a = cv2.imread(str(cand), cv2.IMREAD_UNCHANGED)[:, :, 3]
            cov = float((a > 10).mean())
            if cov > best_cov:
                best, best_cov, best_model = cand, cov, model
    if best is not None:
        Image.open(best).save(out_path)
        for model in models:  # clean ladder losers
            Path(f"{crop_path}.{model}.png").unlink(missing_ok=True)
        return f"{best_model} (coverage-picked)"
    return None

def alpha_cleanup(png_path, despeckle_min_area=25):
    """Donor: tools/smart-extract/extract.py alpha_cleanup (inline)."""
    import cv2, numpy as np
    img = cv2.imread(str(png_path), cv2.IMREAD_UNCHANGED)
    if img is None or img.shape[2] < 4:
        return False
    alpha = img[:, :, 3]
    n, labels, stats, _ = cv2.connectedComponentsWithStats((alpha > 10).astype("uint8"))
    keep = np.zeros_like(alpha)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= despeckle_min_area:
            keep[labels == i] = 255
    img[:, :, 3] = keep
    cv2.imwrite(str(png_path), img)
    return True

# ---------------------------------------------------------------- state
class Job:
    def __init__(self, inp, outdir):
        from PIL import Image
        self.inp = Path(inp)
        self.outdir = Path(outdir)
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.img = Image.open(inp).convert("RGBA")  # working image
        self.mask = None      # current selection (PIL L)
        self.report = {"input": str(inp), "ops": [], "outputs": {},
                       "verify": {}, "t0": time.time()}
        self.n = 0

    def save(self, name, img=None):
        self.n += 1
        p = self.outdir / f"{self.n:02d}_{name}"
        (img or self.img).save(p)
        return p

    def log(self, op, detail, out=None):
        self.report["ops"].append({"op": op, **detail})
        if out:
            self.report["outputs"][op] = str(out)

# ---------------------------------------------------------------- ops
def op_cutout(job, args):
    from PIL import Image
    import numpy as np
    W, H = job.img.size
    if args.bbox:
        x1, y1, x2, y2 = [int(v) for v in args.bbox.split(",")]
    elif args.subject:
        raise SystemExit("cutout --subject needs --bbox: run visual grounding "
                         "first (one agent turn), then pass --bbox X1,Y1,X2,Y2")
    else:
        x1, y1, x2, y2 = 0, 0, W, H
    x1, y1 = max(0, x1), max(0, y1); x2, y2 = min(W, x2), min(H, y2)
    crop = job.outdir / "_crop.png"
    job.img.crop((x1, y1, x2, y2)).convert("RGB").save(crop)
    cut = job.outdir / "_cut.png"
    model = run_rembg_crop(str(crop), str(cut))
    if not model:
        job.report["verify"]["cutout"] = "FAIL: rembg ladder failed"
        raise SystemExit("cutout failed: rembg ladder produced nothing")
    alpha_cleanup(cut)
    part = Image.open(cut).convert("RGBA")
    if args.exclude:
        import cv2
        ex1, ey1, ex2, ey2 = [int(v) for v in args.exclude.split(",")]
        pa = np.array(part)
        # exclude rect is in ORIGINAL coords; shift into crop coords
        pa[max(0, ey1 - y1):ey2 - y1, max(0, ex1 - x1):ex2 - x1, 3] = 0
        part = Image.fromarray(pa)
    # paste back onto transparent canvas at original position
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.paste(part, (x1, y1), part)
    job.img = canvas
    out = job.save("cutout.png")
    a = np.array(part)[:, :, 3]
    cov = float((a > 10).mean())
    job.report["verify"]["cutout"] = ("PASS" if 0.01 < cov < 0.99 else "FAIL") + \
        f" model={model} coverage={cov:.3f} bbox=({x1},{y1},{x2},{y2})"
    job.log("cutout", {"subject": args.subject, "model": model,
                       "coverage": round(cov, 4)}, out)

def op_outline(job, args):
    import cv2, numpy as np
    from PIL import Image
    a = np.array(job.img)[:, :, 3]
    cnts, _ = cv2.findContours((a > 128).astype("uint8"),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = Image.new("RGBA", job.img.size, (0, 0, 0, 0))
    arr = np.array(out)  # writable copy (asarray is readonly)
    cv2.drawContours(arr, cnts, -1,
                     hex_to_bgr(args.color) + (255,), args.width)
    p = job.save("outline.png", Image.fromarray(arr))
    job.report["verify"]["outline"] = \
        "PASS" if len(cnts) else "FAIL: no contours"
    job.log("outline", {"contours": len(cnts), "color": args.color,
                        "width": args.width}, p)

def op_svg(job, args):
    p = job.outdir / "vector.svg"
    ok = via_vtracer(job.img, str(p)) or via_potrace(job.img, str(p))
    job.report["verify"]["svg"] = "PASS" if ok and p.exists() else "FAIL"
    job.log("svg", {"backend": "vtracer" if ok == "vtracer" else "potrace"}, p if ok else None)
    if not ok:
        raise SystemExit("svg failed: no backend worked")

def via_vtracer(img, dst):
    """vtracer via the persistent rembg venv (donor pattern: extract.py)."""
    import tempfile
    rgba_path = Path(dst).with_suffix(".rgba.png")
    img.convert("RGBA").save(rgba_path)
    code = (
        "import sys\n"
        "import vtracer, numpy as np\n"
        "from PIL import Image\n"
        f"rgba = np.array(Image.open(r'''{rgba_path}''').convert('RGBA'))\n"
        "flat = rgba.reshape(-1, 4)\n"
        "pixels = tuple(tuple(int(c) for c in px) for px in flat)\n"
        "svg = vtracer.convert_pixels_to_svg(\n"
        "    pixels, size=(rgba.shape[1], rgba.shape[0]),\n"
        "    colormode='color', hierarchical='stacked', mode='spline',\n"
        "    filter_speckle=8, color_precision=6, layer_difference=16,\n"
        "    corner_threshold=60, length_threshold=4.0, splice_threshold=45,\n"
        "    path_precision=3)\n"
        f"open(r'''{dst}''', 'w').write(svg)\n"
        "print('vtracer-ok')\n"
    )
    r = subprocess.run([REMBG_PY, "-c", code], capture_output=True, text=True,
                       timeout=600)
    rgba_path.unlink(missing_ok=True)
    if "vtracer-ok" in r.stdout and Path(dst).exists():
        return "vtracer"
    print(f"[svg] vtracer venv failed: {r.stderr[-300:]}", file=sys.stderr)
    return None

def via_potrace(img, dst):
    # Donor pattern: font-wizard/tools/art-stack/vectorize.py (potrace->vtracer)
    import numpy as np
    from PIL import Image
    if not shutil.which("potrace"):
        return None
    a = np.array(img.convert("RGBA"))[:, :, 3]
    bw = (a > 128).astype("uint8")
    tmp = Path(dst).with_suffix(".pbm")
    Image.fromarray((bw * 255).astype("uint8")).save(tmp)
    r = subprocess.run(["potrace", str(tmp), "-s", "-o", dst,
                        "--turdsize", "4"], capture_output=True)
    tmp.unlink(missing_ok=True)
    return "potrace" if r.returncode == 0 else None

def op_select(job, args):
    from PIL import Image, ImageDraw
    import numpy as np
    W, H = job.img.size
    if args.bbox:
        x1, y1, x2, y2 = [int(v) for v in args.bbox.split(",")]
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle([x1, y1, x2, y2], fill=255)
        src = f"bbox({x1},{y1},{x2},{y2})"
    elif args.subject and not args.at:
        raise SystemExit("select --subject needs --bbox or --at: run visual "
                         "grounding first, then pass --bbox X1,Y1,X2,Y2")
    elif args.at:
        x, y = [int(v) for v in args.at.split(",")]
        m = magic_mask(job.img, x, y, args.tol)
        src = f"magic({x},{y},tol={args.tol})"
    else:
        raise SystemExit("select needs --bbox, --at, or --subject+--bbox")
    job.mask = m
    p = job.save("mask.png", m.convert("RGBA"))
    cov = float((np.array(m) > 10).mean())
    job.report["verify"]["select"] = \
        ("PASS" if cov > 0 else "FAIL") + f" coverage={cov:.3f} src={src}"
    job.log("select", {"src": src, "coverage": round(cov, 4)}, p)

def magic_mask(img, x, y, tol):
    """Magic-wand select: connected region of similar color (LAB distance)."""
    import cv2, numpy as np
    from PIL import Image
    from scipy import ndimage
    rgb = np.array(img.convert("RGB"))
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype("float32")
    seed = lab[y, x]
    dist = np.linalg.norm(lab - seed, axis=2)
    cand = (dist < tol).astype("uint8")
    lab_, n = ndimage.label(cand)
    m = Image.fromarray((lab_ == lab_[y, x]).astype("uint8") * 255)
    return m

def op_recolor(job, args):
    import cv2, numpy as np
    from PIL import Image
    if job.mask is None:
        raise SystemExit("recolor needs a select first")
    rgb = np.array(job.img.convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype("float32")
    tr, tg, tb = hex_to_rgb(args.color)
    th, ts, _ = cv2.cvtColor(np.uint8([[[tb, tg, tr]]]),
                             cv2.COLOR_BGR2HSV)[0, 0].astype("float32")
    m = (np.array(job.mask) > 10)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    H[m] = th                       # target hue
    S[m] = np.clip(S[m] * (ts / 255.0) * 1.2, 0, 255)  # push toward target sat
    out = cv2.cvtColor(np.stack([H, S, V], -1).astype("uint8"),
                       cv2.COLOR_HSV2RGB)
    rgba = np.array(job.img)
    rgba[..., :3][m] = out[m]
    job.img = Image.fromarray(rgba)
    p = job.save("recolor.png")
    job.report["verify"]["recolor"] = "PASS"
    job.log("recolor", {"color": args.color, "px": int(m.sum())}, p)

CSS_COLORS = {"black": "000000", "white": "ffffff", "red": "ff0000",
    "green": "008000", "blue": "0000ff", "yellow": "ffff00", "orange": "ffa500",
    "purple": "800080", "pink": "ffc0cb", "brown": "a52a2a", "gray": "808080",
    "cyan": "00ffff", "magenta": "ff00ff", "lime": "00ff00", "navy": "000080",
    "teal": "008080", "maroon": "800000", "olive": "808000"}

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def hex_to_bgr(h):
    r, g, b = hex_to_rgb(h)
    return (b, g, r)

def nearest_name(rgb):
    import math
    best, bd = "custom", 1e9
    for name, hx in CSS_COLORS.items():
        cr = hex_to_rgb(hx)
        d = math.dist(rgb, cr)
        if d < bd:
            bd, best = d, name
    return best

def op_eyedropper(job, args):
    import numpy as np
    rgb = np.array(job.img.convert("RGB"))
    if args.region:
        x1, y1, x2, y2 = [int(v) for v in args.region.split(",")]
        px = rgb[y1:y2, x1:x2].reshape(-1, 3)
    elif args.at:
        x, y = [int(v) for v in args.at.split(",")]
        px = rgb[max(0, y-2):y+3, max(0, x-2):x+3].reshape(-1, 3)
    else:
        raise SystemExit("eyedropper needs --at X,Y or --region X1,Y1,X2,Y2")
    med = tuple(int(v) for v in np.median(px, axis=0))
    hx = "#%02x%02x%02x" % med
    name = nearest_name(med)
    print(f"{hx} ({name})")
    job.report["verify"]["eyedropper"] = "PASS"
    job.log("eyedropper", {"hex": hx, "name": name})

def op_fill(job, args):
    import numpy as np
    from PIL import Image
    if job.mask is None:
        if args.at:
            x, y = [int(v) for v in args.at.split(",")]
            job.mask = magic_mask(job.img, x, y, args.tol)
        else:
            raise SystemExit("fill needs a select first or --at X,Y")
    rgba = np.array(job.img)
    m = np.array(job.mask) > 10
    rgba[..., :3][m] = hex_to_rgb(args.color)
    job.img = Image.fromarray(rgba)
    p = job.save("fill.png")
    job.report["verify"]["fill"] = "PASS"
    job.log("fill", {"color": args.color, "px": int(m.sum())}, p)

def op_restore(job, args):
    import cv2, numpy as np
    from PIL import Image
    rgb = np.array(job.img.convert("RGB"))
    if args.denoise:
        rgb = cv2.fastNlMeansDenoisingColored(rgb, None, 7, 7, 7, 21)
    if args.sharpen:
        blur = cv2.GaussianBlur(rgb, (0, 0), 2.0)
        rgb = cv2.addWeighted(rgb, 1.6, blur, -0.6, 0)
    a = np.array(job.img)[:, :, 3]
    job.img = Image.fromarray(np.dstack([rgb, a]).astype("uint8"))
    p = job.save("restore.png")
    job.report["verify"]["restore"] = "PASS"
    job.log("restore", {"denoise": args.denoise, "sharpen": args.sharpen}, p)

def op_ai_edit(job, args):
    """ai_edit: free one-turn AI image edit + self-verification (donor: ai_edit.py)."""
    import tempfile
    from PIL import Image
    if not args.prompt:
        raise SystemExit("ai_edit needs --prompt \"describe the edit in plain language\"")
    import ai_edit as AE
    tmp = tempfile.mkdtemp(prefix="ai_edit_")
    src = os.path.join(tmp, "src.png")
    dst = os.path.join(tmp, "out.png")
    job.img.convert("RGB").save(src)
    # run the backend chain directly (not via CLI) for in-pipeline use
    order = [b.strip() for b in args.backends.split(",") if b.strip()]
    available = dict(AE.BACKENDS)
    errors, data, backend_used = {}, None, None
    for name in order:
        fn = available.get(name)
        if not fn:
            errors[name] = "unknown backend"
            continue
        try:
            data, _meta = fn(src, args.prompt, max_wait=args.max_wait)
            backend_used = name
            break
        except Exception as e:
            errors[name] = f"{type(e).__name__}: {str(e)[:200]}"
    if data is None:
        job.report["verify"]["ai_edit"] = f"FAIL: all backends failed {errors}"
        raise SystemExit(f"ai_edit failed: all backends failed: {errors}")
    with open(dst, "wb") as f:
        f.write(data)
    job.img = Image.open(dst).convert("RGBA")
    out = job.save("ai_edit.png")
    detail = {"backend": backend_used, "prompt": args.prompt[:200],
              "backend_errors": errors}
    if args.no_verify:
        job.report["verify"]["ai_edit"] = "DONE_UNVERIFIED"
    else:
        v = AE.verify_edit(src, dst, face_threshold=args.face_threshold)
        detail.update(v)
        job.report["verify"]["ai_edit"] = v["overall"] + \
            f" backend={backend_used} style_hold={v.get('style_hold')} " \
            f"face_drift={v.get('face_drift')}"
        if v["overall"] == "FAIL":
            job.log("ai_edit", detail, out)
            raise SystemExit(
                f"ai_edit verification FAILED (backend={backend_used} "
                f"style_hold={v.get('style_hold')} face_drift={v.get('face_drift')} "
                f"> threshold {args.face_threshold}). Output kept at {out} for inspection.")
    job.log("ai_edit", detail, out)

# ---------------------------------------------------------------- main
OPS = ["cutout", "outline", "svg", "select", "recolor",
       "eyedropper", "fill", "restore", "ai_edit"]

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("input")
    ap.add_argument("-o", "--outdir", default="out")
    ap.add_argument("--ops", required=True,
                    help="comma-separated ops: " + ",".join(OPS))
    ap.add_argument("--subject")
    ap.add_argument("--bbox")
    ap.add_argument("--exclude",
                    help="cutout only: zero alpha in X1,Y1,X2,Y2 pixels "
                         "(cut a neighbor out of the crop)")
    ap.add_argument("--at")
    ap.add_argument("--region")
    ap.add_argument("--tol", type=float, default=24)
    ap.add_argument("--color", default="#ff0000")
    ap.add_argument("--width", type=int, default=6)
    ap.add_argument("--denoise", action="store_true")
    ap.add_argument("--sharpen", action="store_true")
    # ai_edit options
    ap.add_argument("--prompt", default="",
                    help="ai_edit: plain-language edit instruction (one turn)")
    ap.add_argument("--face-threshold", type=float, default=0.08,
                    help="ai_edit: max allowed face-ROI drift 0..1 (FAIL above)")
    ap.add_argument("--max-wait", type=int, default=480,
                    help="ai_edit: max seconds per backend before falling through")
    ap.add_argument("--backends", default="ai_horde,hf_qwen",
                    help="ai_edit: backend order to try")
    ap.add_argument("--no-verify", action="store_true",
                    help="ai_edit: skip style_hold + face checks")
    args = ap.parse_args()

    job = Job(args.input, args.outdir)
    fn = {"cutout": op_cutout, "outline": op_outline, "svg": op_svg,
          "select": op_select, "recolor": op_recolor,
          "eyedropper": op_eyedropper, "fill": op_fill,
          "restore": op_restore, "ai_edit": op_ai_edit}
    ops = [o.strip() for o in args.ops.split(",") if o.strip()]
    bad = [o for o in ops if o not in fn]
    if bad:
        raise SystemExit(f"unknown ops: {bad} (choose from {OPS})")
    try:
        for op in ops:
            fn[op](job, args)
    except SystemExit as e:
        job.report["verify"]["FATAL"] = str(e)
        raise
    finally:
        job.report["dt_s"] = round(time.time() - job.report.pop("t0"), 2)
        rp = job.outdir / "report.json"
        rp.write_text(json.dumps(job.report, indent=2))
        print(f"[one-turn] {len(job.report['ops'])} ops, "
              f"{job.report['dt_s']}s -> {job.outdir}")
        print(json.dumps(job.report["verify"], indent=2))

if __name__ == "__main__":
    main()
