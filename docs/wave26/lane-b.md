# Wave 26 Lane B — caption burn-in SaaS alternatives + self-hosted caption packaging tools (2026-10-07)

**Worker:** subagent Lane B · **Branch:** `wave26-lane-b` · **Worktree:** `/tmp/w26-lane-b`

## Entry count
- **55 new `####` entries** appended under `## Wave 26 — Lane B` at the end of `docs/RESOURCE_CATALOG.md` (2,508 → 2,563 headings).
- 12 self-hosted/open-source caption packaging tools, 3 freeware packaging tools, 40 SaaS entries (live captioning/translation, pro subtitling software, captioning services, AI editors with burn-in, screen recorders, video API/hosting, free live captioning).
- **Quarantine rows 239–243** added to `docs/LICENSE_QUARANTINE.md`: Performous (GPL-2.0-or-later), Vocaluxe (GPL-3.0), sc0ty/subSync (GPL-3.0), Subler (GPLv2), stream_closed_captioner_phoenix (GPL-3.0).

## Verification method
- Every license verified upstream on 2026-10-07: GitHub API `spdx_id` for repos (rate limit 60/hr, no issues); vendor pricing pages and directory sources for SaaS, all via text-fetch (browser.search / browser.open). Every URL in entries is verbatim from search-result output — no constructed URLs.
- Badges: ✅ only where a permissive license or genuinely free tier was confirmed; ⚠️ for weak copyleft / conditional free tiers (Belle Nuit LGPL, Wisecut free-tier-is-preview); ❓ where terms came from secondary sources or were unverifiable; 🚫 for the 5 GPL/AGPL repos (quarantined).
- Conflicting sources documented in Notes, not resolved by fiat: Kamua (free plan disputed), 2short.ai (watermark disputed), Scribie (trial disputed), CaptionHub (£40/mo vs $27,937/yr).

## Dedup notes
- Pre-append greps run against all 2,508 catalog headings. False-positive substring hits investigated: "Hybrid" → existing entry was HAT (Hybrid Attention Transformer), unrelated — new entry named "Hybrid (Selur video encoder)"; "Tella" → matched Blender-StellarToon ("stellar"), unrelated — new entry named "Tella (screen recorder)"; "subSync" → ffsubsync/VisualSubSync, different tools — new entry named "subSync (sc0ty)".
- Already covered and NOT re-listed: all Waves 12/14/17 caption finds, Wave 24 Lane B long tail, xy-VSFilter/xySubFilter (quarantine 198), VisualSubSync (197), ffsubsync, telxcc (236), QCTools (235), AtomicParsley (238), Subtitle Edit, Aegisub.
- Researched but dropped as unverifiable within budget: Annotation Edit (no substantive sources), DVDStyler/DeVeDe/Bombono/AVStoDVD/TCAX/mkclean/scc2srt (could not ground).

## Honest negatives
- **Qlip.ai** — defunct: acquired by Livestorm May 2026, now a €2,000/yr paid add-on. Listed as an honest negative so future waves don't re-research it.
- **Screen Studio** — no free tier; export paywalled at $29/mo or $108/yr (verified via two independent Sept-2026 sources). Its open-source MIT clone **OpenScreen** (this wave) is the recommended path.
- **Wisecut** — free tier processes 60 min/mo at 360p but downloads require paid; badge ⚠️, effectively trial-only for exports.

## Follow-up resolutions (Wave-25)
1. **Gladia free-tier discrepancy** — RESOLVED, entry stands. Re-fetched https://www.gladia.io/pricing (2026-10-07): €50 one-time no-expiry credits (~80+ h) confirmed. The "~10 hrs/month" secondary-source claims were wrong/stale. Also confirmed: Growth tier now shows automatic training opt-out (free/Starter does not). Re-verification note appended to the entry in place; no history rewritten.
2. **Amara AGPL-to-proprietary badge audit** — MAJOR CHANGE FOUND. Public Workspace closure announced 2026-03-27, closed 2026-04-30 (per Wikipedia, crawled 2026-10-05); thousands of community subtitles deleted unless transferred. amara.org homepage (2026-10-07) shows only Editor / On Demand / Enterprise. License status unchanged (still proprietary; no re-open-sourcing found). Badge changed ✅→⚠️ in place, free-tier line corrected, correction note appended.
3. **Type Studio vendor URL** — vendor domain confirmed as **typestudio.co** via two independent slashdot.org directory pages (2026-10-07): Company Type Studio, founded 2020, Germany, pricing from $14/mo, Free Version: Yes, Free Trial: Yes. Entry URL updated in place. **Live-browser visit STILL DEFERRED**: generic subagents cannot operate a live browser (per standing instructions). The ❓ badge and "do not wire until free-tier limits verified" caveat are retained; a live visit to typestudio.co's pricing page must be delegated to an eligible parent/root browser session.

## Wire-up proof (real, partial)
- **tehendri/ai-video-captions** (MIT): shallow-cloned, ran the backend's `generate_ass()` with a synthetic faster-whisper-style word-level transcript in a venv (only `pysubs2` installed). Result: returned `True`, produced a valid 1008-byte `.ass` file with `[V4+ Styles]`, 4 `Dialogue:` lines, word-level karaoke highlight override tags, emoji stripped. Proof file at `/tmp/w26-wire/proof.ass` (ephemeral).
- NOT tested (documented honestly): full Docker compose stack, faster-whisper model download/inference, FFmpeg burn-in render — those legs need GBs of model downloads and are out of this lane's budget.
- **OpenScreen** (MIT): shallow-cloned successfully (pushed 2026-10-07); Electron/Rust app — build not attempted.

## Draft file
- `/tmp/w26-new-entries.md` (ephemeral scratch; the catalog is the source of truth).
