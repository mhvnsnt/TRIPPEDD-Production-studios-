#!/usr/bin/env python3
"""WedgeRunner (SPEC H-2) — PDG-style wedge / batch-variation driver.

Original implementation. Extends the studio's existing headless-Blender
driver pattern (``blender -b [scene.blend] --python <script> -- <args>``,
as used by the Cape Jones render-proof lanes) into a batch wedge tool:

  * reads a JSON wedge list of named parameter sets,
  * runs EACH variant as its own headless Blender process, with its own
    log file, output directory and result record,
  * a variant that crashes / times out / produces no output is recorded
    as failed and NEVER kills the batch,
  * emits a tiled-PNG contact sheet + an HTML preview page + a
    summary.json (variant -> status / output / sha256 / log).

Usage:
    python3 wedgerunner.py --wedge examples/example_wedge.json \
        --blender /path/to/blender [--out DIR] [--timeout 600] [--strict]

Exit code: 0 when the batch ran to completion (read summary.json for
per-variant truth); 1 with --strict if any variant failed; 2 on a
wedge-file / configuration error (nothing was run).

Wedge JSON schema and the parameter-injection mechanism are documented
in README.md. The in-Blender half is blender_driver.py next to this file.
"""
import argparse
import hashlib
import html
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRIVER = HERE / "blender_driver.py"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve(base, maybe_rel):
    if not maybe_rel:
        return None
    p = Path(maybe_rel)
    return p if p.is_absolute() else (base / p).resolve()


