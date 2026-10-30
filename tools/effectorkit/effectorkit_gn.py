"""
EffectorKit - shared Geometry Nodes construction library.

Original clean-room construction. The *behavior* (a stack of named
effectors - Plain / Random / Step / Shader / Sound / Delay - each shaped
by a spatial falloff, applied in a fixed order to cloned instances) was
studied from public MoGraph documentation only. Every node network here
is built from Blender's own Geometry Nodes primitives by this code; no
third-party code, assets, or presets are included.

Used by:
  - build_effectorkit_library.py  (writes the .blend asset library)
  - demo_effectorkit.py          (demo scene)
  - test_effectorkit.py           (headless proof tests)
  - addon/effectorkit            (panel add-on appends the built groups)

Effector order (fixed, documented in README.md):
  Cloner -> Plain -> Random -> Step -> Shader -> Sound -> Delay

Conventions:
  - Every effector group has Geometry in/out first, then the Falloff
    sockets, then its own sockets.
  - Rotation sockets are in DEGREES at the interface (converted to
    radians inside), because animators think in degrees.
  - 'Strength' (0..1 typical) is multiplied by the falloff weight, so
    Strength * Falloff is the true per-instance influence.
"""

import math

import bpy

DEG2RAD = math.pi / 180.0

EFFECTOR_ORDER = ["EK_Plain", "EK_Random", "EK_Step",
                  "EK_Shader", "EK_Sound", "EK_Delay"]

GROUP_NAMES = ["EK_ClonerGrid"] + EFFECTOR_ORDER + ["EK_EffectorStack"]


# --------------------------------------------------------------------------
# low-level helpers
# --------------------------------------------------------------------------

def _node(ng, idname, x=0.0, y=0.0, label=None):
    n = ng.nodes.new(idname)
    n.location = (x, y)
    if label:
        n.label = label
    return n


def _link(ng, a, ai, b, bi):
    return ng.links.new(a.outputs[ai], b.inputs[bi])


def _math(ng, op, x, y):
    n = _node(ng, "ShaderNodeMath", x, y, label=op)
    n.operation = op
    return n


def _vmath(ng, op, x, y):
    n = _node(ng, "ShaderNodeVectorMath", x, y, label=op)
    n.operation = op
    return n


def _const_vec(ng, vec, x, y):
    n = _node(ng, "ShaderNodeCombineXYZ", x, y, label="const")
    for i in range(3):
        n.inputs[i].default_value = float(vec[i])
    return n


def _mix_float(ng, x, y):
    n = _node(ng, "ShaderNodeMix", x, y, label="mix f")
    n.data_type = 'FLOAT'
    return n  # Factor in0, A in2, B in3, Result out0


def _mix_vec(ng, x, y):
    n = _node(ng, "ShaderNodeMix", x, y, label="mix v")
    n.data_type = 'VECTOR'
    return n  # Factor in0, A in4, B in5, Result out1


def _switch_float(ng, x, y):
    n = _node(ng, "GeometryNodeSwitch", x, y, label="switch f")
    n.input_type = 'FLOAT'
    return n  # Switch in0, False in1, True in2, Output out0


def _ramp_from_d01(ng, d01_node, d01_idx, soft_node, soft_idx, x, y):
    """Shared sphere/box weight curve: d01 in 0..1 (0 = centre).
    Returns (node, out_idx) of weight in 0..1, shaped by softness."""
    inv = _math(ng, 'SUBTRACT', x, y)
    inv.inputs[0].default_value = 1.0
    _link(ng, d01_node, d01_idx, inv, 1)
    # clamp 0..1 via MINIMUM/MAXIMUM chain
    mx = _math(ng, 'MAXIMUM', x + 150, y)
    mx.inputs[1].default_value = 0.0
    _link(ng, inv, 0, mx, 0)
    mn = _math(ng, 'MINIMUM', x + 300, y)
    mn.inputs[1].default_value = 1.0
    _link(ng, mx, 0, mn, 0)
    t = mn
    # smoothstep: s = t * t * (3 - 2t)
    two_t = _math(ng, 'MULTIPLY', x + 450, y)
    two_t.inputs[1].default_value = 2.0
    _link(ng, t, 0, two_t, 0)
    three = _math(ng, 'SUBTRACT', x + 450, y - 150)
    three.inputs[0].default_value = 3.0
    _link(ng, two_t, 0, three, 1)
    m1 = _math(ng, 'MULTIPLY', x + 600, y)
    _link(ng, t, 0, m1, 0)
    _link(ng, three, 0, m1, 1)
    s = _math(ng, 'MULTIPLY', x + 750, y)
    _link(ng, t, 0, s, 0)
    _link(ng, m1, 0, s, 1)
    # softness shapes the exponent: exp = mix(3.0, 0.35, softness)
    ex = _mix_float(ng, x + 750, y - 200)
    ex.inputs[2].default_value = 3.0
    ex.inputs[3].default_value = 0.35
    _link(ng, soft_node, soft_idx, ex, 0)
    pw = _math(ng, 'POWER', x + 900, y)
    _link(ng, s, 0, pw, 0)
    _link(ng, ex, 0, pw, 1)
    return pw, 0


