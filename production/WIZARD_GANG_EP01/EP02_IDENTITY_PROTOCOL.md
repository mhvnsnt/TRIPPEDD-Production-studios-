# WIZARD GANG — EP02 IDENTITY PROTOCOL

**Production law for every shot generator.** This protocol makes likeness drift
IMPOSSIBLE, not just unlikely. It answers the owner's pre-announced critique before
he makes it: no same-character alterations between shots, no character that looks
nothing like their hand-picked card.

Single source of truth: `EP02_LIKENESS_BIBLE.md`. Cards live in
`production/WIZARD_GANG_EP01/character-refs/<character>/`. GLBs live in
`~/workspace/bannon-repair/` (paths per the bible).

---

## 0. THE STILLS GATE (owner workflow, 2026-10-07 — EP01 pipeline)

EP02 follows the EP01 pipeline: **build ALL episode stills first** (character stills,
scene stills, key frames) **for the owner's approval BEFORE any video generation.**
Stills gate, then video. Do NOT start video gen until he OKs the stills.

- Every shot in `EP02_SHOT_LIST.md` gets its still(s) generated and identity-checked
  (this protocol) BEFORE any video work begins.
- The full still set goes to the owner as one package with the shot log. He approves
  the stills — or flags drift — and only approved stills move to video generation.
- A video segment is generated FROM its approved still, never from a fresh prompt.
  The still IS the shot's identity lock.

## 1. The anchor rule

Every shot plan lists, for EACH character in the shot:
- the character's name,
- whether they appear ROBED or UNROBED,
- the ANCHOR CARD (exact filename from the bible),
- the GLB ANCHOR (exact path from the bible, when one exists — MISSING for Kiko).

The generation prompt for a character must name the anchor card explicitly, e.g.:
"Cipher — unrobed, Base Blackheart — anchor `cipher-base-front.png`."

No character is ever generated from memory, from a previous shot, or from a
"similar" card. The anchor card is the only reference.

## 2. GLB-vs-card consistency (owner 2026-10-07)

The card art, the attire refs, AND the GLB must all describe ONE person. A GLB that
doesn't look like the card is a defect.

- **On any GLB-vs-card conflict, THE CARD WINS.** The card is the owner's hand-picked
  likeness. The GLB is repaired, or its defective part is banned from use.
- **Known defects are already ruled** (see bible): Echo's GLB face is banned — the
  GLB is a body donor only, the face always comes from the card. Cipher's
  `CIPHER_feral.glb` / `CIPHER_rigged.glb` are banned entirely (unverifiable).
- **GLB orientation quirks are flagged, not "fixed":** Sombra Negra's GLB faces -Y
  while every other character GLB faces +X — the rig/animation pipeline must handle
  it, not silently rotate the character.
- **Junk geometry in a GLB file is not character:** Sombra's GLB contains environment
  pieces (Object_42, Object_4) — exclude from renders, never treat as body parts.
- When a new or repaired GLB enters the pipeline, it is verified against the card
  BEFORE it becomes an anchor. An unverified GLB is not an anchor.

## 2. One scene = one batch = one card set

All shots in one scene are generated AND checked as a batch against the SAME cards:
1. Generate every shot in the scene.
2. Before ANY shot ships, the checker opens each shot's frames next to the anchor
   card, side by side, and verifies: face · body/build · attire details · robe color ·
   pendant · signature features (horns, ears, mask, grin, paint).
3. Only when every shot in the scene passes does the scene lock. A scene ships whole
   or not at all.

This is what kills "the same character looks different in the same scene."

## 3. The verification checklist (per character, per shot)

| Check | Method |
|---|---|
| Face = card face | Open anchor card + shot frame side by side. Visual compare. |
| Build = card build | Same body type, same proportions. |
| Attire details | Every named element present (e.g., Onyx's chokers, Theory's ears, Ashes' horns, Sombra's thigh tassels — TASSELS ARE INTENTIONAL, never "fixed"). |
| Robe color + pendant | Canon color, canon pendant text. |
| Style declared + held | Shot plan declares CARTOONY or PAINTERLY. The checklist above is style-agnostic — a painterly shot must still match the card. |
| No duplicate | No two same-robe-color copies, no robed+unrobed of the same person in frame (S19). The S11 street-crew wink is the one sanctioned beat — never repeat it elsewhere. |

**Style-switch rule (owner 2026-10-07):** style changes happen ONLY at flagged dramatic
beats (flare · ritual · burning building · foggy pier), NEVER casually mid-scene. A
scene is one style throughout — the whole batch (§"One scene = one batch") is
generated in the scene's declared style. Style is a rendering treatment, never an
excuse for drift: "it looked different because painterly" is a FAILED check.

**Visual FAIL overrides any numerical PASS.** If it looks wrong, it IS wrong.

## 4. Reject-and-regenerate rule

- A shot that fails any check is REJECTED. It is regenerated from the anchor card —
  never "fixed" by editing the failed frame into something the card doesn't show.
- After 3 failed regenerations of the same shot, the shot is CUT or reframed to hide
  the drifting element (e.g., hood stays up, character goes off-camera). A missing
  shot beats a wrong face. Report the cut in the shot log.
- Every rejection is logged: shot id, which character drifted, what drifted, attempt
  number. The log ships with the episode so the owner can see the misses were caught.

## 5. Card-change freeze

Once a scene's batch passes, its cards are FROZEN for that scene. If the owner
approves a new card mid-production (e.g., Theory's robed attire-4, Static's sleeve
logo decision), the new card applies to UNBUILT scenes only — built scenes are not
reopened unless the owner orders it. Note the card version in the shot log.

## 6. Prohibited shortcuts

- NEVER generate a character from a previous EP02 shot instead of the card (drift
  compounds — this is how "alterations between shots" happen).
- NEVER reuse an EP01 frame as a likeness reference (EP01 has known drift; the
  bible's cards are the only anchors).
- NEVER invent an attire. The bible lists every locked attire; anything else needs
  the owner's explicit approval first.
- NEVER drop a signature feature to "simplify" a shot (horns, ears, mask, grin,
  tassels, paint). If a feature can't be rendered, cut the shot.

## 7. Handoff to the visuals worker

The shot log for every scene records: scene id, shot ids, per-shot character +
anchor file, verification result per character, rejection/regeneration count, final
SHA-256 of shipped frames. Reopen the exact shipped bytes after rendering and record
the hash. No artifact bytes = not shipped.
