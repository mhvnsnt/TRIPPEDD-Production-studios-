"""Fail-closed preflight for MARS mouth cutters.

The worker may implement the actual Blender/CGAL operation. This module
encodes the measurements that must be known before a boolean is attempted.
It deliberately accepts measured world-space quantities rather than trusting
linked-library object transforms.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BooleanPreflight:
    cutter_thickness_mm: float
    overlap_depth_mm: float
    intersection_volume_mm3: float
    cutter_is_closed: bool

    def passes(self, *, min_thickness_mm: float = 0.5,
               min_overlap_depth_mm: float = 0.1) -> bool:
        return (
            self.cutter_is_closed
            and self.cutter_thickness_mm >= min_thickness_mm
            and self.overlap_depth_mm >= min_overlap_depth_mm
            and self.intersection_volume_mm3 > 0.0
        )

def assembly_policy(*, owner_override: bool = False,
                    competing_whole_character: bool = False) -> bool:
    """Permanent character separation is denied unless explicitly authorized."""
    return owner_override or not competing_whole_character
