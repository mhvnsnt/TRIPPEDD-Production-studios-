# Infra Resilience Tools

Copied from `~/workspace/3d-toolkit/infra/`. These solve the fragility that kept
breaking Blender renders:

- **`egl-restore.sh`** — Restores the EGL stack after daemon restarts wipe it.
  Run with sudo. Also runs automatically on boot via systemd.
- **`monitoring/safe-watcher.py`** — Monitor-ONLY process watcher. NEVER kills,
  deletes, or restarts anything — it only writes alerts.

See `~/workspace/3d-toolkit/infra/INFRA.md` for the full wire-up guide.
