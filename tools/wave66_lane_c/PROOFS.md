# Wave 66 Lane C — PROOFS: tightening the blind speaker-count decision

Branch: `wave66-lane-c` · Lane dir: `tools/wave66_lane_c/`
Worktree: `/home/hatch/workspace/trippedd-studio-w66c` (main checkout untouched;
`feature/ep02-visual-rebuild` and `production/WIZARD_GANG_EP01/` never written —
episode audio read read-only, as in Wave 65)

## Goal

Wave 65 ported the production diarization operating point (webrtcvad agg 0 /
10 ms / 0.3 s pad, DER 0.0382 exact repro) but on REAL EP01 audio the blind
eigengap speaker-count margin is **1.02x** — a fragile count decision. This
lane tests three ways to strengthen it, measured honestly on the Wave-65
fixture (GT: 3 speakers, 9 turns) AND on real EP01 episode audio (blind):

- (a) longer analysis windows for the count decision
- (b) VAD-gated energy clustering (log-RMS + delta, k-means BIC) as a count prior
- (c) ASR-assisted speaker turns: faster-whisper (MIT) word timestamps →
      inter-pause units (IPUs) → per-IPU mean ECAPA embeddings → count on
      turn-level embeddings instead of dense correlated windows

Tightness is measured by **eigengap margin** (decisiveness) and **bootstrap
stability** P(count == modal count over 20 resamples, seed 66) — the blind
metric for real audio. Fixture DER/JER is the guardrail: a count method that
breaks the 0.0382 baseline loses.

## What was wired

`wire_count_tightening.py` (original MIT lane code; `./run.sh [--only
fixture|production] [--exp a|b|c|all] [--ipu-gap S]`). Donor-first: VAD, grid
math, eigengap, frame labeling/fill, RTTM IO and scoring come from the wave63
(`wire_vad_coverage_recovery`) and wave64 (`wire_vad_recall_experiment`) lane
modules; weight-fetch and the raw-ECAPA encode body come from the wave65
production wire. This file adds only: parameterized window grids, the three
count experiments, bootstrap stability, the faster-whisper ASR stage, and a
`deepfilternet` availability probe.

Quarantine (Wave-61 production rule, honored): ECAPA embeddings are ALWAYS
computed on RAW audio. The ASR stage is a *segmentation donor* — its word
timestamps decide which windows get averaged per turn; no denoised or
transformed audio ever feeds the speaker path.

New third-party component wired: **faster-whisper 1.2.1 (MIT)** — permissive,
license-audit clean (base.en int8 on CPU). Everything else was already WIRED
in prior waves (webrtcvad MIT, SpectralCluster Apache-2.0, pyannote-metrics
MIT, SpeechBrain/ECAPA Apache-2.0).

## Baseline reproduction gate (must pass before any experiment)

| target | kept | k | margin | DER | JER | source |
|---|---|---|---|---|---|---|
| fixture | 102/166 | 3 | 1.721x | 0.0382 | 0.0378 | wave65 cache reuse |
| production | 1081/1195 | 3 | 1.023x | N/A (no GT) | N/A | wave65 cache reuse |

Wave-65's cached raw embeddings were reused (shape-checked against the
regenerated grid: 166 and 1195 windows respectively). Reuse chain validated
end-to-end: fresh 8-window ECAPA spot-check vs cached rows → cos min/mean =
**1.0/1.0** on the fixture. Fixture reproduces the Wave-64/65 baseline
exactly (DER 0.0382, JER 0.0378, margin 1.72x, kept 102 — matches the wave65
`result.json` anchors).

Honest note: bootstrap stability of the baseline count is only **0.55** on
the fixture and (see production) low on real audio — the eigengap decision
is fragile under resampling even where the point estimate is right.

## Experiment (a): longer analysis windows — WINNER

