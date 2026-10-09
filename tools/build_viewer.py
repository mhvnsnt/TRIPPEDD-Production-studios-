"""
BUILD THE PRODUCTION VIEWER — the window everyone watches the work through.

Regenerable on purpose. Any agent re-runs this after a render and republishes,
so the viewer is never a hand-made one-off that drifts from the evidence. It
reads docs/evidence/<set>/index.json (the manifest OWNER LAW #2 requires) and
emits a single self-contained page; the frames themselves ship alongside it as
published files, so what the page shows IS the committed artifact.

  .trippedd_venv/bin/python tools/build_viewer.py --set mouth --out <path>.html
"""
import json, os, sys

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
SET = opt("--set", "mouth")
SRC = os.path.abspath(os.path.join("docs", "evidence", SET))
OUT = os.path.abspath(opt("--out", "/tmp/mars_viewer.html"))

idx = json.load(open(os.path.join(SRC, "index.json")))
proof_name = next((m for m in idx["measurements"] if "proof" in m), None)
proof = json.load(open(os.path.join(SRC, proof_name))) if proof_name else {"poses": [], "checks": []}

poses, cams = [], []
for f in idx["frames"]:
    if f["pose"] not in poses: poses.append(f["pose"])
    if f["camera"] not in cams: cams.append(f["camera"])
cams = [c for c in ("front", "mouth", "profile") if c in cams] + [c for c in cams if c not in ("front", "mouth", "profile")]

DATA = {
    "set": SET,
    "sourceAsset": idx.get("sourceAsset", {}),
    "qc": idx.get("qc", {}),
    "poses": poses, "cameras": cams,
    "frames": {"%s|%s" % (f["pose"], f["camera"]): {"src": f["frame"], "sha": f["sha256"][:12],
               "px": f["renderedPx"], "repoPath": f["repoPath"]} for f in idx["frames"]},
    "measured": {p["pose"]: {"jaw": p["jawDeg"], "gap": p["lipGapPercentOfHeadHeight"],
                             "vis": p["visible"], "shapes": p.get("shapes", {})}
                 for p in proof.get("poses", [])},
    "checks": proof.get("checks", []),
    "engine": proof.get("engine"), "samples": proof.get("samples"),
}

HTML = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "viewer_template.html")).read()
open(OUT, "w").write(HTML.replace("/*__DATA__*/null", json.dumps(DATA, indent=1)))
print("viewer -> %s  (%d frames, %d poses, %d cameras)" % (OUT, len(idx["frames"]), len(poses), len(cams)))
print("publish alongside: " + " ".join(f["frame"] for f in idx["frames"]))
