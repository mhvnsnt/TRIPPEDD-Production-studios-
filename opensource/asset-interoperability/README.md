# TRIPPEDD OpenAssetIO boundary

OpenAssetIO is the horizontal asset-identity boundary for the studio. It is not our database, storage layer, production tracker, or render system.

## Contract

TRIPPEDD asset identity -> OpenAssetIO -> manager/resolver -> concrete media

Rules:
- identity is authoritative; filesystem paths are resolved data, not identity;
- unresolved assets fail loudly;
- no silent local-path fallback;
- resolved assets carry provenance/version information when available;
- DCC, editorial, review, render, and AI-assisted systems may consume the same identity.
