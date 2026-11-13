# Wizard Gang — Cascadeur Posing (vendor-tools wiring)

**Date:** 2026-11-13 · **Lane:** Phase 3B (f) · **Status:** verified + launch-tested (see §4)
**Sources:** `mhvnsnt/vendor-tools` — `README.md` + `cascadeur/README.md`
(retrieved 2026-10-18); release asset `vendor-tools-v1` / `cascadeur-linux.tgz`.
**WG home:** `mhvnsnt/TRIPPEDD-Production-studios-`, `docs/wizard-gang/`.
**Frozen:** Pipeline V1 / EP01 v10 — untouched.

## 1. What Cascadeur is

Cascadeur 2026.2.3 (Linux) — physics-based, AI-assisted keyframe animation
software. The store keeps the Linux build (Windows 493.52 MB and Mac 497.15 MB
builds ship on the same download page). License: **Cascadeur Basic — the FREE
tier** (the download API returns `{"type":"free","planType":"basic"}`).
The CASCADEUR END-USER LICENCE AGREEMENT (version 2025.1, presented before
download) applies — see `licenses/licence.txt` inside the tarball before use.

- **Version:** 2026.2.3 (released 01 Oct 2026; listed on cascadeur.com/download)
- **Binary:** `cascadeur-linux.tgz` — 581,257,231 bytes (~554.33 MB)
- **Source page:** https://cascadeur.com/download
- **Direct download (no account needed):** the download page has no direct href —
  the free build is retrievable via the site's own REST endpoint:
  `GET https://cascadeur.com/rest/download/build?platform=linux&buildId=112`
  (build 112 = 2026.2.3), redirecting to
  `https://cdn.cascadeur.com/storage/builds/2026.2.3/linux/cascadeur-linux.tgz`.
  Only the OLDER-version buttons on that page redirect to `/sign-in`.
- **Contents:** self-contained `cascadeur-linux/` tree (~1.3 GB extracted,
  bundled Qt6 libs under `lib/`); launcher is `cascadeur-linux/cascadeur`.
- **Install:** extract anywhere and run `./cascadeur`.

## 2. Verification (this lane, 2026-11-13)

- **SHA-256 — EXACT MATCH, verified by streaming the 581 MB release asset
  through `sha256sum` (zero bytes stored on disk):**
  `c3409b9915bf654d74f119b25822147bc81e4d0748b6878c897c23abf608b102`
  — identical to the hash in `vendor-tools/cascadeur/README.md` and the survey
  inventory. The binary is authentic.
- **Contents listed (streamed `tar -tzvf`): 4,118 members, 1,231 MB extracted:**
  `lib/` 608 MB (incl. `libtorch_cpu.so` 386 MB — the AI backend),
  `csc-lib/` 284 MB (incl. `libtool_inbetweening.so` 170 MB,
  `libtool_auto_posing.so` 36 MB), `python/` 197 MB (embedded Python 3.11),
  `samples/` 89 MB, `resources/` 29 MB, `qml/` 14 MB, launcher `cascadeur`
  7.4 MB. The launcher is a Qt6 app; `ldd` shows its direct deps resolve
  against the bundled `lib/` + `csc-lib/` — including `libtool_inbetweening.so`,
  `libtool_auto_posing.so`, `libtool_retargeting.so`, `libtool_rigging_mode.so`,
  and `libpython3.11.so.1.0`.

## 3. Install on this VM (what actually happened)

A straight `gh release download` of the 581 MB tarball **failed on the disk
quota wall** at 115/581 MB (`disk quota exceeded`; the partial was deleted).
Home-disk headroom at the time measured ~84 MB by a 300 MB `dd` test
(df still showed 29 GB free — the quota, not the filesystem, is the wall).
The install therefore went the streaming route, which stores nothing:

1. Stream-listed the tarball (`curl | tar -tzvf`) and stream-verified its SHA-256.
2. Stream-extracted everything **except** `libtorch_cpu.so` (386 MB),
   `samples/` (89 MB), and `python/modules/` (122 MB) into `/dev/shm`
   (794 MB tmpfs, the only volume with headroom): 638 MB, rc=0.
