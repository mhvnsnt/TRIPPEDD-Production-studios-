# Sculpt Finisher (SPEC Z-2) + FlowRetopo wrapper (SPEC Z-1)
#
# TRIPPEDD Production Studios — free-versions build-out of the ZBrush-style
# sculpt finishing workflow (BUILD-MAP-FREE-VERSIONS.md, section 3).
#
# DONOR FIRST: this add-on hand-rolls NO remesher, NO unwrapper and NO baker.
# It is pure orchestration (`bpy`) of donors that already exist:
#   * Blender built-in Voxel Remesh      (the DynaMesh analog)
#   * Blender built-in QuadriFlow remesh (the ZRemesher analog, built in)
#   * Blender built-in Smart UV Project + Pack Islands
#   * Blender built-in Multires modifier + Cycles bake (Project-All analog)
#   * Blender built-in glTF / STL exporters
#   * Instant Meshes (free external field-aligned remesher by Wenzel Jakob
#     et al., https://github.com/wjakob/instant-meshes) — optional round-trip
#     used by the FlowRetopo wrapper when its official pre-built binary is
#     present on the machine. If it is absent the wrapper says so, with the
#     reason, and the QuadriFlow path still runs. Nothing is faked.
#
# Fail-soft contract (both operators):
#   * All destructive work happens on a DUPLICATE of the source object.
#     The source object is never modified.
#   * Each step logs [OK] / [FAILED]; on failure the chain stops cleanly,
#     the duplicate is left in the scene (renamed *_FAILED_<step>) for
#     inspection, and the operator reports the failing step.
#
# Original code, written for this studio. License: GPL-3.0-or-later
# (kept Blender-add-on compatible).

bl_info = {
    "name": "Sculpt Finisher + FlowRetopo",
    "author": "TRIPPEDD Production Studios",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Sculpt Finisher",
    "description": (
        "Z-2: one-click sculpt finishing chain (voxel cleanup -> QuadriFlow "
        "-> UV unwrap+pack -> Multires + Cycles bake -> GLB/STL export). "
        "Z-1: FlowRetopo wrapper chaining QuadriFlow (symmetry) and an "
        "Instant Meshes round-trip, density from vertex colors, checked mesh."
    ),
    "category": "Mesh",
}

import os
import shutil
import subprocess
import tempfile

import bmesh
import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
)
from bpy.types import Operator, Panel, PropertyGroup

LOG_PREFIX = "[SculptFinisher]"


def log(msg):
    print(f"{LOG_PREFIX} {msg}", flush=True)


# --------------------------------------------------------------------------
# Mesh checking (shared by Z-1 and Z-2)
# --------------------------------------------------------------------------

def mesh_check(obj):
    """Return a dict of topology facts for a mesh object (pure read)."""
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    boundary = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    loose_verts = sum(1 for v in bm.verts if not v.link_edges)
    degenerate = sum(1 for f in bm.faces if f.calc_area() <= 1e-12)
    quads = sum(1 for f in bm.faces if len(f.verts) == 4)
    tris = sum(1 for f in bm.faces if len(f.verts) == 3)
    ngons = sum(1 for f in bm.faces if len(f.verts) > 4)
    result = {
        "verts": len(bm.verts),
        "edges": len(bm.edges),
        "faces": len(bm.faces),
        "quads": quads,
        "tris": tris,
        "ngons": ngons,
        "non_manifold_edges": non_manifold,
        "boundary_edges": boundary,
        "loose_verts": loose_verts,
        "degenerate_faces": degenerate,
    }
    bm.free()
    return result


def format_check(check):
    return (
        "verts={verts} edges={edges} faces={faces} quads={quads} tris={tris} "
        "ngons={ngons} non_manifold_edges={non_manifold_edges} "
        "boundary_edges={boundary_edges} loose_verts={loose_verts} "
        "degenerate_faces={degenerate_faces}"
    ).format(**check)


