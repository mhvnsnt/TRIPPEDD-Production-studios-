# Open-Source Agent Acceleration Stack

The goal is not to replace the model. The goal is to give every model a better **coding harness**: better repository context, safer execution, smaller diffs, stronger verification, durable memory, and parallel work.

## What actually makes an agent better

A repo cannot magically make an LLM smarter, but it can make the LLM substantially more effective. The highest-value layers are:

1. **Execution** — OpenHands SDK/runtime for isolated, repeatable agent work.
2. **Git-native editing** — Aider-style repo mapping and focused diffs.
3. **Repository intelligence** — ripgrep + fd + tree-sitter/ast-grep for fast structural search and precise edits.
4. **Bounded context** — reproducible task context packets instead of dumping the whole repository into a prompt.
5. **Static verification** — Semgrep plus the project's existing type/test/build gates.
6. **Task solving** — mini-SWE-agent as the preferred lightweight issue-to-patch worker; legacy SWE-agent remains an alternative research harness.
7. **Model routing** — LiteLLM-compatible provider abstraction so a task can use the best available model without rewriting the harness.
8. **Durable evidence** — TRIPPEDD's evidence manifests, hashes, visual proofs, and UNKNOWN-never-PASS law.
9. **Parallel isolation** — Git worktrees so agents never have to destroy another agent's dirty evidence tree to switch tasks.

The last three are project-specific and are deliberately treated as first-class agent infrastructure.

## Recommended stack

| Layer | Open source candidate | Role | Adoption policy |
|---|---|---|---|
| Agent runtime | OpenHands SDK | Long-running coding tasks, tools, sandboxing, multi-agent orchestration | P0; integrate as an adapter, not as the production UI |
| Git-native coding | Aider | Repo map, focused edits, automatic git checkpoints | P0; use for bounded code tasks |
| Issue solver | mini-SWE-agent | Minimal shell-first issue-to-patch loop | P0; benchmark against real TRIPPEDD issues |
| Structural search | tree-sitter + ast-grep | AST-aware search and transformations | P0 for large refactors |
| Fast search | ripgrep + fd | Cheap broad repository discovery | P0 |
| Context packet | `tools/agent/context_pack.py` | Bounded, reproducible task memory/context | P0; derive only from explicit task scope and evidence targets |
| Static analysis | Semgrep | Security/bug-pattern verification | P0; findings are evidence, not automatic truth |
| Model gateway | LiteLLM | Provider/model routing | P1; optional dependency |
| Existing project runtime | Express/Vite + current production cockpit | Human-facing production surface | KEEP as authority |

## Architecture

```text
                    TRIPPEDD task
                         │
                 Agent Task Contract
                         │
                 Bounded Context Packet
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
 OpenHands SDK         Aider         mini-SWE-agent
 long-running       focused diff       issue solver
       └─────────────────┼─────────────────┘
                         ▼
              Repository intelligence
           rg · fd · tree-sitter · ast-grep
                         │
                         ▼
                  Verification loop
        tests · build · Semgrep · visual QC
             geometry/contact · hashes
                         │
                         ▼
                    Evidence bus
       manifest · artifacts · commit · SHA-256
                         │
                         ▼
                 next agent / human
```

## Critical rule: do not vendor agents blindly

Do **not** dump OpenHands, Aider, or another agent's entire source tree into the production application. That creates a giant moving dependency and does not improve reasoning by itself.

Instead:

- keep agent tools as external/open-source runtime dependencies;
- commit small, versioned adapters and manifests;
- record exact tool version and model for reproducible runs;
- build bounded context packets from explicit task scope rather than whole-repo prompt dumps;
- make outputs land in the existing evidence bus;
- make every agent obey the same task contract and quality gates.

This gives TRIPPEDD the useful parts of a Replit/Devin-style harness without making the production app depend on a paid hosted control plane.

## Current adapters

- `tools/agent/agent_stack_manifest.json` — declared components, roles, licenses, priorities, and capabilities.
- `tools/agent/check_agent_stack.py` — fail-closed environment/capability check; missing binaries are UNKNOWN and mini-SWE is the current P0 worker.
- `tools/agent/task_contract.schema.json` — bounded task contract with explicit worktree, scope, verification, and outputs.
- `tools/agent/worktree_guard.py` — verifies explicit worktree/path scope without deleting or resetting evidence.
- `tools/agent/context_pack.py` — creates a reproducible `trippedd.agent-context/v1` packet containing only explicit task-scope/evidence files plus Git identity/history.
- `tools/agent/mini_swe_runner.py` — bounded mini-SWE-agent invocation and run-receipt adapter.
- `tools/agent/openhands_runner.py` — bounded OpenHands SDK invocation; optional runtime, same contract/evidence boundary.
- `tools/agent/orchestrate_task.py` — end-to-end task execution: clean-worktree check, exact source-commit check, agent run, changed-path scope enforcement, declared verification, artifact SHA-256 harvest, and evidence-manifest emission.
- `docs/agent-evidence/evidence_manifest.schema.json` — canonical evidence-manifest contract, including `NOT_ATTEMPTED` for lanes that have not run.

## P0 build sequence

1. Worktree isolation and task contract — **implemented**.
2. mini-SWE-agent bounded repair worker — **implemented**.
3. Evidence harvesting + verification handoff — **implemented**.
4. OpenHands SDK adapter for long-running tasks — **implemented**.
5. Reproducible bounded context packets — **implemented**.
6. Aider/ast-grep structural editing lanes.
7. Semgrep project-specific failure rules.
8. Optional LiteLLM model routing.

## Definition of better

A better agent is not the one that writes the most code. It is the one that:

- finds the right files quickly;
- receives the right bounded context instead of drowning in repository noise;
- understands current authority instead of stale artifacts;
- makes the smallest correct change;
- runs the right test/render/measurement;
- notices when its own result is wrong;
- records enough evidence for another agent to continue;
- never converts UNKNOWN into PASS;
- can recover from a failed or interrupted run without destroying evidence.