3. `libtorch_cpu.so` is a **hard link-time dependency** (`DT_NEEDED`) — the
   launcher refuses to start without it (`error while loading shared libraries:
   libtorch_cpu.so`). It is not dlopen-on-demand. A second streaming pass
   extracted just that file to home disk once headroom recovered past 400 MB,
   symlinked into `cascadeur-linux/lib/`.
4. `/dev/shm` is RAM-backed and ephemeral — this install vanishes on reboot.
   It is a **proof install, not a permanent install**. A permanent install
   needs a machine (or a quota window) with ~1.3 GB free; the commands in §2–3
   are the repeatable path.

## 4. Launch + pose proof — what was actually proven (2026-11-13)

**PROVEN — CLI launch:** `./cascadeur --help` runs under
`QT_QPA_PLATFORM=offscreen`, rc=0: `Program version: 2026.2.3
6f839ab373704c701854a9b4ab3bb788d6f47112`, Ubuntu 24.04, 7,935 MB RAM.
CLI surface confirmed: `-h/--help`, `--help-all`, `-c/--run-python-code <code>`,
`-s/--run-script <command>`, and a `scene` file argument. Full output:
`docs/wizard-gang/proof/cascadeur-help.txt`. The dependency closure was
completed first: `ldd` went from 14 missing libs to **0 not found** once
`libtorch_cpu.so` was supplied (symlinked from the finisher's `min/` extract —
see note below) and 13 system XCB libs were supplied via `LD_LIBRARY_PATH`
from other apps' bundles on this VM (Tahoma2D's squashfs-root and OpenToonz's
extracted/hostlibs: `libxcb-util/-keysyms/-image/-icccm/-xkb/-render-util/
-xinerama`, `libxcb-ewmh/-cursor/-composite/-dri2/-res`, `libXtst.so.6`).