class Kit:
    """One effector group under construction, with tracked input order."""

    def __init__(self, name):
        self.ng = bpy.data.node_groups.new(name=name, type='GeometryNodeTree')
        self.ng.interface.new_socket(name='Geometry', in_out='INPUT',
                                     socket_type='NodeSocketGeometry')
        self.ng.interface.new_socket(name='Geometry', in_out='OUTPUT',
                                     socket_type='NodeSocketGeometry')
        self.gi = _node(self.ng, 'NodeGroupInput', -900, 0)
        self.go = _node(self.ng, 'NodeGroupOutput', 1100, 0)
        self.n_in = 1  # Geometry is input 0

    def input(self, name, stype, default=None, mn=None, mx=None):
        s = self.ng.interface.new_socket(name=name, in_out='INPUT',
                                         socket_type=stype)
        if default is not None:
            try:
                s.default_value = default
            except Exception:
                pass
        if mn is not None:
            try:
                s.min_value = mn
            except Exception:
                pass
        if mx is not None:
            try:
                s.max_value = mx
            except Exception:
                pass
        idx = self.n_in
        self.n_in += 1
        return idx

    def finish(self, geo_node, geo_idx=0):
        _link(self.ng, geo_node, geo_idx, self.go, 0)
        self.ng.asset_mark()
        return self.ng


def add_falloff(kit):
    """Add the shared Falloff sockets + network to a Kit.

    Modes: 0=None (weight 1), 1=Sphere, 2=Box (Chebyshev), 3=Noise.
    Returns (node, out_idx) producing the per-instance weight field.
    """
    ng, gi = kit.ng, kit.gi
    i_mode = kit.input('Falloff Mode', 'NodeSocketInt', 1, 0, 3)
    i_use_obj = kit.input('Falloff Use Object Center', 'NodeSocketInt', 0, 0, 1)
    i_cobj = kit.input('Falloff Center Object', 'NodeSocketObject')
    i_cvec = kit.input('Falloff Center', 'NodeSocketVector', (0.0, 0.0, 0.0))
    i_rad = kit.input('Falloff Radius', 'NodeSocketFloat', 3.0, 0.001)
    i_soft = kit.input('Falloff Softness', 'NodeSocketFloat', 0.5, 0.0, 1.0)
    i_nscale = kit.input('Falloff Noise Scale', 'NodeSocketFloat', 1.5, 0.0)
    i_nstr = kit.input('Falloff Noise Strength', 'NodeSocketFloat', 0.5, 0.0, 1.0)

    x, y = -650, -500
    pos = _node(ng, 'GeometryNodeInputPosition', x, y)
    oi = _node(ng, 'GeometryNodeObjectInfo', x, y - 250, label="center obj")
    _link(ng, gi, i_cobj, oi, 0)
    # centre = UseObject ? ObjectInfo.Location : Center vector
    sw = _node(ng, 'GeometryNodeSwitch', x + 200, y - 250, label="center?")
    sw.input_type = 'VECTOR'
    _link(ng, gi, i_use_obj, sw, 0)
    _link(ng, gi, i_cvec, sw, 1)
    oi_loc_idx = [i for i, s in enumerate(oi.outputs) if s.name == 'Location'][0]
    _link(ng, oi, oi_loc_idx, sw, 2)
    delta = _vmath(ng, 'SUBTRACT', x + 400, y)
    _link(ng, pos, 0, delta, 0)
    _link(ng, sw, 0, delta, 1)

    # --- sphere weight ---
    dist = _vmath(ng, 'LENGTH', x + 600, y + 150)
    _link(ng, delta, 0, dist, 0)
    d01s = _math(ng, 'DIVIDE', x + 750, y + 150)
    _link(ng, dist, 1, d01s, 0)
    _link(ng, gi, i_rad, d01s, 1)
    w_sphere = _ramp_from_d01(ng, d01s, 0, gi, i_soft, x + 900, y + 150)

    # --- box weight (Chebyshev distance) ---
    absd = _vmath(ng, 'ABSOLUTE', x + 600, y - 150)
    _link(ng, delta, 0, absd, 0)
    sep = _node(ng, 'ShaderNodeSeparateXYZ', x + 750, y - 150)
    _link(ng, absd, 0, sep, 0)
    mx1 = _math(ng, 'MAXIMUM', x + 900, y - 150)
    _link(ng, sep, 0, mx1, 0)
    _link(ng, sep, 1, mx1, 1)
    mx2 = _math(ng, 'MAXIMUM', x + 900, y - 300)
    _link(ng, mx1, 0, mx2, 0)
    _link(ng, sep, 2, mx2, 1)
    d01b = _math(ng, 'DIVIDE', x + 1050, y - 150)
    _link(ng, mx2, 0, d01b, 0)
    _link(ng, gi, i_rad, d01b, 1)
    w_box = _ramp_from_d01(ng, d01b, 0, gi, i_soft, x + 1200, y - 150)

    # --- noise weight ---
    npos = _vmath(ng, 'SCALE', x + 600, y - 500)
    _link(ng, pos, 0, npos, 0)
    _link(ng, gi, i_nscale, npos, 3)
    ntex = _node(ng, 'ShaderNodeTexNoise', x + 800, y - 500, label="falloff noise")
    ntex.noise_dimensions = '3D'
    _link(ng, npos, 0, ntex, 0)
    ntex.inputs[3].default_value = 2.0   # Detail
    ntex.inputs[4].default_value = 0.5   # Roughness
    # weight = 1 - strength * (1 - fac)
    one_m = _math(ng, 'SUBTRACT', x + 1000, y - 500)
    one_m.inputs[0].default_value = 1.0
    _link(ng, ntex, 0, one_m, 1)
    scaled = _math(ng, 'MULTIPLY', x + 1150, y - 500)
    _link(ng, one_m, 0, scaled, 0)
    _link(ng, gi, i_nstr, scaled, 1)
    w_noise = _math(ng, 'SUBTRACT', x + 1300, y - 500)
    w_noise.inputs[0].default_value = 1.0
    _link(ng, scaled, 0, w_noise, 1)

    # --- mode select: nested switches ---
    def _eq_mode(target):
        c = _math(ng, 'COMPARE', x + 1400, y - 700 - target * 60)
        _link(ng, gi, i_mode, c, 0)
        c.inputs[1].default_value = float(target)
        c.inputs[2].default_value = 0.1
        return c, 0

    eq1 = _eq_mode(1)
    eq2 = _eq_mode(2)
    eq3 = _eq_mode(3)
    eq0 = _eq_mode(0)
    # inner: mode2 ? box : sphere
    s_a = _switch_float(ng, x + 1550, y - 100)
    _link(ng, eq2[0], eq2[1], s_a, 0)
    _link(ng, w_sphere[0], w_sphere[1], s_a, 1)
    _link(ng, w_box[0], w_box[1], s_a, 2)
    # mode3 ? noise : s_a
    s_b = _switch_float(ng, x + 1700, y - 100)
    _link(ng, eq3[0], eq3[1], s_b, 0)
    _link(ng, s_a, 0, s_b, 1)
    _link(ng, w_noise, 0, s_b, 2)
    # mode0 ? 1.0 : s_b
    one = _math(ng, 'ADD', x + 1700, y + 100)
    one.inputs[0].default_value = 1.0
    one.inputs[1].default_value = 0.0
    s_c = _switch_float(ng, x + 1850, y - 100)
    _link(ng, eq0[0], eq0[1], s_c, 0)
    _link(ng, s_b, 0, s_c, 1)
    _link(ng, one, 0, s_c, 2)
    return s_c, 0


