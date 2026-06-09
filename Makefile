.PHONY: setup verify smoke test lint format notebook

setup:
	uv sync --all-groups

verify:
	uv run python scripts/verify_environment.py

smoke:
	uv run evrptw solve-greedy --instance data/samples/tiny_evrptw.json
	uv run evrptw model-smoke --config configs/problem/small.yaml

test:
	uv run pytest -q

lint:
	uv run ruff check .

format:
	uv run ruff format .
	uv run ruff check --fix .

notebook:
	uv run --group notebook jupyter lab

