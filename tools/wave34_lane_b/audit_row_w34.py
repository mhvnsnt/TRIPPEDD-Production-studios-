#!/usr/bin/env python3
"""Wave 34 Lane B — reusable quarantine-row upstream license verifier.

Serves future re-verification cycles on docs/LICENSE_QUARANTINE.md: given a row
number, it re-checks the claimed license fresh upstream (repo-page existence +
archived status, GitHub API spdx_id, raw README/COPYING/LICENSE fetches) and
writes proof files. It prints evidence + a mechanical verdict (CONFIRMED / NEEDS
REVIEW / REPO MISSING) — the lane auditor still makes the final call.

Usage:
    python3 audit_row_w34.py --row 48
    python3 audit_row.py --row 15 --out-dir /tmp/audit-proofs

The REPO_MAP covers the rows re-verified in Waves 30-31. Extending it to new
rows is the only manual step; everything else is automatic.
"""
import argparse, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "..", "..", "docs", "LICENSE_QUARANTINE.md")

# row -> (github repo, candidate license paths tried in order)
REPO_MAP = {
 1: ("readbeyond/aeneas", ["README.md", "LICENSE", "COPYING"]),
 2: ("readbeyond/aeneas", ["README.md", "LICENSE", "COPYING"]),
 3: ("AnimeEffectsDevs/AnimeEffects", ["LICENSE", "LICENSE.md"]),
 4: ("AUTOMATIC1111/stable-diffusion-webui", ["LICENSE.txt", "LICENSE"]),
 5: ("Comfy-Org/ComfyUI", ["LICENSE", "LICENSE.md"]),
 6: ("Hope2333/enve", ["LICENSE.md", "LICENSE", "COPYING"]),
 7: ("espeak-ng/espeak-ng", ["LICENSE.md", "LICENSE", "COPYING"]),
 8: ("jliljebl/flowblade", ["LICENSE", "COPYING"]),
 9: ("n00mkrad/flowframes", ["LICENSE.md", "LICENSE"]),
 10: ("perarnia/fSpy", ["LICENSE", "LICENSE.md"]),
 11: ("mbasaglia/glaxnimate", ["COPYING", "LICENSES/GPL-3.0-or-later.txt", "LICENSE"]),
 12: ("KDE/krita", ["COPYING", "LICENSE"]),
 13: ("mifi/lossless-cut", ["LICENSE", "LICENSE.md"]),
 14: ("MycroftAI/mimic3", ["LICENSE", "COPYING"]),
 15: ("mypaint/mypaint", ["Licenses.dep5", "LICENSE", "COPYING"]),
 17: ("OpenShot/openshot-qt", ["COPYING", "LICENSE"]),
 20: ("OHF-voice/piper1-gpl", ["LICENSE", "LICENSE.md"]),
 24: ("svc-develop-team/so-vits-svc", ["LICENSE", "LICENSE.md"]),
 27: ("k4yt3x/video2x", ["LICENSE", "LICENSE.md"]),
 68: ("mtytel/helm", ["COPYING", "LICENSE"]),
 85: ("MTG/essentia", ["COPYING", "LICENSE"]),
 236: ("kanongil/telxcc", ["LICENSE", "COPYING"]),
 16: ("olive-editor/olive", ["LICENSE", "LICENSE.md", "COPYING"]),
 18: ("morevnaproject-org/papagayo-ng", ["gpl.txt", "LICENSE", "COPYING"]),
 19: ("pencil2d/pencil", ["LICENSE.TXT", "LICENSE.txt", "LICENSE"]),
 21: ("GDQuest/blender-power-sequencer", ["LICENSE", "COPYING"]),
 22: ("RHVoice/RHVoice", ["LICENSE.md", "doc/en/License.md"]),
 23: ("mltframework/shotcut", ["COPYING", "LICENSE"]),
 25: ("synfig/synfig", ["LICENSE", "COPYING"]),
 26: ("e7appew/tupitube.desk", ["COPYING", "LICENSE"]),
 28: ("xinjli/allosaurus", ["LICENSE", "LICENSE.md", "COPYING"]),
 29: ("mean00/avidemux2", ["COPYING", "LICENSE"]),
 30: ("blender/blender", ["COPYING", "doc/license/GPL-license.txt"]),
 34: ("GNOME/gimp", ["COPYING", "LICENSE"]),
 35: ("HandBrake/HandBrake", ["LICENSE", "COPYING"]),
 38: ("blender/kitsu", ["LICENSE", "README.md"]),
 42: ("praat/praat.github.io", ["README.md"]),
 43: ("Plachtaa/seed-vc", ["LICENSE"]),
 44: ("olstflow/storypencil_for4.4_fix", ["README.md"]),
 45: ("octimot/StoryToolkitAI", ["LICENSE"]),
 46: ("maxrd2/subtitlecomposer", ["LICENSE", "LICENSES/GPL-2.0-or-later.txt"]),
 47: ("upscayl/upscayl", ["LICENSE"]),
 48: ("ozmartian/vidcutter", ["LICENSE", "LICENSE.md"]),
 49: ("linto-ai/whisper-timestamped", ["LICENSE", "LICENSE.md"]),
 52: ("festivities/Blender-StellarToon", ["LICENSE", "LICENSE.md"]),
 53: ("mightymochi/2D-Cel-Toon-Shader-v2-Plus", ["LICENSE", "LICENSE.md"]),
 54: ("zyddnys/manga-image-translator", ["LICENSE", "LICENSE.md"]),
 56: ("mrdhnto/libre-manga-translator", ["LICENSE", "docs/technical.md", "README.md"]),
 76: ("PeterL1n/RobustVideoMatting", ["LICENSE", "LICENSE.md"]),
 77: ("MMD-Blender/blender_mmd_tools", ["LICENSE", "LICENSE.md"]),
 78: ("Kiteretsu77/APISR", ["LICENSE", "LICENSE.md"]),
 79: ("Bing-su/adetailer", ["LICENSE.md", "LICENSE"]),
}

