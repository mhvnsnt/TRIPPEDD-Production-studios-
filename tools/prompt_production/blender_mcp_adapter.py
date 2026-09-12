#!/usr/bin/env python3
"""Fail-closed operator adapter for a live Blender MCP endpoint.

TRIPPEDD remains the production authority. This adapter only transports a
compiled prompt operation envelope to an operator-supplied MCP bridge and
requires structured returned artifact references. It never declares a render,
QC pass, or evidence receipt on its own.

The endpoint is intentionally configured at runtime (BLENDER_MCP_URL) so no
credential, host, or local installation assumption is committed to the repo.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

SCHEMA = "trippedd.blender-mcp-adapter/v1"


def fail(message: str) -> int:
    print(f"BLENDER_MCP_ADAPTER: BLOCKED: {message}", file=sys.stderr)
    return 2


def post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        raw = response.read()
    result = json.loads(raw.decode("utf-8"))
    if not isinstance(result, dict):
        raise ValueError("MCP response must be a JSON object")
    return result


def main() -> int:
    if len(sys.argv) != 2:
        return fail("usage: blender_mcp_adapter.py <compiled-operation.json>")

    source = sys.argv[1]
    try:
        with open(source, "r", encoding="utf-8") as handle:
            operation = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"cannot read operation envelope: {exc}")

    if not isinstance(operation, dict):
        return fail("operation envelope must be a JSON object")
    if operation.get("schema") != "trippedd.prompt-intent/v1":
        return fail("unsupported prompt intent schema")
    if not operation.get("operations"):
        return fail("operation envelope contains no operations")

    endpoint = os.environ.get("BLENDER_MCP_URL", "").strip()
    if not endpoint:
        return fail("BLENDER_MCP_URL is not configured; no live Blender execution attempted")

    request = {
        "schema": SCHEMA,
        "authority": "TRIPPEDD",
        "operation": operation,
        "policy": {
            "adapter_is_not_production_authority": True,
            "do_not_claim_render_without_returned_artifact": True,
            "do_not_claim_qc_without_trippedd_verifiers": True,
            "canonical_identity_is_immutable": True,
        },
    }

    try:
        result = post_json(endpoint, request)
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return fail(f"MCP execution failed or returned invalid JSON: {exc}")

    # A bridge may acknowledge a command, but acknowledgement is not evidence.
    artifacts = result.get("artifacts")
    if not isinstance(artifacts, list):
        artifacts = []

    response = {
        "schema": SCHEMA,
        "execution": "RETURNED",
        "adapter_result": result,
        "artifacts_returned": len(artifacts),
        "production_gate": "BLOCKED_UNTIL_TRIPPEDD_QC",
        "evidence_status": "NOT_ATTEMPTED",
    }
    print(json.dumps(response, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
