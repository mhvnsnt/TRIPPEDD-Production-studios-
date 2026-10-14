# KIKO TANAKA — Voice Build
**Based on:** Keiji Mutoh / The Great Muta
**Built:** 2026-10-11
**Status:** Reference secured, clone pending

## The Three-Voice System (owner 2026-10-11)

Kiko speaks like the real Mutoh:
1. **JAPANESE (primary)** — Kiko mostly speaks Japanese, like Tosh from Family Guy. Subtitles in show.
2. **BROKEN ENGLISH (secondary)** — When he speaks English, it's with a heavy Japanese accent, simple short sentences. Like Mutoh's real English.
3. **REAL CLIPS (tertiary)** — Actual Mutoh audio cut from interviews/HOF, used where appropriate.

## Reference Audio

**Source:** Pro Wrestling NOAH interview, Feb 2023 ("I CAN'T FIGHT..." — Mutoh on injuries before final match)
- File: `ref/mutoh-noah-clip.mp3` (60s, 2:00-3:00 excerpt)
- Content: Mutoh speaking Japanese, conversational, clear audio
- Voice: Medium-deep baritone, calm, unhurried, soft-spoken

**Note:** The raspy hissing Muta in-ring voice is a gimmick. This is Mutoh's real speaking voice.

## Voice Characteristics (for cloning)

| Attribute | Detail |
|---|---|
| Pitch | Medium-deep baritone |
| Pace | Unhurried, measured, deliberate |
| Tone | Calm, soft-spoken, thoughtful |
| Language | Japanese primary; English limited/heavily accented |
| English style | Short simple sentences, strong Japanese accent |
| Personality | Quiet confidence, dry humor, deadpan |

## Sample Lines

### Spoken Japanese
- `kiko-jp-robe.wav`: "ローブを見てくれ。いいだろう？" (Check out my robe. It's nice, isn't it?)
- `kiko-jp-fur.wav`: "白い毛皮だ。councilも認めた。" (White fur. Even the council acknowledged it.)

### Spoken English (Japanese accent)
- `kiko-en-robe.wav`: "Check out my robe, guys. It's nice, isn't it?"
- `kiko-en-fur.wav`: "White fur. Very nice robe."

### Sung (pier scene, EP01 3:57-4:05)
- `kiko-sing-jp-robe.wav`: Sung Japanese about robe/moon/night
- `kiko-sing-en-robe.wav`: "Check out my robe..." sung dramatically

**Singing note:** Chatterbox is a speech model, not a singing synthesizer. "Sung" lines use high-exaggeration dramatic delivery (musical-theater heightened speech, à la Rex Harrison). True melodic singing requires a dedicated SVS model (future work).

## Files
- `ref/mutoh-noah-clip.mp3` — 60s reference (Mutoh speaking Japanese)
- `muta-mannerisms.md` — physical mannerisms reference (pre-existing)
- `VOICE.md` — this file

## Build Pipeline
Chatterbox zero-shot clone from `cb_weights` (see `../cipher/render_cipher.py` for pattern).
Cross-lingual: train on Japanese reference, synthesize English with Japanese accent.

## Full Line Scripts

### Spoken Japanese
1. `kiko-jp-robe.wav`: "ローブを見てくれ。いいだろう？"
   Romaji: "Rōbu o mite kure. Ii darou?"
   English: "Check out my robe. It's nice, isn't it?"

2. `kiko-jp-fur.wav`: "白い毛皮だ。会議も認めた。"
   Romaji: "Shiroi kegawa da. Kaigi mo mitometa."
   English: "It's white fur. The council acknowledged it too."

### Spoken English (Japanese accent)
3. `kiko-en-robe.wav`: "Check out my robe, guys. It's nice, isn't it?"
4. `kiko-en-fur.wav`: "White fur. Very nice robe."

### Sung — Pier Scene (EP01 3:57-4:05)
5. `kiko-sing-jp-moon.wav`: "月明かりに、白い毛皮が輝く。誰もいない劇場で、歌う。"
   Romaji: "Tsukiakari ni, shiroi kegawa ga kagayaku. Dare mo inai gekijou de, utau."
   English: "In the moonlight, the white fur shines. In the empty theater, I sing."
6. `kiko-sing-en-robe.wav`: "Check out my robe... in the moonlight... so beautiful... isn't it?"
   (Dramatic musical-theater delivery, High School Musical earnestness)

## VOICE LOCKED (owner 2026-10-11 ~14:55 CDT)
Owner approved all 4 test lines. This is Kiko's canonical voice going forward.

**DO NOT change the vocal identity** unless the owner explicitly says so.
Different ranges, emotions, and delivery styles are fine — but the core
voice (timbre, character, accent pattern) stays locked.

### Lock specs
- Engine: ChatterboxTTS (from_local)
- Weights: ~/workspace/voice-clone-work/cb_weights/ (3.5GB, shared)
- Reference: ref/mutoh-noah-clip.mp3 (60s Mutoh Japanese, NOAH Feb 2023)
- Device: CPU fp32 (fp16 caused dtype mismatch; watermarker patched to Dummy)
- Approved lines: kiko-jp-robe.wav, kiko-en-robe.wav, kiko-jp-fur.wav, kiko-en-fur.wav
