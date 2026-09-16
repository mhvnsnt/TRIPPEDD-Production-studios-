#!/usr/bin/env python3
"""Character-performance entry point for the EP01 origin builder.

The historical teen_performance.py remains untouched. The active compositor
loads the clean v2 backend before executing the shared deterministic builder,
then installs that same backend as the teen layer.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BUILDER_PATH=ROOT/"show/in-the-bushes/tools/build_origin_opening.py"
RIG_PATH=ROOT/"show/in-the-bushes/tools/teen_performance_v2.py"
def load_module(path: Path, name: str, source_rewrite: tuple[str,str]|None=None):
    source=path.read_text(encoding="utf-8")
    if source_rewrite:
        source=source.replace(source_rewrite[0], source_rewrite[1])
    code=compile(source,str(path),"exec")
    module=importlib.util.module_from_spec(importlib.util.spec_from_file_location(name,path))
    exec(code,module.__dict__)
    return module
# The shared builder historically imports teen_performance.py. Rewrite that
# import in memory so the malformed legacy source never enters the active graph.
builder=load_module(BUILDER_PATH,"origin_builder",("teen_performance.py","teen_performance_v2.py"))
rig=load_module(RIG_PATH,"teen_performance_v2")
def performance_teen_layer(blocks, frame, shot_id):
    if shot_id not in {"S01","S02","S03","S04","S05","S06","S07","S08","S09"}:
        return ""
    return rig.performance_layer(frame,shot_id)
builder.teen_layer=performance_teen_layer
if __name__=="__main__":
    builder.main()
