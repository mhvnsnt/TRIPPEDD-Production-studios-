#!/usr/bin/env python3
"""checkpoint_render_driver.py — SPEC A-1 "Checkpoint render driver".

Frame-resumable, RAM-gated Cycles render driver for Blender.

Pattern (formalized from the proven Cape Jones render lanes — see
README.md "Donor / prior art"):

  * ONE frame per Blender invocation. A crash, OOM or VM restart loses
    at most one frame of work.
  * A JSON inventory (``inventory.json`` in the output dir) records every
    completed frame with its SHA-256, byte size and render duration.
  * On (re)start the driver re-hashes every frame on disk: frames whose
    hash matches the inventory are skipped; the render resumes from the
    first missing or corrupt frame. Existing frames with no inventory
    entry are adopted (hashed and recorded) so hand-copied frames are
    not re-rendered either.
  * Before every frame launch the driver waits until free RAM
    (``MemAvailable``) is above a configurable threshold.
  * At the end it verifies the full frame set (presence + SHA-256) and
    reports PASS/FAIL. Optionally (``--stitch``, OFF by default) it
    stitches an mp4 with ffmpeg once — and only if — verification passes.

Usage:
    python3 checkpoint_render_driver.py \
        --blend scene.blend --output-dir frames/ \
        --frame-start 1 --frame-end 81 \
        --resolution-x 960 --resolution-y 540 --samples 32

    python3 checkpoint_render_driver.py --config config.json

CLI args override config-file values. Exit codes: 0 = verified complete,
1 = incomplete/failed frames remain, 2 = usage/environment error.
Stdlib only; requires Blender on the path given by --blender and
(optional, only for --stitch) ffmpeg.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER_ONE = os.path.join(HERE, "render_one.py")
INVENTORY_NAME = "inventory.json"
LOG_NAME = "driver.log"

DEFAULTS = {
    "blend": None,
    "output_dir": None,
    "frame_start": 1,
    "frame_end": 1,
    "prefix": "frame_",
    "engine": "CYCLES",
    "device": "CPU",
    "samples": 32,
    "adaptive_sampling": True,
    "adaptive_threshold": 0.01,
    "denoise": True,
    "persistent_data": True,
    "resolution_x": None,
    "resolution_y": None,
    "resolution_percentage": 100,
    "fps": 24,
    "view_transform": None,
    "blender": "blender",
    "min_free_mb": 3000,
    "ram_poll_seconds": 15,
    "ram_timeout_seconds": 0,  # 0 = wait forever
    "max_attempts_per_frame": 3,
    "retry_delay_seconds": 10,
    "frame_timeout_seconds": 0,  # 0 = no timeout
    "stitch": False,
    "stitch_output": None,
    "xvfb": True,
}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def mem_available_mb() -> int:
    """MemAvailable from /proc/meminfo (Linux). Falls back to `free`."""
    try:
        with open("/proc/meminfo") as fh:
            for line in fh:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) // 1024
    except OSError:
        pass
    try:
        out = subprocess.run(
            ["free", "-m"], capture_output=True, text=True, timeout=10
        ).stdout
        for line in out.splitlines():
            if line.startswith("Mem:"):
                return int(line.split()[6])
    except Exception:
        pass
    return 0


class Driver:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.outdir = os.path.abspath(cfg["output_dir"])
        os.makedirs(self.outdir, exist_ok=True)
        self.inventory_path = os.path.join(self.outdir, INVENTORY_NAME)
        self.log_path = os.path.join(self.outdir, LOG_NAME)
        self.inventory = self._load_inventory()

    # ---------- logging / inventory ----------
    def log(self, msg: str) -> None:
        line = f"{now_iso()} {msg}"
        print(line, flush=True)
        with open(self.log_path, "a") as fh:
            fh.write(line + "\n")

    def _load_inventory(self) -> dict:
        if os.path.isfile(self.inventory_path):
            try:
                with open(self.inventory_path) as fh:
                    inv = json.load(fh)
                if isinstance(inv, dict) and "frames" in inv:
                    return inv
            except (json.JSONDecodeError, OSError):
                pass
        return {"version": 1, "frames": {}, "created": now_iso()}

    def _save_inventory(self) -> None:
        self.inventory["updated"] = now_iso()
        tmp = self.inventory_path + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(self.inventory, fh, indent=2, sort_keys=True)
        os.replace(tmp, self.inventory_path)

    def frame_path(self, frame: int) -> str:
        return os.path.join(
            self.outdir, f"{self.cfg['prefix']}{frame:04d}.png"
        )

    # ---------- verification ----------
    def check_frame(self, frame: int) -> str:
        """Return 'ok', 'missing', or 'corrupt' for one frame."""
        path = self.frame_path(frame)
        if not (os.path.isfile(path) and os.path.getsize(path) > 0):
            return "missing"
        entry = self.inventory["frames"].get(str(frame))
        if entry is None:
            return "unrecorded"
        if os.path.getsize(path) != entry.get("bytes"):
            return "corrupt"
        return "ok" if sha256_file(path) == entry.get("sha256") else "corrupt"

    def scan(self) -> dict:
        """Classify every frame in range; adopt unrecorded valid files."""
        status = {}
        adopted = 0
        for f in range(self.cfg["frame_start"], self.cfg["frame_end"] + 1):
            st = self.check_frame(f)
            if st == "unrecorded":
                path = self.frame_path(f)
                self.inventory["frames"][str(f)] = {
                    "file": os.path.basename(path),
                    "sha256": sha256_file(path),
                    "bytes": os.path.getsize(path),
                    "status": "adopted",
                    "finished": now_iso(),
                }
                st = "ok"
                adopted += 1
            status[f] = st
        if adopted:
            self._save_inventory()
            self.log(f"scan: adopted {adopted} pre-existing frame(s)")
        return status

    def verify_all(self) -> bool:
        status = self.scan()
        bad = {f: s for f, s in status.items() if s != "ok"}
        total = len(status)
        self.log(
            f"verify: {total - len(bad)}/{total} frames OK"
            + (f"; not OK: {bad}" if bad else "")
        )
        return not bad

    # ---------- RAM gate ----------
    def wait_for_ram(self) -> bool:
        need = int(self.cfg["min_free_mb"])
        deadline = (
            time.time() + self.cfg["ram_timeout_seconds"]
            if self.cfg["ram_timeout_seconds"]
            else None
        )
        while True:
            avail = mem_available_mb()
            if avail >= need:
                return True
            self.log(f"ram-gate: available={avail}MB < required={need}MB; waiting")
            if deadline and time.time() > deadline:
                self.log("ram-gate: TIMEOUT waiting for RAM")
                return False
            time.sleep(self.cfg["ram_poll_seconds"])

    # ---------- rendering ----------
    def render_frame(self, frame: int) -> bool:
        cfg = self.cfg
        settings = {
            "frame": frame,
            "output_dir": self.outdir,
            "prefix": cfg["prefix"],
            "engine": cfg["engine"],
            "device": cfg["device"],
            "samples": cfg["samples"],
            "adaptive_sampling": cfg["adaptive_sampling"],
            "adaptive_threshold": cfg["adaptive_threshold"],
            "denoise": cfg["denoise"],
            "persistent_data": cfg["persistent_data"],
            "resolution_x": cfg["resolution_x"],
            "resolution_y": cfg["resolution_y"],
            "resolution_percentage": cfg["resolution_percentage"],
            "fps": cfg["fps"],
            "view_transform": cfg["view_transform"],
        }
        cmd = [
            cfg["blender"], "-b", os.path.abspath(cfg["blend"]),
            "--python", RENDER_ONE, "--", json.dumps(settings),
        ]
        if cfg["xvfb"] and shutil.which("xvfb-run"):
            cmd = ["xvfb-run", "-a", "env", "-u", "PYTHONPATH"] + cmd
        blender_log = os.path.join(self.outdir, "blender_frames.log")
        t0 = time.time()
        try:
            with open(blender_log, "a") as lf:
                lf.write(f"\n===== frame {frame} {now_iso()} =====\n")
                lf.flush()
                rc = subprocess.run(
                    cmd,
                    stdout=lf,
                    stderr=subprocess.STDOUT,
                    timeout=cfg["frame_timeout_seconds"] or None,
                ).returncode
        except subprocess.TimeoutExpired:
            self.log(f"frame {frame}: TIMEOUT after {cfg['frame_timeout_seconds']}s")
            return False
        dur = time.time() - t0
        path = self.frame_path(frame)
        if rc == 0 and os.path.isfile(path) and os.path.getsize(path) > 0:
            digest = sha256_file(path)
            self.inventory["frames"][str(frame)] = {
                "file": os.path.basename(path),
                "sha256": digest,
                "bytes": os.path.getsize(path),
                "status": "rendered",
                "seconds": round(dur, 2),
                "finished": now_iso(),
            }
            self._save_inventory()
            self.log(f"frame {frame}: OK rc=0 dur={dur:.1f}s sha256={digest[:12]}…")
            return True
        self.log(
            f"frame {frame}: FAILED rc={rc} dur={dur:.1f}s "
            f"(output {'present' if os.path.isfile(path) else 'missing'})"
        )
        return False

    # ---------- main loop ----------
    def run(self) -> int:
        cfg = self.cfg
        frames = list(range(cfg["frame_start"], cfg["frame_end"] + 1))
        self.log(
            f"DRIVER START blend={cfg['blend']} frames={frames[0]}-{frames[-1]} "
            f"engine={cfg['engine']} samples={cfg['samples']} "
            f"out={self.outdir} min_free_mb={cfg['min_free_mb']}"
        )
        status = self.scan()
        todo = [f for f in frames if status[f] != "ok"]
        done = len(frames) - len(todo)
        self.log(f"resume scan: {done}/{len(frames)} already verified; {len(todo)} to render"
                 + (f"; first missing = frame {todo[0]}" if todo else ""))

        attempts = {f: 0 for f in todo}
        queue = list(todo)
        while queue:
            frame = queue.pop(0)
            if not self.wait_for_ram():
                self.log("ABORT: RAM gate timeout")
                return 1
            attempts[frame] += 1
            if self.render_frame(frame):
                continue
            if attempts[frame] < cfg["max_attempts_per_frame"]:
                self.log(
                    f"frame {frame}: retry {attempts[frame] + 1}/"
                    f"{cfg['max_attempts_per_frame']} after "
                    f"{cfg['retry_delay_seconds']}s"
                )
                time.sleep(cfg["retry_delay_seconds"])
                queue.append(frame)
            else:
                self.log(f"frame {frame}: GAVE UP after {attempts[frame]} attempts")

        ok = self.verify_all()
        if not ok:
            self.log("DRIVER DONE: INCOMPLETE — see verify line above")
            return 1
        self.log("DRIVER DONE: ALL FRAMES VERIFIED")
        if cfg["stitch"]:
            return 0 if self.stitch() else 1
        return 0

    def stitch(self) -> bool:
        cfg = self.cfg
        if not shutil.which("ffmpeg"):
            self.log("stitch: ffmpeg not found — skipping (frames are verified)")
            return False
        out = cfg["stitch_output"] or os.path.join(
            os.path.dirname(self.outdir.rstrip("/")) or ".",
            f"{os.path.basename(self.outdir.rstrip('/'))}.mp4",
        )
        pattern = os.path.join(self.outdir, f"{cfg['prefix']}%04d.png")
        cmd = [
            "ffmpeg", "-y", "-framerate", str(cfg["fps"]),
            "-start_number", str(cfg["frame_start"]),
            "-i", pattern, "-c:v", "libx264", "-pix_fmt", "yuv420p", out,
        ]
        self.log(f"stitch: {' '.join(cmd)}")
        rc = subprocess.run(cmd, capture_output=True, text=True).returncode
        self.log(f"stitch: {'OK -> ' + out if rc == 0 else 'FAILED rc=' + str(rc)}")
        return rc == 0


def load_config(args) -> dict:
    cfg = dict(DEFAULTS)
    if args.config:
        with open(args.config) as fh:
            file_cfg = json.load(fh)
        unknown = set(file_cfg) - set(DEFAULTS)
        if unknown:
            print(f"warning: ignoring unknown config keys: {sorted(unknown)}",
                  file=sys.stderr)
        cfg.update({k: v for k, v in file_cfg.items() if k in DEFAULTS})
    # CLI overrides (only when explicitly given)
    for key in DEFAULTS:
        val = getattr(args, key, None)
        if val is not None:
            cfg[key] = val
    return cfg


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Checkpoint render driver (SPEC A-1): one frame per "
        "Blender invocation, hash-verified inventory, RAM gate, resume "
        "from first missing/corrupt frame."
    )
    p.add_argument("--config", help="JSON config file (CLI args override it)")
    p.add_argument("--blend")
    p.add_argument("--output-dir")
    p.add_argument("--frame-start", type=int)
    p.add_argument("--frame-end", type=int)
    p.add_argument("--prefix")
    p.add_argument("--engine", choices=["CYCLES", "BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"])
    p.add_argument("--device", choices=["CPU", "GPU"])
    p.add_argument("--samples", type=int)
    p.add_argument("--resolution-x", type=int)
    p.add_argument("--resolution-y", type=int)
    p.add_argument("--resolution-percentage", type=int)
    p.add_argument("--fps", type=int)
    p.add_argument("--view-transform")
    p.add_argument("--blender", help="path to the blender binary")
    p.add_argument("--min-free-mb", type=int,
                   help="free-RAM gate: wait until MemAvailable >= this (MB)")
    p.add_argument("--max-attempts-per-frame", type=int)
    p.add_argument("--stitch", action="store_true", default=None,
                   help="after verification passes, stitch an mp4 via ffmpeg "
                   "(OFF by default)")
    p.add_argument("--stitch-output")
    p.add_argument("--no-xvfb", dest="xvfb", action="store_false", default=None,
                   help="do not wrap Blender in xvfb-run")
    p.add_argument("--verify-only", action="store_true",
                   help="only verify the frame set + inventory; render nothing")
    return p


def main() -> int:
    args = build_parser().parse_args()
    cfg = load_config(args)
    if not cfg["blend"] and not args.verify_only:
        print("error: --blend is required (or in config)", file=sys.stderr)
        return 2
    if not cfg["output_dir"]:
        print("error: --output-dir is required (or in config)", file=sys.stderr)
        return 2
    if cfg["blend"] and not os.path.isfile(cfg["blend"]):
        print(f"error: blend file not found: {cfg['blend']}", file=sys.stderr)
        return 2
    if cfg["frame_end"] < cfg["frame_start"]:
        print("error: --frame-end must be >= --frame-start", file=sys.stderr)
        return 2
    driver = Driver(cfg)
    if args.verify_only:
        return 0 if driver.verify_all() else 1
    return driver.run()


if __name__ == "__main__":
    sys.exit(main())
