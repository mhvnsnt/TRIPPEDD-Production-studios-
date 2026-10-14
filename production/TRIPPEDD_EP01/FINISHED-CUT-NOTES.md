# TRIPPEDD EP01 "THE WALK" — Finished Cut Notes (2026-10-14)

**File:** `EP01-THE-WALK-finished.mp4` — 1265.0s (~21:05), 1920x1080, 30fps, h264/AAC 48kHz.
**Review encode (in git):** `EP01-THE-WALK-finished-REVIEW-SMALL.mp4` — 854x480.
**Method:** 20 pieces, each normalized to identical params, concatenated with the
ffmpeg demuxer + stream copy. A/V sync: video 1265.005s vs audio 1264.983s
(0.022s delta, limit 0.1s).

## Segment order (LOCKED_CANON, per EP01-SEGMENTS.md)

| # | Segment | Source | Timecode |
|---|---------|--------|----------|
| 1 | Cold Open | 104606093 [0:00–0:15] (re-cut to avoid Shumafied overlap) | 0.0–15.0 |
| 2 | Motel | 170241977 [0:00–43s] (NOT rotated — verified upright, base-cut note was wrong for this file) | 15.0–58.0 |
| 3 | Shumafied | segments/shumafied/shumafied-seg3-select.mp4 (104606093 @15–28s, the "What does that shit do?" beat) | 58.0–71.1 |
| 4 | Shumafied Disappointment + Cigar Setup | seg4a (104606093 @28–44.4s, green pack + laughter) + seg4b (104742101 full, rotated to landscape, cigar beat) | 71.1–104.7 |
| — | Card | card-black-loti-100pct-more-leprechaun ("Now with 100% more leprechaun") | 104.7–114.7 |
| 5 | Luck of the Irish | 160938849 raw A/B/C (37.4s) + luck-of-the-irish-commercial-final.mp4 (53.4s) | 114.7–205.5 |
| 6 | Cigars / The Walk | 105329690 (259.9s) + 105836936 (75s) + 110016345 (152.6s) + 105955736 (17.4s) | 205.5–710.5 |
| 7 | Bag Sequence | 122211926 [2:00–6:00] | 710.5–950.5 |
| — | Card + Promo | card-well-be-right-back (6s) + goodville-promo-15s_SMART.mp4 (15s) | 950.5–971.5 |
| 8 | Joe | segments/joe/joe-prayer-scene-assembly.mp4 (160.4s, 16 watercolor panels) | 971.5–1131.9 |
| 9 | TV | 170846691 (20.8s, Harry Potter → Naked and Afraid: Shipwrecked) | 1131.9–1152.7 |
| 10 | Clothed and Confused | segments/clothed-and-confused/clothed-and-confused-final.mp4 (66.5s) | 1152.7–1219.2 |
| 11 | Smoking / Hanging Out | 160715990 [0:40–1:20] | 1219.2–1259.0 |
| — | Card | card-stay-trippedd (6s) | 1259.0–1265.0 |

## Verification (own eyes, per deliverable verification law)
- 57 frames sampled across the whole timeline (mid-segment + both sides of every
  transition) — all segments present in locked order, transitions clean, no black
  gaps, no aspect pops. Two dark thumbnails investigated with surrounding frames —
  both normal footage.
- Joe: 16/16 panels watercolor-verified. Clothed and Confused: 8 timeline frames
  + audio check. Shumafied selects: frame-verified.

## Owner calls remaining
- **Lost Acid ending:** NOT included (candidate only, per "do not assume").
- **Clothed and Confused voices:** built with tts backend (Chatterbox weights were
  deleted by disk-guardian); lines in segments/clothed-and-confused/work/narrator_script.txt
  for a Chatterbox re-render if the owner wants it.
- **Goodville Geography gag:** not cut (optional flavor, not a listed gap).
