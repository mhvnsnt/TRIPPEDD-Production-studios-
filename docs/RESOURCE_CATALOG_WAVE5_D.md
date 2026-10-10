# RESOURCE_CATALOG APPENDIX — Wave 5 D (2026-10-07)

**No NEW entries this wave.** All four models already have catalog entries;
below are the proposed UPDATED entries (standard format, [Wave 5] tag) for
the coordinator to apply to `docs/RESOURCE_CATALOG.md`. Full evidence lives
in `docs/VOICE_COMMERCIAL_USE_WAVE5.md` (voice) and
`tools/lipsync/ovr-lipsync/README.md` (OVRLipSync EULA read).

---

## UPDATE PROPOSAL 1 — OVRLipSync (replaces the ⚠️ commercial-OK-per-mirrors entry)

#### OVRLipSync ⚠️ commercial-OK-per-license-text
- **What:** Meta Oculus lip-sync SDK: real-time viseme analysis from audio (native C API, Unity, Unreal)
- **URL:** https://developers.meta.com/horizon/downloads/package/oculus-lipsync-unity/
- **License:** Oculus SDK License (Meta proprietary EULA). Wave 5 READ the actual license text (v3.5, via scancode LicenseDB mirror — canonical `developer.oculus.com/licenses/audio-3.3/` still HTTP 403 from sandbox): §2.1 — "You may sublicense and redistribute the source, binary, or object code of the Oculus SDK in whole for no charge or as part of a for-charge piece of Developer Content" (commercial/for-charge use EXPRESSLY permitted). Conditions: redistribute in its entirety; Oculus Approved Products only; ship the copyright notice + license copy; no reverse-engineering (§1.4); Meta retains SDK rights, you retain all rights to your Developer Content (§1.2). Badge: commercial-OK-per-license-text / VERIFY-AUDIO-3.3-VARIANT-BEFORE-SHIP (2026-10-07)
- **Free tier:** free SDK; download login-gated
- **Repo lane:** trippedd (lip-sync)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5 (native integration)
- **Status:** WIRED-PARTIAL — SDK download requires Meta login (owner action: sign in → download → unzip → stage `LibOVRLipSync/<platform>/libovrlipsync.*` + `Include/OVRLipSync.h` into `tools/lipsync/ovr-lipsync/sdk/`). Exact owner steps + integration paths in lane README. Do NOT commit binary to git until audio-3.3 license text is read. Proof: `tools/lipsync/PROOFS_WAVE4_LIPSYNC.md`
- **Notes:** Lowest-latency viseme path for game-engine characters. §2.1 "Oculus Approved Products" clause needs an owner read of the audio-3.3 variant before shipping inside desktop pipeline tools [Wave 5]

## UPDATE PROPOSAL 2 — Zonos (supersedes the ✅ entry — org rename + evidence)

#### Zonos ✅
- **What:** Zyphra AI open zero-shot TTS with eSpeak phonemization and audio-prefix voice cloning
- **URL:** https://github.com/Zyphra/Zonos (ORG RENAMED: `ZyphraAI` → `Zyphra`; old URL 404s — update all links)
- **License:** Apache-2.0 (verified via GitHub API license endpoint 2026-10-07; Wave 5 re-confirmed via HF model cards + Zyphra release announcement). NOTE: ZONOS2 is a separate model under MIT — different terms, evaluate separately
- **Free tier:** fully open
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** WIRED-PARTIAL — pip-installed (torch CPU), import verified after fixing a real upstream packaging bug (pyproject drops zonos/backbone subpackage; one-line local patch); espeak-ng installed; generation blocked (3.25GB weights vs ~1.4GB free disk). Lane: `tools/voice/zonos/`. Proof: `tools/voice/PROOFS_WAVE4_TTS.md`
- **Notes:** Wave 5 verdict: ✅ COMMERCIAL-SAFE — primary casting engine. DEPENDENCY NOTE: uses eSpeak phonemization — eSpeak-NG is GPL-3.0 (quarantine row 7); use the eSpeak binary as a standalone tool per the quarantine doctrine, never link the library [Wave 5]

## UPDATE PROPOSAL 3 — Dia (re-badge ⚠️ → ❓, evidence added)

#### Dia ❓
- **What:** 1.6B text-to-dialogue model with two-speaker turn-taking and emotion tags (upstream active; Dia2 released 2025-11-19)
- **URL:** https://github.com/nari-labs/Dia
- **License:** Apache-2.0 (read live 2026-10-07: commit 876125e) BUT upstream README: "intended for research and educational use" — identity misuse / deceptive content / illegal use strictly forbidden; release framed as "to accelerate research". Verdict: NEEDS-OWNER-REVIEW before commercial ship (2026-10-07)
- **Free tier:** fully open
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** WIRED-PARTIAL — lean --no-deps install, `from dia.model import Dia` OK; generation blocked (6.44GB fp32 weights; upstream GPU-only, CPU support "coming soon"). Lane: `tools/voice/dia/`. Proof: `tools/voice/PROOFS_WAVE4_TTS.md`
- **Notes:** Dialogue-native TTS is ideal for multi-character cartoon scenes. Audition/R&D/animatics OK; cast primary voices on Zonos until owner rules on the research-intent language [Wave 5]

## UPDATE PROPOSAL 4 — VibeVoice (re-badge ⚠️ → 🚫, evidence added)

#### VibeVoice 🚫
- **What:** Long-form multi-speaker podcast-style TTS (up to ~90 min continuous); Realtime-0.5B streaming variant (actively maintained into 2026; commit 1541f59, 54,662 stars)
- **URL:** https://github.com/microsoft/VibeVoice
- **License:** MIT (code) BUT Microsoft upstream designates the MODEL research-only: "VibeVoice is an open-source research framework"; TTS code REMOVED 2025-09-05 after misuse; "We do not recommend using VibeVoice in commercial or real-world applications… intended for research and development purposes only"; model card: "limited to research purpose use" (2026-10-07)
- **Free tier:** fully open
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** WIRED-PARTIAL — repo cloned, modeling code present; generation blocked (5.41GB/2.04GB weights vs free disk). Lane: `tools/voice/vibevoice/`. Proof: `tools/voice/PROOFS_WAVE4_TTS.md`
- **Notes:** 🚫 RESEARCH-ONLY — scratch/evaluation only, never in monetized episodes. CASTING KILLER: VibeVoice-Realtime-0.5B removes the acoustic tokenizer to PREVENT voice cloning by design, embeds an audible AI disclaimer + watermark in every output. Not a casting engine [Wave 5]
