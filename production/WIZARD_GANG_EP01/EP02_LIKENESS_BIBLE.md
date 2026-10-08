# WIZARD GANG — EP02 LIKENESS BIBLE (master)

**Owner-locked 2026-10-07 · production truth for every EP02 shot.**
One character = one face, one body, every shot. Any generated shot where a character
drifts from this bible is REJECTED and regenerated — never shipped.

**Canonical show canon (all characters):**
- Robed = hood UP, face is a BLACK VOID with two white eye glints. EXCEPT Ashes:
  his DIAMOND-GRILL GRIN shows in every style, robed or unrobed.
- Robe colors (LOCKED): Ashes scarlet · Onyx green · Theory purple · Cipher yellow ·
  Echo pink · Static deep blue · Hollow orange · Sombra Negra black robe/purple trim ·
  Kiko Tanaka white fur trim.
- Name pendants (canon-locked text): ASHES · ONYX · THEORY · CIPHER · ECHO · STATIC ·
  HOLLOW · KIKO. Sombra Negra wears a SKULL pendant. Never "SWMG" as text on screen.
- The Narrator is VOICE-ONLY. No purple-robed figure on screen, ever.
- **GLB rule (owner 2026-10-07): the card art, the attire refs, AND the 3D GLB must all
  describe ONE person.** A GLB that doesn't look like the card is a defect. Each
  character section below lists its GLB anchor(s) with a MATCH / DEFECT / MISSING
  verdict against the card. On any GLB-vs-card conflict, THE CARD WINS — the card is
  the owner's hand-picked likeness; the GLB is repaired or its defective part is
  banned from use. See `EP02_IDENTITY_PROTOCOL.md` §2 for the enforcement procedure.
- S19 (EP2 onward): NO duplicate characters in one scene — no two copies of the same
  robe color, no robed + unrobed version of the same person standing together.
  The S11 "street crew vs robes" wink is ONE sanctioned beat per the storyboard —
  the street crew there reads as the same people, not duplicates, and the camera
  cuts away (never stated, never explained).

## Art styles (owner 2026-10-07)

- **Base = CARTOONY** — the Shadow Wizard Money Gang meme look. The show's home base.
  Style refs: `assets/wizard-gang-style-refs/cartoonier/`.
- **Painterly/detailed SOMETIMES** — at flagged dramatic beats only (EP01 grammar:
  the flare, the ritual, the burning building, the foggy pier). Style refs:
  `assets/wizard-gang-style-refs/detailed/`.
- **Likeness holds in BOTH styles.** Style is a rendering treatment, NEVER a redesign:
  the same face, same body, same attire details, same robe color, same pendant, same
  signature features (horns, ears, mask, grin, paint, tassels) in cartoony AND in
  painterly. A painterly shot where Cipher's tattoos vanish is a drift defect, not a
  "style choice."
- The anchor cards may be cartoony or detailed — the CHECKLIST (face · body · attire ·
  robe · pendant · signature features) is style-agnostic. See `EP02_IDENTITY_PROTOCOL.md`
  §3 for the style-switch rule.

**Anchor files:** full path under `production/WIZARD_GANG_EP01/character-refs/`.

---

## 1. ASHES / BUFFALO BILL

| | |
|---|---|
| Robe | SCARLET · gold $ pendant · black void face + DIAMOND-GRILL GRIN |
| Identity anchor (robed) | Series canon: owner-supplied art style refs (`assets/wizard-gang-style-refs/`) — scarlet robe, grin visible in the hood. |
| Unrobed anchor | `ashes/ashes-street-34.png` + `ashes-street-front.png` (owner-made Tripo GLB screenshots) |

**Likeness:** Black man, heavy muscular build. **Large curled ram horns** — signature,
never dropped. Braided hair with beads hanging beside the horns. Tribal tattoos on
chest, shoulders, arms. Short beard. The diamond-grill grin shows in EVERY form.

**Attires (both locked):**
1. Unrobed 1 "street": black t-shirt, layered gold chains, black jeans, black boots.
2. Attire 2 "horned": shirtless, black cargo pants, barefoot.

**GLB anchor:** owner-made Tripo GLBs — MATCH (the in-repo screenshots ARE renders of
them; horn shape, braid/bead layout, tattoo placement, and grin all match the cards).
No .glb bytes in the workspace — the screenshots above are the filed GLB evidence.
If the .glb files land in-repo, re-verify against the screenshots before use.

**Drift hazards:** horns disappearing/reshaping · beard vanishing · grin replaced by
generic smile · horns on the wrong head position.