def run_variant(blender, wedge, variant, out_root, timeout):
    name = variant["name"]
    vdir = out_root / name
    vdir.mkdir(parents=True, exist_ok=True)
    variant_json = vdir / "variant.json"
    variant_json.write_text(json.dumps(variant, indent=2), encoding="utf-8")
    render_out = vdir / "render.png"
    log_path = vdir / "blender.log"

    cmd = [str(blender), "-b"]
    blend = resolve(wedge["_base"], wedge.get("blend_file"))
    if blend:
        cmd.append(str(blend))
    cmd += ["--python-exit-code", "1", "--python", str(DRIVER), "--",
            "--variant-json", str(variant_json), "--out", str(render_out)]
    scene_script = resolve(wedge["_base"], wedge.get("scene_script"))
    if scene_script:
        cmd += ["--scene-script", str(scene_script)]

    env = dict(os.environ)
    env.pop("PYTHONPATH", None)  # Blender bundles its own python/numpy
    started = time.time()
    status, error, exit_code = "failed", None, None
    try:
        with open(log_path, "w", encoding="utf-8") as log:
            proc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT,
                                  timeout=timeout, env=env)
        exit_code = proc.returncode
        if exit_code == 0 and render_out.is_file() and render_out.stat().st_size > 0:
            status = "ok"
        else:
            error = f"blender exit code {exit_code}" if exit_code != 0 else "no render output produced"
    except subprocess.TimeoutExpired:
        status, error = "timeout", f"exceeded --timeout {timeout}s; process killed"
    except Exception as exc:  # spawn failure etc. — record, don't die
        error = f"{type(exc).__name__}: {exc}"
    rec = {
        "name": name,
        "status": status,
        "exit_code": exit_code,
        "duration_s": round(time.time() - started, 2),
        "params": variant.get("params", {}),
        "output": str(render_out) if status == "ok" else None,
        "output_bytes": render_out.stat().st_size if status == "ok" else None,
        "output_sha256": sha256_of(render_out) if status == "ok" else None,
        "log": str(log_path),
    }
    if error:
        rec["error"] = error
    (vdir / "result.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
    print(f"[wedgerunner] {name}: {status} ({rec['duration_s']}s)", flush=True)
    return rec


def make_contact_sheet(records, out_root, cols=3, thumb=256):
    """Tiled PNG contact sheet via PIL. Returns path or None."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("[wedgerunner] PIL unavailable — skipping PNG contact sheet", file=sys.stderr)
        return None
    ok = [r for r in records if r["status"] == "ok"]
    tiles = ok if ok else records
    if not tiles:
        return None
    label_h = 22
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb, rows * (thumb + label_h)), (24, 24, 24))
    draw = ImageDraw.Draw(sheet)
    for i, rec in enumerate(tiles):
        x, y = (i % cols) * thumb, (i // cols) * (thumb + label_h)
        if rec["status"] == "ok":
            with Image.open(rec["output"]) as im:
                im = im.convert("RGB")
                im.thumbnail((thumb, thumb))
                sheet.paste(im, (x + (thumb - im.width) // 2, y))
        draw.text((x + 6, y + thumb + 5), f"{rec['name']} [{rec['status']}]", fill=(255, 255, 80))
    path = out_root / "contact_sheet.png"
    sheet.save(path)
    return path


def make_preview_page(records, out_root, batch_name):
    rows = []
    for r in records:
        img = (f'<img src="{html.escape(r["name"])}/render.png" width="256">'
               if r["status"] == "ok" else "<em>no render</em>")
        rows.append(f"<tr><td>{img}</td><td>{html.escape(r['name'])}</td>"
                    f"<td>{html.escape(r['status'])}</td>"
                    f"<td>{html.escape(json.dumps(r['params']))}</td></tr>")
    page = ("<!doctype html><meta charset='utf-8'>"
            f"<title>WedgeRunner — {html.escape(batch_name)}</title>"
            "<h1>WedgeRunner contact sheet</h1>"
            f"<p>{html.escape(batch_name)} — {sum(r['status']=='ok' for r in records)}/"
            f"{len(records)} variants ok</p>"
            "<table border='1' cellspacing='0' cellpadding='6'>"
            "<tr><th>render</th><th>variant</th><th>status</th><th>params</th></tr>"
            + "".join(rows) + "</table>")
    path = out_root / "index.html"
    path.write_text(page, encoding="utf-8")
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description="WedgeRunner — headless Blender wedge/batch driver (SPEC H-2)")
    ap.add_argument("--wedge", required=True, help="wedge JSON file")
    ap.add_argument("--blender", default=os.environ.get("BLENDER_BIN"),
                    help="Blender binary (or set BLENDER_BIN)")
    ap.add_argument("--out", help="output directory (default: wedge's output_dir or ./wedge_out)")
    ap.add_argument("--timeout", type=int, default=600, help="per-variant timeout seconds (default 600)")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any variant failed")
    args = ap.parse_args(argv)

    wedge_path = Path(args.wedge).resolve()
    try:
        wedge = json.loads(wedge_path.read_text(encoding="utf-8"))
        variants = wedge["variants"]
        assert isinstance(variants, list) and variants
        names = [v["name"] for v in variants]
        assert len(names) == len(set(names)), "variant names must be unique"
    except Exception as exc:
        print(f"[wedgerunner] invalid wedge file {wedge_path}: {exc}", file=sys.stderr)
        return 2
    blender = args.blender or wedge.get("blender")
    if not blender or not Path(blender).is_file():
        print(f"[wedgerunner] Blender binary not found: {blender!r} "
              "(pass --blender or set BLENDER_BIN)", file=sys.stderr)
        return 2
    wedge["_base"] = str(wedge_path.parent)
    out_root = Path(args.out or wedge.get("output_dir") or "wedge_out")
    if not out_root.is_absolute():
        out_root = (wedge_path.parent / out_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    records = [run_variant(blender, wedge, v, out_root, args.timeout) for v in variants]
    sheet = make_contact_sheet(records, out_root)
    page = make_preview_page(records, out_root, wedge.get("name", wedge_path.stem))
    summary = {
        "batch": wedge.get("name", wedge_path.stem),
        "wedge_file": str(wedge_path),
        "blender": str(blender),
        "generated_at_epoch": int(time.time()),
        "counts": {"total": len(records),
                   "ok": sum(r["status"] == "ok" for r in records),
                   "failed": sum(r["status"] == "failed" for r in records),
                   "timeout": sum(r["status"] == "timeout" for r in records)},
        "contact_sheet_png": str(sheet) if sheet else None,
        "preview_page_html": str(page),
        "variants": records,
    }
    (out_root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[wedgerunner] done: {summary['counts']['ok']}/{len(records)} ok -> {out_root}/summary.json")
    if args.strict and summary["counts"]["ok"] != len(records):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
