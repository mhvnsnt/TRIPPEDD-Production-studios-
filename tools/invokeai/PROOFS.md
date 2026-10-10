# PROOFS — InvokeAI full install + CPU smoke test (Wave 3 Worker C, 2026-10-07)

Nothing here is simulated. Every claim below has a log or an artifact.

## 1. Install — SUCCESS
- `pip install invokeai` → **invokeai 6.14.2** (PyPI, Apache-2.0) in a Python 3.12 venv.
- Full dep tree: torch-2.14.1+cpu, torchvision-0.29.1+cpu, diffusers-0.40.0,
  transformers-5.5.4, onnxruntime-1.19.2, mediapipe, jupyter stack, ~190 packages.
- Install log: `~/workspace/agent-ops/scratch/w3c-invoke/install3.log`
  ("Successfully installed ... invokeai-6.14.2 ...").
- Two gotchas documented in README.md: (1) default install pulls CUDA torch —
  use `--extra-index-url https://download.pytorch.org/whl/cpu` on CPU boxes;
  (2) pip needs `TMPDIR` on the big volume when `/tmp` is a small tmpfs.

## 2. Server boot — SUCCESS
- `invokeai-web` with `INVOKEAI_ROOT` + `invokeai.yaml`
  (`schema_version: "4.0.3"`, port 19090): database initialized, model manager
  up, **"Invoke running on http://127.0.0.1:19090"**.
- `GET /api/v1/app/version` → `{"version":"6.14.2"}`.
- Config note: hand-written `invokeai.yaml` needs `schema_version: "4.0.3"`
  or the loader dies with `KeyError: 'schema_version'`; `invokeai-web` takes
  no `--port` flag (port lives in the yaml).
- Server log: `~/workspace/agent-ops/scratch/w3c-invoke/server3.log`.

## 3. Model install — SUCCESS
- SD 1.5 `v1-5-pruned-emaonly.safetensors` (4,265,146,304 bytes, downloaded
  from huggingface.co/runwayml/stable-diffusion-v1-5; integrity checked with
  `safetensors`: 1145 tensors, first `alphas_cumprod`).
- Installed via `POST /api/v2/models/install?source=<local path>` →
  job completed, model key `f3e6e07d-1388-40df-b996-b21b4e3ecf38`
  (name `sd15-smoke`, base `sd-1`, type `main`).

## 4. Generation — SUCCESS (real image, CPU)
- Enqueued via `POST /api/v1/queue/default/enqueue_batch` with a 6-node
  SD1.5 text-to-image graph (`main_model_loader` → `compel` ×2 → `noise` →
  `denoise_latents` (10 steps, euler, cfg 7.5) → `l2i`), 512×512, seed 1234.
  Batch `cbc1012c-0b4f-4c77-87ff-b42420f4dca9` → status `completed`.
- Prompt: "a friendly cartoon wizard with a purple robe, flat 2d animation
  style". Negative: "blurry, photo, watermark".
- Timing: ~35 s/step on this CPU box, ~6 min for 10 steps.
- **Proof: `proof-smoke.png`** (303,798 bytes, in this directory) — opened and
  eyeballed 2026-10-07: cartoon wizard in purple robe + pointed hat, flat 2D
  style, blue sky. Matches the prompt. Downloaded from
  `GET /api/v1/images/i/084e71e2-001f-4d85-bcbe-f2dc20191376.png/full`.

## 5. Honest failure encountered and fixed
- First generation attempt failed with `InvalidURL: Invalid port: ':1]'` —
  the known httpx/no_proxy IPv6-literal bug (see `~/TOOLS.md`). The InvokeAI
  server had inherited the sandbox's `no_proxy` (contains `[::1]` etc.).
  Fixed by restarting the server with IPv6 literals stripped from
  `no_proxy`/`NO_PROXY` (see `start-server.sh` in the scratch dir).
  Second attempt completed cleanly. Documented so the next worker doesn't
  re-hit it.

## Limits
- CPU-only: 10-step 512² SD1.5 ≈ 6 min. Hero-quality generations belong on a
  GPU box, but the full InvokeAI generation path is proven working here.
- Scratch (venv, server root, logs, scripts): `~/workspace/agent-ops/scratch/w3c-invoke/`
