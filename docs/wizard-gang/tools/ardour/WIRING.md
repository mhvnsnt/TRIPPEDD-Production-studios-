# WIRING — Ardour 8.4.0 (Ubuntu noble universe) — BLOCKED
**Status: NOT WIRED — blocked, 2026-11-13 (exact blockers below, no proof)**
**Upstream:** https://ardour.org/ (GPL) — the Pro Tools-class free multitrack
DAW. Ubuntu noble universe package `ardour 1:8.4.0+ds1-2ubuntu8`
(14,889,412 B) + `ardour-data` (4,815,808 B) + `ardour-lv2-plugins`
(63,920 B). ~45 direct Depends (libaubio5, libfluidsynth3, liblilv-0-0,
librubberband2, libvamp-hostsdk3v5, libwebsockets19t64, libcwiid1t64, ...).
**Local state:** `~/workspace/tools/ardour/hostlibs/` (73 MB, 282 files) —
CORRUPT, do not trust. Iterative closure script
`work/close-ardour-deps.sh` (noble main+universe index based, same pattern
as the Inkscape resolver) was written and run; killed 2026-11-13 22:46
before finishing.
**Gap it would fill:** the multitrack DAW — dialogue/music/SFX mix desk.
Audacity (already wired) is an editor, not a mix desk.

## Exact blockers
1. **The VM's child-process write-block episode corrupted the seed
   extraction.** The ardour .deb downloaded whole (14,889,412 B, exact
   index size) and extracted to 73 MB, but the key binaries are 0-byte
   files: `usr/bin/ardour`, `usr/lib/ardour8/ardour-8.4.0~ds1`,
   `ardour-avahi`, `ardour-exec-wrapper`, `ardour-request-device`,
   `ardour-vst-scanner`. Content writes from child processes fail during
   these episodes (`Operation not permitted` / ENOSPC at flush; file
   creation succeeds, content never lands — the same failure mode recorded
   in ~/TOOLS.md 2026-11-11). A re-download attempt failed the same way
   (curl (23) after 3,612 bytes). The closure cannot complete until a
   write-clean window returns.
2. **Closure is large.** Even in a clean window it needs the ~45-package
   iterative resolve (the script is ready: `work/close-ardour-deps.sh 8`).
   Expect 60–100 MB of .debs. LMMS (AppImage, ~130 MB) is the fallback
   if Ardour's closure proves too heavy — but LMMS is a pattern/beat DAW,
   not a multitrack mix desk, so it is a weaker substitute, not an equal one.
**What would unblock it:** a write-clean window (verify with
`git clone` succeeding or a python write landing non-zero bytes), then
re-run `work/close-ardour-deps.sh 8`, verify `ldd` on the ardour binary
shows 0 missing, and prove with `ardour --version` + a session render.
