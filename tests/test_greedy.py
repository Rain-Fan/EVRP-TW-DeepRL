from evrptw.baselines.greedy import solve_greedy
from evrptw.core.simulator import is_complete
from evrptw.data.io import load_instance
from evrptw.evaluation.metrics import collect_metrics


def test_greedy_solves_tiny_instance():
    instance = load_instance("data/samples/tiny_evrptw.json")
    state = solve_greedy(instance)
    metrics = collect_metrics(instance, state, "greedy")

    assert is_complete(instance, state)
    assert metrics.feasible is True
    assert metrics.customers_served == 3
    assert metrics.total_distance > 0

