# PROOFS — puppet lane (Wave 3 Worker C, 2026-10-07)

Method: prebuilt Linux binaries downloaded from GitHub releases, launched
under Xvfb (virtual display) + a D-Bus session, screenshot via `mss` on `:99`.
Proof images reopened and eyeballed before filing. Nothing here is simulated.

## 1. nijigenerate v1.0.0-beta2 — RUNNING
- Binary: `nijigenerate/nijigenerate` (ELF 64-bit x86-64), from
  `nijigenerate-linux-x86_64.zip` (30,092,332 bytes), release v1.0.0-beta2.
- License: BSD-2-Clause ✅ — verified at the PRIMARY source
  (`api.github.com/repos/nijigenerate/nijigenerate` → `license.spdx_id =
  "BSD-2-Clause"`). (Wave 2 cited alternativeTo/deepwiki; the GitHub API is
  the stronger verification.)
- Proof: `proofs/nijigenerate-xvfb2-proof.png` — full editor window:
  menu bar, "Edit Puppet" / "Edit Animation" tabs, Nodes panel with Puppet,
  Parameters tab, Inspector, Undo History, Quick Setup (Language/Color
  Theme/UI Scale), NijiGenerate logo + sample character.
- Negative proof: `proofs/nijigenerate-crash-before-dbus.png` — the crash
  dialog you get WITHOUT a D-Bus session (ddbus exception). Documents the
  headless prerequisite, not a defect.

## 2. Inochi Creator v0.8.6 — RUNNING
- Binary: `inochi-creator/inochi-creator` (ELF 64-bit x86-64), from
  `inochi-creator-linux.zip` (22,341,517 bytes), release v0.8.6 (2024-09-18).
- License: BSD-2-Clause ✅ — verified via
  `api.github.com/repos/Inochi2D/inochi-creator`.
- Proof: `proofs/inochi-creator-xvfb-proof.png` — editor open behind the
  first-run "Thank you!" donation nagscreen; Nodes/Inspector/History panels
  visible. Note: the nagscreen says "buy a copy today" — that is a donation
  prompt; the code remains BSD-2-Clause. Upstream is slow (last release Sep
  2024); nijigenerate is the active line — use nijigenerate for new rigs.

## Honest limits
- GUI proof only: no puppet was rigged end-to-end in this lane (that is a
  character-lab task, not a wiring task).
- Inochi2D D SDK: not compiled here — no D toolchain (dmd/dub/ldc2) on this
  box; prebuilt binaries made that unnecessary for the editors.
- Proof screenshots were taken on a 1280x800 virtual display; real
  workstation use needs a physical display or RDP/VNC session.
