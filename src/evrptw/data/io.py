"""JSON serialization for EVRP-TW instances."""

from __future__ import annotations

import json
from pathlib import Path

from evrptw.core.instance import EVRPTWInstance


def load_instance(path: str | Path) -> EVRPTWInstance:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return EVRPTWInstance.from_dict(data)


def save_instance(instance: EVRPTWInstance, path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(instance.to_dict(), indent=2) + "\n", encoding="utf-8")

