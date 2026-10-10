# VibeVoice — Commercial-Use Legal Read (Wave 6, 2026-10-07)

**Model:** Microsoft Research VibeVoice family (VibeVoice-TTS-1.5B long-form
multi-speaker TTS; VibeVoice-Realtime-0.5B streaming TTS; ASR variants are
out of scope for casting).
Upstream repo: https://github.com/microsoft/VibeVoice (read live 2026-10-07;
current commit 1541f59; 54,662 stars; actively maintained into 2026).
Model card: https://huggingface.co/microsoft/VibeVoice-1.5B (read 2026-10-07).

**I am not a lawyer.** This is a read of published license, README, and
model-card text — not legal advice.

---

## 1. The license file: MIT (code)

The upstream `LICENSE` is the MIT License (confirmed via the GitHub
repository license field, 2026-10-07). MIT *normally* permits commercial use,
modification, and distribution.

**BUT — the critical distinction:** the MIT license covers the **code**.
The **model weights** and the vendor's published terms for them are where
the restriction lives, and vendor terms for the model explicitly override
the default-MIT expectation.

## 2. Upstream intent statements — verbatim operative excerpts

README `## Risks and Limitations`
(https://github.com/microsoft/VibeVoice, read 2026-10-07):

> "We do not recommend using VibeVoice in commercial or real-world
> applications without further testing and development. This model is
> intended for research and development purposes only. Please use
> responsibly."

README News, 2025-09-05 (still present 2026-10-07):

> "VibeVoice is an open-source research framework intended to advance
> collaboration in the speech synthesis community. After release, we
> discovered instances where the tool was used in ways inconsistent with the
> stated intent... we have **removed the VibeVoice-TTS code** from this
> repository."

Model card "Responsible Usage", Direct intended uses
(https://huggingface.co/microsoft/VibeVoice-1.5B, read 2026-10-07):

> "The VibeVoice model is limited to research purpose use exploring highly
> realistic audio dialogue generation detailed in the tech report."

(Quotes are brief operative excerpts; full text at the URLs above.)

## 3. MIT vs. stated intent — analysis

- MIT permits commercial use of the *code*. It does **not** override the
  vendor's explicit model-level terms. The model card and README form a
  separate, more specific terms-of-use layer for the weights; where the
  license grant and the vendor terms conflict, a reasonable producer treats
  the stricter terms as governing.
- Microsoft escalated from words to actions in 2025–2026: TTS inference code
  was *removed* from the repo (2025-09-05), Quick Try on the 1.5B weights is
  *disabled*, and VibeVoice-Realtime-0.5B was engineered *against* misuse
  (no voice-cloning capability, audible AI disclaimer baked into every
  output, imperceptible watermark).
- Unlike Dia, this is not ambiguous wording — Microsoft plainly states
  research-and-development-only and acted to enforce it. A fictional
  cartoon series is a "commercial or real-world application" under that
  language.

## 4. Functional disqualification from casting (independent of licensing)

Even setting licensing aside, VibeVoice cannot carry a voice cast:
- **VibeVoice-Realtime-0.5B deliberately cannot clone voices** — Microsoft
  removed the acoustic tokenizer so no custom speaker embeddings exist;
  only experimental built-in speakers are offered.
- Every 1.5B output carries an **audible AI disclaimer** and a
  **provenance watermark** — incompatible with character dialogue.
- The 1.5B inference code was pulled from the repo; only weights remain,
  with Quick Try disabled.
- Microsoft's published best practice: *"disclose to the end user that they
  are listening to AI-generated content."*

**VibeVoice is the wrong engine for voice casting regardless of legal
reading.**

## 5. Verdict + recommendation

**Verdict: 🚫 RESEARCH-ONLY — not for commercial use.**

- Scratch/evaluation use only. **Never load-bearing in any monetized
  episode.** Never as a cast-voice engine.
- Catalog badge: **VibeVoice 🚫** — already correct; re-verified this wave
  (2026-10-07).
- Not GPL/AGPL — no `docs/LICENSE_QUARANTINE.md` row; the restriction is
  vendor intent + functional, not copyleft.

---

*Reads: microsoft/VibeVoice README (commit 1541f59) + microsoft/VibeVoice-1.5B
model card, 2026-10-07. Not legal advice.*
