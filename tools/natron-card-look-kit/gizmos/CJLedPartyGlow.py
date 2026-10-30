# -*- coding: utf-8 -*-
# CJLedPartyGlow.py - TRIPPEDD / Cape Jones studio gizmo (original code).
#
# CJLedPartyGlow - static LED grade + glow, packaged from the cape-jones recipes:
#   * static grade: production/pipeline/grades.py LED_PARTY
#     colour matrix rr=1.15 rb=0.10 / gg=1.05 gb=0.10 / br=0.10 bg=0.05 bb=1.15, eq saturation=1.80 first in chain, saturation 1.80, contrast 1.12
#     (ffmpeg eq/colour-channel-mixer values, translated 1:1 to a Natron
#     Multiply tint + Saturation + Grade chain - see
#     docs/LOOKS-AND-LED-KNOBS.md for the translation table)
#   * glow: production/pipeline/comp_glow.py preset "energy-blast"
#     (glow 1.0, screen-blended blur, comp_glow.py's own recipe)
# Animated versions of the LED presets (hue cycling over time) stay in
# led_controller.py - Natron groups here are the static comp finishing
# form; animate the Tint / Glow Strength knobs for movement.
#
# Chain: Input -> Multiply(tint) -> Saturation -> Grade -+
#          Input -> Blur --------------------------------> Merge(screen) -> Output
import NatronEngine
import sys

def getPluginID():
    return "com.trippedd.CJLedPartyGlow"

def getLabel():
    return "CJ LED Party Glow"

def getVersion():
    return 1

def getGrouping():
    return "Color/TRIPPEDD"

def getPluginDescription():
    return "LED PARTY grade (grades.py, saturation 1.80) + energy-blast glow (comp_glow.py). Party / Baked Jones scenes. Knobs: Intensity, Saturation Scale, Glow Strength, Glow Size."

def _mk_node(app, group, candidates):
    for pid, ver in candidates:
        try:
            n = app.createNode(pid, ver, group)
        except Exception:
            n = None
        if n is not None:
            return n
    return None

def _set(node, names, value, dim=0):
    if node is None:
        return False
    for name in names:
        try:
            p = node.getParam(name)
        except Exception:
            p = None
        if p is not None:
            try:
                p.setValue(value, dim)
                return True
            except Exception:
                try:
                    p.set(value)
                    return True
                except Exception:
                    pass
    return False

def _set_expr(node, names, expr):
    if node is None:
        return False
    for name in names:
        try:
            p = node.getParam(name)
        except Exception:
            p = None
        if p is not None:
            try:
                p.setExpression(expr, False, 0)
                return True
            except Exception:
                pass
    return False

def _color_expr(node, name, expr, fallback):
    """Set the same expression on all 4 dims of a colour param, else fallback values."""
    if node is None:
        return
    try:
        p = node.getParam(name)
    except Exception:
        p = None
    if p is None:
        return
    ok = True
    for dim in range(4):
        try:
            p.setExpression(expr, False, dim)
        except Exception:
            ok = False
            break
    if not ok:
        for dim, v in enumerate(fallback):
            try:
                p.setValue(v, dim)
            except Exception:
                pass

def _color_set(node, name, values):
    if node is None:
        return
    try:
        p = node.getParam(name)
    except Exception:
        p = None
    if p is None:
        return
    for dim, v in enumerate(values):
        try:
            p.setValue(v, dim)
        except Exception:
            pass

def _knob(group, page, name, label, mn, mx, dmn, dmx, default, helptext):
    param = group.createDoubleParam(name, label)
    param.setMinimum(mn, 0); param.setMaximum(mx, 0)
    param.setDisplayMinimum(dmn, 0); param.setDisplayMaximum(dmx, 0)
    param.setDefaultValue(default, 0); param.restoreDefaultValue(0)
    page.addParam(param)
    param.setHelp(helptext)
    param.setAddNewLine(True); param.setAnimationEnabled(True)
    setattr(group, name, param)
    return param

TINT = [1.15, 1.05, 1.15]
SATURATION = 1.80
CONTRAST = 1.12
GLOW_DEFAULT = 1.0

