# EVRP-TW DeepRL

A reproducible research framework for the Electric Vehicle Routing Problem with
Time Windows (EVRP-TW), with classical baselines, constraint-level evaluation,
and attention-based reinforcement-learning components.

## Research Scope

The first milestone targets a homogeneous electric fleet with:

- customer demand and vehicle-capacity constraints;
- customer time windows and service durations;
- battery consumption proportional to travel distance;
- optional charging-station visits and full recharging;
- multiple routes bounded by the available vehicle count.

The repository separates problem semantics from algorithms so that OR-Tools,
heuristics, POMO-style policies, local search, and hybrid repair methods can be
compared under the same feasibility checker.

## Quick Start

Requirements: Python 3.11 and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
make verify
make smoke
make test
```

Run the command-line interface:

```bash
# Generate a deterministic instance.
uv run evrptw generate --config configs/problem/small.yaml --output data/generated/demo.json

# Solve it with the greedy baseline and write structured metrics.
uv run evrptw solve-greedy \
  --instance data/generated/demo.json \
  --output results/greedy_demo.json

# Check the attention policy output against a dynamic feasibility mask.
uv run evrptw model-smoke --config configs/problem/small.yaml
```

## Repository Layout

```text
configs/                 Problem and experiment configurations
data/samples/            Small version-controlled instances
docs/                    Formulation and experiment protocol
experiments/             Reproducible experiment entry points
src/evrptw/
  baselines/             Classical and heuristic solvers
  core/                  Data model, state transition, feasibility
  data/                  Instance generation and serialization
  evaluation/            Shared metrics and result schemas
  models/                DeepRL policy components
tests/                   Unit and integration tests
```

## Current Status

| Component | Status |
|---|---|
| EVRP-TW data model and JSON format | Available |
| Dynamic capacity/time/battery constraints | Available |
| Deterministic instance generator | Available |
| Greedy feasible baseline | Available |
| Attention policy network | Initial scaffold |
| OR-Tools mathematical baseline | Planned |
| REINFORCE/POMO training loop | Planned |
| Solomon/Schneider benchmark loaders | Planned |

The attention network is deliberately not presented as a trained solver. It is
an implementation boundary for the next research milestone.

## Reproducibility Standard

Every reported experiment must include:

- Git commit and `uv.lock`;
- instance source and preprocessing;
- random seed and full configuration;
- objective and feasibility together;
- capacity, time-window, energy, and fleet-size violations;
- runtime, hardware, and selected compute device.

See [experiment protocol](docs/experiment_protocol.md) and
[problem formulation](docs/problem_formulation.md).

## Development

```bash
make format
make lint
make test
```

Work on a feature branch and use a pull request. Keep generated data, raw
benchmarks, checkpoints, and tracking logs out of Git.
