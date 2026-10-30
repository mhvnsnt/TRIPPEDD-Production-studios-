# -*- coding: utf-8 -*-
# run_donor_test.py - executed INSIDE NatronRenderer.
# Verifies the adopted community donor PM_Card3D + PM_Camera load in
# Natron 2.5.0 and that a card renders through PM_Card3D.
import os
OUT = os.environ.get("N1_OUT", "/tmp/n1-test-out")
INP = os.environ.get("N1_IN", os.path.join(OUT, "test_input.png"))
logf = open(os.path.join(OUT, "donor_test_log.txt"), "w")
def log(*a):
    s = " ".join(str(x) for x in a); logf.write(s + "\n"); logf.flush(); print(s)
import NatronEngine
ids = NatronEngine.natron.getPluginIDs()
log("DONOR_IN_PLUGIN_IDS PM_Card3D", "natron.community.plugins.PM_Card3D" in ids)
log("DONOR_IN_PLUGIN_IDS PM_Camera", "natron.community.plugins.PM_Camera" in ids)
cam = None
try:
    cam = app.createNode("natron.community.plugins.PM_Camera", 1)
    log("PM_Camera CREATE", cam is not None)
    if cam is not None:
        log("PM_Camera LABEL", cam.getLabel())
except Exception as e:
    log("PM_Camera CREATE FAIL", e)
try:
    read = app.createNode("fr.inria.built-in.Read", 1)
    read.getParam("filename").set(INP)
    card = app.createNode("natron.community.plugins.PM_Card3D", 1)
    log("PM_Card3D CREATE", card is not None)
    if card is not None:
        log("PM_Card3D LABEL", card.getLabel())
        log("PM_Card3D NINPUTS", card.getMaxInputCount() if hasattr(card, "getMaxInputCount") else "n/a")
        card.connectInput(0, read)
        if cam is not None:
            for i in range(1, 4):
                try:
                    if card.connectInput(i, cam):
                        log("PM_Card3D CAMERA_CONNECTED_ON_INPUT", i); break
                except Exception as e:
                    log("PM_Card3D connectInput", i, "fail", e)
        w = app.createNode("fr.inria.built-in.Write", 1)
        outpath = os.path.join(OUT, "out_donor_card.png")
        w.getParam("filename").set(outpath)
        w.connectInput(0, card)
        app.render(w, 1, 1)
        ok = os.path.exists(outpath) and os.path.getsize(outpath) > 0
        log("PM_Card3D RENDER_OUTPUT_EXISTS", ok, outpath, os.path.getsize(outpath) if os.path.exists(outpath) else -1)
except Exception as e:
    log("PM_Card3D CHAIN FAIL", e)
logf.close()
