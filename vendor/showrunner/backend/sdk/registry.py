"""Vendored Showrunner asset-registry pattern.

Stable typed refs address assets; filenames are not production identity.
TRIPPEDD extends this pattern with content hashes, receipts and evidence.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .types import CastMemberRef, ClipRef, ImageRef, KeyframeRef, SetRef

@dataclass
class AssetRecord:
    id: str
    type: str
    location: str
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
    compatible_with: list[str] = field(default_factory=list)

class AssetRegistry:
    def __init__(self) -> None:
        self._records: dict[str, AssetRecord] = {}

    def register(self, record: AssetRecord) -> None:
        existing = self._records.get(record.id)
        if existing and record.version <= existing.version:
            record.version = existing.version + 1
        self._records[record.id] = record

    def remove(self, asset_id: str) -> None:
        self._records.pop(asset_id, None)

    def get(self, asset_id: str) -> AssetRecord | None:
        return self._records.get(asset_id)

    def resolve_image(self, ref: ImageRef) -> AssetRecord | None:
        return self.get(ref.id)

    def resolve_cast(self, ref: CastMemberRef) -> AssetRecord | None:
        return self.get(f"cast:{ref.id}")

    def resolve_set(self, ref: SetRef) -> AssetRecord | None:
        return self.get(f"set:{ref.id}")

    def resolve_keyframe(self, ref: KeyframeRef) -> AssetRecord | None:
        return self.get(f"keyframe:{ref.id}")

    def resolve_clip(self, ref: ClipRef) -> AssetRecord | None:
        return self.get(f"clip:{ref.id}")

    def by_type(self, asset_type: str) -> list[AssetRecord]:
        return [r for r in self._records.values() if r.type == asset_type]

    def all(self) -> list[AssetRecord]:
        return list(self._records.values())
