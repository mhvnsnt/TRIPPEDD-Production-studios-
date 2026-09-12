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

`storyrunner-YYYY-MM-DD-topic.md`

under the month directory:

`YYYY/YYYY-MM/`

Example:

`2026/2026-09/storyrunner-2026-09-08-the-bastard-series-development.md`

## Required record fields

Each record should identify, when known:

- date/time
- property / project
- layer (`STORYRUNNER`)
- participants
- status (`DISCUSSION`, `DECISION`, `DISCOVERY`, `REFERENCE`, `UNRESOLVED`, or `RECONSTRUCTED`)
- source/provenance
- resulting production artifacts
- related canon decisions
- related autonomous discoveries/cuts

## Historical reconstruction rule

If the original conversation is available, preserve it faithfully.

If only prior project context is available, create a section explicitly labeled `RECONSTRUCTED FROM AVAILABLE CONTEXT`. Never manufacture a verbatim transcript that is not actually available.

## Current conversation policy

The production-room archive is **append-oriented**. New materially relevant exchanges should become new dated records rather than silently rewriting older records. Corrections should preserve the history of the correction.

The archive should preserve not only decisions, but also:

- ideas that were rejected;
- reversals and changes of mind;
- unresolved questions;
- references and influences;
- technical discoveries that change production;
- disagreements between showrunner and autonomous systems;
- the reasoning that makes a decision intelligible later.

## Cross-references

Production conversation records should link to resulting docs/assets when known. A creative decision should be traceable in both directions:

`conversation → production artifact`

and

`production artifact → originating conversation`

## Standing cross-repository convention

For any repository used as a production workspace through the connected GitHub workflow, use this same architecture whenever technically possible:

```text
<repo>/docs/PRODUCTION-CONVERSATION-ARCHIVE.md
<repo>/docs/production-conversations/README.md
<repo>/docs/production-conversations/YYYY/YYYY-MM/storyrunner-YYYY-MM-DD-topic.md
```

The archive remains a separate source layer from implementation/canon and from machine-generated/autonomous work. This convention applies to entertainment projects and to other substantive projects where preserving the reasoning/history materially helps continuity.

## Technical boundary

A repository-local policy cannot make GitHub or ChatGPT automatically capture private conversations that are not supplied to the connected workflow. It is therefore not accurate to claim that GitHub is globally recording every ChatGPT conversation. The standing production convention is instead: **whenever a connected workflow has access to a materially relevant production conversation, archive it in the repository's production-conversation layer.**
