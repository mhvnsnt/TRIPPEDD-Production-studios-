# RESOURCE_CATALOG appendix — Wave 5 A2 (music libraries + free plugins/instruments)

Worker: Wave 5 A2 (replacement worker — original killed by daemon restart; the two wired proofs under `tools/music/` were downloaded by the original worker minutes before the kill and re-verified by ffprobe by the replacement).
Canonical count rule: only `####` headings in `docs/RESOURCE_CATALOG.md` count. This appendix is merged by the coordinator — do NOT edit `docs/RESOURCE_CATALOG.md` directly.
License rule: every license verified from the upstream source (repo LICENSE, official terms/licensing page) — never assumed. Badges: ✅ commercial-safe, 🚫 not commercial-safe (research lane), ❓ unverified/conditional.

## Music libraries

#### Ross Bugden ✅ commercial-safe
- **What:** Epic/trailer/dramatic orchestral music, free incl. commercial with credit
- **URL:** https://www.youtube.com/@rossbugden
- **License:** CC-BY 4.0 (verified via Wikimedia Commons file page "File:Black Heat WAV by Ross Bugden.wav" + artist's own licensing notes "free to use and monetize, just credit me", 2026-10-07)
- **Free tier:** fully free; attribution required ("Music: 'Black Heat' by Ross Bugden — CC-BY 4.0")
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** WIRED
- **Notes:** Wire proof: `tools/music/ross-bugden/ross-bugden-black-heat.wav` (PCM s24le 44.1kHz stereo, 2:00, 31,761,364 B) + MANIFEST.md; ffprobe-verified clean decode. Caveats: artist runs YouTube Content ID — expect automated claims, dispute with credit line; do NOT register tracks as your own. [Wave 5]

#### Open Goldberg Variations ✅ commercial-safe
- **What:** Bach's Goldberg Variations — definitive studio recording (Kimiko Ishizaka, Bösendorfer 290 Imperial) + open MuseScore score
- **URL:** https://opengoldbergvariations.org
- **License:** CC0 1.0 Universal, 28 May 2012 (verified via en.wikipedia.org/wiki/Open_Goldberg_Variations and opengoldbergvariations.org "free of copyright (all uses allowed)", 2026-10-07)
- **Free tier:** fully free, no attribution (courtesy credit recommended)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** WIRED
- **Notes:** Wire proof: `tools/music/open-goldberg-variations/ogv-aria.mp3` (MP3 48kHz stereo, 4:59.5, 5,849,600 B) + `ogv-variatio-01.mp3` (1:55.5, 2,637,824 B) + MANIFEST.md; ffprobe-verified clean decode. Score was re-engraved by the project (also CC0); Bach's original PD for centuries. Piano underscore for series scoring; zero Content ID risk. [Wave 5]

#### Silverman Sound Studios (Shane Ivers) ✅ commercial-safe
- **What:** 200+ professional tracks — orchestral scores, chiptune, rock, hip-hop, ambient, cinematic
- **URL:** https://www.silvermansound.com/
- **License:** CC-BY 4.0 (verified via official about page: "free to use under Creative Commons CC BY 4.0 licensing. Credit 'silvermansound.com'... YouTube, TikTok, podcasts, films, games, radio, wherever you create", 2026-10-07)
- **Free tier:** fully free; credit silvermansound.com (Pro no-attribution licenses available for purchase)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** One of the best clean-CC-BY catalogs explicitly naming games. If a claim ever lands, the composer handles disputes personally. No redistribution as standalone music. [Wave 5]

#### Patrick de Arteaga ✅ commercial-safe
- **What:** Royalty-free music made for indie game developers + MIDI/chiptune packs (editable source)
- **URL:** https://patrickdearteaga.com/
- **License:** Free License = Creative Commons with attribution (verified via https://patrickdearteaga.com/licensing/: video games, YouTube, mobile apps, podcasts, indie films all included; "Monetize all multimedia projects above with unlimited copies"; credit patrickdearteaga.com; Pro €13/track = no-attribution), 2026-10-07
- **Free tier:** fully free with credit
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** MIDI packs let us re-render/adapt cues — strongest game-scoring fit in this wave. Moral rights stay with composer (credit in game credits). TV/radio needs Broadcast License (€35) — not needed for games/episodes. [Wave 5]

#### Mixaund ✅ commercial-safe
- **What:** Corporate/advertising/motivational background music, 100+ tracks (free-stock-music.com-promoted catalog)
- **URL:** https://www.free-stock-music.com/artist.mixaund.html
- **License:** CC-BY 4.0 per-track (verified via free-stock-music.com usage matrix: "Podcasts / Apps / Games ✔" free-with-credit; monetized use allowed with credit to Mixaund + link; $8/track no-credit license on Bandcamp), 2026-10-07
- **Free tier:** free with credit (MP3 320kbps + WAV 44.1kHz 16-bit downloads)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Corporate/motivational bed music — fits production interstitials, UI menus, sponsor bumpers. Do NOT re-upload tracks to Spotify/etc. as your own (license forbids). Confirm the CC-BY 4.0 badge on each track page before shipping. [Wave 5]

#### Netlabels.org ❓ unverified (per-release check)
- **What:** Directory/archive of CC netlabels — thousands of free electronic/experimental releases, many mirrored on archive.org
- **URL:** https://netlabels.org/
- **License:** Per-release CC licenses (verified via netlabels.org/music + release pages, 2026-10-07); many releases are CC-BY-NC — check EACH release
- **Free tier:** free downloads
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Discovery source, not a blanket license. Workflow: pick release → confirm license on its release page → keep proof. Live site verified 2026-10-07. [Wave 5]

#### Argofox ❓ unverified (conditional)
- **What:** Electronic/EDM royalty-free record label (YouTube-first), no-copyright-claims catalog
- **URL:** https://www.youtube.com/@argofox
- **License:** Label permission: "use our songs in monetized videos if you give credit" (verified via track descriptions, e.g. DOCTOR VOX - Frontier; updated Sept 2026), BUT "If you're interested in using our music in a video game you're developing or publishing, please DM us on Discord" — game sync needs explicit permission, 2026-10-07
- **Free tier:** free for monetized videos with credit
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** Episodes published to YouTube = fine with the label's video credit. Game/app sync = contact first. Keep per-track credit blocks. Badge ❓ until a game-use permission is on file. [Wave 5]

#### Pretzel Rocks ❓ unverified (conditional)
- **What:** Stream-safe licensed music service for livestreamers (catalog cleared with artists/rightsholders)
- **URL:** https://www.pretzel.rocks/
- **License:** Pretzel proprietary license for stream use (verified via help.pretzel.rocks FAQ "Why does Pretzel exist" + Streamlabs/Digital Music News coverage, 2026-10-07); covers Twitch/YouTube/Facebook streams — sync into a produced series/game is NOT covered
- **Free tier:** free tier (mandatory chat attribution; some labels premium-only)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Stream-bed music only, not a sync library for produced episodes/games. Useful for livestreamed production sessions. Verify current availability — help center pages are sparse/stale. [Wave 5]

#### AShamaluevMusic ❓ unverified (conditional)
- **What:** Cinematic/action/trailer background music, large free catalog (SoundCloud + archive.org mirrors)
- **URL:** https://soundcloud.com/ashamaluevmusic
- **License:** Mixed/conditional (verified via artist's own archive.org track posts: "absolutely FREE for using in any video or project... even in commercial purposes" with credit — BUT artist FAQ states monetized YouTube videos require a purchased per-track license and tracks are claimed via AdRev Content ID), 2026-10-07
- **Free tier:** free non-monetized use with credit; monetization needs paid license
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** Contradictory terms between posts and FAQ = badge ❓. Only use for non-monetized cuts unless a purchased license is on file. Do not rely on "free" posts alone. [Wave 5]

#### Meta Sound Collection 🚫 not commercial-safe
- **What:** Meta's built-in music/SFX library inside Creator Studio (Facebook/Instagram publishing)
- **URL:** https://www.facebook.com/sound/collection/terms
- **License:** Sound Collection Terms (verified verbatim, last modified March 16, 2022): "license to use the SC Audio Content for commercial or non-commercial purposes in content you create, upload, and distribute on the Meta Company Products ... only. You may not ... otherwise use the SC Audio Content separately from the Meta Company Products." — 2026-10-07
- **Free tier:** free within Meta products
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** 🚫 NOT game-safe: rights do not travel off Meta platforms (YouTube uploads can trigger mutes/blocks). Only usable for episodes distributed natively on Facebook/Instagram. Included as a warning entry. [Wave 5]

#### Spinningmerkaba 🚫 not commercial-safe
- **What:** Electronic/ambient instrumentals (often suggested as royalty-free)
- **URL:** https://freemusicarchive.org/music/spinningmerkaba/
- **License:** Per-track CC-BY-NC / CC-BY-NC-SA (verified via FMA track pages: "Commercial use not allowed", 2026-10-07)
- **Free tier:** free for non-commercial use with attribution
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** 🚫 Warning entry: commonly mistaken for commercial-safe. A few older tracks may carry plain CC-BY — check each track page; default to NC = research lane only. [Wave 5]

#### Uppbeat 🚫 not commercial-safe (free tier)
- **What:** Curated royalty-free music + SFX + stock video for creators (freemium)
- **URL:** https://uppbeat.io/
- **License:** Uppbeat Free plan (verified via official FAQ + license tiers, 2026-10-07): "The free license covers non-commercial content" — 3 downloads/month topping up, credit required; paid ads and client work need Pro
- **Free tier:** free for non-commercial content with accreditation
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** 🚫 Free tier is NOT commercial-safe (paid ads/client work excluded). Useful only for non-commercial internal cuts. Included as a warning entry since the free tier looks commercial-safe at a glance. [Wave 5]
## More music libraries

#### Punch Deck ✅ commercial-safe
- **What:** Trap/hip-hop/rap beats for videos and games — free including commercial with credit
- **URL:** https://punchdeck.com
- **License:** CC-BY 4.0 (verified via official terms page, 2026-10-07)
- **Free tier:** fully free MP3 downloads; attribution required
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Explicit commercial-use OK (incl. games) with credit. Good fit for game-menu/trap-flavored scoring beds. [Wave 5]

#### SampleScience ✅ commercial-safe
- **What:** 30+ free VST/AU virtual instruments (vintage synths, romplers, drum machines, ambient)
- **URL:** http://www.samplescience.info
- **License:** free-proprietary (use OK, check EULA) — verified 2026-10-07: developer reverted a 2025 paywall, whole catalog free again per multiple 2026 plugin press reports; SampleScience Player (200-patch rompler) documents per-patch licenses (public domain / made for production / CC 3.0 w/ attribution) — all usable in commercial music production
- **Free tier:** fully free; some time-limited promo codes rotate
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Huge free instrument pool for scoring. Caveat: developer flipped free↔paid before — re-download availability is strong now (Oct 2026) but keep local copies. [Wave 5]

#### Freebeats.io ✅ commercial-safe (credit required)
- **What:** Royalty-free hip-hop/trap/R&B beats by producer White Hot, commercial use OK
- **URL:** https://freebeats.io
- **License:** custom royalty-free non-exclusive license (verified via freebeats.io/terms-of-use, 2026-10-07): commercial use incl. film/TV/radio allowed; written credit required ("Beat provided by https://freebeats.io / Produced by White Hot"); MUST NOT register with YouTube Content ID
- **Free tier:** free untagged 320kbps MP3 (via social-follow download); tracked-out WAVs = $4.95 processing fee
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Watch the Content ID clause — works for studio productions but cannot claim exclusivity. Strong source for beat beds in promos/street-real content. [Wave 5]

#### Alex-Productions ❓ license partially unverified
- **What:** Free background/orchestral music by Alex-Productions (Greece)
- **URL:** https://www.youtube.com/@AlexProductionsmusic
- **License:** ❓ — free for monetized YouTube videos with credit (stated on channel); video-GAME use explicitly requires the paid BUSINESS license per channel terms. Studio production use beyond YouTube (series/film) not clearly granted — verify per project or buy the license
- **Free tier:** free for YouTube content with credit; paid license for games
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Downgraded from seed-list assumption of "free commercial" — animated-series/film usage is a gray zone. Do not wire without license purchase or written confirmation. [Wave 5]

#### Timbres of Heaven ❓ license partially unverified
- **What:** Huge free orchestral/church-organ sample libraries (SoundFont format) by Don Allen
- **URL:** https://www.timbresofheaven.com
- **License:** ❓ custom free terms — unlimited personal use per Don Allen's statements; redistribution restricted; COMMERCIAL terms not stated on site
- **Free tier:** fully free downloads (SoundFonts)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Excellent orchestra sources for scoring IF commercial terms can be confirmed with the author. Research lane until confirmed — do not ship in monetized productions without written OK. [Wave 5]

#### GeneralUser GS ❓ license partially unverified
- **What:** Popular free General-MIDI SoundFont (S. Christian Collins) — big upgrade over default GM
- **URL:** https://www.schristiancollins.com/generaluser.php
- **License:** ❓ gray area — distributed free; Musical Artifacts licensing flags note some samples may be derived from proprietary (Yamaha) sources; commercial-use verification not obtainable from author
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Fine for personal/internal use; NOT commercial-safe until the sample provenance question is resolved. Use Salamander/FluidR3/VSCO2 instead for shipped work. [Wave 5]

#### Yevhen Lokhmatov 🚫 not commercial-safe
- **What:** Folk/pop background music (YouTube channel) for videos
- **URL:** https://www.youtube.com/@YevhenLokhmatov
- **License:** CC-BY-NC (verified via artist's own site/license page, 2026-10-07) — non-commercial only
- **Free tier:** free for non-commercial use with credit
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Research lane only — NC kills all monetized-studio use. Listed here to prevent accidental commercial use. [Wave 5]

#### TuneTank 🚫 not commercial-safe
- **What:** Free music for creators (timetank/freemusic brand)
- **URL:** https://www.tunetank.com
- **License:** custom license (verified via tunetank.com/legal/license, 2026-10-07) — EXPLICITLY FORBIDS use in video games AND advertising
- **Free tier:** free for creators within those restrictions
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Research lane only — the games/advertising ban makes it unusable for TRIPPEDD studio productions. Listed to prevent accidental use. [Wave 5]

## Free plugins & virtual instruments (scoring stack)

#### Airwindows ✅ commercial-safe
- **What:** 300+ free, minimal, open DSP audio plugins (EQs, compressors, saturation, reverbs) by Chris Johnson
- **URL:** https://www.airwindows.com
- **License:** MIT (verified via github.com/airwindows/airwindows LICENSE, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** MIT = fully wireable incl. source integration. The backbone free mixing/mastering stack — hundreds of quality effects at zero cost. [Wave 5]

#### Valhalla Supermassive ✅ commercial-safe
- **What:** Legendary free reverb/delay plugin (massive spaces, shimmer) by Valhalla DSP
- **URL:** https://valhalladsp.com/shop/reverb/valhalla-supermassive/
- **License:** free-proprietary (use OK, check EULA) — official page: "free. No strings attached." (verified 2026-10-07)
- **Free tier:** fully free, no time limit, no account needed
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** The single best free reverb for score ambience. Zero-cost industry-standard sound. [Wave 5]

#### TDR Nova ✅ commercial-safe
- **What:** Parallel dynamic equalizer (free edition) by Tokyo Dawn Labs
- **URL:** https://www.tokyodawn.net/tdr-nova/
- **License:** free-proprietary (use OK, check EULA) — Standard Edition free, verified via official page, 2026-10-07
- **Free tier:** free Standard Edition (GE = paid)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Pro-grade dynamic EQ at $0 — ideal for dialogue/music carving in the animated series. [Wave 5]

#### TDR Kotelnikov ✅ commercial-safe
- **What:** Transparent mastering/bus compressor (free edition) by Tokyo Dawn Labs
- **URL:** https://www.tokyodawn.net/tdr-kotelnikov/
- **License:** free-proprietary (use OK, check EULA) — Standard Edition free, verified via official page, 2026-10-07
- **Free tier:** free Standard Edition (Gentleman's Edition = paid)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Master-bus glue for final score mixes. Pairs with TDR Nova as the free TDR mastering chain. [Wave 5]

#### Vital ✅ commercial-safe
- **What:** Spectral-warping wavetable synth (free Basic tier) — Serum-class sound design
- **URL:** https://vital.audio
- **License:** free-proprietary (use OK, check EULA) — Basic tier free; NOTE: the source code is GPLv3, so do NOT embed source — use the compiled plugin per the free tier (verified 2026-10-07)
- **Free tier:** free Basic tier (Plus/Pro = paid); account required
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** The free-tier synth for score sound design (risers, pads, basses). GPL source is a trap — use binary only, keep off the quarantine list. [Wave 5]

#### Spitfire LABS ✅ commercial-safe
- **What:** Free curated virtual instruments (strings, pianos, choirs, drums) by Spitfire Audio
- **URL:** https://www.spitfireaudio.com/labs
- **License:** free-proprietary (use OK, check EULA) — free per official page (verified 2026-10-07); CAVEAT: Spitfire is folding LABS into "Splice INSTRUMENT" — availability of the standalone LABS app may change
- **Free tier:** fully free; Spitfire app/account required
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Best free orchestral/organic instrument library for the animated series score. Grab while standalone LABS exists. [Wave 5]

#### BBC Symphony Orchestra Discover ✅ commercial-safe
- **What:** Free 33-instrument BBC orchestral library (Spitfire) — strings/brass/woodwinds/percussion
- **URL:** https://www.spitfireaudio.com/bbc-symphony-orchestra-discover
- **License:** free-proprietary (use OK, check EULA) — free via Spitfire EULA; licensed for 2 computers; commercial-use OK (verified 2026-10-07)
- **Free tier:** fully free; Spitfire account + short survey required
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** NOT the BBC Sound Effects Archive (RemArc NC, already in catalog) — this is Spitfire's free orchestral VST, commercial-safe. Core orchestral scoring tool. [Wave 5]

#### Komplete Start ✅ commercial-safe
- **What:** Free bundle of 2,000+ sounds / 16 synths & sampled instruments by Native Instruments
- **URL:** https://www.native-instruments.com/en/products/komplete/bundles/komplete-start/
- **License:** free-proprietary (use OK, check EULA) — NI EULA; Native Access install required (verified 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Massive free content pool (Kontakt Player instruments, synths, FX). Good all-rounder for score layering. [Wave 5]

#### Decent Sampler (+ Pianobook) ✅ commercial-safe
- **What:** Free cross-platform sampler (VST/VST3/AU/AAX/standalone) + Pianobook.co.uk community sample-library hub
- **URL:** https://www.decentsamples.com / https://www.pianobook.co.uk
- **License:** free-proprietary (use OK, check EULA) — Decent Sampler app free; Pianobook libraries carry the Pianobook EULA: copyright-free samples, commercial use OK, no sample redistribution (verified 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** The free sampling ecosystem — hundreds of Pianobook community instruments (pianos, strings, oddities) load in Decent Sampler. Huge scoring asset. [Wave 5]

#### VSCO2 Community Edition ✅ commercial-safe
- **What:** Full orchestral sample library (strings, brass, woodwinds, percussion) — the free community version of Versilian's VSCO2
- **URL:** https://www.versilian-studios.com/vsco-community
- **License:** CC0 1.0 Universal (verified via official page, 2026-10-07) — public-domain dedication
- **Free tier:** fully free; also on GitHub
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** CC0 orchestra = zero-restriction scoring. Loads in Sforzando/SFZ players. Top-tier free orchestral resource. [Wave 5]

#### Virtual Playing Orchestra ✅ commercial-safe
- **What:** Free full orchestral sample library (SFZ) assembled from public-domain sources
- **URL:** https://virtualplaying.com
- **License:** free for all use incl. commercial — official page: no restrictions on making music (even commercial); source samples are mixed CC (noted: do not redistribute raw samples) (verified 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Second CC-friendly orchestra; pairs with VSCO2 CE. Respect the no-raw-redistribution clause — rendered music is fine. [Wave 5]

#### Sonatina Symphonic Orchestra ✅ commercial-safe
- **What:** Free full orchestral sample module (SFZ/SoundFont) — classic free orchestra
- **URL:** https://sso.mattiaswestlund.net
- **License:** CC Sampling Plus 1.0 (verified via official page, 2026-10-07) — commercial use allowed; no endorsement/sample resale
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Long-standing free orchestra standard. CC Sampling Plus allows commercial music; read the license before sampling the samples. [Wave 5]

#### Salamander Grand Piano ✅ commercial-safe
- **What:** Beautifully sampled Yamaha C5 grand piano (SFZ/SoundFont) by Alexander Holm
- **URL:** https://archive.org/details/SalamanderGrandPianoV3
- **License:** CC-BY 3.0 (verified via archive.org item page, 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** The go-to free grand piano for scoring. CC-BY = commercial-safe with credit. [Wave 5]

#### FluidR3 SoundFont ✅ commercial-safe
- **What:** Full General-MIDI SoundFont (Frank Wen) — orchestra, drums, everything
- **URL:** https://github.com/pianobooster/fluid-soundfont
- **License:** MIT (verified via GitHub repo LICENSE, 2026-10-07) — note: some third-party repackages claim other licenses; the upstream repo is MIT, attribution due
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Free GM soundfont for MIDI rendering pipelines. MIT = fully wireable. Prefer over GeneralUser GS (gray-area provenance). [Wave 5]

#### Ivy Audio ✅ commercial-safe
- **What:** Free high-quality sample libraries (pianos, strings, choirs — e.g. Clare Soloists) by Ivy Audio
- **URL:** https://ivyaudio.com
- **License:** free-proprietary (use OK, check EULA) — free for personal AND commercial use; sample redistribution prohibited (verified via official terms, 2026-10-07)
- **Free tier:** fully free; needs full Kontakt or SFZ player (versions vary)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Gorgeous free piano/strings. Check format per library (Kontakt full vs SFZ). [Wave 5]

#### Karoryfer Free Samples ✅ commercial-safe
- **What:** 19+ free sample libraries (Bear Sax, War Tuba, Meatbass double bass, Big Rusty Drums, etc.) by Karoryfer Samples
- **URL:** https://shop.karoryfer.com/pages/free-samples
- **License:** open-source/royalty-free — e.g. Bear Sax README: "open source instrument... Royalty-free for all commercial and non-commercial use" (verified via github.com/sfzinstruments/karoryfer.bear-sax + official free-samples page, 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Characterful folk/jazz instruments you can't get elsewhere (baritone sax from 1926 Conn, folk-punk tuba). Requires Plogue Sforzando (free) or any SFZ player. [Wave 5]

#### OTT (Xfer Records) ✅ commercial-safe
- **What:** Free multiband upward/downward compressor — the famous "OTT" preset as a plugin
- **URL:** https://xferrecords.com/freeware
- **License:** freeware — free-proprietary (use OK, check EULA); latest v1.37 (verified 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** The EDM/aggro-compression secret weapon, free. Useful for punchy score percussion/bass. [Wave 5]

#### Camel Crusher ✅ commercial-safe
- **What:** Free "British" distortion/compressor plugin (Camel Audio, discontinued 2015 — still distributed)
- **URL:** https://bedroomproducersblog.com/free-vst-plugins/camelcrusher/ (official dev site defunct since Apple acquisition; BPB hosts the last build with permission)
- **License:** freeware — free-proprietary (use OK, check EULA); caveat: 32-bit-era builds, macOS versions may need Rosetta/legacy support (verified 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Classic free distortion for grit in scores. Works best on Windows/legacy setups; test on current Mac before relying on it. [Wave 5]

#### Limiter No6 (VladG) ✅ commercial-safe
- **What:** Free modular mastering limiter (RMS comp + peak limiter + HF limiter + clipper + true-peak) by Vladislav Goncharov
- **URL:** https://vladgsound.wordpress.com/plugins/limiter6/
- **License:** freeware — free-proprietary (use OK, check EULA) (verified 2026-10-07)
- **Free tier:** fully free; Windows/Mac VST/AU
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Deep, surgical mastering limiter — the free final-limiter for score delivery masters. [Wave 5]

#### Auburn Sounds Free Editions ✅ commercial-safe
- **What:** Free editions of Panagement 2 (binaural panner/reverb), Couture (transient shaper/saturation), Graillon (pitch correction)
- **URL:** https://www.auburnsounds.com
- **License:** free-proprietary (use OK, check EULA) — Free Editions not time-limited, no-strings-attached per official pages (verified 2026-10-07); Full editions paid
- **Free tier:** free editions (feature-reduced: e.g. Panagement Free omits delay/PGMT-400 chip)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** Panagement Free is gold for 3D/animated-series spatial placement (binaural). Couture Free handles transient shaping. [Wave 5]

#### Melda MFreeFXBundle ✅ commercial-safe
- **What:** 37+ free effects (EQ, compressor, reverb, analyzers, pitch correction, saturation) by MeldaProduction
- **URL:** https://www.meldaproduction.com/MFreeFXBundle
- **License:** free-proprietary (use OK, check EULA) — "completely free" per official page; commercial plugins unlock extras (verified 2026-10-07)
- **Free tier:** fully free; account needed for installer
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** The biggest free FX bundle on the market — covers nearly every mixing need in the scoring chain. Slight nag-screen in free tier; fully usable. [Wave 5]

#### Kilohearts Essentials ✅ commercial-safe
- **What:** 30+ free snapin-style effects (EQ, delay, reverb, distortion, dynamics, pitch) by Kilohearts
- **URL:** https://kilohearts.com/products/kilohearts_essentials
- **License:** free-proprietary (use OK, check EULA) — free collection, verified via official page, 2026-10-07
- **Free tier:** fully free; lifetime free updates; growing collection
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Clean, low-CPU modern FX with a unified UI. Snapin hosts (Phase Plant etc.) are paid; the effects themselves are free standalone. [Wave 5]

#### MT Power Drum Kit ✅ commercial-safe
- **What:** Free realistic acoustic drum-kit sampler (groove library + fills generator) by Manda Audio
- **URL:** https://www.powerdrumkit.com
- **License:** free-proprietary (use OK, check EULA) — free download, activation screen skippable, no strings (verified via official site, 2026-10-07)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** Best free acoustic drums for rock/pop score beds; the groove/fill generator speeds up drum-track sketching. Windows/Mac VST/AU. [Wave 5]
## GPL/AGPL quarantine (research only — never wired into shipping paths)

#### Surge XT 🚫 QUARANTINED
- **What:** Open-source hybrid synthesizer (Surge Synth Team)
- **URL:** https://surge-synthesizer.github.io
- **License:** GPL-3.0 (verified via GitHub repo LICENSE, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL-3.0. Standalone use by musicians is fine, but copyleft bars any source/binary integration into studio tooling. Use Vital free tier instead. [Wave 5]

#### Dexed 🚫 QUARANTINED
- **What:** Open-source Yamaha DX7 FM synth clone (asb2m10)
- **URL:** https://asb2m10.github.io/dexed/
- **License:** GPL-3.0 (verified via GitHub repo LICENSE, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL-3.0. Great FM synth for score sound design when used standalone; do not integrate its code into shipping pipelines. [Wave 5]

#### Helm 🚫 QUARANTINED
- **What:** Open-source polyphonic synth by Matt Tytel
- **URL:** https://tytel.org/helm/
- **License:** GPL-3.0 (verified via GitHub repo LICENSE, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL-3.0. Standalone sound-design use OK; code integration barred. Prefer Vital free tier for wired synth work. [Wave 5]

#### Odin 2 🚫 QUARANTINED
- **What:** Open-source 24-voice polyphonic synth (TheWaveWarden)
- **URL:** https://www.thewavewarden.com/odin2
- **License:** GPL-3.0 (verified via GitHub repo LICENSE, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL-3.0. Excellent free synth for standalone scoring; not for code integration. [Wave 5]

#### ZynAddSubFX 🚫 QUARANTINED
- **What:** Open-source software synthesizer (additive/subtractive/FM engines)
- **URL:** https://zynaddsubfx.sourceforge.io
- **License:** GPL-2.0-or-later (verified via project license docs, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL. Powerful but deep; standalone use only. [Wave 5]

#### LMMS 🚫 QUARANTINED
- **What:** Open-source digital audio workstation (Linux MultiMedia Studio)
- **URL:** https://lmms.io
- **License:** GPL-2.0 (verified via GitHub repo LICENSE, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL-2.0. Free DAW for score sketching in the research lane; code/plugins ecosystem is copyleft. [Wave 5]

#### Ardour 🚫 QUARANTINED
- **What:** Open-source professional DAW
- **URL:** https://ardour.org
- **License:** GPL-2.0 (verified via project license, 2026-10-07)
- **Free tier:** free source builds; official binaries pay-what-you-want
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL-2.0. Research-lane DAW option; do not build shipping tooling on its codebase. [Wave 5]

#### Audacity 🚫 QUARANTINED
- **What:** Open-source audio editor/recorder (Muse Group)
- **URL:** https://www.audacityteam.org
- **License:** GPL-2.0-or-later (verified via GitHub repo LICENSE, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL. Fine as a standalone editor for researchers; barred from code integration. [Wave 5]

#### CHOW Tape Model 🚫 QUARANTINED
- **What:** Open-source analog tape-machine physical model (chowdsp / Jatin Chowdhury)
- **URL:** https://chowdsp.com/products.html#tape
- **License:** GPL-3.0 (verified via GitHub README license badge, 2026-10-07)
- **Free tier:** fully free & open-source
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL-3.0. Beautiful tape saturation for standalone scoring; code integration barred. [Wave 5]

#### Dragonfly Reverb 🚫 QUARANTINED
- **What:** Open-source reverb bundle (hall/room/plate/early reflections) by Michael Willis
- **URL:** https://github.com/michaelwillis/dragonfly-reverb
- **License:** GPL-3.0 (verified via upstream GitHub README "distributed under the GPL 3.0 License", 2026-10-07)
- **Free tier:** fully free & open-source; Linux/macOS/Windows
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** UNWIRED
- **Notes:** QUARANTINED — GPL-3.0. Excellent free reverb for standalone score mixing; use Valhalla Supermassive instead for shipped pipelines. [Wave 5]