**NOT PROVEN — GUI viewport and pose.** Three GUI attempts, all with
`Cascy.casc` (the bundled rigged mascot scene, copied read-only to `/dev/shm`
— the bundled `samples/` were in the parallel finisher's extract, not this
lane's) under `xvfb-run`, all aborted at the same place:

- Attempt 1 (xcb, own Xvfb display): `QGLXContext: Failed to create dummy
  context` → `Failed to create OpenGL context in the probe` → `Failed to
  create RHI (backend 2)` → `Failed to initialize graphics backend for OpenGL.`
- Attempt 2 (`+extension GLX`, `LIBGL_ALWAYS_SOFTWARE=1`): identical failure.
- Attempt 3 (`QT_XCB_GL_INTEGRATION=xcb_egl`, `LIBGL_ALWAYS_SOFTWARE=1`):
  identical failure.

**Exact blocker:** this VM has **no `/dev/dri`** (no GPU/render node) and its
Xvfb provides no working GL drawable for Qt's OpenGL probe — GLX and EGL
both fail at "failed to create drawable". Mesa llvmpipe (`swrast_dri.so`) is
present, but Qt's probe cannot create a context against this X server.
`--help` works because it exits before the viewport is created; the GUI
cannot get past viewport initialization here. Two scripted `-c` attempts
(offscreen, 120 s and 180 s) both timed out (rc=124) during scene init
("default constants initialization") — the probe code never ran, so no
scripted pose could be executed either.

**What unblocks it:** a machine (or display) with working OpenGL — a real GPU,
a render node under `/dev/dri`, or an X server whose GLX actually yields a
drawable (e.g. Xvfb with working Mesa GLX, or XWayland). The install recipe
in §3 plus the `LD_LIBRARY_PATH` above is the repeatable path there. The pose
to prove first on that machine: open `samples/Cascy.casc`, pose one joint,
screenshot the viewport.

**Parallel-work note (read before re-doing this):** a second agent — the "WG
Cascadeur finisher" named in the disk-cleanup log — is working the same
Cascadeur item in this same workdir (`cascadeur/min/`, its own extraction from
`downloads/cascadeur-linux.tgz`). This lane's `libtorch_cpu.so` (405 MB) was
extracted complete (404,856,960 B) and then **deleted at ~21:52 by an unknown
hand while this lane's stream was still running** (likely the disk guardian or
the finisher's cleanup during the quota crunch); this lane then used the
finisher's already-extracted `min/.../libtorch_cpu.so` read-only via symlink
(sha256 `830adc66e4c598d13ab47bf8cda0e58f3cac2b585f461802b21297743e601e34`)
to complete its `ldd` closure. This lane did not touch the finisher's files
except that read-only symlink. If the finisher lands its own Cascadeur proof,
the two PRs need reconciling — this doc is this lane's verified record, not
the finisher's.

## 5. How WG uses Cascadeur (posing workflow)

Honest scope first: **WG characters are 2D FLA puppets, not rigged 3D models.**
Cascadeur poses rigged 3D characters (FBX import, Quick Rigging, Auto-Posing).
There is no WG 3D rig for Cascadeur to pose today. The WG uses, in order:

1. **3D pose reference for 2D drawing (the real use now).** Pose a rigged
   stand-in in Cascadeur (physics-based posing + Auto-Posing + trajectory
   tools), screenshot/export the pose, and draw the WG puppet to it — the
   same 3D→2D technique Cape Jones already uses. This is how Cascadeur helps
   WG before any WG rig exists.
2. **Mocap retarget + Auto-Posing onto a rig.** When a WG 3D rig exists (or a
   stand-in rig is used), `libtool_retargeting.so` / `libtool_auto_posing.so` /
   `libtool_mocap.so` retarget motion onto it; `libtool_inbetweening.so` is the
   AI inbetweening backend (needs `libtorch_cpu.so` — see §3).
3. **Physics cleanup.** `libtool_auto_physics.so`, `libtool_fix_foot.so`,
   `libtool_fix_collisions.so`, ballistic-trajectory and angular-momentum tools
   clean foot sliding / collisions / weight — the defects hand-tweaked
   rotations keep producing.
4. **Rigging.** `libtool_rigging_mode.so` + `libtool_rigging_tool_window.so`
   (Quick Rigging) can rig a new model in-app when WG builds a 3D character.

What Cascadeur does **not** do for WG: it does not edit FLA puppets, does not
replace Pipeline One, and does not animate the 2D puppets directly. Anyone
claiming a WG puppet was "posed in Cascadeur" without a 3D rig step is
skipping the step that makes the claim true.

## 6. Western Heart usage — UNVERIFIED claim

The vendor-tools README says Cascadeur is "used in the Western Heart pipeline".
Checked 2026-11-13: GitHub code search `cascadeur repo:mhvnsnt/western-heart`
returns **0 hits**. No mention of Cascadeur was found in `mhvnsnt/western-heart`
by that search. The claim is **unverified, not confirmed** — do not cite
Western Heart as proof of Cascadeur use until someone finds the reference.
(Adjacent, not proof: `mhvnsnt/physics-playground-pwa` has 42 Cascadeur
mentions across its docs — a different repo's research notes, not Western Heart.)

## 7. Gaps (logged, not filled)

1. No permanent install on this VM — the proof install lives in `/dev/shm`
   (ephemeral) because home-disk quota headroom was ~84–400 MB and flickering.
   Re-install per §3 on any machine with 1.3 GB free.
2. `samples/` (89 MB) was excluded from the proof install for space — the
   bundled sample scenes were not available for the pose test.
3. The VM lacks the system XCB helper libs Qt's xcb plugin needs
   (`libxcb-util`, `-keysyms`, `-image`, `-icccm`, `-xkb`, `-render-util`,
   `-ewmh`, `-cursor`, `-composite`, `-xinerama`, `-dri2`, `-res`, `libXtst`;
   base `libxcb-render/-shm/-randr` are present). A visible X11 window needs
   those or another machine; the proof launch uses Qt's bundled offscreen
   platform plugin (`libqoffscreen.so`, shipped in `plugins/platforms/`).
   `apt` is broken on this VM (standing note), so the libs cannot be installed here.
4. No WG 3D rig exists yet — Cascadeur's WG value today is pose reference
   (§5.1), not direct puppet posing.
