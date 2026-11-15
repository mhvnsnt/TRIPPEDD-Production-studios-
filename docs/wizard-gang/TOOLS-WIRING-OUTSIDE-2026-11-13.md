# Wizard Gang — Outside Tools Wire-Up (Phase 4, 2026-11-13)

Free production-grade tools the owner's stack genuinely lacked, wired and
proven on this VM. Grease Pencil (Blender) stays the rig/animation core;
these join for cleanup / hand-drawn 2D / compositing / lipsync / sound.
Pipeline V1 (EP01 v10) is untouched — this is V2 material only.

**Installs live in `~/workspace/tools/<tool>/`** with a per-tool `WIRING.md`
(upstream, version, install path, proof command + output, limits learned).
Big binaries stay out of git — the WIRING.md files are the repo record.

## Proven and wired

| Tool | Version | Gap filled | Proof |
|---|---|---|---|
| Inkscape | 1.4.4 | Vector art / boards cleanup / SVG→PNG | `run-inkscape.sh --version`; SVG→PNG render `proof/test.png` (480x270, PIL-verified) |
| OpenToonz | 1.4.0 (Morevna) | Cleanup / hand-drawn 2D / compositing (Schematic, tcleanup, tcomposer) | `run-opentoonz.sh -version`; tconverter PNG→TGA `proof/test.tga` (PIL-verified) |
| OpenFaceFX | 0.24.0 | Lipsync: smooth 15-viseme curves + coarticulation from Rhubarb cues | `naive` on voice.wav: 7 channels, 93 keyframes, 1.60 s (matches upstream README); `from-cues` from Rhubarb JSON: 3 channels, 18 keyframes |
| GIMP | 2.10.25 | Raster cleanup / photo-manip / BG plates | `AppRun --version` → 2.10.25; Script-Fu batch invert+export proof (see WIRING.md) |
| Storypencil | 1.1.4 | Storyboards inside Blender (VSE scene strips) | Addon enables, 11 operators register, setup() creates Base+Edit scenes (verified on re-open of `proof/storypencil-test.blend`); strip creation needs a GUI session — see limits |
| Ardour | 8.4.0 | Multitrack DAW — dialogue/music/SFX mix desk | BLOCKED (see gaps log; seed extraction corrupted by write-block episode) |

## Blocked — exact blockers, nothing hand-waved

- **sketch-simplification** (line cleanup): torch 2.2.2 will not install —
  pip `OSError(28) No space left` at 152.0/186.7 MB of the wheel while `df`
  shows 29 GB free (quota wall trips on ~150 MB+ single writes). The
  original also needs PyTorch 0.4.1 `load_lua` (removed in modern torch);
  the esslab.jp model serves at ~20 KB/s (~5 h for 350 MB). Successor
  virtual_sketching needs torch too. See its WIRING.md.
- **Papagayo-NG** (lipsync GUI over Rhubarb): needs PySide2 (Qt5, EOL);
  PySide2 5.15.2.1 has no Python 3.12 wheel. Rhubarb CLI stays the lipsync
  engine; OpenFaceFX bridges its cues into smooth viseme curves.
- **Montreal Forced Aligner 3.4.3** (word-level alignment): pip install
  failed `OSError(28)` at 5.0/59.7 MB (same quota wall). OpenFaceFX `mfa`
  mode and Rhubarb cues are the working alternatives.
- **OpenToonz 1.8.0** (current upstream): no Linux binary; Flatpak blocked
  (no FUSE/loop on this VM); no .deb in Debian trixie or Ubuntu noble.
  Wired 1.4.0 Morevna instead; Tahoma2D 1.6.3 stays the newer Toonz-family
  front-end.

## Not added (evaluated, honestly no gap)

- **Compositing extra:** Natron is already wired; no other free compositor
  adds a real gap (Olive is an NLE, Cavalry has no Linux build, DaVinci
  Resolve free needs GPU + ~4 GB).
- **Storyboard extra:** Boords is SaaS free-tier only (web, not
  installable). Storyboarder is already wired; Storypencil is the
  in-Blender path added here.

## Per-tool records

- `~/workspace/tools/inkscape/WIRING.md`
- `~/workspace/tools/opentoonz/WIRING.md`
- `~/workspace/tools/openfacefx/WIRING.md`
- `~/workspace/tools/gimp/WIRING.md`
- `~/workspace/tools/storypencil/WIRING.md`
- `~/workspace/tools/ardour/WIRING.md` (blocked — full detail)
- `~/workspace/tools/sketch-simplification/WIRING.md` (blocked — full detail)

## Environment notes (2026-11-13)

- Ubuntu 24.04.5, Python 3.12.3, 4 CPUs, 7.7 GB RAM. Disk 150 GB, ~121 GB
  used — a quota wall trips large single writes (ENOSPC/EDQUOT) despite
  ~29 GB `df`-free. `/tmp` is a 512 MB tmpfs, ~95% full — never extract
  AppImages there. No torch, no docker/podman/snap/flatpak, no system Qt5,
  no `/dev/fuse`, no `/dev/loop*`. `apt` is broken; `.deb` installs are
  direct downloads from archive.ubuntu.com + `dpkg-deb -x`.

## Ardour — blocked (2026-11-13, exact)
- The ardour .deb downloaded whole (14,889,412 B) and extracted to 73 MB,
  but the key binaries are 0-byte files (`usr/bin/ardour`,
  `usr/lib/ardour8/ardour-8.4.0~ds1`, `ardour-avahi`, `ardour-exec-wrapper`,
  `ardour-request-device`, `ardour-vst-scanner`). Cause: the VM's
  child-process write-block episode — file creation succeeds, content
  writes fail (`Operation not permitted` / ENOSPC at flush). A re-download
  failed the same way (curl (23) after 3,612 bytes). The iterative closure
  script (`work/close-ardour-deps.sh`) is ready; re-run it in a write-clean
  window, verify `ldd` shows 0 missing, prove with `ardour --version`.
