# TRIPPEDD Resource Pull Program — Wave 13, Lane C: caption/transcription SaaS free tiers + self-hosted caption tools

Lane scope: caption/transcription SaaS free tiers and self-hosted caption tools NOT already covered in `RESOURCE_CATALOG.md` (waves 1–12) or `docs/wave12/lane-c-captions.md`. Dedup verified via grep 2026-10-07 — skipped as already covered: Rev, Kapwing, TurboScribe, WhisperX, whisper.cpp, faster-whisper, openai/whisper, whisper-timestamped, insanely-fast-whisper, distil-whisper, whisper-jax, WhisperLive, whisper_streaming, whisperer (hclivess), WhisperSubTranslate, yt-whisper, whisper-subs, Open-Lyrics, CrisperWhisper, whisper-diarization, whisper-lrc, auto_subtitle (m1guelpf), subtitle (innovatorved), Buzz, aTrain, CaptionSubsGenerator, auto-subtitle-translate, SubtitleEdit, SubtitleComposer, pycaption, Gnome Subtitles, Subtitle Workshop, youtube-transcript-api, YouTube auto-captions, OpenSubtitles, oTranscribe, jev-subtitle-translator, ttconv, ttml2ssa, YTSubConverter, SCF, Aegisub packs, PyonFX, kashi, SOFA, Qwen3-ForcedAligner, DSAlign, subaligner, webrtcvad, TEN VAD, Moonshine, shortsmith, anime-whisper, Coqui STT, Descript, VEED, Clideo, Flixier, Maestra, Zeemo, Submagic, Captions (captions.ai), OpusClip, Deepgram, AssemblyAI, Speechmatics, Gladia, Sonix, Trint, HappyScribe, Otter.ai, Notta, MacWhisper, Rev AI, CapCut, ElevenLabs (platform entry covers it — Scribe STT omitted per lane brief), SubtitleBee (URL-cited only, no entry — now given a full entry).

NOTE on lane-brief "skip" items: Fireflies, Lemonfox, Rask, Podcastle, Riverside, StreamYard were listed in the brief as covered, but `grep -ri` over the entire `docs/` tree found ZERO hits — they are not in the catalog. Entries added below.

