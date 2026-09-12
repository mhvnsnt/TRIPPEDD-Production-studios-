import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "contact_gate.py"


def run(payload):
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "receipt.json"
        p.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(GATE), str(p)],
            text=True,
            capture_output=True,
        )


def base():
    return {
        "schema": "trippedd.contact-measurement/v1",
        "pair": "hair->head",
        "mode": "BLOCK",
        "penetrationMM": {"p50": 0, "p90": 0, "p99": 0, "max": 0},
        "violatingSamples": 0,
        "toleranceMM": 0.5,
        "selfCollision": "PASS",
        "visualEvidence": "docs/evidence/hair_motion/sequence.json",
        "sourceHash": "source",
        "proxyHash": "proxy",
    }


def test_block_passes_when_clean():
    result = run(base())
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "PASS"


def test_block_fails_on_penetration():
    payload = base()
    payload["penetrationMM"]["max"] = 0.51
    result = run(payload)
    assert result.returncode == 45
    assert "FAIL" in result.stderr


def test_missing_visual_evidence_fails_closed():
    payload = base()
    payload.pop("visualEvidence")
    result = run(payload)
    assert result.returncode == 45


def test_style_override_requires_reason():
    payload = base()
    payload["mode"] = "STYLE_OVERRIDE"
    result = run(payload)
    assert result.returncode == 45


def test_allow_is_explicit():
    payload = base()
    payload["mode"] = "ALLOW"
    result = run(payload)
    assert result.returncode == 0
    assert json.loads(result.stdout)["status"] == "ALLOW"
