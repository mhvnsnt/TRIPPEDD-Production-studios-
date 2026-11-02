# Wizard Gang Tools Wiring — 2026-11-02

What is wired, how it is invoked, and the proof it ran. Audited live 2026-11-02 for the Cape Jones → Wizard Gang transfer program (see `CAPE-JONES-TRANSFER-INVENTORY-2026-11-02.md`).

## The FLA chain — wired and PROVEN (no installs, no archive restore)

| Stage | Tool | Invocation | Proof |
|---|---|---|---|
| Build (.fla/XFL authoring) | `production/wizard-gang-fla/tools/build_ashes.py` (Ashes, PR #293) and the generalized `production/wizard-gang-fla/tools/build_puppet.py` + `tools/characters/*.json` (Phase 4) | `python3 build_puppet.py <char>` — python3 3.12.3, Pillow 10.2.0, stdlib zipfile | .fla files built for all 9 characters; unzip listing verified |
| Validate / parse | In-repo XFL parser/renderer `production/wizard-gang-fla/tools/fla_render.py` (parses DOMDocument.xml + every DOMSymbolItem; rendering *is* the parse) + `parse_xfl.py` from the 2026-10-30 FLA puppets program | `python3 fla_render.py <xfl_dir> --scene --frame N --out f.png` | Exit 0 renders for every puppet; parse errors would fail the render |
| Render frames | `fla_render.py` (Pillow affine warp per instance matrix, Flash semantics) | as above | Per-character frame sequences rendered 2026-11-02 |
| Clip assembly | ffmpeg 8.1.2 (system) | `ffmpeg -framerate 24 -i f%03d.png -c:v libx264 -crf 17 -pix_fmt yuv420p` | Per-character proof MP4s + Ashes scene MP4 (449,467 B) |
| Template gate | `production/wizard-gang-fla/tools/transferred/check_template_gate.py` (transferred from cape-jones) | `python3 check_template_gate.py <folder>` → exit 0 PASS / 1 FAIL | Run over the Phase 4 proof folders before landing |
| Lip-sync timing | `production/wizard-gang-fla/tools/transferred/LIPSYNC-TIMING-TEMPLATE.csv` (transferred) | Reference grid for mouth-swap timing in post (Chatterbox voices laid in post, never generated in the video step) | — |
| In-Animate timeline build | `production/wizard-gang-fla/tools/transferred/build-fla-timeline-wg.jsfl` (adapted from cape-jones) | Open in Adobe Animate, paste clip JSON, run | NOT run here — no Animate in this VM (same status as the source file). The Python chain above is the proven route. |

## Renderer limits (honest)
- Bitmap/symbol instances only. Raw `DOMShape` vector geometry is not rasterised by the Python renderer. All Wizard Gang puppet parts are bitmaps, so the chain is complete for this cast; vector-only donor rigs would render shapes missing — logged gap, not faked.
- The renderer canvas comes from each character's config (canvases differ per character: 245×910 … 1060×1945). The PR #293 renderer hardcoded the Ashes canvas (400×864); the generalized renderer in `tools/wg_render.py` (Phase 4) takes canvas from config.

## Archive-only tools (wired 2026-10-29, stored 2026-10-31 — restore only on need)
`~/workspace/tools/` was stored to GitHub release `tools-archive-2026-10-31` on `mhvnsnt/western-heart` (29 hash-verified pieces, pull-back tested) and deleted locally under the owner's storing order. Pull-back: `gh release download tools-archive-2026-10-31 --repo mhvnsnt/western-heart`, reassemble per the release's `MANIFEST-tools.md`.

| Tool | Status 2026-11-02 | Needed for |
|---|---|---|
| Blender 4.0.2 / 5.2.3 | archive-only | 3D pose-reference renders, 3D scenes |
| Krita 6.0.4, Synfig 1.5.5, Tahoma2D 1.6.3, Glaxnimate 0.6.0, Storyboarder 2.1.0 | archive-only | Drawing/authoring passes |
| Kdenlive 26.08.2, melt 7.43.0 | archive-only | Edit/assembly (ffmpeg covers the FLA proof chain) |
| Natron 2.5.0 | archive-only; this repo also carries `tools/natron/README.md` OFX wiring; cape-jones carries a vendored Natron tree wired BY REFERENCE (not copied — see inventory §1e) | Compositing |
| Ghostscript 10.07.1 | archive-only (not on PATH) | EPS/PDF/SVG rasterising |
| Java 21 + JPEXS FFDec | archive-only | SWF decompile (donor scene work) |
| .NET SDK + FlashXFLParser (C#) | archive-only | Optional stricter XFL cross-check; the Python parser is the wired validator |
| BasicPBC | archive-only (torch venv, ~GBs) | Paint-bucket colourisation stage only |

## Cape Jones production software — wired by reference, not copied
Cape Jones's `production/tools/` holds vendored trees (Natron, Pencil2D, Synfig, Tahoma2D, Glaxnimate, OpenToonz, Rhubarb lip-sync, RIFE) totalling ~12.4 GB / ~59k files. Wizard Gang does not duplicate them. When a WG step needs one, it uses (in order): (1) the system/python chain above, (2) the tools-archive pull-back, (3) the cape-jones tree in place via its own checkout. The one exception class is small, WG-adapted code — which is what `tools/transferred/` holds.