Badge key: ✅ commercial-safe · 🚫 NC-or-quarantine · ❓ unverified (ToS/free-tier terms unclear — what's unclear is noted per entry).

---

#### Fireflies.ai — meeting bot with unlimited free transcription ❓ unverified
- **What:** AI meeting assistant that joins Zoom/Google Meet/Teams calls, records, transcribes (100+ languages), and generates summaries, action items, and searchable transcripts; also takes audio/video uploads and has a public API.
- **URL:** https://fireflies.ai (terms: https://fireflies.ai/blog/fireflies-pricing-which-plan-is-right-for-you)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via official Fireflies pricing blog; ToS page not checked)
- **Free tier:** Unlimited transcription, 400 min storage per team, 20 one-time AI credits, limited integrations; Pro $10/seat/mo annual
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Most generous free *meeting* transcription found (uncapped meetings) — but it's a meeting bot, not a caption-file tool; SRT/export path needs checking before any caption use. Storage cap (400 min/team) is the real constraint. [Wave 13 Lane C]

#### Lemonfox.ai — EU Whisper large-v3 STT API, first month free ❓ unverified
- **What:** Developer STT API on Whisper large-v3: 100+ languages, speaker diarization, speech-to-text translation, immediate data deletion, EU-based processing; also TTS + image APIs.
- **URL:** https://lemonfox.ai (terms: https://www.aitechsuite.com/tools/14983)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via aitechsuite FAQ; official pricing page not fetched)
- **Free tier:** First month free for new users; then from $5/mo (10M credits ≈ 30 h transcription); extra credits $0.50/1M
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Trial-only free access (not a recurring free tier). Privacy angle (immediate deletion, EU processing) is its differentiator vs Gladia/Deepgram free credits. [Wave 13 Lane C]

#### Rask AI — video translation/dubbing with auto-subtitles, trial only ❓ unverified
- **What:** AI video localization: auto-transcription, subtitle translation in 130+ languages, voice cloning, multispeaker lip-sync, SRT download on paid tiers, dubbing API.
- **URL:** https://www.rask.ai (terms: https://www.techraisal.com/blog/rask-ai-review-2026/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via techraisal hands-on review; official pricing page not fetched)
- **Free tier:** Free trial — 3 included minutes, no credit card; NO exports on trial (no video, audio, or subtitle file). Creator from $60/mo (25 min)
- **Repo lane:** trippedd (captions)
- **Status:** not-started
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 3/5
- **Notes:** Trial is evaluation-only — no SRT export without paying, so it produces zero usable caption assets for free. Listed so no sibling lane wastes time on it. Lip-sync is the relevant benchmark if we ever dub Wizard Gang. [Wave 13 Lane C]

#### Castmagic — podcast audio → transcripts + content assets, trial only ❓ unverified
- **What:** AI podcast post-production: transcripts, show notes, timestamps, highlights, quotes, social posts from audio/video uploads; speaker ID, timestamping, 60+ languages on higher tiers.
- **URL:** https://www.castmagic.io (terms: https://www.grabon.in/castmagic-coupons/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via grabon pricing FAQ; official pricing page not fetched)
- **Free tier:** Free trial only (older sources: 30 min transcription/week on trial; current trial size unclear), no credit card; no permanent free version. Hobby from $39/mo (300 min/mo)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** No SRT/caption-file export documented on trial — evaluate transcript export formats before any use. Rising Star adds API for automation. [Wave 13 Lane C]

#### Podcastle — browser podcast studio with text-based editing ❓ unverified
- **What:** All-in-one browser podcast studio: multitrack remote recording, automatic transcription, text-based audio editing, Magic Dust audio cleanup, 7,000+ music/SFX tracks, 4K video recording.
- **URL:** https://podcastle.ai (terms: https://podcastpontifications.com/helpful-info/async-podcastle-pricing/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via podcastpontifications pricing breakdown; official pricing page not fetched)
- **Free tier:** Free plan — unlimited audio recording (MP3 160kbps); transcription limited to 1 hour LIFETIME (not monthly); video exports watermarked 720p. Essentials from $11.99/mo (10 h transcription/mo)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The lifetime (not monthly) transcription cap is the gotcha — 1 hour total, then it's gone. Text-based editing is the Descript-parallel worth knowing. No public API. [Wave 13 Lane C]

#### Riverside.fm — studio recording with AI transcripts + styled captions ❓ unverified
- **What:** Remote studio recording (local 4K video / WAV per guest), automatic AI transcription in 100+ languages (SRT/TXT download), text-based editor, caption styling/positioning, Magic Clips for social cutdowns.
- **URL:** https://riverside.fm (terms: https://riverside.fm/blog/best-transcription-software-for-mac)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via official Riverside blog; official pricing page not fetched)
- **Free tier:** Free plan — 2 h multitrack recording/mo, 720p, Riverside watermark; built-in AI transcription is paid (Pro $24/mo). Separate free online transcription tool exists on riverside.fm with its own limits.
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Caption styling (font/position) + transcript→caption workflow is directly relevant to episode masters; free tier watermark makes it draft-only. [Wave 13 Lane C]

#### StreamYard — browser live studio, AI captioned clips on free ❓ unverified
- **What:** Browser-based live-streaming studio (multistream, guests, overlays); AI clips turn recordings into captioned vertical clips; transcript downloads on higher tiers.
- **URL:** https://streamyard.com (terms: https://www.learningrevolution.net/streamyard-vs-zoom/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via learningrevolution comparison; official pricing page not fetched)
- **Free tier:** Free plan — 20 h streaming/mo, 720p, StreamYard watermark, 1 destination; 2 AI clips/mo (captioned vertical clips); full transcript download only on Advanced plan
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Not a transcription tool — the only caption value is 2 AI-generated captioned clips/mo. Transcript is paywalled. Marginal for caption pipeline; listed for completeness. [Wave 13 Lane C]

#### Tactiq — bot-free Chrome-extension live transcription ❓ unverified
- **What:** Chrome extension that captures live captions inside Google Meet / Zoom / Teams without sending a bot into the call; 60+ languages, AI summaries, action items, exports to Google Docs/Notion/Slack/HubSpot.
- **URL:** https://tactiq.io (terms: https://tactiq.io/learn/google-meet-alternatives — official)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via official Tactiq page; free tier: 10 transcripts/mo, 5 AI credits/mo, no credit card)
- **Free tier:** 10 meeting transcripts/mo, 5 AI summary credits/mo, live captions, Google Docs & Notion exports. Pro $8/user/mo annual (unlimited transcripts)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Transcript-only capture — no audio/video recording, so nothing to caption from. Useful as a live-transcript reference tool; SOC-2 Type II, no training on meeting data. [Wave 13 Lane C]

#### ScriptMe — production-oriented transcription/subtitling with SRT/VTT export ❓ unverified
- **What:** AI transcription + subtitle editor aimed at film/TV production (ScriptMe AB, Sweden): 30+ languages, styled subtitle editing, SRT/VTT/burned-in export, API, enterprise collaboration.
- **URL:** https://scriptme.io (terms: https://www.capterra.in/software/1064367/scriptme)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via Capterra; official pricing page not fetched)
- **Free tier:** Free version + free trial available (exact free minutes unclear); paid from $45/mo (pay-as-you-go $29/h)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Production pedigree (timecoding, subtitle styling) is the interesting bit; free-tier size needs confirming on scriptme.io/pricing before planning any use. [Wave 13 Lane C]

#### Vocalmatic — 30-min free transcription; reliability reports are dire ❓ unverified
- **What:** Simple upload-a-file AI transcription (mp3/flac/wav/mp4/mov/ogg/webm), email-delivered transcripts with an editor, subtitle support, API; founded 2017, Canada.
- **URL:** https://vocalmatic.com (terms: https://sourceforge.net/software/compare/Smart-Scribe-vs-Vocalmatic/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via sourceforge comparison; official pricing page not fetched)
- **Free tier:** 30 minutes of complimentary automatic transcription; then ~$15/h pay-as-you-go
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** ⚠️ HONESTY FLAG: multiple recent user reviews call the service broken/scam-adjacent — uploads stuck "pending" forever, no support response, while payments process fine. Do NOT route caption work here; listed only so nobody rediscovers it. [Wave 13 Lane C]

#### Pictory — AI video builder; transcript/subtitle export free only during trial ❓ unverified
- **What:** Script/URL/audio/PPT → captioned video builder with stock library (Getty/Storyblocks), ElevenLabs voices, text-based editing, AI highlight clips; transcript generator exports subtitles as SRT/VTT ZIP or burned-in.
- **URL:** https://pictory.ai (terms: https://pictory.ai/blog/transcript-generator — official)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via official Pictory blog; official pricing page not fetched)
- **Free tier:** No permanent free plan — 14-day trial: 3 video projects, watermarked exports; transcript generator free during trial (files up to 5 GB / 180 min). Starter from $25–29/mo
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Trial-only — the 180-min transcript allowance is the usable bit, but watermarked video and no recurring free tier make it a one-shot. [Wave 13 Lane C]

#### Zubtitle — social auto-captions, free-forever 2 videos/mo ❓ unverified
- **What:** Focused auto-caption tool for talking-head/social video: AI subtitles in 60+ languages, styled burned-in captions, supertitles/progress bar/logo, crop/resize for Reels/Shorts/TikTok, SRT + TXT download per video.
- **URL:** https://zubtitle.com (terms: https://seektool.ai/ai/zubtitle-com)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via seektool pricing; official pricing page not fetched)
- **Free tier:** "Bootstrapper" free forever — 2 videos/mo, 720p, Zubtitle watermark, SRT download included. Guru from $19/mo (10 videos)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** One of the few caption-first tools with a real recurring free tier AND SRT download on free. Watermark on video exports — but SRT is what the caption lane needs. [Wave 13 Lane C]

#### Vizard — AI clipper with animated captions, 60 credits/mo free ❓ unverified
- **What:** Long-video → viral-clips engine: AI highlight detection, auto-captions in 30+ languages, caption translation to 100+ languages, speaker detection, auto-reframe 9:16, REST API on paid tiers.
- **URL:** https://vizard.ai (terms: https://appscribed.com/software/vizard-ai-video-editing-review/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via appscribed review; official pricing page not fetched)
- **Free tier:** 60 credits/mo (~60 min input), 1 GB files, 720p, 10-min export cap, 3-day storage, watermarked, 1 social account. Creator from ~$14.50/mo annual
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Free tier is a trial in practice (watermark + 3-day storage). Caption translation (not dubbing) is the useful feature; no caption-file export documented — check before use. [Wave 13 Lane C]

#### Temi — Rev's pay-as-you-go transcription, 45-min free trial ❓ unverified
- **What:** Lean AI transcription by Rev: fast single-engine transcription, filler-word removal, speaker ID, text editor; exports Word/PDF/SRT/VTT/TXT; mobile apps; developer API. English-only.
- **URL:** https://www.temi.com (terms: https://speakai.co/alternatives/speak-ai-vs-temi-a-more-useful-temi-alternative/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via speakai comparison; official pricing page not fetched)
- **Free tier:** One 45-minute transcript free (trial); then $0.25/min pay-as-you-go, no subscription, no minimum
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Trial-only. SRT/VTT export is included (unlike some trial tiers), so the single free transcript is actually usable as a caption source. English-only is the limit. [Wave 13 Lane C]

#### Simon Says — transcription/subtitling with NLE integrations ❓ unverified
- **What:** Production transcription + translation in 100 languages with direct export into Adobe Premiere, Final Cut Pro, DaVinci Resolve, and Avid (timecoded transcripts, visual subtitle editor, speaker separation, collaborative web editor).
- **URL:** https://www.simonsaysai.com (terms: https://aitools.inc/tools/simon-says-ai)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via aitools.inc; official pricing page not fetched)
- **Free tier:** Free trial (older reviews: 30-min credit for new users; current size unclear); pay-as-you-go from $15; Creator $16/mo (2 h credit/mo)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The NLE-native export (Premiere/FCP/DaVinci/Avid) is the standout — unique in this wave for an edit-pipeline fit. Trial size needs confirming; Capterra rating is weak (1.6/5) — trial before trust. [Wave 13 Lane C]

#### Grain — video-first meeting notetaker, generous free tier ❓ unverified
- **What:** Video-first AI notetaker: bot joins Zoom/Meet/Teams, records video, transcribes with speaker labels, AI summaries with chapters/action items, shareable video clips from transcript moments, CRM sync, 25-language transcription.
- **URL:** https://grain.com (terms: https://grain.com/blog/best-meeting-transcription-software — official)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via official Grain blog; official pricing page not fetched)
- **Free tier:** Free plan — unlimited AI meeting notes/recordings (one Notetaker seat); some reviewers report a 5-recording cap — confirm live. Starter from $19/user/mo
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Transcript→shareable-clip workflow is adjacent to caption cutdowns. AssemblyAI speech models under the hood (already catalogued). Conflicting free-cap reports — verify before relying on it. [Wave 13 Lane C]

#### Fathom — unlimited free recording + transcription, AI summaries capped ❓ unverified
- **What:** AI meeting notetaker: bot joins Zoom/Meet/Teams, unlimited recording and transcription (38 languages, auto-detect), AI summaries in ~30s, clickable highlights linked to video moments, Ask Fathom search, clip cutting, desktop app + Chrome extension.
- **URL:** https://fathom.video (terms: https://get-alfred.ai/blog/fathom-pricing)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via get-alfred pricing review; official pricing page not fetched)
- **Free tier:** Unlimited recordings, unlimited transcription, unlimited storage; advanced AI summaries capped at 5 calls/mo (basic chronological template after). Premium $16/user/mo annual
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strongest free tier in the meeting category (unlimited recording AND transcription at $0). 38-language transcription with auto-detect is genuinely useful; transcripts link to video timestamps — closest thing to a free caption-timing source here. [Wave 13 Lane C]

#### tl;dv — unlimited free recording/transcription, AI notes lifetime-capped ❓ unverified
- **What:** Meeting recorder/transcriber (Zoom/Meet/Teams, 30+ languages): timestamped highlights, shareable clips, searchable library; bot or bot-free desktop capture.
- **URL:** https://tldv.io (terms: https://curatahub.com/blog/tldv-pricing-explained)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via curatahub pricing review; official pricing page not fetched)
- **Free tier:** Unlimited recordings + transcripts; AI notes capped at 10 LIFETIME (not monthly), 10 Ask AI queries lifetime, recordings deleted after 3 months, 5 file uploads total. Pro from $18/user/mo annual
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The lifetime (not monthly) AI-note cap and 90-day recording deletion are the gotchas — treat free as a recorder, not an archive. Clip-and-share is the caption-adjacent feature. [Wave 13 Lane C]

#### Granola — bot-free AI notepad, free Basic with 30-day history ❓ unverified
- **What:** Meeting notepad that captures system audio on-device (no bot joins the call), merges your typed notes with the transcript into structured AI notes; AI chat across meetings, templates, shared folders; macOS/Windows/iOS/Android.
- **URL:** https://www.granola.ai (terms: https://scored.tools/blog/granola-review-2026/ — figures sourced from granola.ai/pricing)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via scored.tools review of official pricing; official pricing page not fetched)
- **Free tier:** Basic free — AI meeting notes, AI chat, templates, shared folders, multi-language; only last 30 days of history visible (some reviews report a 25-meeting lifetime cap — confirm live). Business $14/user/mo
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** No-bot capture is the differentiator; conflicting free-cap reports (30-day history vs 25-meeting lifetime) — verify on granola.ai/pricing. Notepad-first, not a caption tool. [Wave 13 Lane C]

#### Read AI — meeting AI with 5 free meetings/mo ❓ unverified
- **What:** Meeting assistant unifying meetings, email, and messaging into a searchable knowledge graph: real-time transcription, AI summaries, meeting coach, topic readouts; 20+ languages; iOS app for in-person capture.
- **URL:** https://www.read.ai (terms: https://www.saasworthy.com/product/read-ai-transcription/pricing)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via saasworthy pricing; official pricing page not fetched)
- **Free tier:** 5 meetings/mo with full AI summaries, real-time transcription, notes, unlimited enterprise search, meeting coach; no credit card. Pro $15/user/mo (unlimited transcripts)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Thin free allowance (5 meetings/mo). Included because the cross-meeting search is a novel reference pattern; not a caption pipeline tool. [Wave 13 Lane C]

#### Fellow — AI meeting notes, 5 free notes lifetime/user ❓ unverified
- **What:** Meeting management + AI assistant: agendas, recording (bot or botless desktop capture), transcription in 90+ languages, AI summaries with chapters, action items, transcript redaction, 50+ integrations (Salesforce/HubSpot/Zapier), API; SOC 2 Type II.
- **URL:** https://fellow.ai (terms: https://www.fellow.ai/pricing?ref=saaspo.com — official)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via official Fellow pricing page)
- **Free tier:** 5 AI notes + 5 AI recordings LIFETIME per user, audio/video uploads, AI transcription/summary/action items. Team $7/user/mo annual
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Lifetime (not monthly) caps make this evaluation-only. Transcript redaction + 90+ languages are the notable features; security posture is the best in this wave. [Wave 13 Lane C]

#### Circleback — unlimited free meeting transcription, 30-day history ❓ unverified
- **What:** Meeting notetaker (bot or bot-free desktop app): speaker-labeled transcripts, AI notes, action items, transcript search, mobile + Apple Watch recording, Slack/Linear integrations, API/MCP/CLI access; 100+ languages.
- **URL:** https://circleback.ai (terms: https://techcrunch.com/2026/08/31/meeting-notetaker-circleback-adds-a-free-tier-to-attract-more-customers/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via TechCrunch, Aug 2026; official pricing page not fetched)
- **Free tier:** Unlimited meetings + transcription, AI notes, action items, Ask Circleback, 30-day meeting/recording history, limited API/MCP/CLI. Pro from $15/user/mo annual
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Free tier launched Aug 2026 (TechCrunch-confirmed) — generous and current. API + MCP + CLI on free is unusual and worth noting for automation experiments. [Wave 13 Lane C]

#### Avoma — meeting/revenue intelligence; free plan status CONFLICTED ❓ unverified
- **What:** AI meeting assistant for revenue teams: recording, real-time transcription (50+ languages), AI notes, conversation intelligence, deal boards, coaching scorecards, CRM sync (Salesforce/HubSpot), dialer integrations.
- **URL:** https://www.avoma.com (terms: https://meetgeek.ai/blog/avoma-review and https://www.ricavi.ai/blog/avoma-pricing-2026 — conflict noted)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via two review sources; official pricing page not fetched)
- **Free tier:** CONFLICT: ricavi.ai reports a free Starter plan (AI notes, basic transcription, 20 meetings/mo cap); meetgeek.ai (Aug 2026) reports NO free plan, only an unrestricted 14-day trial. Do not rely on either — check avoma.com/pricing live.
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Conflict between sources is itself the finding — treat as trial-only until verified at source. Revenue-intelligence focus, not caption-relevant anyway. [Wave 13 Lane C]

#### Mem — AI note workspace; meeting transcription in beta on paid ❓ unverified
- **What:** AI note-taking workspace with semantic auto-organization: capture by voice/during calls/web, Mem Chat over your notes, meeting briefs (beta) that record, transcribe, and summarize calls; desktop apps capture system audio.
- **URL:** https://mem.ai (terms: https://nubiapage.com/mem-ai-review-2026-pricing-app-alternatives-free-plan/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via nubiapage review; official pricing page not fetched)
- **Free tier:** 25 notes/mo + 25 AI chat messages/mo, basic search. Meeting record/transcribe/summarize ("meeting briefs") is a Pro beta feature (~$12–15/mo)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Marginal for captions — transcription is paywalled in beta. Included for the lane-candidate-pool sweep; deprioritize. [Wave 13 Lane C]

#### Sembly — meeting AI with free Personal plan ❓ unverified
- **What:** AI meeting assistant: records/transcribes meetings (~94% claimed accuracy), auto meeting minutes, summaries with action items, sentiment analysis, CRM integrations, Glance/briefing features.
- **URL:** https://sembly.ai (terms: https://www.fahimai.com/sembly-vs-mem-ai)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via fahimai comparison; official pricing page not fetched)
- **Free tier:** Free Personal plan; Professional $10/mo, Team $20/user/mo (paid unlocks sentiment analysis, CRM integration)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** "Sembly" grep hits in the catalog were all "AssemblyAI" substrings — no standalone Sembly entry existed. Free Personal plan details are thin in sources; verify live before use. [Wave 13 Lane C]

#### SubtitleBee — caption-first subtitler; free tier disables downloads ❓ unverified
- **What:** Online subtitle generator: upload video/URL → AI subtitles (claimed 95% on clear speech), editor, burned-in styled subtitles, SRT/ASS/VTT/TXT export, subtitle translation in 100+ languages, supertitles/progress bar/logo, crop/resize for Shorts/Reels.
- **URL:** https://subtitlebee.com (terms: https://subtitlebee.com/pricing — official)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via official SubtitleBee pricing page)
- **Free tier:** 1 video up to 10 min to try the editor — DOWNLOADS DISABLED on free (no SRT/file export until paid). Starter from $19/mo (240 min/mo, watermark-free)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Only URL-cited (in Kapwing's entry), never given a full entry — hence included. The no-downloads-on-free rule makes the free tier evaluation-only; the minute-metered paid plans are the honest comparison point vs Kapwing. [Wave 13 Lane C]

#### EasySub — auto-subtitles, 30-min free + free translation forever ❓ unverified
- **What:** Web auto-subtitle generator: 150+ languages, timeline editor (timing/text/position/split), SRT/ASS/TXT download, subtitle translation, YouTube-URL import, no-upload-limit positioning for long videos.
- **URL:** https://www.easysub.com (terms: https://aivideotoolspro.com/detail/easyssub)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via aivideotoolspro; official pricing page not fetched)
- **Free tier:** 30 min free transcription (some sources say 15 min — confirm live); SRT download included on free; subtitle translation free forever. Pay-as-you-go ~$0.10–0.20/min after
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Stronger than SubtitleBee's free tier (SRT download works on free). Free-translation-forever is a real differentiator for multilingual caption variants. Has an API. [Wave 13 Lane C]

#### Zencastr — podcast recorder, free tier includes unlimited transcription (reports conflict) ❓ unverified
- **What:** Browser podcast recording: local 16-bit 48k WAV per guest, 4K video, separate tracks, searchable multilingual transcripts, AI editing, hosting/distribution.
- **URL:** https://zencastr.com (terms: https://pixelpulseservices.com/zencastr-review-2025/)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via pixelpulse review of official pricing; official pricing page not fetched)
- **Free tier:** "Vibecastr" free — CONFLICT: Sept-2026 review reports unlimited recording + unlimited transcription hours; other reviews report 8 h/mo, 2 guests. Confirm live. Paid from $24/mo
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** If the unlimited-transcription reading is current, this is a strong free caption source for dialogue-heavy content. Verify before planning. [Wave 13 Lane C]

#### invideo — AI video builder; free tier has NO commercial rights 🚫 NC-or-quarantine
- **What:** Prompt → video platform: script, 16M+ stock library, AI voiceover (50+ languages), auto-subtitles, transitions; subtitles editable and exported with final file on all tiers.
- **URL:** https://invideo.io (terms: https://max-productive.ai/ai-tools/invideo-ai/)
- **License:** Proprietary SaaS — free plan EXPLICITLY excludes commercial usage rights (verified 2026-10-07 via max-productive review)
- **Free tier:** ~10 AI generation min/week, 4 video exports/week, watermarked, NO commercial usage rights. Plus from $28/mo removes watermark + grants commercial rights
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** 🚫 Free tier is evaluation-only by license — watermarked exports cannot legally be used for business/monetized purposes. Only paid tiers are pipeline-relevant. Listed as the wave's clearest NC case. [Wave 13 Lane C]

#### Aiko — Sindre Sorhus on-device Whisper transcription (iOS/macOS) ❓ unverified
- **What:** Native Swift/SwiftUI transcription app: on-device Whisper (100 languages), audio+video files, sentence-segmented transcripts, export to JSON/CSV/subtitles, Shortcuts automation; no live transcription, no in-app editing, no diarization.
- **URL:** https://sindresorhus.com/aiko (terms: https://www.saashub.com/compare-otter-ai-vs-aiko)
- **License:** Proprietary (closed-source App Store app) — terms unverified (verified 2026-10-07 via saashub/HN references; App Store page not checked)
- **Free tier:** CONFLICT: HN describes a free App Store app; dataconomy reports paid from $20/mo; slashdot reports a free 14-day TestFlight trial. Confirm on the App Store listing.
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Not open-source despite appearing in open-source tool lists — do not file it as one. On-device privacy is the draw; MacWhisper (already catalogued) is the fuller-featured sibling from the same developer. [Wave 13 Lane C]

#### GoTranscript — human+AI transcription; small free trial ❓ unverified
- **What:** Transcription service with human (99.4% claimed, from $0.84/min) and AI ($0.06–0.10/min) tiers; 40–50+ languages; exports TXT/DOCX/PDF + SRT/VTT/SCC/DFXP subtitle formats; timestamps, speaker labels, verbatim options.
- **URL:** https://gotranscript.com (terms: https://www.thinkingineducating.com/is-gotranscript-a-reliable-choice-for-your-transcription-needs-2/ and http://gotranscript.com/en/blog/the-most-affordable-transcription-services-for-audio-and-video — official)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via review + official GoTranscript blog; official pricing page not fetched)
- **Free tier:** Free trial only — CONFLICT: 30 min free automated transcription (review) vs 5-min trial (official blog) vs 10-min business trial (coupon page). Confirm live.
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Pro subtitle formats (SCC/DFXP) are the broadcast-relevant bit; human tier exists for legally load-bearing accuracy. Trial size is genuinely unclear — verify, don't quote a number. [Wave 13 Lane C]

#### Cockatoo — fast transcription with working free tier ❓ unverified
- **What:** Drag-and-drop audio/video transcription (90+ languages): in-browser editor, real-time transcription option, export SRT/DOCX/PDF/TXT, secure encrypted handling; aimed at interviews, lectures, meetings, documentary producers.
- **URL:** https://cockatoo.ai (terms: https://www.toolify.ai/compare/cockatoo-vs-shots-maker)
- **License:** Proprietary SaaS — commercial terms per ToS unverified (verified 2026-10-07 via toolify comparison; official pricing page not fetched)
- **Free tier:** Free — 2–3 uploads/mo, 20–30 min max transcript length (sources differ), 90+ languages, SRT export included. Pro from ~$12–15/mo
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Small but genuinely usable free tier with SRT export — comparable to EasySub's. Paid-plan pricing varies across sources ($12–29/mo) — confirm live. [Wave 13 Lane C]

---

## Self-hosted caption tools (licenses verified from repo LICENSE / README)

#### jhj0517/Whisper-WebUI — Gradio subtitle workbench on Whisper ✅ commercial-safe
- **What:** Gradio web UI for easy subtitling: switchable backends (openai/whisper, faster-whisper default, insanely-fast-whisper); subtitles from files, YouTube, microphone; SRT/WebVTT/TXT output; NLLB/DeepL text translation; Silero VAD; pyannote speaker diarization (needs HF token + terms acceptance); UVR vocal separation; REST API backend; Docker + Pinokio installers.
- **URL:** https://github.com/jhj0517/Whisper-WebUI (terms: repo README + LICENSE)
- **License:** Apache-2.0 (verified 2026-10-07 via GitHub repo license metadata: "Apache License 2.0")
- **Free tier:** Self-hosted — free, no limits (GPU recommended; CUDA 12+ for NVIDIA)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strongest self-hosted caption workbench found this wave (2,890 stars, 1,447 commits): VAD + diarization + translation in one UI, plus a REST API for pipeline wiring. Known gotcha: Docker build fragility (setuptools/pkg_resources issue reported upstream). [Wave 13 Lane C]

#### aadnk/whisper-webui — faster-whisper Gradio UI + CLI ❓ unverified
- **What:** Lightweight faster-whisper web UI (Gradio) + CLI: parallel CPU/GPU transcription, Silero VAD options, YouTube/file/URL input, config-file driven; deployed as a Hugging Face Space.
- **URL:** https://huggingface.co/spaces/aadnk/faster-whisper-webui (terms: https://huggingface.co/spaces/aadnk/whisper-webui/blob/main/README.md)
- **License:** Apache-2.0 per Space metadata (verified 2026-10-07 via HF Space README frontmatter `license: apache-2.0`; repo LICENSE file not separately fetched — hence ❓)
- **Free tier:** Self-hosted — free, no limits; HF Space demo usable without install
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The "whisper-webui"/"faster-whisper-webui" slot the brief asked to check — no catalog entry existed, so it's covered here. Lighter than jhj0517's (no diarization/translation UI); pick jhj0517 for features, aadnk for speed/simplicity. [Wave 13 Lane C]

#### sherpa-onnx (k2-fsa) — streaming/offline ASR runtime, Apache-2.0 ✅ commercial-safe
- **What:** ONNX-based speech runtime: streaming + non-streaming ASR, TTS, Silero VAD, keyword spotting, speaker ID/diarization; C++/Python/Swift/Kotlin bindings, iOS/Android/desktop; runs SenseVoice, Paraformer, Whisper, Parakeet models.
- **URL:** https://github.com/k2-fsa/sherpa-onnx (terms: repo LICENSE)
- **License:** Apache-2.0 (verified 2026-10-07 via repo LICENSE; multiple downstream THIRD_PARTY_NOTICES confirm)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** License nuance (honest): runtime is Apache-2.0, but prebuilt TTS binaries embed eSpeak-NG (GPL-3.0) for phonemization — ASR-only caption use avoids the GPL path entirely. Streaming ASR makes it the candidate for live-caption experiments. [Wave 13 Lane C]

#### FunASR (modelscope) — Alibaba production ASR toolkit ✅ commercial-safe
- **What:** Industrial ASR toolkit (Alibaba DAMO/Speech Lab, 16k+ stars): Paraformer/Conformer models, VAD → ASR → punctuation → diarization pipeline, streaming + offline, WebSocket/REST/gRPC servers, Docker one-command deploy, ONNX edge runtime, SenseVoice multilingual models.
- **URL:** https://github.com/modelscope/FunASR (terms: repo README + LICENSE)
- **License:** Apache-2.0 code (verified 2026-10-07 via repo; linuxlinks + production-ML references); model weights under FunASR Model License v1.1 — commercial use OK with attribution to Alibaba/FunAudioLLM
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Attribution requirement on the model weights is the only commercial-use condition — keep the attribution in any derived artifacts. Full VAD+ASR+punct+diarization in one Docker image is the fastest path to a self-hosted caption server. Already partially referenced via auto-subtitle-translate (FunASR-based) but never given its own entry. [Wave 13 Lane C]

#### OpenWhispr — open-source local-first Whisper dictation + meeting transcription ✅ commercial-safe
- **What:** Privacy-first cross-platform (macOS/Windows/Linux) voice-to-text: hotkey dictation, local Whisper/Parakeet/Orukeet models (audio never leaves device), meeting recording + transcription + notes, speaker identification, BYOK cloud fallback, webhooks/API for pipeline integration.
- **URL:** https://github.com/OpenWhispr/openwhispr (terms: repo README + LICENSE)
- **License:** MIT (verified 2026-10-07 via raw LICENSE fetch: "MIT License, Copyright (c) 2024 OpenWhispr Team")
- **Free tier:** Self-hosted/open — free, no limits; local transcription free, cloud is BYOK (pay providers directly, ~$0–5/mo typical)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Chosen over "Whispering" (license unpinable) — OpenWhispr is the verified-MIT local-first alternative to MacWhisper/WisprFlow/Granola. Webhooks + API make it wireable into the caption pipeline; meeting transcription covers the dialogue-capture case. [Wave 13 Lane C]

---

## Quarantine candidates

#### YounessMoustaouda/faster-whisper-generate-srt-subtitles — GPL-3.0, standalone-tool/research only 🚫 NC-or-quarantine
- **What:** Minimal faster-whisper → .srt generator script (single `generate-srt.py`, CLI, 3 commits, 22 stars).
- **URL:** https://github.com/YounessMoustaouda/faster-whisper-generate-srt-subtitles (terms: repo LICENSE)
- **License:** GPL-3.0 (verified 2026-10-07 via GitHub repo license metadata) — copyleft; not usable inside proprietary TRIPPEDD tooling
- **Free tier:** Self-hosted — free
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** 🚫 Quarantined per lane rule (GPL-3.0 → no ✅ badge). Research/standalone reference only; the MIT/Apache alternatives above (jhj0517, aadnk, faster-whisper itself) cover the same job without copyleft. [Wave 13 Lane C]

---

## Lane summary — Wave 13 Lane C

- **Entries:** 37 new `####` rows (32 SaaS + 5 self-hosted), plus 1 quarantine row (GPL-3.0) — 38 total.
- **Badge split:** ✅ commercial-safe × 4 (jhj0517/Whisper-WebUI, sherpa-onnx, FunASR, OpenWhispr) · 🚫 NC-or-quarantine × 2 (invideo — no commercial rights on free; YounessMoustaouda faster-whisper-generate-srt — GPL-3.0) · ❓ unverified × 32 (all remaining SaaS — ToS commercial terms and/or free-tier details unverified at the vendor's own pricing page; plus aadnk/whisper-webui, whose Apache-2.0 comes from Space metadata only).
- **Most generous free tiers found:** Fathom (unlimited recording + transcription + storage, AI summaries 5 calls/mo) · Fireflies (unlimited transcription, 400 min storage/team) · Circleback (unlimited transcription, 30-day history, API/MCP/CLI on free) · tl;dv (unlimited recording/transcription, 3-mo retention, 10 AI notes lifetime) · EasySub (30 min free + SRT download on free + translation free forever) · Zubtitle (2 videos/mo free with SRT download).
- **Notable finds / gotchas:** Rask trial exports NOTHING (evaluation-only) · SubtitleBee disables downloads on free · Podcastle transcription is 1 hour LIFETIME · Fellow/Granola free caps are lifetime or 30-day, not monthly · Vocalmatic has active scam/broken-service reports — do not use · Avoma, Zencastr, Granola, GoTranscript, EasySub, Aiko all have conflicting free-tier reports between sources — verify live before planning · ElevenLabs Scribe omitted per lane brief (platform entry already covers ElevenLabs) · Fireflies/Lemonfox/Rask/Podcastle/Riverside/StreamYard were listed as covered in the lane brief but `grep -ri` over all of `docs/` found zero hits — entries added.
- **No signups, API keys, or downloads** beyond LICENSE/README fetches were performed. No commits made — coordinator merges.
