# RESOURCE_CATALOG Wave 5 appendix — Worker B (GPU handoff specs)

Coordinator: merge into RESOURCE_CATALOG.md. Do not edit RESOURCE_CATALOG.md in this file — entries below are in the standard format with [Wave 5] tags.

Only genuinely NEW or materially CHANGED items are listed. Already-catalogued (Waves 1–4): Wan2.2-S2V ✅, Zonos ✅, Dia ⚠️, VibeVoice ⚠️, Wan 2.2 TI2V-5B ✅ — not re-listed except where Wave 5 verification changes their status.

## New entries

#### Dia2 ✅ commercial-safe
- **What:** Streaming dialogue TTS from Nari Labs (successor to Dia): starts generating as the first words arrive; audio-prefix conditioning for stable two-speaker conversation; word timestamps from Mimi ~12.5 Hz frames
- **URL:** https://github.com/nari-labs/dia2
- **License:** Apache-2.0 (verified: repo LICENSE file text + badge, 2026-10-07; announced 2025-11-19 in the Dia README)
- **Free tier:** fully open
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5 (uv-based; CLI auto-selects CUDA else CPU, bfloat16 default)
- **Status:** not-started
- **Notes:** Checkpoints 1B/2B (`nari-labs/Dia2-2B`), English only, ≤2 min generation per run. Quickstart: `uv sync && uv run -m dia2.cli --hf nari-labs/Dia2-2B --input input.txt --cfg 6.0 --temperature 0.8 --cuda-graph --verbose output.wav`. "Quality and voices vary per generation… Use with prefix or fine-tune in order to obtain stable output." Real-time dialogue lane candidate — pairs with Dia (non-streaming) for the series' conversation scenes [Wave 5]

## Status / license updates to existing entries (verify at merge)

#### VibeVoice — re-verify: ⚠️ → 🚫 research-only (recommendation)
- Current catalog badge ⚠️ says "TTS code was removed after misuse (partially restored since)". **Wave 5 re-verification 2026-10-07 found NO evidence of restoration:** the README's Models table lists only VibeVoice-Realtime-0.5B + VibeVoice-ASR; the 2025-09-05 entry ("we have removed the VibeVoice-TTS code from this repository") stands as the latest word on VibeVoice-TTS. The long-form multi-speaker TTS variant (90-min, 4-speaker) cannot be obtained from upstream.
- Realtime model card (`microsoft/VibeVoice-Realtime-0.5B`, `license:mit`, ungated) adds binding intended-use terms: "limited to research purposes"; "We do not recommend using VibeVoice in commercial or real-world applications… intended for research and development purposes only"; **audible AI disclaimer embedded in every output file + imperceptible watermark**. The audible disclaimer alone disqualifies it from finished episodes.
- Recommendation: re-badge 🚫 (research-only upstream terms), move shipping-path references to research lane only. Wave 4's "modeling code present" WIRED-PARTIAL status for VibeVoice-TTS is stale against current upstream [Wave 5]

#### Dia — license note re-verified
- Wave 5 re-verified 2026-10-07: repo LICENSE = Apache-2.0 (full text); model card `nari-labs/Dia-1.6B-0626` = `license:apache-2.0`; upstream sentence is "To accelerate research, we are providing access to pretrained model checkpoints and inference code" — no commercial restriction in the license text itself. The existing ⚠️ badge (based on an "intended for research and educational use" reading) is a coordinator judgment call; the underlying license documents are clean Apache-2.0. Keeping ⚠️ vs ✅ is a merge-time decision [Wave 5]

#### Verified model download sizes (HF API `safetensors.total`, 2026-10-07)
- Wan-AI/Wan2.2-S2V-14B: **16,295,755,609 B (~16.3 GB)** + VAE/audio-encoder files
- Zyphra/Zonos-v0.1-hybrid: **1,651,820,416 B (~1.65 GB)**
- Zyphra/Zonos-v0.1-transformer: **1,624,411,136 B (~1.62 GB)**
- microsoft/VibeVoice-Realtime-0.5B: **1,017,626,722 B (~1.02 GB)**
- nari-labs/Dia-1.6B-0626: **1,611,160,576 B (~1.61 GB)** + Descript Audio Codec on first run
- All five repos ungated (`gated: False`) as of 2026-10-07 [Wave 5]

#### Upstream org correction (applies to Wan2.2-S2V + Wan 2.2 entries)
- The Wan org moved from `Wan-AI` to `Wan-Video`. Correct code repo is **https://github.com/Wan-Video/Wan2.2** (GitHub API: `spdx_id: Apache-2.0`); `github.com/Wan-AI/Wan2.2-S2V` returns **HTTP 404**. Weights remain under the `Wan-AI` HF org. Any doc/command still pointing at `Wan-AI/Wan2.2*` GitHub paths is stale [Wave 5]
