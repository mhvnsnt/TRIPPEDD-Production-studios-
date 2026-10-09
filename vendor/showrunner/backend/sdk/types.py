"""Vendored from Showrunner: typed production artifacts.

TRIPPEDD adoption note: these contracts are the reference model for typed
handoffs. TRIPPEDD extends them with world refs, render receipts, physical
QC and evidence artifacts. Upstream: divi-vijayakumar/Showrunner.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Generic, Literal, Protocol, TypeVar, runtime_checkable

@dataclass(frozen=True)
class ImageRef: id: str
@dataclass(frozen=True)
class CastMemberRef: id: str
@dataclass(frozen=True)
class SetRef: id: str
@dataclass(frozen=True)
class KeyframeRef: id: str
@dataclass(frozen=True)
class ClipRef: id: str

AspectRatio = Literal["9:16", "16:9", "1:1", "4:5"]
RenderStyle = Literal["photoreal", "stylized_3d_pixar_adjacent", "anime", "watercolor"]

@dataclass(frozen=True)
class Resolution:
    width: int
    height: int

@dataclass(frozen=True)
class VoiceConfig:
    gender: str = ""
    pace: float = 1.0
    warmth: str = ""
    accent_hint: str = ""
    energy: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class CameraSpec:
    motion: str = "static"
    focus_on: CastMemberRef | None = None

@dataclass(frozen=True)
class CompositionSpec:
    framing: str = "medium_close_up"
    cast_visible: tuple[CastMemberRef, ...] = ()

@dataclass(frozen=True)
class LightingSpec:
    key_position: str = "camera_left"
    key_temperature: str = "neutral"
    contrast: str = "medium"

@runtime_checkable
class CastMember(Protocol):
    id: str
    name: str
    character_sheet: ImageRef
    voice: VoiceConfig

@runtime_checkable
class Cast(Protocol):
    members: list[CastMember]
    anchor_sheet: ImageRef

@runtime_checkable
class Set(Protocol):
    id: str
    master_image: ImageRef
    lighting: LightingSpec
    style: RenderStyle

@runtime_checkable
class SetLibrary(Protocol):
    sets: dict[str, Set]

P = TypeVar("P")

@dataclass
class Scene(Generic[P]):
    id: str
    show_id: str
    duration_seconds: int
    aspect_ratio: AspectRatio
    resolution: Resolution
    cast: list[CastMemberRef]
    set: SetRef
    start_keyframe: KeyframeRef | None
    end_keyframe: KeyframeRef | None
    camera: CameraSpec
    composition: CompositionSpec
    payload: P

@dataclass
class ShotPlan:
    scene_id: str
    scene_number: int | str
    speaker: CastMemberRef | None
    start_image_url: str | None
    end_image_url: str | None = None
    motion: str = "static"
    framing: str = "medium_close_up"
    mode_tag: str = "i2v-avatar"
    prompt: str = ""
    spoken_line: str = ""
    duration_seconds: int = 5
    aspect_ratio: AspectRatio = "9:16"
    seed: int = 0
    notes: str = ""

@dataclass
class Keyframe:
    ref: KeyframeRef
    image: ImageRef
    scene_id: str
    position: Literal["start", "end"]

@dataclass
class Clip:
    ref: ClipRef
    scene_id: str
    duration_seconds: float
    video_url: str | None
    local_path: str | None
    cost_usd: float = 0.0

@dataclass
class ContinuityReport:
    scene_id: str
    checks: dict[str, bool]
    notes: dict[str, str] = field(default_factory=dict)
    passed: bool = True
