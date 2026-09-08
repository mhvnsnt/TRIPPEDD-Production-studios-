# Production Conversations

This directory contains the chronological **storyrunner / production-room archive** for TRIPPEDD Production Studios.

## Recording rule

When a conversation materially affects a production, capture the conversation as a dated Markdown record. Preserve both sides of the room:

- `USER / SHOWRUNNER`
- `CHATGPT / AGENT`
- other production agents when applicable

Do not silently rewrite the conversation into a polished summary. A summary may accompany the record, but the conversation itself is the source layer.

## Relationship to other production records

```text
PRODUCTION CONVERSATION
        │
        ├── idea / discovery
        ├── decision / rejection / unresolved question
        │
        ▼
CANON / PRODUCTION DOCUMENTS
        │
        ├── assets
        ├── editorial plans
        ├── scripts / storyboards
        └── manifests
        │
        ├───────────────┐
        ▼               ▼
SHOWRUNNER CUT     AUTONOMOUS CUT
        │               │
        └───────┬───────┘
                ▼
          COMPARISON / LEARNING
```

## File naming

Use:

`YYYY-MM-DD-<topic>.md`

For example:

`2026-09-08-the-bastard-series-development.md`

## Required front matter

```yaml
---
date: YYYY-MM-DD
property: TRIPPEDD | The Walk | The Bastard | Bannon | Studio
layer: STORYRUNNER
participants:
  - USER_SHOWRUNNER
  - CHATGPT
status: DISCUSSION | DECISION | DISCOVERY | REFERENCE | UNRESOLVED
---
```

## Historical reconstruction rule

If the original conversation is available, preserve it faithfully.

If only prior project context is available, create a section explicitly labeled `RECONSTRUCTED FROM AVAILABLE CONTEXT`. Never manufacture a verbatim transcript that is not actually available.

## Cross-references

Production conversation records should link to resulting docs/assets when known. A creative decision should be traceable in both directions:

`conversation → production artifact`

and

`production artifact → originating conversation`

## Permanent studio policy

The same archive pattern should be applied to future repositories/projects that are used as production workspaces whenever technically possible. The repository-local archive policy is the enforceable implementation; it does not imply that GitHub account settings can automatically capture private ChatGPT conversations.
