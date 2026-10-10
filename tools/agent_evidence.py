"""
ONE COMMAND FOR ANY AGENT TO SHOW ITS WORK — and it cannot be faked.

Owner: "make it so they can show me previews and stuff and all that while they do
the work just like how you do or at least bring artifacts to me... they always
tell me what they can't do, but I know there's a way for stuff in the repo to
connect to the thing to give them abilities."

docs/agent-evidence/ already defines the contract (trippedd.agent-evidence/v1).
Nothing WROTE one, and nothing CHECKED one, so it was a schema with no teeth --
an agent could still say "the preview is ready" and move on.

This is the teeth. It computes the hashes itself from bytes on disk, so an agent
cannot assert a file it does not have, and it REFUSES rather than writing a
manifest that claims more than it can show:

  * an artifact path that does not exist            -> REFUSED
  * an artifact outside the repository              -> REFUSED
  * status PASS with no gates at all                -> REFUSED
      (a gate with zero checks reports 0/0 PASS -- that is a documented bug class
       in this repo, not a hypothetical)
  * status PASS while any gate says FAIL            -> REFUSED
  * --visual work with no image or video artifact   -> REFUSED
      (the contract makes a preview mandatory for visual work; this enforces it)

WRITE (any agent, any model):
  ./.trippedd_venv/bin/python tools/agent_evidence.py \
      --agent chatgpt --status PASS --visual \
      --artifact docs/evidence/quality/MARS_quality_SOURCE.png \
      --gate "rest_drift=PASS:max 0.0026 mm" \
      --command "vendor/blender/blender -b -P tools/models/upgrade_render_mesh.py --" \
      --note "bound the full source mesh to the rigged cage"

VALIDATE EVERYTHING (CI, or any agent checking another's claim):
  ./.trippedd_venv/bin/python tools/agent_evidence.py --validate
"""
import json, os, sys, glob, hashlib, subprocess, time, mimetypes

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANI = os.path.join(ROOT, "docs", "agent-evidence", "manifests")
SCHEMA = os.path.join(ROOT, "docs", "agent-evidence", "evidence_manifest.schema.json")
IMAGEY = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm", ".mov")

argv = sys.argv[1:]
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.exit(1)
def opts(flag):
    return [argv[i + 1] for i, a in enumerate(argv) if a == flag and i + 1 < len(argv)]
def opt(flag, default=None):
    v = opts(flag); return v[0] if v else default
def has(flag): return flag in argv


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "UNKNOWN"


def describe(rel):
    """Hash and size an artifact FROM ITS BYTES. An agent never supplies these."""
    p = os.path.abspath(os.path.join(ROOT, rel))
    if not p.startswith(ROOT + os.sep):
        die("artifact %r is outside the repository -- every other agent has to be able "
            "to retrieve it from a plain checkout" % rel)
    if not os.path.isfile(p):
        die("artifact %r does not exist. This is the whole point of the tool: "
            "'the preview is ready' without retrievable bytes is NOT_ATTEMPTED, "
            "never PASS (OWNER LAW #2)." % rel)
    if os.path.getsize(p) == 0:
        die("artifact %r is zero bytes" % rel)
    return {"path": os.path.relpath(p, ROOT).replace(os.sep, "/"),
            "sha256": sha256(p), "bytes": os.path.getsize(p),
            "mime": mimetypes.guess_type(p)[0] or "application/octet-stream"}


def parse_gate(s):
    # "name=RESULT:detail"  /  "name=RESULT"
    if "=" not in s: die("gate %r must look like name=PASS or name=FAIL:detail" % s)
    name, rest = s.split("=", 1)
    result, _, detail = rest.partition(":")
    result = result.strip().upper()
    if result not in ("PASS", "FAIL", "UNKNOWN", "NOT_ATTEMPTED"):
        die("gate %r result must be PASS, FAIL, UNKNOWN or NOT_ATTEMPTED" % s)
    g = {"name": name.strip(), "result": result}
    if detail.strip(): g["detail"] = detail.strip()
    return g


