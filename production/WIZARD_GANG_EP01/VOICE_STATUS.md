# WIZARD GANG EPISODE 1 — "THE SUMMIT" — Voice Readiness Report

**Prepared:** 2026-10-07 (voice-prep worker). **Scope:** prep only.
**CRITICAL LAW:** every dialogue line needs the OWNER'S approval before ANY voice work.
**NO episode line has been synthesized in this prep pass.** All 31 scripted lines are DRAFT.

## Voice law (owner-locked)

- AI voices tight to likeness. Stock TTS approximations are RETIRED wherever the owner has
  rejected them (Static: Piper `en_US-danny-low` rejected 2026-10-06 — "not sound nothing like Enzo").
- A character with no ready AI voice does not speak — never a placeholder voice,
  never a wrong-likeness voice, never synthetic filler.
- The Narrator is VOICE-ONLY (no purple-robed figure on screen, ever).
- The episode cuts clean WITHOUT Narrator lines N1/N2 (S10 works on the flare alone; S28's
  button works on the freeze-frame + L23) — if the Bill $aber clone isn't ready, ship the
  Static-only mix; Narrator stems drop in later.

## Voice-status key

- `READY` = voice pipeline exists; line awaits owner SCRIPT approval.
- `PENDING` = clone in progress; line not recorded until the clone lands + owner approves.
- `HELD` = no voice work; line scripted for a future episode and staged visual-only here.

---

## 1. Per-cast readiness table

| # | Cast member | Based-on lock | Voice pipeline | Status | Ep1 lines |
|---|---|---|---|---|---|
| 1 | STATIC | Enzo Amore | Chatterbox zero-shot clone (weights + 3 Enzo refs; test wav valid) | READY | 25 — P1–P2 (pilot, kept) + L1–L23 |
| 2 | NARRATOR (V.O.) | Bill $aber | XTTS v2 clone in progress — no verified sample has landed | PENDING | 2 — N1, N2 |
| 3 | ASHES | Bill $aber | Shares the Narrator's Bill $aber voice (same clone) | HELD | 1 — H2 (visual-only Ep1; recorded when clone lands) |
| 4 | ONYX | TBD (owner has never heard her speak) | none | HELD | 1 — H1 (visual-only Ep1) |
| 5 | SOMBRA | Damian Priest | none | HELD | 1 — H3 (visual-only Ep1) |
| 6 | KIKO | Keiji Mutoh / Great Muta | none | HELD | 1 — H4 (visual-only Ep1) |
| 7 | THEORY | Black 20-year-old NY woman (TBD) | none | HELD | 0 — no line written; style UNKNOWN, never invented |
| 8 | CIPHER | Lio Rush | none | HELD | 0 — no line written; style UNKNOWN beyond likeness lock |
| 9 | ECHO | Shotzi Blackheart | none | HELD | 0 — no line written; style UNKNOWN beyond likeness lock |
| — | HOLLOW | Super Dragon | none | HELD | 0 — no line written; talk/silent conflict unresolved by owner |

**Episode mix voice:** only Static (25 READY lines, all awaiting script approval).
6 lines are not voiced in Ep1: N1/N2 (PENDING — Narrator clone) and H1–H4 (HELD — staged visual-only).

---

## 2. Static pipeline — readiness check

**Location:** `~/workspace/voice-clone-work/`

| Artifact | Present | Detail |
|---|---|---|
| `cb_weights/t3_cfg.safetensors` | yes | 2.13 GB, 2026-10-06 (Chatterbox TTS transformer weights) |
| `cb_weights/s3gen.safetensors` | yes | 1.06 GB, 2026-10-06 (Chatterbox speech-generation weights) |
| `cb_weights/conds.pt` | yes | 107 KB (conditioning) |
| `cb_weights/ve.safetensors` | yes | 5.7 MB (voice encoder) |
| `cb_weights/tokenizer.json` | yes | 25 KB |
| `refs/enzo_ref_14s.wav` | yes | 618 KB |
| `refs/enzo_ref_29s.wav` | yes | 1.28 MB |
| `refs/enzo_roast.wav` | yes | 8.9 MB |
| `static_cloned_test.wav` | yes | 24 kHz mono, 12.92 s — valid audio bytes |
| `static_cloned_test_16bit.wav` / `.mp3` | yes | downsample + compressed copies |

