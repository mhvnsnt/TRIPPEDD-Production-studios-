# Universal Entrance + 3D Video Production Kit

This is the portable production contract extracted from the verified Bannon entrance system.

## Proven source

The Bannon implementation was built and measured in:
- `7cf8bafd48741a95cf56b36871b349932311e57e` — sequential entrances + per-character entrance kit.
- `521fb9503afc88b14d1bcd84ae0dc5e90edf10bc` — real pyro, smoke, animated tron and entrance/victory FX.
- `5b9ccad590cb377e083c1d83e17a57a6a50f058a` — real saved entrance timeline editor.
- `9e15a70abb15b6ee49b24fa5141371527c07e263` — custom tron studio with persistent media storage.

## Portable kit

Every supported game/3D production should expose the same logical controls, while mapping them to that game's actual renderer:

### Character identity
- canonical character ID
- display name
- game/project ID
- verified model/GLB asset ID
- attire ID
- rig/skin verification status

### Entrance presentation
- titantron: AUTO / VIDEO / NAME / NONE
- mini-trons
- lighting: ARENA / DARK / SPOT / STROBE / COLOUR
- optional light colour
- smoke: NONE / LOW / HEAVY
- pyro: NONE / STAGE / RINGPOST / FULL
- gait/motion preset
- hold/pause duration
- ordered camera shots

### Timeline
Cues are data, not hard-coded video edits:
`{ t, type, payload }`

Supported baseline cue types:
- TRON
- PYRO
- PYRO_RING
- SMOKE
- LIGHT
- CAMERA
- MUSIC
- HOLD

The host game may add cues, but must never silently reinterpret another game's cues.

### Video outputs

A production run can emit:
- gameplay/entrance master
- 16:9
- 9:16
- 1:1
- thumbnail/still
- title-card sequence
- captions/subtitles
- provenance manifest
- SHA-256 checksums

## Evidence gates

A character video is READY only if:
1. The actual intended game/build was rendered.
2. The intended character asset was actually loaded at runtime.
3. Rig/skin/deformation evidence is clean.
4. Every move/effect shown exists in that build or is explicitly marked production-only.
5. No other game's branding, UI, arena or character data leaked into the cut.
6. No placeholder canon data appears.
7. Audio has been listened to/checked.
8. The source build, model, timeline and output hashes are recorded.

UNKNOWN stays UNKNOWN. A filename, static manifest entry or generated preview is not proof of runtime use.

## Cross-game rule

A character appearing in multiple games gets a separate production package per game. Never relabel Bannon footage as Brutal Fist, AshLane, OTR, or another project.

The shared kit provides controls and production machinery; the game supplies its own:
- arena
- renderer
- lighting language
- UI
- character model
- moves
- camera behavior
- branding/canon

## Asset-generation rule

The kit can orchestrate:
- GLB/model preparation
- rig/skin QA
- animation intake
- camera staging
- lighting
- particles
- tron/title-card generation
- real gameplay capture
- edit/export

It must not silently substitute a generated character for a required real game character. Generated assets must be explicitly labeled as generated/reference/production-only.

## Reference look

The El Toro de Oro entrance package is a Bannon visual reference only:
dark arena, controlled spotlight, smoke, pyro, deliberate camera cuts, character-focused presentation.

It is not a universal visual skin. Other games retain their own visual identity.
