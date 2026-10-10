# InvokeAI — permissive local generation backend (Wave 3: full install)

Date: 2026-10-07.

## License (verified 2026-10-07, primary sources)
**Apache-2.0** — GitHub API `invoke-ai/InvokeAI` → `license.spdx_id =
"Apache-2.0"`; PyPI `invokeai` 6.14.2 classifier "License :: OSI Approved ::
Apache Software License". ✅ commercial-safe.

**Model-license caveat (unchanged from Wave 2):** the software is Apache-2.0,
but the *models* you run in it carry their own licenses (SD/SDXL: Stability
Community License — non-commercial; FLUX.1-dev: non-commercial). Commercial-safe
generation needs commercial-safe model weights; the backend license does not
launder the model license.

## Install (CPU-only, verified path)
```bash
python3 -m venv venv
TMPDIR=<big-volume-tmp> venv/bin/pip install --no-cache-dir --prefer-binary \
  --extra-index-url https://download.pytorch.org/whl/cpu invokeai
```
Two gotchas found 2026-10-07 (both cost a full install attempt each):
1. Default `pip install invokeai` resolves CUDA torch → multi-GB NVIDIA wheels.
   On a CPU box, use the PyTorch **CPU** index as above.
2. pip unpacks big wheels into `TMPDIR`; if `/tmp` is a small tmpfs (512 MB
   here), set `TMPDIR` to a directory on the big volume or you get
   `OSError: [Errno 28] No space left on device` on the torch wheel.

## Pipeline slot
Local still/frame generation backend for the cartoon pipeline: concept art,
background plates, style-locked character stills — the permissive-licensed
substitute for the GPL-quarantined ComfyUI / AGPL-quarantined AUTOMATIC1111.

## Smoke test
See PROOFS.md.
