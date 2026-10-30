# -*- coding: utf-8 -*-
# run_natron_test.py — executed INSIDE NatronRenderer (see run_test.sh).
# Builds one graph per gizmo: Read -> gizmo -> Write, renders frame 1.
# Also dumps the real parameter names of the OFX nodes the gizmos use,
# so the log grounds every param the gizmos touch. Writes results to
# $N1_OUT (default: this folder's out/).
import os
import NatronEngine

OUT = os.environ.get("N1_OUT", "/tmp/n1-test-out")
INP = os.environ.get("N1_IN", os.path.join(OUT, "test_input.png"))
os.makedirs(OUT, exist_ok=True)
logf = open(os.path.join(OUT, "natron_test_log.txt"), "w")

def log(*a):
    s = " ".join(str(x) for x in a)
    logf.write(s + "\n"); logf.flush()
    print(s)

log("NATRON_VERSION", NatronEngine.natron.getNatronVersionString())
ids = NatronEngine.natron.getPluginIDs()
for pat in ["SaturationPlugin", "GradePlugin", "MultiplyPlugin", "MergePlugin",
            "CImgBlur", "CornerPinPlugin", "TransformPlugin"]:
    log("PLUGIN_IDS", pat, [i for i in ids if pat in i])

for pid, ver in [("net.sf.openfx.SaturationPlugin", 2), ("net.sf.openfx.GradePlugin", 1),
                 ("net.sf.openfx.MultiplyPlugin", 2), ("net.sf.openfx.MergePlugin", 1),
                 ("net.sf.cimg.CImgBlur", 3), ("net.sf.openfx.CornerPinPlugin", 1),
                 ("net.sf.openfx.TransformPlugin", 1)]:
    try:
        n = app.createNode(pid, ver)
        if n is None:
            log("PARAMS", pid, ver, "NODE_NONE"); continue
        names = []
        for p in n.getParams():
            try:
                names.append(p.getScriptName())
            except Exception:
                pass
        log("PARAMS", pid, ver, names)
    except Exception as e:
        log("PARAMS", pid, ver, "FAIL", e)

def render_chain(tag, gizmo_id, knob_sets):
    try:
        read = app.createNode("fr.inria.built-in.Read", 1)
        read.getParam("filename").set(INP)
        giz = app.createNode(gizmo_id, 1)
        if giz is None:
            log("CHAIN", tag, "GIZMO_NONE", gizmo_id); return False
        for kname, kval in knob_sets:
            try:
                p = giz.getParam(kname)
                if p is not None:
                    p.setValue(kval)
                    log("CHAIN", tag, "knob", kname, "=", kval)
                else:
                    log("CHAIN", tag, "knob MISSING", kname)
            except Exception as e:
                log("CHAIN", tag, "knob FAIL", kname, e)
        giz.connectInput(0, read)
        w = app.createNode("fr.inria.built-in.Write", 1)
        outpath = os.path.join(OUT, tag + ".png")
        w.getParam("filename").set(outpath)
        w.connectInput(0, giz)
        log("CHAIN", tag, "rendering ->", outpath)
        app.render(w, 1, 1)
        ok = os.path.exists(outpath) and os.path.getsize(outpath) > 0
        log("CHAIN", tag, "OUTPUT_EXISTS", ok, outpath,
            os.path.getsize(outpath) if os.path.exists(outpath) else -1)
        return ok
    except Exception as e:
        log("CHAIN", tag, "FAIL", e)
        return False

results = {}
results["look2"] = render_chain("out_look2", "com.trippedd.CJLook2DeepSaturation", [])
results["look1"] = render_chain("out_look1", "com.trippedd.CJLook1PaleWash", [])
results["led_purple"] = render_chain("out_led_purple", "com.trippedd.CJLedDeepPurpleGlow", [])
results["led_party"] = render_chain("out_led_party", "com.trippedd.CJLedPartyGlow", [])
results["card"] = render_chain("out_card", "com.trippedd.TrippeddCard25D",
                               [("camPanX", 40.0), ("depth", 1.0), ("camZoom", 1.0)])
log("RESULTS", results)
logf.close()
