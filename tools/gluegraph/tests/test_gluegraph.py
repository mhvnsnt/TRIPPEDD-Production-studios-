"""GlueGraph headless proof test (SPEC H-1).

Run (box discipline: one heavy sim at a time, RAM gate in the wrapper):

    flock /tmp/heavy-test.lock bash -c \
      'xvfb-run -a env -u PYTHONPATH <blender> -b --factory-startup \
       --python tools/gluegraph/tests/test_gluegraph.py'

What it proves, with measured numbers (printed as one GLUEGRAPH_RESULT
JSON line):

1. Fracture: one box wall -> N pieces via fracture_core (Cell Fracture
   donor if available, else the Voronoi/bisect fallback; method printed).
2. Stand phase (frames 1-30, no projectile): the glued structure holds --
   max piece displacement and count of pieces displaced > 0.15 m.
3. Impact phase: a heavy sphere is driven kinematically along +Y
   through the wall (frames 30-55; releasing a keyframed kinematic body
   to dynamic was measured not to transfer velocity on 4.5.3, so the
   impactor stays kinematic -- contact impulse is still physical), sim
   runs to frame 65.
4. Break measurement: bpy exposes no per-constraint "broken" flag, so
   breakage is measured geometrically from the bond records -- a bond
   counts as separated when its pieces' centre distance exceeds
   rest_distance * 1.5 + 0.25 m -- plus pieces displaced > 0.3 m.

Exit code 0 only if the structure both stood AND broke (stand displaced
count == 0 and at least 3 bonds separated and at least 3 pieces displaced
after impact); otherwise 2, and the numbers say why.
"""

import json
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ADDON_DIR = os.path.join(HERE, "..", "gluegraph_addon")
sys.path.insert(0, os.path.abspath(ADDON_DIR))

import constraints as gg_constraints  # noqa: E402
import fracture_core as gg_fracture  # noqa: E402

GLUE_STRENGTH = 20.0
FALLOFF = 1.5
PIECES = 12
STAND_FRAME = 30
END_FRAME = 65


def main():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = END_FRAME
    bpy.ops.rigidbody.world_add()
    scene.rigidbody_world.substeps_per_frame = 10

    # Target: a small wall (3.0 x 0.6 x 2.0 m), base on the ground plane.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.0))
    wall = bpy.context.active_object
    wall.name = "GlueWall"
    wall.scale = (3.0, 0.6, 2.0)
    bpy.ops.object.transform_apply(scale=True)

    pieces, method = gg_fracture.fracture_object(
        wall, piece_count=PIECES, seed=7)
    bpy.data.objects.remove(wall, do_unlink=True)

    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Ground"
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    ground.rigid_body.collision_shape = 'BOX'
    ground.rigid_body.friction = 0.9

    _empties, bonds = gg_constraints.build_constraint_network(
        pieces, glue_strength=GLUE_STRENGTH, falloff=FALLOFF,
        impact_threshold=1.0)

    # Projectile: heavy sphere driven kinematically along +Y (the wall is
    # thin in Y) straight through the wall.  Measured on 4.5.3: releasing
    # a keyframed kinematic body to dynamic does NOT transfer its
    # keyframe velocity (it dropped straight down, ending at rest in
    # front of the wall), so the impactor stays kinematic for the whole
    # pass -- contact impulse on the pieces is still fully physical, and
    # the bonds, not the projectile, decide what breaks.
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45, location=(0, -4.0, 1.0))
    proj = bpy.context.active_object
    proj.name = "Projectile"
    bpy.ops.rigidbody.object_add(type='ACTIVE')
    proj.rigid_body.mass = 8.0
    proj.rigid_body.collision_shape = 'SPHERE'
    proj.rigid_body.kinematic = True
    scene.frame_set(STAND_FRAME)
    proj.location = (0, -4.0, 1.0)
    proj.keyframe_insert('location', frame=STAND_FRAME)
    scene.frame_set(55)
    proj.location = (0, 3.0, 1.0)
    proj.keyframe_insert('location', frame=55)

    # The frame_set() calls above (keyframing the projectile) pollute the
    # rigid-body point cache; free it so the measured run steps fresh.
    bpy.ops.ptcache.free_bake_all()
    scene.frame_set(1)

    # Headless rigid-body stepping (measured on Blender 4.5.3): jumping
    # frame_set(1) -> frame_set(30) does NOT step Bullet -- a free cube
    # stayed at its start height.  Stepping sequentially through every
    # frame (or baking the point cache) does.  This harness steps.
    def run_to(frame):
        snap = None
        for f in range(1, frame + 1):
            scene.frame_set(f)
            if f in (1, STAND_FRAME, END_FRAME):
                bpy.context.view_layer.update()
                if f == frame:
                    snap = {p.name: p.matrix_world.translation.copy()
                            for p in pieces}
        return snap

    start = run_to(1)
    stand = run_to(STAND_FRAME)
    stand_disp = {k: (v - start[k]).length for k, v in stand.items()}
    after = run_to(END_FRAME)
    after_disp = {k: (v - start[k]).length for k, v in after.items()}
    proj_end = proj.matrix_world.translation.copy()

    separated = 0
    for bond in bonds:
        d1 = (after[bond["a"]] - after[bond["b"]]).length
        if d1 > bond["rest_distance"] * 1.5 + 0.25:
            separated += 1

    result = {
        "blender": bpy.app.version_string,
        "fracture_method": method,
        "pieces": len(pieces),
        "constraints": len(bonds),
        "glue_strength": GLUE_STRENGTH,
        "stand_frame": STAND_FRAME,
        "stand_max_displacement_m": round(max(stand_disp.values()), 4),
        "stand_displaced_gt_0.15m": sum(
            1 for v in stand_disp.values() if v > 0.15),
        "end_frame": END_FRAME,
        "after_max_displacement_m": round(max(after_disp.values()), 4),
        "after_displaced_gt_0.3m": sum(
            1 for v in after_disp.values() if v > 0.3),
        "after_displaced_gt_0.15m": sum(
            1 for v in after_disp.values() if v > 0.15),
        "bonds_separated_after_impact": separated,
        "projectile_end_location": [round(v, 3) for v in proj_end],
    }
    print("GLUEGRAPH_RESULT " + json.dumps(result))

    stood = result["stand_displaced_gt_0.15m"] == 0
    broke = separated >= 3 and result["after_displaced_gt_0.3m"] >= 3
    print("GLUEGRAPH_VERDICT stood=%s broke=%s" % (stood, broke))
    sys.exit(0 if (stood and broke) else 2)


main()
