#!/usr/bin/env python3
"""Clone/update the five open-source generative production runtimes used by TRIPPEDD.

Models/checkpoints are intentionally NOT bundled here. They are downloaded separately
after license/hardware validation.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2] / "third_party" / "generative"
PROJECTS = {
    # Generative image/video stack
    "ComfyUI": ("https://github.com/comfyanonymous/ComfyUI.git", "master"),
    "InvokeAI": ("https://github.com/invoke-ai/InvokeAI.git", "main"),
    "DiffSynth-Studio": ("https://github.com/modelscope/DiffSynth-Studio.git", "main"),
    "LTX-Video": ("https://github.com/Lightricks/LTX-Video.git", "main"),
    "Wan2.1": ("https://github.com/Wan-Video/Wan2.1.git", "main"),
    # 3D / 2D / compositing production stack
    "Blender": ("https://github.com/blender/blender.git", "main"),
    "OpenToonz": ("https://github.com/opentoonz/opentoonz.git", "master"),
    "Synfig": ("https://github.com/synfig/synfig.git", "master"),
    "Natron": ("https://github.com/NatronGitHub/Natron.git", "RB-2.6"),
    "MPFB2": ("https://github.com/makehumancommunity/mpfb2.git", "master"),
}

def run(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True)

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for name, (url, branch) in PROJECTS.items():
        dst = ROOT / name
        if (dst / ".git").exists():
            run("git", "fetch", "--prune", "origin", cwd=dst)
            run("git", "checkout", branch, cwd=dst)
            run("git", "pull", "--ff-only", "origin", branch, cwd=dst)
        else:
            run("git", "clone", "--branch", branch, "--depth", "1", url, str(dst))
        print(f"READY {name}: {dst}")

if __name__ == "__main__":
    main()
