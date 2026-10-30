# -*- coding: utf-8 -*-
# CJLook2DeepSaturation — TRIPPEDD / Cape Jones studio gizmo (original code).
#
# LOOK 2 — DEEP SATURATION (canon: mhvnsnt/cape-jones
# docs/lighting/RENDER-LOOKS.md, PR #264): the ACES 1.0 - SDR Video look.
# The canonical definition lives in Blender (ACES OCIO view transform).
# This Natron group is the comp-side translation for display-referred
# plates, built from the cape-jones grade recipes in
# production/pipeline/grades.py (CJ_DAY / OUTSIDE_ACID family):
#   saturation 1.45, contrast ~1.10, blacks deepened, whites protected.
# If your plate is a linear ACEScg EXR, prefer the exact route instead:
# set the project OCIO config to the cape-jones cg-config ACES file and
# view ACES 1.0 - SDR Video (see docs/LOOKS-AND-LED-KNOBS.md).
#
# Chain: Input -> Saturation -> Grade -> Output
import NatronEngine
import sys

def getPluginID():
    return "com.trippedd.CJLook2DeepSaturation"

def getLabel():
    return "CJ LOOK 2 Deep Saturation"

def getVersion():
    return 1

def getGrouping():
    return "Color/TRIPPEDD"

def getPluginDescription():
    return ("LOOK 2 - DEEP SATURATION (ACES family). Rich, punchy color for "
            "night / LED / moody scenes. Comp-side translation of the "
            "cape-jones ACES look using its own grade recipes "
            "(saturation 1.45, contrast 1.10, deepened blacks). "
            "Knobs: Saturation Scale (multiplies 1.45), Contrast, "
            "Black Lift (negative deepens blacks).")

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
    """Set the same expression on all 4 dims of a colour param, else fallback."""
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

def createInstance(app, group):
    lastNode = group
    lastNode.controls = lastNode.createPageParam("controls", "Controls")

    param = lastNode.createDoubleParam("saturationScale", "Saturation Scale")
    param.setMinimum(0, 0); param.setMaximum(4, 0)
    param.setDisplayMinimum(0, 0); param.setDisplayMaximum(2, 0)
    param.setDefaultValue(1, 0); param.restoreDefaultValue(0)
    lastNode.controls.addParam(param)
    param.setHelp("Multiplies the baked LOOK 2 saturation (1.45). 1.0 = canon.")
    param.setAddNewLine(True); param.setAnimationEnabled(True)
    lastNode.saturationScale = param; del param

    param = lastNode.createDoubleParam("contrast", "Contrast")
    param.setMinimum(0, 0); param.setMaximum(4, 0)
    param.setDisplayMinimum(0, 0); param.setDisplayMaximum(2, 0)
    param.setDefaultValue(1.10, 0); param.restoreDefaultValue(0)
    lastNode.controls.addParam(param)
    param.setHelp("Grade gamma-side contrast. Canon 1.10 (grades.py CJ family).")
    param.setAddNewLine(True); param.setAnimationEnabled(True)
    lastNode.contrast = param; del param

    param = lastNode.createDoubleParam("blackLift", "Black Lift")
    param.setMinimum(-0.2, 0); param.setMaximum(0.2, 0)
    param.setDisplayMinimum(-0.1, 0); param.setDisplayMaximum(0.1, 0)
    param.setDefaultValue(-0.02, 0); param.restoreDefaultValue(0)
    lastNode.controls.addParam(param)
    param.setHelp("Grade black point. Canon -0.02: blacks deepened, not crushed.")
    param.setAddNewLine(True); param.setAnimationEnabled(True)
    lastNode.blackLift = param; del param

    lastNode.setPagesOrder(['controls', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    inp = _mk_node(app, group, [("fr.inria.built-in.Input", 1)])
    if inp is not None:
        inp.setScriptName("Input1"); inp.setLabel("Source"); inp.setPosition(0, 0)
    sat = _mk_node(app, group, [("net.sf.openfx.SaturationPlugin", 2),
                                ("net.sf.openfx.SaturationPlugin", 1)])
    if sat is not None:
        sat.setScriptName("Saturation1"); sat.setLabel("Saturation LOOK2"); sat.setPosition(0, 100)
    grade = _mk_node(app, group, [("net.sf.openfx.GradePlugin", 1),
                                  ("net.sf.openfx.GradePlugin", 2)])
    if grade is not None:
        grade.setScriptName("Grade1"); grade.setLabel("Grade LOOK2"); grade.setPosition(0, 200)
    out = _mk_node(app, group, [("fr.inria.built-in.Output", 1)])
    if out is not None:
        out.setLabel("Output1"); out.setPosition(0, 300)

    if sat is not None:
        if not _set_expr(sat, ["saturation"], "thisGroup.saturationScale.get() * 1.45"):
            _set(sat, ["saturation"], 1.45)
    if grade is not None:
        # Grade gamma (4-dim colour param, probed) tracks the contrast knob;
        # (expression set on every colour dimension, static fallback -0.02).
        _color_expr(grade, "gamma", "thisGroup.contrast.get()", [1.10, 1.10, 1.10, 1.10])
        bp_ok = False
        try:
            bp = grade.getParam("blackPoint")
        except Exception:
            bp = None
        if bp is not None:
            for dim in range(4):
                try:
                    bp.setExpression("thisGroup.blackLift.get()", False, dim)
                    bp_ok = True
                except Exception:
                    bp_ok = False
                    break
            if not bp_ok:
                for dim in range(4):
                    try:
                        bp.setValue(-0.02, dim)
                    except Exception:
                        pass

    if inp is not None and sat is not None:
        sat.connectInput(0, inp)
    if sat is not None and grade is not None:
        grade.connectInput(0, sat)
    if grade is not None and out is not None:
        out.connectInput(0, grade)
    elif sat is not None and out is not None:
        out.connectInput(0, sat)
    elif inp is not None and out is not None:
        out.connectInput(0, inp)
