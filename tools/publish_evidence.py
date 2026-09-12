"""
PUBLISH EVIDENCE — so every other agent has EYES.

renders/ is gitignored, on purpose: it is regenerable and it is large. The
consequence nobody accounted for is that a frame I render is visible to exactly
one process on one container. Grok, ChatGPT, Gemini, AI Studio and every CI
runner see an empty repository where the proof should be, and the only thing
they can do is take a text summary on trust. That is the same failure as a
worker reporting MARS_CANDIDATES: NONE while the file sits on someone's disk.

So: derived frames stay ignored, and a DOWNSCALED, committed copy of the ones
that are evidence goes to docs/evidence/<set>/ with the measurement that
produced it, plus an index a human or an agent can read on GitHub directly.

  .trippedd_venv/bin/python tools/publish_evidence.py --src renders/_mouth_proof --set mouth
"""
import json, os, sys, glob, shutil, hashlib

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
SRC = os.path.abspath(opt("--src", "renders/_mouth_proof"))
SET = opt("--set", os.path.basename(SRC).lstrip("_"))
MAXPX = int(opt("--max", "900"))
DEST = os.path.abspath(os.path.join("docs", "evidence", SET))
os.makedirs(DEST, exist_ok=True)

from PIL import Image

VISUAL = opt("--visual", os.environ.get("TRIPPEDD_VISUAL_VERDICT", "PENDING")).upper()
if VISUAL not in ("PASS", "FAIL", "PENDING"):
    sys.exit("--visual must be PASS, FAIL or PENDING")

SOURCE_ASSET = {}
_prov = os.path.join("assets", "source_models", "MARS_source.provenance.json")
if os.path.exists(_prov):
    _p = json.load(open(_prov))
    SOURCE_ASSET = {"assetId": _p.get("assetId"), "character": _p.get("character"),
                    "sha256": _p.get("integrity", {}).get("sha256"),
                    "driveFileId": _p.get("source", {}).get("fileId")}

