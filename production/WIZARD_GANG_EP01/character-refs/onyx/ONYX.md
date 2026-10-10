# ONYX — Locked Likeness & Attire Inventory (EP02 character reference set)

Reference stills in this folder were rendered 2026-10-07 via Blender 4.0.2 headless
(EEVEE, neutral gray background, front view, full body in frame).
Owner anchors: `onyx-glb-blackhair.png` (Attire 1), `onyx-glb-greenhair.png` (Attire 2).

## LOCKED likeness (applies to every Onyx appearance, hood-off/unrobed)
- **Face:** full white clown face paint. Black teardrop/diamond markings around the eyes,
  black nose, large black mouth/smile region, small black forehead mark. This face is
  consistent across both owner anchors and all four GLBs below — it is the locked face.
- **Build:** full-figured / curvy. Brown/dark skin on exposed areas.
- **Signature features:** layered chokers/necklaces at the neck.

## Attire inventory (GLB -> owner attire)
| GLB file | Render | Owner attire | Verdict |
|---|---|---|---|
| `ONYX_corset_repaired.glb` | `onyx-corset-front.png` | **Attire 1** (blackhair anchor) | MATCH |
| `ONYX.glb` | `onyx-base-front.png` | **Attire 2** (greenhair anchor) | MATCH |
| `ONYX_street_repaired.glb` | `onyx-street-front.png` | **Street** | LOCKED (owner 2026-10-07) |
| `ONYX_straightjacket_repaired.glb` | `onyx-straightjacket-front.png` | **Straightjacket** | LOCKED (owner 2026-10-07) |

### Attire 1 — `ONYX_corset_repaired.glb` — MATCHES `onyx-glb-blackhair.png`
- Hair: black, voluminous wavy/curly with the two side coils framing the face. Matches.
- Face paint: white base, black teardrops around eyes, black mouth region, black nose. Matches.
- Outfit: black-and-white studded corset bodysuit (strapless sweetheart neckline, white cups
  with black paneling and studs). Matches.
- Studded black arm guards with white cuff bands. Matches.
- Black studded knee-high boots with white trim bands at top. Matches.
- Chokers, bare brown thighs. Matches.
- **Gaps:** none significant. This GLB is the Attire 1 reference.

### Attire 2 — `ONYX.glb` — MATCHES `onyx-glb-greenhair.png`
- Hair: neon/lime green, long and straight, darker green gradient toward the ends. Matches.
- Face paint: white base, black teardrop markings under eyes, solid black clown nose,
  big black smile. Matches.
- Outfit: white-dominant corset-style top with black tribal/graffiti print, long spiked
  sleeves, high-waisted tribal-print briefs, spiked arm guards, black boots. Matches.
- **Gaps (minor):** the anchor shows white printed shin-wrap/sock coverage between boots and
  shorts; the GLB renders printed thigh-high/shin coverage in the same print — near match,
  same print family. Build matches (full-figured).

### Street — `ONYX_street_repaired.glb` — LOCKED (owner 2026-10-07)
- Neon green hair (same as Attire 2) + same white clown face paint — identity reads as Onyx.
- Outfit: black/white striped graphic sweatshirt (skull print), baggy dark cargo jeans with
  black cross prints and vertical text print, black crossbody bag, black/white sneakers.

### Straightjacket — `ONYX_straightjacket_repaired.glb` — LOCKED (owner 2026-10-07)
- Dark hood/hair covering the head, white clown face with black diamond/teardrop eye markings,
  black nose, black smile — face reads as Onyx.
- Outfit: black vinyl buckled straitjacket-style top (asymmetric buckles), pleated black mini
  skirt, neon-yellow web-pattern stockings, chunky black platform boots.

## Defects / gaps
- Non-repaired variants (`ONYX_corset.glb`, `ONYX_straightjacket.glb`, `ONYX_street.glb`) exist
  but were not rendered — repaired variants preferred per brief.
- All four GLBs face +X in Blender space (camera side `+x`). Consistent.
- GLBs contain a low-poly `Icosphere` proxy mesh (42 verts) that inflates auto-framing;
  the render script ignores meshes under 500 verts for framing.
- No GLB contradicts the locked face. The two owner anchors are both covered 1:1 by GLBs.

## Alt attire — "Bomber" (owner-supplied 2026-10-07, locked)
- onyx-attire-bomber.png
- Green hair, white clown face paint; black/green bomber jacket, layered gold chains, black jumpsuit.