def _strength_weight(kit, w, x, y):
    """Strength socket * falloff weight -> (node, idx)."""
    ng, gi = kit.ng, kit.gi
    i_str = kit.input('Strength', 'NodeSocketFloat', 1.0, 0.0)
    m = _math(ng, 'MULTIPLY', x, y)
    _link(ng, gi, i_str, m, 0)
    _link(ng, w[0], w[1], m, 1)
    return m, 0


def _deg_vec_to_rad_weighted(ng, deg_node, deg_idx, w_node, w_idx, x, y):
    """Vector of degrees -> radians * per-instance weight. Returns (node,0)."""
    conv = _const_vec(ng, (DEG2RAD, DEG2RAD, DEG2RAD), x, y + 120)
    rad = _vmath(ng, 'MULTIPLY', x + 200, y)
    _link(ng, deg_node, deg_idx, rad, 0)
    _link(ng, conv, 0, rad, 1)
    out = _vmath(ng, 'SCALE', x + 400, y)
    _link(ng, rad, 0, out, 0)
    _link(ng, w_node, w_idx, out, 3)
    return out, 0


def _apply_trs(kit, offset, rotation, scale, x=500):
    """Chain Translate -> Rotate -> Scale instances. Each arg is
    (node, out_idx) or None to skip that stage."""
    ng, gi = kit.ng, kit.gi
    cur_node, cur_idx = gi, 0
    if offset is not None:
        t = _node(ng, 'GeometryNodeTranslateInstances', x, 200, label="translate")
        _link(ng, cur_node, cur_idx, t, 0)
        _link(ng, offset[0], offset[1], t, 2)
        t.inputs[3].default_value = False  # world-space offset
        cur_node, cur_idx = t, 0
    if rotation is not None:
        r = _node(ng, 'GeometryNodeRotateInstances', x, 0, label="rotate")
        _link(ng, cur_node, cur_idx, r, 0)
        _link(ng, rotation[0], rotation[1], r, 2)
        cur_node, cur_idx = r, 0
    if scale is not None:
        s = _node(ng, 'GeometryNodeScaleInstances', x, -200, label="scale")
        _link(ng, cur_node, cur_idx, s, 0)
        _link(ng, scale[0], scale[1], s, 2)
        cur_node, cur_idx = s, 0
    return cur_node, cur_idx