def validate(man, where):
    """Re-check a manifest against the bytes on disk. Returns a list of problems."""
    bad = []
    if man.get("schema") != "trippedd.agent-evidence/v1":
        bad.append("schema is %r, expected trippedd.agent-evidence/v1" % man.get("schema"))
    st = man.get("status")
    if st not in ("PASS", "FAIL", "UNKNOWN", "IN_PROGRESS"):
        bad.append("status %r is not one of PASS/FAIL/UNKNOWN/IN_PROGRESS" % st)
    gates = man.get("gates") or []
    if st == "PASS" and not gates:
        bad.append("status PASS with zero gates -- asserts nothing")
    for g in gates:
        if st == "PASS" and g.get("result") == "FAIL":
            bad.append("status PASS while gate %r FAILED" % g.get("name"))
    arts = man.get("artifacts") or []
    for a in arts:
        p = os.path.join(ROOT, a.get("path", ""))
        if not os.path.isfile(p):
            bad.append("artifact %r is named but MISSING from the checkout" % a.get("path"))
            continue
        if os.path.getsize(p) != a.get("bytes"):
            bad.append("artifact %r is %d bytes, manifest says %s"
                       % (a["path"], os.path.getsize(p), a.get("bytes")))
        elif sha256(p) != a.get("sha256"):
            bad.append("artifact %r sha256 does not match the manifest" % a["path"])
    return bad


# ---------------------------------------------------------------- validate mode
if has("--validate"):
    files = sorted(glob.glob(os.path.join(MANI, "*.json")))
    if not files:
        print("no agent manifests yet in %s" % os.path.relpath(MANI, ROOT))
        print("that is NOT_ATTEMPTED, not PASS -- nothing has been claimed here")
        sys.exit(0)
    fails = 0
    for f in files:
        try:
            man = json.load(open(f))
        except Exception as e:
            print("INVALID JSON  %s  (%s)" % (os.path.relpath(f, ROOT), e)); fails += 1; continue
        bad = validate(man, f)
        tag = "OK    " if not bad else "FAIL  "
        print("%s%-46s agent=%-14s status=%-11s artifacts=%d"
              % (tag, os.path.relpath(f, ROOT), man.get("agent"), man.get("status"),
                 len(man.get("artifacts") or [])))
        for b in bad:
            print("        - %s" % b); fails += 1
    print("\n%d manifest(s), %d problem(s)" % (len(files), fails))
    sys.exit(1 if fails else 0)

# ---------------------------------------------------------------- write mode
agent = opt("--agent")
status = (opt("--status") or "").upper()
if not agent: die("--agent is required (chatgpt | claude | grok | replit | jules | ...)")
if status not in ("PASS", "FAIL", "UNKNOWN", "IN_PROGRESS"):
    die("--status must be PASS, FAIL, UNKNOWN or IN_PROGRESS (got %r)" % status)

arts = [describe(a) for a in opts("--artifact")]
gates = [parse_gate(g) for g in opts("--gate")]
cmds = opts("--command")
notes = opts("--note")

if status == "PASS" and not gates:
    die("status PASS with no --gate. A gate with zero checks reports 0/0 PASS, which "
        "is a bug class this repo has hit before. State what was checked.")
for g in gates:
    if status == "PASS" and g["result"] == "FAIL":
        die("status PASS while gate %r FAILED. VISUAL_FAIL outranks a passing physical "
            "gate, and a failing gate outranks a hopeful status." % g["name"])
if has("--visual") and not any(a["path"].lower().endswith(IMAGEY) for a in arts):
    die("--visual work with no image or video artifact. The contract makes a preview "
        "mandatory for visual/model/animation work -- a status page is not a preview.")
if status == "PASS" and not arts:
    die("status PASS with no --artifact. Published or it does not exist (OWNER LAW #2).")

os.makedirs(MANI, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
out = opt("--out", os.path.join(MANI, "%s-%s.json" % (agent.lower(), stamp)))
man = {
    "schema": "trippedd.agent-evidence/v1",
    "agent": agent, "commit": commit(), "status": status,
    "created": stamp,
    "artifacts": arts, "commands": cmds, "gates": gates, "notes": notes,
}
bad = validate(man, out)
if bad: die("the manifest this tool just built does not validate: %s" % "; ".join(bad))
json.dump(man, open(out, "w"), indent=2)
print("manifest -> %s" % os.path.relpath(out, ROOT))
print("  agent %s  status %s  %d artifact(s)  %d gate(s)" % (agent, status, len(arts), len(gates)))
for a in arts:
    print("    %s  %d bytes  %s" % (a["path"], a["bytes"], a["sha256"][:16]))
print("\nit is now visible to every other agent, and "
      "`--validate` re-checks these hashes against the checkout.")
