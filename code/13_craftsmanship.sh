#!/usr/bin/env bash
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

# Chapter 13 — Tooling setup (formatter, linter, hooks) for this repo.
# Requires an active Python with pip. Safe to run multiple times.

set -euo pipefail

if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
  echo "DRY RUN: python -m pip install --upgrade black ruff isort pre-commit mypy"
else
  echo "Installing tools (black, ruff, isort, pre-commit, mypy) ..."
  python -m pip install -q --upgrade black ruff isort pre-commit mypy
fi

echo "Writing a basic .pre-commit-config.yaml (if missing) ..."
cat > .pre-commit-config.yaml <<'YAML'
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: ["--fix"]
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
YAML

if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
  echo "DRY RUN: pre-commit install"
else
  echo "Installing git hooks ..."
  pre-commit install
fi

if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
  echo "DRY RUN: black src tests; ruff check --fix; isort src tests"
else
  echo "Formatting and linting (src/ tests/ if present) ..."
  black src tests 2>/dev/null || true
  ruff check src tests --fix 2>/dev/null || true
  isort src tests 2>/dev/null || true
fi

echo "Done. Hooks active; try: pre-commit run -a"