def _scale_from_uniform(ng, f_node, f_idx, x, y):
    c = _node(ng, 'ShaderNodeCombineXYZ', x, y, label="uniform scale")
    for i in range(3):
        _link(ng, f_node, f_idx, c, i)
    return c, 0


# --------------------------------------------------------------------------
# Cloner
# --------------------------------------------------------------------------

def build_cloner_grid():
    name = 'EK_ClonerGrid'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    kit = Kit(name)
    ng, gi = kit.ng, kit.gi
    i_obj = kit.input('Instance Object', 'NodeSocketObject')
    i_cx = kit.input('Count X', 'NodeSocketInt', 5, 1)
    i_cy = kit.input('Count Y', 'NodeSocketInt', 5, 1)
    i_sp = kit.input('Spacing', 'NodeSocketFloat', 1.2, 0.0)

    grid = _node(ng, 'GeometryNodeMeshGrid', -400, 200, label="grid")
    # Size = (Count-1) * Spacing
    for axis, ci, si in (('X', 0, 0), ('Y', 1, 1)):
        sub = _math(ng, 'SUBTRACT', -650, 350 - si * 120)
        sub.inputs[1].default_value = 1.0
        _link(ng, gi, i_cx if axis == 'X' else i_cy, sub, 0)
        mul = _math(ng, 'MULTIPLY', -500, 350 - si * 120)
        _link(ng, sub, 0, mul, 0)
        _link(ng, gi, i_sp, mul, 1)
        _link(ng, mul, 0, grid, si)          # Size X / Size Y
        _link(ng, gi, i_cx if axis == 'X' else i_cy, grid, 2 + si)  # Vertices
    m2p = _node(ng, 'GeometryNodeMeshToPoints', -150, 200, label="to points")
    _link(ng, grid, 0, m2p, 0)
    oi = _node(ng, 'GeometryNodeObjectInfo', -400, -100, label="proto")
    oi.inputs[1].default_value = True  # As Instance
    _link(ng, gi, i_obj, oi, 0)
    oi_geo = [i for i, s in enumerate(oi.outputs) if s.name == 'Geometry'][0]
    iop = _node(ng, 'GeometryNodeInstanceOnPoints', 100, 200, label="instance")
    _link(ng, m2p, 0, iop, 0)
    _link(ng, oi, oi_geo, iop, 2)
    return kit.finish(iop)


# --------------------------------------------------------------------------
# Effectors
# --------------------------------------------------------------------------

def build_plain():
    name = 'EK_Plain'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    kit = Kit(name)
    ng, gi = kit.ng, kit.gi
    w = add_falloff(kit)
    i_off = kit.input('Offset', 'NodeSocketVector', (0.0, 0.0, 0.0))
    i_rot = kit.input('Rotation (deg)', 'NodeSocketVector', (0.0, 0.0, 0.0))
    i_scl = kit.input('Scale', 'NodeSocketVector', (1.0, 1.0, 1.0))
    sw = _strength_weight(kit, w, 100, -500)

    off = _vmath(ng, 'SCALE', 100, 200)
    _link(ng, gi, i_off, off, 0)
    _link(ng, sw[0], sw[1], off, 3)
    rot = _deg_vec_to_rad_weighted(ng, gi, i_rot, sw[0], sw[1], 100, 0)
    # scale_i = mix(1, Scale_i, sw)
    sep = _node(ng, 'ShaderNodeSeparateXYZ', 100, -250)
    _link(ng, gi, i_scl, sep, 0)
    comb = _node(ng, 'ShaderNodeCombineXYZ', 500, -250)
    for i in range(3):
        m = _mix_float(ng, 300, -150 - i * 100)
        m.inputs[2].default_value = 1.0
        _link(ng, sep, i, m, 3)
        _link(ng, sw[0], sw[1], m, 0)
        _link(ng, m, 0, comb, i)
    end = _apply_trs(kit, (off, 0), rot, (comb, 0))
    return kit.finish(*end)


