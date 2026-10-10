# PROOFS — Wave 4 TTS wiring (Zonos / Dia / VibeVoice)

Date: 2026-10-07. Worker A, TRIPPEDD Resource Pull Program Wave 4.
Workdir: `/home/hatch/workspace/trippedd-studio`, lane `tools/voice/`.
Venv: `~/venvs/wave4-tts` (torch 2.14.1+cpu, torchaudio 2.11.0+cpu).

## License verification (upstream, checked 2026-10-07)

| Engine | Upstream | License (upstream source) | Verdict |
|---|---|---|---|
| Zonos | https://github.com/Zyphra/Zonos | **Apache-2.0** — repo page "License: Apache License 2.0 (Apache-2.0)", root `LICENSE` file present | ✅ commercial-safe, wired |
| Dia | https://github.com/nari-labs/dia | **Apache-2.0** — repo page "License: Apache License 2.0 (Apache-2.0)"; README: "This project is licensed under the Apache License 2.0" | ✅ commercial-safe by license, wired with use-disclaimer (see below) |
| VibeVoice | https://github.com/microsoft/VibeVoice | **MIT** — repo page "License: MIT License (MIT)"; `LICENSE` file text begins "MIT License / Copyright (c) 2025 Microsoft" | ✅ commercial-safe by license, wired with R&D-intent caveat (see below) |

- Dia upstream README disclaimer (not a license change, but load-bearing for the voice-cast lane): "intended for research and educational use"; identity misuse, deceptive content, illegal/malicious use are **strictly forbidden**.
- VibeVoice upstream README (2025-09-05): "we have removed the VibeVoice-TTS code from this repository" after misuse; "We do not recommend using VibeVoice in commercial or real-world applications without further testing and development. This model is intended for **research and development purposes only**." Note: the current tree (commit `1541f590`) again contains TTS modeling code (`vibevoice/modular/modeling_vibevoice.py`) and realtime inference scripts — the removal was partial/reversed — but the R&D-intent statement stands. **VibeVoice is research/scratch only; never load-bearing.**

No GPL/AGPL anywhere in this lane. Nothing quarantined.

## Sandbox resources (measured 2026-10-07)

- CPU: 2 cores. RAM: 7 GB total, **~2 GB free**. Disk: 100 GB total, **~1.4–2.1 GB free, 98–99% used** (shared box).
- Weight sizes measured via `HEAD https://huggingface.co/<repo>/resolve/main/<file>` (HTTP 200, exact `Content-Length`):

| Weights | Bytes | GB |
|---|---|---|
| `Zyphra/Zonos-v0.1-transformer` / `model.safetensors` | 3,248,848,864 | **3.25** |
| `nari-labs/Dia-1.6B-0626` / `dia-v1.pth` (fp32) | 6,440,000,000 (~6.44) | **6.44** |
| `nari-labs/Dia-1.6B-0626` / `model-00001-of-00002.safetensors` + `model-00002-of-00002.safetensors` | 4.99 + 1.45 | **6.44** |
| `microsoft/VibeVoice-1.5B` / `model-0000{1,2,3}-of-00003.safetensors` | 1.98 + 1.98 + 1.45 | **5.41** |
| `microsoft/VibeVoice-Realtime-0.5B` / `model.safetensors` | 2,035,332,888 | **2.04** |

**Every engine's weights exceed free disk AND free RAM. No full TTS generation is possible on this box. No WAVs from the three engines were produced — and none were faked.**

## Zonos — installed, import-proven, generation BLOCKED (disk+RAM)

