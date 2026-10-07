# PROOFS — Wave 4 lip-sync wiring (Worker B)

Date: 2026-10-07. Lane: `tools/lipsync/`. Sandbox: CPU-only (no `nvidia-smi`),
7 GB RAM. Nothing was faked: every claim below names what actually ran.

## 1. Wan2.2-S2V — BLOCKED-HONEST (no GPU in sandbox)

- **License: Apache-2.0 — VERIFIED from upstream.** `Wan-Video/Wan2.2`
  `LICENSE.txt` is the Apache 2.0 text (cloned `--depth 1`, vendored
  excerpt under `tools/lipsync/wan2p2-s2v/upstream/`); HF model card for
  `Wan-AI/Wan2.2-S2V-14B` reports `cardData.license: apache-2.0`
  (HF API, 2026-10-07). Commercial-safe.
- Verified in-sandbox: repo layout, `requirements_s2v.txt`, S2V CLI surface
  in `generate.py` (`--task s2v-14B --ckpt_dir … --image … --audio …`),
  official GPU compute table (`upstream/assets/comp_effic.png`).
- **GPU-worker handoff:** ≥80 GB VRAM single-GPU for the first-party command
  (e.g. H100/H20 80 GB); multi-GPU via
  `--ulysses_size 4/8 --dit_fsdp --t5_fsdp`. Reference: A14B backbone at
  720p ≈ 1050 s / 60 GB peak on 1×H100 (81 frames @24fps); S2V-14B is in the
  same band. Weights `Wan-AI/Wan2.2-S2V-14B` (~28 GB bf16). Exact command in
  `tools/lipsync/wan2p2-s2v/README.md`. Community VRAM-optimised forks exist
  (Apache-2.0) — re-measure on target hardware before quoting lower numbers.
- **Sandbox error log:** none — no inference attempted (no GPU, no 28 GB
  download on 4.3 GB free disk). Deliberately not faked.

## 2. Ditto — PARTIAL (CPU proof of audio→motion brain: RAN, real output)

- **License: Apache-2.0 — VERIFIED from upstream.**
  `antgroup/ditto-talkinghead` README: "released under the Apache-2.0
  license"; GitHub license badge Apache-2.0. Weights
  `digital-avatar/ditto-talkinghead` (HF). Commercial-safe.
- **Proof (this sandbox, CPU, onnxruntime 1.30.0, no TensorRT, no CUDA):**
  `tools/lipsync/ditto/ditto_cpu_motion_proof.py`
  - `hubert.onnx` (1.4 GB, downloaded from HF) → 16 kHz WAV →
    1024-dim audio features @25 fps — REAL, timed in-script.
  - cond assembly = aud(1024) + neutral emo(8) + eye_open(2) + eye_ball(6) +
    sc(63) = 1103-dim (matches upstream `v0.4_hubert_cfg_pytorch.pkl`).
  - `lmdm_v0.4_hubert.onnx` + upstream `core/models/lmdm.py` LMDM class
    (CPUExecutionProvider), 50 DDIM steps, 80-frame window →
    `(1, 80, 265)` motion keypoint sequence → saved `.npy` in `proofs/`.
- **Honest caveats:** `cond_frame` (source-face keypoint condition) is a
  neutral zeros vector and emo/eye/sc are neutral constants — the full
  pipeline derives them from the source portrait via the motion extractor /
  face registration. This proves the audio-driven motion generator, not
  portrait rendering. The warp renderer (appearance/warp/stitch/decoder
  ONNX) was NOT run here.
- **GPU-worker handoff:** full offline pipeline =
  `stream_pipeline_offline.py`/`inference.py` with `ditto_pytorch/*` or the
  ONNX set via `scripts/cvt_onnx_to_trt.py`; realtime on RTX 3090/4090
  (24 GB), 8 GB minimum reported. Exact recipe in
  `tools/lipsync/ditto/README.md`.
- **Environment quirk hit:** `huggingface_hub`'s httpx crashes on this
  sandbox's `no_proxy` IPv6 literals (`::1`, `[::1]`) —
  `httpx.InvalidURL: Invalid port: ':1]'`. Workaround (documented in the
  Ditto README): strip entries containing `::` from `no_proxy`/`NO_PROXY`
  before downloading (matches `~/TOOLS.md` proxy note). `curl -L` on the
  HF resolve URLs works without the workaround.
- **Sandbox error log:** (a) initial `pip install` on system python blocked
  by PEP 668 → used a venv; (b) `/tmp` is a 512 MB tmpfs → moved venv to
  `~/workspace/.venvs/ditto`; (c) first HF download stalled at 440 MB in
  cache → killed, restarted with `curl -L --retry -C -` (~2.2 MB/s through
  the egress proxy).

### Ditto proof run record

Command (CPU, onnxruntime 1.30.0, 7 GB RAM sandbox):

    python ditto_cpu_motion_proof.py \
      --audio ../proofs/rhubarb_speech_3s.wav \
      --out   proofs/ditto_motion_3s.npy

Input: `tools/lipsync/proofs/rhubarb_speech_3s.wav` — 3.05 s of real Piper
TTS speech ("The council does not explain itself. It declares."), 16 kHz
mono, the same file used for the rhubarb smoke test.

Results (verbatim from the run):
- `[2/4] hubert.onnx -> audio features` → `aud_feat: (77, 1024) in 20.2s`
- `[3/4]` cond `(77, 1103)` (aud 1024 + neutral emo 8 + eye_open 2 +
  eye_ball 6 + sc 63 — matches upstream `audio_feat_dim=1103`)
