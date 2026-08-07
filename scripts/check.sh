#!/usr/bin/env sh
set -eu

uv run --locked ruff check app tests
uv run --locked ruff format --check app tests
uv run --locked pyright
uv run --locked pytest --cov=app --cov-report=term-missing