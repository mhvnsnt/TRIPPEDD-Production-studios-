# art-stack (shim)

This repo wires into the shared **Free Art Stack** — home base is
`~/workspace/font-wizard/tools/art-stack/` (branch `feature/free-art-stack`).

Don't duplicate the tools here. Call them via:

```bash
AS=~/workspace/font-wizard/tools/art-stack
$AS/run.sh bg_remove.py photo.jpg cutout.png --model birefnet-general
$AS/run.sh inpaint.py in.jpg mask.png out.jpg --radius 5
$AS/run.sh vectorize.py logo.png logo.svg
$AS/run.sh composite.py --bg card.png --text "STAY TRIPPEDD" \
    --size 120 --out final.png
$AS/run.sh vid.py vertical in.mp4 out.mp4
```

Full docs: font-wizard's TOOLS.md.
Pocket Studio (mobile web UI) also wraps inpaint / textcard / vidcut —
see `~/workspace/video-fix-tools/pocket-studio/`.