# --------------------------------------------------------------------------
# Vertex-color density (Z-1)
# --------------------------------------------------------------------------

def density_target_faces(obj, base_faces):
    """Scale a base face target by painted vertex-color density.

    Looks for a POINT-domain color attribute named like *density* first,
    otherwise the first POINT color attribute. Brighter paint = denser
    retopo: factor = 0.5 + mean_luminance  (range 0.5x .. 1.5x).
    Returns (target_faces, human_readable_note).
    """
    attrs = [a for a in obj.data.color_attributes if a.domain == 'POINT']
    if not attrs:
        return base_faces, "no vertex colors present; density factor 1.0"
    chosen = None
    for attr in attrs:
        if 'density' in attr.name.lower():
            chosen = attr
            break
    if chosen is None:
        chosen = attrs[0]
    total = 0.0
    count = 0
    for c in chosen.data:
        col = c.color
        total += 0.2126 * col[0] + 0.7152 * col[1] + 0.0722 * col[2]
        count += 1
    if count == 0:
        return base_faces, "vertex color attribute empty; density factor 1.0"
    mean = total / count
    factor = 0.5 + mean
    target = max(100, int(round(base_faces * factor)))
    note = (
        f"density from vertex colors '{chosen.name}': mean luminance "
        f"{mean:.3f} -> factor {factor:.2f} -> target faces {target} "
        f"(base {base_faces})"
    )
    return target, note


# --------------------------------------------------------------------------
# Instant Meshes resolution (Z-1 donor)
# --------------------------------------------------------------------------

def find_instant_meshes_binary(explicit_path=""):
    """Locate the Instant Meshes binary. Returns (path_or_None, reason).

    Search order: explicit path from the panel, $INSTANT_MESHES_BIN,
    PATH (both spellings), then the studio tools install location.
    """
    candidates = []
    if explicit_path:
        candidates.append(bpy.path.abspath(explicit_path))
    env = os.environ.get("INSTANT_MESHES_BIN")
    if env:
        candidates.append(env)
    for name in ("Instant Meshes", "instant-meshes", "InstantMeshes"):
        found = shutil.which(name)
        if found:
            candidates.append(found)
    home = os.path.expanduser("~")
    candidates.append(os.path.join(
        home, "workspace", "tools", "instant-meshes", "Instant Meshes"))
    candidates.append("/usr/local/bin/Instant Meshes")
    for cand in candidates:
        if cand and os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand, f"found at {cand}"
    return None, (
        "Instant Meshes binary not found (searched panel path, "
        "$INSTANT_MESHES_BIN, PATH, ~/workspace/tools/instant-meshes/). "
        "Official free pre-built Linux binary: "
        "https://instant-meshes.s3.eu-central-1.amazonaws.com/"
        "instant-meshes-linux.zip (linked from the README of "
        "https://github.com/wjakob/instant-meshes). QuadriFlow path "
        "is unaffected."
    )


def run_instant_meshes(binary, obj, target_faces, workdir):
    """Round-trip `obj` through Instant Meshes in batch mode.

    Exports OBJ, runs the binary with -f <faces> -r 4 -p 4 (pure quad,
    4-RoSy orientation / 4-PoSy position fields), imports the result as a
    NEW object and returns it. Raises RuntimeError on any failure.
    """
    in_obj = os.path.join(workdir, "im_in.obj")
    out_obj = os.path.join(workdir, "im_out.obj")

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.obj_export(
        filepath=in_obj,
        export_selected_objects=True,
        export_materials=False,
        export_uv=True,
        export_normals=True,
    )
    if not os.path.isfile(in_obj):
        raise RuntimeError("OBJ export for Instant Meshes produced no file")

    cmd = [binary, in_obj, "-o", out_obj,
           "-f", str(int(target_faces)), "-r", "4", "-p", "4"]
    log(f"Instant Meshes run: {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    tail = (proc.stdout or "")[-400:] + (proc.stderr or "")[-400:]
    if proc.returncode != 0:
        raise RuntimeError(
            f"Instant Meshes exited {proc.returncode}: {tail.strip()}")
    if not os.path.isfile(out_obj) or os.path.getsize(out_obj) == 0:
        raise RuntimeError(
            f"Instant Meshes wrote no output. Log: {tail.strip()}")

    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=out_obj)
    new_objs = [o for o in bpy.data.objects if o not in before
                and o.type == 'MESH']
    if not new_objs:
        raise RuntimeError("Instant Meshes OBJ import produced no mesh object")
    result = new_objs[0]
    result.name = obj.name + "_IM"
    result.matrix_world = obj.matrix_world.copy()
    return result


