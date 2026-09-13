#!/usr/bin/env python3
"""Blender-side MARS oral repair.

The canonical MARS skin is an identity surface, not a generic jaw-open clay
surface. The oral donor supplies the cavity and internal anatomy; its measured
GNM jaw-open delta is applied to donor anatomy only. A previous implementation
added a radial, world-space ``jaw_open`` displacement directly to every MARS
skin vertex inside an ellipse. That produced exactly the failure this contract
is intended to prevent: skin stretched across the oral cavity while teeth,
gums, and tongue were also moving.

Inputs:
  --donor-npz   output of build_gnm_oral_donor.py
  --mouth-frame measured Mars mouth frame JSON
  --output      repaired .blend

Placement law (fail-closed):
  All oral donor geometry must sit BEHIND the measured lip plane.
  The canonical MARS surface is never given a synthetic radial jaw deformation.
  GNM mouth-open motion belongs to the GNM anatomical donor components.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector, Matrix

DEFAULT_RECESS = 0.008
PROTRUSION_TOLERANCE = 1e-4


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--donor-npz", required=True)
    ap.add_argument("--mouth-frame", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--render-dir", default="")
    ap.add_argument("--recess", type=float, default=DEFAULT_RECESS)
    return ap.parse_args(argv)


def require_mesh():
    named = bpy.data.objects.get("MARS_CANONICAL")
    if named and named.type == "MESH":
        return named
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        raise RuntimeError("MARS_ORAL_BRIDGE: FAIL — no mesh in source blend")
    return max(meshes, key=lambda o: len(o.data.vertices))


def collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in [x.name for x in bpy.context.scene.collection.children]:
        bpy.context.scene.collection.children.link(c)
    return c


def unlink_all(obj):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)


def make_mesh(name, verts, faces, parent):
    me = bpy.data.meshes.new(name + "_MESH")
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    ob = bpy.data.objects.new(name, me)
    parent.objects.link(ob)
    return ob


def submesh(verts, faces, mask):
    face_mask = np.all(mask[np.asarray(faces, dtype=np.int32)], axis=1)
    selected = np.asarray(faces, dtype=np.int32)[face_mask]
    if len(selected) == 0:
        raise RuntimeError("MARS_ORAL_BRIDGE: empty anatomical submesh")
    used = np.unique(selected)
    remap = np.full(len(verts), -1, dtype=np.int32)
    remap[used] = np.arange(len(used), dtype=np.int32)
    return verts[used], remap[selected], used


def add_shape(ob, name, delta_by_vertex):
    if not ob.data.shape_keys:
        ob.shape_key_add(name="Basis")
    key = ob.shape_key_add(name=name)
    for i, delta in enumerate(delta_by_vertex):
        key.data[i].co = ob.data.vertices[i].co + Vector(delta)
    return key


def world_vertices(ob):
    return np.asarray([ob.matrix_world @ v.co for v in ob.data.vertices], dtype=np.float64)


def find_front_surface(mars, center):
    pts = world_vertices(mars)
    dxz = np.linalg.norm(pts[:, [0, 2]] - np.asarray(center)[[0, 2]], axis=1)
    radius = max(float(np.ptp(pts[:, 0])) * 0.08, 1e-3)
    near = pts[dxz <= radius]
    if len(near) < 20:
        near = pts[np.argsort(dxz)[: min(200, len(pts))]]
    return float(np.percentile(near[:, 1], 95.0))


def lip_plane(frame, mars):
    center = np.asarray(frame["center"], dtype=np.float64)
    if "outward_normal" in frame:
        n = np.asarray(frame["outward_normal"], dtype=np.float64)
        n = n / max(np.linalg.norm(n), 1e-12)
        return center, n
    plane_y = float(frame.get("plane_y", frame.get("front_surface_y", find_front_surface(mars, center))))
    point = np.array([center[0], plane_y, center[2]], dtype=np.float64)
    return point, np.array([0.0, 1.0, 0.0], dtype=np.float64)


def signed_distances(pts, plane_point, plane_normal):
    return (pts - plane_point) @ plane_normal


def protrusion_mm(ob, plane_point, plane_normal):
    pts = world_vertices(ob)
    if len(pts) == 0:
        return 0.0
    return float(np.max(signed_distances(pts, plane_point, plane_normal)))


def recess_object_behind_plane(ob, plane_point, plane_normal, recess):
    pts = world_vertices(ob)
    d = signed_distances(pts, plane_point, plane_normal)
    front = float(np.percentile(d, 95.0))
    target_front = -abs(recess)
    if front <= target_front:
        return 0.0, front
    shift = Vector(((-plane_normal) * (front - target_front)).tolist())
    ob.matrix_world.translation += shift
    pts2 = world_vertices(ob)
    d2 = signed_distances(pts2, plane_point, plane_normal)
    return float(front - target_front), float(np.percentile(d2, 95.0))


def assert_no_protrusion(objects, plane_point, plane_normal, label="oral donor"):
    worst_name = None
    worst = -1e9
    report = {}
    for name, ob in objects.items():
        p = protrusion_mm(ob, plane_point, plane_normal)
        report[name] = p
        if p > worst:
            worst = p
            worst_name = name
    if worst > PROTRUSION_TOLERANCE:
        detail = ", ".join(f"{k}={v:.6f}" for k, v in report.items())
        raise RuntimeError(
            f"MARS_ORAL_BRIDGE: PROTRUSION_FAIL — {label} crosses lip plane "
            f"(worst={worst_name} protrusion={worst:.6f}; {detail})."
        )
    return report


def fit_transform(sock_verts, frame):
    center = np.asarray(frame["center"], dtype=np.float64)
    left = np.asarray(frame["left_corner"], dtype=np.float64)
    right = np.asarray(frame["right_corner"], dtype=np.float64)
    target_width = float(np.linalg.norm(left - right))
    if target_width <= 0:
        raise RuntimeError("MARS_ORAL_BRIDGE: invalid measured mouth width")
    lo = sock_verts.min(axis=0)
    hi = sock_verts.max(axis=0)
    donor_width = max(float(hi[0] - lo[0]), 1e-8)
    scale = target_width / donor_width
    roll = math.radians(float(frame.get("roll_degrees", 0.0)))
    rot = Matrix.Rotation(roll, 4, "Z")
    donor_center = (lo + hi) * 0.5
    scaled_center = Vector((donor_center * scale).tolist())
    trans = Vector(center.tolist()) - (rot @ scaled_center)
    mat = Matrix.Translation(trans) @ rot @ Matrix.Diagonal((scale, scale, scale, 1.0))
    return mat, scale


def solidify_cutter_inward(sock, thickness=0.012):
    bpy.context.view_layer.objects.active = sock
    sock.select_set(True)
    mod = sock.modifiers.new("ORAL_SOCK_SOLIDIFY", "SOLIDIFY")
    mod.thickness = thickness
    mod.offset = -1.0
    bpy.ops.object.modifier_apply(modifier=mod.name)
    sock.select_set(False)


def boolean_cavity(mars, cutter):
    bpy.context.view_layer.objects.active = mars
    mod = mars.modifiers.new("MARS_ORAL_CAVITY_BOOLEAN", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "EXACT"
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    if len(mars.data.vertices) == 0:
        raise RuntimeError("MARS_ORAL_BRIDGE: boolean destroyed Mars mesh")


def main():
    a = args()
    donor_path = Path(a.donor_npz).resolve()
    frame_path = Path(a.mouth_frame).resolve()
    out = Path(a.output).resolve()
    if not donor_path.is_file() or not frame_path.is_file():
        raise SystemExit("MARS_ORAL_BRIDGE: FAIL — donor or measured mouth frame missing")

    donor = np.load(donor_path, allow_pickle=False)
    frame = json.loads(frame_path.read_text(encoding="utf-8"))
    for key in ("center", "left_corner", "right_corner"):
        if key not in frame:
            raise RuntimeError(f"MARS_ORAL_BRIDGE: measured mouth frame missing {key}")

    mars = require_mesh()
    original_count = len(mars.data.vertices)
    repaired = mars.copy()
    repaired.data = mars.data.copy()
    repaired.name = "MARS_ORAL_REPAIRED_SURFACE"
    repaired_coll = collection("MARS_ORAL_REPAIR")
    unlink_all(repaired)
    repaired_coll.objects.link(repaired)

    v = np.asarray(donor["vertices"], dtype=np.float64)
    f = np.asarray(donor["faces"], dtype=np.int32)
    jaw = np.asarray(donor["jaw_open_delta"], dtype=np.float64)
    masks = {
        "sock": np.asarray(donor["mouth_sock_mask"], dtype=bool),
        "upper": np.asarray(donor["upper_mask"], dtype=bool),
        "lower": np.asarray(donor["lower_mask"], dtype=bool),
        "teeth": np.asarray(donor["teeth_mask"], dtype=bool),
        "gums": np.asarray(donor["gums_mask"], dtype=bool),
        "tongue": np.asarray(donor["tongue_mask"], dtype=bool),
    }

    mat, scale = fit_transform(v[masks["sock"]], frame)
    plane_point, plane_normal = lip_plane(frame, repaired)
    recess = float(a.recess)

    material_specs = {
        "sock": ("MARS_ORAL_CAVITY", (0.012, 0.002, 0.003, 1.0), 0.78),
        "teeth": ("MARS_ORAL_TEETH", (0.82, 0.76, 0.60, 1.0), 0.34),
        "gums": ("MARS_ORAL_GUMS", (0.24, 0.018, 0.025, 1.0), 0.52),
        "tongue": ("MARS_ORAL_TONGUE", (0.42, 0.045, 0.065, 1.0), 0.48),
    }

    def ensure_material(tag):
        name, rgba, rough = material_specs[tag]
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        m.diffuse_color = rgba
        m.roughness = rough
        return m

    objs = {}
    for tag in ("sock", "teeth", "gums", "tongue"):
        sv, sf, used = submesh(v, f, masks[tag])
        ob = make_mesh("MARS_ORAL_" + tag.upper(), sv, sf, repaired_coll)
        ob.matrix_world = mat.copy()
        ob.data.materials.append(ensure_material(tag))
        objs[tag] = (ob, used)

        # IMPORTANT: GNM's canonical jaw-open motion is applied only to donor
        # anatomy. The MARS identity skin receives ZERO synthetic jaw displacement.
        if tag in ("teeth", "gums", "tongue"):
            local_jaw = jaw[used] * scale
        else:
            local_jaw = np.zeros_like(jaw[used])
        add_shape(ob, "jaw_open", local_jaw)

    oral_objects = {tag: objs[tag][0] for tag in objs}
    recess_report = {}
    for tag, ob in oral_objects.items():
        moved, front_after = recess_object_behind_plane(ob, plane_point, plane_normal, recess)
        recess_report[tag] = {"moved": moved, "front_signed": front_after}

    assert_no_protrusion(oral_objects, plane_point, plane_normal, label="oral donor pre-boolean")

    sock = objs["sock"][0]
    cutter = sock.copy()
    cutter.data = sock.data.copy()
    cutter.name = "MARS_ORAL_CAVITY_CUTTER"
    repaired_coll.objects.link(cutter)
    cutter.matrix_world = sock.matrix_world.copy()
    cutter.scale = cutter.scale * 1.02
    cutter.matrix_world.translation += Vector(((-plane_normal) * (recess * 0.5)).tolist())
    solidify_cutter_inward(cutter, thickness=0.010)

    cutter_protrusion = protrusion_mm(cutter, plane_point, plane_normal)
    if cutter_protrusion > PROTRUSION_TOLERANCE:
        cutter.matrix_world.translation += Vector(((-plane_normal) * (cutter_protrusion + recess * 0.25)).tolist())
        cutter_protrusion = protrusion_mm(cutter, plane_point, plane_normal)
        if cutter_protrusion > PROTRUSION_TOLERANCE:
            raise RuntimeError(
                "MARS_ORAL_BRIDGE: PROTRUSION_FAIL — cavity cutter still past lip plane "
                f"(protrusion={cutter_protrusion:.6f})."
            )

    boolean_cavity(repaired, cutter)
    bpy.data.objects.remove(cutter, do_unlink=True)

    protrusion_after = assert_no_protrusion(oral_objects, plane_point, plane_normal, label="oral donor post-boolean")

    lower_delta = jaw[masks["lower"]]
    travel = float(np.linalg.norm(np.mean(lower_delta, axis=0)) * scale)
    if travel <= 1e-5:
        raise RuntimeError("MARS_ORAL_BRIDGE: GNM jaw-open donor has zero lower travel")

    # Do NOT synthesize a mouth-opening shape on MARS_CANONICAL. The old radial
    # deformation was the measured source of the gooey-skin failure: it moved
    # arbitrary skin vertices according to an ellipse rather than the mesh's own
    # anatomical crease. Keep the canonical skin identity surface stationary
    # until a measured seam/crease-driven lip rig is installed.
    skin_delta = np.zeros((len(repaired.data.vertices), 3), dtype=np.float64)
    skin_motion_max_mm = 0.0
    add_shape(repaired, "jaw_open", skin_delta)
    key = repaired.data.shape_keys.key_blocks["jaw_open"]
    for i, p in enumerate(key.data):
        if (Vector(p.co) - repaired.data.vertices[i].co).length > skin_motion_max_mm:
            skin_motion_max_mm = float((Vector(p.co) - repaired.data.vertices[i].co).length)

    # Preserve phoneme keys as aliases of the donor-anatomy-driven state. Do not
    # introduce additional skin deformation until crease-derived lip ownership is
    # available. This makes the current bridge honest rather than visually wrong.
    base = repaired.data.vertices
    for name, factor in (("AA", 1.0), ("OH", 0.78), ("EE", 0.28), ("MM", 0.0)):
        k = repaired.shape_key_add(name=name)
        for i, p in enumerate(key.data):
            k.data[i].co = base[i].co

    repaired["mars_source_object"] = mars.name
    repaired["mars_source_vertex_count"] = original_count
    repaired["oral_donor"] = "Google GNM Head v3 / Apache-2.0"
    repaired["cavity_source"] = "GNM mouth_sock"
    repaired["sphere_cavity"] = False
    repaired["procedural_tooth_grid"] = False
    repaired["measured_mouth_frame"] = str(frame_path)
    repaired["jaw_open_source"] = "GNM canonical mouth-open expression"
    repaired["mars_skin_jaw_deformation"] = "FORBIDDEN_RADIAL_DISABLED"
    repaired["mars_skin_jaw_motion_max"] = float(skin_motion_max_mm)
    repaired["oral_jaw_travel"] = float(travel)
    repaired["mouth_fix_routing"] = "GNM_INTERNAL_ANATOMY_ONLY_UNTIL_CREASE_RIG"
    repaired["visual_truth_note"] = (
        "Canonical skin receives zero synthetic jaw-open displacement. "
        "Lip opening must be driven from the MARS mesh crease/seam, not an interpolated ellipse."
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print("MARS_ORAL_BRIDGE: VERIFIED")
    print(f"SOURCE_VERTICES={original_count}")
    print(f"ORAL_JAW_TRAVEL={travel:.6f}")
    print(f"SKIN_JAW_MOTION_MAX={skin_motion_max_mm:.9f}")
    print("SKIN_JAW_DEFORMATION=DISABLED")
    print("JAW_OPEN_SOURCE=GNM_CANONICAL")
    print(f"OUTPUT={out}")


if __name__ == "__main__":
    import sys
    main()
