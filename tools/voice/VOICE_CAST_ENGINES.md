# VOICE_CAST_ENGINES — final commercial verdicts + 9-character casting (Wave 7)

Date: 2026-10-07. Lane B, TRIPPEDD Resource Pull Wave 7.
Supersedes the capability routing in `VOICE_CAST_MAPPING.md` (Wave 4) as the
**commercial decision** record. Every license claim below was re-verified
against upstream sources this wave (2026-10-07); verification method is noted
per row.

**I am not a lawyer.** These are reads of published license and README text,
not legal advice.

**Standing rules for this lane (owner law, non-negotiable):**
- AI voices for based-on characters must be **TIGHT to the real people** —
  a stock-voice approximation is not an acceptable commercial cast.
- Clone **only** voices the owner has approved targets for, from
  **owner-supplied / explicitly consented** reference audio. Never scrape
  real-person audio from the internet.
- Theory and Onyx have no approved voice targets: **a character with no
  acceptable matched voice stays silent — never a placeholder voice.**
- No character lines are synthesized until the owner approves scripts —
  engine smoke tests only.

---

## (a) Commercial verdict per candidate engine

### Zonos (Zyphra) — ✅ LICENSE-CLEAR, EXECUTION-BLOCKED

- **License evidence:** code repo `Zyphra/Zonos` → GitHub API `spdx_id:
  Apache-2.0` (live check 2026-10-07); weights `Zyphra/Zonos-v0.1-transformer`
  and `Zyphra/Zonos-v0.1-hybrid` → HF model-card frontmatter `license:
  apache-2.0` (live check 2026-10-07). No revenue cap, no territory
  restriction. Full legal read: `docs/VOICE_COMMERCIAL_USE_WAVE5.md` §1.
- **Quarantine note (process, not license):** phonemization runs through
  eSpeak-NG (GPL-3.0) — invoke the `espeak-ng` *binary* as a standalone tool,
  never link the library into shipping paths.
- **What remains blocked:** no GPU smoke test has ever been executed. The CPU
  path is definitively infeasible (OOM-137/SIGKILL, Wave 5 — `docs/GPU_HANDOFF_SPECS_WAVE5.md`;
  hybrid has no CPU path at all). Upstream `pip install` is also broken at HEAD
  (setuptools packaging drops `zonos/backbone/` — one-line patch documented).
  Execution needs a CUDA card with 6 GB+ VRAM (recipe: `ZONOS_GPU_RUNBOOK.md`).
- **Verdict:** the commercial-safe casting engine for the Wizard Gang — but
  **not genuinely ready** until a GPU-box smoke test passes. HELD.

### Dia (nari-labs) — ❓ NEEDS-OWNER-REVIEW — QUARANTINE-IN-PRACTICE

- **License evidence:** repo `nari-labs/dia` → GitHub API `spdx_id: Apache-2.0`
  (live check 2026-10-07); weights `nari-labs/Dia-1.6B-0626` → HF frontmatter
  `license: apache-2.0` (live check 2026-10-07). The Apache-2.0 file itself
  permits commercial use.
- **The rider:** upstream README states the model is **"intended for research
  and educational use"** and lists strictly forbidden uses (identity misuse,
  deceptive content, illegal/malicious use). Whether README intent binds
  beyond the Apache-2.0 grant is genuinely unresolved and jurisdiction-dependent
  (needs-lawyer). Full read: `DIA_COMMERCIAL_READ.md` (Wave 6).
- **What remains blocked:** (1) the **owner's explicit call** (or counsel's
  ruling on the README-vs-license tension) before Dia voices ship in
  monetized episodes; (2) Dia2 (released 2025-11-19) is a separate artifact
  with **unread terms** — do not assume continuity; (3) Dia is GPU-only
  upstream ("CPU support is to be added soon" — no timeline) and no GPU smoke
  test has ever run.
- **Verdict:** fine for internal R&D, animatics, audition/line-iteration.
  **Do NOT carry production dialogue in monetized episodes until the owner
  makes an explicit call.** HELD.

### VibeVoice (Microsoft) — 🚫 RESEARCH-ONLY — DO NOT CAST

- **License evidence:** repo `microsoft/VibeVoice` → GitHub API `spdx_id: MIT`
  (live check 2026-10-07); weights `microsoft/VibeVoice-Realtime-0.5B` → HF
  frontmatter `license: mit` (live check 2026-10-07). Full read:
  `VIBEVOICE_COMMERCIAL_READ.md` (Wave 6).
- **The blockers (three):** (1) upstream README states VibeVoice is **"limited
  to research purpose use"** and not recommended for commercial/real-world
  applications; (2) on 2025-09-05 Microsoft **removed the VibeVoice-TTS code**
  from the repo after misuse — the long-form 90-min/4-speaker TTS cannot be
  obtained from upstream (code-availability blocker, not hardware; later tree
  partially restored modeling code but the R&D-intent statement stands —
  `PROOFS_WAVE4_TTS.md`); (3) every synthesized file gets an **audible AI
  disclaimer embedded** plus an imperceptible provenance watermark —
  unusable in finished episodes.