---

## 2. ONYX

| | |
|---|---|
| Robe | GREEN · ONYX pendant · black void face, eye glints |
| Identity anchor (robed) | Owner GLB screenshots: `onyx/onyx-glb-blackhair.png`, `onyx/onyx-glb-greenhair.png` |
| Unrobed anchor (face) | `onyx/onyx-glb-blackhair.png` — the locked clown face |

**Likeness:** Black woman, full-figured. **Full white clown face paint — the locked face:**
black teardrop/diamond markings around the eyes, black nose, large black mouth/smile
region, small black forehead mark. Layered chokers/necklaces. **This face is identical
across every anchor and every GLB — it is the single source of truth for her face.**

**Attires (ALL FIVE LOCKED):**
1. Corset (Attire 1): black hair, voluminous wavy with side coils; black/white studded
   corset bodysuit; studded arm guards; studded knee-high boots. → `onyx-corset-front.png`
2. Green hair (Attire 2): neon green long straight hair; white-dominant corset top with
   black tribal/graffiti print; spiked sleeves/arm guards; printed briefs. → `onyx-base-front.png`
3. Street (LOCKED): neon green hair; black/white striped skull graphic sweatshirt;
   baggy dark cargo jeans with cross prints; crossbody bag; black/white sneakers. → `onyx-street-front.png`
4. Straightjacket (LOCKED): dark hood/hair; black vinyl buckled top; pleated black mini
   skirt; neon-yellow web-pattern stockings; chunky platform boots. → `onyx-straightjacket-front.png`
5. Bomber (LOCKED, owner-supplied): green hair; black/green bomber jacket; layered gold
   chains; black jumpsuit. → `onyx-attire-bomber.png`

**GLB anchors (all MATCH the card — face, build, attire):**
| GLB | Attire | Verdict |
|---|---|---|
| `~/workspace/bannon-repair/out/ONYX_corset_repaired.glb` | 1 (blackhair) | MATCH |
| `~/workspace/bannon-repair/assets/models/ONYX.glb` | 2 (greenhair) | MATCH (minor leg-print coverage note, same print family) |
| `~/workspace/bannon-repair/out/ONYX_street_repaired.glb` | 3 (street) | MATCH |
| `~/workspace/bannon-repair/out/ONYX_straightjacket_repaired.glb` | 4 (straightjacket) | MATCH |

Non-repaired variants (`ONYX_corset.glb`, `ONYX_straightjacket.glb`, `ONYX_street.glb`)
exist but are SUPERSEDED — never use them. All four locked GLBs carry the same locked
clown face as the cards: GLB, card, and attire refs describe ONE person.

**Drift hazards:** clown face paint changing pattern between shots · hair color swapping
mid-scene · build changing (she is full-figured, never slimmed).

---

## 3. THEORY

| | |
|---|---|
| Robe | DEEP PURPLE, gold celestial embroidery (moons, stars, runes) on hood/collar/cuffs · gold THEORY pendant + crescent-moon/compass charms · black void face, eye glints |
| Identity anchor (robed) | `theory-attire-4/theory-attire4-robed.png` — **APPROVED owner 2026-10-07** (replaces the old chibi-style robed Theory; the blurred shoulder-patch text is accurate to her likeness) |
| Unrobed anchor (face) | `theory-unrobed/theory-face-front.png` + `theory-face-34.png` — the face and the blue-purple cat-ear headpiece are law |

**Likeness:** Black woman, ~20s, warm brown skin. Medium-length dark locs past the
shoulders with beads/charms (attire 1). **Blue-purple cat-ear headpiece** (large pointed
ears, iridescent blue/violet, pink inner ear) — signature, never dropped (attire 1).
Septum nose ring. Full lips, soft features. **Same face across every attire** (S18).

**Attires (LOCKED):**
1. Unrobed 1: black star-print crop top with mesh panels; fishnet midriff; star-print
   mini skirt over fishnet leggings; layered black beads/choker with ring; platform
   boots; cat-ear headpiece. → `theory-unrobed/theory-front.png`
2. Unrobed 2 "caped dominatrix" (owner-supplied): SHORT twisted locs pinned up, round
   dark sunglasses, floor-length RED cape with high collar, black leather bodysuit with
   strappy chest cutout, opera gloves, studded belt with red trim, leather pants,
   knee-high heeled boots. → `theory-attire-2/theory-attire2-full-front.png`