def build_random():
    name = 'EK_Random'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    kit = Kit(name)
    ng, gi = kit.ng, kit.gi
    w = add_falloff(kit)
    i_seed = kit.input('Seed', 'NodeSocketInt', 0)
    i_pamt = kit.input('Position Amount', 'NodeSocketVector', (0.5, 0.5, 0.5))
    i_ramt = kit.input('Rotation Amount (deg)', 'NodeSocketVector',
                       (180.0, 180.0, 180.0))
    i_samt = kit.input('Scale Amount', 'NodeSocketVector', (0.3, 0.3, 0.3))
    sw = _strength_weight(kit, w, 100, -500)

    def _rand_vec(seed_node, seed_idx, x, y):
        r = _node(ng, 'FunctionNodeRandomValue', x, y, label="random vec")
        r.data_type = 'FLOAT_VECTOR'
        r.inputs[0].default_value = (0.0, 0.0, 0.0)
        r.inputs[1].default_value = (1.0, 1.0, 1.0)
        if seed_node is not None:
            _link(ng, seed_node, seed_idx, r, 8)  # Seed
        return r, 0

    rv1 = _rand_vec(gi, i_seed, -200, 300)
    seed2 = _node(ng, 'FunctionNodeIntegerMath', -400, 100, label="seed+1000")
    seed2.operation = 'ADD'
    seed2.inputs[1].default_value = 1000
    _link(ng, gi, i_seed, seed2, 0)
    rv2 = _rand_vec(seed2, 0, -200, 100)
    half = _const_vec(ng, (0.5, 0.5, 0.5), -200, -50)

    def _centered(rv, x, y):
        sub = _vmath(ng, 'SUBTRACT', x, y)
        _link(ng, rv[0], rv[1], sub, 0)
        _link(ng, half, 0, sub, 1)
        two = _vmath(ng, 'SCALE', x + 200, y)
        two.inputs[3].default_value = 2.0
        _link(ng, sub, 0, two, 0)
        return two, 0

    c1 = _centered(rv1, 100, 300)   # -1..1 per axis
    c2 = _centered(rv2, 100, 100)
    off = _vmath(ng, 'MULTIPLY', 400, 300)
    _link(ng, c1[0], c1[1], off, 0)
    _link(ng, gi, i_pamt, off, 1)
    off2 = _vmath(ng, 'SCALE', 600, 300)
    _link(ng, off, 0, off2, 0)
    _link(ng, sw[0], sw[1], off2, 3)

    rotdeg = _vmath(ng, 'MULTIPLY', 400, 100)
    _link(ng, c2[0], c2[1], rotdeg, 0)
    _link(ng, gi, i_ramt, rotdeg, 1)
    rot = _deg_vec_to_rad_weighted(ng, rotdeg, 0, sw[0], sw[1], 600, 100)

    # scale = 1 + c1 * ScaleAmount * sw
    smul = _vmath(ng, 'MULTIPLY', 400, -150)
    _link(ng, c1[0], c1[1], smul, 0)
    _link(ng, gi, i_samt, smul, 1)
    ssc = _vmath(ng, 'SCALE', 600, -150)
    _link(ng, smul, 0, ssc, 0)
    _link(ng, sw[0], sw[1], ssc, 3)
    ones = _const_vec(ng, (1.0, 1.0, 1.0), 600, -300)
    sadd = _vmath(ng, 'ADD', 800, -150)
    _link(ng, ones, 0, sadd, 0)
    _link(ng, ssc, 0, sadd, 1)

    end = _apply_trs(kit, (off2, 0), rot, (sadd, 0))
    return kit.finish(*end)


def build_step():
    name = 'EK_Step'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    kit = Kit(name)
    ng, gi = kit.ng, kit.gi
    w = add_falloff(kit)
    i_off = kit.input('Offset Per Step', 'NodeSocketVector', (0.0, 0.0, 0.25))
    i_rot = kit.input('Rotation Per Step (deg)', 'NodeSocketVector',
                      (0.0, 0.0, 15.0))
    i_scl = kit.input('Scale Per Step', 'NodeSocketVector', (0.0, 0.0, 0.0))
    sw = _strength_weight(kit, w, 100, -500)

    idx = _node(ng, 'GeometryNodeInputIndex', -200, 300)
    k = _math(ng, 'MULTIPLY', 100, 300, )  # k = index * sw
    _link(ng, idx, 0, k, 0)
    _link(ng, sw[0], sw[1], k, 1)

    off = _vmath(ng, 'SCALE', 300, 300)
    _link(ng, gi, i_off, off, 0)
    _link(ng, k, 0, off, 3)
    rotdeg = _vmath(ng, 'SCALE', 300, 100)
    _link(ng, gi, i_rot, rotdeg, 0)
    _link(ng, k, 0, rotdeg, 3)
    # rotation: degrees already weighted by k; just convert to radians
    conv = _const_vec(ng, (DEG2RAD, DEG2RAD, DEG2RAD), 500, 220)
    rad = _vmath(ng, 'MULTIPLY', 700, 100)
    _link(ng, rotdeg, 0, rad, 0)
    _link(ng, conv, 0, rad, 1)
    smul = _vmath(ng, 'SCALE', 300, -150)
    _link(ng, gi, i_scl, smul, 0)
    _link(ng, k, 0, smul, 3)
    ones = _const_vec(ng, (1.0, 1.0, 1.0), 300, -300)
    sadd = _vmath(ng, 'ADD', 500, -150)
    _link(ng, ones, 0, sadd, 0)
    _link(ng, smul, 0, sadd, 1)

    end = _apply_trs(kit, (off, 0), (rad, 0), (sadd, 0))
    return kit.finish(*end)


