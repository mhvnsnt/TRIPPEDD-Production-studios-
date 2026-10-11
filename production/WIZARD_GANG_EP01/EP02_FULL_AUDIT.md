# EP02 FULL VISUAL + AUDIO AUDIT

**Date:** 2026-10-10
**Auditor:** Subagent (frame-by-frame, 165 frames @ 2s intervals)
**Source:** `wizard-gang-ep02-full-5min.mp4` (330.17s, original master)
**Method:** Every frame visually inspected. Character likeness checked against `EP02_LIKENESS_BIBLE.md`.

---

## PART 1: AUDIO FIX (COMPLETE)

### What was wrong
The previous build (`wizard-gang-ep02-repaired-v1.mp4`):
1. Made the 50s pilot SILENT (dropped its original audio with music/sound)
2. Placed P1/P2 Static lines at 0:23/0:40 — during the pilot
3. Placed all dialogue at ABSOLUTE script times instead of script+50s

### Critical correction applied
Per owner clarification: **ALL DIALOGUE.md timestamps are relative to new-content start (after 50s pilot).** Absolute = script + 50s. The pilot is music/sound only, no voices.

### What was built
`/tmp/ep02-audio-corrected.wav` (48kHz stereo, 330.17s):
- **Pilot audio (0–50.02s):** Restored bit-exact from `ep02-pilot-50s.mp4`. Verified: maxdiff=0, numdiff=0 across 2,400,758 samples.
- **28 dialogue lines** placed at corrected positions (24 Static + Cipher C1/C2/C3 + Sombra H3 + Narrator N1)
- **13 lines** adjusted +0.5–8s to prevent overlap (cascade)
- **Peak:** 29,022 (no clipping, no limiting needed)
- All lines loudnorm'd to -16 LUFS / -1.5 dBTP

### Corrected dialogue map (absolute times)

| Line | Script TC | Abs Start | Abs End | Status |
|------|-----------|-----------|---------|--------|
| P1 (Static) | 0:23 | 1:13 (73s) | 1:21 | Placed |
| P2 (Static) | 0:40 | 1:30 (90s) | 1:35 | Placed |
| N1 (Narrator) | 0:52 | 1:42 (102s) | 1:44 | Placed |
| L1 | 0:56 | 1:46 (106s) | 1:53 | Placed |
| L2 | 1:06 | 1:56 (116s) | 2:04 | Placed |
| L3 | 1:12 | 2:05 (124.58s) | 2:12 | Adjusted |
| L4 | 1:20 | 2:13 (132.64s) | 2:22 | Adjusted |
| L5 | 1:28 | 2:22 (142.18s) | 2:36 | Adjusted |
| L6 | 1:40 | 2:36 (156.16s) | 2:45 | Adjusted |
| L7 | 1:50 | 2:46 (165.70s) | 2:53 | Adjusted |
| H3 (Sombra) | 1:56 | 2:53 (173.28s) | 2:56 | Adjusted |
| L8 | 2:12 | 3:02 (182s) | 3:10 | Placed |
| L9 | 2:22 | 3:12 (192s) | 3:20 | Placed |
| L10 | 2:31 | 3:21 (201s) | 3:31 | Placed |
| L11 | 2:40 | 3:32 (211.86s) | 3:39 | Adjusted |
| L12 | 2:49 | 3:40 (219.68s) | 3:45 | Adjusted |
| L13 | 2:59 | 3:49 (229s) | 3:54 | Placed |
| L14 | 3:08 | 3:58 (238s) | 4:05 | Placed |
| L15 | 3:16 | 4:06 (246s) | 4:12 | Placed |
| L16 | 3:24 | 4:14 (254s) | 4:21 | Placed |
| C1 (Cipher) | 3:26 | 4:22 (261.62s) | 4:30 | Adjusted |
| C2 (Cipher) | 3:31 | 4:30 (270.36s) | 4:35 | Adjusted |
| L17 | 3:33 | 4:36 (275.55s) | 4:46 | Adjusted |
| L18 | 3:42 | 4:47 (286.69s) | 4:54 | Adjusted |
| C3 (Cipher) | 3:52 | 4:55 (294.51s) | 5:02 | Adjusted |
| L20 | 3:58 | 5:03 (302.74s) | 5:14 | Adjusted |
| L21 | 4:14 | 5:14 (314.00s) | 5:21 | Adjusted |
| L22 | 4:38 | 5:28 (328s) | 5:30* | **CLIPPED at video end** |
| N2 (Narrator) | 4:50 | 5:40 (340s) | — | **AUDIO MISSING (never rendered)** |
| L23 | 4:53 | 5:43 (343s) | 5:45 | **NOT PLACED (past video end)** |

*L22 audio extends to 337.36s but video ends at 330.17s — last 7.2s cut off.

### Audio issues remaining
1. **N2 ("Nothing was resolved") was never rendered.** Bill $aber clone exists, N1 done, N2 missing.
2. **L22/L23/N2 need ~15s of additional footage** (see Part 3).
3. Cipher C1 uses `voice-cipher-c1-v3-feral.mp3` (matches "feral 2026 Blackheart" direction).

---

## PART 2: VISUAL AUDIT — SHOT BY SHOT

**Legend:** ✅ PASS (correct 2D cartoon + likeness) · ❌ FAIL (photorealistic/style drift) · ⚠️ MIXED (style clash in frame) · 🔍 LIKENESS (character model violation)

### Pilot (0:00–0:50) — frames 0–25

| Time | Frame | Verdict | Notes |
|------|-------|---------|-------|
| 0–50s | 0–25 | ✅ PASS | Correct 2D cartoon throughout. IT SEES tags, robed figures, Cipher (green jester), Echo (pink), council with Kiko. Style matches Shadow Wizard Money Gang base. |

### S10 "THE SUMMONS" (0:50–1:02) — frames 26–31

| Time | Frame | Verdict | Notes |
|------|-------|---------|-------|
| 52–60s | 26–30 | ❌ **FAIL** | **PHOTOREALISTIC.** Cauldron ritual with realistic human faces (old man with white beard, woman, etc.). These are NOT void-black hoods. Painterly/realistic rendering. Complete style violation. Owner flagged this specifically. |
| 62s | 31 | ✅ PASS | Cut to 2D cartoon lineup. Correct style resumes. |

**Repair needed:** Regenerate frames 26–30 (52–60s) as 2D cartoon. The cauldron/summons scene with 8 robed figures (void hoods) + Kiko's dark fire.

### Council scenes (1:02–1:50) — frames 31–55

| Time | Frame | Verdict | Notes |
|------|-------|---------|-------|
| 62–90s | 31–45 | ✅ PASS | Correct 2D cartoon. Void-black hoods, correct robe colors (red/green/purple/yellow/pink/blue/orange/black). Council lineup and table scenes. |
| 90–100s | 45–50 | ❌ **FAIL** | **PHOTOREALISTIC street crew lineup** (clip-05). Already repaired in separate pass, but present in audited master. |
| 102–106s | 51–53 | 🔍 **LIK
...[truncated 8618 chars]