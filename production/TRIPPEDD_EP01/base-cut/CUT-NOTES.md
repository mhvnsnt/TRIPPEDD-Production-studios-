# TRIPPEDD EP01 "THE WALK" — Base Cut Notes (Review Cut)

**File:** `EP01-THE-WALK-basecut-review.mp4` — 943.9s (~15:44), 854x480 review encode
(~80MB, sized to fit git's 100MB file limit; watchable for editorial review).
**Full-res master (NOT in git):** `EP01-THE-WALK-basecut-master-1080p.mp4` —
1080p30, h264/AAC 48kHz, local at
`~/workspace/.worktrees/ep01cut/production/TRIPPEDD_EP01/base-cut/`.
**Master SHA-256:** `84da81e1845ff01fabc0c18b18818851ed3fd53274c9b2b92d22836acccc8ef1`
**Method:** 14 pieces, each normalized to identical params (1920x1080, 30fps,
yuv420p, h264 ultrafast, AAC 48kHz), concatenated with the ffmpeg demuxer +
stream copy. Review encode: scale 854x480, veryfast crf 34, aac 64k.
Rebuild manifest: `concat2.txt` + `pieces/norm/` (local).
A/V sync verified by sampling across the whole timeline.
**Order:** Immutable, per `docs/creative/EP01-THE-WALK-CANON.md`. Footage chronology
was NOT used to determine order.

## Per-segment source mapping

| # | Segment | Source | Notes |
|---|---------|--------|-------|
| 1 | Cold Open | `VID_20260906_104606093.mp4` [0:00–0:44] | Two outside room 226, laughing/talking. Strongest opening energy. |
| 2 | Motel | `VID_20260906_170241977.mp4` [0:00–0:43] | Motel 6 lobby, "Book Faster" signage. **Fix:** source was recorded upside-down (phone flipped); rotated 180° in the cut. |
| 3 | Shumafied | SLATE — material not found | **UNRESOLVED.** No visual or audio confirmation of the pack/device bit in any of the 17 clips. |
| 4 | Shumafied Disappointment + Cigar Setup | SLATE — material not found | **UNRESOLVED.** "This thing's not doing shit" not found in audio. The store run (segment 6) is documented but the decision beat is not. |
| 5 | Luck of the Irish | `VID_20260906_160938849.mp4` (full 0:37) — **FOUND IN FOOTAGE.** Shot A [0:00–0:12]: far/slow-zoom, Person A chilling on the motel balcony. Shot B [0:12–0:30]: closer angle, suspense, on phone; "Look at the Irish." audio at ~0:18. Shot C [0:30–0:37]: fourth-wall break, direct to camera. Assembled A→B→C per CLAUDE.md (recorded A,C,B; ad runs A,B,C). The GREEN IRIS effect was NOT observed in these frames — remains a visual-inspection target (do not mark found). |
| 6 | Cigars / The Walk | `VID_20260906_105329690.mp4` (full 4:20) + `VID_20260906_105836936.mp4` (store, zigzag purchase) + `VID_20260906_110016345.mp4` (2:33 B-roll) + `VID_20260906_105955736.mp4` (0:17 bridge) | The walk backbone: parking lot → street → bank → Goodlettsville storefront → convenience store. |
| 7 | Bag Sequence | `VID_20260906_122211926.mp4` [2:00–6:00] | Person C (straw hat, dashiki, towel) with bags on stairs; heated exchange with Person A; duffel/suitcase close-up. Transcript is noisy (overlapping speech) — the "What's wrong with you?" exchange lands ~0:53–1:17 in the source. |
| 8 | Joe | SLATE — produced segment | Per canon: 2D reconstruction, no footage exists. Exact 2D style not recorded — owner call before building. |
| 9 | TV | `VID_20260906_170846691.mp4` (full 0:21) | Harry Potter on wall-mounted TV, Person B on bed reacting/gesturing. Channel-change and survival material not in the clips. |
| 10 | Clothed and Confused | SLATE — produced segment | Realistic Naked-and-Afraid parody — produced, not base footage. |
| 11 | Smoking / Hanging Out | `VID_20260906_160715990.mp4` [0:40–1:20] | Balcony, afternoon, Person A to camera. Closer energy. |

## What the transcripts revealed

All 17 clips transcribed with local Whisper (base model on 6 clips, tiny on 11 —
VM load forced the switch; noisy phone audio throughout).
- **No "shumafied," "pack/device," "cigar decision," or "this thing's not doing shit"**
  found in any transcript (keyword scan across all 17). Segments 3–4 stay unresolved.
- Store clips confirm the supply run (zigzags purchased in `105836936`).
- `160938849` [0:18–0:33]: "Look at the Irish" — Luck of the Irish raw material.
- Bag-sequence audio is heavily overlapped; transcript is unreliable there — the
  visual select (stairs/bags/argument) is the authority.
- Two clips unusable: `105110928` (camera covered), `160926393` (1.3s blip).

## Unresolved / owner calls

1. **Segments 3–4 (Shumafied + Disappointment):** no footage or clean audio found.
   Options: owner points at the material, or these become produced/VO-driven beats.
2. **Joe 2D style:** not recorded — owner call before building the reconstruction.
3. **Lost Acid ending:** candidate only; no footage tied to the acid search.
4. **Goodville Geography:** `105329690` ~2:50 Goodlettsville storefront is the
   documentary-gag candidate; placement not locked.

## Verification

- 28 frames sampled across the WHOLE cut (2 per segment + slate checks),
  extracted with output seeking from the final MP4 — content and order confirmed
  against the locked segment table. Per AGENTS.md "my eyes on every deliverable":
  every segment was visually re-opened from the final bytes.
- Audio present and synced throughout (AAC 48kHz, carried from sources).
- Slate cards mark produced/unresolved segments explicitly — no silent gaps.
- LOTI segment: Shot A (far, ~0:05), Shot B (closer, ~0:15), Shot C (fourth-wall
  break, ~0:33) confirmed in the assembled segment-5 window (95.0–132.4s).