- `[4/4] lmdm diffusion sampling (50 steps, 80-frame window)` →
  `diffusion done in 19.9s` → `proofs/ditto_motion_3s.npy`, shape
  `(1, 80, 265)`, float32, sha256
  `6297d26bd85490fe8d8af1403792c4ce32a4e6971865d91e397e2354b779bcac`
- Sanity: per-dim temporal std min 0.0000 / mean 0.0095 / max 0.0303 —
  the sequence is temporally alive, not frozen noise.

Audio-conditioning check (same seed, same 50 steps, speech vs 3.05 s of
digital silence — silence run at `/tmp/ditto_motion_silence50.npy`):
- pose dims pitch/yaw/roll (1:199): mean|speech−silence| = 0.01733
- exp dims (202:265): mean|speech−silence| = 0.00056 (near-neutral under
  the neutral face condition)
- all 265 dims: mean|speech−silence| = 0.01321

Read honestly: the output motion IS audio-conditioned (head-pose motion
differs clearly between speech and silence); expression dims stay
near-neutral with the neutral `cond_frame`. This proves the real
audio→motion path end-to-end on CPU — not portrait rendering, not a
beauty claim.

Bugs hit and fixed during the proof (all in `ditto_cpu_motion_proof.py`):
- hubert.onnx output is 2-D `(T, 1024)`, not `(1, T, 1024)` — frame slice
  is `enc[-14:-4]`, no `[0]` index.
- upstream `core/models/lmdm.py` imports torch at module level → the proof
  carries a faithful torch-free numpy port of `_init_np/_setup_np/_one_step/
  _call_np` (DDIM, eta=1) instead of importing it; no behavior change.
- loop variable shadowed the `time` module; float64 schedule arrays
  promoted the state — scalars cast to Python floats, state kept float32.

## 3. OVRLipSync — PARTIAL (blocked-honest on SDK download)

- **License: Oculus SDK License (proprietary Meta EULA) — posture verified
  from mirrors, primary text UNVERIFIED.** Five independent mirrors
  (aerovfx/ovrlipsync-ue5, metyatech/ovrlipsync-ue5, viniciushelder/
  ovrlipsync-ue5, avatarsdk/metaperson-oculus-ue-sample,
  Shiyatzu/OculusLipsyncPlugin-UE5) all state the plugin is "provided under
  the Oculus SDK License, which allows for personal and commercial use".
  The canonical license text at `developer.oculus.com/licenses/…` returned
  **HTTP 403** from this sandbox, so the primary source could not be read.
  Badge: **commercial-OK-per-mirrors / proprietary-EULA — owner must read
  the actual text before commercial ship.**
- Verified in-sandbox: the download page
  `https://developers.meta.com/vr/downloads/package/oculus-lipsync-sdk/`
  (301 from `developer.oculus.com`, then HTTP 200) contains only a login
  redirect (`/login/?redirect_uri=…/oculus-lipsync-sdk/`) — **downloading
  the SDK requires a Meta developer account sign-in**, not attempted with
  credentials.
- Integration path documented in `tools/lipsync/ovr-lipsync/README.md`:
  native C API (`LibOVRLipSync/<platform>/libovrlipsync.*` +
  `Include/OVRLipSync.h`; feed 512-sample float PCM chunks → 15 viseme
  weights + laughter score per frame), Unity components
  (`OVRLipSyncContext`, `OVRLipSyncContextMorphTarget`), Unreal plugin
  (`Edit → Plugins → Audio`, `[Voice] bEnabled=true`). Exact C signatures
  must be verified against the shipped `OVRLipSync.h` — documented from
  SDK-header knowledge, not from a downloaded copy.
- **Owner handoff:** (1) owner signs in at developers.meta.com → Downloads →
  Oculus Lipsync SDK; (2) stage `LibOVRLipSync/<platform>/libovrlipsync.*` +
  `Include/OVRLipSync.h` into `tools/lipsync/ovr-lipsync/sdk/` (do NOT commit
  the binary until the EULA is confirmed to allow redistribution); (3) read
  the actual Oculus SDK License text and confirm commercial terms before
  shipping; (4) wire the C API and add the automated proof (feed the 3 s
  test WAV, record the viseme stream, assert non-silent visemes during
  speech frames).
- **Sandbox error log:** `browser.open` on the Meta developer docs page →
  HTTP 403 (not retried — treated as the access-denied it is).

## Lane files

- `tools/lipsync/wan2p2-s2v/README.md` — install recipe, run command,
  GPU handoff spec
- `tools/lipsync/ditto/README.md` — install recipe, CPU proof command,
  GPU handoff spec
- `tools/lipsync/ditto/ditto_cpu_motion_proof.py` — the CPU proof script
- `tools/lipsync/ditto/proofs/ditto_motion_3s.npy` — the real proof artifact
- `tools/lipsync/ovr-lipsync/README.md` — license posture, download attempt,
  integration path, owner handoff
- `tools/lipsync/{ditto,wan2p2-s2v,ovr-lipsync}/.gitignore` — `weights/`,
  `upstream/`, `sdk/` kept out of git

## License summary (badges)

| Engine | License | Verified from | Badge |
|---|---|---|---|
| Wan2.2-S2V | Apache-2.0 | upstream `LICENSE.txt` + HF model card | commercial-safe |
| Ditto | Apache-2.0 | upstream README + GitHub license badge | commercial-safe |
| OVRLipSync | Oculus SDK License (Meta proprietary EULA) | 5 mirrors agree "personal and commercial use"; canonical text 403 | commercial-OK-per-mirrors / verify-EULA-before-ship |

No GPL/AGPL encountered — nothing quarantined.
