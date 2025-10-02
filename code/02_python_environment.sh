#!/usr/bin/env bash
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

# Chapter 2 — Python Environment quick tasks.
# Safe to run multiple times. Creates .venv in current folder if missing.

set -euo pipefail

echo "Python version:" && python3 --version || true
echo "pip version:" && python3 -m pip --version || true

if [ ! -d .venv ]; then
  if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
    echo "DRY RUN: would create .venv"
  else
    echo "Creating .venv ..."
    python3 -m venv .venv
  fi
fi

echo "Upgrading pip in .venv (subshell) ..."
# Note: activation in a script does not persist to the parent shell.
if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
  echo "DRY RUN: source .venv/bin/activate && python -m pip install --upgrade pip"
else
  source .venv/bin/activate && python -m pip -q install --upgrade pip && deactivate
fi

echo "Freeze current site packages (if venv active in parent shell)."
echo "Run: python -m pip freeze > requirements.txt"

echo "To add a Jupyter kernel (from an active venv) run:"
cat <<'EOT'
python -m ipykernel install --user \
  --name py-primer --display-name "Python (py-primer)"
EOT
