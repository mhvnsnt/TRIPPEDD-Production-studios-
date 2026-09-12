# AYON core platform

Upstream: https://github.com/ynput/ayon-core
Deployment: https://github.com/ynput/ayon-docker
Role: studio-wide pipeline platform and DCC integration layer.

AYON core provides the base building blocks for AYON addons, including the
pipeline API, publishing plugins, loaders, launcher actions, global hooks and
artist-facing tools. AYON Docker provides the reference containerized server
deployment.

TRIPPEDD contract:
- TRIPPEDD remains the top-level production policy/orchestration layer.
- AYON is a reusable pipeline/DCC services layer.
- Kitsu/Zou remains the current production-tracking candidate.
- OpenPype is explicitly NOT adopted: its repository is archived and directs
  users to AYON.
- Do not duplicate AYON's DCC/publishing mechanisms inside TRIPPEDD when an
  upstream addon can be used instead.

Promotion gate:
AYON server + launcher -> Blender addon -> publish/load round-trip -> version
identity -> render submission -> TRIPPEDD event/provenance -> QC.
