# CIPHER — Locked Likeness & Attire Inventory (EP02 character reference set)

Reference stills rendered 2026-10-07 via Blender 4.0.2 headless
(EEVEE, neutral gray background, front view, full body in frame).
No owner anchor image was supplied for Cipher in this task — likeness notes below are
observed from the GLB only. Do NOT treat them as owner-locked.

## Observed likeness (from `CIPHER_feral_v2.glb`)
- **Face/head:** bald, heavy brow, wide feral grin showing teeth. No face paint.
- **Build:** heavy, powerfully muscular.
- **Signature features:** extensive tattoos — large moth on the chest, full arm sleeves,
  script/text tattoo across the abdomen.

## Attire inventory (GLB -> render)
| GLB file | Render | Status |
|---|---|---|
| `CIPHER_feral_v2.glb` | `cipher-feral-v2-front.png` | RENDERED — feral crouch pose, black trunks, black knee pads, black boots, black wrist tape |
| `CIPHER_feral.glb` | — | **RENDER FAILED** (see below) |
| `CIPHER_rigged.glb` (alt) | — | **RENDER FAILED** (see below) |

Per the brief, feral is the canon look for the show; `CIPHER_rigged.glb` was to be the alt.
Only the v2 feral could be rendered.

## Defects / gaps
- **RENDER FAILURE — `CIPHER_feral.glb`:** Blender 4.0.2's glTF importer rejects it:
  `RuntimeError: Error: Extension EXT_meshopt_compression is not available on this addon version`.
  Fallbacks attempted: gltf-transform CLI 4.5.1 (no geometry-decompress command),
  repo donor search (only a vendored JS meshopt decoder, no decompress script).
  A correct decompress script needs per-attribute filter metadata — flagged as follow-up work,
  not attempted, to avoid shipping a corrupt decode.
- **RENDER FAILURE — `CIPHER_rigged.glb`:** same EXT_meshopt_compression failure.
- **Gap:** with both v1 feral and the rigged alt unrenderable, there is no alt-attire
  reference for Cipher. The canon feral (v2) is covered.
- Rendered GLB faces +X in Blender space (camera side `+x`), consistent with the others.