| grid (win/hop) | fixture k | margin | stability | DER | JER | production k | margin | stability |
|---|---|---|---|---|---|---|---|---|
| 1.5 s / 0.25 s (baseline) | 3 | 1.72x | 0.55 | 0.0382 | 0.0378 | 3 | 1.02x | 0.25 |
| 2.0 s / 0.5 s | 3 | 4.31x | 0.65 | 0.0382 | 0.0378 | 1 | 1.26x | 0.40 |
| **2.5 s / 0.5 s** | **3** | **7.35x** | **0.95** | **0.0382** | **0.0378** | 1 | 1.16x | 0.25 |
| 3.0 s / 0.5 s | 3 | 1.97x | 0.70 | 0.0382 | 0.0378 | 7 | 1.24x | 0.40 |
| 2.5 s / 0.25 s | 3 | 1.40x | 0.40 | 0.0382 | 0.0378 | not measured (restart) | — | — |

Fixture reading: **2.5 s windows at 0.5 s hop are the sweet spot** — margin
1.72x → 7.35x, stability 0.55 → 0.95, DER/JER unchanged at 0.0382/0.0378.
Longer windows give each embedding more phonetic content (cleaner affinity
structure); the 0.5 s hop keeps samples independent. The (2.5 s / 0.25 s)
control proves the point from the other side: same window length but dense
hop → margin collapses to 1.40x, stability 0.40 — correlated samples flatten
the gap spectrum. 3.0 s windows overshoot (fewer kept windows, 24/80, margin
back down to 1.97x). DER is identical across all five grids: the count
decision tightens without moving a single boundary.

Production (real EP01, blind) reading: the baseline's k=3 (1.02x, stab 0.25)
looks like phantom structure from correlated short windows. The 2.0 s and
2.5 s grids **agree on k=1** (1.26x/1.16x) — consistent with a
single-narrator episode (98.5% continuous speech, 12 VAD segments). The 3.0 s
grid jumps to k=7: with 25 s average VAD segments, 3 s windows fit inside
VAD but straddle speaker turns *within* a segment, creating mixed embeddings
and phantom clusters — the same overshoot the fixture showed (margin 1.97x).
Honest caveat: no GT exists, so k=1 is the better-supported hypothesis, not
a proven finding — margins stay weak (1.2x) because a single dominant voice
gives the gap spectrum little to bite on. The fixture anchoring is what makes
the long-window decision trustworthy: it gets GT right with 7.35x margin.

## Experiment (b): VAD-gated energy clustering as count prior — REJECTED

k-means on [log RMS, Δlog RMS] over VAD-gated 0.25 s frames, k by BIC.

- Fixture: energy-BIC k = **9** vs GT k = 3 → **prior FAILS GT validation**.
  k=9 is exactly the turn count: energy clusters track turn-level loudness,
  not speaker identity. The transparent fallback rule (trust eigengap iff
  margin ≥ 1.5x) correctly kept k=3 on the fixture.
- Production: energy-BIC k = **10** (the search ceiling) — BIC decreases
  monotonically from k=1 (−204) to k=10 (−1816): the energy features have NO
  natural cluster structure, the prior just slices the loudness continuum.
  The fallback rule would adopt k=10, which is absurd.

Honest conclusion: the energy prior is not validated and is NOT adopted.
It measures prosody/turn energy, an independent-but-wrong evidence family
for speaker count. Recorded as a negative result, not hidden.

## Experiment (c): ASR-assisted speaker turns — REJECTED (confidently wrong)

faster-whisper base.en int8 (CPU): 116 words on the fixture, word timestamps
→ IPUs split at inter-word gaps → per-IPU mean of fine-grid ECAPA embeddings
→ eigengap on turn-level samples.

| IPU gap | IPUs | k | margin | stability | purity | DER | JER |
|---|---|---|---|---|---|---|---|
| 0.5 s | 15 | 2 | 3.62x | 0.85 | 0.68 | 0.3626 | 0.5193 |
| 1.0 s | 5 | 2 | 6.74x | 1.00 | — | 0.4892 | 0.6480 |

