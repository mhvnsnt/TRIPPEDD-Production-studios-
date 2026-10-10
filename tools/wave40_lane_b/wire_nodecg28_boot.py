#!/usr/bin/env python3
"""Wave 40 Lane B — NodeCG 2.8.0 broadcast-graphics boot wiring (Node 24).

Wave 39 proved NodeCG (MIT) bundle *parsing* but could not boot the full
server: nodecg 2.2.0 pins better-sqlite3@8.7.0, which ships no Node 24
(ABI 137) prebuild and cannot compile against Node 24's V8 API (hard
incompatibility, documented in tools/wave39_lane_b/nodecg_boot_attempt.log).

This lane's finding: nodecg@2.8.0 moved sqlite into
@nodecg/database-adapter-sqlite-legacy@2.7.2, which requires
better-sqlite3@^12.4.1 — and better-sqlite3 12.x ships Node 24 ABI-137
prebuilds. Result: the full NodeCG 2.8.0 server BOOTS on Node 24.

What this script does (reproduce the wiring proof):
  1. npm-installs nodecg@2.8.0 into a scratch dir (node_modules excluded
     from git — see .gitignore note in PROOFS.md),
  2. asserts better-sqlite3's native binding loads on Node 24 (the exact
     wave-39 failure point),
  3. installs the MIT trippedd-lowerthird proof bundle (from
     tools/wave39_lane_b/nodecg_bundles/, compatibleRange ^2.0.0),
  4. boots `nodecg start`, waits, and HTTP-probes:
       /bundles/trippedd-lowerthird/graphics/lowerthird.html -> 200
       /bundles/trippedd-lowerthird/dashboard/panel.html    -> 200
       /socket.io/?EIO=4&transport=polling                   -> 200
     (dashboard root 302-redirects to login by design in NodeCG 2.x)
  5. greps the server log for the extension-loaded + replicant lines.

Usage: python3 wire_nodecg28_boot.py [--scratch DIR] [--port 9090]
The script prints PASS/FAIL per gate and exits nonzero on failure.
"""
import argparse, json, os, re, shutil, signal, socket, subprocess, sys, time
import urllib.request

NODECG_VERSION = "2.8.0"
BUNDLE_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "wave39_lane_b", "nodecg_bundles",
                          "trippedd-lowerthird")

def run(cmd, cwd, timeout=600):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout)
    return p.returncode, p.stdout[-3000:], p.stderr[-3000:]