3. Attire 3 (owner: "Perfect, yes. Save that as attire three."): attire 1's EXACT head
   (medium locs, NO glasses) on attire 2's cape/leather body. → `theory-attire-3/theory-attire3-final.png`
   (⚠️ the rejected long-haired sunglasses v1 is DEAD — never regenerate or reuse it)

**GLB anchor:** owner-supplied GLB screenshots (attires 1 and 2) — MATCH (the filed
screenshots ARE the GLB evidence; face, ears, and attire details match the cards).
No .glb bytes in the workspace; attires 3 and 4 are generated images with no GLB.
If .glb files land in-repo, verify them against the cards before use.

**Drift hazards:** cat ears shrinking/disappearing · locs lengthening or changing color ·
sunglasses appearing on attire 1/3 · face drifting to a generic face between attires.

---

## 4. CIPHER

| | |
|---|---|
| Robe | YELLOW · CIPHER pendant · black void face, eye glints |
| Identity anchor | `cipher/cipher-base-front.png` (Base Blackheart) — bald, manic grin, tattooed |

**Likeness:** based on Lio Rush's 2026 BLACKHEART persona (owner-locked). Feral, zoned-out,
manic — whisper-to-shriek. Voice motifs: "No no no…", "He sees you.", "He knows.",
"The cuts…", "The rain…", "WE…". The generic speedster voice set is DEAD.

**Attires (ALL FOUR LOCKED — owner: "I want all."):**
1. Feral: bald, heavy brow, wide feral grin, moth chest tattoo, arm-sleeve tattoos,
   abdomen script; feral crouch; black trunks, knee pads, boots, wrist tape. → `cipher-feral-v2-front.png`
2. Minion: white/black face paint, styled hair, tattooed torso/arms, heart pendant,
   black patterned tights, wrist tape. → `cipher-minion-front.png`
3. Base Blackheart: bald, manic grin with dark mouth (Blackheart liquid), tattooed
   torso/arms, black trunks, knee pads, boots with emblem. → `cipher-base-front.png`
4. Card suit (owner-supplied): bald Black man, GOLD GRILL, nose ring; black leather
   jacket + pants COVERED in playing-card faces; layered gold chains, bracelets, rings.
   → `cipher-attire-cardsuit.png`

**GLB anchors:**
| GLB | Attire | Verdict |
|---|---|---|
| `~/workspace/bannon-repair/out/plateau/CIPHER_feral_v2.glb` | 1 (feral) | MATCH |
| `~/workspace/bannon-repair/out/CIPHER_minion_repaired.glb` | 2 (minion) | MATCH |
| `~/workspace/bannon-repair/out/CIPHER_repaired.glb` | 3 (base Blackheart) | MATCH |

`CIPHER_feral.glb` and `CIPHER_rigged.glb` FAIL to render (Blender 4.0.2 rejects
EXT_meshopt_compression) — unverifiable = DEFECT, banned from use. No GLB exists for
the card-suit attire (owner-supplied image is the anchor).

**Drift hazards:** losing the feral grin to a calm face · tattoos vanishing between
shots · the dark mouth/Blackheart-liquid reading as "dirty" instead of intentional.

---

## 5. ECHO

| | |
|---|---|
| Robe | PINK · ECHO pendant · black void face, eye glints |
| Identity anchor (face) | `echo/echo-attire-pinkjacket.png` — **face reference = Shotzi Blackheart** (owner 2026-10-07). Echo has THREE canon face variants — the possessed black-mist-mouth GLB face, the clean Shotzi face, and the pink-jacket clean face. See below. |
| Identity anchor (body) | Same file — long green hair, tattoo sleeves, choker. |

**Likeness:** Shotzi Blackheart face. Long straight GREEN hair. Athletic build. Full
tattoo sleeves on both arms, chest tattoo, leg tattoo. Black choker at the neck.
Dark fingers (black polish/claws). Physical mimic — copies movements (the claw machine).
Speaking style UNKNOWN — visual-only until owner locks a voice.

**Attires (LOCKED):**
1. Base (GLB): black studded corset bodysuit, studded belt/briefs, black boots.
   → `echo/echo-base-front.png` (body only — face anchor is the pink-jacket image)
2. Pink jacket (owner-supplied; owner: "really nice and unique"): pink cat-ear hoodie
   COVERED in patches, worn open with NO shirt (tattooed torso visible, hair coverage);
   black cargo pants with patches; black boots. → `echo/echo-attire-pinkjacket.png`

