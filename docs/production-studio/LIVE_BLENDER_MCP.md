# Live Blender MCP adapter

This adapter is the runtime boundary between TRIPPEDD's typed prompt-production envelope and an operator-hosted Blender MCP bridge.

## Runtime

Set `BLENDER_MCP_URL` to the HTTP endpoint exposed by the Blender MCP bridge, then run:

```bash
python3 tools/prompt_production/blender_mcp_adapter.py compiled-operation.json
```

The adapter does not embed a provider-specific Blender MCP protocol. Different bridges can sit behind the endpoint as long as they accept the TRIPPEDD envelope and return a JSON object containing an optional `artifacts` list.

## Authority and evidence

- TRIPPEDD owns canon, production graph, provenance, gates, and evidence.
- The MCP bridge executes Blender operations; it is not production authority.
- An MCP acknowledgement is not render evidence.
- Returned artifact references are not accepted as production evidence until the existing TRIPPEDD artifact/pixel, physical, and visual QC chain verifies them.
- `MARS_CANONICAL` must not be replaced by a generated substitute.
- No credentials, endpoint URLs, or local Blender paths are committed to the repository.

## Next connection

The operator supplies the actual Blender MCP endpoint. Once available, the prompt compiler output can be sent through this adapter, and returned render paths can be handed to the existing first-shot evidence verifiers.
