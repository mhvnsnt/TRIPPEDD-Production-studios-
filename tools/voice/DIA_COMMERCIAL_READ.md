# Dia — Commercial-Use Legal Read (Wave 6, 2026-10-07)

**Model:** nari-labs/Dia, 1.6B text-to-dialogue TTS (two-speaker `[S1]`/`[S2]`,
emotion/non-verbal tags). Upstream: https://github.com/nari-labs/Dia
(read live 2026-10-07; current commit 876125e; 19,396 stars; **Dia2 released
2025-11-19 — a separate artifact with its own terms, read separately**).

**I am not a lawyer.** This is a read of published license and README text,
not legal advice. Items needing counsel are marked **needs-lawyer**.

---

## 1. The license file: Apache-2.0

Upstream `LICENSE` is the Apache License 2.0 (confirmed via the GitHub
repository license field, 2026-10-07). The Apache-2.0 grant (§2–3 of the
license text) permits use, reproduction, and distribution — including
commercial use — with attribution and a copy of the license. **Nothing in the
license file restricts commercial use.**

## 2. The README disclaimer — verbatim operative text

Upstream README (`## Disclaimer`, nari-labs/Dia, read 2026-10-07):

> "This project offers a high-fidelity speech generation model **intended
> for research and educational use**. The following uses are **strictly
> forbidden**: ... By using this model, you agree to uphold relevant legal
> standards and ethical responsibilities."

The forbidden-uses list: (1) **Identity Misuse** — no audio resembling real
individuals without permission; (2) **Deceptive Content** — no misleading
content (e.g. fake news); (3) **Illegal or Malicious Use** — no illegal or
harm-causing activity.

The README intro also frames the release as: *"To accelerate research, we
are providing access to pretrained model checkpoints and inference code."*

(Sources: https://github.com/nari-labs/Dia, README `## Disclaimer` section,
read 2026-10-07. Quotes are brief operative excerpts; full text at the URL.)

## 3. What the disclaimer does / doesn't restrict for a commercial animated series

**Does NOT restrict:** our actual use — original fictional cartoon characters
voiced with owned/consented reference audio (no real-person impersonation),
no deceptive content, no illegal activity. The strictly-forbidden list does
not cover fictional animation dialogue.

**DOES create a real tension:** the model is described as *"intended for
research and educational use"* — a vendor-stated intent that points away from
commercial production, while the Apache-2.0 file simultaneously grants
commercial rights.

**Key legal-analysis note (needs-lawyer):** the disclaimer sits in the README,
not in the license grant. Under Apache-2.0, the operative commercial rights
come from the license file. Whether a vendor can bind users to a stricter
intent stated outside the license — and whether a court would treat the
README language as contractually binding — is genuinely unresolved and
jurisdiction-dependent. **A lawyer's call.**

## 4. What remains ambiguous

- Is the "intended for research and educational use" line a binding
  restriction, a soft ethical request, or just context about why the model
  was released?
- Could the vendor alter terms, gate, or pull weights in future commits
  (as Microsoft did with VibeVoice's TTS code)?
- Does the Dia2 release (2025-11-19) carry different terms? Unread by this
  wave — do not assume continuity.

## 5. Verdict + recommendation

**Verdict: ❓ needs-owner-review — QUARANTINE-IN-PRACTICE.**

- Fine for internal R&D, animatics, audition/line-iteration. ✅
- Do **not** carry production dialogue in monetized episodes until the owner
  makes an explicit call (or counsel rules on the README-vs-license tension).
- Cast primary voices on Zonos (Apache-2.0, no such rider) in the meantime.

Catalog badge: **Dia ❓** — already correct; re-verified this wave
(2026-10-07). Not GPL/AGPL — no `docs/LICENSE_QUARANTINE.md` row.

---

*Read: nari-labs/Dia README + license field, 2026-10-07. Not legal advice.*
