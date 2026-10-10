"""Definitions for topology-quality receipts.

This module deliberately contains no mesh mutation. A separate worker may use
PyMeshLab, CGAL, Instant Meshes, Open3D, or Blender to produce candidates.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TriangleQualityGate:
    minimum_angle_deg: float = 15.0
    maximum_sliver_fraction: float = 0.05


@dataclass(frozen=True)
class ProtectedAnatomyGate:
    max_curve_deviation_mm: float = 0.5


def candidate_is_better(
    *,
    source_min_angle_deg: float,
    candidate_min_angle_deg: float,
    source_sliver_fraction: float,
    candidate_sliver_fraction: float,
    source_self_intersections: int,
    candidate_self_intersections: int,
    protected_curve_deviation_mm: float,
    gate: TriangleQualityGate = TriangleQualityGate(),
    anatomy: ProtectedAnatomyGate = ProtectedAnatomyGate(),
) -> bool:
    """Fail closed unless topology improves and protected anatomy remains valid."""
    if candidate_self_intersections != 0:
        return False
    if protected_curve_deviation_mm > anatomy.max_curve_deviation_mm:
        return False
    improved = (
        candidate_min_angle_deg > source_min_angle_deg
        and candidate_sliver_fraction < source_sliver_fraction
    )
    passes_floor = candidate_min_angle_deg >= gate.minimum_angle_deg
    passes_slivers = candidate_sliver_fraction <= gate.maximum_sliver_fraction
    return improved and passes_floor and passes_slivers
