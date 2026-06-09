"""Result records shared by baselines and learned policies."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from evrptw.core.instance import EVRPTWInstance
from evrptw.core.simulator import RouteState, is_complete


@dataclass(frozen=True, slots=True)
class SolutionMetrics:
    instance: str
    algorithm: str
    feasible: bool
    total_distance: float
    vehicles_used: int
    charging_visits: int
    charging_time: float
    customers_served: int
    customer_count: int
    routes: tuple[tuple[int, ...], ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def collect_metrics(
    instance: EVRPTWInstance,
    state: RouteState,
    algorithm: str,
) -> SolutionMetrics:
    return SolutionMetrics(
        instance=instance.name,
        algorithm=algorithm,
        feasible=is_complete(instance, state),
        total_distance=state.total_distance,
        vehicles_used=state.vehicles_used,
        charging_visits=state.charging_visits,
        charging_time=state.charging_time,
        customers_served=len(state.visited_customers),
        customer_count=len(instance.customer_ids),
        routes=tuple(tuple(route) for route in state.routes),
    )

