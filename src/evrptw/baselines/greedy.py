"""A deterministic feasibility-first EVRP-TW baseline."""

from __future__ import annotations

from evrptw.core.instance import EVRPTWInstance, NodeType
from evrptw.core.simulator import (
    RouteState,
    apply_transition,
    feasible_action_mask,
    is_complete,
)


def _best_customer(instance: EVRPTWInstance, state: RouteState, feasible: list[int]) -> int:
    return min(
        feasible,
        key=lambda node_id: (
            instance.nodes[node_id].due_time,
            instance.distance(state.position, node_id),
            node_id,
        ),
    )


def solve_greedy(instance: EVRPTWInstance) -> RouteState:
    state = RouteState.initial(instance)
    max_steps = len(instance.customer_ids) * 8 + instance.vehicle.count * 4

    for _ in range(max_steps):
        if is_complete(instance, state):
            return state

        mask = feasible_action_mask(instance, state)
        customer_actions = [
            node_id
            for node_id in instance.customer_ids
            if mask[node_id]
        ]
        if customer_actions:
            apply_transition(instance, state, _best_customer(instance, state, customer_actions))
            continue

        if state.visited_customers == set(instance.customer_ids):
            if mask[0]:
                apply_transition(instance, state, 0)
                continue

        station_actions = [
            station_id
            for station_id in instance.station_ids
            if mask[station_id] and instance.nodes[station_id].kind is NodeType.STATION
        ]
        if station_actions and (
            state.battery < instance.vehicle.battery_capacity * 0.75 or not mask[0]
        ):
            station = min(
                station_actions,
                key=lambda node_id: instance.distance(state.position, node_id),
            )
            apply_transition(instance, state, station)
            continue

        if mask[0]:
            apply_transition(instance, state, 0)
            continue

        raise RuntimeError(
            "Greedy baseline reached a dead end. The instance may be infeasible "
            "or require a stronger charging-station lookahead."
        )

    raise RuntimeError("Greedy baseline exceeded its transition limit.")
