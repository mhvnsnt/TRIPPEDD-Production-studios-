# Production checklist — WIZARD_GANG_SHORT_01

## Pre-production (before the approval gate)

- [ ] Storyboard stills/key art for shots 1–9 assembled from ASSET_MAP.md
- [ ] swmg-red fix pass completed (mouth removed; eye glints only) OR owner-directed alternate
- [ ] Sombra Negra render brief drafted (black robe, purple trim/edges, buried face, white eye glints, full arm reach, void-white version)
- [ ] Narrator render brief drafted (purple robe, void-black face, eye glints, diamond-grill smile, blonde braids, gold chains, full arm reach, void-white version)
- [ ] Hollows night rooftop key art brief drafted (shot 1)
- [ ] No placeholder text anywhere; title cards "WIZARD GANG" / "TRIPPEDD" only; missing billing = "parts unknown"
- [ ] **OWNER GATE 1 — storyboard + key art approved.** No production without it.

## Asset gates

- [ ] Robed GLBs exist and are verified loaded at runtime (or owner approves staged-stills v1 method — see MOCAP_PLAN.md)
- [ ] Rig/skin/deformation evidence clean per character
- [ ] Real mocap sourced per MOCAP_PLAN.md (Mixamo clip IDs + CMU takes recorded in runbook.json)
- [ ] Retarget verified on the universal retargeter or approved fallback — no procedural motion

## Evidence gates (from UNIVERSAL_ENTRANCE_VIDEO_KIT.md — a character video is READY only if)

- [ ] 1. The actual intended game/build was rendered
- [ ] 2. The intended character asset was actually loaded at runtime
- [ ] 3. Rig/skin/deformation evidence is clean
- [ ] 4. Every move/effect shown exists in that build or is explicitly marked production-only
- [ ] 5. No other game's branding, UI, arena or character data leaked into the cut
- [ ] 6. No placeholder canon data appears
- [ ] 7. Audio has been listened to/checked
- [ ] 8. Source build, model, timeline and output hashes are recorded

## Editorial gates

- [ ] Timeline cues authored as timestamps (TRON/PYRO/SMOKE/LIGHT/CAMERA/MUSIC/HOLD)
- [ ] Title cards: "WIZARD GANG" + "TRIPPEDD" ident, canon-locked text only
- [ ] "SWMG" appears only on pendant jewelry; never as on-screen text or billing
- [ ] Purple robe appears on the Narrator only (no Theory in SHORT 01 until the ambiguity is resolved)
- [ ] The Narrator has no spoken line (voice pending owner recording)
- [ ] 9:16 master + 16:9 + 1:1 + thumbnail/still + captions exported
- [ ] Provenance manifest + SHA-256 checksums recorded
- [ ] Metadata block (README.md) preserved through the pipeline — never flattened into generic "TRIPPEDD content"

## Post gates

- [ ] **OWNER GATE 3 — final review.** Blocking.
- [ ] On approval: commit, hash, push. Recurring-segment variants (10–20s bumper cut) generated from the same master with `recurringKey: WIZARD_GANG`.
