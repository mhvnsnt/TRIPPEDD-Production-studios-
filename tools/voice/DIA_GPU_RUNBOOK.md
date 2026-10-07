# Dia (nari-labs) — GPU handoff runbook (Wave 6 Worker B)

**Status:** SPEC ONLY — nothing in this file was executed on a GPU in this sandbox.
Do not fabricate audio.

**What it is:** nari-labs' 1.6B text-to-dialogue model — one-pass two-speaker
`[S1]`/`[S2]` turn-taking with non-verbal tags ((laughs), (coughs), (sighs)…),
audio-prompt voice cloning (5–10 s), emotion/tone conditioning. English only.
Best fit in the stack for Wizard Gang **dialogue scenes** (Static↔Cipher banter,
ensemble exchanges).

**License / commercial-use read — Worker D, Wave 5** (`docs/VOICE_COMMERCIAL_USE_WAVE5.md` §2):
the LICENSE file is **Apache-2.0** (which legally permits commercial use), BUT
the upstream README states the model is **"intended for research and
educational use"** and lists strictly forbidden uses (identity misuse, deceptive
content, illegal/malicious use). Worker D's conservative verdict: **❓
NEEDS-OWNER-REVIEW.** Fine for internal R&D, animatics, and audition/line
iteration. **The owner must make an explicit call before Dia voices ship in
monetized episodes** — or re-verify whether Dia2 carries different terms.
Until then, cast primary voices on Zonos/others.

**Upstream:** https://github.com/nari-labs/dia · weights
`nari-labs/Dia-1.6B-0626` (ungated, public). Note: **Dia2** (1B/2B, streaming)
exists as a separate repo — do not conflate with this checkpoint.

---

## Hardware floor

| Item | Floor | Source |
|---|---|---|
| GPU (VRAM) | **≥ 8 GB VRAM recommended** | upstream RTX 4090 benchmarks: ~4.4 GB @ bf16/float16, ~7.9 GB @ float32 |
| CPU synthesis | **NOT SUPPORTED — do not attempt** | upstream README: "Dia has been tested on only GPUs (pytorch 2.0+, CUDA 12.6). **CPU support is to be added soon.**" This is an upstream support blocker, independent of hardware. |
| CUDA | **12.6+**, torch ≥ 2.0 | upstream requirement |

Realtime factors (upstream, RTX 4090): ≈ 2.1× (bf16, torch-compiled) / ≈ 1.5×
(no compile). Expect ~2–5 s of audio per second of wall-clock on a 4090-class
card at bf16.

## Disk floor

Weights are modest — **budget ~10 GB** (weights + venv + cache):

| Checkpoint | Verified size (2026-10-07, HTTP HEAD on full file list) |
|---|---|
| `nari-labs/Dia-1.6B-0626` | full snapshot **19.33 GB**; **unique ≈ 6.44 GB** — the repo carries the same 1.6B checkpoint in three containers (`dia-v1.pth` 6.44 GB, `pytorch_model.bin` 6.44 GB, `model-00001/2-of-00002.safetensors` 6.44 GB); download one container only |

> ⚠️ The HF API figure (1.61 GB, noted in the Wave-5 catalog) was ~4× wrong —
> the same ~2×-style metadata under-reporting seen with Zonos, worse. Do not
> budget 2 GB.

## Exact download commands

```bash
# CUDA torch FIRST so pip doesn't drag the CPU wheel in transitively
python -m venv ~/venvs/dia-gpu && source ~/venvs/dia-gpu/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cu126

# the engine itself (1.6B checkpoint downloads on first from_pretrained)
pip install git+https://github.com/nari-labs/dia.git

# OR via HF transformers (main branch first):
# pip install git+https://github.com/huggingface/transformers.git
```

Weights download automatically on first load (`from_pretrained`). To pin a
single container and skip the ~13 GB of redundant copies:
`huggingface-cli download nari-labs/Dia-1.6B-0626 --include "dia-v1.pth"`.

## Test recipe — wizard dialogue scene

Two wizard voices in one pass (Static + Cipher banter), exercising speaker
separation and non-verbals. Follows upstream's generation guidelines verbatim:
**always start with `[S1]`; alternate `[S1]`/`[S2]` (never `[S1]`…`[S1]`);
keep input at 5–20 s of audio-equivalent.** Voice-clone prompts need a 5–10 s
reference with a correct speaker-tagged transcript — use default voices for the
smoke test, owner-supplied/consented reference audio for real casting (same
identity-misuse guard as Zonos: no scraped real-person audio).

```python
from dia.model import Dia

model = Dia.from_pretrained("nari-labs/Dia-1.6B-0626", compute_dtype="float16")
# Dia is GPU-only; do NOT run this on a CPU box.

text = ("[S1] You hear that? The block's quiet tonight. (laughs) Too quiet. "
        "[S2] Quiet means they're listening, Static. Keep your voice down. "
        "[S1] Me? Keep it down? Baby, I AM the noise. (scoffs)")

out = model.generate(text, use_torch_compile=False, verbose=False)
model.save_audio("dia_static_cipher_test.wav", out)
print("wrote dia_static_cipher_test.wav")
```

For voice-cloned takes (casting lane, after GPU smoke test passes), pass the
audio prompt per the upstream README (5–10 s reference + speaker-tagged
transcript) — keep the reference audio under the same consent rules as Zonos.

## Expected artifacts

- `dia_static_cipher_test.wav` — 44.1 kHz output, ~8–12 s, **two distinct
  speakers** with the (laughs)/(scoffs) non-verbals audible in the right turns.

## How the GPU worker verifies success

1. `ffprobe dia_static_cipher_test.wav` → sane duration (>5 s), no truncation.
2. Listen to the whole clip: **both speakers audible and distinct** (not one
   voice, not a blend); non-verbals present where tagged.
3. Duration sanity vs input: input ~35 words ⇒ ~10–15 s of speech; far outside
   that band = generation went off the rails.
4. `nvidia-smi` log: confirm which dtype path ran (float16 ≈ 4.4 GB) and the
   measured realtime factor; report it back.
5. Report back: GPU model, VRAM peak, RTF, whether `use_torch_compile=True`
   was attempted and its effect, any speaker-bleed notes.

## What stays blocked without a GPU (summary)

**Everything.** Dia is GPU-only upstream with no CPU path ("CPU support is to
be added soon" — no timeline). The install/import wiring can be prepared on a
CPU box, but synthesis cannot be attempted, even slowly, until a CUDA card
exists. Do not report a CPU attempt as "blocked but tried" — it is
unsupported by design.

## Wave 10 re-verification (2026-10-07 — sandbox still GPU-less)

- `nari-labs/Dia-1.6B-0626` re-verified: **19,334,302,562 B = 19.33 GB** total
  (unchanged); the safetensors shards are 4.99 + 1.45 GB — the table's combined
  "6.44 GB" figure for the pair stands.
- The 2025-11-19 Dia2 announcements are already covered in the license note
  above — no new API drift for the Dia-1.6B path.
