import pytest

from evrptw.core.simulator import RouteState, apply_transition, inspect_transition
from evrptw.data.io import load_instance


def test_capacity_violation_is_rejected():
    instance = load_instance("data/samples/tiny_evrptw.json")
    state = RouteState.initial(instance)
    state.remaining_capacity = 1

    transition = inspect_transition(instance, state, 1)

    assert transition.feasible is False
    assert transition.reason == "capacity"


def test_customer_transition_updates_resources():
    instance = load_instance("data/samples/tiny_evrptw.json")
    state = RouteState.initial(instance)

    apply_transition(instance, state, 1)

    assert state.position == 1
    assert state.remaining_capacity == pytest.approx(7)
    assert state.battery < instance.vehicle.battery_capacity
    assert state.visited_customers == {1}


def test_customer_requires_energy_reserve_to_recharge():
    instance = load_instance("data/samples/tiny_evrptw.json")
    state = RouteState.initial(instance)
    state.battery = 3

    transition = inspect_transition(instance, state, 1)

    assert transition.feasible is False
    assert transition.reason == "energy_reserve"
