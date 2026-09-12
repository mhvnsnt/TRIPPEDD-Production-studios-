from pathlib import Path
import os
import subprocess
from mcp.server.fastmcp import FastMCP

ROOT = Path(os.environ.get("STUDIO_ROOT", "/workspace")).resolve()
mcp = FastMCP("studio-production-tools")

ALLOWED = {
    "audit_integrity": ["npm", "run", "studio:audit:integrity"],
    "audit_toolchain": ["npm", "run", "studio:audit"],
    "test_provenance": ["npm", "run", "studio:test:provenance"],
    "build_pilot": ["npm", "run", "pilot:build"],
    "validate_artifact": ["npm", "run", "pilot:validate"],
}

@mcp.tool()
def list_capabilities() -> dict:
    return {"workspace": str(ROOT), "tools": sorted(ALLOWED)}

@mcp.tool()
def run_production_tool(name: str) -> dict:
    if name not in ALLOWED:
        raise ValueError(f"Tool not allowlisted: {name}")
    result = subprocess.run(
        ALLOWED[name],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=3600,
    )
    return {
        "name": name,
        "returncode": result.returncode,
        "stdout": result.stdout[-12000:],
        "stderr": result.stderr[-12000:],
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
