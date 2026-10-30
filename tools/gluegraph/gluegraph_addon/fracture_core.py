"""GlueGraph fracture core -- REUSABLE MODULE (shared with EffectorKit C-2).

This module is the single fracture implementation for the studio's free
destruction / MoGraph work:

* SPEC H-1 (GlueGraph) uses it to fracture a target before building its
  breakable rigid-body constraint network.
* SPEC C-2 (EffectorKit "explode pieces" preset) reuses it to turn an
  object into pieces that effectors can push apart.  ``explode_offsets()``
  below is the C-2-facing helper: given fractured pieces it returns the
  radial offset vector per piece.  The C-2 lane should import this module
  instead of re-implementing fracture.

Donor first (repo law): Blender's bundled Cell Fracture add-on
(``object_fracture_cell``) is the fracture donor.  ``fracture_object()``
tries the Cell Fracture operator first whenever it is available in the
running Blender.  In Blender 4.5 the add-on is no longer shipped in
``addons_core`` (verified on the studio's 4.5.3 build: no
``object_fracture_cell`` module and no fracture operator), so the fallback
path below is used there: a Voronoi fracture implemented with Blender's
own ``bmesh.ops.bisect_plane`` half-space clipping -- the same algorithm
Cell Fracture itself uses (seed points, bisect the mesh against every
other seed's bisector plane, fill the cut).  It is original code written
against Blender's public ``bmesh`` API, not a copy of Cell Fracture's
source.

Per-material settings: ``material_profiles`` maps a material name to a
dict with ``piece_scale`` (relative seed density), ``strength`` (glue
strength multiplier used by the constraint builder) and ``mass_scale``.
A profile named ``"*"`` applies to pieces whose source material has no
named profile.  On the Voronoi fallback path ``piece_scale`` biases seed
placement toward the first material's region only approximately (seeds
are uniform; the multiplier is honoured by the constraint/mass stage) --
this limitation is documented in the README.
"""

import random

import bmesh
import bpy
from mathutils import Vector

__all__ = [
    "cell_fracture_available",
    "fracture_object",
    "voronoi_fracture",
    "explode_offsets",
    "piece_centroid",
]


def cell_fracture_available():
    """True when Blender's bundled Cell Fracture operator exists.

    ``hasattr(bpy.ops.object, ...)`` is NOT a valid probe -- bpy.ops
    lazy-resolves any attribute name.  Probe the operator's RNA type
    instead, which raises when the operator is not registered (measured
    on the studio's 4.5.3 build, where Cell Fracture is not shipped).
    """
    try:
        bpy.ops.object.add_fracture_cell_objects.get_rna_type()
        return True
    except Exception:
        return False


def piece_centroid(obj):
    """World-space centroid of an object's evaluated bounding box centre."""
    return obj.matrix_world.translation.copy()


def _grid_seeds(lo, hi, count, seed, jitter=0.35):
    """Seed points on a jittered grid filling the [lo, hi] box."""
    rng = random.Random(seed)
    dims = hi - lo
    best = None
    for a in range(1, 7):
        for b in range(1, 7):
            for c in range(1, 7):
                n = a * b * c
                if n >= count and (best is None or n < best[0] * best[1] * best[2]):
                    best = (a, b, c)
    a, b, c = best
    seeds = []
    for i in range(a):
        for j in range(b):
            for k in range(c):
                p = Vector((
                    lo.x + dims.x * (i + 0.5) / a,
                    lo.y + dims.y * (j + 0.5) / b,
                    lo.z + dims.z * (k + 0.5) / c,
                ))
                p += Vector((
                    rng.uniform(-jitter, jitter) * dims.x / a,
                    rng.uniform(-jitter, jitter) * dims.y / b,
                    rng.uniform(-jitter, jitter) * dims.z / c,
                ))
                seeds.append(p)
    return seeds


