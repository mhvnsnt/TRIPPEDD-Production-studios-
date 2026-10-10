# WIZARD GANG Ep1 "THE SUMMIT" — Music Manifest

**Scored block:** 0:50–5:00 (S10–S29; the 0:00–0:50 cold open reuses the pilot's existing soundscape).
**Total music:** 20 per-scene stems + 1 full show mix (250.14s ≈ 4:10).
**Format:** 44.1 kHz / 16-bit / stereo WAV. Mixed as beds under dialogue — peaks
capped at −5.2 dBFS (0.55) or lower, RMS −17 to −23 dBFS, so Static's lines and the
VO-pending Narrator lines have clear headroom. Smash-cut transitions between the
13 Act-2 beats (0.42s whoosh-hits) follow the episode's Adult Swim hard-cut grammar.

## Source / license — every stem

| Stem | Source | License |
|---|---|---|
| ALL 20 stems + full mix | **100% original code synthesis** — every note, drum, and texture generated at render time by `compose_ep01_music.py` (numpy oscillators, Karplus-Strong plucks, filtered-noise beds). No samples, no loops, no third-party audio, no soundfonts. | TRIPPEDD original work — all rights held by the production. Zero third-party material = zero clearance risk. |

**Hybrid-direction note:** the owner's standing direction allows open-source
samples/loops combined with code synthesis. After review, this episode was built
with the code-synthesis half only: pulling in external loop packs would have
introduced provenance risk for zero creative gain on a dialogue-bed score.
If a future episode wants sampled texture, sources will be documented per-stem here.

**Originality QC:** all melodies, basslines, chord voicings, and motifs were
composed for this episode in the script (see "Musical notes" per stem below).
No quoted or recognizable existing melodies; the carnival waltz (S24) and
chiptune lead (S15) are original minor-key lines, not public-domain tunes.

## Stems

| # | File | Timecode | Dur | Peak | RMS | Musical notes |
|---|---|---|---|---|---|---|
| S10 | `s10_the_summons.wav` | 0:50–1:02 | 12.0s | 0.550 | 0.131 | D-drone sub-bass flare, wind bed, heartbeat kick pairs, rising 16th-note tom roll, slam into S11 |
| S11 | `s11_the_meeting.wav` | 1:02–1:18 | 16.0s | 0.500 | 0.133 | Solemn 72bpm taiko pattern under the ritual; drums die at 13.5s when the candle gutters out |
| S12 | `s12_order_of_business.wav` | 1:18–1:38 | 20.0s | 0.500 | 0.093 | 100bpm roll-call snare cadence; 8 low stabs (one per name); sub-hit on Ashes' declaration; dice-rattle hint |
| S13 | `s13_the_derail_begins.wav` | 1:38–2:10 | 32.0s | 0.500 | 0.153 | Solemn pad decays → warm 90bpm cookout boombap, grill-sizzle bed, comedic bass fill into Act 2 |
| S14 | `s14_dice_game.wav` | 2:10–2:20 | 10.0s | 0.500 | 0.115 | Tense 96bpm swing groove, original minor riff; dice shaker roll; rimshot on the aces |
| S15 | `s15_arcade.wav` | 2:20–2:30 | 10.0s | 0.450 | 0.078 | Original 128bpm chiptune bounce (square arp, original melody); claw-servo blips; plushie-win sparkle |
| S16 | `s16_basketball.wav` | 2:30–2:39 | 9.0s | 0.500 | 0.136 | 92bpm 90s hoop bounce; synth whistle accents; ball-bounce thumps |
| S17 | `s17_bodega.wav` | 2:39–2:48 | 9.0s | 0.450 | 0.119 | 84bpm lo-fi stroll, vinyl crackle, original jazzy loop |
| S18 | `s18_night_market.wav` | 2:48–2:58 | 10.0s | 0.500 | 0.135 | 80bpm sway groove; ominous low pulse + detuned shimmer when the IT SEES tag glows (~6.5s) |
| S19 | `s19_subway.wav` | 2:58–3:07 | 9.0s | 0.500 | 0.116 | Train-chug 8ths at 100bpm, driving bass, rail-clack accents |
| S20 | `s20_bridge.wav` | 3:07–3:15 | 8.0s | 0.450 | 0.091 | 70bpm tense sparse pizz (Karplus-Strong) over low pad — the "classified exchange" |
| S21 | `s21_parking_garage.wav` | 3:15–3:23 | 8.0s | 0.420 | 0.073 | 66bpm minimal spy-ish pulse; muted kick, sparse plucks |
| S22 | `s22_skate_park.wav` | 3:23–3:32 | 9.0s | 0.520 | 0.110 | 140bpm pop-punk-ish bounce (original riff); crash at the failed trick (~6.9s); one comedic low "womp" |
| S23 | `s23_studio.wav` | 3:32–3:41 | 9.0s | 0.500 | 0.092 | 100bpm talk-show bounce with claps; mic-feedback squeal at the hijack (~6.9s) |
| S24 | `s24_carnival.wav` | 3:41–3:51 | 10.0s | 0.450 | 0.144 | Dark original A-minor calliope waltz (3/4); music stops DEAD at 8.3s for Sombra's stone face |
| S25 | `s25_grill_incident.wav` | 3:51–3:57 | 6.0s | 0.550 | 0.105 | Fire riser + flare hit at 2.1s; hard cut to casual "everything's fine" plucks |
| S26 | `s26_the_pier.wav` | 3:57–4:05 | 8.0s | 0.450 | 0.092 | Fog bed, two fog-horn swells, sparse theatrical KS plucks — Kiko alone at the wrong pier |
| S27 | `s27_the_adjunction.wav` | 4:10–4:35 | 25.0s | 0.500 | 0.127 | Warm 76bpm night groove, ember crackle, fireworks blooms at 2/6/9/13/17/21s; groove thins to pad + embers |
| S28 | `s28_the_photo_button.wav` | 4:35–4:55 | 20.0s | 0.500 | 0.119 | Warm swell + original "nothing was resolved" pluck motif; flash hit at 16.4s; 2s freeze; quiet tail |
| S29 | `s29_ident.wav` | 4:55–5:00 | 5.0s | 0.550 | 0.102 | Logo sting: sub hit, shimmer gliss, trippy pitch-wobble under the TRIPPEDD card |

**Full mix:** `ep01_full_mix_0050-0500.wav` — 250.14s, peak 0.550, RMS 0.098.
Stems butt-joined in timecode order; twelve 0.42s smash-cut whoosh-hits inserted
between the Act-2 beats (S14→S15 … S25→S26) per the storyboard's transition math
(115s of beats + 5s of transitions = 120s).

## Build / QC

- Composed by `compose_ep01_music.py` (kept in this directory for reproducibility).
- QC 2026-10-07: all 20 stems + mix — duration ±0.05s vs storyboard, stereo
  44.1k/16-bit, zero clipped samples, DC offset < 0.01, audible-band energy
  confirmed, no near-silent stems, peaks ≤ 0.55. Structural beats spot-checked
  (S11 drum death @13.5s, S24 dead stop @8.3s, S25 flare hit @2.1s, S28 flash
  @16.4s, S26 sparse tail).
- Originality: no samples used; all motifs composed in-script; no copyrighted
  or recognizable existing melodies.

## Handoff notes for the edit

- Duck −6 dB under Static's dialogue (pilot convention per storyboard audio notes).
- S11: the drum-death at 13.5s is timed to the candle guttering — align the visual there.
- S24: the dead stop at 8.3s is the joke — do not fill it.
- Narrator N1/N2 are VO-pending; the score carries S10 and S28 without them.