- **Verdict:** research lane only — never load-bearing, never in shipping
  paths. **Do not cast VibeVoice commercially.**

### sherpa-tts — ⚠️ RUNTIME-CLEAR, VOICE-WEIGHTS UNCLEARED

- **License evidence:** runtime `k2-fsa/sherpa-onnx` → GitHub API `spdx_id:
  Apache-2.0` (live check 2026-10-07); Vocos vocoder → MIT (upstream
  gemelo-ai/vocos, "Copyright (c) 2023 Charactr Inc.").
- **The problem:** the bundled acoustic-model weights
  (`csukuangfj/matcha-icefall-en_US-ljspeech`, the single female LJSpeech
  voice) carry **NO license statement from the weight author** — training
  data (LJSpeech, public-domain LibriVox) is fine, the *weight distribution*
  is not. Read: `sherpa-tts/README.md` ❓ UNKNOWN badge.
- **Capability:** single fixed voice, **no cloning** — cannot satisfy the
  owner law of TIGHT likeness for based-on characters.
- **Proof:** genuinely executed on a real box — `sherpa-tts/proofs/sherpa_test.wav`,
  3.84 s @ 22050 Hz, real audible speech (sha256
  `a40034bc696e7da5607a494c55eddc6ae191f6f566059c34ece8c5590c89c813` —
  from `sherpa-tts/PROOFS.md`).
- **Verdict:** working and proven, safe for scratch/animatics/temp VO **now**.
  Not a commercial cast voice for any of the 9 characters until the owner
  clears the weight license (or a licensed voice is swapped in) — and even
  then it cannot do likeness cloning.

### kokoro — ✅ LICENSE-CLEAR, NO-CLONING

- **License evidence:** weights `hexgrad/Kokoro-82M` → HF frontmatter `license:
  apache-2.0` (live check 2026-10-07); the Kokoro-82M code is Apache-2.0.
  Engine lives in the god-molecule lane: `god-molecule-studio/tools/voice/`
  (`README.md`, `PROOFS.md`).
- **Capability:** stock voices only (`af_heart`, `af_bella`, `af_nicole`,
  `af_sarah`, `am_adam`, `am_michael`, UK set) — **no cloning**, so it cannot
  carry based-on characters under owner law.