UA = {"User-Agent": "trippedd-lane-b-audit"}


def curl(url, binary=False):
    cmd = ["curl", "-sL", "--max-time", "30", "-H", f"User-Agent: {UA['User-Agent']}", url]
    return subprocess.run(cmd, capture_output=True).stdout


def get_row_claim(row):
    txt = open(MANIFEST).read()
    m = re.search(r"^\|\s*%d\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|" % row, txt, re.M)
    if not m:
        return None, None
    name, lic = m.group(1).strip(), m.group(2).strip()
    spdx = re.findall(r"\b(AGPL-3\.0(?:-or-later|-only)?|GPL-3\.0(?:-or-later|-only)?|"
                      r"GPL-2\.0(?:-or-later|-only)?|LGPL-[23]\.[01](?:-or-later|-only)?|"
                      r"MPL-2\.0|CeCILL-2\.1|ODbL-1\.0|CC BY-SA|CC BY-NC-ND|ISC|Apache-2\.0)\b", lic)
    return name, spdx


def fetch_raw(repo, path, out_dir):
    for branch in ("master", "main"):
        body = curl(f"https://raw.githubusercontent.com/{repo}/{branch}/{path}")
        if body and not body.startswith(b"404: Not Found") and len(body) > 100:
            fname = path.replace("/", "_")
            open(os.path.join(out_dir, fname), "wb").write(body)
            return branch, body
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--row", type=int, required=True)
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    if args.row not in REPO_MAP:
        print(f"row {args.row} not in REPO_MAP — add (repo, license-paths) first"); sys.exit(2)
    repo, paths = REPO_MAP[args.row]
    out_dir = args.out_dir or os.path.join(HERE, "proofs_row%d" % args.row)
    os.makedirs(out_dir, exist_ok=True)

    name, claim_spdx = get_row_claim(args.row)
    print(f"ROW {args.row}: {name} | manifest claims: {claim_spdx}")

    api = json.loads(curl(f"https://api.github.com/repos/{repo}") or b"{}")
    if not api.get("full_name"):
        print(f"REPO MISSING: {repo} — {api.get('message')}")
        return
    json.dump(api, open(os.path.join(out_dir, "api.json"), "w"), indent=1)
    spdx = (api.get("license") or {}).get("spdx_id")
    print(f"repo: {api['full_name']} | archived: {api.get('archived')} | "
          f"pushed: {api.get('pushed_at')} | api spdx_id: {spdx}")

    fetched = {}
    for p in paths:
        branch, body = fetch_raw(repo, p, out_dir)
        if body:
            fetched[p] = (branch, body)
            head = body[:160].decode("utf-8", "replace").replace("\n", " ")
            print(f"  raw {p} (branch {branch}, {len(body)} bytes): {head}")

    verdict = "NEEDS REVIEW"
    if claim_spdx:
        norm = lambda s: (s or "").replace("-only", "").replace("GPL-3.0", "GPL-3.0").upper()
        api_norm = {"GPL-2.0": "GPL-2.0", "GPL-3.0": "GPL-3.0",
                    "AGPL-3.0": "AGPL-3.0"}.get(spdx)
        claim_first = claim_spdx[0].upper()
        if api_norm and (api_norm == claim_first or claim_first.startswith(api_norm)):
            verdict = "CONFIRMED"
        elif any(x in (claim_first or "") for x in ("ISC",)) and b"ISC" in (fetched.get(paths[0], (None, b""))[1] if fetched else b""):
            verdict = "CONFIRMED"
        else:
            # fall back: license text mentions the claimed version family
            haystack = b" ".join(b for _, b in fetched.values()).upper()  # no truncation: license clauses can sit deep in READMEs (e.g. row 42 Praat §2.1)
            gpl = b"GENERAL PUBLIC LICENSE" in haystack or b"GPL-3.0" in haystack or b"GPL-3" in haystack
            if claim_first.startswith("GPL-2") and gpl and b"VERSION 2" in haystack:
                verdict = "CONFIRMED"
            elif claim_first.startswith("GPL-3") and gpl and (b"VERSION 3" in haystack):
                verdict = "CONFIRMED"
            elif claim_first.startswith("AGPL-3") and b"AFFERO" in haystack:
                verdict = "CONFIRMED"
    print(f"VERDICT: {verdict} (mechanical — auditor decides)")
    print(f"proofs: {out_dir}/")


if __name__ == "__main__":
    sys.exit(main())
