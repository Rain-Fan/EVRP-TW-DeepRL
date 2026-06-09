"""Feature extraction shared by policy training and inference."""

from __future__ import annotations

import numpy as np
import torch

from evrptw.core.instance import EVRPTWInstance, NodeType
from evrptw.core.simulator import RouteState


def static_node_features(instance: EVRPTWInstance) -> torch.Tensor:
    scale = max(max(node.x, node.y) for node in instance.nodes) or 1.0
    horizon = max(node.due_time for node in instance.nodes if np.isfinite(node.due_time)) or 1.0
    rows = []
    for node in instance.nodes:
        rows.append(
            [
                node.x / scale,
                node.y / scale,
                node.demand / instance.vehicle.capacity,
                node.ready_time / horizon,
                node.due_time / horizon,
                node.service_time / horizon,
                float(node.kind is NodeType.DEPOT),
                float(node.kind is NodeType.CUSTOMER),
                float(node.kind is NodeType.STATION),
            ]
        )
    return torch.tensor(rows, dtype=torch.float32)


def dynamic_state_features(instance: EVRPTWInstance, state: RouteState) -> torch.Tensor:
    horizon = max(node.due_time for node in instance.nodes if np.isfinite(node.due_time)) or 1.0
    return torch.tensor(
        [
            state.remaining_capacity / instance.vehicle.capacity,
            state.battery / instance.vehicle.battery_capacity,
            state.time / horizon,
            state.vehicles_used / instance.vehicle.count,
        ],
        dtype=torch.float32,
    )

