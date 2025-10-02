#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Run/validate chapter scripts in code/.

Features
- Discovers Python scripts (NN_*.py) and runs them with the current interpreter.
- Optionally runs bash scripts (NN_*.sh) with PRIMER_DRY_RUN=1 for safety.
- Captures return codes and durations; prints a compact summary.

Usage
  python code/run_all.py                 # run Python scripts only
  python code/run_all.py --with-bash     # also run bash scripts (dry-run)
  python code/run_all.py --list          # list discovered scripts

Environment
  MPLBACKEND=Agg is set for headless plotting.
  PRIMER_DRY_RUN=1 is passed to bash scripts by default.
"""

from __future__ import annotations

import argparse
import os
import subprocess as sp
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


CODE_DIR = Path(__file__).resolve().parent


@dataclass
class Result:
    name: str
    kind: str  # "py" or "sh"
    returncode: int
    duration: float

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def discover(pattern: str) -> List[Path]:
    return sorted(CODE_DIR.glob(pattern))


def run_py(script: Path, timeout: float) -> Result:
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    t0 = time.perf_counter()
    proc = sp.run([sys.executable, str(script)], env=env, stdout=sp.PIPE,
                  stderr=sp.STDOUT, timeout=timeout, text=True)
    dur = time.perf_counter() - t0
    print(f"[py] {script.name} -> rc={proc.returncode} ({dur:.2f}s)")
    if proc.stdout:
        print(proc.stdout.strip()[:10_000])
    return Result(script.name, "py", proc.returncode, dur)


def run_sh(script: Path, timeout: float) -> Result:
    env = os.environ.copy()
    env.setdefault("PRIMER_DRY_RUN", "1")
    t0 = time.perf_counter()
    proc = sp.run(["bash", str(script)], env=env, stdout=sp.PIPE,
                  stderr=sp.STDOUT, timeout=timeout, text=True)
    dur = time.perf_counter() - t0
    print(f"[sh] {script.name} -> rc={proc.returncode} ({dur:.2f}s)")
    if proc.stdout:
        print(proc.stdout.strip()[:10_000])
    return Result(script.name, "sh", proc.returncode, dur)


def main(argv: Iterable[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--timeout", type=float, default=60.0,
                   help="per-script timeout in seconds (default: 60)")
    p.add_argument("--with-bash", action="store_true",
                   help="also run bash scripts (dry-run)")
    p.add_argument("--list", action="store_true", help="list scripts and exit")
    args = p.parse_args(list(argv) if argv is not None else None)

    pys = discover("[0-9][0-9]_*.py")
    shs = discover("[0-9][0-9]_*.sh") if args.with_bash else []

    if args.list:
        for s in pys:
            print("[py]", s.name)
        for s in shs:
            print("[sh]", s.name)
        return 0

    results: List[Result] = []
    for s in pys:
        try:
            results.append(run_py(s, args.timeout))
        except sp.TimeoutExpired:
            print(f"[py] {s.name} timed out ({args.timeout}s)")
            results.append(Result(s.name, "py", 124, args.timeout))

    for s in shs:
        try:
            results.append(run_sh(s, args.timeout))
        except sp.TimeoutExpired:
            print(f"[sh] {s.name} timed out ({args.timeout}s)")
            results.append(Result(s.name, "sh", 124, args.timeout))

    # Summary
    ok = sum(r.ok for r in results)
    total = len(results)
    print("\nSummary:")
    for r in results:
        status = "OK" if r.ok else f"FAIL({r.returncode})"
        print(f"  {r.kind} {r.name:28} {status:10} {r.duration:6.2f}s")
    print(f"\nPassed {ok}/{total} scripts")
    return 0 if ok == total else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

