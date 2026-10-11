# TOOLS.md — trippedd-studio

Free art/editing stack. Everything is open-source, local, costs nothing.
Per repo law (DONOR FIRST): this repo does not duplicate the stack — it
wires into the shared home base.

## Wired: Free Art Stack

Home: `~/workspace/font-wizard/tools/art-stack/` (full docs in that repo's
TOOLS.md). Shim: `tools/art-stack/README.md`.

```bash
AS=~/workspace/font-wizard/tools/art-stack

# Background removal / cutouts (SOTA matting)
$AS/run.sh bg_remove.py photo.jpg cutout.png --model birefnet-general

# Erase objects / fence wires (mask = white where you want gone)
$AS/run.sh inpaint.py in.jpg mask.png out.jpg --radius 5

# Raster -> SVG (logos, card art)
$AS/run.sh vectorize.py logo.png logo.svg

# Text overlays (network cards, bumpers, thumbnails)
$AS/run.sh composite.py --bg card.png --text "STAY TRIPPEDD" \
    --size 120 --fill white --stroke 4 --pos center --out final.png

# Video shortcuts (Shorts cuts, trims, caption burns, GIFs)
$AS/run.sh vid.py vertical in.mp4 out.mp4
$AS/run.sh vid.py trim in.mp4 3 12 out.mp4
$AS/run.sh vid.py captions in.mp4 subs.srt out.mp4
```

## Pocket Studio (mobile web UI)

The same inpaint / text-overlay / video-cut tools are also wrapped in
Pocket Studio for phone use:
`~/workspace/video-fix-tools/pocket-studio/` — tools `inpaint`,
`textcard`, `vidcut` alongside the existing bgremove/sticker/trace/etc.

## Existing animation pipeline (don't duplicate)

- Playbook: `~/workspace/animation-techniques/ANIMATION-PLAYBOOK.md`
- Per-shot QC: `~/workspace/animation-techniques/PIPELINE-CHECKLIST.md`
- Free toolkit: `~/workspace/animation-techniques/tools/TOOLKIT.md`

## Provenance

Free Art Stack wired 2026-10-10 (owner: "wire up all that's free").
Branch `feature/free-art-stack`.
