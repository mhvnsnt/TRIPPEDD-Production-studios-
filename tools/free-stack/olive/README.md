> **Staged here:** adapted from the sweep doc on mhvnsnt/dream-girl, branch
> `tools/production-stack-free` (@91314564, `tools/production-stack-free/sweep/olive/README.md`),
> staged 2026-11-20 (lane B, branch `tools/free-stack-wireup-20261120`).
> The binary lives on release `production-stack-free-20261120` on
> mhvnsnt/dream-girl — it is NOT stored in this repo. Fetch + verify with
> `tools/free-stack/fetch-verify.sh`. Pipeline slot for this repo: see
> `tools/free-stack/PIPELINE-STAGE.md`.

# Olive Video Editor — Secondary / Alpha NLE

**Version:** 0.2.0-nightly (build `8ac191ce`, rebuild of master from
2024-12-04; last code change 2023-09-24) · **Licence:** GPL-3.0 (free, open source)
**Upstream:** https://github.com/olive-editor/olive
**Status:** BINARY LANDED on release `production-stack-free-20261120` (verified 2026-11-20).

## Verdict

PULLED and verified — as the SECONDARY / ALPHA editor, not the primary.
Kdenlive (see `../kdenlive/`) is the primary free editor: stable,
maintained, current. Olive is the node-based promise that stalled.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `Olive-8ac191ce-Linux-x86_64.AppImage` |
| Size | 154,107,880 B (matches published release asset size exactly) |
| SHA-256 | `30a6c0d18dfb4ff77addd06984348656fd69d153cfa913eb3cde56a60aa14160` (computed locally 2026-11-20; no published sums to check against) |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, no FUSE needed;
extracted 353M): `AppRun`, `org.olivevideoeditor.Olive.desktop`,
`usr/bin/olive-editor`, plus `crashpad_handler` and
`olive-crashhandler` (it ships its own crash handler — consistent
with the alpha/unstable status).

Notes: repo last push 2024-12-05. The project is PAUSED, not dead: the
official site now serves an "Olive will return" placeholder; the
0.1.0 alpha and this 0.2.0-nightly are the only GitHub binaries. The
project publishes no SHA256SUMS file for this release, so verification
is size-exact + GitHub release provenance, not a hash-against-published-
sums check (unlike AniCraft/Rigby2D).

## What it is

Free, node-based, non-linear editor; billed by the project as a
fully-featured alternative to high-end professional editors. The README
itself calls Olive alpha software and highly unstable.

Stage it serves: video editing — node-based timeline/compositing
experiments, and a fallback if Kdenlive ever blocks. NOT the primary
editor.

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'Olive-8ac191ce-Linux-x86_64.AppImage'
chmod +x Olive-8ac191ce-Linux-x86_64.AppImage
./Olive-8ac191ce-Linux-x86_64.AppImage
# No FUSE: extract instead of mounting:
./Olive-8ac191ce-Linux-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the fetch script for all 10 tools at once:
# tools/free-stack/fetch-verify.sh
```

GPU route (owner law 2026-11-20): GPU-accelerated preview/effects route
via Kaggle GPU / Colab / Lightning AI / Oracle (coordinator owns the
routing); CPU fallback works. No local-GPU dead end — the tool runs,
just slower without one.

## Honest limits

- Alpha, unstable by its own README; community reports freezes
  several times per hour on the stock AppImage. No releases since
  Dec 2024; no code changes since Sep 2023.
- Do NOT cut anything deadline-critical in Olive. Kdenlive is the
  editor for real work.
- GUI app — no headless render run attempted here; extraction + file
  list is the probe. The AppImage needs FUSE 2 to run normally (per
  community install guides); extraction works without it.

## Licence

GPL-3.0. Repo integration is legal — document the version pin on
upgrade. Source + licence logged honestly next to the item, per lane
rule; licence never gated the pull.
