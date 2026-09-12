from typing import TypedDict
import os
from langgraph.graph import StateGraph, START, END

class StudioState(TypedDict, total=False):
    objective: str
    phase: str
    action: str
    result: dict
    approved: bool
    error: str

TRIPPEDD_ACTIONS = {
    "audit_integrity": ["npm", "run", "studio:audit:integrity"],
    "audit_toolchain": ["npm", "run", "studio:audit"],
    "test_provenance": ["npm", "run", "studio:test:provenance"],
    "build_pilot": ["npm", "run", "pilot:build"],
    "validate_artifact": ["npm", "run", "pilot:validate"],
}

def plan(state: StudioState):
    # The model layer may choose among these actions, but never supplies commands.
    objective = state.get("objective", "")
    if "provenance" in objective.lower():
        action = "test_provenance"
    elif "audit" in objective.lower():
        action = "audit_integrity"
    elif "pilot" in objective.lower() or "episode" in objective.lower():
        action = "build_pilot"
    else:
        action = "audit_toolchain"
    return {"phase": "planned", "action": action}

def execute(state: StudioState):
    import subprocess
    action = state["action"]
    command = TRIPPEDD_ACTIONS[action]
    p = subprocess.run(command, cwd=os.environ.get("STUDIO_ROOT", "."), text=True,
                       capture_output=True, timeout=3600)
    return {"phase": "executed", "result": {
        "action": action, "returncode": p.returncode,
        "stdout": p.stdout[-12000:], "stderr": p.stderr[-12000:]
    }}

def qc(state: StudioState):
    result = state["result"]
    return {"phase": "qc", "approved": result["returncode"] == 0}

graph = StateGraph(StudioState)
graph.add_node("plan", plan)
graph.add_node("execute", execute)
graph.add_node("qc", qc)
graph.add_edge(START, "plan")
graph.add_edge("plan", "execute")
graph.add_edge("execute", "qc")
graph.add_edge("qc", END)
studio_graph = graph.compile()
