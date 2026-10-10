# Puppet-rig lane: nijigenerate + Inochi Creator (Wave 3 Worker C)

Date: 2026-10-07. **Status: RUN-PROVEN on Linux x86_64** (was: docs-path).

## What this is
VTuber-style 2D puppet rigging for the mostly-2D cartoon series: layered
cutout characters, parameter-driven mesh deform, simple physics, face-track
driving. The Inochi2D ecosystem is the Live2D-class open answer.

## Verified binaries (both launched headless under Xvfb, screenshot-verified)

| App | Version | License | Status |
|---|---|---|---|
| **nijigenerate** | v1.0.0-beta2 (2026-06-04) | **BSD-2-Clause** ✅ (github.com/nijigenerate/nijigenerate, GitHub API `spdx_id`) | RUN-PROVEN — full editor UI (File/Edit/View/Tools/Help, Edit Puppet / Edit Animation tabs, Nodes/Parameters/Inspector/History panels, Quick Setup) |
| **Inochi Creator** | v0.8.6 (2024-09-18) | **BSD-2-Clause** ✅ (github.com/Inochi2D/inochi-creator, GitHub API `spdx_id`) | RUN-PROVEN — editor opens (shows donation nagscreen "buy a copy today"; the code is BSD-2, the nagscreen is just a donation prompt) |

## Headless recipe (this is how the proofs were made)
```bash
# 1. fetch prebuilt (no D toolchain needed)
curl -sL -o nijigenerate-linux.zip \
  https://github.com/nijigenerate/nijigenerate/releases/download/v1.0.0-beta2/nijigenerate-linux-x86_64.zip
unzip nijigenerate-linux.zip -d nijigenerate

# 2. virtual display + D-Bus session (BOTH required)
Xvfb :99 -screen 0 1280x800x24 &
ADDR=$(dbus-daemon --session --fork --print-address)
env DBUS_SESSION_BUS_ADDRESS="$ADDR" DISPLAY=:99 \
    XDG_RUNTIME_DIR=/tmp/xdg ./nijigenerate/nijigenerate
```
Gotchas found the hard way (2026-10-07):
- Without D-Bus: crash dialog "`ddbus.exception.DBusException: /usr/bin/dbus-launch
  terminated abnormally`" — crash report lands in `~/.local/state/`.
- Without a display: falls back to "tiny file dialogs" console mode.
- `XDG_RUNTIME_DIR` must be set or it complains on startup.

## Ecosystem map (all BSD-2-Clause ✅, already in RESOURCE_CATALOG.md)
- **nijigenerate/nijigenerate** — the active editor (use for ALL new rigging)
- **nijigenerate/nijilive** — the nijilive puppet format + runtime
- **nijigenerate/nijiui** — UI framework
- **Inochi2D/inox2d** — Rust runtime (WASM-capable puppet playback for web)
- **Inochi2D/inochi-session** — face-tracking → VMC puppet driving (live performance)
- **Inochi2D/inochi2d** — the D SDK (needs D toolchain: dub/ldc2 — not installed here)

## Pipeline slot
God-Molecule character lab: rig the wizard cast once as nijilive puppets,
drive via params/physics or face tracking, composite in the TRIPPEDD pipeline.
