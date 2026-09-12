# Autonomous Studio Agent Stack

This is the autonomous production team layer for TRIPPEDD. It does not replace the existing production tools; it coordinates and audits them.

LangGraph supplies durable stateful orchestration. CrewAI supplies role-based specialist collaboration. MCP is the tool boundary. LiteLLM routes model providers. OpenHands handles autonomous software work. n8n handles schedules, webhooks and approvals. MinIO stores evidence artifacts and PostgreSQL stores durable agent state.

The same agent contract is intended to run against TRIPPEDD and God Molecule.

Every tool execution must have intent, inputs, an execution record, outputs, provenance and validation. Model claims never substitute for physical evidence. Final greenlight remains human-only.

Secrets belong only in local environment files or GitHub Actions secrets. Never commit API keys, GitHub tokens, Drive credentials or private-repository tokens.
