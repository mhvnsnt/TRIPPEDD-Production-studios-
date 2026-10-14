# Dangly voice v2 — build notes

**Policy (owner): NEVER clone John Dunsworth (d. 2017).**
Style-alike parody scratch voice only — no real person's voice was copied at any point.

## What was built

- **Base voice:** ElevenLabs premade stock voice "Bill — Wise, Mature, Balanced"
  (`pqHfZKP75CvOlQylNhV4`, category=premade, labeled old male, American).
  Synthetic stock voice; not a real person. No clone, no sample-based anything.
- **Model:** `eleven_v3` (delivery-direction audio tags).
- **Ranges** (three direction presets on the same base voice):
  - `drunk` — default old-head mode: `[slurred, drunkenly, grandiose]`, stability 0.30, style 0.70
  - `sober` — scheming mode: `[quietly, menacingly, deliberate]`, stability 0.55, style 0.45
  - `calm` — coherent mode: `[warmly, gently, thoughtfully]`, stability 0.70, style 0.30

## Lines (canonical, owner-dictated)

1. `line1_ive-seen-some-things` — "I've seen some things..."
2. `line2_dinosaur-story` — "One time... I saw a guy in traffic, he beat up a dinosaur,
   ripped its head off, did ungodly things, unspeakable.."

Files: `dangly_{range}_{line}.mp3` × 6 (2.3–14.3s each, verified non-silent via ffprobe/volumedetect).
Manifest: `dangly_voice_manifest.json` (voice ID, settings, directed texts, byte sizes).

## Regeneration

`build_dangly_voice.py` in this directory — rerunnable (needs the `custom.elevenlabs` credential).
NOTE: ElevenLabs **Voice Design** (description → new voice) is paid-plan-only on this
account, so v2 uses a stock base voice + delivery tags instead of a designed voice.
If the account ever gets a paid tier, redo with description-based design per
`production/TRIPPEDD_EP01/reference/goodville/lahey-voice-study.md` §5.

## Status

SCRATCH / STAND-IN. Human performance (Tyneshia considering) replaces this wherever
possible; generated style-alike only where a human isn't available. Owner signs off
at final mix.
