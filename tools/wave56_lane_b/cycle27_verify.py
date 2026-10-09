#!/usr/bin/env python3
"""Wave 56 Lane B — re-verification cycle 27 (rows 281-290) + drift watch.
Fresh upstream checks: repo existence/archived/pushed_at/owner, GitHub API
spdx_id, Codeberg API, raw license-file fetches (HTTP 200). No assumptions.
Run from repo worktree; results -> /tmp/cycle27_results.json"""
import json, subprocess, base64, sys

UA = "cycle27-verify/1.0"
OUT = "/tmp/cycle27_results.json"

def curl_json(url):
    r = subprocess.run(["curl", "-sS", "-A", UA, "-w", "\n%{http_code}", url],
                       capture_output=True, text=True, timeout=60)
    *body, code = r.stdout.rsplit("\n", 1)
    return int(code), "\n".join(body)

def curl_bytes(url):
    r = subprocess.run(["curl", "-sS", "-A", UA, "-o", "-", "-w", "\n%{http_code}", url],
                       capture_output=True, timeout=60)
    blob = r.stdout
    *data, code = blob.rsplit(b"\n", 1)
    return int(code), b"\n".join(data)

def gh_repo(owner_repo):
    code, body = curl_json(f"https://api.github.com/repos/{owner_repo}")
    j = json.loads(body) if code == 200 else {}
    lic = (j.get("license") or {})
    return {"http": code, "archived": j.get("archived"),
            "pushed_at": j.get("pushed_at"), "owner": (j.get("owner") or {}).get("login"),
            "spdx": lic.get("spdx_id"), "default_branch": j.get("default_branch")}

def gh_license_raw(owner_repo):
    """Fetch the repo's detected license file content (raw text + path + size)."""
    code, body = curl_json(f"https://api.github.com/repos/{owner_repo}/license")
    if code != 200:
        return {"http": code}
    j = json.loads(body)
    try:
        text = base64.b64decode(j.get("content", "")).decode("utf-8", "replace")
    except Exception:
        text = "<binary/decode-fail>"
    return {"http": 200, "path": j.get("path"), "size": len(text.encode()),
            "spdx": j.get("license", {}).get("spdx_id"), "text": text}

def codeberg_repo(owner_repo):
    code, body = curl_json(f"https://codeberg.org/api/v1/repos/{owner_repo}")
    j = json.loads(body) if code == 200 else {}
    return {"http": code, "archived": j.get("archived"),
            "updated": j.get("updated_at"), "owner": j.get("owner", {}).get("login") if isinstance(j.get("owner"), dict) else None,
            "default_branch": j.get("default_branch")}

ROWS = [
    # (row, name, owner/repo, claimed_license)
    (281, "PSn00bSDK", "Lameguy64/PSn00bSDK", "MPL-2.0"),
    (282, "mkpsxiso", "Lameguy64/mkpsxiso", "GPL-2.0"),
    (283, "WLA DX", "vhelin/wla-dx", "GPL-2.0-or-later"),
    (284, "batari Basic", "batari-Basic/batari-Basic", "GPL-2.0"),
    (285, "DASM", "dasm-assembler/dasm", "GPL-2.0"),
    (286, "7800basic", "7800-devtools/7800basic", "GPL-2.0"),
    (287, "MSXgl", "aoineko-fr/MSXgl", "CC-BY-SA-4.0"),
    (288, "CPCtelera", "lronaldo/cpctelera", "LGPL-3.0"),
    (289, "ngdevkit", "dciabrin/ngdevkit", "LGPL-3.0"),
    (290, "AzuraCast", "AzuraCast/AzuraCast", "AGPL-3.0"),
]

DRIFT = [
    (68, "Helm", "mtytel/helm", "github"),
    (236, "telxcc", "kanongil/telxcc", "github"),
    (118, "MB-Lab", "animate1978/MB-Lab", "github"),
    (195, "SubDownloader", "subdownloader/subdownloader", "github"),
    (191, "MPC-HC", "mpc-hc/mpc-hc", "github"),
    (206, "ScanTailor", "scantailor/scantailor", "github"),
    (243, "Strudel", "tidalcycles/strudel", "github"),
    (253, "subSync", "sc0ty/subSync", "github"),
    (155, "MKVToolNix", "mbunkus/mkvtoolnix", "codeberg"),
    (101, "uzu/tidal", "uzu/tidal", "codeberg"),
]

results = {"rows": [], "drift": []}
for row, name, repo, claimed in ROWS:
    meta = gh_repo(repo)
    lic = gh_license_raw(repo)
    results["rows"].append({"row": row, "name": name, "repo": repo,
                            "claimed": claimed, "meta": meta,
                            "lic": {k: v for k, v in lic.items() if k != "text"},
                            "lic_snippet": lic.get("text", "")[:400]})
    print(f"row {row} {name}: http={meta['http']} archived={meta['archived']} "
          f"pushed={meta['pushed_at']} owner={meta['owner']} spdx={meta['spdx']} "
          f"lic_path={lic.get('path')} lic_size={lic.get('size')}", flush=True)

for row, name, repo, host in DRIFT:
    if host == "github":
        meta = gh_repo(repo)
        lic = gh_license_raw(repo)
        extra = {"lic_path": lic.get("path"), "lic_size": lic.get("size")}
    else:
        meta = codeberg_repo(repo)
        extra = {}
    results["drift"].append({"row": row, "name": name, "repo": repo, "host": host,
                             "meta": meta, **extra})
    print(f"drift {name} (row {row}): http={meta['http']} archived={meta['archived']} "
          f"updated={meta.get('pushed_at') or meta.get('updated')} owner={meta['owner']} "
          f"spdx={meta.get('spdx')} {extra}", flush=True)

# Byte-identity checks for Codeberg license files
for owner_repo, path, expect_bytes in [
        ("mbunkus/mkvtoolnix", "COPYING", 18092),
        ("uzu/tidal", "LICENSE", 35106)]:
    url = f"https://codeberg.org/{owner_repo}/raw/branch/main/{path}"
    code, data = curl_bytes(url)
    ok = (code == 200 and len(data) == expect_bytes)
    results.setdefault("byte_checks", {})[owner_repo] = {
        "http": code, "bytes": len(data), "expected": expect_bytes, "identical": ok}
    print(f"bytecheck {owner_repo}/{path}: http={code} bytes={len(data)} expected={expect_bytes} identical={ok}", flush=True)

json.dump(results, open(OUT, "w"), indent=1)
print("saved", OUT)
