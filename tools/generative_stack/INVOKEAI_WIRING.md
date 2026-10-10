# InvokeAI — permissive local generation backend (Wave 2 wiring, docs-path)

Date: 2026-10-07. Repo: both (trippedd production + god-molecule creative).

## License (verified 2026-10-07)
**Apache-2.0** — confirmed via `github.com/invoke-ai/InvokeAI` repo metadata.
This is the shippable substitute for the GPL-quarantined backends:
- ComfyUI = GPL-3.0 → quarantined
- AUTOMATIC1111 SD WebUI = AGPL-3.0 → quarantined

**Model-license caveat:** InvokeAI the software is Apache-2.0, but the
*models* you run in it carry their own licenses (SD/SDXL: Stability Community
License — non-commercial; FLUX: FLUX.1-dev non-commercial; SDXL-Turbo etc.).
Commercial-safe generation needs commercial-safe model weights (e.g. models
under Apache-2.0/CC0) — the backend license does not launder the model license.

## Wiring status
**Docs-path (Wave 2).** InvokeAI is a full application with a multi-GB
dependency tree + model downloads — it installs on a workstation/GPU box, not
in this sandbox. Install path:

```bash
pip install invokeai        # then: invokeai-web
```

First launch downloads the default SDXL-class model set; point it at
commercial-safe weights for shipped work.

## Pipeline slot
Local still/frame generation backend for the cartoon pipeline: concept art,
background plates, and style-locked character stills — everywhere the
storyboard calls for generated imagery, without touching GPL code.
