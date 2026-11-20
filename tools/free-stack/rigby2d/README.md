> **Staged here:** adapted from the sweep doc on mhvnsnt/dream-girl, branch
> `tools/production-stack-free` (@91314564, `tools/production-stack-free/sweep/rigby2d/README.md`),
> staged 2026-11-20 (lane B, branch `tools/free-stack-wireup-20261120`).
> The binary lives on release `production-stack-free-20261120` on
> mhvnsnt/dream-girl — it is NOT stored in this repo. Fetch + verify with
> `tools/free-stack/fetch-verify.sh`. Pipeline slot for this repo: see
> `tools/free-stack/PIPELINE-STAGE.md`.

# Rigby2D — 2D Skeletal Animation (Spine / Moho Cover)

**Version:** 0.5.1 (release tag `v0.5.1`) · **Licence:** Apache-2.0 (free, open source)
**Upstream:** https://github.com/jaisurya-dev-art/rigby2d — docs: rigby2d.com/docs
**Status:** BINARY LANDED on release `production-stack-free-20261120` (verified 2026-11-20).

## Verdict

PULLED and verified. The strongest live Spine/Moho cover found in the
sweep: a real, actively developed open-source 2D skeletal animation
editor with a Linux AppImage — the role DragonBones' dead editor used
to hold.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `Rigby2D_0.5.1_amd64.AppImage` |
| Size | 96,979,448 B (matches published release asset size exactly) |
| SHA-256 | `27afa7de71a43e2fe45f27e605176a62b9a559db4b7f5f00f3a105870bdbd6ee` — verified against the project's published `SHA256SUMS.txt`: **OK** |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, no FUSE needed;
extracted 280M): `AppRun`, `AppRun.wrapped`, `Rigby2D.desktop`,
`usr/bin/rigby2d` (binary present under usr/).

Notes: repo last push 2026-11-19 (active; a release landed the day
before the sweep, and related repos were updated 2026-11-20). Also
published (not pulled): `.deb`, Godot/Unity/Phaser/Pixi runtimes,
`SHA256SUMS.txt`.

## What it is

Open-source 2D skeletal animation editor for games and film. AutoRig
layered PSDs, animate with meshes, IK and physics, lip-sync from audio,
render video, export JSON/.skel. JavaScript, Rust, Godot and Unity
runtimes. Built-in MCP server for AI assistants.

Stage it serves: 2D skeletal/bone rig + mesh animation with
game-engine runtimes — the Spine slot (replacing the dead DragonBones
editor) and the Moho slot (vector/mesh rig + IK + physics). Exports
JSON/.skel, so it can feed engines directly.

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'Rigby2D_0.5.1_amd64.AppImage'
chmod +x Rigby2D_0.5.1_amd64.AppImage
./Rigby2D_0.5.1_amd64.AppImage
# No FUSE: extract instead of mounting:
./Rigby2D_0.5.1_amd64.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the fetch script for all 10 tools at once:
# tools/free-stack/fetch-verify.sh
```

## Honest limits

- v0.5.1 is young and moving fast (0.x); API/format stability is not
  Spine-grade yet. No production history on our shots.
- No headless/CLI proof run done here; GUI-only probing so far. The
  built-in MCP server is a later-lane integration candidate, not tested
  here.
- Rigby2D is the skeletal/game-runtime complement, not a core
  replacement for this repo's rig/animation core (see
  `tools/free-stack/PIPELINE-STAGE.md`).

## Licence

Apache-2.0. Repo integration is legal — document the version pin on
upgrade. Source + licence logged honestly next to the item, per lane
rule; licence never gated the pull.
