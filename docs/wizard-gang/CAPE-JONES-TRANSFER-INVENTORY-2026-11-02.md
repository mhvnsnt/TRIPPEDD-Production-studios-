# Cape Jones → Wizard Gang Transfer Inventory — 2026-11-02

Owner's order (verbatim, 2026-11-02): "Look at all the stuff in our Cape Jones repo that would help us and copy it over to wizard gang and start making foas of the characters and good clean industry standard and production studio grade tools and software 100% wired up and helping u"

Coordinator's interpretation (marked as mine): "foas" = FLAs. This continues the standing FLA program order (2026-10-30): FLA puppets, rigs and scene files for all shows, Wizard Gang first.

Source: `mhvnsnt/cape-jones` main @ `f33c7cd` (2026-11-02). Target: this repo, main @ `dae6d16` (PR #298).
Full audit files (working copies): `~/workspace/agent-ops/cjwg-cape-inventory.md`, `cjwg-trippedd-inventory.md`, `cjwg-parts-audit.md`, `cjwg-tools-audit.md`.

Transfer rule applied throughout (owner's FREE-GAME RULE): all craft, tools, flows, techniques and templates transfer. EXCLUDED: Cape Jones's characters, character names, logos, verbatim script/dialogue, and Cape Jones-specific art/story files. Nothing below copies any of those.

---

## 1. What Cape Jones has that helps Wizard Gang

### 1a. FLA / rig tooling — TRANSFERRED in this PR
| Source (cape-jones) | What it is | Landed at |
|---|---|---|
| `donor-fla-rig-pull-20261101/check_template_gate.py` | Release gate: FAILs any FINAL deliverable that carries donor art/voice/lines unmarked. Directly enforces the FREE-GAME rule on our own output. | `production/wizard-gang-fla/tools/transferred/check_template_gate.py` |
| `donor-fla-rig-pull-20261101/LIPSYNC-TIMING-20261101.csv` | 96-frame syllable-grid lip-sync timing template (12-frame blocks, mouth classes, no words). Wizard Gang voices are laid in post (Chatterbox), so the grid is how mouth swaps get timed. Ashes-only in practice (the other 8 are mouthless by canon). | `production/wizard-gang-fla/tools/transferred/LIPSYNC-TIMING-TEMPLATE.csv` |
| `cape-jones-rig/build-fla-timeline.jsfl` | JSFL timeline builder: creates rig symbols/layers and sets per-keyframe joint rotations from a clip JSON, with the screen-angle → Animate-rotation conversion documented. | Adapted as `production/wizard-gang-fla/tools/transferred/build-fla-timeline-wg.jsfl` (WG symbol anatomy; CJ cape/leg symbols removed — WG arms are single-piece and legs don't exist in the art, see §4) |

### 1b. Pipeline documents — TRANSFERRED in this PR (reference, provenance-headed)
| Source | Landed at |
|---|---|
| `production/pipeline/FLIPACLIP-POST-PIPELINE.md` (post pipeline: holds, inbetween discipline, export discipline) | `docs/wizard-gang/transferred-from-cape-jones/FLIPACLIP-POST-PIPELINE.md` |
| `production/pipeline/ANIMATION-PIPELINE-2026.md` | `docs/wizard-gang/transferred-from-cape-jones/ANIMATION-PIPELINE-2026.md` |
| `production/dance-choreo/README.md` + `INVENTORY.md` (choreography-extraction format: beat layers, on-twos keyframing, per-layer keyframe JSON) | `docs/wizard-gang/transferred-from-cape-jones/DANCE-CHOREO-README.md` / `DANCE-CHOREO-INVENTORY.md` |

The choreography JSON data file itself (a Gumball character's dance) was NOT copied: the format and method transfer; performance data of another show's character does not move into Wizard Gang's repo. Wizard Gang choreo extractions get authored fresh in the same format when ordered.

### 1c. Production FX modules — QUEUED as transfer batch 2 (review-gated)
`production/fx/` in cape-jones (~44 entries, ~7 MB): teleport swirl, speed lines, impact frames, eye-glow, smear modules + an `fx_catalog.json` pattern (id-indexed effect catalog). These are procedural effect code (craft), and Wizard Gang needs exactly this class of effect for acting/action beats. Not copied in this PR because each module must be checked for Cape Jones art baked into frames before it lands; the catalog pattern is adopted in principle now and the modules land in a follow-up PR after that check. Logged here so the batch is not lost.

### 1d. Patterns adopted (no files copied — the pattern is the transfer)
- **Afterglow shot-preset pattern** (cape-jones `cape-jones-rig/afterglow-videos-20261031/`): a JSON shot-preset (background / pose / effect / camera push) + one builder script + proof contact sheet per preset. Adopted for Wizard Gang scene work: presets live beside the scene FLA, proof sheet mandatory.
- **Beatsync preset pattern**: audio-energy → flash-opacity envelope mapping for beat-synced cuts. Adopted for WG music/social beats.
- **Frame-data JSON pattern** (cape-jones FD-29 work): timing/numbers as JSON next to the FLA, character art excluded. This is the same shape as our per-character puppet configs in `production/wizard-gang-fla/tools/characters/`.
- **3D→2D pose-reference technique**: render a 3D pose reference at 60° steps to draw/check 2D poses against. Adopted as method for future WG pose work (no 3D assets copied).
- **Template-gate discipline** (donor pull): structure/timing may be retargeted; donor art/voice/lines never ship as final, and template files carry TEMPLATE markers. Now enforced by the transferred gate script (§1a).

### 1e. Deliberately NOT copied (with reasons)
| Cape Jones material | Why not |
|---|---|
| `production/tools/` (~12.4 GB vendored trees: Natron source, Pencil2D, Synfig, Tahoma2D, Glaxnimate, OpenToonz, Rhubarb, Blender-adjacent trees, etc.) | This repo already carries its own `tools/` wiring (incl. `tools/natron/README.md` OFX wiring); duplicating 12 GB of vendored source into a second repo is the opposite of the one-store discipline. Wired BY REFERENCE instead — see `docs/wizard-gang/TOOLS-WIRING-2026-11-02.md`. Also flagged in the source inventory: that tree contains an Adobe Animate 2024 program-bytes folder — not copied, not used (the owner's settled line: "we have better than a cracked installer"; our FLA route is the free XFL/Python chain). |
| Episodes CJ-01→CJ-30, Charlie work, dance scene videos, songs, scripts, Cape Jones art/rigs of the character himself | Cape Jones characters, names, story and art — excluded by the FREE-GAME RULE. |
| `tools/puppet/wizard-rig-proof/` (the GMSS puppet packs) | Already the source of Wizard Gang's own part libraries (`~/workspace/your_files/wizard-gang-part-libraries/*/rig-proof/`). Copying it again would duplicate our own cast source inside the repo. No-dupe: skipped. |
| Movement/dance preset DATA for Cape Jones (preset JSONs tied to his model/scenes) | The preset PATTERN transfers (§1d); his character's preset data does not. |

## 2. What Wizard Gang already had (no duplicates created)
- `production/wizard-gang-fla/` (PR #293): `WG101_ORIGINAL_PUPPET_ASHES_VERSION_001.fla`, `WG101ARRIVAL_Sc001_Clean_V001_ASH.fla`, `tools/build_ashes.py` (XFL authoring engine), `tools/fla_render.py` (XFL compositor/renderer), `tools/finish_proof.py`, proof frames f000–f052, docs (ashes-inventory, gumball-dissection, renderer-contract).
- `docs/wizard-gang/FLA-PRODUCTION-STANDARD.md` (PR #285), `WG-RIG-TEMPLATE.md`, `WG-PRODUCTION-METHOD.md`, `FIRST-SHOT-SPEC.md`, Pipeline One method + clips (PR #290), V2 stack docs.
- Tools wired 2026-10-29 (FlashXFLParser, BasicPBC, Synfig, Glaxnimate, Kdenlive, melt, Blender, Tahoma2D, Krita, Storyboarder, Natron, Ghostscript) — see §3 for their current status; most are archive-only since 2026-10-31 and are NOT needed for the FLA chain.

## 3. Tool status for the FLA chain (audited live 2026-11-02)
- **Runnable today, zero restore:** python3 3.12.3 + Pillow 10.2.0 + lxml 5.2.1 + stdlib zipfile + ffmpeg/ffprobe 8.1.2. The FLA build → validate → render → clip chain runs entirely on these plus the in-repo Python XFL code. PROVEN this program: `finish_proof.py` completed (see §5) and the generalized builder + renderer build and render all 9 puppets (Phase 4 PR).
- **Validator wired:** the repo's own `fla_render.py` parse + `agent-ops/fla-puppets-program-2026-10-30/work/parse_xfl.py` (stdlib XFL parser). FlashXFLParser (C#) is archive-only (in `tools-archive-2026-10-31` on western-heart, needs .NET SDK, also archived) — kept as an optional cross-check, not a dependency. Full wiring notes: `docs/wizard-gang/TOOLS-WIRING-2026-11-02.md`.
- **Archive-only (restore only when a step truly needs them):** Blender, Krita, Synfig, Tahoma2D, Kdenlive, melt, Natron, Ghostscript, Java+FFDec, .NET+FlashXFLParser, BasicPBC. Pull-back: `gh release download tools-archive-2026-10-31 --repo mhvnsnt/western-heart`, reassemble per the release `MANIFEST-tools.md`.
- **Honest renderer limit:** the Python XFL renderer handles bitmap/symbol instances (all WG puppet parts are bitmaps). Raw `DOMShape` vector geometry is not rasterised by it — a gap for vector-only rigs, logged, not faked.

## 4. Parts ground truth for the 9 puppets (audited 2026-11-02)
Real separated parts exist for all 9 in `~/workspace/your_files/wizard-gang-part-libraries/<char>/rig-proof/parts/` (full-common-canvas layers + `parts_manifest.json` bboxes), plus cut-apart Ashes (the only measured pivot set). Universal gaps — LOGGED, never fabricated:
- **Legs / hips / knees: do not exist for any character.** Every source design is robe-to-the-floor; there is no leg art to extract. No puppet in this program claims hip/knee bends.
- **Elbows: do not exist for any character.** Every extracted arm is one drawn piece (REST pose). Shoulders bend; elbows cannot without inventing art.
- **Neck/shoulder overlap: 0 px measured** (upstream segmentation partitioned the figure). Small rotations stay closed; wide rotations open wedges — pose ranges in the builder are set accordingly, and the robe-full + figure underlay layers sit beneath so a wedge never shows void.
- **Sombra Negra and Hollow have NO separated arms or hands in their source** (arms were never separated; they live inside the robe drawing). Their puppets are head/eyes/chain/robe builds with the arm gap logged; their motion proof comes from neck, waist, skirt and eye work.
- **Kiko's standard eye system is 4 sparkle files only** (her full eye set exists only in her battle variant). Her puppet uses her head-baked eyes + sparkle overlays; blink system logged as a gap for the standard variant.
- Only Ashes has a real mouth (his grill, canon — always on). The other 8 are mouthless in the puppets by canon; their built Set-One mouth shapes are NOT default symbols.

## 5. Phase status
- Phase 1 (this inventory): DONE in this PR.
- Phase 2 (transfer): DONE in this PR (§1a/§1b); FX modules queued as batch 2 (§1c).
- Phase 3 (tool wiring + Ashes proof finish): `finish_proof.py` RUN 2026-11-02 — frames f053–f071 rendered (72/72), `WG101ARRIVAL_Sc001_V001.mp4` (449,467 B), frame strip + pose sheet + structure sheet built; outputs land with the Phase 4 PR in `production/wizard-gang-fla/proof/`. Own-eyes QC: scene motion is a slow push-in (subtle at scene scale by shot design); puppet pose sheet shows the distinct poses at figure scale; known defect — inpainted robe fill (dark blocks) reveals at robe edges on the widest moves (documented in the Ashes parts.json since 2026-10-30).
- Phase 4 (puppets ×9): generalized builder `tools/build_puppet.py` + per-character configs; Ashes verified against PR #293, other 8 built from their real parts with gaps per §4; per-character motion proof (clip + frame strip) with unique filenames. Lands as its own PR.
