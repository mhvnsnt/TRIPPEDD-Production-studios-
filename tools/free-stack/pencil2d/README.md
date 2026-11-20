> **Staged here:** adapted from the sweep doc on mhvnsnt/dream-girl, branch
> `tools/production-stack-free` (@91314564, `tools/production-stack-free/sweep/pencil2d/README.md`),
> staged 2026-11-20 (lane B, branch `tools/free-stack-wireup-20261120`).
> The binary lives on release `production-stack-free-20261120` on
> mhvnsnt/dream-girl — it is NOT stored in this repo. Fetch + verify with
> `tools/free-stack/fetch-verify.sh`. Pipeline slot for this repo: see
> `tools/free-stack/PIPELINE-STAGE.md`.

# Pencil2D — Hand-Drawn Frame-by-Frame Animation

**Version:** 0.7.2 (release tag `v0.7.2`) · **Licence:** GPL-2.0 (free, open source)
**Upstream:** https://github.com/pencil2d/pencil — https://www.pencil2d.org/
**Status:** BINARY LANDED on release `production-stack-free-20261120` (verified 2026-11-20).

## Verdict

PULLED and verified. The TVPaint-equivalent find of the sweep: a free,
open-source, raster+vector hand-drawn animation tool — the closest free
pen-first frame-by-frame tool not already in the stack. (OpenToonz and
Krita already cover adjacent ground; Pencil2D is the lightweight,
single-purpose traditional-animation option.)

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `pencil2d-linux-amd64-v0.7.2.AppImage` |
| Size | 60,471,800 B (matches published release asset size exactly) |
| SHA-256 | `4034b036258b6a13d4540911ebce085f31ee18a9dacf438845ac71998d42ff91` (size-exact + GitHub release provenance; the project publishes no SHA256SUMS file for this release) |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, no FUSE needed;
extracted 154M): `AppRun`, `org.pencil2d.Pencil2D.desktop`,
`usr/bin/pencil2d`, `qt.conf`.

Notes: repo last push 2026-11-13 (active). Platforms: Windows, macOS,
Linux, FreeBSD.

## What it is

Hand-drawn frame-by-frame / cel animation — the TVPaint slot for roughs,
timing tests, and simple hand-drawn cuts. Raster + vector layers in one
timeline, bitmap/vector/camera/sound layers, onion skinning, direct
export to MP4, AVI, animated GIF, PNG sequences. Lightweight complement
to Tahoma2D/OpenToonz, not a replacement for either.

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'pencil2d-linux-amd64-v0.7.2.AppImage'
chmod +x pencil2d-linux-amd64-v0.7.2.AppImage
./pencil2d-linux-amd64-v0.7.2.AppImage
# No FUSE: extract instead of mounting:
./pencil2d-linux-amd64-v0.7.2.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the fetch script for all 10 tools at once:
# tools/free-stack/fetch-verify.sh
```

## Honest limits

- No bones, no tweening, no mesh deformation — pure traditional
  frame-by-frame. Anything rigged still goes through the rigging seats
  (Synfig / Rigby2D — see `tools/free-stack/PIPELINE-STAGE.md`).
- Small volunteer project; 0.7.2 is the current stable, not a
  studio-scale pipeline.
- GUI app — no headless render run attempted here; extraction + file
  list is the probe.

## Licence

GPL-2.0. Repo integration is legal — document the version pin on
upgrade. Source + licence logged honestly next to the item, per lane
rule; licence never gated the pull.