**GLB anchor:** `~/workspace/bannon-repair/out/ECHO_repaired.glb` — **FACE VARIANTS, not defect (owner 2026-10-07).** Echo's GLB face (the possessed-looking black-mist mouth) is CANON VARIANT 1. The card's clean Shotzi face is CANON VARIANT 2. The pink-jacket clean face is CANON VARIANT 3. Face variance between these three is INTENTIONAL — never flag it as drift. GLB body is a valid body/pose donor.

**Drift hazards:** green hair turning black/brown · tattoos vanishing on the pink-jacket attire · using a face that is NONE of the three canon variants.

---

## 6. STATIC

| | |
|---|---|
| Robe | DEEP BLUE · STATIC pendant · black void face, eye glints |
| Identity anchor | `static/static-base-front.png` — bleached-blond messy hair, dark full beard |
| Voice | Enzo Amore clone (ONLY voice in the EP02 mix until script approval) |

**Likeness:** light skin, BLEACHED-BLOND messy medium-length hair, DARK FULL BEARD.
Muscular, tattooed torso and arms. Same head/face on every attire — consistent.

**Attires (ALL THREE LOCKED):**
1. Base (GLB): black/white vertically striped shorts with heart-"1" emblem and "G"
   waistband; black arm sleeves; "e"/"a" knee pads; black/white boots. → `static-base-front.png`
2. Alt (GLB): split shorts (white snakeskin with black "R" / black with white crowned
   "A"); mismatched arm sleeves; "SINCE"/"S.MZE" knee pads; gold sneakers. → `static-alt-front.png`
3. Tactical (owner-supplied): black leather jacket with BLUE ELECTRIC accents; black
   tee; tactical belt/holsters; knee pads; fingerless gloves; black boots. → `static-attire-tactical.png`

**GLB anchors (both MATCH — same head/face on both, consistent):**
| GLB | Attire | Verdict |
|---|---|---|
| `~/workspace/bannon-repair/out/STATIC_repaired.glb` | 1 (base) | MATCH |
| `~/workspace/bannon-repair/out/STATIC_alt_repaired.glb` | 2 (alt) | MATCH (sleeve logo pending owner decision — see below) |

Non-repaired `STATIC.glb` / `STATIC_alt.glb` are SUPERSEDED — never use them.

**Sleeve logo — RESOLVED (owner 2026-10-07):** the alt's black arm sleeve carries **"S.A.W.F.T."** in white script (owner: "Perfect"). The old "Supreme"-style script is retired — never regenerate it. Alt-attire reference: `static/static-alt-sawft-preview.webp`.

**Drift hazards:** beard thinning/disappearing · hair darkening · the sleeve logo
morphing into gibberish script.

---

## 7. HOLLOW

| | |
|---|---|
| Robe | ORANGE · HOLLOW pendant · black void face, eye glints |
| Identity anchor (mask) | `hollow/hollow-attire-dragon.png` — the Super-Dragon mask (owner: matches approved likeness) |
| Identity anchor (body) | `hollow/hollow-base-front.png` |