def build_shader():
    name = 'EK_Shader'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    kit = Kit(name)
    ng, gi = kit.ng, kit.gi
    w = add_falloff(kit)
    i_img = kit.input('Image', 'NodeSocketImage')
    i_mscale = kit.input('Mapping Scale', 'NodeSocketFloat', 0.25, 0.0)
    i_moff = kit.input('Mapping Offset', 'NodeSocketVector', (0.5, 0.5, 0.0))
    i_off = kit.input('Offset Amount', 'NodeSocketVector', (0.0, 0.0, 1.0))
    i_samt = kit.input('Scale Amount', 'NodeSocketFloat', 0.5)
    sw = _strength_weight(kit, w, 100, -500)

    pos = _node(ng, 'GeometryNodeInputPosition', -200, 300)
    psc = _vmath(ng, 'SCALE', 0, 300)
    _link(ng, pos, 0, psc, 0)
    _link(ng, gi, i_mscale, psc, 3)
    padd = _vmath(ng, 'ADD', 200, 300)
    _link(ng, psc, 0, padd, 0)
    _link(ng, gi, i_moff, padd, 1)
    tex = _node(ng, 'GeometryNodeImageTexture', 400, 300, label="image")
    _link(ng, gi, i_img, tex, 0)
    _link(ng, padd, 0, tex, 1)
    lum_w = _const_vec(ng, (0.299, 0.587, 0.114), 400, 100)
    dot = _vmath(ng, 'DOT_PRODUCT', 600, 300)
    _link(ng, tex, 0, dot, 0)
    _link(ng, lum_w, 0, dot, 1)
    gray = _math(ng, 'MULTIPLY', 800, 300)  # gray * sw
    _link(ng, dot, 1, gray, 0)
    _link(ng, sw[0], sw[1], gray, 1)

    off = _vmath(ng, 'SCALE', 800, 100)
    _link(ng, gi, i_off, off, 0)
    _link(ng, gray, 0, off, 3)
    sfac = _math(ng, 'MULTIPLY', 800, -100)  # gray * ScaleAmount
    _link(ng, gray, 0, sfac, 0)
    _link(ng, gi, i_samt, sfac, 1)
    splus = _math(ng, 'ADD', 950, -100)
    splus.inputs[0].default_value = 1.0
    _link(ng, sfac, 0, splus, 1)
    scl = _scale_from_uniform(ng, splus, 0, 1050, -100)

    end = _apply_trs(kit, (off, 0), None, scl)
    return kit.finish(*end)


def build_sound():
    name = 'EK_Sound'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    kit = Kit(name)
    ng, gi = kit.ng, kit.gi
    w = add_falloff(kit)
    i_curve = kit.input('Bands Curve', 'NodeSocketObject')
    i_cycle = kit.input('Cycle Length', 'NodeSocketInt', 16, 1)
    i_off = kit.input('Offset Amount', 'NodeSocketVector', (0.0, 0.0, 2.0))
    i_samt = kit.input('Scale Amount', 'NodeSocketFloat', 1.0)
    sw = _strength_weight(kit, w, 100, -500)

    idx = _node(ng, 'GeometryNodeInputIndex', -300, 300)
    band = _math(ng, 'MODULO', -100, 300)  # band = index % cycle
    _link(ng, idx, 0, band, 0)
    _link(ng, gi, i_cycle, band, 1)

    oi = _node(ng, 'GeometryNodeObjectInfo', -300, 0, label="curve obj")
    _link(ng, gi, i_curve, oi, 0)
    oi_geo = [i for i, s in enumerate(oi.outputs) if s.name == 'Geometry'][0]
    # Sample the curve's control points directly by band index.
    # (Sample Curve's factor mode is arc-length parameterized, which
    # distorts a band lookup when Y varies - control-point indexing is
    # the exact "band i -> point i" mapping the bake produces.)
    cpos = _node(ng, 'GeometryNodeInputPosition', 100, 0, label="curve pos")
    sample = _node(ng, 'GeometryNodeSampleIndex', 300, 200, label="band point")
    sample.data_type = 'FLOAT_VECTOR'
    sample.domain = 'POINT'
    _link(ng, oi, oi_geo, sample, 0)
    _link(ng, cpos, 0, sample, 1)
    _link(ng, band, 0, sample, 2)
    sep = _node(ng, 'ShaderNodeSeparateXYZ', 550, 200)
    _link(ng, sample, 0, sep, 0)
    val = _math(ng, 'MULTIPLY', 700, 200)  # value * sw
    _link(ng, sep, 1, val, 0)              # Y of curve point = band level
    _link(ng, sw[0], sw[1], val, 1)

    off = _vmath(ng, 'SCALE', 800, 100)
    _link(ng, gi, i_off, off, 0)
    _link(ng, val, 0, off, 3)
    sfac = _math(ng, 'MULTIPLY', 700, -100)
    _link(ng, val, 0, sfac, 0)
    _link(ng, gi, i_samt, sfac, 1)
    splus = _math(ng, 'ADD', 850, -100)
    splus.inputs[0].default_value = 1.0
    _link(ng, sfac, 0, splus, 1)
    scl = _scale_from_uniform(ng, splus, 0, 950, -100)

    end = _apply_trs(kit, (off, 0), None, scl)
    return kit.finish(*end)


