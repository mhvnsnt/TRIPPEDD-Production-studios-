# ASHES / BUFFALO BILL — Likeness Notes (EP02 character reference set)

## Status: NO GLB FOUND — nothing rendered
Searched 2026-10-07 across `~/workspace/bannon-repair`, `~/workspace/game-sweep/AshLanev2`,
`~/workspace/brutal-fist-v10`, and a full `~/workspace` sweep for `*ashes*`, `*narrator*`,
`*bill*`, `*buffalo*` GLBs: **no Ashes or Buffalo Bill GLB exists.** Findings:
- `BILL_DOZER.glb` (AshLanev2 `public/models/cast/`) is the Goldberg-based canon wrestler
  **Bill Dozer** — a different character, NOT Buffalo Bill / Ashes.
- 2D references only: `~/workspace/game-sweep/AshLanev2/public/portraits/buffalo-bill*.webp`
  (buffalo-bill, buffalo-bill-hood, buffalo-bill-robed, buffalo-bill-robed-red).
- A generator script exists: `~/workspace/game-sweep/AshLanev2/tools/generative/3d/buffalo_bill.py`
  — untested in this task; potential route to produce the missing GLB.

## Gap
EP02 cannot get a GLB-based character reference for Ashes/Buffalo Bill until a model is
generated (the `buffalo_bill.py` script is the lead). Episode generators must use the
webp portraits above, not invent a look. Note the canon distinction: the purple-robed
Narrator is Ashes-outside-the-fiction (voice-only in the cartoon); the red robe is
Ashes in-world.
