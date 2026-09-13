"""Immutable-reference annotation contract.

The contract has no image-generation path: annotations are data layered over
the exact source pixels.
"""

from dataclasses import dataclass, asdict
from hashlib import sha256
from pathlib import Path
import json

PALETTE = {
    "eye_aperture": "#00FF00",
    "eyeball_optic": "#FF00FF",
    "eyebrow": "#FFFF00",
    "nose_nostril": "#FF0000",
    "mouth": "#FF8000",
    "tongue": "#FF1493",
    "hair_root": "#FFFFFF",
    "hair_lock": "#00FFFF",
    "hair_motion": "#FFD700",
    "collision": "#FF4500",
    "anatomical_reference": "#0080FF",
}

@dataclass(frozen=True)
class Annotation:
    region_id: str
    semantic_type: str
    points: list[tuple[float, float]]
    confidence: float | None = None
    source: str = "unknown"

def sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def write_manifest(reference: Path, annotations: list[Annotation], out: Path) -> None:
    payload = {
        "schema": "tripped.annotation_overlay.v1",
        "reference": {"path": str(reference), "sha256": sha256_file(reference)},
        "palette": PALETTE,
        "annotations": [asdict(a) for a in annotations],
        "immutable_reference": True,
        "replacement_image": False,
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