- **Proof:** genuinely executed — `god-molecule-studio/tools/voice/kokoro_test.wav`,
  3.55 s @ 24 kHz, real speech (sha256 `1868854d…55e41d13`, full hash in
  that lane's `PROOFS.md`).
- **Verdict:** commercial-safe by license; usable for scratch, animatics, and
  *original* (non-based-on) voices **with owner approval of the voice choice**.
  Not a cast voice for any based-on character.

### piper-tts — ⛔ QUARANTINED (GPL)

- **License evidence:** PyPI package `piper-tts` (v1.8.0, the exact package
  the lane installed) declares **`GPL-3.0-or-later`** in its own package
  metadata (live check 2026-10-07). NOTE: the `rhasspy/piper` GitHub repo's
  `LICENSE.md` reads MIT (Michael Hansen, 2022) — the repo text and the
  distributed package metadata disagree; the **installed package's own
  declaration** is the conservative binding one, so the quarantine stands.
- **Standing:** per `docs/LICENSE_QUARANTINE.md` — runs only as a separate
  local process, never linked into shipping code, never in shipping paths.
- **Proof:** genuinely executed — `god-molecule-studio/tools/voice/piper_test.wav`,
  3.05 s @ 22050 Hz.
- **Verdict:** scratch-only. Never cast commercially.

### RVC / Applio — ✅ LICENSE-CLEAR, GPU-AND-CONSENT-BLOCKED

- **License evidence:** `RVC-Project/Retrieval-based-Voice-Conversion-WebUI` →
  GitHub API `spdx_id: MIT` (live check 2026-10-07); `IAHispano/Applio` →
  GitHub API `spdx_id: MIT` (live check 2026-10-07). Wiring:
  `god-molecule-studio/tools/voice/RVC_APPLIO_WIRING.md`.
- **What remains blocked:** (1) **training needs a GPU box** — no approved
  remote/paid GPU exists (owner has not approved spend); Applio is docs-path
  only (large WebUI download — install on a workstation/GPU box); (2)
  **owner-supplied / consented reference audio per character** — the
  owner-consent rule binds before any cloning; (3) RVC inference on CPU is
  possible with a trained `.pth`, but no trained wizard voices exist.
- **Verdict:** commercial-safe code; the likeness-training path once a GPU
  box and consented references exist. HELD.

---

## (b) Final casting — 9 wizard characters

Standard applied: a character is cast only where the engine is
**commercial-safe for the use, proven working on a real box, and capable of
the required delivery** (owner law: tight likeness for based-on characters).
Zonos is license-clear but has never run on a GPU; sherpa-tts/kokoro run but
cannot do likeness cloning. **Result: all nine are HELD.** The lane below is
the first casting move each character takes the moment its blockers clear.

| # | Character | Voice target (owner-confirmed) | Final cast | Status / blocker |
|---|---|---|---|---|
| 1 | Ashes / Narrator | Bill $aber deep narrator | **HELD → Zonos** | Zonos GPU smoke test + owner-supplied/consented Bill $aber reference |
| 2 | Static | Enzo Amore fast Jersey braggadocio | **HELD → Zonos** (+Dia for banter scenes once owner reviews Dia) | same Zonos blockers + consented reference; Dia needs the §(a) owner call |
| 3 | Cipher | Lio Rush high-energy | **HELD → Zonos** (+Dia for banter) | same as Static |
| 4 | Echo | Shotzi Blackheart raspy punk | **HELD → Zonos** (+Dia for ad-libs) | same as Static |
| 5 | Hollow | Super Dragon | **HELD → Zonos** | same as Narrator |
| 6 | Sombra Negra | Damian Priest deep menace | **HELD → Zonos** (audio-prefix whisper elicitation) | same as Narrator; ref must be male (canon binding) |
| 7 | Kiko | Keiji Mutoh theatrical | **HELD → Zonos** (+Dia for theatrical non-verbals) | same as Static |
| 8 | Theory | Black 20yo NY woman — exact voice TBD | **HELD — UNASSIGNED** | **owner must define the voice target**; stock voices prohibited as placeholders; stays silent until then |
| 9 | Onyx | TBD | **HELD — UNASSIGNED** | **owner must define the voice target**; Zonos zero-shot is the flexible default once a target exists |

Scratch tier (not casting): sherpa-tts and kokoro are proven working and
license-clear-enough for **animatics, timing, and audition line-iteration
only** — no based-on likeness, no shipped episodes.

---

## (c) Exact owner approvals still needed

1. **Dia commercial verdict** — explicit owner call (or counsel's ruling) on
   the README-"research and educational use"-vs-Apache-2.0 tension before
   Dia voices ship in monetized episodes. (Dia2 terms: unread — flag if
   evaluating.)
2. **sherpa Matcha voice weights** — no license statement from the weight
   author (`csukuangfj/matcha-icefall-en_US-ljspeech`); clear with the owner
   before that voice appears in anything commercial.
3. **Meta-login SDK staging** — the Oculus LipSync SDK (lipsync lane,
   `tools/lipsync/OVRLIPSYNC_STAGING.md`): owner logs in to developers.meta.com,
   downloads the SDK zip, reads the audio-variant license/EULA inside it,
   confirms the commercial/for-charge clause — ~5 minutes, no agent can do it.
4. **Consented reference audio** — owner supplies (or explicitly approves)
   10–30 s reference clips for all 7 based-on voices (Bill $aber, Enzo Amore,
   Lio Rush, Shotzi Blackheart, Super Dragon, Damian Priest, Keiji Mutoh)
   before ANY Zonos or RVC cloning. Never scraped audio.
5. **Theory + Onyx voice targets** — owner defines them; until then both
   characters stay silent (no placeholder voices).
6. **Script approval** — no character lines synthesized until the owner
   approves scripts; engine smoke tests only.
7. **GPU box** — no approved remote/paid GPU exists in this environment
   (no `nvidia-smi`, no CUDA, no torch; owner has not approved spend).
   Unblocking Zonos/Dia/S2V/I2V synthesis requires an owner-approved GPU box
   — see the per-task `GPU-HANDOFF_*.md` files (this wave) for exact floors.

## Files touched/added this wave (Lane B)

- `tools/voice/GPU-HANDOFF_ZONOS.md` (new) — concise GPU handoff
- `tools/generative_stack/GPU-HANDOFF_WAN22_I2V.md` (new) — concise GPU handoff
- `tools/lipsync/GPU-HANDOFF_WAN22_S2V.md` (new) — concise GPU handoff
- `tools/voice/zonos/README.md` (fixed) — retired the stale CPU-inference
  recipe (OOM-137 definitive), corrected the model-download recipe to
  `huggingface-cli` (no CPU load), added the upstream packaging-bug note
- `tools/voice/VOICE_CAST_ENGINES.md` (this file)
- Verified, no changes needed: `WAN22_I2V_GPU_RUNBOOK.md` (diffusers import
  re-proven live in `~/venvs/whisperx`), `WAN22_S2V_GPU_RUNBOOK.md` (command
  shape verified verbatim against current upstream README), `DIA_GPU_RUNBOOK.md`
  (`model.save_audio` confirmed in current upstream `example/simple.py`),
  `ZONOS_GPU_RUNBOOK.md`, `VIBEVOICE_GPU_RUNBOOK.md`