# --------------------------------------------------------------------------
# Small shared helpers
# --------------------------------------------------------------------------

def duplicate_object(src, suffix):
    bpy.ops.object.select_all(action='DESELECT')
    dup = src.copy()
    dup.data = src.data.copy()
    dup.name = src.name + suffix
    bpy.context.collection.objects.link(dup)
    dup.select_set(True)
    bpy.context.view_layer.objects.active = dup
    return dup


def set_active_only(obj):
    bpy.ops.object.select_all(action='DESELECT')
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


# --------------------------------------------------------------------------
# Settings
# --------------------------------------------------------------------------

class SculptFinisherSettings(PropertyGroup):
    do_voxel: BoolProperty(
        name="Voxel-remesh cleanup", default=True,
        description="Uniform voxel remesh of the duplicate (DynaMesh analog)")
    voxel_size: FloatProperty(
        name="Voxel size", default=0.08, min=0.005, max=1.0)
    do_quadriflow: BoolProperty(
        name="QuadriFlow retopo", default=True,
        description="QuadriFlow quad retopology on the duplicate")
    target_faces: IntProperty(
        name="Target faces", default=4000, min=100, max=500000)
    use_symmetry: BoolProperty(
        name="Mesh symmetry", default=True)
    symmetry_axis: EnumProperty(
        name="Symmetry axis",
        items=[('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")],
        default='X')
    do_uv: BoolProperty(
        name="UV unwrap + pack", default=True)
    uv_margin: FloatProperty(
        name="UV island margin", default=0.003, min=0.0, max=0.1)
    do_multires: BoolProperty(
        name="Add Multires", default=True)
    multires_levels: IntProperty(
        name="Multires levels", default=1, min=0, max=4)
    do_bake: BoolProperty(
        name="Bake maps (Cycles)", default=True,
        description="Bake from the high-res source onto the duplicate")
    bake_normal: BoolProperty(name="Normal", default=True)
    bake_ao: BoolProperty(name="AO", default=True)
    bake_color: BoolProperty(name="Color", default=True)
    bake_resolution: IntProperty(
        name="Bake resolution", default=1024, min=64, max=8192)
    bake_samples: IntProperty(
        name="Bake samples", default=16, min=1, max=256)
    bake_ray_distance: FloatProperty(
        name="Bake ray distance", default=0.25, min=0.0, max=10.0)
    bake_dir: StringProperty(
        name="Bake output dir", subtype='DIR_PATH', default="//bakes/")
    export_preset: EnumProperty(
        name="Export preset",
        items=[
            ('GAME_GLB', "Game (GLB)", "Export a game-ready GLB"),
            ('PRINT_STL', "Print (STL)", "Export a print-ready STL"),
            ('BOTH', "Both (GLB + STL)", ""),
            ('NONE', "None", "No export"),
        ],
        default='GAME_GLB')
    export_dir: StringProperty(
        name="Export dir", subtype='DIR_PATH', default="//export/")
    im_binary: StringProperty(
        name="Instant Meshes binary", subtype='FILE_PATH', default="",
        description="Path to the free Instant Meshes binary; blank = auto-detect")
    use_instant_meshes: BoolProperty(
        name="Then Instant Meshes round-trip", default=True,
        description="After QuadriFlow, try the Instant Meshes round-trip "
                    "when its binary is available")
    last_log: StringProperty(name="Last result", default="")


# --------------------------------------------------------------------------
# Z-2 — Sculpt Finisher chain steps
# --------------------------------------------------------------------------

def step_voxel_remesh(obj, s):
    obj.data.remesh_voxel_size = s.voxel_size
    obj.data.remesh_voxel_adaptivity = 0.0
    set_active_only(obj)
    bpy.ops.object.voxel_remesh()
    if len(obj.data.vertices) == 0:
        raise RuntimeError("voxel remesh produced an empty mesh")


def step_quadriflow(obj, s, target_faces=None):
    set_active_only(obj)
    # Blender 4.5: QuadriFlow has no symmetry_axis argument — the symmetry
    # axis lives on the mesh itself (Mesh.use_mirror_x/y/z, the Symmetry
    # panel). Set it on the (duplicate) mesh before remeshing.
    if s.use_symmetry:
        obj.data.use_mirror_x = s.symmetry_axis == 'X'
        obj.data.use_mirror_y = s.symmetry_axis == 'Y'
        obj.data.use_mirror_z = s.symmetry_axis == 'Z'
    bpy.ops.object.quadriflow_remesh(
        use_mesh_symmetry=s.use_symmetry,
        use_preserve_sharp=False,
        use_preserve_boundary=False,
        preserve_attributes=True,
        smooth_normals=True,
        mode='FACES',
        target_faces=int(target_faces if target_faces is not None
                         else s.target_faces),
        seed=0,
    )
    if len(obj.data.polygons) == 0:
        raise RuntimeError("QuadriFlow produced an empty mesh")


def step_uv_unwrap_pack(obj, s):
    if not obj.data.uv_layers:
        obj.data.uv_layers.new(name="UVMap")
    set_active_only(obj)
    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=s.uv_margin)
        bpy.ops.uv.pack_islands(margin=s.uv_margin)
    finally:
        bpy.ops.object.mode_set(mode='OBJECT')
    if not obj.data.uv_layers.active:
        raise RuntimeError("UV unwrap produced no UV layer")


def step_multires(obj, s):
    mod = obj.modifiers.new(name="SF_Multires", type='MULTIRES')
    # Blender >= 4.3 removed MultiresModifier.subdivision_type
    # (Catmull-Clark is the only subdivision type now).
    set_active_only(obj)
    for _ in range(s.multires_levels):
        bpy.ops.object.multires_subdivide(
            modifier=mod.name, mode='CATMULL_CLARK')
    return mod


def step_bake(obj, high, s):
    """Bake normal / AO / color from `high` onto `obj` (Cycles selected-to-active)."""
    scene = bpy.context.scene
    out_dir = bpy.path.abspath(s.bake_dir)
    os.makedirs(out_dir, exist_ok=True)

    prev_engine = scene.render.engine
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = s.bake_samples
    scene.cycles.device = 'CPU'
    bake = scene.render.bake
    bake.use_selected_to_active = True
    bake.use_cage = False
    bake.max_ray_distance = s.bake_ray_distance  # BakeSettings name in 4.x
    bake.margin = 8

    # Multires on the low would fight the bake; park it during baking.
    parked = []
    for mod in obj.modifiers:
        if mod.type == 'MULTIRES':
            parked.append((mod, mod.show_render, mod.show_viewport))
            mod.show_render = False
            mod.show_viewport = False

    mat = bpy.data.materials.new(name=f"{obj.name}_BakeMat")
    mat.use_nodes = True
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    nodes = mat.node_tree.nodes

    wanted = []
    if s.bake_normal:
        wanted.append(('NORMAL', 'Normal', None))
    if s.bake_ao:
        wanted.append(('AO', 'AO', None))
    if s.bake_color:
        wanted.append(('DIFFUSE', 'Color', {'COLOR'}))

    baked_paths = []
    try:
        for bake_type, suffix, pass_filter in wanted:
            img_name = f"{obj.name}_{suffix}"
            img = bpy.data.images.get(img_name)
            if img is None:
                img = bpy.data.images.new(
                    img_name, s.bake_resolution, s.bake_resolution,
                    alpha=False, float_buffer=False)
            tex = nodes.new('ShaderNodeTexImage')
            tex.image = img
            tex.name = f"SF_BAKE_{suffix}"
            for n in nodes:
                n.select = False
            tex.select = True
            nodes.active = tex

            bpy.ops.object.select_all(action='DESELECT')
            high.select_set(True)
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            kwargs = {"type": bake_type}
            if pass_filter is not None:
                kwargs["pass_filter"] = pass_filter
            bpy.ops.object.bake(**kwargs)

            path = os.path.join(out_dir, f"{img_name}.png")
            img.filepath_raw = path
            img.save()
            if not os.path.isfile(path) or os.path.getsize(path) == 0:
                raise RuntimeError(f"bake of {suffix} wrote no file at {path}")
            baked_paths.append(path)
            log(f"bake {suffix}: wrote {path} "
                f"({os.path.getsize(path)} bytes)")
            nodes.remove(tex)
    finally:
        for mod, sr, sv in parked:
            mod.show_render = sr
            mod.show_viewport = sv
        scene.render.engine = prev_engine
    return baked_paths


def step_export(obj, s):
    out_dir = bpy.path.abspath(s.export_dir)
    os.makedirs(out_dir, exist_ok=True)
    written = []
    set_active_only(obj)
    if s.export_preset in ('GAME_GLB', 'BOTH'):
        path = os.path.join(out_dir, f"{obj.name}.glb")
        bpy.ops.export_scene.gltf(
            filepath=path, export_format='GLB',
            use_selection=True, export_apply=False)
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            raise RuntimeError(f"GLB export wrote no file at {path}")
        written.append(path)
    if s.export_preset in ('PRINT_STL', 'BOTH'):
        path = os.path.join(out_dir, f"{obj.name}.stl")
        try:
            bpy.ops.wm.stl_export(
                filepath=path, use_selection=True, apply_modifiers=False)
        except AttributeError:
            bpy.ops.export_mesh.stl(
                filepath=path, use_selection=True, use_mesh_modifiers=False)
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            raise RuntimeError(f"STL export wrote no file at {path}")
        written.append(path)
    return written


class OBJECT_OT_sculpt_finisher(Operator):
    """Run the full Z-2 sculpt finishing chain on a duplicate."""
    bl_idname = "object.sculpt_finisher_run"
    bl_label = "Run Sculpt Finisher (Z-2)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene.sculpt_finisher
        src = context.active_object
        if src is None or src.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object first")
            return {'CANCELLED'}

        before = mesh_check(src)
        log(f"Z-2 start on '{src.name}': {format_check(before)}")
        work = duplicate_object(src, "_FINISHED")
        high = src  # bake source: the untouched original

        baked = []
        exported = []
        steps = []
        if s.do_voxel:
            steps.append(("voxel_remesh",
                          lambda: step_voxel_remesh(work, s)))
        if s.do_quadriflow:
            steps.append(("quadriflow",
                          lambda: step_quadriflow(work, s)))
        if s.do_uv:
            steps.append(("uv_unwrap_pack",
                          lambda: step_uv_unwrap_pack(work, s)))
        if s.do_multires:
            steps.append(("multires",
                          lambda: step_multires(work, s)))
        if s.do_bake:
            steps.append(("bake",
                          lambda: baked.extend(step_bake(work, high, s))))
        if s.export_preset != 'NONE':
            steps.append(("export",
                          lambda: exported.extend(step_export(work, s))))

        wm = context.window_manager
        wm.progress_begin(0, len(steps))
        failed_step = None
        try:
            for i, (name, fn) in enumerate(steps):
                log(f"step {i + 1}/{len(steps)}: {name} ...")
                try:
                    fn()
                except Exception as exc:  # fail soft: log + stop cleanly
                    failed_step = name
                    log(f"step {name} FAILED: {exc}")
                    break
                log(f"step {name} OK: verts={len(work.data.vertices)} "
                    f"faces={len(work.data.polygons)}")
                wm.progress_update(i + 1)
        finally:
            wm.progress_end()

        after = mesh_check(work)
        if failed_step is not None:
            work.name = f"{src.name}_FAILED_{failed_step}"
            msg = (f"Z-2 stopped at step '{failed_step}' (see console log). "
                   f"Original untouched ({before['verts']} verts). "
                   f"Duplicate kept as '{work.name}'.")
            s.last_log = msg
            log(msg)
            # WARNING, not ERROR: an ERROR report raises RuntimeError for
            # scripted bpy.ops callers, which would break the fail-soft
            # contract for orchestration lanes driving this add-on.
            self.report({'WARNING'}, msg)
            return {'CANCELLED'}

        msg = (f"Z-2 done: '{src.name}' {before['verts']} verts -> "
               f"'{work.name}' {after['verts']} verts / {after['faces']} faces; "
               f"baked={len(baked)} exported={len(exported)}; "
               f"check: {format_check(after)}")
        s.last_log = msg
        log(msg)
        self.report({'INFO'}, msg)
        return {'FINISHED'}


# --------------------------------------------------------------------------
# Z-1 — FlowRetopo wrapper
# --------------------------------------------------------------------------

class OBJECT_OT_flow_retopo(Operator):
    """QuadriFlow (symmetry) then an Instant Meshes round-trip, checked."""
    bl_idname = "object.flow_retopo_run"
    bl_label = "Run FlowRetopo (Z-1)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene.sculpt_finisher
        src = context.active_object
        if src is None or src.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object first")
            return {'CANCELLED'}

        before = mesh_check(src)
        target, density_note = density_target_faces(src, s.target_faces)
        log(f"Z-1 start on '{src.name}': {format_check(before)}")
        log(f"Z-1 {density_note}")

        work = duplicate_object(src, "_RETOPO")
        result_obj = work
        engine_used = []

        # Stage 1 — QuadriFlow with symmetry (Blender built-in donor).
        try:
            step_quadriflow(work, s, target_faces=target)
            engine_used.append("QuadriFlow")
            log(f"Z-1 QuadriFlow OK: {format_check(mesh_check(work))}")
        except Exception as exc:
            work.name = f"{src.name}_FAILED_quadriflow"
            msg = (f"Z-1 stopped: QuadriFlow failed: {exc}. "
                   f"Original untouched. Duplicate kept as '{work.name}'.")
            s.last_log = msg
            log(msg)
            self.report({'WARNING'}, msg)  # see Z-2 note on ERROR reports
            return {'CANCELLED'}

        # Stage 2 — Instant Meshes round-trip, when honestly available.
        im_status = "not attempted (disabled in panel)"
        if s.use_instant_meshes:
            binary, reason = find_instant_meshes_binary(s.im_binary)
            if binary is None:
                im_status = f"unavailable: {reason}"
                log(f"Z-1 Instant Meshes {im_status}")
            else:
                try:
                    with tempfile.TemporaryDirectory(
                            prefix="sf_im_") as tmp:
                        im_obj = run_instant_meshes(binary, work, target, tmp)
                    im_check = mesh_check(im_obj)
                    qf_check = mesh_check(work)
                    log(f"Z-1 Instant Meshes result: {format_check(im_check)}")
                    if (im_check["faces"] > 0
                            and im_check["non_manifold_edges"]
                            <= qf_check["non_manifold_edges"]):
                        old_data = work.data
                        bpy.data.objects.remove(work, do_unlink=True)
                        bpy.data.meshes.remove(old_data)
                        im_obj.name = f"{src.name}_RETOPO"
                        result_obj = im_obj
                        engine_used.append("Instant Meshes")
                        im_status = (
                            f"ran ({binary}); result adopted (non-manifold "
                            f"{im_check['non_manifold_edges']} <= QuadriFlow "
                            f"{qf_check['non_manifold_edges']})")
                    else:
                        bpy.data.objects.remove(im_obj, do_unlink=True)
                        im_status = (
                            f"ran ({binary}); QuadriFlow result kept "
                            f"(IM non-manifold {im_check['non_manifold_edges']} "
                            f"> QuadriFlow {qf_check['non_manifold_edges']})")
                    log(f"Z-1 Instant Meshes {im_status}")
                except Exception as exc:
                    im_status = (f"attempted with {binary} but failed: {exc}; "
                                 f"QuadriFlow result kept")
                    log(f"Z-1 Instant Meshes {im_status}")

        after = mesh_check(result_obj)
        msg = (f"Z-1 done via {' + '.join(engine_used)}: "
               f"'{src.name}' {before['verts']} verts -> "
               f"'{result_obj.name}' {after['verts']} verts; "
               f"Instant Meshes: {im_status}; "
               f"check: {format_check(after)}")
        s.last_log = msg
        log(msg)
        self.report({'INFO'}, msg)
        return {'FINISHED'}


# --------------------------------------------------------------------------
# Panel
# --------------------------------------------------------------------------

class VIEW3D_PT_sculpt_finisher(Panel):
    bl_label = "Sculpt Finisher"
    bl_idname = "VIEW3D_PT_sculpt_finisher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sculpt Finisher"

    def draw(self, context):
        s = context.scene.sculpt_finisher
        layout = self.layout

        box = layout.box()
        box.label(text="Z-2 Sculpt Finisher chain", icon='MOD_REMESH')
        box.prop(s, "do_voxel")
        if s.do_voxel:
            box.prop(s, "voxel_size")
        box.prop(s, "do_quadriflow")
        box.prop(s, "do_uv")
        if s.do_uv:
            box.prop(s, "uv_margin")
        box.prop(s, "do_multires")
        if s.do_multires:
            box.prop(s, "multires_levels")
        box.prop(s, "do_bake")
        if s.do_bake:
            row = box.row(align=True)
            row.prop(s, "bake_normal")
            row.prop(s, "bake_ao")
            row.prop(s, "bake_color")
            box.prop(s, "bake_resolution")
            box.prop(s, "bake_samples")
            box.prop(s, "bake_ray_distance")
            box.prop(s, "bake_dir")
        box.prop(s, "export_preset")
        if s.export_preset != 'NONE':
            box.prop(s, "export_dir")
        box.operator("object.sculpt_finisher_run", icon='PLAY')

        box = layout.box()
        box.label(text="Z-1 FlowRetopo (shared settings)", icon='MESH_GRID')
        box.prop(s, "target_faces")
        row = box.row(align=True)
        row.prop(s, "use_symmetry")
        row.prop(s, "symmetry_axis")
        box.prop(s, "use_instant_meshes")
        if s.use_instant_meshes:
            box.prop(s, "im_binary")
        box.operator("object.flow_retopo_run", icon='PLAY')

        if s.last_log:
            box = layout.box()
            box.label(text="Last result", icon='INFO')
            box.label(text=s.last_log[:64])


classes = (
    SculptFinisherSettings,
    OBJECT_OT_sculpt_finisher,
    OBJECT_OT_flow_retopo,
    VIEW3D_PT_sculpt_finisher,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sculpt_finisher = bpy.props.PointerProperty(
        type=SculptFinisherSettings)


def unregister():
    del bpy.types.Scene.sculpt_finisher
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
