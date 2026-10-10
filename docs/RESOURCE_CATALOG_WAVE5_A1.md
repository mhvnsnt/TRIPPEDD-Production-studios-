# RESOURCE CATALOG — Wave 5 Appendix A1 (SFX / Foley / CC0-Voice Sources)

Worker: Wave 5 A1 (replacement — original worker killed by daemon restart; restarted fresh 2026-10-07).
Scope: NEW entries only. Every candidate grepped (`grep -i`) against `docs/RESOURCE_CATALOG.md` (366 `####` entries) before inclusion — no duplicates. Licenses verified from upstream sources (official terms pages, bundled license files, per-item license badges) on 2026-10-07. Copyleft (GPL/AGPL/LGPL) candidates: none found in this lane this wave — no new quarantine rows.
Badge key: ✅ = commercial-safe (verified) · 🚫 = not commercial-safe (NC/platform-restricted/research lane) · ❓ = unverified (read LICENSE before wiring)

## Kenney CC0 audio packs (7 entries — distinct per-pack pages, CC0 via Kenney's own asset pages + bundled License.txt)

#### Kenney — Interface Sounds ✅ commercial-safe
- **What:** 103 CC0 UI sounds (clicks, ticks, toggles, confirms, errors, glitches) in OGG
- **URL:** https://kenney.nl/assets/interface-sounds
- **License:** CC0 1.0 Universal (verified via kenney.nl asset page license text + bundled License.txt in pack zips, 2026-10-07)
- **Free tier:** fully free, no account, no attribution required
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** WIRED (2026-10-07 — smoke-tested; see tools/sfx/kenney-interface-sounds/)
- **Notes:** Menu/UI SFX backbone; distinct pack from the catalog's casino-audio entry. [Wave 5]

#### Kenney — Impact Sounds ✅ commercial-safe
- **What:** 130 CC0 impact sounds (punches, footsteps on 5 surfaces, glass/metal/wood breaks) in OGG
- **URL:** https://kenney.nl/assets/impact-sounds
- **License:** CC0 1.0 Universal (verified via kenney.nl asset page license text + bundled License.txt in pack zips, 2026-10-07)
- **Free tier:** fully free, no account, no attribution required
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Combat SFX core (punches, body hits, footsteps) — direct AshLane/Concrete Dragon fit. [Wave 5]

#### Kenney — Sci-Fi Sounds ✅ commercial-safe
- **What:** CC0 sci-fi SFX pack (phasers, power-ups, sweeps, laser zaps) in OGG
- **URL:** https://kenney.nl/assets/sci-fi-sounds
- **License:** CC0 1.0 Universal (verified via kenney.nl asset page license text, 2026-10-07)
- **Free tier:** fully free, no account, no attribution required
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Sci-fi stingers, UI sweeps, transition whooshes. [Wave 5]

#### Kenney — Digital Audio ✅ commercial-safe
- **What:** CC0 retro/digital SFX pack (bleeps, blips, 8-bit style effects) in OGG
- **URL:** https://kenney.nl/assets/digital-audio
- **License:** CC0 1.0 Universal (verified via kenney.nl asset page license text, 2026-10-07)
- **Free tier:** fully free, no account, no attribution required
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Retro/arcade UI layer for HUDs and minigames. [Wave 5]

#### Kenney — Music Jingles ✅ commercial-safe
- **What:** CC0 short musical stingers/jingles pack in OGG
- **URL:** https://kenney.nl/assets/music-jingles
- **License:** CC0 1.0 Universal (verified via kenney.nl asset page license text, 2026-10-07)
- **Free tier:** fully free, no account, no attribution required
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Win/lose/level stingers, logo hits. [Wave 5]

#### Kenney — RPG Audio ✅ commercial-safe
- **What:** CC0 fantasy RPG SFX pack (spells, coins, swords, potions) in OGG
- **URL:** https://kenney.nl/assets/rpg-audio
- **License:** CC0 1.0 Universal (verified via kenney.nl asset page license text, 2026-10-07)
- **Free tier:** fully free, no account, no attribution required
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Fantasy/action-adventure layer; coin/sword/potion sounds. [Wave 5]

#### Kenney — UI Audio ✅ commercial-safe
- **What:** CC0 UI sound pack (modern interface clicks, hovers, notifications) in OGG
- **URL:** https://kenney.nl/assets/ui-audio
- **License:** CC0 1.0 Universal (verified via kenney.nl asset page license text, 2026-10-07)
- **Free tier:** fully free, no account, no attribution required
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Second UI pack alongside Interface Sounds — more modern/soft UI set. [Wave 5]