**Likeness:** Super Dragon likeness. **FULLY MASKED — the face is never visible.**
Black lucha mask with jagged white shark-tooth mouth, pointed ear protrusions, blue
trim + hanging tassels; long black hair/dreadlock-like strands hang from the mask
sides. Tall, lean-muscular. Mostly SILENT (owner hasn't found the voice) — visual-only,
always mid-recruiting-pitch. **No exposed-face likeness risk.**

**Attires (BOTH LOCKED):**
1. Base: black full-body suit with white serpent/dragon chest emblem; white accent
   panels under the arms. → `hollow-base-front.png`
2. Dragon (owner-supplied): BLACK LONG-SLEEVE rashguard with blue dragon print; black
   kung-fu pants with blue dragon embroidery; black boots. → `hollow-attire-dragon.png`

**GLB anchor:** `~/workspace/bannon-repair/out/HOLLOW_repaired.glb` — MATCH (fully
masked; mask pattern, serpent emblem, and build match the cards). Non-repaired
`HOLLOW.glb` exists but is SUPERSEDED — never use it.

**Drift hazards:** mask pattern changing between shots · face appearing under the mask
· hair strands vanishing.

---

## 8. SOMBRA NEGRA

| | |
|---|---|
| Robe | BLACK robe with PURPLE trim · SKULL pendant · black void face, eye glints |
| Identity anchor | `sombra-negra/sombra-negra-base-front.png` |
| Voice | Damian Priest likeness — SPEAKS (1 line in EP02, pending script approval) |

**Likeness:** white face paint/mask, RED eyes, long black hair worn back. Tall,
muscular. Skeleton-ribcage vest (white ribs on black), pendant necklace, black pants,
black boots with straps, black/white wristbands.

**⚠️ Owner-verified outfit detail:** the dark angular shards behind his thighs are
LOOSE PARTS / TASSELS on his tights — INTENTIONAL, part of the outfit. They need
INDIVIDUAL RIGGING (separate bones/weights). Never "fixed" or removed.

**GLB anchor:** `~/workspace/bannon-repair/assets/models/SOMBRA_NEGRA.glb` — MATCH
(white face, red eyes, ribcage vest, tassels all match the card). Notes: the GLB
faces -Y in Blender space (every other character GLB faces +X) — flag for the
rig/animation pipeline. The GLB contains junk environment geometry (Object_42,
Object_4) that is NOT part of the character — exclude from renders, never from the
character. No `_repaired` variant exists.

**Drift hazards:** red eyes turning normal · thigh tassels deleted as "defects" ·
ribcage vest pattern changing.

---

## 9. KIKO TANAKA

| | |
|---|---|
| Robe | WHITE with FUR trim · KIKO pendant · black void face, eye glints |
| Identity anchor (masked) | `kiko/kiko-masked.png` — silver/black segmented mask, mature heavyweight build |
| Identity anchor (unmasked) | `kiko/kiko-unmasked-older.png` — older Mutoh, short dark hair, lined face |

**Likeness:** OLDER Keiji Mutoh / Great Muta ONLY. Young versions are REJECTED —
never generate or use them.

**Canon versions (from `~/workspace/ashlane-art/kiko-cards/`):**
1. Masked (primary): silver/black segmented mask, mature heavyweight build, white pants
   with black trim, black boots — the classic Muta look. → `kiko-masked.png`
2. Masked (alt): red/black horned demon mask, red tribal tattoos, black pants with red
   trim. → `kiko-masked-horned-alt.png`
3. Unmasked (older): older Mutoh, short dark hair, mature lined face, black singlet,
   black tights, boots. NO face paint. → `kiko-unmasked-older.png`

**⚠️ NO KIKO GLB EXISTS anywhere in the repos (swept 2026-10-07).** The cards above
are the likeness anchors for EP02 generation until a model is built. GLB status:
MISSING (not a defect — a gap). If a Kiko GLB is generated or supplied, it must be
verified against these cards BEFORE it becomes an anchor — an older-Mutoh mismatch
is a defect.

**Drift hazards:** young Muta face appearing (banned) · mask design changing between
shots · unmasked face gaining paint.

**Drift hazards:** young Muta face appearing (banned) · mask design changing between
shots · unmasked face gaining paint.

---

## GLB-vs-card verdicts (owner 2026-10-07: a GLB that doesn't look like the card is a defect)

| Character | GLB anchor(s) | Verdict |
|---|---|---|
| Ashes | Owner Tripo GLBs (screenshots filed) | MATCH |
| Onyx | 4 repaired GLBs (attires 1–4) | MATCH × 4 |
| Theory | Owner GLB screenshots (attires 1–2) | MATCH |
| Cipher | feral_v2 / minion_repaired / repaired | MATCH × 3 |
| Cipher | `CIPHER_feral.glb`, `CIPHER_rigged.glb` | DEFECT — render failure (meshopt), unverifiable, banned |
| Echo | `ECHO_repaired.glb` | **3 canon face variants** — possessed black-mist-mouth (GLB), clean Shotzi (card), pink-jacket clean; variance between them is intentional, not drift |
| Hollow | `HOLLOW_repaired.glb` | MATCH |
| Sombra Negra | `SOMBRA_NEGRA.glb` | MATCH (tassels intentional; -Y orientation flagged) |
| Static | `STATIC_repaired.glb`, `STATIC_alt_repaired.glb` | MATCH × 2 |
| Kiko | none | MISSING (gap, not defect — cards only until a GLB is verified) |

## Bible gaps (flagged, not hidden)

1. **Kiko has no GLB** — generation anchors are 2D cards only.
2. **Cipher's feral/rigged GLBs are banned** — unverifiable render failures.
3. **Ashes' .glb bytes aren't in-repo** — screenshots are the filed GLB evidence.
4. **Card-suit Cipher has no GLB** — the owner-supplied image is the anchor.

## Card → shot binding (see EP02_IDENTITY_PROTOCOL.md)

Every shot lists its characters and the anchor file for each. The generator prompt for
a character cites the anchor file BY NAME. Verification is visual: the checker opens
the anchor card and the shot frame side by side and confirms face/body/attire/pendant
before the shot ships. Visual FAIL overrides any numerical pass.
