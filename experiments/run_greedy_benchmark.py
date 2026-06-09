"""Run the greedy baseline over configured synthetic seeds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from evrptw.baselines.greedy import solve_greedy
from evrptw.config import load_yaml
from evrptw.data.generator import GeneratorConfig, generate_instance
from evrptw.evaluation.metrics import collect_metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/experiment/greedy_small.yaml")
    args = parser.parse_args()
    experiment = load_yaml(args.config)
    problem = load_yaml(experiment["problem_config"])
    output = Path(experiment["output"])
    output.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for seed in experiment["seeds"]:
        instance = generate_instance(GeneratorConfig(**{**problem, "seed": seed}))
        try:
            state = solve_greedy(instance)
            record = collect_metrics(instance, state, experiment["solver"]).to_dict()
            record["error"] = None
        except RuntimeError as exc:
            record = {
                "instance": instance.name,
                "algorithm": experiment["solver"],
                "feasible": False,
                "error": str(exc),
            }
        records.append(record)

    output.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )
    print(f"Wrote {len(records)} records to {output}")


if __name__ == "__main__":
    main()
