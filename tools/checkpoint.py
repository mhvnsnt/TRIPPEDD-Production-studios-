"""
IMMUTABLE CHECKPOINTS, AND AN EXPLICIT PROMOTION STEP.

    "don't let this repair overwrite yesterday's known-good oral donor again.
     The donor and the canonical MARS head need separate immutable checkpoints,
     with an explicit promotion step."

The GNM oral donor is INPUT. The canonical head is a WORKING ARTIFACT that tools
save over in place -- rig_face.py writes straight to assets/rigs/MARS_FACE.blend,
which is how the good mouth was lost under the eye work in the first place.
Those two things need different protection, so they get separate checkpoints.

A checkpoint is content-addressed and REFUSES TO BE OVERWRITTEN. Restoring is a
separate, named command, so nothing is ever recovered by accident and nothing is
ever silently replaced.

    python tools/checkpoint.py save  before-mouth-retopo
    python tools/checkpoint.py list
    python tools/checkpoint.py verify before-mouth-retopo
    python tools/checkpoint.py restore before-mouth-retopo --yes
"""
import argparse, hashlib, json, os, shutil, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STORE = os.path.join(ROOT, "assets/checkpoints")

# what a checkpoint covers, and why it is in the list
TRACKED = [
    ("rig", "assets/rigs/MARS_FACE.blend",
     "the canonical head -- tools save over this IN PLACE, which is how the good mouth "
     "was lost under the eye work"),
    ("rig", "assets/rigs/MARS_FACE.glb", "the exported head"),
    ("rig", "assets/rigs/MARS_ORAL.blend", "the carved-cavity head the face rig is built from"),
    ("donor", "assets/donor/gnm_oral", "the Google GNM oral donor (Apache-2.0) -- INPUT, "
     "never a working artifact"),
    ("measure", "renders/_rig_measure/mouth_anatomy.json", "his measured mouth frame"),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def files_of(rel):
    a = os.path.join(ROOT, rel)
    if os.path.isfile(a):
        return [rel]
    if os.path.isdir(a):
        out = []
        for d, _, fs in os.walk(a):
            for f in sorted(fs):
                out.append(os.path.relpath(os.path.join(d, f), ROOT))
        return out
    return []


def save(label, note):
    dest = os.path.join(STORE, label)
    if os.path.exists(dest):
        print("*** REFUSED: checkpoint %r already exists. A checkpoint is immutable; "
              "pick another label." % label)
        return 1
    man = {"label": label, "note": note, "savedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "files": []}
    n = 0
    for kind, rel, why in TRACKED:
        for f in files_of(rel):
            src = os.path.join(ROOT, f)
            dst = os.path.join(dest, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            man["files"].append({"kind": kind, "path": f, "sha256": sha256(src),
                                 "bytes": os.path.getsize(src), "why": why})
            n += 1
    os.makedirs(dest, exist_ok=True)
    json.dump(man, open(os.path.join(dest, "manifest.json"), "w"), indent=2)
    tot = sum(x["bytes"] for x in man["files"])
    print("checkpoint %r: %d files, %.1f MB -> %s" % (label, n, tot / 1e6,
                                                      os.path.relpath(dest, ROOT)))
    for x in man["files"]:
        print("  %-8s %-46s %s" % (x["kind"], x["path"], x["sha256"][:12]))
    return 0


def listing():
    if not os.path.isdir(STORE):
        print("no checkpoints yet"); return 0
    for label in sorted(os.listdir(STORE)):
        mp = os.path.join(STORE, label, "manifest.json")
        if not os.path.exists(mp): continue
        m = json.load(open(mp))
        print("%-32s %s  %d files  %s" % (label, m["savedAt"], len(m["files"]),
                                          m.get("note", "")))
    return 0


def verify(label):
    m = json.load(open(os.path.join(STORE, label, "manifest.json")))
    bad = 0
    for x in m["files"]:
        stored = os.path.join(STORE, label, x["path"])
        if not os.path.exists(stored):
            print("MISSING from the checkpoint: %s" % x["path"]); bad += 1; continue
        if sha256(stored) != x["sha256"]:
            print("CHECKPOINT CORRUPT: %s" % x["path"]); bad += 1; continue
        live = os.path.join(ROOT, x["path"])
        state = "gone" if not os.path.exists(live) else (
            "same" if sha256(live) == x["sha256"] else "CHANGED since the checkpoint")
        print("  %-46s %s" % (x["path"], state))
    print("checkpoint %r: %s" % (label, "intact" if bad == 0 else "%d PROBLEM(S)" % bad))
    return 1 if bad else 0


def restore(label, yes):
    m = json.load(open(os.path.join(STORE, label, "manifest.json")))
    if not yes:
        print("would restore %d files from %r. Pass --yes to do it." % (len(m["files"]), label))
        for x in m["files"]:
            print("  %s" % x["path"])
        return 2
    for x in m["files"]:
        src = os.path.join(STORE, label, x["path"])
        if sha256(src) != x["sha256"]:
            print("*** REFUSED: %s in the checkpoint no longer matches its hash" % x["path"])
            return 1
        dst = os.path.join(ROOT, x["path"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print("  restored %s" % x["path"])
    print("restored %r" % label)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["save", "list", "verify", "restore"])
    ap.add_argument("label", nargs="?")
    ap.add_argument("--note", default="")
    ap.add_argument("--yes", action="store_true")
    a = ap.parse_args()
    if a.action == "list": return listing()
    if not a.label:
        print("a label is required"); return 2
    if a.action == "save": return save(a.label, a.note)
    if a.action == "verify": return verify(a.label)
    return restore(a.label, a.yes)


if __name__ == "__main__":
    raise SystemExit(main())
