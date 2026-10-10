#!/usr/bin/env python3
"""Run the first-shot Blender render without fabricating evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "trippedd.render-evidence/v1"
SHOT_ID = "GM-WORLD-0001-FIRST-SHOT"
SCENE_ID = "GM-WORLD-0001"
WORLD_ID = "GM-WORLD-0001"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("rendered artifact is not a valid PNG")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def run_contract_validator(repo_root: Path) -> None:
    validator = repo_root / "scripts" / "validate_first_shot_contract.py"
    if not validator.is_file():
        raise RuntimeError(f"missing contract validator: {validator}")
    result = subprocess.run(
        [sys.executable, str(validator), "--repo-root", str(repo_root)],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or "FIRST_SHOT_CONTRACT: PASS" not in result.stdout:
        raise RuntimeError("first-shot contract validation failed\n" + result.stdout + result.stderr)


def blender_version(blender: str) -> str:
    result = subprocess.run([blender, "--version"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError("unable to query Blender version")
    return result.stdout.splitlines()[0].strip() if result.stdout.splitlines() else "unknown"


def build_receipt(repo_root: Path, receipt: Path, blend: Path, png: Path, frame: int, version: str) -> dict:
    width, height = png_dimensions(png)
    artifact_path = str(png.relative_to(receipt.parent)) if png.is_relative_to(receipt.parent) else str(png)
    return {
        "schema": SCHEMA,
        "rendered": True,
        "shot_id": SHOT_ID,
        "scene_id": SCENE_ID,
        "world_id": WORLD_ID,
        "executor": "Blender",
        "blender_version": version,
        "source_scene": {
            "path": str(blend.relative_to(repo_root)) if blend.is_relative_to(repo_root) else str(blend),
            "sha256": sha256_file(blend),
        },
        "frame": frame,
        "artifact": {
            "path": artifact_path,
            "sha256": sha256_file(png),
            "bytes": png.stat().st_size,
            "format": "png",
            "width": width,
            "height": height,
        },
        "visual_qc": "NOT_EVALUATED",
        "physical_qc": "NOT_EVALUATED",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def verify_receipt(repo_root: Path, receipt: Path) -> None:
    verifier = repo_root / "scripts" / "verify_render_evidence.py"
    if not verifier.is_file():
        raise RuntimeError(f"missing render evidence verifier: {verifier}")
    result = subprocess.run(
        [sys.executable, str(verifier), "--receipt", str(receipt)],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or "RENDER_EVIDENCE: PASS" not in result.stdout:
        raise RuntimeError("render receipt verification failed\n" + result.stdout + result.stderr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--blend", type=Path, required=True, help="existing resolved Blender scene; never synthesized by this worker")
    parser.add_argument("--blender", help="Blender executable; defaults to PATH lookup")
    parser.add_argument("--frame", type=int, default=1)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--receipt", type=Path, default=None)
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--enable-autoexec", action="store_true", help="allow Blender autoexec; off by default")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    blend = args.blend.resolve()
    output_dir = (args.output_dir or repo_root / "artifacts" / "first-shot").resolve()
    receipt = (args.receipt or output_dir / "render-receipt.json").resolve()
    log_path = (args.log or output_dir / "blender.log").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        run_contract_validator(repo_root)
        if not blend.is_file():
            raise RuntimeError(f"resolved Blender scene does not exist: {blend}")
        if blend.suffix.lower() != ".blend":
            raise RuntimeError("--blend must point to a .blend file")

        blender = args.blender or shutil.which("blender")
        if not blender:
            raise RuntimeError("Blender executable not found; provide --blender or install Blender on the worker")

        version = blender_version(blender)
        prefix = output_dir / "GM-WORLD-0001-FIRST-SHOT"
        command = [blender, "-b", str(blend), "-o", str(prefix), "-F", "PNG", "-f", str(args.frame)]
        if args.enable_autoexec:
            command.insert(1, "--enable-autoexec")

        result = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
        log_path.write_text(result.stdout + "\n--- STDERR ---\n" + result.stderr, encoding="utf-8")
        expected = Path(f"{prefix}{args.frame:04d}.png")
        if result.returncode != 0:
            raise RuntimeError(f"Blender render failed with exit code {result.returncode}; see {log_path}")
        if not expected.is_file():
            raise RuntimeError(f"Blender exited successfully but produced no expected PNG: {expected}")

        data = build_receipt(repo_root, receipt, blend, expected, args.frame, version)
        receipt.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        verify_receipt(repo_root, receipt)
        print(f"RENDER_EVIDENCE: PASS {receipt}")
        print("VISUAL_QC: NOT_EVALUATED")
        print("PHYSICAL_QC: NOT_EVALUATED")
        print("PRODUCTION_GATE: BLOCKED_UNTIL_QC")
        return 0
    except Exception as exc:
        failure = {
            "schema": SCHEMA,
            "rendered": False,
            "shot_id": SHOT_ID,
            "scene_id": SCENE_ID,
            "world_id": WORLD_ID,
            "executor": "Blender",
            "error": str(exc),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        receipt.write_text(json.dumps(failure, indent=2) + "\n", encoding="utf-8")
        print("RENDER_EVIDENCE: BLOCKED")
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
