# Experiment Protocol

## Comparison Ladder

1. deterministic greedy feasibility-first baseline;
2. OR-Tools or PyVRP classical baseline;
3. attention policy trained with REINFORCE;
4. POMO-style multi-start decoding;
5. learned construction plus local-search repair.

Do not compare later stages until the shared feasibility checker passes for all
algorithms.

## Required Record

Each run must record:

- instance name, source, size, and preprocessing;
- algorithm version and full configuration;
- random seed;
- total distance and feasibility;
- customers served and vehicles used;
- capacity, time-window, energy, and fleet violations;
- charging visits and charging time;
- wall-clock runtime and hardware.

## Dataset Splits

Synthetic training, validation, and test seeds must not overlap. Public
benchmarks must retain their original instance names. Any coordinate, time, or
energy scaling must be documented and version controlled.

## Statistical Reporting

For learned methods report mean, standard deviation, and feasibility rate over
multiple seeds. For stochastic decoding, separate training seeds from inference
seeds. Compare objective gaps only among feasible solutions.