def http_probe(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "trippedd-wave40/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()[:2000]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default="/tmp/wave40-nodecg28")
    ap.add_argument("--port", type=int, default=9090)
    a = ap.parse_args()
    base = f"http://localhost:{a.port}"
    gates = {}
    print(f"[1/5] npm install nodecg@{NODECG_VERSION} -> {a.scratch}")
    os.makedirs(a.scratch, exist_ok=True)
    # NodeCG 2.8 parses the CWD as a bundle: package.json MUST have "name".
    # (npm init -y proved unreliable here, so write it explicitly.)
    pkg_path = os.path.join(a.scratch, "package.json")
    if not os.path.exists(pkg_path):
        with open(pkg_path, "w") as f:
            json.dump({"name": "wave40-nodecg-scratch", "private": True}, f)
    # NOTE (2026-10-08): plain `npm install` is flaky in this sandbox —
    # better-sqlite3's `prebuild-install || node-gyp rebuild` fallback chain
    # breaks two ways here: (a) node-gyp header-tarball extraction hits
    # EPERM fchown, (b) npm's rollback leaves a truncated package.json that
    # poisons the next attempt. Deterministic route: install with
    # --ignore-scripts (pure-JS extraction, reliable), then fetch the
    # better-sqlite3 prebuild explicitly via prebuild-install.
    nm = os.path.join(a.scratch, "node_modules")
    if not os.path.exists(os.path.join(nm, "nodecg")):
        rc, out, err = run(["npm", "install", f"nodecg@{NODECG_VERSION}",
                            "--no-audit", "--no-fund", "--ignore-scripts"],
                           a.scratch, timeout=900)
        if rc != 0:
            print("npm install FAILED"); print(out); print(err); sys.exit(1)
    # better-sqlite3 may be hoisted top-level or nested under the adapter pkg
    bs3_dir = None
    for cand in (os.path.join(nm, "better-sqlite3"),
                 os.path.join(nm, "@nodecg", "database-adapter-sqlite-legacy",
                              "node_modules", "better-sqlite3")):
        if os.path.isdir(cand):
            bs3_dir = cand
            break
    if not bs3_dir:
        print("better-sqlite3 not found under node_modules; aborting")
        sys.exit(1)
    print("    better-sqlite3 at", os.path.relpath(bs3_dir, a.scratch))
    if not os.path.exists(os.path.join(bs3_dir, "build", "Release",
                                       "better_sqlite3.node")):
        print("    fetching better-sqlite3 prebuild explicitly")
        rc, out, err = run(["npx", "--yes", "prebuild-install", "--verbose"],
                           bs3_dir, timeout=300)
        if rc != 0:
            print("prebuild-install FAILED"); print(out); print(err); sys.exit(1)
    nver = json.load(open(os.path.join(a.scratch, "node_modules", "nodecg",
                                       "package.json")))["version"]
    bver = json.load(open(os.path.join(a.scratch, "node_modules", "better-sqlite3",
                                       "package.json")))["version"]
    print(f"    nodecg {nver}, better-sqlite3 {bver}")
    gates["install"] = nver.startswith("2.8.")

    print("[2/5] better-sqlite3 native binding on Node", end=" ")
    rc, out, err = run(["node", "-e",
        "const d=require('better-sqlite3')(':memory:');"
        "d.exec('CREATE TABLE t(x)');d.prepare('INSERT INTO t VALUES(?)').run(7);"
        "if(d.prepare('SELECT x FROM t').get().x!==7)process.exit(1);"
        "console.log('NATIVE-OK')"], a.scratch, timeout=60)
    gates["sqlite_native"] = ("NATIVE-OK" in out)
    print("PASS" if gates["sqlite_native"] else f"FAIL\n{out}\n{err}")
    if not gates["sqlite_native"]:
        sys.exit(1)

    print("[3/5] install trippedd-lowerthird bundle")
    bdst = os.path.join(a.scratch, "bundles", "trippedd-lowerthird")
    if os.path.exists(bdst):
        shutil.rmtree(bdst)
    shutil.copytree(os.path.normpath(BUNDLE_SRC), bdst)
    bpkg = json.load(open(os.path.join(bdst, "package.json")))
    gates["bundle_present"] = bpkg["name"] == "trippedd-lowerthird"
    print("    bundle:", bpkg["name"], bpkg["version"], "license:", bpkg["license"])

    print("[4/5] boot nodecg server")
    log_path = os.path.join(a.scratch, "boot.log")
    logf = open(log_path, "w")
    srv = subprocess.Popen(["npx", "nodecg", "start"], cwd=a.scratch,
                           stdout=logf, stderr=subprocess.STDOUT)
    try:
        booted = False
        for _ in range(40):
            time.sleep(2)
            try:
                st, _ = http_probe(
                    base + "/bundles/trippedd-lowerthird/graphics/lowerthird.html")
                booted = (st == 200)
            except Exception:
                pass
            if booted:
                break
        gates["server_booted_graphic_200"] = booted
        print("    graphic html reachable ->", "PASS" if booted else "FAIL")
        if booted:
            try:
                st, body_g = http_probe(
                    base + "/bundles/trippedd-lowerthird/graphics/lowerthird.html")
                gates["graphic_markup"] = (st == 200 and b"Lower Third" in body_g
                                           and len(body_g) > 500)
                print("    graphic markup real ->",
                      "PASS" if gates["graphic_markup"] else "FAIL")
            except Exception as e:
                gates["graphic_markup"] = False
                print("    graphic probe error:", e)
            try:
                st, _ = http_probe(
                    base + "/bundles/trippedd-lowerthird/dashboard/panel.html")
                gates["panel_200"] = (st == 200)
                print("    dashboard panel ->", st,
                      "PASS" if gates["panel_200"] else "FAIL")
            except Exception as e:
                gates["panel_200"] = False
                print("    panel probe error:", e)
            try:
                st, _ = http_probe(base + "/socket.io/?EIO=4&transport=polling")
                gates["socketio_200"] = (st == 200)
                print("    socket.io ->", st,
                      "PASS" if gates["socketio_200"] else "FAIL")
            except Exception as e:
                gates["socketio_200"] = False
                print("    socket.io probe error:", e)
    finally:
        srv.send_signal(signal.SIGTERM)
        try:
            srv.wait(timeout=15)
        except subprocess.TimeoutExpired:
            srv.kill()
        logf.close()
    log = open(log_path, encoding="utf-8", errors="replace").read()
    gates["log_server_running"] = "NodeCG running on" in log
    gates["log_node24"] = "Running on Node.js v24" in log
    gates["log_extension_loaded"] = "trippedd-lowerthird extension loaded" in log
    gates["log_extension_mounted"] = "Mounted trippedd-lowerthird extension" in log
    gates["log_replicant_live"] = "lowerThird replicant updated" in log
    print("[5/5] log gates:", {k: v for k, v in gates.items()
                               if k.startswith("log_")})

    print("\nGATES:", json.dumps(gates, indent=1))
    failed = [k for k, v in gates.items() if not v]
    if failed:
        print("FAIL:", failed); sys.exit(1)
    print("WIRE OK: NodeCG 2.8.0 boots on Node 24 with trippedd-lowerthird bundle live.")
    manifest = {"tool": "wire_nodecg28_boot.py", "nodecg": nver,
                "better_sqlite3": bver,
                "node": subprocess.run(["node", "--version"], capture_output=True,
                                       text=True).stdout.strip(),
                "gates": gates}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "nodecg28_proof_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    sys.exit(main())
