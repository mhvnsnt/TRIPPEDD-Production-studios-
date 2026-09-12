#!/usr/bin/env python3
"""Prepare or submit a proven first-shot render to OpenCue.

OpenCue is deliberately downstream of local proof. This adapter refuses to
schedule a render unless the Blender worker receipt says the exact .blend and
PNG bytes were rendered and hashed. It never changes visual/physical QC and
never treats queue submission as production approval.

Without --submit, the tool only emits a deterministic PyOutline-compatible
job description. With --submit it requires the OpenCue PyOutline client and a
shared filesystem path for the resolved .blend.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SHOT_ID = "GM-WORLD-0001-FIRST-SHOT"
EXPECTED_WORLD = "GM-WORLD-0001"
EXPECTED_SEED = 742918


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_receipt(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("rendered") is not True:
        raise RuntimeError("dispatch blocked: receipt is not a proven render")
    if data.get("shot_id") != SHOT_ID:
        raise RuntimeError("dispatch blocked: unexpected shot_id")
    if data.get("world_id") != EXPECTED_WORLD:
        raise RuntimeError("dispatch blocked: unexpected world_id")
    artifact = data.get("artifact") or {}
    source = data.get("source_scene") or {}
    if artifact.get("format") != "png" or not artifact.get("sha256"):
        raise RuntimeError("dispatch blocked: receipt has no exact PNG hash")
    if not source.get("sha256") or not source.get("path"):
        raise RuntimeError("dispatch blocked: receipt has no source-scene hash/path")
    if data.get("visual_qc") not in {"NOT_EVALUATED", "NOT_ATTEMPTED"}:
        raise RuntimeError("dispatch blocked: unexpected visual QC state")
    if data.get("physical_qc") not in {"NOT_EVALUATED", "NOT_ATTEMPTED"}:
        raise RuntimeError("dispatch blocked: unexpected physical QC state")
    return data


def resolve_source(receipt_path: Path, receipt: dict, shared_root: Path | None) -> Path:
    raw = Path(receipt["source_scene"]["path"])
    candidates = [raw]
    if not raw.is_absolute():
        candidates.append(receipt_path.parent / raw)
    if shared_root:
        candidates.append(shared_root / raw.name)
        candidates.append(shared_root / raw)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise RuntimeError("dispatch blocked: resolved .blend is not present on this worker")


def verify_source(blend: Path, expected_sha: str) -> None:
    actual = sha256_file(blend)
    if actual != expected_sha:
        raise RuntimeError(f"dispatch blocked: .blend SHA-256 mismatch expected={expected_sha} actual={actual}")


def build_job(receipt: dict, blend: Path, output_root: str) -> dict:
    frame = int(receipt.get("frame", 1))
    return {
        "schema": "trippedd.opencue-dispatch/v1",
        "status": "READY_FOR_OPENCUE_SUBMISSION",
        "dispatch_authority": "OpenCue",
        "production_authority": "TRIPPEDD_RENDER_EVIDENCE",
        "shot_id": SHOT_ID,
        "world_id": EXPECTED_WORLD,
        "world_seed": EXPECTED_SEED,
        "frame_range": f"{frame}-{frame}",
        "blend": str(blend),
        "command": ["blender", "-b", str(blend), "-o", f"{output_root}/{SHOT_ID}.#####", "-F", "PNG", "-f", "#IFRAME#"],
        "source_scene_sha256": receipt["source_scene"]["sha256"],
        "proven_render_png_sha256": receipt["artifact"]["sha256"],
        "visual_qc": "NOT_EVALUATED",
        "physical_qc": "NOT_EVALUATED",
        "gate": "BLOCKED_UNTIL_QC",
        "policy": {
            "opencue_is_dispatcher_not_source_of_truth": True,
            "local_proof_required_before_submission": True,
            "queue_success_is_not_qc": True,
            "proxy_never_canonical": True,
        },
    }


def submit_with_pyoutline(job_spec: dict, show: str, user: str) -> None:
    try:
        import outline
        import outline.modules.shell
    except ImportError as exc:
        raise RuntimeError("--submit requires OpenCue PyOutline (opencue-pyoutline)") from exc

    frame_range = job_spec["frame_range"]
    layer = outline.modules.shell.Shell(name="first-shot-render", command=job_spec["command"], range=frame_range)
    layer.set_service("blender")
    job = outline.Outline(name="trippedd-first-shot-v1", shot=SHOT_ID, show=show, user=user)
    job.set_frame_range(frame_range)
    job.add_layer(layer)
    outline.cuerun.launch(job, use_pycuerun=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--shared-root", type=Path, default=None)
    parser.add_argument("--output-root", default="/shared/renders/first-shot")
    parser.add_argument("--job-json", type=Path, default=None)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--show", default="trippedd")
    parser.add_argument("--user", default="trippedd")
    args = parser.parse_args()

    try:
        receipt_path = args.receipt.resolve()
        receipt = load_receipt(receipt_path)
        blend = resolve_source(receipt_path, receipt, args.shared_root.resolve() if args.shared_root else None)
        verify_source(blend, receipt["source_scene"]["sha256"])
        spec = build_job(receipt, blend, args.output_root)
        out = args.job_json or receipt_path.with_name("opencue_dispatch.json")
        out.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        print(f"OPENCUE_DISPATCH: READY {out}")
        print(f"SOURCE_BLEND_SHA256: {spec['source_scene_sha256']}")
        print(f"PROVEN_RENDER_SHA256: {spec['proven_render_png_sha256']}")
        print("PRODUCTION_GATE: BLOCKED_UNTIL_QC")
        if args.submit:
            submit_with_pyoutline(spec, args.show, args.user)
            print("OPENCUE_SUBMISSION: ACCEPTED_BY_CLIENT")
        else:
            print("OPENCUE_SUBMISSION: NOT_ATTEMPTED")
        return 0
    except Exception as exc:
        print("OPENCUE_DISPATCH: BLOCKED")
        print(exc)
        return 40


if __name__ == "__main__":
    raise SystemExit(main())
