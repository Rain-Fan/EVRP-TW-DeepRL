"""Print versions and accelerator support used by experiments."""

from __future__ import annotations

import importlib.metadata
import json
import platform
import sys

import torch


def main() -> None:
    packages = ("numpy", "pandas", "torch", "pyyaml", "matplotlib")
    report = {
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "accelerators": {
            "mps": torch.backends.mps.is_available(),
            "cuda": torch.cuda.is_available(),
        },
        "packages": {name: importlib.metadata.version(name) for name in packages},
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

