# WIRING — GIMP 2.10.25 (aferrero2707 AppImage)
**Status: WIRED + VERSION-PROVEN — 2026-11-13 (batch render blocked, see limits)**
**Upstream:** https://github.com/aferrero2707/gimp-appimage (continuous release)
— GIMP 2.10.25 git build 2021-06-10, `GIMP_AppImage-git-2.10.25-20210610-x86_64.AppImage`
(148,055,232 B, SHA256 `9f43ed00220dd75b474fd2b5533d870b9322300d2ea6d58173950ec3a9e06db9`).
**Install:** `~/workspace/tools/gimp/` — AppImage kept, `extracted/` (458 MB,
8,925 files, via p7zip 16.02 squashfs extract — no FUSE/loop on this VM),
`run-gimp.sh` wrapper, `proof-test-out.png` (0 B — batch never completed).
**Gap it fills:** raster cleanup / photo-manip / background plates. Krita
(already wired) is the paint tool; GIMP is the cleanup half — levels, masks,
healing, plate prep, texture cleanup — the Photoshop-class raster editor a
2D pipeline needs next to a paint app.

## Proof (run 2026-11-13)
```
$ ./extracted/AppRun --version
GNU Image Manipulation Program version 2.10.25
```
Extraction notes (reproducible): 7z 16.02 extracts squashfs but writes
symlinks as tiny text files (e.g. `usr/bin/gimp` = 9-byte file containing
`gimp-2.10`) and drops exec bits. Fixed with a symlink-restore pass (166
symlinks restored: single-token files whose content resolves to an existing
tree path) + `chmod -R +x` on `usr/lib/gimp/2.0/plug-ins/` and
`usr/lib/gimp/2.0/interpreters/`. After the fix the plug-in scanner DOES
find script-fu and file-png ("bundled process found" in the log).

## Limits learned (honest)
- **Batch render NOT proven.** Three Script-Fu batch runs (invert + export
  a 320x180 PNG) never completed: the first two died on the missing
  script-fu registration (exec-bit cause, fixed); the third ran >20 min
  stuck in plug-in query/font init with the output file left at 0 B and
  was killed. GIMP startup on this VM is extremely slow (plug-in scan +
  fonts, >100 s to first batch even in the version run) and the batch path
  never got past init in three attempts. GUI use (open, edit, export by
  hand) is the unproven-but-plausible path; headless batch is BLOCKED on
  this VM until the startup hang is diagnosed on a quieter machine.
- This is GIMP **2.10.25 (2021)**, not GIMP 3.x: the aferrero2707 repo's
  latest assets are 2.10.x/2.99 dev builds (2020–2021); no 3.x AppImage
  exists there. 2.10 is the proven raster editor; 3.x would need a Flatpak
  (blocked: no FUSE) or a source build.
- The update-check call to gimp.org fails ("Operation not supported") —
  harmless, offline VM.
- AppRun's `gimp-2.10.wrapper` extracted as a 0-byte file; harmless
  (AppRun launches `gimp-2.10` directly).
