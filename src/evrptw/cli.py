"""Command-line entry points for reproducible EVRP-TW experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from evrptw.baselines.greedy import solve_greedy
from evrptw.config import load_yaml
from evrptw.core.simulator import RouteState, feasible_action_mask
from evrptw.data.generator import GeneratorConfig, generate_instance
from evrptw.data.io import load_instance, save_instance
from evrptw.evaluation.metrics import collect_metrics
from evrptw.models import AttentionPolicy
from evrptw.models.features import dynamic_state_features, static_node_features


def _write_or_print(data: dict[str, object], output: str | None) -> None:
    rendered = json.dumps(data, indent=2)
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


def generate_command(args: argparse.Namespace) -> None:
    config = GeneratorConfig(**load_yaml(args.config))
    instance = generate_instance(config)
    save_instance(instance, args.output)
    print(f"Saved {instance.name} to {args.output}")


def solve_greedy_command(args: argparse.Namespace) -> None:
    instance = load_instance(args.instance)
    state = solve_greedy(instance)
    metrics = collect_metrics(instance, state, algorithm="greedy")
    _write_or_print(metrics.to_dict(), args.output)


def model_smoke_command(args: argparse.Namespace) -> None:
    torch.manual_seed(42)
    instance = generate_instance(GeneratorConfig(**load_yaml(args.config)))
    state = RouteState.initial(instance)
    node_features = static_node_features(instance)
    state_features = dynamic_state_features(instance, state)
    action_mask = torch.from_numpy(feasible_action_mask(instance, state))
    policy = AttentionPolicy()
    policy.eval()
    with torch.inference_mode():
        logits = policy(
            node_features,
            state_features,
            current_node=torch.tensor([state.position]),
            action_mask=action_mask,
        )
    report = {
        "instance": instance.name,
        "logits_shape": list(logits.shape),
        "feasible_actions": torch.where(action_mask)[0].tolist(),
        "selected_action": int(logits.argmax(dim=-1).item()),
        "parameter_count": sum(parameter.numel() for parameter in policy.parameters()),
    }
    _write_or_print(report, None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evrptw")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate a synthetic instance.")
    generate_parser.add_argument("--config", required=True)
    generate_parser.add_argument("--output", required=True)
    generate_parser.set_defaults(handler=generate_command)

    greedy_parser = subparsers.add_parser("solve-greedy", help="Run the greedy baseline.")
    greedy_parser.add_argument("--instance", required=True)
    greedy_parser.add_argument("--output")
    greedy_parser.set_defaults(handler=solve_greedy_command)

    model_parser = subparsers.add_parser("model-smoke", help="Run one policy forward pass.")
    model_parser.add_argument("--config", required=True)
    model_parser.set_defaults(handler=model_smoke_command)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()