def build_delay():
    name = 'EK_Delay'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    kit = Kit(name)
    ng, gi = kit.ng, kit.gi
    w = add_falloff(kit)
    i_fac = kit.input('Factor', 'NodeSocketFloat', 0.2, 0.0, 1.0)
    i_start = kit.input('Start Frame', 'NodeSocketInt', 1)
    sw = _strength_weight(kit, w, 100, -600)  # Strength * falloff scales Factor

    fac = _math(ng, 'MULTIPLY', 300, -600)  # effective factor = Factor * sw
    _link(ng, gi, i_fac, fac, 0)
    _link(ng, sw[0], sw[1], fac, 1)

    # first-frame snap: factor = 1 while frame <= Start Frame
    stime = _node(ng, 'GeometryNodeInputSceneTime', -300, -800)
    startf = _math(ng, 'ADD', -100, -800)
    startf.inputs[1].default_value = 0.5
    _link(ng, gi, i_start, startf, 0)
    lt = _math(ng, 'LESS_THAN', 100, -800)
    _link(ng, stime, 1, lt, 0)  # Frame
    _link(ng, startf, 0, lt, 1)
    fsw = _switch_float(ng, 300, -800)
    _link(ng, lt, 0, fsw, 0)
    _link(ng, fac, 0, fsw, 1)
    fsw.inputs[2].default_value = 1.0

    # simulation zone: previous frame's smoothed positions
    sim_in = _node(ng, 'GeometryNodeSimulationInput', -100, 100, label="sim in")
    sim_out = _node(ng, 'GeometryNodeSimulationOutput', 800, 100, label="sim out")
    sim_in.pair_with_output(sim_out)
    si_geo = [i for i, s in enumerate(sim_in.outputs)
              if s.type == 'GEOMETRY'][0]
    so_in = [i for i, s in enumerate(sim_out.inputs)
             if s.type == 'GEOMETRY' and s.name == 'Geometry'][0]
    so_out = [i for i, s in enumerate(sim_out.outputs)
              if s.type == 'GEOMETRY' and s.name == 'Geometry'][0]

    pos = _node(ng, 'GeometryNodeInputPosition', -300, 300, label="target pos")
    idx = _node(ng, 'GeometryNodeInputIndex', -300, -100)
    named = _node(ng, 'GeometryNodeInputNamedAttribute', -100, -200,
                  label="ek_smooth")
    named.data_type = 'FLOAT_VECTOR'
    named.inputs[0].default_value = 'ek_smooth'
    sample = _node(ng, 'GeometryNodeSampleIndex', 200, -100, label="prev smooth")
    sample.data_type = 'FLOAT_VECTOR'
    sample.domain = 'INSTANCE'  # ek_smooth is stored on the INSTANCE domain
    _link(ng, sim_in, si_geo, sample, 0)
    attr_out = [i for i, s in enumerate(named.outputs)
                if s.name == 'Attribute'][0]
    _link(ng, named, attr_out, sample, 1)
    _link(ng, idx, 0, sample, 2)

    mix = _mix_vec(ng, 450, 100)
    _link(ng, fsw, 0, mix, 0)
    _link(ng, sample, 0, mix, 4)   # A = previous smoothed
    _link(ng, pos, 0, mix, 5)      # B = current target

    # Store ek_smooth BEFORE Set Position: both nodes must evaluate the
    # mix field in the *target* geometry's context. (Storing after
    # Set Position re-reads Position from the already-moved geometry
    # and stores a wrongly re-mixed state.)
    store = _node(ng, 'GeometryNodeStoreNamedAttribute', 550, 100,
                  label="store ek_smooth")
    try:
        store.data_type = 'FLOAT_VECTOR'
    except Exception:
        pass
    store.domain = 'INSTANCE'
    store.inputs[2].default_value = 'ek_smooth'
    _link(ng, gi, 0, store, 0)
    _link(ng, mix, 1, store, 3)
    setp = _node(ng, 'GeometryNodeSetPosition', 700, 300, label="set smoothed")
    _link(ng, store, 0, setp, 0)
    _link(ng, mix, 1, setp, 2)
    _link(ng, setp, 0, sim_out, so_in)
    return kit.finish(sim_out, so_out)