1. `pip install git+https://github.com/Zyphra/Zonos.git` — first attempt **FAILED**:
   `OSError: [Errno 28] No space left on device` while building `sudachidict-full` (pip's build temp defaulted to the 512 MB tmpfs `/tmp`). Retried with `TMPDIR` on workspace disk + `pip cache purge` → **installed OK** (`zonos-0.1.0`).
2. **Upstream packaging bug found:** `from zonos.model import Zonos` → `ModuleNotFoundError: No module named 'zonos.backbone'`. Root cause: upstream `pyproject.toml` has `[tool.setuptools.packages.find] include = ["zonos"]`, which drops the `zonos/backbone/` subpackage added in the current tree. The canonical `pip install git+https://…` path is **broken at upstream HEAD** (`bc40d98`). Workaround used for this smoke test only: shallow clone + one-line patch (`include = ["zonos", "zonos.*"]`) + `pip install --force-reinstall --no-deps <clone>` → `zonos import OK`. (Upstream issue-worthy; the lane README documents the stock install command.)
3. `snapshot_download("Zyphra/Zonos-v0.1-transformer", allow_patterns=["*.json"])` → **OK** (config.json fetched; keys: `backbone`, `eos_token_id`, `masked_token_id`, `prefix_conditioner`). HF network path works through the egress proxy.
4. **Weight load NOT attempted** (deliberate): 3.25 GB weights vs ~1.4–2.1 GB free disk → deterministic `ENOSPC`; ~3.3 GB fp16 RAM need vs ~2 GB free → deterministic OOM. Filling the shared 98%-full filesystem was judged unsafe; the arithmetic is exact and measured.
5. System dep: `espeak-ng 1.51` installed via apt (Zonos phonemization requirement) — OK.

## Dia — installed (lean path), import-proven, generation BLOCKED (disk+RAM, GPU-only upstream)

1. Canonical `pip install git+https://github.com/nari-labs/dia.git` — **ABORTED by operator**: dia pins `torch==2.6.0` / `torchaudio==2.6.0` (PyPI CUDA builds), which would have replaced the venv's CPU torch with ~2 GB+ of CUDA wheels; the shared disk hit **100% (131 MB free)** mid-install. Killed, temp/cache cleaned, disk recovered to 1.4 GB free. Exact failure mode: dependency pin incompatible with a CPU-only box.
2. Lean path: `pip install --no-deps` from shallow clone (`nari-tts-0.1.0`) + `pip install descript-audio-codec` → `from dia.model import Dia` → **import OK**. (pip notes `nari-tts 0.1.0 requires torchaudio==2.6.0` vs installed `2.11.0+cpu` — version-mismatch warning only; dia's `model.py` has no triton import and its device helper falls back to CPU.)
3. `snapshot_download("nari-labs/Dia-1.6B-0626", allow_patterns=["*.json"])` → **OK** (7 config files; `model_type: "dia"`, encoder-decoder).
4. **Weight load NOT attempted** (deliberate): 6.44 GB fp32 weights vs ~1.4 GB free disk and ~2 GB free RAM. Upstream additionally states Dia is **tested on GPUs only; CPU support "to be added soon"** — CPU inference is unsupported upstream regardless of resources.

## VibeVoice — repo inspected, generation BLOCKED (disk+RAM, no 1.5B file-inference demo)

1. Shallow clone of `microsoft/VibeVoice` @ `1541f590` — OK. `LICENSE` verified MIT from file text.
2. Tree state: `vibevoice/modular/` contains `modeling_vibevoice.py`, `modeling_vibevoice_streaming.py`, `modeling_vibevoice_streaming_inference.py`, tokenizers, diffusion head; `vibevoice/processor/`, `vibevoice/schedule/`, `vibevoice/configs/` present. `demo/` has realtime + ASR inference scripts (`realtime_model_inference_from_file.py`, `vibevoice_realtime_demo.py`) — **no file-based inference demo for the 1.5B TTS model** in the repo.
3. **Weight download NOT attempted** (deliberate): 5.41 GB (1.5B) / 2.04 GB (Realtime-0.5B) vs ~1.4 GB free disk. Realtime-0.5B additionally needs voice-preset `.pt` files (`demo/download_experimental_voices.sh`) and the `[streamingtts]` extra (flash-attn, GPU-oriented).
4. Upstream intent (README): research/development only — badge accordingly.

## Component proof (honestly labeled — NOT a TTS generation)

`tools/voice/proofs/dac_roundtrip_COMPONENT_ONLY__NOT_TTS.wav` (112,684 bytes, 1.28 s, 44.1 kHz, peak 0.905 — re-read verified) — espeak-ng formant synthesis of "The block remembers." passed through the **Descript Audio Codec** (`dac` 1.0.0, `44khz` model), the neural vocoder both Dia and Zonos use as their audio codec. Proves the codec stage of both pipelines runs on this CPU. **This is not a Zonos/Dia/VibeVoice voice — do not present it as one.**

## Resource requirements (for a real run)

| Engine | Weights | Disk needed | RAM/VRAM needed | Notes |
|---|---|---|---|---|
| Zonos-v0.1-transformer | 3.25 GB | ~8 GB free (weights + deps + temp) | 6 GB+ VRAM per upstream; CPU needs ~4–6 GB free RAM | Needs espeak-ng |
| Dia-1.6B | 6.44 GB | ~10 GB free | ~4.4 GB VRAM @ bf16, ~7.9 GB @ fp32 (RTX 4090 benches); GPU-only upstream | Needs 5–10 s audio prompt for cloning |
| VibeVoice-1.5B | 5.41 GB | ~10 GB free | GPU recommended; no official CPU story | Research-only per upstream |
| VibeVoice-Realtime-0.5B | 2.04 GB | ~5 GB free | GPU recommended | Streaming; preset voices via download script |

Minimum viable rerun: a box (or Colab/VPS) with **≥16 GB free disk, ≥8 GB RAM (or any CUDA GPU with 6 GB+ VRAM)**, then follow the per-engine READMEs.

## edge-tts bonus retry (Wave 4 — 1 shot, 30 s timeout)

**4th failure, unchanged.** `~/venvs/wave3-voice/bin/edge-tts --proxy "$https_proxy" --voice en-US-AriaNeural --text "The block remembers." --write-media /tmp/edge_tts_wave4.mp3` → `aiohttp.client_exceptions.WSServerHandshakeError: 101, message='Invalid connection header'` on the wss handshake to `speech.platform.bing.com`; 0-byte output deleted. Existing `tools/voice/PROOFS.md` / `sherpa-tts/PROOFS_edge_tts.md` left untouched per instructions.

## Bottom line

- **Wired with recipes + license verification:** all three (READMEs in `tools/voice/{zonos,dia,vibevoice}/`).
- **Proven on this box:** pip installs (Zonos with one-line upstream packaging patch; Dia via lean `--no-deps` path), `import` of both model classes, HF config downloads, espeak-ng install, DAC codec round-trip (component only).
- **Honest failures:** no TTS audio from any engine — weights (3.25 / 6.44 / 5.41 GB) exceed free disk (~1.4 GB) and free RAM (~2 GB) with exact measured byte counts; Dia is GPU-only upstream; VibeVoice-1.5B has no file-inference demo in-repo and carries upstream's research-only intent.
