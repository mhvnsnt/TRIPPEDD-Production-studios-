#!/usr/bin/env python3
"""Assemble a fail-closed human-review package for God Molecule oral / facial gates.

Promotion steps covered:
  oral_placement_gate → aperture_survey → human_review_evidence

This tool does NOT declare the mouth correct. It only packages physical inputs
and refuses CREATIVE_FINAL language when required pieces are missing.

Usage:
  python3 tools/character/assemble_human_review_package.py \\
    --out artifacts/evidence/god_molecule/oral-review-001 \\
    --survey path/to/aperture_survey.json \\
    --pose REST=path/to/rest.png \\
    --pose JAW_OPEN=path/to/open.png \\
    --pose PROFILE=path/to/profile.png \\
    --pose FRONT=path/to/front.png \\
    --mars-sha256 <hex> \\
    [--bridge-json config/god_molecule_trippedd_bridge.json]

Exit codes:
  0  package written; structural PASS (human still must review pixels)
  40 missing/empty required evidence — package may still be written under ./INCOMPLETE
  2  bad usage
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_POSES = ("REST", "JAW_OPEN", "PROFILE", "FRONT")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_pose(spec: str) -> tuple[str, Path]:
    if "=" not in spec:
        raise SystemExit(f"bad --pose {spec!r}; expected NAME=path")
    name, path = spec.split("=", 1)
    return name.strip().upper(), Path(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--survey", type=Path, help="aperture survey JSON")
    ap.add_argument("--pose", action="append", default=[], help="NAME=path (repeat)")
    ap.add_argument("--mars-sha256", default="")
    ap.add_argument("--bridge-json", type=Path, default=None)
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    poses = dict(parse_pose(s) for s in args.pose)
    errors: list[str] = []
    files_meta: list[dict] = []

    if args.survey is None or not args.survey.is_file() or args.survey.stat().st_size == 0:
        errors.append("missing or empty aperture survey JSON")
    for name in REQUIRED_POSES:
        p = poses.get(name)
        if p is None or not p.is_file() or p.stat().st_size == 0:
            errors.append(f"missing or empty pose image: {name}")

    survey_data = {}
    protrusion = "UNKNOWN"
    if args.survey and args.survey.is_file() and args.survey.stat().st_size:
        try:
            survey_data = json.loads(args.survey.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append("survey JSON not parseable")
            survey_data = {}
        protrusion = (
            survey_data.get("protrusion_gate")
            or survey_data.get("PROTRUSION_GATE")
            or survey_data.get("gate")
            or "UNKNOWN"
        )
        if str(protrusion).upper() not in ("PASS", "OK", "TRUE"):
            # Still package for human review, but structural gate fails
            if "PROTRUSION" not in json.dumps(survey_data).upper():
                errors.append(f"protrusion_gate not PASS (got {protrusion!r})")
            else:
                errors.append(f"protrusion_gate not PASS (got {protrusion!r})")

    incomplete = bool(errors)
    out = args.out if not incomplete else args.out.parent / (args.out.name + "_INCOMPLETE")
    out.mkdir(parents=True, exist_ok=True)
    poses_dir = out / "poses"
    poses_dir.mkdir(exist_ok=True)

    if args.survey and args.survey.is_file():
        dst = out / "aperture_survey.json"
        shutil.copy2(args.survey, dst)
        files_meta.append(
            {"role": "survey", "path": "aperture_survey.json", "sha256": sha256_file(dst)}
        )

    for name, src in poses.items():
        if not src.is_file():
            continue
        dst = poses_dir / f"{name}{src.suffix.lower() or '.png'}"
        shutil.copy2(src, dst)
        files_meta.append(
            {
                "role": "pose",
                "pose": name,
                "path": str(dst.relative_to(out)),
                "sha256": sha256_file(dst),
                "bytes": dst.stat().st_size,
            }
        )

    bridge = {}
    if args.bridge_json and args.bridge_json.is_file():
        bridge = json.loads(args.bridge_json.read_text(encoding="utf-8"))

    manifest = {
        "schema": "god-molecule.human-review-package.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "promotion_step": "human_review_evidence",
        "structural_status": "INCOMPLETE" if incomplete else "READY_FOR_HUMAN_REVIEW",
        "creative_final": False,
        "telemetry_substitution": False,
        "identity_source": "MARS_CANONICAL",
        "mars_sha256": args.mars_sha256 or None,
        "protrusion_gate": protrusion,
        "required_poses": list(REQUIRED_POSES),
        "files": files_meta,
        "errors": errors,
        "notes": args.notes,
        "bridge": {
            "name": bridge.get("bridge"),
            "version": bridge.get("version"),
            "handoff_trippedd": (bridge.get("handoff_paths") or {}).get("trippedd"),
        },
        "human_checklist": [
            "REST: lips sealed, no pink plank past lip plane",
            "JAW_OPEN: visible cavity behind lips",
            "JAW_OPEN: distinct teeth (not a pink slab) and gums when donor provides masks",
            "JAW_OPEN: tongue present if donor includes tongue",
            "PROFILE: no cavity liner / sock protruding past lips (Y-depth plane)",
            "FRONT: aperture matches OPEN claim",
            "Survey JSON protrusion_gate agrees with pixels (trust pixels if conflict)",
        ],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (out / "README_HUMAN.txt").write_text(
        "\n".join(
            [
                "God Molecule human review package",
                f"status: {manifest['structural_status']}",
                "This is NOT creative_final.",
                "Inspect poses/ and aperture_survey.json.",
                "If pixels show protrusion, FAIL regardless of JSON.",
                "",
                *[f"- {c}" for c in manifest["human_checklist"]],
                "",
                *([f"ERROR: {e}" for e in errors] if errors else ["structural: ready for human review"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"PACKAGE={out}")
    print(f"STATUS={manifest['structural_status']}")
    if incomplete:
        print("HUMAN_REVIEW: STRUCTURAL_FAIL")
        for e in errors:
            print(" -", e)
        return 40
    print("HUMAN_REVIEW: READY_FOR_HUMAN")
    print("creative_final: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