def sha_full(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

def sha8(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()[:8]

published = []
for p in sorted(glob.glob(os.path.join(SRC, "*.png"))):
    im = Image.open(p).convert("RGB")
    if max(im.size) > MAXPX:
        r = MAXPX / max(im.size)
        im = im.resize((int(im.size[0] * r), int(im.size[1] * r)), Image.LANCZOS)
    name = os.path.basename(p)
    out = os.path.join(DEST, name)
    # BEFORE/AFTER. Keep the frame this one replaces, so a viewer can see what
    # changed instead of being told. Without it every re-render silently
    # overwrites the only copy of the thing you were comparing against.
    prev_dir = os.path.join(DEST, "prev")
    if os.path.exists(out):
        old = sha_full(out)
        os.makedirs(prev_dir, exist_ok=True)
        Image.open(out).convert("RGB").save(os.path.join(prev_dir, name), "PNG", optimize=True)
    im.save(out, "PNG", optimize=True)
    # The manifest has to answer every question another agent could ask WITHOUT
    # anyone hunting through temp directories: what it is, where it is, whether
    # the pixels are the ones that were measured, and what the measurement said.
    pose, _, cam = name.rsplit(".", 1)[0].rpartition("_")
    # The SOURCE hash proves which render this came from; the PUBLISHED hash is
    # what a viewer can actually verify, because publishing re-encodes the PNG
    # and the bytes therefore differ from the production file by design.
    published.append({
        "frame": name,
        "publishedSha256": sha_full(out),
        "repoPath": os.path.relpath(out, os.getcwd()),
        "productionPath": os.path.relpath(p, os.getcwd()),
        "sha256": sha_full(p),
        "sourceSha8": sha8(p),
        "bytes": os.path.getsize(out),
        "renderedPx": list(Image.open(p).size),
        "publishedPx": list(im.size),
        "pose": pose, "camera": cam,
        "aliases": [name.rsplit(".", 1)[0],
                    "%s_%s" % (pose.split("_", 1)[-1].lower(), cam),
                    "%s_%s" % (pose.split("_", 1)[0], cam)],
        "sourceAsset": SOURCE_ASSET,
        "prev": ("prev/" + name) if os.path.exists(os.path.join(DEST, "prev", name)) else None,
    })

measurements = {}
for j in glob.glob(os.path.join(SRC, "*.json")):
    shutil.copy2(j, DEST)
    measurements[os.path.basename(j)] = json.load(open(j))

lines = ["# Evidence — %s\n" % SET,
         "Rendered frames and the measurements that produced them, committed so that",
         "**every agent and every CI runner can see them**, not just the container that",
         "made them. `renders/` stays gitignored; these are downscaled copies with the",
         "source hash recorded, published by `tools/publish_evidence.py`.\n",
         "| frame | source sha256[:8] | rendered |", "|---|---|---|"]
for f in published:
    lines.append("| `%s` | `%s` | %dx%d |" % (f["frame"], f["sourceSha8"], *f["renderedPx"]))

mp = measurements.get("mouth_proof.json")
if mp:
    lines += ["\n## Measured, per pose\n",
              "Rays are fired at the mouth and classified by the MATERIAL each one lands on.",
              "Material identity cannot be fooled by a hole in the wrong place; a plane test can.\n",
              "| pose | jaw | lip gap (% head height) | skin | cavity | teeth | gum | tongue |",
              "|---|---|---|---|---|---|---|---|"]
    for r in mp["poses"]:
        v = r["visible"]
        lines.append("| %s | %.0f° | %.2f%% | %.1f | %.1f | %.1f | %.1f | %.1f |"
                     % (r["pose"], r["jawDeg"], r["lipGapPercentOfHeadHeight"],
                        v["skin"], v["cavity"], v["teeth"], v["gum"], v["tongue"]))
    lines += ["\n## Gate\n", "| check | result | detail |", "|---|---|---|"]
    for c in mp["checks"]:
        lines.append("| %s | %s | %s |" % (c["check"], "PASS" if c["pass"] else "**FAIL**", c["detail"]))
    lines.append("\n**Physical gate: %s** — %d of %d checks pass.\n"
                 % ("PASS" if mp["verified"] else "FAIL",
                    sum(1 for c in mp["checks"] if c["pass"]), len(mp["checks"])))
    lines.append("**Visual gate: %s.** A passing physical gate is not a passing model — "
                 "these exact numbers went green on a frame whose crowns still read as "
                 "separate pegs. VISUAL_FAIL outranks the measurements; PENDING is not "
                 "PASS.\n" % VISUAL)

for f in sorted(set(x["frame"] for x in published)):
    lines.append("\n### %s\n\n![%s](%s)\n" % (f.rsplit(".", 1)[0].replace("_", " "), f, f))

open(os.path.join(DEST, "README.md"), "w").write("\n".join(lines) + "\n")
gate = measurements.get("mouth_proof.json", {})
json.dump({
    "set": SET,
    "publishedBy": "tools/publish_evidence.py",
    "retrieve": "docs/evidence/%s/<frame>  (committed; also listed in README.md)" % SET,
    "runId": os.environ.get("GITHUB_RUN_ID") or os.environ.get("TRIPPEDD_RUN_ID") or "local",
    "sourceAsset": SOURCE_ASSET,
    # TWO GATES, AND THE PHYSICAL ONE ALONE IS NOT A PASS.
    # Measured 13.5% teeth / 21.8% tongue / 13.7% cavity with every physical
    # check green, on a frame where the crowns still read as separate pegs and
    # the cavity still showed a hard rim. A metric that cannot express the
    # failure is not evidence that the failure is absent. The visual verdict is
    # PENDING until a human or a vision agent records one against THESE pixels,
    # and overall status is the AND of the two.
    "qc": {
        "physical": {"verified": gate.get("verified"),
                     "checks": gate.get("checks", []),
                     "engine": gate.get("engine"), "samples": gate.get("samples")},
        "visual": {"verdict": VISUAL, "reviewer": os.environ.get("TRIPPEDD_VISUAL_REVIEWER", ""),
                   "notes": os.environ.get("TRIPPEDD_VISUAL_NOTES", ""),
                   "rule": "VISUAL_FAIL outranks a passing physical gate. "
                           "PENDING is not PASS."},
        "status": ("PASS" if (gate.get("verified") and VISUAL == "PASS")
                   else "VISUAL_FAIL" if VISUAL == "FAIL"
                   else "PHYSICAL_PASS_VISUAL_PENDING" if gate.get("verified")
                   else "FAIL"),
    },
    "frames": published,
    "measurements": sorted(measurements),
}, open(os.path.join(DEST, "index.json"), "w"), indent=2)
print("published %d frames + %d measurement files -> %s"
      % (len(published), len(measurements), DEST))
