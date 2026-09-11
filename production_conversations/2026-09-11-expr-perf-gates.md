# Production log — 2026-09-11 Expression/blink + performance render gates

Steps 8–10 orchestration on TRIPPEDD:

- `tools/character/validate_expression_blink_package.py`
- `tools/animation/validate_performance_render.py`

CREATIVE_FINAL requires:
1. physical PNG frames
2. optional upstream oral/jaw/rhubarb checks when paths supplied
3. explicit HUMAN_OK.txt
4. `--allow-creative-final`

No human file → never creative_final.
