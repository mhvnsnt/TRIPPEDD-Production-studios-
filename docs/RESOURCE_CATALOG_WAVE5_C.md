# RESOURCE_CATALOG Wave 5 appendix — Worker C (council rigs: Onyx, Echo, Kiko)

Coordinator: merge into RESOURCE_CATALOG.md. Do not edit RESOURCE_CATALOG.md in this file — entries below are in the standard format with [Wave 5] tags.

## New entries

#### Onyx nijilive rig ✅
- **What:** Puppet rig for council member Onyx (green robe, jester-bell hood, black void face, green/white eye glints, gold sleeve studs) — nijilive `.inp`, opens in nijigenerate
- **URL:** god-molecule-studio `tools/puppet/wizard-rig-proof/onyx/Onyx.inp` (sha256 `73b0765230509c1347ca5fba512084851415d0e8843fe2160d6485c18d7972f7`)
- **License:** BSD-2-Clause toolchain (image2live2d + nijigenerate/Inochi2D); rig art derived from owner canon
- **Free tier:** fully open
- **Repo lane:** god-molecule (puppet)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5 (drop-in `.inp`)
- **Status:** verified (structural validation + eyes-on proof renders)
- **Notes:** 12 parts, 18 params (all bound), 2 physics, 13 anims. Proof renders: neutral, head-turn, blink (real closed-eye art swap). Recipe: Wave-4 Ashes pipeline. No mouth layer (void face by design) [Wave 5]

#### Echo nijilive rig ✅
- **What:** Puppet rig for council member Echo (pink splatter robe, ECHO name pendant, black void face, pink glints) — nijilive `.inp`, opens in nijigenerate
- **URL:** god-molecule-studio `tools/puppet/wizard-rig-proof/echo/Echo.inp` (sha256 `a814fc1cd8182d8f54444cc1a0a3d9d67cfec5a34ef2739d7712b7f1c549a066`)
- **License:** BSD-2-Clause toolchain (image2live2d + nijigenerate/Inochi2D); rig art derived from owner canon
- **Free tier:** fully open
- **Repo lane:** god-molecule (puppet)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5 (drop-in `.inp`)
- **Status:** verified (structural validation + eyes-on proof renders)
- **Notes:** 11 parts, 16 params (all bound, incl. ParamAcc0 chain sway), 2 physics, 13 anims. Proof renders: neutral, head-turn, blink. No spray can (street-persona card only — not grafted). No mouth layer (void face by design) [Wave 5]

#### Kiko nijilive rig ✅ (honest gap: no blink)
- **What:** Puppet rig for council member Kiko (white fur hooded robe, black void face, gold chains on bare chest, gold KIKO pendant, colorful dragon tights) — nijilive `.inp`, opens in nijigenerate
- **URL:** god-molecule-studio `tools/puppet/wizard-rig-proof/kiko/Kiko.inp` (sha256 `62f3daf9a4146f1431a1d04fd0647246b122c397d367fdd83a5bfbc949bedfb5`)
- **License:** BSD-2-Clause toolchain (image2live2d + nijigenerate/Inochi2D); rig art from the owner-approved robed card (`AshLanev2/public/portraits/kiko-tanaka-robed.webp`, 2026-10-06)
- **Free tier:** fully open
- **Repo lane:** god-molecule (puppet)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5 (drop-in `.inp`)
- **Status:** verified (structural validation + eyes-on proof renders)
- **Notes:** 9 parts, 18 params (all bound), 2 physics, 10 anims. Proof renders: neutral, head-turn. NO blink: the robed card's face is pure black void (max V=90; the "sparkly white glints" live on the group-art Kiko, a different source — not composited, would invent canon). Documented in RIG_PROOF_WAVE5.md [Wave 5]

## Process note (applies to all three rigs)

#### nijigenerate headless setup-wizard bypass — SOLVED
- Wave 4 set `"firstrun_complete": true` in `~/.config/nijigenerate/settings.json` but the wizard still appeared. Root cause (nijigenerate source, `source/app.d` + `source/nijigenerate/windows/welcome.d`): the Quick Setup wizard is gated by **`hasDoneQuickSetup`**, not `firstrun_complete`. With `"hasDoneQuickSetup": true` set and a file path passed as `argv[1]`, nijigenerate calls `incOpenProject()` directly — no WelcomeWindow, no wizard. No `--no-wizard` flag exists; the settings key + file argument is the supported bypass. Fix applied to the settings file 2026-10-07. Headless recipe: `xvfb-run nijigenerate /path/to/rig.inp`. Caveat: verified by source reading; the binary is not currently installed here, so re-verify with a live binary before automating [Wave 5]
