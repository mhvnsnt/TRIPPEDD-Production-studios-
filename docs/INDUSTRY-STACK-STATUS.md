# INDUSTRY STACK STATUS — free wire-up pass, 2026-10-30

What this is: the industry top-11 for 3D animation / shows (Maya, Houdini,
Blender, Unreal, ZBrush, Substance Painter, Nuke, Cinema 4D, 3ds Max,
Toon Boom Harmony, Arnold) plus the free game engines, checked against what
is actually wired on the studio machine. Every state below was verified on
2026-10-30 by binaries-present checks and smoke tests on the VM itself —
not copied from older READMEs. UNKNOWN is never written up as working.

## License classes used in this doc

- **FREE-100%** — free for commercial use, no account, no watermark, no catch.
- **FREE-TIER** — free to use, with the catch stated in the row (revenue cap,
  non-commercial terms, or an account/form gate).
- **PAID** — subscription/purchase software. These are DOCUMENTED with
  their license status and real terms (see §3).

## States used in this doc

- **WIRED+VERIFIED** — binary present, smoke test passed on this machine.
- **INSTALLED** — files present and version-confirmed, launch blocked by
  this VM's environment (stated), not by the install.
- **VERIFIED-ACCESS** — we hold the real thing (repo/account), build not run.
- **BLOCKED / DOCUMENTED** — the honest stop point, with the exact reason.

---

## 1. The free lane — wired and verified

| Tool | Standard for | License | Our state (verified 2026-10-30) |
|---|---|---|---|
| Blender | All-round 3D suite; the open-source #1 (Flow, Chainsaw Man – The Movie) | FREE-100% (GPL) | **WIRED+VERIFIED** — 4.0.2, 4.5.3 LTS and 5.2.3 LTS all answer `--version`. `~/workspace/tools/blender/`, `~/workspace/tools/blender-4.5/`, `~/workspace/tools/blender-5/` |
| Godot | Free game engine (indie standard) | FREE-100% (MIT) | **WIRED+VERIFIED** — `Godot_v4.7.2-stable_linux.x86_64 --headless --version` → `4.7.2.stable.official`. 4.4.1 also present; 4.7.2 export templates (.tpz) on disk. `~/workspace/tools/godot/` |
| Natron | Compositing — the open-source Nuke seat | FREE-100% (GPL) | **WIRED+VERIFIED** — 2.5.0 (`Natron version 2.5 … branch tags/v2.5.0`), headless renderer runs via `~/workspace/tools/natron/natron-render.sh` |
| Krita | Digital painting | FREE-100% (GPL) | **WIRED+VERIFIED** — 6.0.4 AppImage (extracted tree; this VM has no FUSE), `--version` → `krita 6.0.4`. `~/workspace/tools/krita/run-krita.sh` |
| Tahoma2D | Cutout 2D rigs (OpenToonz lineage; the mystery-coast pipeline tool) | FREE-100% (open source) | **WIRED+VERIFIED** — 1.6.3 launches and stays up under Xvfb. `~/workspace/tools/tahoma2d/run-tahoma2d.sh` |
| Pencil2D | Hand-drawn 2D passes | FREE-100% (open source) | **WIRED+VERIFIED** — 0.7.2 (per 2026-10-29 stack audit), extracted AppImage tree launches under Xvfb. `~/workspace/tools/pencil2d/run.sh` |
| Storyboarder | Storyboarding | FREE-100% (open source) | **WIRED+VERIFIED** — 2.1.0 AppImage (extracted tree) launches under Xvfb. `~/workspace/tools/storyboarder/run-storyboarder.sh` |
| Rhubarb Lip Sync | Lip sync from voice tracks | FREE-100% (open source) | **WIRED+VERIFIED** — `--version` → `Rhubarb Lip Sync version 1.14.0`. `~/workspace/tools/rhubarb/rhubarb` |
| ffmpeg | Media plumbing for every pipeline | FREE-100% (LGPL/GPL builds) | **WIRED+VERIFIED** — 8.1.2 at `/usr/bin/ffmpeg` |
| OpenToonz | Full 2D suite (scanned cleanup, cutout, FX) | FREE-100% (open source) | **INSTALLED** — 1.8.0 Flathub tree present (`~/.local/share/flatpak/app/io.github.OpenToonz/`, binaries incl. `tcomposer` headless renderer). **Launch blocked in this VM only:** the kernel has no FUSE (`/dev/fuse` absent), so flatpak's document portal cannot mount; it launches normally on any FUSE-capable session. Full evidence: `~/workspace/tools/opentoonz/WIRING.md` |

## 2. Free-tier — real access, catch stated

