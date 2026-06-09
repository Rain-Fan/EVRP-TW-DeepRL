"""Typed EVRP-TW instance definitions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from math import hypot
from typing import Any


class NodeType(StrEnum):
    DEPOT = "depot"
    CUSTOMER = "customer"
    STATION = "station"


@dataclass(frozen=True, slots=True)
class Node:
    id: int
    kind: NodeType
    x: float
    y: float
    demand: float = 0.0
    ready_time: float = 0.0
    due_time: float = float("inf")
    service_time: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Node:
        return cls(**{**data, "kind": NodeType(data["kind"])})


@dataclass(frozen=True, slots=True)
class VehicleSpec:
    count: int
    capacity: float
    battery_capacity: float
    energy_rate: float = 1.0
    speed: float = 1.0
    charging_rate: float = 1.0


@dataclass(frozen=True, slots=True)
class EVRPTWInstance:
    name: str
    nodes: tuple[Node, ...]
    vehicle: VehicleSpec

    def __post_init__(self) -> None:
        if not self.nodes or self.nodes[0].kind is not NodeType.DEPOT:
            raise ValueError("Node 0 must be the depot.")
        if [node.id for node in self.nodes] != list(range(len(self.nodes))):
            raise ValueError("Node IDs must be contiguous and match tuple positions.")
        if self.vehicle.count < 1:
            raise ValueError("At least one vehicle is required.")

    @property
    def customer_ids(self) -> tuple[int, ...]:
        return tuple(node.id for node in self.nodes if node.kind is NodeType.CUSTOMER)

    @property
    def station_ids(self) -> tuple[int, ...]:
        return tuple(node.id for node in self.nodes if node.kind is NodeType.STATION)

    def distance(self, source: int, target: int) -> float:
        first, second = self.nodes[source], self.nodes[target]
        return hypot(first.x - second.x, first.y - second.y)

    def travel_time(self, source: int, target: int) -> float:
        return self.distance(source, target) / self.vehicle.speed

    def energy(self, source: int, target: int) -> float:
        return self.distance(source, target) * self.vehicle.energy_rate

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "nodes": [
                {**asdict(node), "kind": node.kind.value}
                for node in self.nodes
            ],
            "vehicle": asdict(self.vehicle),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EVRPTWInstance:
        return cls(
            name=data["name"],
            nodes=tuple(Node.from_dict(node) for node in data["nodes"]),
            vehicle=VehicleSpec(**data["vehicle"]),
        )

