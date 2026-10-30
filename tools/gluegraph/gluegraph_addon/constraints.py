"""GlueGraph constraint network: breakable rigid-body bonds between pieces.

Impact-triggered release -- approach chosen (documented per SPEC H-1):
Blender's Bullet rigid-body constraints are natively breakable.  A
constraint with ``use_breaking = True`` is removed by the solver during
the step in which the impulse through it exceeds ``breaking_threshold``.
That mechanism works identically headless and in the viewport, needs no
per-frame Python, and bakes correctly with the point cache -- so it is
the primary release mechanism here.

The alternative (a ``frame_change_pre`` handler that watches piece
velocities and disables constraints by hand) was rejected: handlers do
not run reliably during headless point-cache bakes, they make the result
depend on Python being loaded when the file is reopened, and they
duplicate what Bullet already does.  The handler approach is only worth
revisiting if a shot needs *scripted* (non-physical) release timing; the
bake operator in ``__init__`` notes where it would hook in.

Strength model: for a neighbouring pair at centre distance ``d`` whose
bounding spheres first touch at ``touch = r_a + r_b``::

    gap      = max(0, d - touch)
    strength = glue_strength * material_factor * exp(-falloff * gap)
               * impact_scale

``glue_strength`` is the panel knob (Bullet breaking-threshold units,
impulse).  ``material_factor`` comes from the fracture material
profiles (default 1.0).  Pairs whose centres are farther apart than
``neighbour_factor * touch`` are not bonded at all -- Voronoi neighbours
tile the volume, so centre distance vs. bounding-sphere touch distance
is a reliable adjacency test for convex pieces.
"""

import math

import bpy

__all__ = ["setup_piece_rigid_body", "build_constraint_network",
           "pair_strength"]


def pair_strength(glue_strength, falloff, gap, material_factor=1.0):
    """Breaking threshold for one bond (see module docstring)."""
    return glue_strength * material_factor * math.exp(-falloff * max(0.0, gap))


def setup_piece_rigid_body(piece, mass_scale=1.0, friction=0.8):
    """Make ``piece`` an ACTIVE rigid body suited to a fractured part."""
    bpy.context.view_layer.objects.active = piece
    piece.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
    if piece.rigid_body is None:
        bpy.ops.rigidbody.object_add(type='ACTIVE')
    rb = piece.rigid_body
    rb.type = 'ACTIVE'
    # Voronoi / Cell Fracture pieces are convex, so CONVEX_HULL is exact
    # and much more stable than MESH for stacks.
    rb.collision_shape = 'CONVEX_HULL'
    vol = max(piece.dimensions.x * piece.dimensions.y * piece.dimensions.z,
              1e-4)
    rb.mass = max(0.05, vol * 10.0 * mass_scale)
    rb.friction = friction
    rb.restitution = 0.0
    rb.linear_damping = 0.05
    rb.angular_damping = 0.1
    rb.use_deactivation = False
    piece.select_set(False)
    return rb


def _material_factor(piece, material_profiles):
    if not material_profiles:
        return 1.0
    for slot in piece.data.materials:
        if slot and slot.name in material_profiles:
            return float(material_profiles[slot.name].get("strength", 1.0))
    if "*" in material_profiles:
        return float(material_profiles["*"].get("strength", 1.0))
    return 1.0


def _mass_scale(piece, material_profiles):
    if not material_profiles:
        return 1.0
    for slot in piece.data.materials:
        if slot and slot.name in material_profiles:
            return float(material_profiles[slot.name].get("mass_scale", 1.0))
    if "*" in material_profiles:
        return float(material_profiles["*"].get("mass_scale", 1.0))
    return 1.0


def build_constraint_network(pieces, glue_strength=20.0, falloff=1.5,
                             neighbour_factor=0.95, impact_threshold=1.0,
                             material_profiles=None, collection=None):
    """Create breakable FIXED constraints between neighbouring pieces.

    ``impact_threshold`` is a global multiplier on every bond's breaking
    threshold (the panel's impact knob: raise it and the same structure
    survives harder hits).  Returns ``(constraint_objects, bond_records)``
    where each record is ``{a, b, rest_distance, strength}`` -- the test
    harness uses the records to measure bond separation after a sim.
    """
    if collection is None:
        collection = bpy.context.collection
    for p in pieces:
        setup_piece_rigid_body(p, mass_scale=_mass_scale(p, material_profiles))

    bonds = []
    empties = []
    for i, a in enumerate(pieces):
        ra = max(a.dimensions.length / 2.0, 0.01)
        for b in pieces[i + 1:]:
            rb_ = max(b.dimensions.length / 2.0, 0.01)
            d = (a.location - b.location).length
            touch = ra + rb_
            if d >= neighbour_factor * touch:
                continue
            gap = d - touch
            factor = (_material_factor(a, material_profiles)
                      + _material_factor(b, material_profiles)) / 2.0
            strength = pair_strength(glue_strength, falloff, gap, factor)
            strength *= impact_threshold
            bpy.ops.object.empty_add(
                type='PLAIN_AXES', location=(a.location + b.location) / 2.0)
            empty = bpy.context.active_object
            empty.name = "Glue_%s_%s" % (a.name, b.name)
            bpy.ops.rigidbody.constraint_add(type='FIXED')
            con = empty.rigid_body_constraint
            con.object1 = a
            con.object2 = b
            con.use_breaking = True
            con.breaking_threshold = strength
            con.disable_collisions = True
            empties.append(empty)
            bonds.append({"a": a.name, "b": b.name, "rest_distance": d,
                          "strength": strength, "object": empty.name})
    return empties, bonds
