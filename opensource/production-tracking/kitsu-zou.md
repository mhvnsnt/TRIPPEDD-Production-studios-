# Kitsu / Zou production-tracking layer

Upstream: https://github.com/cgwire/zou
Role: horizontal production-tracking and review backend.

Kitsu/Zou is an open-source animation/VFX production tracker. Zou stores
projects, shots, assets, tasks, file metadata, previews and versions, and
publishes an event stream; Gazu provides the Python integration client.

TRIPPEDD contract:
- TRIPPEDD remains the orchestration/production policy layer.
- Kitsu is the structured production-tracking system.
- OTIO remains editorial interchange truth.
- Source media remains physically sourced truth.
- Render systems report jobs/results into tracking; they do not become the
  tracker.
- Every shot/version published to Kitsu carries TRIPPEDD project/episode/scene/
  shot identifiers and provenance.
- Review/approval state is synchronized back into the production graph.

Initial status: integration candidate. Promote only after a self-hosted Zou
instance passes project -> shot -> task -> version -> preview -> event-stream
round-trip tests.

AI boundary:
Kitsu's API is suitable for agent-assisted production operations, but agents
must use least-privilege credentials and explicit write gates. Agent actions
must remain attributable to an agent identity and a human/co-producer approval
where TRIPPEDD policy requires it.
