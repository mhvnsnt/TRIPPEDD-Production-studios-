# WIRING — OpenToonz 1.4.0 (Morevna Edition)
**Status: WIRED+PROVEN — 2026-11-13**
**Upstream:** https://github.com/opentoonz/opentoonz (DWANGO; GPL) — Morevna Edition
builds at https://github.com/morevnaproject/opentoonz (Morevna Project).
**Release:** `v1.4.0-morevna`, asset
`OpenToonz-1.4.0-morevna-2020.06.14-linux64-b6177.appimage`
(115,474,432 B — size-verified exact against the release API. NOTE: the
release's `checksum-sha256.txt` only covers the 2020.02.29 build, not the
06.14 build, so there is no published SHA256 for this exact asset; the
size match + TLS download is the verification. Do not claim a hash match.)
**Install path:** `~/workspace/tools/opentoonz/`
- `OpenToonz-...appimage` — the downloaded AppImage (kept; re-extraction source).
- `extracted/` — the AppImage contents, 295 MB, 3,896 files (see extraction story).
- `hostlibs/` — host libraries the AppImage expects from the system (see below).
- `run-opentoonz.sh` — launcher (sets the library path, execs the bundled
  `launch-opentoonz.sh`). `env-opentoonz.sh` — source it for the CLI tools
  (`tconverter`, `tcleanup`, `tcomposer`).
- `extract-zisofs.py` — the extractor written for this lane (see below).
- `proof/test.tga` — tconverter proof output.
- `7z/` — p7zip 16.02 (jammy .deb, extracted) — used ONLY to list the ISO;
  it does NOT decompress zisofs (see extraction story).

## Gap it fills
OpenToonz PROPER — the Studio Ghibli-lineage 2D production app: node-based
compositing/effects (Toonz Schematic), multiplane camera, `tcleanup` line
cleanup, `tcomposer` headless scene rendering. Tahoma2D 1.6.3 (already wired)
is the friendlier drawing fork; OpenToonz proper is the comp/cleanup room and
the only tool that reads/writes native `.tnz` scenes interchangeably with
Tahoma2D. The Oct 29 wire-up left it WIRED-but-launch-UNPROVEN (Flatpak dies
on the document-portal step — no FUSE on this VM; unpacked Flatpak binaries
segfault outside their sandbox mounts). This lane proves the NON-Flatpak route.

## Extraction story (the hard part — no FUSE, no loop mounts, uid 0)
1. The Morevna AppImage is **Type 1** (ISO9660, `CD001` at offset 32769; no
   squashfs magic). `--appimage-extract` fails: the runtime needs
   `libfuse.so.2` just to load, then tries to mount (no `/dev/fuse`, no loop
   devices on this VM) and dies before any flag handling.
2. `libfuse2` (jammy .deb) was pulled so the runtime loads — still mount-bound.
3. p7zip 16.02 lists the ISO correctly but extracts zisofs files RAW
   (every file starts `37 e4 53 96...` — not ELF, not data).
4. `extract-zisofs.py` (written in this lane, Joliet tree walk + zisofs
   decode, ~150 lines) cracks the stored format, verified on real files:
   - Stored file layout: 16-byte header (constant magic-ish
     `37 e4 53 96 c9 db d6 07`, uncompressed size at bytes 8–11 LE,
     constant `0x1104` at bytes 12–15), then a pointer table at byte 16 of
     (nblocks+1) LE u32 offsets (first = 16+4*(nblocks+1), last = stored size),
     then zlib streams of **131072-byte** blocks (last may be shorter).
   - Proof: `canbusutil` zlib@24 → 37,128-byte ELF; `OpenToonz` block 0 →
     131,072-byte ELF. Full tree: **3,896 files, 2,105 zisofs-decoded,
     1,791 plain, 0 failures**. Every binary is a valid ELF after decode.
5. Symlinks do not survive a Joliet walk (Rock Ridge SL entries are invisible
   there): 227 SONAME symlinks (`libQt5Xml.so.5 -> libQt5Xml.so.5.9.2`, etc.)
   were recreated by the `--fix-symlinks` pass in the same script. Without
   them the loader fails on the first Qt lib.
6. Host-lib closure (jammy .debs unless noted; `fetch-deb.sh` in the phase4
   work dir verifies each .deb actually contains the SONAME before extracting):
   libfuse2, libglew2.0 (**bionic** — jammy only has 2.2; the AppImage wants
   the 2.0 SONAME), libglu1-mesa, libopenblas0-pthread (the bare libopenblas0
   .deb is docs-only — the lib lives in the -pthread split, under
   `openblas-pthread/`), libopengl0, libglx0, libglx-mesa0, libglapi-mesa,
   libxtst6. `libpulsecommon-11.1.so` comes from the AppImage's own
   `usr/lib/pulseaudio/` (the launcher adds it to the path). Final `ldd` on
   OpenToonz/tcomposer/tconverter/tcleanup: **0 not found**.

## Proof (run 2026-11-13)
```
$ ./run-opentoonz.sh -version
OpenToonz  v1.4.0 (Morevna Edition)
$ ./run-opentoonz.sh -h        # prints full usage (layout/TOONZROOT flags)
$ xvfb-run -a tconverter inkscape-proof/test.png proof/test.tga
Conversion terminated!        # its normal completion message
proof/test.tga: 22,697 B, PIL-verified 480x270 RGB — real Toonz codec round-trip
$ tcleanup -h / tcomposer -h   # both print their full usage under xvfb
```

## Limits learned (honest)
- **1.4.0 is from 2020 — six years behind upstream 1.8.0 (June 2026).**
  It is the NEWEST Morevna AppImage that exists (their latest release is
  v1.4.0-morevna; the Snap `opentoonz-morevna` stable channel is also 1.4.0
  and snapd is not installed here). Upstream ships NO Linux binary; the only
  1.8.0 Linux route is the Flathub Flatpak, which is BLOCKED on this VM by
  the missing FUSE (proven Oct 29, re-confirmed: no /dev/fuse, no loop
  devices). Debian trixie main has NO opentoonz package (checked
  2026-11-13), and Ubuntu 24.04 noble universe has none either — so there is
  no .deb route to a newer build. Tahoma2D 1.6.3 stays the newer Toonz-family
  tool; OpenToonz 1.4.0 is wired for Schematic/multiplane/tcleanup/tcomposer
  compatibility, NOT as the drawing front-end.
- `tcomposer` scene rendering was NOT proven with a real `.tnz` (no sample
  scene ships in the AppImage; building a scene by hand is a separate job).
  The binary executes and prints usage; the render path is the same binary
  Tahoma2D's `tcomposer` uses (proven headless in lane 1). Do not claim a
  scene render until one is run.
- The GUI launches under xvfb (usage/version proven); no interactive GUI
  session was driven. The `update stuff` first-run copy to
  `~/.config/OpenToonz` happens automatically via the bundled launcher.
- Disk cost: AppImage 115 MB + extracted tree 295 MB + hostlibs ~35 MB.
  The 7z-extracted garbage tree (114 MB of raw zisofs bytes) was deleted.
- Download fragility: the AppImage download failed twice with transient
  disk-quota flicker (EDQUOT at ~112/115 MB) before completing on retry;
  `gh release download` does not resume — delete the partial and retry.