GT k = 3. At both gap thresholds the turn-level count picks **k=2 with high
margin and high stability — confidently wrong**. The failure is
threshold-fragile (15 IPUs at 0.5 s vs 5 at 1.0 s from the same 9-turn audio)
and merges two of the three Kokoro voices at turn granularity: with few,
short, noisy turn samples the Laplacian has no structure to separate them.
- Production: **could not be measured** — the ASR stage returned only
  **10 words for the full 300 s** (see "Real EP01 audio contains no speech"
  below): 5 IPUs, 3 with embeddings → the eigengap hit a single-sample edge
  case (`max() on empty`, donor edge in `eigengap_laplacian`) and the run
  exited honestly instead of fabricating a count. faster-whisper itself is
  fine (116 words on the 43 s fixture) — there is simply no speech to turn
  into turns.

Honest conclusion: (c) is rejected — it fails the fixture gate (confidently
wrong count) AND has no measurable input on the real episode audio.

## CRITICAL FINDING: the "real EP01 audio" contains no speech

`production/WIZARD_GANG_EP01/audio-orig.m4a` (the file Wave 65 used for the
"real episode audio" production run) is a **music/effects bed with
essentially no speech**:

- faster-whisper base.en (validated: 116 words on the 43 s fixture):
  **10 words in the full 300 s** (60 s slice probes at 0/60/150/240 s:
  1/0/0/0 words; the single word was "Oh" at 44.6 s).
- The episode video's own audio track (`wizard-gang-ep01-16x9.mp4`, 30–100 s
  probe): 5 words — the episode is visual + music in the sampled sections.
- `VOICE_STATUS.md` (2026-10-07) confirms: **no episode dialogue has been
  voiced** — every line is PENDING/HELD awaiting the owner's script approval.
  There is no multi-speaker EP01 dialogue audio in existence.

Consequences, stated plainly:
1. webrtcvad at aggressiveness 0 passes music as speech (98.5% "speech") —
   the VAD operating point is too permissive for music beds. Any future
   production diarization must gate on ASR word presence (or a music-robust
   VAD), not webrtcvad alone.
2. The Wave-65 production run and this wave's production counts measured
   **speaker count on music texture, not speakers**. The (a) production
   numbers above are honest blind measurements of the file's content, but
   they are not speaker counts of an episode — there are no episode speakers
   to count yet.
3. The GT-anchored multi-speaker evidence in this lane is the Wave-65
   fixture (3 real voices, 9 turns) — that is where the 2.5 s / 0.5 s
   recommendation earns its keep.

## Supplementary: blind count on real single-speaker voice

`wire_cipher_voice_check.py`: the three cipher-refs voice clips
(backstage-manic 20 s, interview-loop 30 s, ring-taunt 20 s — real voice
recordings, one speaker, three different recording setups/effects),
concatenated with 1 s gaps (72 s total, read-only sources).

| grid | k | margin | stability | kept |
|---|---|---|---|---|
| 1.5 s / 0.25 s (baseline) | 5 | 1.70x | 0.45 | 249/283 |
| 2.5 s / 0.5 s | 5 | 1.10x | 0.60 | 121/140 |

Both grids overcount a single speaker as 5 — the three clips' different
mics/rooms/effects fragment the voiceprint (condition mismatch, a known
ECAPA limitation), and longer windows do NOT fix it. Honest limitation:
window length tightens the count against short-window noise (fixture), not
against acoustic-condition fragmentation. Proof: `proofs/w66_cipher_voice_count.json`.

## DeepFilterNet — BLOCKED (environment absent, recorded honestly)

- `deepfilternet` 0.5.6 is a py3-none-any wheel, but its hard dependency
  `deepfilterlib==0.5.6` has **no cp312 wheel on PyPI** and builds from
  source only via a **Rust toolchain, which this VM does not have**
  (`pip download` fails in metadata generation: "Cargo ... is not installed").
  Same blocker as Wave 64 — still present.
- DF3 checkpoint bytes remain in `~/.cache/DeepFilterNet/DeepFilterNet3`
  (Wave-62) but are unusable without the inference lib.
- Per the task: environment absent → recorded, **not wired**. The Wave-61
  quarantine (denoise never upstream of ECAPA) holds trivially.

## Environment / rebuild recipe

