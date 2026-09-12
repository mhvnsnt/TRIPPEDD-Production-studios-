"""Vendored Showrunner agent protocols.

Agents consume and emit typed artifacts and receive the asset registry
explicitly. TRIPPEDD keeps the same boundary and adds compiler, render,
physical-QC and evidence gates around execution.
"""
from __future__ import annotations
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable
from ..registry import AssetRegistry
from ..types import Cast, Clip, ContinuityReport, Keyframe, Scene, SetLibrary, ShotPlan
P = TypeVar("P")

@runtime_checkable
class ResearchAgent(Protocol):
    async def run(self, *, premise: str, goal: str, context: dict[str, Any]) -> dict[str, Any]: ...

@runtime_checkable
class StructureAgent(Protocol):
    async def run(self, *, premise: str, research: dict[str, Any]) -> dict[str, Any]: ...

@runtime_checkable
class ScriptAgent(Protocol, Generic[P]):
    async def run(self, *, beats: dict[str, Any], research: dict[str, Any]) -> list[Scene[P]]: ...

@runtime_checkable
class CastingAgent(Protocol):
    async def run(self, *, registry: AssetRegistry, **kwargs: Any) -> Cast: ...

@runtime_checkable
class SetAgent(Protocol):
    async def run(self, *, registry: AssetRegistry, **kwargs: Any) -> SetLibrary: ...

@runtime_checkable
class DirectorAgent(Protocol, Generic[P]):
    async def run(self, *, scene: Scene[P], registry: AssetRegistry) -> ShotPlan: ...

@runtime_checkable
class StoryboardAgent(Protocol, Generic[P]):
    async def run(self, *, scene: Scene[P], plan: ShotPlan, registry: AssetRegistry, position: str) -> Keyframe: ...

@runtime_checkable
class ContinuityAgent(Protocol, Generic[P]):
    async def run(self, *, scene: Scene[P], registry: AssetRegistry) -> ContinuityReport: ...

@runtime_checkable
class AnimatorAgent(Protocol, Generic[P]):
    async def run(self, *, scene: Scene[P], plan: ShotPlan, start: Keyframe, end: Keyframe | None, registry: AssetRegistry) -> Clip: ...

@runtime_checkable
class EditorAgent(Protocol, Generic[P]):
    async def run(self, *, scenes: list[Scene[P]], clips: list[Clip], registry: AssetRegistry, timeline_extras: dict[str, Any] | None = None) -> dict[str, Any]: ...