## CC0 / public-domain voice & speech datasets (5 entries)

#### Mozilla Common Voice ✅ commercial-safe
- **What:** 130+ language crowd-read speech corpus, thousands of hours, with transcriptions
- **URL:** https://commonvoice.mozilla.org/
- **License:** CC0 1.0 Universal — public domain dedication (verified via Mozilla Data Collective license terms + dataset cards, 2026-10-07)
- **Free tier:** free download (account + terms acceptance via Mozilla Data Collective API)
- **Repo lane:** trippedd (voice)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** CC0 voice corpus for training/evaluating TTS/ASR and for ambient crowd-voice sourcing; keep license text with downloads. [Wave 5]

#### LJSpeech Dataset ✅ commercial-safe
- **What:** 24h single-female-speaker English TTS corpus (13,100 clips from LibriVox readings)
- **URL:** https://keithito.com/LJ-Speech-Dataset/
- **License:** Public domain in the US (verified via the dataset's own License section on keithito.com, 2026-10-07); no restrictions, attribution not required
- **Free tier:** free download (2.6 GB tarball)
- **Repo lane:** trippedd (voice)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Single-speaker baseline TTS corpus; distinct from the Matcha LJSpeech *model* already in the catalog. [Wave 5]

#### VoxPopuli ✅ commercial-safe
- **What:** Large-scale multilingual speech corpus from European Parliament recordings (ASR/translation)
- **URL:** https://github.com/facebookresearch/voxpopuli
- **License:** CC0 1.0 (verified via HuggingFace dataset card licensing section, 2026-10-07); raw audio additionally subject to European Parliament legal notice
- **Free tier:** free download
- **Repo lane:** trippedd (voice)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Multilingual voice variety for non-English VO and crowd beds; mind the EU Parliament legal notice on raw audio. [Wave 5]

#### Thorsten-Voice ✅ commercial-safe
- **What:** High-quality German TTS voice datasets (neutral, emotional, Hessisch dialect, 44kHz full set)
- **URL:** https://github.com/thorstenMueller/Thorsten-Voice
- **License:** CC0 1.0 Universal (verified via repo README license statements, 2026-10-07)
- **Free tier:** free download (Zenodo DOI + HuggingFace mirrors)
- **Repo lane:** trippedd (voice)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** German VO / narrator voice source for Wizard Gang localization; CC0-clean. [Wave 5]

#### HiFi-TTS ✅ commercial-safe
- **What:** 292h multi-speaker (10 speakers, 44.1kHz) English TTS dataset from LibriVox audiobooks (NVIDIA)
- **URL:** https://research.nvidia.com/publication/2021-04_hi-fi-multi-speaker-english-tts-dataset
- **License:** CC BY 4.0 (verified via arXiv 2104.01497 paper Table 1 + NVIDIA research page, 2026-10-07) — commercial OK with attribution
- **Free tier:** free download (openslr.org/109)
- **Repo lane:** trippedd (voice)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Multi-speaker English VO training/eval; attribution required in credits. [Wave 5]

## Public-domain spoken-word & radio archives (3 entries)

#### LibriVox ✅ commercial-safe
- **What:** 21,000+ volunteer-read public-domain audiobooks (fiction, drama, poetry, many languages)
- **URL:** https://librivox.org/
- **License:** Public domain (verified via wiki.librivox.org Copyright_and_Public_Domain page: "anyone can use those audio files however they wish", incl. commercial, 2026-10-07)
- **Free tier:** fully free streaming + MP3/OGG downloads; files mirrored on Internet Archive
- **Repo lane:** trippedd (voice)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** WIRED (2026-10-07 — smoke-tested; see tools/sfx/librivox/)
- **Notes:** PD narration, dialogue beds, period voice texture; no clearance friction at all. [Wave 5]

#### OTRR — Old Time Radio Researchers Group ✅ commercial-safe
- **What:** Thousands of restored public-domain old-time radio series (drama, sci-fi, western) on Internet Archive
- **URL:** https://archive.org/details/OTRR_Certified_Dimension_X
- **License:** Public domain (verified via OTRR item notes on archive.org: group releases its restored transfers into the public domain, 2026-10-07)
- **Free tier:** free MP3/zip downloads per series
- **Repo lane:** trippedd (voice)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** URL is a representative series (Dimension X, sci-fi); browse the OTRR creator on archive.org for the full set. Vintage VO + foley-rich drama beds. [Wave 5]

#### Prelinger Archives ✅ commercial-safe
- **What:** 8,500+ ephemeral films (ads, industrials, educationals, home movies) on Internet Archive; audio tracks usable as foley/ambience
- **URL:** https://archive.org/details/prelinger
- **License:** Per-film public-domain dedication (verified via Prelinger licensing FAQ: films carrying the CC Public Domain Dedication are reusable without restriction — CHECK EACH FILM's item page, 2026-10-07)
- **Free tier:** free downloads (MP4/Ogg/MPEG2 per film)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** ~65% of holdings are PD; ~28/30 top downloads carry the dedication. Strip soundtracks if music rights are unclear. [Wave 5]

## CC0 SFX libraries & foley (8 entries)

#### BigSoundBank (LaSonotheque) ✅ commercial-safe
- **What:** Thousands of per-sound CC0 SFX with UCS categories, 48kHz/24-bit, no account
- **URL:** https://bigsoundbank.com/applause-from-40-people-3-s3519.html
- **License:** CC0 / public-domain equivalent per sound (verified via the per-sound FAQ on bigsoundbank.com: "I intentionally release it under the CC0 license", commercial OK, no attribution, 2026-10-07)
- **Free tier:** free downloads, no signup
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** URL is a representative sound page; the whole library is CC0. UCS-categorized — ideal for systematic foley pulls. [Wave 5]

#### BVKER — Footsteps Foley Library ✅ commercial-safe
- **What:** 700+ WAV foley files (footsteps, ambience recordings, one-shots, pops, clicks)
- **URL:** https://bvker.com/foley-sound-effects/
- **License:** CC0 1.0 (verified via bvker.com foley page license section, 2026-10-07) — no credit required
- **Free tier:** free download pack
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Dedicated foley source — footsteps, cloth, handling sounds for fight-scene beds. [Wave 5]

#### 99Sounds — Cinematic Textures ✅ commercial-safe
- **What:** 40 cinematic drones, textures and SFX by Dronny Darko, 24-bit WAV (429 MB)
- **URL:** https://99sounds.org/cinematic-textures/
- **License:** Royalty-free for commercial and non-commercial use (verified via 99Sounds release terms, 2026-10-07)
- **Free tier:** free download
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Dark cinematic beds for Wizard Gang interstitials; distinct pack from the catalog's 99Sounds sci-fi entry. [Wave 5]

#### 99Sounds — Free Sound Effects index ✅ commercial-safe
- **What:** Master index of all 99Sounds royalty-free packs (sci-fi, horror, glitch, foley, drums)
- **URL:** https://99sounds.org/free-sound-effects/
- **License:** Royalty-free for commercial and non-commercial use (verified via 99Sounds release terms, 2026-10-07)
- **Free tier:** free downloads
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Pack-discovery hub; pull individual packs from here. [Wave 5]

#### FreePD.com catalog (via mirrors) ✅ commercial-safe
- **What:** Former CC0 music/SFX catalog (2008–2025); all tracks CC0
- **URL:** https://web.archive.org/web/20250106221458/https://freepd.com/upbeat.php
- **License:** CC0 1.0 Universal (verified via Wayback snapshot of FreePD's own banner: "Creative Commons 0 — Completely Royalty Free", 2026-10-07)
- **Free tier:** free (via Internet Archive mirrors and the SoundSafari GitHub CC0 mirror)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Site SHUT DOWN late 2025 — use Internet Archive mirror items or the SoundSafari/CC0-1.0-Music GitHub mirror. Verify each file's CC0 tag on the mirror. [Wave 5]

#### Partners In Rhyme — SFX & Ambience ✅ commercial-safe
- **What:** Free SFX/ambience category (nature, crowd, rain, thunder, jungle, ocean loops)
- **URL:** https://www.partnersinrhyme.com/soundfx/WEB-DESIGN-SOUNDS/AMBIENT.shtml
- **License:** Free royalty-free (verified via Partners In Rhyme site terms, 2026-10-07)
- **Free tier:** free downloads
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Distinct SFX/ambience page from the catalog's PIR music-loops entry. [Wave 5]

#### Bryce835 — AI-generated SFX (Freesound) ✅ commercial-safe
- **What:** Small CC0 pack of AI-generated sound effects on Freesound
- **URL:** https://freesound.org/people/Bryce835/packs/40655/
- **License:** CC0 1.0 (verified via the Freesound pack page license badge, 2026-10-07)
- **Free tier:** free (Freesound account required for download)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Small pack but CC0-clean; example of AI-generated SFX usable commercially. [Wave 5]

#### MLG9309 — Creative Commons Zero pack (Freesound) ✅ commercial-safe
- **What:** CC0 foley/ambience recordings pack on Freesound (office ambience, money handling)
- **URL:** https://freesound.org/people/MLG9309/packs/27750/
- **License:** CC0 1.0 (verified via the Freesound pack page license badge, 2026-10-07)
- **Free tier:** free (Freesound account required for download)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Everyday foley (workspace, handling) for realism beds. [Wave 5]

## OpenGameArt CC0 packs (4 entries — verified CC0 per-pack)

#### OpenGameArt — 50 CC0 Sci-Fi SFX (rubberduck) ✅ commercial-safe
- **What:** 50 CC0 sci-fi sound effects bundle
- **URL:** https://opengameart.org/content/50-cc0-sci-fi-sfx
- **License:** CC0 1.0 (verified via the OGA item page license field + third-party credits file, 2026-10-07)
- **Free tier:** free download
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Sci-fi UI/weapons layer. [Wave 5]

#### OpenGameArt — 30 CC0 SFX Loops (rubberduck) ✅ commercial-safe
- **What:** 30 loopable CC0 SFX
- **URL:** https://opengameart.org/content/30-cc0-sfx-loops
- **License:** CC0 1.0 (verified via the OGA item page license field + third-party credits file, 2026-10-07)
- **Free tier:** free download
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Loop-ready effects for ambience beds and game loops. [Wave 5]

#### OpenGameArt — 100 CC0 SFX #2 (rubberduck) ✅ commercial-safe
- **What:** 100 assorted CC0 sound effects, second volume
- **URL:** https://opengameart.org/content/100-cc0-sfx-2
- **License:** CC0 1.0 (verified via the OGA item page license field + third-party credits file, 2026-10-07)
- **Free tier:** free download
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** General-purpose CC0 grab bag. [Wave 5]

#### OpenGameArt — Loopable Dungeon Ambience (JaggedStone) ✅ commercial-safe
- **What:** Loopable CC0 dungeon ambience track
- **URL:** https://opengameart.org/content/loopable-dungeon-ambience
- **License:** CC0 1.0 (verified via the OGA item page license field + third-party credits file, 2026-10-07)
- **Free tier:** free download
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Dark loopable bed for horror/fantasy segments. [Wave 5]

## Freesound curated packs — CC-BY / per-sound licenses (6 entries — badge each honestly)

#### SoundFlakes — Diablo sound redesign pack (Freesound) ✅ commercial-safe
- **What:** 24-bit WAV game SFX redesign pack (impacts, roars, swings, atmospheres)
- **URL:** https://freesound.org/people/SoundFlakes/packs/27753/
- **License:** Per-sound license on Freesound (author states: use in any projects incl. commercial; do not resell standalone — verified via sound-page text, 2026-10-07)
- **Free tier:** free (Freesound account required)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Confirm each sound's license badge on its page before wiring. [Wave 5]

#### LittleRobotSoundFactory — Voices: Human (Freesound) ✅ commercial-safe
- **What:** Human voice SFX pack (grunts, reactions, efforts) for games
- **URL:** https://freesound.org/people/LittleRobotSoundFactory/packs/17725/
- **License:** CC-BY 4.0 (verified via per-sound license badges on Freesound, 2026-10-07) — attribution required
- **Free tier:** free (Freesound account required)
- **Repo lane:** trippedd (voice)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Fight-effort/voice-reaction source; keep attribution list. [Wave 5]

#### LittleRobotSoundFactory — Horror Sound Effects Library (Freesound) ✅ commercial-safe
- **What:** Horror SFX pack (breaths, scares, creature sounds)
- **URL:** https://freesound.org/people/LittleRobotSoundFactory/packs/16688/
- **License:** CC-BY 4.0 (verified via per-sound license badges on Freesound, 2026-10-07) — attribution required
- **Free tier:** free (Freesound account required)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Halloween-season lane material (October-gated per owner rule); attribution list required. [Wave 5]

#### Benboncan — Ambience field recordings (Freesound) ✅ commercial-safe
- **What:** Stereo field-recording ambience pack (streams, waves, crowds, winds)
- **URL:** https://freesound.org/people/Benboncan/packs/4374/
- **License:** CC-BY 4.0 / Attribution (verified via per-sound license badges on Freesound, 2026-10-07) — attribution required
- **Free tier:** free (Freesound account required)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** High-rated loopable nature beds; attribution list required. [Wave 5]

#### deadrobotmusic — Foley//Textures (Freesound) ✅ commercial-safe
- **What:** Field-mic foley/texture pack with per-sound CC0 tags (water, rain, forest percussion)
- **URL:** https://freesound.org/people/deadrobotmusic/packs/30937/
- **License:** CC0 per sound (verified via //cc0 tags on the pack listing, 2026-10-07) — re-confirm each sound's page before wiring
- **Free tier:** free (Freesound account required)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Textures for sound-design layering. [Wave 5]

#### InspectorJ — Freesound SFX (attribution) ✅ commercial-safe
- **What:** Professional water/ambience/soundscape recordings (drips, streams, sewers)
- **URL:** https://freesound.org/people/InspectorJ/sounds/342566/
- **License:** CC-BY — NOT public domain (verified via sound-page text: "This sound is not in the public domain. Please attribute/credit the sound if you use it", 2026-10-07) — attribution required
- **Free tier:** free (Freesound account required)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** URL is a representative verified sound; browse the artist page for the full set. Keep attribution list. [Wave 5]

## Restricted / unverified (honest badges)

#### Meta Sound Collection 🚫 not commercial-safe
- **What:** 14,000+ royalty-free tracks and SFX inside Meta's creator tools
- **URL:** https://www.facebook.com/legal/musicguidelines
- **License:** Meta platform license — free for use ON Facebook/Instagram (verified via Meta music guidelines + third-party reporting, 2026-10-07); use outside Meta products risks violating terms
- **Free tier:** free inside Meta products
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** RESEARCH/REFERENCE ONLY — do not ship in games or YouTube cuts; licensed for Reels/Stories on Meta surfaces only. [Wave 5]

#### BBC Sound Effects Archive 🚫 not commercial-safe
- **What:** 33,000+ BBC archive recordings (nature, transport, crowds, footsteps) in WAV/MP3
- **URL:** https://sound-effects.bbcrewind.co.uk/licensing
- **License:** BBC RemArc Licence — personal, educational and research use ONLY (verified via BBC licensing page + reporting, 2026-10-07); commercial use requires separate licensing via Pro Sound Effects
- **Free tier:** free downloads
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** RESEARCH/REFERENCE ONLY — never ship in commercial cuts; metadata separately under Open Government Licence 3.0. [Wave 5]

#### Glitchmachines — free sample packs ❓ unverified
- **What:** Free experimental SFX packs from Glitchmachines (Teratoma, SEISM and others)
- **URL:** https://free-sample-packs.com/glitchmachines-teratoma/
- **License:** ❓ NOT verified — no public license text found for the free packs (checked official site references + mirrors, 2026-10-07); read the license inside the pack before any use
- **Free tier:** free downloads from the official site's free section
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** DO NOT wire until the pack's own license text is read; URL is a mirror listing — download from glitchmachines.com directly. [Wave 5]

#### FindSounds ❓ unverified
- **What:** Long-running web search engine for sound effects (links out to host sites)
- **URL:** https://FindSounds.com/help1.html
- **License:** ❓ unverified — official help page states: "We do not make any claims regarding the licensing or commercial use of those sounds" — check each sound at its source (verified 2026-10-07)
- **Free tier:** free search
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Discovery tool only; per-sound clearance at the hosting site is mandatory. [Wave 5]

#### Tabletop Audio ❓ unverified
- **What:** 200+ professionally designed RPG ambience tracks (fantasy, sci-fi, horror, historical) with a live mixer and offline save
- **URL:** https://tabletopaudio.com/
- **License:** ❓ NOT verified upstream — no license/terms text found on the site during research (verified 2026-10-07); do not redistribute or ship without written clearance
- **Free tier:** free streaming in browser; offline save of individual tracks
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Reference/ambience inspiration only until terms are confirmed; read their terms before any wire-up. [Wave 5]

#### NASA Voyager — "Symphonies of the Planets" (unofficial album masters) ❓ unverified
- **What:** Voyager plasma-wave recordings of planetary magnetospheres (Jupiter, Saturn, Uranus, Neptune, Io, etc.)
- **URL:** https://archive.org/details/VoyagerRecordings-SymphoniesOfThePlanets15CompleteRecordings
- **License:** ❓ MIXED — the underlying Voyager plasma-wave DATA is NASA public domain, but these are commercial CD album masters (LaserLight 1992 / Brain-Mind Research releases) uploaded by a third party; the album mastering is NOT cleanly PD (verified 2026-10-07)
- **Free tier:** free downloads on the item page
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Do NOT ship from this item; for clean PD space audio use NASA-published sources instead. Kept as a research lead only. [Wave 5]