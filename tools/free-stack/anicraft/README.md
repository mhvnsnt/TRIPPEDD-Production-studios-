> **Staged here:** adapted from the sweep doc on mhvnsnt/dream-girl, branch
> `tools/production-stack-free` (@91314564, `tools/production-stack-free/sweep/anicraft/README.md`),
> staged 2026-11-20 (lane B, branch `tools/free-stack-wireup-20261120`).
> The binary lives on release `production-stack-free-20261120` on
> mhvnsnt/dream-girl — it is NOT stored in this repo. Fetch + verify with
> `tools/free-stack/fetch-verify.sh`. Pipeline slot for this repo: see
> `tools/free-stack/PIPELINE-STAGE.md`.

# AniCraft — Clean-Room Adobe Animate Reimplementation (Rust)

**Version:** 0.2.1 (release tag `v0.2.1`) · **Licence:** Apache-2.0 (free, open source)
**Upstream:** https://github.com/storytold/anicraft
**Status:** BINARY LANDED on release `production-stack-free-20261120` (verified 2026-11-20).

## Verdict

PULLED and verified. The decomp/recomp find of the sweep: a clean-room,
open-source 2D animation editor written from scratch in pure Rust,
file-compatible with Adobe Animate (XFL/FLA, SWF) per the project
description. The closest thing in the sweep to a free reimplementation of
a paid animation tool — real, released, and runnable on Linux.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `anicraft-0.2.1-linux-x86_64.AppImage` |
| Size | 19,024,376 B (matches published release asset size exactly) |
| SHA-256 | `352456384d1e82f373d836dcbcd9f1473b1603c5c9c7b185d763218470091b31` — verified against the project's published `SHA256SUMS.txt`: **OK** |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, no FUSE needed;
extracted 44M): `AppRun`, `ai.storyteller.anicraft.desktop`,
`usr/bin/anicraft`, `usr/bin/anicraft-cli`.

Notes: repo last push 2026-11-20 (active — pushed the same day as the
sweep). A second repo of the same name, `soof-golan/anicraft`, describes
itself as "file-compatible with Adobe Animate (XFL/FLA, SWF)" but has NO
releases; the `storytold/anicraft` repo is the one shipping builds.

## What it is

2D vector/raster animation authoring — the Adobe Animate slot. Shape
tweens, Bone tool, camera layer. Candidate for Animate-format (XFL/FLA)
interchange. NOT a rig/animation core replacement — the core of this
repo's pipeline is unchanged (see `tools/free-stack/PIPELINE-STAGE.md`).

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'anicraft-0.2.1-linux-x86_64.AppImage'
chmod +x anicraft-0.2.1-linux-x86_64.AppImage
./anicraft-0.2.1-linux-x86_64.AppImage
# No FUSE: extract instead of mounting:
./anicraft-0.2.1-linux-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the fetch script for all 10 tools at once:
# tools/free-stack/fetch-verify.sh
```

The `anicraft-cli` binary inside the AppImage is the headless candidate
for a later lane (convert/render via CLI, if it supports it).

## Honest limits

- v0.2.1 is early (0.x). No production history on our shots yet.
- FLA compatibility is claimed by the sibling fork's description, not
  yet proven by us against a real .fla — a follow-up lane must test it.
- No Windows/macOS testing done here (Linux AppImage only).
- GUI app — no headless render run attempted here; extraction + file
  list is the probe.

## Licence

Apache-2.0. Repo integration is legal — document the version pin on
upgrade. Source + licence logged honestly next to the item, per lane
rule; licence never gated the pull.
