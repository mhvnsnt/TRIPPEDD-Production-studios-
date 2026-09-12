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
    im.save(out, "PNG", optimize=True)
    published.append({"frame": name, "bytes": os.path.getsize(out),
                      "sourceSha8": sha8(p), "renderedPx": list(Image.open(p).size)})

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
    lines.append("\n**%s** — %d of %d checks pass.\n"
                 % ("MOUTH_ANATOMY_VERIFIED" if mp["verified"] else "NOT VERIFIED",
                    sum(1 for c in mp["checks"] if c["pass"]), len(mp["checks"])))

for f in sorted(set(x["frame"] for x in published)):
    lines.append("\n### %s\n\n![%s](%s)\n" % (f.rsplit(".", 1)[0].replace("_", " "), f, f))

open(os.path.join(DEST, "README.md"), "w").write("\n".join(lines) + "\n")
json.dump({"set": SET, "frames": published, "measurements": sorted(measurements)},
          open(os.path.join(DEST, "index.json"), "w"), indent=2)
print("published %d frames + %d measurement files -> %s"
      % (len(published), len(measurements), DEST))
