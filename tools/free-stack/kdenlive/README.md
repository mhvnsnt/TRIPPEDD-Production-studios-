> **Staged here:** adapted from the sweep doc on mhvnsnt/dream-girl, branch
> `tools/production-stack-free` (@91314564, `tools/production-stack-free/sweep/kdenlive/README.md`),
> staged 2026-11-20 (lane B, branch `tools/free-stack-wireup-20261120`).
> The binary lives on release `production-stack-free-20261120` on
> mhvnsnt/dream-girl — it is NOT stored in this repo. Fetch + verify with
> `tools/free-stack/fetch-verify.sh`. Pipeline slot for this repo: see
> `tools/free-stack/PIPELINE-STAGE.md`.

# Kdenlive — Primary Free Video Editor

**Version:** 26.08.3 (released 2026-11-07; maintenance release of the
26.08 series, includes an important security fix for manipulated
`.kdenlive` project files — upgrade advised by the project)
· **Licence:** GPL-3.0 (KDE project; free, open source)
**Upstream:** https://kdenlive.org/ — downloads at
https://download.kde.org/stable/kdenlive/26.08/linux/
**Status:** BINARY LANDED on release `production-stack-free-20261120` (verified 2026-11-20).

## Verdict

PULLED and verified. The PRIMARY free video editor for the stack:
stable, actively maintained, current release. Olive (see `../olive/`)
is the secondary/alpha editor only.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `kdenlive-26.08.3-x86_64.AppImage` |
| Size | 214,346,232 B (confirmed by Content-Length from the KDE mirror and by the completed download) |
| SHA-256 | `2c8322edfc86605e4c98a78a019310d9b4fc46bb8e94e6fe313dc7dd987e7671` (published by KDE alongside the AppImage; verified locally with `sha256sum -c`) |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, no FUSE needed):
`AppRun`, `org.kde.kdenlive.desktop`, `usr/bin/kdenlive`,
`usr/bin/kdenlive_render`, plus bundled `ffmpeg`/`ffplay`/`ffprobe`.

Notes: platforms: Linux (AppImage / Flatpak — the only two Linux
formats the Kdenlive team supports), Windows, macOS, BSD.

## What it is

Multi-track non-linear editing, nested sequences, multicam, 3-point
editing, markers, automatic backups, proxy editing, motion tracking,
colour correction, video scopes (histogram, vectorscope, RGB parade,
waveform), subtitling, speech-to-subtitles.

Stage it serves: video editing — the primary editor: cutting episodes,
assembling renders, subtitles, colour. This is the editing slot's real
answer. Glaxnimate integrates with Kdenlive for titles and motion
graphics (see `tools/harmony/glaxnimate/README.md`).

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'kdenlive-26.08.3-x86_64.AppImage'
chmod +x kdenlive-26.08.3-x86_64.AppImage
./kdenlive-26.08.3-x86_64.AppImage
# No FUSE: extract instead of mounting:
./kdenlive-26.08.3-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the fetch script for all 10 tools at once:
# tools/free-stack/fetch-verify.sh
```

GPU route (owner law 2026-11-20): GPU-accelerated effects, preview and
render route via Kaggle GPU / Colab / Lightning AI / Oracle (coordinator
owns the routing); CPU + proxy editing works without one. No
local-GPU dead end.

## Honest limits

- Needs proxies for smooth playback of heavy footage on low-end
  systems (the project's own guidance).
- The 26.08.3 AppImage is ~200 MB; Flatpak is the project's other
  supported Linux route — AppImage is the working route here.
- GUI app — no headless render run attempted here; extraction + file
  list is the probe.

## Licence

GPL-3.0. Repo integration is legal — document the version pin on
upgrade. Source + licence logged honestly next to the item, per lane
rule; licence never gated the pull.
