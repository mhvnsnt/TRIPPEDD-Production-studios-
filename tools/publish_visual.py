"""
NO BYTES = NO EVIDENCE. THE REPOSITORY IS THE SHARED VISUAL EVIDENCE BUS.

    "Claude should be dropping the visual results in the repo for you to see, so
     you can stop asking me for the images."          -- the owner, 2026-09-13

Every meaningful render lands in the repo with its bytes, its sha256, and enough
provenance for another agent -- ChatGPT, Rocket, a CI runner -- to find it, trust
it, and reproduce it, without a human carrying a screenshot between tools.

  * NOTHING IS EVER OVERWRITTEN. Filenames are deterministic and versioned, so an
    A/B keeps both halves and yesterday's known-good reference stays immutable.
  * A sidecar records the source .blend and ITS hash, the producing tool and
    commit, Blender version, camera, view transform, what was shown or hidden,
    the measurements, and a PASS / FAIL / UNAVAILABLE status.
  * docs/evidence/VISUAL_EVIDENCE_INDEX.json is append-only history.
  * docs/evidence/LATEST_VISUAL_EVIDENCE.json points at what is current.
  * A claim is only written AFTER the bytes are on disk and hashed. UNKNOWN is
    never PASS.

    python tools/publish_visual.py --src renders/_x/frame.png --set mars/mouth \
        --label after_remesh --source-blend assets/rigs/MARS_FACE.blend \
        --status PASS --note "..." --measure key=value
"""
import argparse, hashlib, json, os, shutil, subprocess, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
EV = os.path.join(ROOT, "docs/evidence")
INDEX = os.path.join(EV, "VISUAL_EVIDENCE_INDEX.json")
LATEST = os.path.join(EV, "LATEST_VISUAL_EVIDENCE.json")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def git(*args):
    try:
        return subprocess.check_output(["git", "-C", ROOT] + list(args),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""


def png_size(p):
    try:
        with open(p, "rb") as f:
            d = f.read(33)
        if d[:8] == b"\x89PNG\r\n\x1a\n":
            return [int.from_bytes(d[16:20], "big"), int.from_bytes(d[20:24], "big")]
    except Exception:
        pass
    return None


def next_version(dest_dir, label, ext):
    n = 1
    while os.path.exists(os.path.join(dest_dir, "%s.v%03d%s" % (label, n, ext))):
        n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--set", required=True, help="e.g. mars/mouth, mars/topology, mars/a_b")
    ap.add_argument("--label", required=True)
    ap.add_argument("--source-blend", default="")
    ap.add_argument("--tool", default="")
    ap.add_argument("--status", default="UNAVAILABLE",
                    choices=["PASS", "FAIL", "PENDING", "UNAVAILABLE"])
    ap.add_argument("--note", default="")
    ap.add_argument("--camera", default="")
    ap.add_argument("--view-transform", default="")
    ap.add_argument("--shown", default="")
    ap.add_argument("--hidden", default="")
    ap.add_argument("--blender", default="")
    ap.add_argument("--measure", action="append", default=[])
    ap.add_argument("--latest-key", default="", help="what this becomes the current answer for")
    a = ap.parse_args()

    src = os.path.abspath(a.src)
    if not os.path.exists(src) or os.path.getsize(src) == 0:
        print("*** REFUSED: %s has no bytes. NO BYTES = NO EVIDENCE." % a.src)
        return 1

    dest_dir = os.path.join(EV, a.set)
    os.makedirs(dest_dir, exist_ok=True)
    ext = os.path.splitext(src)[1] or ".png"
    v = next_version(dest_dir, a.label, ext)
    name = "%s.v%03d%s" % (a.label, v, ext)
    dst = os.path.join(dest_dir, name)
    shutil.copy2(src, dst)                     # never overwrite: v001, v002, ...

    digest = sha256(dst)
    if digest != sha256(src):
        print("*** REFUSED: the copy does not hash the same as the source")
        os.remove(dst)
        return 1

    rec = {
        "artifact": os.path.relpath(dst, ROOT),
        "sha256": digest,
        "bytes": os.path.getsize(dst),
        "resolution": png_size(dst),
        "set": a.set, "label": a.label, "version": v,
        "producedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "producingTool": a.tool,
        "producingCommit": git("rev-parse", "HEAD"),
        "producingBranch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "blenderVersion": a.blender,
        "camera": a.camera, "viewTransform": a.view_transform,
        "shown": [s for s in a.shown.split(",") if s],
        "hidden": [s for s in a.hidden.split(",") if s],
        "status": a.status, "note": a.note,
        "measurements": dict(kv.split("=", 1) for kv in a.measure if "=" in kv),
    }
    if a.source_blend:
        sb = os.path.join(ROOT, a.source_blend)
        rec["sourceArtifact"] = a.source_blend
        rec["sourceSha256"] = sha256(sb) if os.path.exists(sb) else "MISSING"
    json.dump(rec, open(dst + ".json", "w"), indent=2)

    idx = json.load(open(INDEX)) if os.path.exists(INDEX) else {
        "schema": "trippedd.visual-evidence-index/v1",
        "law": "NO BYTES = NO EVIDENCE. UNKNOWN IS NEVER PASS. Append-only.",
        "entries": []}
    idx["entries"].append(rec)
    json.dump(idx, open(INDEX, "w"), indent=2)

    key = a.latest_key or ("%s/%s" % (a.set, a.label))
    lat = json.load(open(LATEST)) if os.path.exists(LATEST) else {
        "schema": "trippedd.latest-visual-evidence/v1",
        "purpose": "what any agent should look at NOW, per question. The repository is "
                   "the shared evidence bus -- no human carries images between tools.",
        "current": {}}
    lat["current"][key] = rec
    lat["updatedAt"] = rec["producedAt"]
    json.dump(lat, open(LATEST, "w"), indent=2)

    print("published %s  %s  %d bytes  %s"
          % (rec["artifact"], digest[:12], rec["bytes"], a.status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