def createInstance(app, group):
    lastNode = group
    lastNode.controls = lastNode.createPageParam("controls", "Controls")
    _knob(lastNode, lastNode.controls, "intensity", "Intensity (Mix)",
          0, 1, 0, 1, 1.0, "Overall strength of the tint+grade. 1.0 = canon static LED grade.")
    _knob(lastNode, lastNode.controls, "saturationScale", "Saturation Scale",
          0, 4, 0, 2, 1.0, "Multiplies the baked LED saturation (1.80). 1.0 = canon.")
    _knob(lastNode, lastNode.controls, "glowStrength", "Glow Strength",
          0, 1, 0, 1, GLOW_DEFAULT, "Screen-blended blur glow (comp_glow.py). Canon 1.0. 0 = grade only.")
    _knob(lastNode, lastNode.controls, "glowSize", "Glow Size",
          0, 100, 0, 50, 16.0, "Blur size for the glow pass.")
    lastNode.setPagesOrder(['controls', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    inp = _mk_node(app, group, [("fr.inria.built-in.Input", 1)])
    if inp is not None:
        inp.setScriptName("Input1"); inp.setLabel("Source"); inp.setPosition(0, 0)
    mult = _mk_node(app, group, [("net.sf.openfx.MultiplyPlugin", 2),
                                 ("net.sf.openfx.MultiplyPlugin", 1)])
    if mult is not None:
        mult.setScriptName("Multiply1"); mult.setLabel("LED Tint"); mult.setPosition(0, 100)
    sat = _mk_node(app, group, [("net.sf.openfx.SaturationPlugin", 2),
                                ("net.sf.openfx.SaturationPlugin", 1)])
    if sat is not None:
        sat.setScriptName("Saturation1"); sat.setLabel("Saturation LED"); sat.setPosition(0, 200)
    grade = _mk_node(app, group, [("net.sf.openfx.GradePlugin", 1),
                                  ("net.sf.openfx.GradePlugin", 2)])
    if grade is not None:
        grade.setScriptName("Grade1"); grade.setLabel("Grade LED"); grade.setPosition(0, 300)
    blur = _mk_node(app, group, [("net.sf.cimg.CImgBlur", 3), ("net.sf.cimg.CImgBlur", 4),
                                 ("net.sf.cimg.CImgBlur", 2), ("net.sf.cimg.CImgBlur", 1)])
    if blur is not None:
        blur.setScriptName("Blur1"); blur.setLabel("Glow Blur"); blur.setPosition(250, 300)
    merge = _mk_node(app, group, [("net.sf.openfx.MergePlugin", 1),
                                  ("net.sf.openfx.MergePlugin", 2)])
    if merge is not None:
        merge.setScriptName("Merge1"); merge.setLabel("Glow Screen"); merge.setPosition(0, 420)
    out = _mk_node(app, group, [("fr.inria.built-in.Output", 1)])
    if out is not None:
        out.setLabel("Output1"); out.setPosition(0, 520)

    if mult is not None:
        # Diagonal of the grades.py colour matrix, as a Multiply tint.
        # Off-diagonal mixer terms are documented in the knobs doc; the
        # diagonal carries the dominant tint of every LED grade.
        _color_set(mult, "value", [TINT[0], TINT[1], TINT[2], 1.0])
        _color_set(mult, "color", [TINT[0], TINT[1], TINT[2], 1.0])
    if sat is not None:
        if not _set_expr(sat, ["saturation"], "thisGroup.saturationScale.get() * " + str(SATURATION)):
            _set(sat, ["saturation"], SATURATION)
    if grade is not None:
        _color_set(grade, "gamma", [CONTRAST, CONTRAST, CONTRAST, CONTRAST])
        if not _set_expr(grade, ["mix"], "thisGroup.intensity.get()"):
            _set(grade, ["mix"], 1.0)
    if blur is not None:
        if not _set_expr(blur, ["size"], "thisGroup.glowSize.get()"):
            _set(blur, ["size"], 16.0)
    if merge is not None:
        _set(merge, ["operation"], "screen")
        try:
            p = merge.getParam("userTextArea")
            if p is not None:
                p.setValue("<Natron>(screen)</Natron>")
        except Exception:
            pass
        if not _set_expr(merge, ["mix"], "thisGroup.glowStrength.get()"):
            _set(merge, ["mix"], GLOW_DEFAULT)

    if inp is not None and mult is not None:
        mult.connectInput(0, inp)
    if mult is not None and sat is not None:
        sat.connectInput(0, mult)
    if sat is not None and grade is not None:
        grade.connectInput(0, sat)
    if grade is not None and blur is not None:
        blur.connectInput(0, grade)
    if grade is not None and merge is not None:
        merge.connectInput(0, grade)
    if blur is not None and merge is not None:
        merge.connectInput(1, blur)
    if merge is not None and out is not None:
        out.connectInput(0, merge)
    elif grade is not None and out is not None:
        out.connectInput(0, grade)
    elif inp is not None and out is not None:
        out.connectInput(0, inp)
