#!/usr/bin/env bash
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

# Chapter 12 — Everyday Git commands (safe demo).
# This script prints commonly used commands and runs a few safe ones
# in a temporary demo directory unless a path is provided.

set -euo pipefail

DEMO_DIR=${1:-demo-repo}
echo "Creating demo dir: $DEMO_DIR"
if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
  echo "DRY RUN: would remove and recreate $DEMO_DIR"
  mkdir -p "$DEMO_DIR" && cd "$DEMO_DIR"
else
  rm -rf "$DEMO_DIR" && mkdir -p "$DEMO_DIR" && cd "$DEMO_DIR"
fi

echo "Initializing repository ..."
if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
  echo "DRY RUN: git init; add README; commit"
else
  git init -q
  printf "# Demo Repo\n\nTiny repo for practice.\n" > README.md
  git add README.md
  git commit -q -m "Add README"
fi

echo "Create a feature branch ..."
if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
  echo "DRY RUN: git switch -c feature/hello; add hello.py; commit"
else
  git switch -c feature/hello -q
  printf "print('Hello, world!')\n" > hello.py
  git add hello.py && git commit -q -m "Add hello script"
fi

echo "Back to main and merge fast-forward ..."
if [[ "${PRIMER_DRY_RUN:-0}" = "1" ]]; then
  echo "DRY RUN: git switch main; git merge --ff-only feature/hello"
else
  git switch -q -c main || git switch -q main
  git merge -q feature/hello --ff-only
fi

cat <<'EOT'
Suggested remote setup (edit USER/REPO):
  git branch -M main
  git remote add origin https://github.com/USER/REPO.git
  git push -u origin main

Undo and safety:
  git restore PATH                 # discard unstaged changes
  git restore --staged PATH        # unstage but keep changes
  git revert COMMIT_SHA            # safe undo (new commit)
EOT

echo "Done. Repo at: $(pwd)"
