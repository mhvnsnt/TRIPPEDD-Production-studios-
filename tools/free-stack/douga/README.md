> **Staged here:** adapted from the sweep doc on mhvnsnt/dream-girl, branch
> `tools/production-stack-free` (@91314564, `tools/production-stack-free/sweep/douga/README.md`),
> staged 2026-11-20 (lane B, branch `tools/free-stack-wireup-20261120`).
> The binary lives on release `production-stack-free-20261120` on
> mhvnsnt/dream-girl — it is NOT stored in this repo. Fetch + verify with
> `tools/free-stack/fetch-verify.sh`. Pipeline slot for this repo: see
> `tools/free-stack/PIPELINE-STAGE.md`.

# Douga — Pen-First Cel Animation with a Real Dope Sheet

**Version:** build 1116, updated 2026-11-17 13:18 UTC · **Licence:** free (see watermark note below)
**Upstream:** https://douga.app — download page: https://keihoag.itch.io/douga (author: keihoag)
**Status:** BINARY LANDED on release `production-stack-free-20261120` (browser pull, verified 2026-11-20).

## Verdict

VERIFIED REAL and landed. Pen-first cel animation with a real dope
sheet — the TVPaint-adjacent slot for hand-drawn timing work.
Complements Pencil2D (Linux, pulled) and Tahoma2D (in stack).

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `browser-download-20261120T160026.367892390Z-0-douga-windows.zip` (Windows build zip) |
| Size | 3,766,009 B |
| SHA-256 | `bf3bd41c5593736caf4b7d74ebcf4c00c52766691c3596f3d3c7b34a9ea0b774` |
| Format | Windows zip |

Contents verified: `Douga/douga.exe` 6,263,648 B, `EULA.txt`,
`lang/en.ini` + `ja.ini`, plugins (effects blur/levels/mosaic/noise/
sample_invert/smooth, ffmpeg exporter).

Related plugins NOT pulled: douga-rig-import.zip 190 kB, brush_convert
279 kB, video_import 83 kB, update_check 85 kB, poses 13 MB.

## What it is

- Price: **free · no installer · no account**
- Tagline: "Pen-first cel animation with a real dope sheet."
- Platform: **Windows 10 / 11, 64-bit ONLY** — `douga.exe`, Direct3D 11;
  Wacom / XP-Pen / Huion / Surface Pen. No Linux build, no macOS build.
  (The zip downloads and verifies on any machine; it runs on Windows.)
- Features: pressure-sensitive brush engine (ink, pencil, splatter,
  marker, airbrush; custom `.dbrush` files), stabilizer, perspective/
  grid/symmetry guides, drop a GLB/GLTF/OBJ to trace over, real dope
  sheet (keys, holds, loops, exposure on ones/twos, warm/cool onion
  skin), scenes > cuts > layers, managed palettes (`.dpal`), one `.dga`
  file per project.
- Export: PNG sequence, GIF, APNG, H.264 MP4 with sound, built in.
- Status: beta, one person's program. "It draws, it times, it saves, it
  exports." Vector layers + more of the shooting stage (glow, focus,
  motion blur) are next, not shipped.

## Watermark — read this

**Exports from an unlicensed copy carry a small "made with douga.app"
line in the bottom-right corner**; a licence key from douga.app/buy
removes it. The tool itself is free; the watermark-free export is paid.
Log it honestly, do not present Douga as watermark-free.

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'browser-download-20261120T160026.367892390Z-0-douga-windows.zip'
# Unzip on Windows 10/11 64-bit and run Douga/douga.exe (no installer).
# Or use the fetch script for all 10 tools at once:
# tools/free-stack/fetch-verify.sh
```

Note: the itch.io download files sit behind itch download buttons —
`curl` to itch.io from the source lane's VM returned 0-byte bodies, so
the zip was pulled via the live browser. No direct file URL is exposed
in the page text.

## Honest limits

- Windows-only. Beta, single author. Watermark on free exports (above).
- No Linux/macOS build, so no run/probe on a Linux box — staged for
  Windows use.

## Licence

Free to use; watermark-free export is a paid licence key (see above).
Source + licence logged honestly next to the item, per lane rule;
licence never gated the pull.