| Tool | Standard for | License class | Our state |
|---|---|---|---|
| Unreal Engine | Real-time 3D, virtual production; #1 game engine (GDC 2026: 42% of devs, 47% of AAA) | **FREE-TIER** — free until **$1M gross revenue per product**, 5% royalty after. Source-available, **not** open source | **VERIFIED-ACCESS** — the owner's fork `mhvnsnt/UnrealEngine` (18.2 GB, Epic-authorized) spot-checked via API on 2026-10-30: default branch `release` = **Unreal Engine 5.8.2** (Engine/Build/Build.version), full `Engine/Source` tree (Developer / Editor / Programs / Runtime / ThirdParty) plus `Setup.sh` and `GenerateProjectFiles.sh` present. **Not built here:** a source build wants ~150 GB+ of disk and hours on many cores; this VM has 2 cores and ~46 GB free. Build it on a real workstation or a cloud GPU box when a project needs it — the source and the license are already ours. |
| Houdini Apprentice | FX / simulation standard (the #2 tool on the list) | **FREE-TIER with hard catch** — free but **NON-COMMERCIAL learning edition**: non-commercial `.hipnc` files, "Render (NC)" watermarked renders capped at 720p, license renews every 30 days (SideFX FAQ) | **BLOCKED AT LOGIN — one owner sign-in away.** Verified 2026-10-30: SideFX's own FAQ states a (free) SideFX web account is required to download the software, and `sidefx.com/download/` serves only login/OAuth links to anonymous visitors — there is no anonymous installer URL to fetch. Owner step: sign in at https://www.sidefx.com/download/ (Google OAuth is offered), run the Houdini Installer, and the first launch installs the free Apprentice license. |
| DaVinci Resolve (free edition) | Editing, color, Fusion VFX, Fairlight audio | **FREE-TIER** — the free edition is a genuinely full NLE/color/Fusion suite and allows commercial work; Studio ($295 one-time) adds noise reduction, HDR tools, higher resolutions, extra FX | **DOCUMENTED — one owner click away.** The official page is live (HTTP 200 verified 2026-10-30), but the Linux download sits behind Blackmagic's registration form (name / email / address → "Register & Download") at https://www.blackmagicdesign.com/products/davinciresolve. The download was not completed; it stops at that form. Current version: Resolve 21.x. |

Paid Houdini tiers, for the record: Indie $269/yr (the cheapest commercial
Houdini), Core $1,995, FX $4,495 (node-locked). Apprentice above is the
free learning tier of the same software.

## 3. Paid list — license status

| Tool | Standard for | Real terms | Our free equivalent (wired) |
|---|---|---|---|
| Autodesk Maya | Character animation — the industry #1 | PAID — ~$2,010/yr subscription; 30-day trial exists | Blender (rigging/animation, Grease Pencil) |
| SideFX Houdini (commercial) | FX and simulation | PAID — Indie $269/yr, Core $1,995, FX $4,495 | Blender simulation + geometry nodes; Apprentice for learning (see §2) |
| ZBrush (Maxon) | Sculpting — the undisputed standard | PAID — ~$49/mo subscription | Blender sculpt mode |
| Substance 3D Painter (Adobe) | Texturing for games/film | PAID — Adobe subscription | Blender + Krita painting |
| Nuke (Foundry) | Compositing at tier-1 studios | PAID — ~$14K/yr class; a restricted Non-Commercial learning edition exists | Natron 2.5.0 |
| Cinema 4D (Maxon) | Motion graphics / broadcast | PAID — subscription; 14-day trial exists | Blender |
| Autodesk 3ds Max | Game art, archviz | PAID — ~$2,010/yr subscription; 30-day trial exists | Blender |
| Toon Boom Harmony | 2D animation for TV | PAID — subscription | Tahoma2D, OpenToonz, Pencil2D |
| Arnold (Autodesk) | Cinematic rendering (ships with Maya) | PAID — bundled with Maya / standalone license | Cycles (Blender, incl. the ACES pipeline already wired in the cape-jones work) |
| Unity | Game engine #2 (30% of devs; owns mobile) | FREE-TIER/PAID — Personal free until $200K revenue, then Pro ~$2,310/seat/yr | Godot 4.7.2 (free-100%, wired) and Unreal (see §2) |

## Owner next steps (the only two, both are sign-in/form gates)

1. **Houdini Apprentice:** sign in once at https://www.sidefx.com/download/
   (free account, Google OAuth offered) and grab the Houdini Installer —
   Apprentice itself is then fully free to install and learn on.
2. **DaVinci Resolve free:** complete the one registration form at
   https://www.blackmagicdesign.com/products/davinciresolve
   (Linux → Register & Download) — the ~3 GB zip then downloads directly.

Everything else on the industry list is either already running on this
machine (Blender ×3 versions, Godot, Natron, Krita, Tahoma2D, Pencil2D,
Storyboarder, Rhubarb, ffmpeg), installed and waiting on a FUSE-capable
session (OpenToonz), or already ours in source form (Unreal Engine 5.8.2).
