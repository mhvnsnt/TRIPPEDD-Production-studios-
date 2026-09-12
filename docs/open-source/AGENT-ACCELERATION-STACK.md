# Open-Source Agent Acceleration Stack

The goal is not to replace the model. The goal is to give every model a better **coding harness**: better repository context, safer execution, smaller diffs, stronger verification, durable memory, and parallel work.

## What actually makes an agent better

A repo cannot magically make an LLM smarter, but it can make the LLM substantially more effective. The highest-value layers are:

1. **Execution** — OpenHands SDK/runtime for isolated, repeatable agent work.
2. **Git-native editing** — Aider-style repo mapping and focused diffs.
3. **Repository intelligence** — ripgrep + fd + tree-sitter/ast-grep for fast structural search and precise edits.
4. **Static verification** — Semgrep plus the project's existing type/test/build gates.
5. **Task solving** — SWE-agent/mini-swe-agent patterns for issue-to-patch loops.
6. **Model routing** — LiteLLM-compatible provider abstraction so a task can use the best available model without rewriting the harness.
7. **Durable evidence** — TRIPPEDD's evidence manifests, hashes, visual proofs, and UNKNOWN-never-PASS law.
8. **Parallel isolation** — Git worktrees so agents never have to destroy another agent's dirty evidence tree to switch tasks.

The last two are project-specific and are deliberately treated as first-class agent infrastructure.

## Recommended stack

| Layer | Open source candidate | Role | Adoption policy |
|---|---|---|---|
| Agent runtime | OpenHands SDK | Long-running coding tasks, tools, sandboxing, multi-agent orchestration | P0; integrate as an adapter, not as the production UI |
| Git-native coding | Aider | Repo map, focused edits, automatic git checkpoints | P0; use for bounded code tasks |
| Issue solver | SWE-agent / mini-swe-agent | Issue-to-test-to-patch loop | P1; evaluate on real TRIPPEDD issues |
| Structural search | tree-sitter + ast-grep | AST-aware search and transformations | P0 for large refactors |
| Fast search | ripgrep + fd | Cheap broad repository discovery | P0 |
| Static analysis | Semgrep | Security/bug-pattern verification | P0; findings are evidence, not automatic truth |
| Model gateway | LiteLLM | Provider/model routing | P1; optional dependency |
| Existing project runtime | Express/Vite + current production cockpit | Human-facing production surface | KEEP as authority |

## Architecture

```text
                    ┌────────────────────────────┐
                    │        TRIPPEDD task        │
                    │ issue / lane / evidence ID  │
                    └─────────────┬──────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │      Agent Task Contract     │
                    │ scope · inputs · gates ·     │
                    │ outputs · rollback · owner   │
                    └─────────────┬──────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
        OpenHands SDK          Aider              SWE-agent
        long-running          focused diff       issue solver
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  ▼
                    ┌────────────────────────────┐
                    │ Repository intelligence     │
                    │ rg · fd · tree-sitter      │
                    │ ast-grep · git worktree    │
                    └─────────────┬──────────────┘
                                  ▼
                    ┌────────────────────────────┐
                    │ Verification loop            │
                    │ tests · build · Semgrep     │
                    │ visual QC · hashes          │
                    │ contact/geometry gates      │
                    └─────────────┬──────────────┘
                                  ▼
                    ┌────────────────────────────┐
                    │ Evidence bus                 │
                    │ manifest + artifacts +       │
                    │ command + commit + hashes    │
                    └────────────────────────────┘
```

## Critical rule: do not vendor agents blindly

Do **not** dump OpenHands, Aider, or another agent's entire source tree into the production application. That creates a giant moving dependency and does not improve reasoning by itself.

Instead:

- keep the agent tools as external/open-source runtime dependencies;
- commit a small, versioned adapter/manifest in this repository;
- record the exact tool version and model used for every reproducible run;
- make outputs land in the existing evidence bus;
- make every agent obey the same task contract and quality gates.

This gives TRIPPEDD the useful parts of a Replit/Devin-style harness without making the production app depend on a paid hosted control plane.

## What we should build next

### P0

- `tools/agent/agent_stack_manifest.json` — versions, licenses, roles, install commands, capability flags.
- `tools/agent/check_agent_stack.py` — fail-closed environment/capability check; never claims a missing binary is installed.
- Agent task contract with bounded scope and required verification commands.
- Worktree-per-task convention for Claude/Jules/ChatGPT/other agents.
- Automatic evidence manifest generation after a successful task.
- Fast repository map generated from source/config, excluding binary evidence and generated caches.

### P1

- OpenHands SDK adapter for long-running tasks.
- Aider adapter for focused code changes.
- SWE-agent/mini-swe-agent adapter for issue-driven repair.
- ast-grep recipes for the project's recurring TypeScript/Python/Blender patterns.
- Semgrep rules for production-specific failure modes.
- LiteLLM model-routing adapter with per-task model selection.

## Definition of better

A better agent is not the one that writes the most code. It is the one that:

- finds the right files quickly;
- understands the current authority instead of stale artifacts;
- makes the smallest correct change;
- runs the right test/render/measurement;
- notices when its own result is wrong;
- records enough evidence for another agent to continue;
- never converts UNKNOWN into PASS;
- can recover from a failed or interrupted run without destroying evidence.

That is the target for this repository.
