#!/usr/bin/env python3
"""TRIPPEDD OpenAssetIO boundary adapter."""
import json
try:
 import openassetio
 AVAILABLE=True
 VERSION=getattr(openassetio,"__version__","unknown")
except Exception:
 AVAILABLE=False
 VERSION=None
def probe():
 return {"backend":"openassetio","available":AVAILABLE,"version":VERSION,"mode":"identity-first","fallback":"none","policy":"missing-resolution-is-fail"}
if __name__=="__main__":
 print(json.dumps(probe(),sort_keys=True))
 raise SystemExit(0 if AVAILABLE else 40)
