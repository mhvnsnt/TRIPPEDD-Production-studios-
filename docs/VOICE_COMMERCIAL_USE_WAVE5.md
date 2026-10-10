# VOICE COMMERCIAL-USE LEGAL READ — Wave 5 (2026-10-07)

This doc gates **voice-camp casting**: which TTS engines may carry production
dialogue in anything monetized. All terms below were read from upstream this
wave (2026-10-07). Verdicts are conservative by design — when in doubt, the
stricter badge wins. These are reads of published license/terms text, not
legal advice; the owner makes final ship calls.

**Summary table**

| Model | Verdict | License file | README / model-card terms |
|---|---|---|---|
| Zonos (Zyphra) | ✅ commercial-safe | Apache-2.0 | none restrictive; eSpeak-NG GPL-3.0 *dependency* handled by standalone-use doctrine (quarantine row 7) |
| Dia (nari-labs) | ❓ needs-owner-review | Apache-2.0 | "intended for research and educational use" + strict misuse forbiddens |
| VibeVoice (microsoft) | 🚫 research-only | MIT (code) | "limited to research purpose use"; "do not recommend… commercial or real-world applications"; TTS code pulled 2025-09-05 after misuse |

---

## 1. Zonos — ✅ COMMERCIAL-SAFE

- **What:** Zyphra open zero-shot TTS (1.6B transformer/hybrid), 5–30s audio-prefix
  voice cloning, emotion/pitch/rate conditioning, 44 kHz native output.
- **URL:** https://github.com/Zyphra/Zonos (org renamed: `ZyphraAI` → `Zyphra`;
  the old `ZyphraAI/Zonos` URL 404s — update links to `Zyphra/Zonos`)
- **License read (Wave 5):** upstream LICENSE is **Apache-2.0** (Wave 4 verified
  via GitHub API license endpoint; HF model cards for Zonos-v0.1 mark
  `apache-2.0`; Zyphra's release announcement states "both… models, all under
  the Apache 2.0 license"). Apache-2.0 permits commercial use, sublicensing,
  and distribution with attribution — no research/non-commercial rider in the
  upstream repo or model card.
- **Caveats (not blockers):**
  - Phonemization runs through **eSpeak-NG (GPL-3.0, quarantine row 7)** — the
    Wave-4/standby doctrine stands: invoke the eSpeak *binary* as a standalone
    tool, never link the library into shipping paths. This affects process
    architecture, not commercial eligibility of Zonos output.
  - Zyphra now ships **ZONOS2** as a separate model under **MIT** (vendor
    NOTICE dir tracks third-party components) — distinct from Zonos v0.1;
    evaluate separately if casting it.
- **Verdict: ✅ commercial-safe.** Strongest open zero-shot voice-cloning
  candidate for the voice camp. Generate each cast voice from owned/consented
  reference audio (identity-misuse laws apply to *us* regardless of license).

## 2. Dia — ❓ NEEDS-OWNER-REVIEW

- **What:** nari-labs 1.6B text-to-dialogue, two-speaker `[S1]`/`[S2]`
  turn-taking, emotion/non-verbal tags (laughs, coughs…).
- **URL:** https://github.com/nari-labs/Dia (read live this wave:
  commit 876125e, 19,396 stars — repo is active; a **Dia2** released 2025-11-19)
- **License file:** **Apache-2.0** — *"This project is licensed under the Apache
  License 2.0 - see the LICENSE file for details."* The license *file itself*
  grants commercial rights.
- **README disclaimer (upstream, verbatim, operative part):** *"This project
  offers a high-fidelity speech generation model **intended for research and
  educational use**. The following uses are **strictly forbidden**: Identity
  Misuse … Deceptive Content … Illegal or Malicious Use."* The README also
  frames the whole release as *"To accelerate research, we are providing access
  to pretrained model checkpoints and inference code."*
- **Analysis:** the forbidden-uses list (no real-person impersonation, no
  deceptive content) does not block fictional cartoon characters — our use is
  not on the forbidden list. But the vendor's *stated intent* is
  research/educational. Apache-2.0 legally permits commercial use; the README
  is a strong ethical/intent signal from the vendor, not a license restriction.
  There is genuine ambiguity, so per the conservative rule this lands on:
- **Verdict: ❓ needs-owner-review.** Fine for internal R&D, animatics, and
  audition/line-iteration. Owner must make an explicit call before Dia voices
  ship in monetized episodes (or re-verify whether Dia2 carries different terms).
  Recommend casting primary voices on Zonos/others instead until decided.

## 3. VibeVoice — 🚫 RESEARCH-ONLY

- **What:** Microsoft Research long-form multi-speaker TTS (up to ~90 min,
  4 speakers); plus VibeVoice-Realtime-0.5B (streaming, 300 ms first audio).
- **URL:** https://github.com/microsoft/VibeVoice (read live this wave:
  commit 1541f59, 54,662 stars — actively maintained into 2026)
- **License file:** **MIT** — code is MIT-licensed, which *normally* permits
  commercial use.
- **README / model-card terms (upstream, operative quotes):**
  - *"VibeVoice is an open-source research framework intended to advance
    collaboration in the speech synthesis community."*
  - *"After release, we discovered instances where the tool was used in ways
    inconsistent with the stated intent… we have **removed the VibeVoice-TTS
    code** from this repository."* (2025-09-05 — Microsoft pulled the TTS
    code over misuse; 1.5B weights remain on HF but Quick Try is disabled)
  - *"**We do not recommend using VibeVoice in commercial or real-world
    applications** without further testing and development. This model is
    intended for **research and development purposes only**."*
  - Model card (1.5B): *"The VibeVoice model is **limited to research purpose
    use**"* — with out-of-scope uses including voice impersonation,
    disinformation, and real-time voice conversion.
- **Voice-camp killers beyond licensing:**
  - VibeVoice-Realtime-0.5B deliberately **cannot clone**: Microsoft removed the
    acoustic tokenizer to prevent voice embeddings, embeds an **audible AI
    disclaimer** in every output, and adds an **imperceptible watermark**.
    Experimental built-in speakers exist (Dec 2025), but custom cast voices
    are blocked *by design* — the exact opposite of a casting engine.
  - Microsoft's published best practice: *"disclose to the end user that they
    are listening to AI-generated content."*
- **Verdict: 🚫 research-only — NOT for commercial use, and not for voice
  casting anyway.** Scratch/evaluation use only. Never load-bearing in any
  monetized episode. The MIT code license does not override Microsoft's
  explicit research-only designation of the model.

---

## Casting gate (bottom line)

- **Cast voices on: Zonos ✅** (Apache-2.0, zero-shot cloning, commercial-safe).
- **Dia: audition/R&D only** until the owner rules on the research-intent
  language (❓).
- **VibeVoice: never for cast voices** — research-only per Microsoft, and the
  realtime variant is anti-cloning by design (🚫).
- **Zonos v0.1 only** for this verdict — ZONOS2 (MIT) and Dia2 need their own
  reads if casting touches them.

*Reads: upstream GitHub READMEs/License badges fetched 2026-10-07 (nari-labs/Dia,
microsoft/VibeVoice); Oculus/Zyphra license texts via mirrors/search snippets.
Not legal advice.*
