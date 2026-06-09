"""Deterministic synthetic EVRP-TW instance generation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from evrptw.core.instance import EVRPTWInstance, Node, NodeType, VehicleSpec


@dataclass(frozen=True, slots=True)
class GeneratorConfig:
    seed: int = 42
    num_customers: int = 10
    num_stations: int = 2
    num_vehicles: int = 3
    map_size: float = 20.0
    vehicle_capacity: float = 30.0
    battery_capacity: float = 35.0
    energy_rate: float = 1.0
    speed: float = 1.0
    charging_rate: float = 4.0
    customer_demand_min: int = 1
    customer_demand_max: int = 8
    service_duration: float = 1.0
    time_horizon: float = 100.0
    time_window_width: float = 45.0


def generate_instance(config: GeneratorConfig) -> EVRPTWInstance:
    rng = np.random.default_rng(config.seed)
    coordinates = rng.uniform(0, config.map_size, size=(1 + config.num_customers, 2))
    coordinates[0] = config.map_size / 2

    nodes = [
        Node(
            id=0,
            kind=NodeType.DEPOT,
            x=float(coordinates[0, 0]),
            y=float(coordinates[0, 1]),
            due_time=config.time_horizon,
        )
    ]
    for customer_id in range(1, config.num_customers + 1):
        distance_from_depot = float(np.linalg.norm(coordinates[customer_id] - coordinates[0]))
        earliest = min(
            distance_from_depot + float(rng.uniform(0, 10)),
            config.time_horizon - config.time_window_width,
        )
        nodes.append(
            Node(
                id=customer_id,
                kind=NodeType.CUSTOMER,
                x=float(coordinates[customer_id, 0]),
                y=float(coordinates[customer_id, 1]),
                demand=float(
                    rng.integers(config.customer_demand_min, config.customer_demand_max + 1)
                ),
                ready_time=earliest,
                due_time=min(config.time_horizon, earliest + config.time_window_width),
                service_time=config.service_duration,
            )
        )

    depot = coordinates[0]
    radius = config.map_size * 0.22
    for offset in range(config.num_stations):
        angle = 2 * np.pi * offset / max(config.num_stations, 1)
        nodes.append(
            Node(
                id=len(nodes),
                kind=NodeType.STATION,
                x=float(np.clip(depot[0] + radius * np.cos(angle), 0, config.map_size)),
                y=float(np.clip(depot[1] + radius * np.sin(angle), 0, config.map_size)),
                due_time=config.time_horizon,
            )
        )

    return EVRPTWInstance(
        name=f"synthetic-c{config.num_customers}-s{config.num_stations}-seed{config.seed}",
        nodes=tuple(nodes),
        vehicle=VehicleSpec(
            count=config.num_vehicles,
            capacity=config.vehicle_capacity,
            battery_capacity=config.battery_capacity,
            energy_rate=config.energy_rate,
            speed=config.speed,
            charging_rate=config.charging_rate,
        ),
    )