# --------------------------------------------------------------------------
# Stack + library assembly
# --------------------------------------------------------------------------

def build_stack():
    name = 'EK_EffectorStack'
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    subs = [bpy.data.node_groups[n] for n in EFFECTOR_ORDER]
    ng = bpy.data.node_groups.new(name=name, type='GeometryNodeTree')
    ng.interface.new_socket(name='Geometry', in_out='INPUT',
                            socket_type='NodeSocketGeometry')
    ng.interface.new_socket(name='Geometry', in_out='OUTPUT',
                            socket_type='NodeSocketGeometry')
    gi = _node(ng, 'NodeGroupInput', -1400, 0)
    go = _node(ng, 'NodeGroupOutput', 1400, 0)
    # expose every sub-group input (except Geometry), prefixed, in order
    plan = []  # (socket_index_on_gi, group_node, sub_input_name)
    n_in = 1
    group_nodes = []
    for si, sub in enumerate(subs):
        gn = _node(ng, 'GeometryNodeGroup', -1000 + si * 450, 0,
                   label=sub.name)
        gn.node_tree = sub
        group_nodes.append(gn)
        for item in sub.interface.items_tree:
            if getattr(item, 'in_out', None) != 'INPUT':
                continue
            if item.name == 'Geometry':
                continue
            short = sub.name.replace('EK_', '')
            s = ng.interface.new_socket(
                name="%s: %s" % (short, item.name), in_out='INPUT',
                socket_type=item.socket_type)
            for attr in ('default_value', 'min_value', 'max_value'):
                try:
                    setattr(s, attr, getattr(item, attr))
                except Exception:
                    pass
            plan.append((n_in, gn, item.name))
            n_in += 1
    for gi_idx, gn, sub_name in plan:
        tgt = [i for i, s in enumerate(gn.inputs) if s.name == sub_name]
        if tgt:
            _link(ng, gi, gi_idx, gn, tgt[0])
    cur_node, cur_idx = gi, 0
    for gn in group_nodes:
        _link(ng, cur_node, cur_idx, gn, 0)
        cur_node, cur_idx = gn, 0
    _link(ng, cur_node, cur_idx, go, 0)
    ng.asset_mark()
    return ng


def build_all():
    """Build (or fetch) every EffectorKit group. Returns list of groups."""
    build_cloner_grid()
    build_plain()
    build_random()
    build_step()
    build_shader()
    build_sound()
    build_delay()
    build_stack()
    return [bpy.data.node_groups[n] for n in GROUP_NAMES]


# --------------------------------------------------------------------------
# Sound: bake an audio spectrum to a curve object
# --------------------------------------------------------------------------

def bake_spectrum_curve(wav_path, bands=16, name="EK_Spectrum", height=2.0):
    """Analyse a wav file and create a curve object whose point Y values
    are the per-band spectrum levels (X = band position 0..1).

    Pure stdlib (wave + Goertzel per band) so it runs identically inside
    Blender's Python and anywhere else. Returns (object, [levels]).
    """
    import math as _math
    import struct
    import wave

    w = wave.open(wav_path, 'rb')
    n = w.getnframes()
    sr = w.getframerate()
    ch = w.getnchannels()
    sw = w.getsampwidth()
    raw = w.readframes(n)
    w.close()
    fmt = {1: 'b', 2: 'h', 4: 'i'}[sw]
    count = len(raw) // sw
    vals = struct.unpack('<' + fmt * count, raw)
    if ch > 1:
        vals = vals[::ch]
    full_scale = float(2 ** (8 * sw - 1))
    samples = [v / full_scale for v in vals]
    total = len(samples)
    if total == 0:
        raise ValueError("empty wav: %s" % wav_path)

    max_f = sr / 2.0
    min_f = 40.0
    levels = []
    for b in range(bands):
        f0 = min_f * (max_f / min_f) ** (b / bands)
        f1 = min_f * (max_f / min_f) ** ((b + 1) / bands)
        fc = _math.sqrt(f0 * f1)
        k = 2.0 * _math.pi * fc / sr
        coeff = 2.0 * _math.cos(k)
        s1 = s2 = 0.0
        for x in samples:
            s0 = x + coeff * s1 - s2
            s2 = s1
            s1 = s0
        power = s1 * s1 + s2 * s2 - coeff * s1 * s2
        mag = _math.sqrt(max(power, 0.0)) / (total / 2.0)
        levels.append(mag)
    peak = max(levels) or 1.0
    levels = [(v / peak) * height for v in levels]

    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    sp = cu.splines.new('POLY')
    if bands > 1:
        sp.points.add(bands - 1)
    for i, y in enumerate(levels):
        x = i / (bands - 1) if bands > 1 else 0.0
        sp.points[i].co = (x, y, 0.0, 1.0)
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    return ob, levels
