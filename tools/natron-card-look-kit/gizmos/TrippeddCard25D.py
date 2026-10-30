# -*- coding: utf-8 -*-
# TrippeddCard25D — TRIPPEDD studio gizmo (original code).
#
# SPEC N-1 fallback / companion: a minimal, verified card-projection
# group for Natron 2.5.0. Natron has no native 3D system, and the
# community PMCard3D / PMcamera scripts could NOT be fetched (see
# docs/SOURCES-AND-PROVENANCE.md for the verbatim fetch record), so this
# original group covers the shot types Pipeline One actually uses:
# a flat card (background plate, matte painting, title card, character
# plate) moved by a virtual camera, with perspective keystone.
#
# What it does, in comp terms (the 2.5D card trick):
#   * "Camera pan" moves every card by the same pan, scaled by the
#     card's Depth: near cards move more, far cards move less. That
#     differential IS the parallax in Wizard Gang's pan-and-zoom move
#     and in Cape Jones's TV-parallel gag.
#   * CornerPin gives the card a perspective keystone (the card as if
#     photographed at an angle by the virtual camera).
#   * Transform scale = camera zoom / dolly for that card's depth.
# For true camera-mapped projection (a moving 3D camera, geometry the
# camera orbits), use the Blender route in docs/CARD-PROJECTION-RECIPE.md
# — the decision rule there says which shots go which way.
#
# Chain: Input -> CornerPin -> Transform -> Output
import NatronEngine
import sys

def getPluginID():
    return "com.trippedd.TrippeddCard25D"

def getLabel():
    return "TRIPPEDD Card 2.5D"

def getVersion():
    return 1

def getGrouping():
    return "Transform/TRIPPEDD"

def getPluginDescription():
    return ("Minimal card-projection group: virtual-camera pan/zoom with "
            "per-card Depth parallax scaling + CornerPin perspective "
            "keystone. Knobs: Camera Pan X/Y, Camera Zoom, Depth "
            "(0 = locked to camera, 1 = full pan; use >1 for foreground "
            "cards). Perspective is fitted on the CornerPin inside the "
            "group. See "
            "docs/CARD-PROJECTION-RECIPE.md for the route decision rule.")

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

def _set_expr_dim(node, name, expr, dim):
    if node is None:
        return False
    try:
        p = node.getParam(name)
    except Exception:
        p = None
    if p is None:
        return False
    try:
        p.setExpression(expr, False, dim)
        return True
    except Exception:
        return False

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
    _knob(lastNode, lastNode.controls, "camPanX", "Camera Pan X",
          -4000, 4000, -500, 500, 0.0,
          "Virtual camera pan, X (pixels at project format). Every card in the shot gets the same pan; Depth scales it.")
    _knob(lastNode, lastNode.controls, "camPanY", "Camera Pan Y",
          -4000, 4000, -500, 500, 0.0,
          "Virtual camera pan, Y (pixels).")
    _knob(lastNode, lastNode.controls, "camZoom", "Camera Zoom",
          0.05, 20, 0.25, 4, 1.0,
          "Virtual camera zoom/dolly for this card (Transform scale). Animate for the Pipeline One pan-and-zoom move.")
    _knob(lastNode, lastNode.controls, "depth", "Depth (Parallax Factor)",
          0, 4, 0, 2, 1.0,
          "Parallax factor: pan applied to this card = camera pan x depth. Background 0.3-0.6, midground 1.0, foreground 1.5-2.5, locked-to-camera (HUD/TV screen content) 0.")
    lastNode.setPagesOrder(['controls', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    inp = _mk_node(app, group, [("fr.inria.built-in.Input", 1)])
    if inp is not None:
        inp.setScriptName("Input1"); inp.setLabel("Card"); inp.setPosition(0, 0)
    corner = _mk_node(app, group, [("net.sf.openfx.CornerPinPlugin", 1),
                                   ("net.sf.openfx.CornerPinMaskedPlugin", 1)])
    if corner is not None:
        corner.setScriptName("CornerPin1"); corner.setLabel("Card Perspective"); corner.setPosition(0, 100)
    xform = _mk_node(app, group, [("net.sf.openfx.TransformPlugin", 1)])
    if xform is not None:
        xform.setScriptName("Transform1"); xform.setLabel("Camera Move"); xform.setPosition(0, 200)
    out = _mk_node(app, group, [("fr.inria.built-in.Output", 1)])
    if out is not None:
        out.setLabel("Output1"); out.setPosition(0, 300)

    if xform is not None:
        # translate = camera pan * depth (per axis, dims 0 and 1)
        if not _set_expr_dim(xform, "translate", "thisGroup.camPanX.get() * thisGroup.depth.get()", 0):
            _set(xform, ["translate"], 0.0, 0)
        if not _set_expr_dim(xform, "translate", "thisGroup.camPanY.get() * thisGroup.depth.get()", 1):
            _set(xform, ["translate"], 0.0, 1)
        if not _set_expr_dim(xform, "scale", "thisGroup.camZoom.get()", 0):
            _set(xform, ["scale"], 1.0, 0)
        if not _set_expr_dim(xform, "scale", "thisGroup.camZoom.get()", 1):
            _set(xform, ["scale"], 1.0, 1)
    # Perspective is fitted on the CornerPin's own to-points inside the
    # group — keyframable, deliberately not expression-locked, so a TD
    # can fit a card to a photographed plate corner-by-corner. The
    # recipe doc gives the corner math for the standard keystone move.

    if inp is not None and corner is not None:
        corner.connectInput(0, inp)
    if corner is not None and xform is not None:
        xform.connectInput(0, corner)
    if xform is not None and out is not None:
        out.connectInput(0, xform)
    elif corner is not None and out is not None:
        out.connectInput(0, corner)
    elif inp is not None and out is not None:
        out.connectInput(0, inp)
