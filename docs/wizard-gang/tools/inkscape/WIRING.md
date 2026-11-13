# WIRING — Inkscape 1.4.4 (vector editor)
**Status: WIRED+PROVEN — 2026-11-13**
**Upstream:** https://inkscape.org/ — Inkscape 1.4.4, GPL-licensed vector graphics editor.
**Source of the binary:** `mhvnsnt/vendor-tools` release `vendor-tools-v1`,
asset `inkscape_1.4.4-ubuntu22.04_amd64.deb` (26,529,444 B, SHA256
`87b35e53f87ee6e6dadd7e023b9bafcb0f53703fc994bc8746cab8f799b36454` — verified
byte-exact on re-download 2026-11-13; the first download hit a transient
disk-quota flicker at 16 MB and was deleted + redownloaded clean).
**Install path:** `~/workspace/tools/inkscape/`
- `extracted/` — the .deb extracted with `dpkg-deb -x` (no system install; apt is
  broken on this VM). 201 MB. `extracted/usr/bin/inkscape`, `inkview`.
- `hostlibs/` — the dependency closure, 64 MB: Ubuntu 22.04 (jammy) .debs
  downloaded from `archive.ubuntu.com` and extracted with `dpkg-deb -x`.
  19 packages closed 21 missing SONAMEs (see below).
- `run-inkscape.sh` — wrapper: sets `LD_LIBRARY_PATH` to hostlibs + extracted
  libs, then execs inkscape. Use this, never the raw binary.
- `proof/test.svg` + `proof/test.png` — proof render.
- `~/workspace/_wizard-gang-wireup-20261113/phase4-outside-tools/work/close-inkscape-deps.sh`
  — the iterative closure resolver (ldd → map SONAME to jammy package → fetch
  from the jammy Packages index → extract → repeat until clean).

## Gap it fills
Vector drawing / SVG editing for the show: title cards, logos, signage, cutout
part cleanup, SVG interchange with Tahoma2D/Blender/Grease Pencil and with the
Foster's EPS/AI study material. Lane 1 (2026-10-29) downloaded + verified the
.deb but left the binary BLOCKED on 21 missing host libraries; this lane closes
that exact blocker. No vector editor in the stack could open/edit SVG before
this (Krita is raster paint; Tahoma2D is raster/vector animation, not an SVG editor).

## Dependency closure (the 21 libs, all jammy .debs)
libgtkmm-3.0-1v5, libgdkmm-3.0-1v5, libglibmm-2.4-1v5 (giomm+glibmm),
libatkmm-1.6-1v5, libpangomm-1.4-1v5, libcairomm-1.0-1v5, libsigc++-2.0-0v5,
libboost-filesystem1.74.0, libgsl27, libgslcblas0, libgc1, libpoppler118,
libpoppler-glib8, libpotrace0, libgspell-1-2, libenchant-2-2, libaspell15,
libgtksourceview-4-0, libmagick++-6.q16-8, libmagickcore-6.q16-6,
libmagickwand-6.q16-6, libtiff5, liblqr-1-0, libdouble-conversion3, libicu70.
Transitive second-wave libs the closure also pulled: libMagickCore/Wand,
libenchant, libgslcblas, libtiff5, liblqr, libaspell, libicu70 (ICU 70 —
the last two stragglers; jammy's libicu70, not the host's newer ICU).
All other direct deps resolve against the Ubuntu 24.04 host (libgtk-3,
libglib, libcairo, libpango, libfreetype, libfontconfig — SONAME-stable).
Final `ldd`: **0 not found**. Closure script re-runnable; the jammy
Packages index it reads lives in the phase4 work dir (`jammy-Packages.gz`).

## Proof (run 2026-11-13)
```
$ ./run-inkscape.sh --version
Inkscape 1.4.4 (1:1.4.4+202605061432+dcaf3e7d9e)
$ xvfb-run -a ./run-inkscape.sh proof/test.svg --export-type=png \
    --export-filename=proof/test.png --export-width=480
proof/test.png: PNG image data, 480 x 270, 8-bit/color RGBA, non-interlaced (14,396 B)
```
The test SVG (purple circle face + gold caption) renders correctly to PNG.
GUI launch was not headless-proven beyond the xvfb render; Inkscape is a GUI
app and the render path above is the production-relevant proof on this VM.

## Limits learned
- The .deb is a 22.04 build running on a 24.04 host — it works ONLY via the
  bundled jammy hostlibs; do not `apt install` it (apt is broken here) and do
  not point it at the host's newer boost/poppler (SONAMEs differ: boost 1.74
  vs 1.83, poppler 118 vs 126).
- Disk-quota flicker: large single writes intermittently fail with EDQUOT
  even with ~29 GB `df` free. If a re-download fails mid-write, delete the
  partial and retry; the failure is transient. NOTE 2026-11-13 ~19:35: even
  small file writes via the agent file tools started failing with EDQUOT
  while bash-builtin `echo > file` still works — use exec heredocs for writes
  while this flicker lasts (TOOLS.md 2026-11-11 note).
- The installer .deb itself was deleted from the work dir after extraction to
  save disk; re-fetch from the vendor-tools release if the extracted tree is
  ever lost (SHA256 above).
