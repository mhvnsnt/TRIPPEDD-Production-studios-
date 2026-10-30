# Install note — Natron card + LOOK kit

## This box (verified 2026-10-30)

- Natron **2.5.0** is wired at
  `~/workspace/tools/natron/Natron-2.5.0-Linux-x86_64-no-installer/`
  with the headless wrapper `~/workspace/tools/natron/natron-render.sh`
  (sets `LD_LIBRARY_PATH` for the local libGLU/libOpenGL copies).
- Install the gizmos into that Natron:

```bash
tools/natron-card-look-kit/gizmos/install_gizmos.sh
# = copies gizmos/*.py into
#   ~/workspace/tools/natron/Natron-2.5.0-Linux-x86_64-no-installer/Plugins/PyPlugs/
```

- Natron loads PyPlugs at startup ("Loading PyPlugs..." in the
  NatronRenderer log). After installing, the groups appear as:
  - Color → TRIPPEDD → **CJ LOOK 1 Pale Wash**, **CJ LOOK 2 Deep Saturation**,
    **CJ LED Deep Purple Glow**, **CJ LED Party Glow**
  - Transform → TRIPPEDD → **TRIPPEDD Card 2.5D**
- The same script also installs the N-1 community donor
  (PM_Card3D + PM_Camera from `card-kit/community-donor/`) into
  `Plugins/PyPlugs/PM_Card3D/` and `Plugins/PyPlugs/PM_Camera/`
  subfolders — each PM plugin imports its `*Ext.py` companion from
  its own folder, so the subfolder layout matters.
- Status on this box: installed + headless-verified, see
  `test/TEST-LOG.md`.

## Any other Natron 2.5.0

```bash
gizmos/install_gizmos.sh /path/to/Natron/Plugins/PyPlugs
```

PyPlugs are plain Python (NatronEngine API only, no other deps).
Natron also supports `.ntp` project files as shared presets; this pack
ships PyPlug groups instead because they are the group/gizmo format
Natron itself exports, they carry documented knobs, and they are
diff-able text in git.

## Headless use

```bash
~/workspace/tools/natron/natron-render.sh your_script.py   # Natron python
~/workspace/tools/natron/natron-render.sh project.ntp 1,50 # render frames
```

Note: NatronRenderer exits non-zero with "Project file is missing a
writer node" when a bare python script leaves no Write node in the
project — check for your script's own output files, not just the exit
code. The kit's test script creates Write nodes, so it exits cleanly.