**Verdict: READY for extension.** Weights load (standard Chatterbox pretrained cache; the clone
is zero-shot — the Enzo ref WAV is the voice prompt, no Static-specific fine-tune exists).
The runbook exists as a CLI: `~/workspace/multiplayer-work/tools/voice/clone-voice.py`
(MIT-licensed; documented usage matches the cached weights).

**Gaps / notes:**
- I have NOT listened to `static_cloned_test.wav` — no owner likeness-approval for the Enzo
  clone is on record. The owner must hear it (or a fresh approved-line sample) before any ship.
- This box has no GPU; Chatterbox generation here is CPU-speed. A GPU run path is an automation
  gap (Colab was rejected as manual homework — do NOT route manual setup through the owner).
- Do not confuse this pipeline with the retired Piper `en_US-danny-low` samples — those are dead.

## 3. Narrator (Bill $aber) clone — status

**Verdict: does NOT exist yet.** XTTS v2 clone is in progress (owner-confirmed 2026-10-06:
AI-performed, never owner-recorded). What remains:

1. Land the Bill $aber reference audio (voice worker owns the ref; owner has not supplied it —
   the staged Chatterbox fallback doc notes the ref is not in Drive yet).
2. Run the clone build (XTTS v2 path; Chatterbox fallback staged in
   `~/workspace/money-machine-hq/pipeline/video/staged/chatterbox_colab.md` — MIT, needs GPU).
3. Generate a verification sample; owner approves the likeness.
4. Only then: record N1 ("They got the call. All nine.") and N2 ("Nothing was resolved.")
   — both PENDING, both still DRAFT.

N1/N2 are VO-PENDING. The episode ships without them if the clone misses the cut.

---

## 4. Extend procedure (POST-APPROVAL ONLY — do not run before the owner approves the script)

One-time setup (weights then load automatically from cache):

```bash
pip install --break-system-packages chatterbox-tts torchaudio
```

For each approved Static line:

```bash
python3 ~/workspace/multiplayer-work/tools/voice/clone-voice.py \
  --ref ~/workspace/voice-clone-work/refs/enzo_ref_29s.wav \
  --text "<APPROVED LINE TEXT EXACTLY AS IN DIALOGUE.md>" \
  --out ~/workspace/trippedd-studio/production/WIZARD_GANG_EP01/audio/stems/static_<LINEID>.wav \
  --exaggeration 0.7 --cfg 0.6
```

(Tuning flags used for fast Jersey cadence; `--model turbo` default. `--ref` may be
`enzo_ref_14s.wav` or `enzo_roast.wav` if a different Enzo prompt sounds closer on test.)

Post-synthesis per line: listen to every take, confirm it sounds like Static (Enzo), trim head/tail,
then mix per DIALOGUE.md mix notes (duck ritual drums −6 dB under Static; party bed −4 dB under
Act 2 montage; keep L17's mic-feedback squeal).

Narrator lines (once the clone lands): same extend procedure against the Bill $aber clone
(XTTS v2 or Chatterbox), output to `audio/stems/narrator_<LINEID>.wav`. N1 over the flare's
sub-bass hit (0:52); N2 on the freeze-frame (4:50), 2 s held frame before hard cut.

---

## 5. Blockers

1. **Owner script approval (ALL 31 lines DRAFT)** — the hard gate. Nothing synthesizes before this.
2. **Owner likeness approval of the Enzo clone** — pipeline works, but no approved-likeness record
   for `static_cloned_test.wav`. Play it to him.
3. **Narrator clone missing** — no Bill $aber reference audio landed yet; no verified clone sample.
   Not a ship-blocker: the Static-only mix is the designed fallback (DIALOGUE.md).
4. **GPU automation gap** — Chatterbox generation is slow on this CPU box; no headless GPU path yet,
   and manual Colab is forbidden. Worth solving before 25 lines are due.
5. **No other cast member has a likeness voice** — Onyx, Theory, Cipher, Echo, Hollow, Sombra,
   Kiko are all HELD/visual-only in Ep1. Any future-episode voice work for them starts with a
   genuine-clone pipeline each, same standard.

## 6. Evidence

- `~/workspace/voice-clone-work/static_cloned_test.wav` — 24 kHz mono, 12.92 s, valid audio.
- This report: `production/WIZARD_GANG_EP01/VOICE_STATUS.md` (committed to trippedd-studio).