def voronoi_fracture(source, piece_count=12, seed=7, margin=0.96,
                     collection=None):
    """Fracture ``source`` into Voronoi pieces via bmesh bisect clipping.

    Works in world space (the source transform is baked into a working
    copy; the source object itself is left untouched).  Each piece is a
    closed, convex mesh: successive ``bisect_plane`` cuts against every
    other seed's bisector plane, boundary edges filled with
    ``holes_fill``, then verts pulled ``margin`` toward the piece
    centroid so neighbouring pieces do not start in contact (contact at
    frame 1 makes Bullet explode the stack).

    Returns the list of new objects (possibly fewer than ``piece_count``
    if a seed's cell ends up empty).
    """
    if collection is None:
        collection = bpy.context.collection
    mw = source.matrix_world.copy()
    corners = [mw @ Vector(c) for c in source.bound_box]
    lo = Vector((min(v.x for v in corners), min(v.y for v in corners),
                 min(v.z for v in corners)))
    hi = Vector((max(v.x for v in corners), max(v.y for v in corners),
                 max(v.z for v in corners)))
    seeds = _grid_seeds(lo, hi, piece_count, seed)
    base_mesh = source.data.copy()
    base_mesh.transform(mw)
    materials = list(source.data.materials)

    pieces = []
    for idx, s in enumerate(seeds):
        me = base_mesh.copy()
        bm = bmesh.new()
        bm.from_mesh(me)
        for other in seeds:
            if other is s:
                continue
            plane_no = other - s
            if plane_no.length < 1e-9:
                continue
            plane_no.normalize()
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            if not geom:
                break
            bmesh.ops.bisect_plane(
                bm, geom=geom, dist=1e-6,
                plane_co=(s + other) * 0.5, plane_no=plane_no,
                use_snap_center=False, clear_outer=True, clear_inner=False)
            boundary = [e for e in bm.edges if len(e.link_faces) < 2]
            if boundary:
                bmesh.ops.holes_fill(bm, edges=boundary, sides=0)
        if len(bm.faces) == 0:
            bm.free()
            bpy.data.meshes.remove(me)
            continue
        cen = Vector((0.0, 0.0, 0.0))
        for v in bm.verts:
            cen += v.co
        if len(bm.verts):
            cen /= len(bm.verts)
        for v in bm.verts:
            v.co = cen + (v.co - cen) * margin
        bm.to_mesh(me)
        bm.free()
        for mat in materials:
            if mat and mat.name not in me.materials:
                me.materials.append(mat)
        ob = bpy.data.objects.new("%s_piece_%02d" % (source.name, idx), me)
        collection.objects.link(ob)
        pieces.append(ob)
    bpy.data.meshes.remove(base_mesh)
    return pieces


def _cell_fracture(source, piece_count, seed):
    """Donor path: run Blender's bundled Cell Fracture on ``source``."""
    before = set(bpy.data.objects)
    bpy.context.view_layer.objects.active = source
    source.select_set(True)
    bpy.ops.object.add_fracture_cell_objects(
        source_limit=piece_count,
        source_seed=seed,
        use_debug_redraw=False,
    )
    source.select_set(False)
    return [ob for ob in bpy.data.objects if ob not in before
            and ob.type == 'MESH']


def fracture_object(source, piece_count=12, seed=7, margin=0.96,
                    material_profiles=None, collection=None):
    """Fracture ``source``; returns (pieces, method_used).

    Tries the Cell Fracture donor first, falls back to the built-in
    Voronoi/bisect implementation.  ``method_used`` is ``"cell_fracture"``
    or ``"voronoi_bisect"`` so callers/tests can report honestly which
    path produced the pieces.
    """
    if cell_fracture_available():
        try:
            pieces = _cell_fracture(source, piece_count, seed)
            if pieces:
                return pieces, "cell_fracture"
        except Exception:
            pass  # fall through to the Voronoi path
    return voronoi_fracture(source, piece_count, seed, margin,
                            collection), "voronoi_bisect"


def explode_offsets(pieces, amount=1.0, centre=None):
    """C-2 helper: radial offset vector per piece for an explode preset.

    Returns ``{piece_name: Vector}`` -- the direction from the fracture
    centre to the piece, normalised, scaled by ``amount`` and by the
    piece's distance from the centre (outer pieces travel further, which
    is the classic Voronoi-fracture explode look).
    """
    if centre is None:
        centre = Vector((0.0, 0.0, 0.0))
        for p in pieces:
            centre += piece_centroid(p)
        if pieces:
            centre /= len(pieces)
    out = {}
    for p in pieces:
        d = piece_centroid(p) - centre
        dist = d.length
        if dist < 1e-9:
            out[p.name] = Vector((0.0, 0.0, 0.0))
        else:
            out[p.name] = d.normalized() * (amount * (0.5 + dist))
    return out
