# -*- coding: utf-8 -*-
# CJLook1PaleWash - TRIPPEDD / Cape Jones studio gizmo (original code).
#
# LOOK 1 - PALE WASH (canon: mhvnsnt/cape-jones docs/lighting/RENDER-LOOKS.md,
# PR #264): Blender AgX view transform, the show default - flat, pale,
# washed-out everyday colour. The canonical definition lives in Blender;
# this Natron group is the comp-side translation for display-referred
# plates: saturation pulled down to 0.82, gamma lifted (pale, low
# contrast), whites left alone. Stack order in canon is lights -> look
# -> finish grade (grades.py on top if the scene wants one).
#
# Chain: Input -> Saturation -> Grade -> Output
import NatronEngine
import sys

def getPluginID():
    return "com.trippedd.CJLook1PaleWash"

def getLabel():
    return "CJ LOOK 1 Pale Wash"

def getVersion():
    return 1

def getGrouping():
    return "Color/TRIPPEDD"

def getPluginDescription():
    return ("LOOK 1 - PALE WASH (AgX family, the show default). Flat, pale, "
            "washed-out colour for everyday / daylight / talking scenes. "
            "Knobs: Saturation Scale (multiplies 0.82), Lift (gamma lift).")

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

def createInstance(app, group):
    lastNode = group
    lastNode.controls = lastNode.createPageParam("controls", "Controls")
    _knob(lastNode, lastNode.controls, "saturationScale", "Saturation Scale",
          0, 4, 0, 2, 1.0, "Multiplies the baked LOOK 1 saturation (0.82). 1.0 = canon.")
    _knob(lastNode, lastNode.controls, "lift", "Lift (Gamma)",
          0, 4, 0, 2, 1.12, "Grade gamma lift. Canon 1.12: pale, lifted, low contrast (AgX feel).")
    lastNode.setPagesOrder(['controls', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    inp = _mk_node(app, group, [("fr.inria.built-in.Input", 1)])
    if inp is not None:
        inp.setScriptName("Input1"); inp.setLabel("Source"); inp.setPosition(0, 0)
    sat = _mk_node(app, group, [("net.sf.openfx.SaturationPlugin", 2),
                                ("net.sf.openfx.SaturationPlugin", 1)])
    if sat is not None:
        sat.setScriptName("Saturation1"); sat.setLabel("Saturation LOOK1"); sat.setPosition(0, 100)
    grade = _mk_node(app, group, [("net.sf.openfx.GradePlugin", 1),
                                  ("net.sf.openfx.GradePlugin", 2)])
    if grade is not None:
        grade.setScriptName("Grade1"); grade.setLabel("Grade LOOK1"); grade.setPosition(0, 200)
    out = _mk_node(app, group, [("fr.inria.built-in.Output", 1)])
    if out is not None:
        out.setLabel("Output1"); out.setPosition(0, 300)

    if sat is not None:
        if not _set_expr(sat, ["saturation"], "thisGroup.saturationScale.get() * 0.82"):
            _set(sat, ["saturation"], 0.82)
    if grade is not None:
        # Grade "gamma" is a 4-dim colour param in Natron 2.5.0 (probed -
        # see test log); the lift must land on every dimension.
        _color_expr(grade, "gamma", "thisGroup.lift.get()", [1.12, 1.12, 1.12, 1.12])

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
