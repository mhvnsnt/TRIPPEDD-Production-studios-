#!/usr/bin/env python3
"""Wave 20 Lane B — EBU-TT-D ecosystem wire.

Downloads the official EBU-TT-D W3C XML Schema (ebu/ebu-tt-d-xsd, BSD-3-Clause)
and one IRT EBU-TT-D application sample (IRT-Open-Source/irt-ebu-tt-d-application-samples,
Apache-2.0), then validates the sample against the schema with lxml.

Proof: tools/captions/proofs/wave20_ebuttd_validation.json
Honest failure modes: network fetch failures, schema invalidity, sample
non-conformance are all recorded in the proof JSON — no fake PASS.
"""
import io, json, os, sys, urllib.request, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROOF = os.path.join(HERE, "..", "captions", "proofs", "wave20_ebuttd_validation.json")
CACHE = os.path.join(HERE, ".cache_ebuttd")
os.makedirs(CACHE, exist_ok=True)

XSD_FILES = ["ebutt_d.xsd", "ebutt_datatypes.xsd", "ebutt_metadata.xsd",
             "ebutt_styling.xsd", "metadata.xsd", "parameter.xsd", "styling.xsd"]
XSD_BASE = "https://raw.githubusercontent.com/ebu/ebu-tt-d-xsd/master/"
SAMPLE = ("https://raw.githubusercontent.com/IRT-Open-Source/"
          "irt-ebu-tt-d-application-samples/master/ttml/cumulative-rows-001-ttml.xml")


def fetch(url, dest):
    if os.path.exists(dest):
        return open(dest, "rb").read()
    req = urllib.request.Request(url, headers={"User-Agent": "TRIPPEDD-wave20-lane-b"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    open(dest, "wb").write(data)
    return data


def main():
    from lxml import etree
    proof = {"tool": "validate_ebuttd.py", "wave": "20-lane-b",
             "run_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "xsd_source": "https://github.com/ebu/ebu-tt-d-xsd (BSD-3-Clause, GitHub API spdx_id BSD-3-Clause)",
             "sample_source": "https://github.com/IRT-Open-Source/irt-ebu-tt-d-application-samples (Apache-2.0)",
             "fetched": {}, "errors": []}
    try:
        for f in XSD_FILES:
            data = fetch(XSD_BASE + f, os.path.join(CACHE, f))
            proof["fetched"][f] = len(data)
        sample = fetch(SAMPLE, os.path.join(CACHE, "sample.xml"))
        proof["fetched"]["sample.xml"] = len(sample)
        schema = etree.XMLSchema(etree.parse(os.path.join(CACHE, "ebutt_d.xsd")))
        doc = etree.parse(io.BytesIO(sample))
        ok = schema.validate(doc)
        proof["schema_valid"] = True
        proof["sample_valid_against_schema"] = ok
        proof["validation_errors"] = [str(e) for e in schema.error_log] if not ok else []
        proof["root_tag"] = doc.getroot().tag
        proof["verdict"] = "PASS" if ok else "FAIL (sample non-conformant — honest)"
    except Exception as e:  # noqa: BLE001 — honest failure recording
        proof["errors"].append(f"{type(e).__name__}: {e}")
        proof["verdict"] = "FAIL (wire error — honest)"
    os.makedirs(os.path.dirname(PROOF), exist_ok=True)
    json.dump(proof, open(PROOF, "w"), indent=2)
    print(json.dumps({"verdict": proof["verdict"],
                      "errors": proof["errors"][:2],
                      "proof": os.path.relpath(PROOF, os.path.expanduser("~/workspace/trippedd-studio"))},
                     indent=2))
    return 0 if proof["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