```bash
./install.sh   # lane venv: torch 2.14.1+cpu + torchaudio 2.11.0+cpu (direct
               # install), numpy 1.26.4 / scipy 1.11.4 / pandas 2.1.4 pins;
               # speechbrain 1.1.1, webrtcvad, spectralcluster, pyannote-metrics;
               # faster-whisper 1.2.1 from system site-packages (verified).
./run.sh --only fixture        # baseline gate + all three experiments
./run.sh --only production     # real EP01 audio, blind
./run.sh --only fixture --exp c --ipu-gap 1.0   # (c) threshold sensitivity
```

Environment incident (honest): the original plan reused torch/torchaudio
read-only from the cipher lane venv via a `.pth` entry (disk was >80%).
A VM/service restart on 2026-10-09 wiped that venv's site-packages entirely
(1.7 GB → 15 MB) AND removed scikit-learn/soundfile from this lane's venv —
this lane never wrote to the cipher venv. With the donor gone and no torch
anywhere on the filesystem, torch 2.14.1+cpu + torchaudio 2.11.0+cpu were
installed directly in the lane venv (~1.7 GB; the disk guardian had cleaned
to 75% by then, so headroom was fine). `install.sh` reflects the final
recipe; `venv-pins.txt` verifies it.

Timings: fixture full pass ~6.5 min (ECAPA weight fetch once); production
~1 h (four fresh long-window ECAPA grids on 300 s audio dominate).
ECAPA weights: `scratch/ecapa_weights/` (~89 MB, gitignored).
faster-whisper base.en: `scratch/fw_models/` (~145 MB, gitignored).

Install incident (honest): the first `install.sh` run left numpy 2.5.3 in the
venv — pip's resolver upgraded numpy/scipy/pandas during the pyannote step
(the Wave-65 recipe pinned them *before* that step and got lucky with a fresh
venv). Fixed by pinning the Wave-64 numerical stack *after* all other
installs; `install.sh` now does this and `venv-pins.txt` verifies
numpy==1.26.4 / scipy==1.11.4.

ASR incidents (honest, both fixed in-script):
1. `huggingface_hub` (via httpx) crashed on IPv6 literals in `no_proxy`
   (`InvalidURL: Invalid port: ':1]'`) — the documented TOOLS.md quirk.
   Fixed by stripping `::` entries from no_proxy/NO_PROXY before download.
2. `HF_HUB_OFFLINE=1` (set for local ECAPA weights) blocked the
   faster-whisper model download — fixed with a scoped override restored
   after init.

## Proof artifacts (all under `tools/wave66_lane_c/proofs/`)

See `SHA256SUMS` (covers proofs + wire scripts + install/run.sh +
venv-pins.txt).
- `w66_results_fixture_gap05.json` — full fixture pass (baseline + a/b/c).
- `w66_results_fixture_c_gap10.json` — fixture (c) IPU-gap sensitivity.
- `w66_results_production_a.json` — production (a) grids (from
  `w66_production_run.log`; JSON checkpoint lost to a service restart).
- `w66_results_production_b.json` — production (b) energy prior.
- `w66_results_production_c.json` — production (c) attempt (documents the
  no-speech ASR failure).
- `w66_cipher_voice_count.json` — real single-speaker voice check.
- `hyp_<tag>.rttm` — fixture hypothesis RTTMs per grid.
- `w66_production_run.log`, `w66_prod_b.log`, `w66_prod_c.log`,
  `w66_cipher_voice.log` — run logs.

## License audit

| component | license | role |
|---|---|---|
| webrtcvad 2.0.10 | MIT | VAD (WIRED since Wave 49) |
| SpectralCluster 0.2.22 | Apache-2.0 | forced-k clustering (WIRED since Wave 57) |
| pyannote-metrics 4.1 | MIT | DER/JER scoring (WIRED since Wave 57) |
| SpeechBrain 1.1.1 spkrec-ecapa-voxceleb | Apache-2.0 | ECAPA embeddings (WIRED since Wave 56/58) |
| faster-whisper 1.2.1 | MIT | ASR word timestamps, experiment (c) — NEW, permissive |
| DeepFilterNet | dual MIT/Apache-2.0 | NOT wired (no cp312-compatible build available) |

No catalog status flips except faster-whisper: proposed WIRED (run-proven
this wave, MIT). No GPL components. `production/` read, never written.
