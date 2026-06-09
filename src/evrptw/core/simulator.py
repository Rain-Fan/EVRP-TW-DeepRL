"""Canonical EVRP-TW state transitions and feasibility checks."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from evrptw.core.instance import EVRPTWInstance, NodeType

EPSILON = 1e-9


@dataclass(slots=True)
class RouteState:
    position: int
    time: float
    remaining_capacity: float
    battery: float
    vehicles_used: int
    visited_customers: set[int] = field(default_factory=set)
    routes: list[list[int]] = field(default_factory=lambda: [[0]])
    total_distance: float = 0.0
    charging_visits: int = 0
    charging_time: float = 0.0

    @classmethod
    def initial(cls, instance: EVRPTWInstance) -> RouteState:
        vehicle = instance.vehicle
        return cls(
            position=0,
            time=instance.nodes[0].ready_time,
            remaining_capacity=vehicle.capacity,
            battery=vehicle.battery_capacity,
            vehicles_used=1,
        )

    @property
    def current_route(self) -> list[int]:
        return self.routes[-1]


@dataclass(frozen=True, slots=True)
class Transition:
    feasible: bool
    reason: str | None
    arrival: float
    service_start: float
    battery_after_travel: float


def inspect_transition(
    instance: EVRPTWInstance,
    state: RouteState,
    target: int,
) -> Transition:
    if target < 0 or target >= len(instance.nodes):
        return Transition(False, "unknown_node", 0.0, 0.0, state.battery)
    if target == state.position:
        return Transition(False, "same_node", state.time, state.time, state.battery)

    node = instance.nodes[target]
    if node.kind is NodeType.CUSTOMER and target in state.visited_customers:
        return Transition(False, "customer_already_visited", 0.0, 0.0, state.battery)
    if node.kind is NodeType.CUSTOMER and node.demand > state.remaining_capacity + EPSILON:
        return Transition(False, "capacity", 0.0, 0.0, state.battery)
    if (
        node.kind is NodeType.DEPOT
        and state.visited_customers != set(instance.customer_ids)
        and state.vehicles_used >= instance.vehicle.count
    ):
        return Transition(False, "fleet", 0.0, 0.0, state.battery)

    energy = instance.energy(state.position, target)
    battery_after = state.battery - energy
    if battery_after < -EPSILON:
        return Transition(False, "energy", 0.0, 0.0, battery_after)

    arrival = state.time + instance.travel_time(state.position, target)
    service_start = max(arrival, node.ready_time)
    if service_start > node.due_time + EPSILON:
        return Transition(False, "time_window", arrival, service_start, battery_after)

    if node.kind is NodeType.CUSTOMER:
        recharge_nodes = (0, *instance.station_ids)
        reserve = min(instance.energy(target, recharge_id) for recharge_id in recharge_nodes)
        if battery_after + EPSILON < reserve:
            return Transition(False, "energy_reserve", arrival, service_start, battery_after)

    if target == 0 and len(state.current_route) == 1:
        return Transition(False, "empty_route", arrival, service_start, battery_after)

    return Transition(True, None, arrival, service_start, battery_after)


def feasible_action_mask(instance: EVRPTWInstance, state: RouteState) -> np.ndarray:
    return np.asarray(
        [inspect_transition(instance, state, node.id).feasible for node in instance.nodes],
        dtype=bool,
    )


def apply_transition(instance: EVRPTWInstance, state: RouteState, target: int) -> None:
    transition = inspect_transition(instance, state, target)
    if not transition.feasible:
        raise ValueError(f"Infeasible transition to node {target}: {transition.reason}")

    node = instance.nodes[target]
    travel_distance = instance.distance(state.position, target)
    state.total_distance += travel_distance
    state.battery = max(0.0, transition.battery_after_travel)
    state.position = target
    state.time = transition.service_start + node.service_time
    state.current_route.append(target)

    if node.kind is NodeType.CUSTOMER:
        state.remaining_capacity -= node.demand
        state.visited_customers.add(target)
    elif node.kind is NodeType.STATION:
        energy_needed = instance.vehicle.battery_capacity - state.battery
        duration = energy_needed / instance.vehicle.charging_rate
        state.battery = instance.vehicle.battery_capacity
        state.time += duration
        state.charging_visits += 1
        state.charging_time += duration
    elif node.kind is NodeType.DEPOT:
        if state.visited_customers != set(instance.customer_ids):
            state.vehicles_used += 1
            state.routes.append([0])
            state.time = instance.nodes[0].ready_time
            state.remaining_capacity = instance.vehicle.capacity
            state.battery = instance.vehicle.battery_capacity


def is_complete(instance: EVRPTWInstance, state: RouteState) -> bool:
    return (
        state.visited_customers == set(instance.customer_ids)
        and state.position == 0
    )
