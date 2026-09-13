"""Canonical motion-proof launcher: prove the scene selected is the scene rendered.

OWNER LAW: CHECK THE THING YOU TEST IS THE THING THAT RUNS.

The hi-res render scene is an explicit input. This launcher refuses to silently
fall back to the old cage/LOD scene and writes a machine-readable invocation
receipt containing the exact scene SHA-256 before Blender is launched.

Usage:
  python tools/character/run_motion_proof_canonical.py --clip blink
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CANONICAL = os.path.join(ROOT, "assets", "rigs", "MARS_FACE_HIRES.blend")
RECEIPT_DIR = os.path.join(ROOT, "renders", "_motion")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", default="blink")
    ap.add_argument("--blender", default=os.path.join(ROOT, "vendor", "blender", "blender"))
    ap.add_argument("--frames", default="16")
    ap.add_argument("--res", default="540")
    args = ap.parse_args()

    if not os.path.isfile(CANONICAL):
        print(f"UNKNOWN: canonical hi-res scene missing: {CANONICAL}")
        return 45
    if not os.path.isfile(args.blender):
        print(f"UNKNOWN: Blender missing: {args.blender}")
        return 45

    # These are known stale/ambiguous scene names. A proof may not accidentally
    # resolve one of them by cwd, glob order, or an old default argument.
    stale_names = [
        "MARS_FACE_HIRES_LOD1.blend",
        "MARS_FACE_HIRES_OLD.blend",
        "MARS_FACE_LATEST.blend",
    ]
    nearby = []
    for base in (os.path.join(ROOT, "assets", "rigs"), os.path.join(ROOT, "renders")):
        if os.path.isdir(base):
            for name in os.listdir(base):
                if name in stale_names:
                    nearby.append(os.path.join(base, name))
    if nearby:
        print("UNKNOWN: stale/ambiguous hi-res scene(s) exist; delete or quarantine them before proof:")
        for p in nearby:
            print("  ", p)
        return 45

    digest = sha256(CANONICAL)
    out = os.path.join(RECEIPT_DIR, args.clip, "invocation.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    receipt = {
        "schema": "trippedd.mars-motion-proof-invocation/v1",
        "status": "PASS",
        "scene": os.path.relpath(CANONICAL, ROOT),
        "sceneSHA256": digest,
        "sceneSelection": "EXPLICIT_CANONICAL_HIRES",
        "clip": args.clip,
        "blender": os.path.relpath(args.blender, ROOT),
        "argv": ["--rig", CANONICAL, "--clip", args.clip, "--frames", args.frames, "--res", args.res],
    }
    with open(out, "w") as f:
        json.dump(receipt, f, indent=2)
    print(f"CANONICAL SCENE: {CANONICAL}")
    print(f"CANONICAL SHA256: {digest}")
    print(f"INVOCATION RECEIPT: {out}")

    cmd = [
        args.blender, "-b", "-P", os.path.join(ROOT, "tools", "character", "motion_proof.py"),
        "--", "--rig", CANONICAL, "--clip", args.clip,
        "--frames", args.frames, "--res", args.res,
    ]
    print("EXEC:", " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
