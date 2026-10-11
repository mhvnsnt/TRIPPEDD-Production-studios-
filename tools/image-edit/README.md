# one-turn image edit toolkit

One command = one finished job. The answer to "Gemini does it in one prompt,
we take twenty turns" (owner + Tyneshia, 2026-10-11).

## Ops (chainable, left to right)

| op | what | donor |
|---|---|---|
| `cutout` | subject extraction, rembg isnet ladder | `tools/smart-extract/` |
| `outline` | clean edge outline PNG | new (OpenCV contours) |
| `svg` | raster → SVG (vtracer color, potrace fallback) | `font-wizard/tools/art-stack/vectorize.py` pattern |
| `select` | mask region: `--bbox`, magic `--at X,Y --tol N`, or `--subject`+`--bbox` | new |
| `recolor` | HSV-shift masked region to `--color` (edges preserved) | new |
| `eyedropper` | color at `--at`/`--region` → hex + name | new |
| `fill` | fill current mask with `--color` | new |
| `restore` | denoise (`--denoise`) + unsharp (`--sharpen`) | OpenCV |

## Usage

```bash
# one-turn cutout + vector trace (the proving run):
edit.py keyart.png -o out/ --ops cutout,svg --subject "Amos Jr, beer-can guy" --bbox 900,280,1330,900

# magic-select a region and recolor it red:
edit.py photo.png -o out/ --ops select,recolor --at 400,300 --tol 24 --color "#ff0000"

# sample a color:
edit.py photo.png -o out/ --ops eyedropper --at 100,100

# restore a photo:
edit.py photo.png -o out/ --ops restore --denoise --sharpen
```

Agent pattern (one turn): run visual grounding ONCE for the subject bbox,
then ONE `edit.py` call. `--bbox` is pixels `X1,Y1,X2,Y2`.

## Verification

Every op self-checks (coverage, components, file existence) into
`report.json`. The agent's eye-read of the outputs is the final gate —
**visual FAIL overrides numerical PASS** (repo law).

## Rules

- $0 free tools only. rembg runs in the persistent venv
  `~/workspace/.venvs/rembg`; vtracer pip-installs into it if missing.
- NEVER flood-fill for extraction (SMART-WAY LAW). Magic-select is a
  color-similarity region op for recolor/fill, not an extraction cutter.
- Never AI-generate new imagery — transform input pixels only.
