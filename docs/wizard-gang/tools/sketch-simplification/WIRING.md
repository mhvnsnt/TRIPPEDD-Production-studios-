# WIRING — sketch-simplification (Simo-Serra et al.) — BLOCKED
**Status: NOT WIRED — blocked, 2026-11-13 (exact blockers below, no proof)**
**Upstream:** https://github.com/bobbens/sketch_simplification (MIT) — the
Simo-Serra et al. line-cleanup model (SIGGRAPH Asia 2017). Successor:
https://github.com/MarkMoHR/virtual_sketching (same group, SIGGRAPH 2021,
modern PyTorch, `test_rough_sketch_simplification.py`,
`pretrain_rough_sketches` model 105 MB).
**Local state:** source cloned at `~/workspace/tools/sketch-simplification/`
(bobbens) and `work/virtual-sketching/` (MarkMoHR); venv at
`~/workspace/tools/sketch-simplification/venv/` (torch NOT installed).
**Gap it would fill:** cleanup — turning rough pencil sketches into clean
line art automatically (the stage between Storypencil boards and Grease
Pencil ink). No other free tool in the stack does learned line cleanup.

## Exact blockers (all three must clear)
1. **Torch will not install on this VM (disk quota wall).** Two attempts:
   `pip install --no-cache-dir torch==2.2.2 torchvision==0.17.2` failed
   `OSError(28) No space left on device` at 152.0/186.7 MB of the torch
   wheel (2026-11-13, twice), while `df` shows 29 GB free — the volume's
   quota wall trips on ~150 MB+ single writes. Freeing 207 MB of my own
   redundant files did not clear it (torch needs ~850 MB installed).
2. **The original cannot run on modern torch anyway.** It needs PyTorch
   0.4.1 and `torch.utils.serialization.load_lua` (removed in PyTorch 1.6+);
   its `.t7` models are Torch7 format. PyTorch 0.4.1 cannot install on
   Python 3.12. The modern successor (virtual_sketching) is the only
   runnable path — and it needs torch (blocker 1).
3. **The model download is too slow to finish here.** `download_models.sh`
   fetches `model_gan.t7` (~350 MB) from `https://esslab.jp/~ess/data/` at
   ~20 KB/s (wget progress, ETA ~4h36m); the partial reached 92,831,744 B
   with MD5 `499504603315997b989bb1959514d0a1` vs expected
   `3a5b4088f2490ca4b8140a374e80c878` (mismatch — incomplete). The partial
   was deleted 2026-11-13 to ease the disk wall.
**What would unblock it:** a VM/disk state where torch installs (quota headroom
or a pre-built torch), then the virtual_sketching route with its
`pretrain_rough_sketches` model. Do NOT attempt the bobbens original on
modern torch — it is a dead end by design.
