#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Validate chapter scripts under code/.

Features
- Discovers code scripts (NN_*.py) and runs them with the current interpreter.
- Optionally runs bash scripts (NN_*.sh) with PRIMER_DRY_RUN=1 for safety.
- Per-script timeout, fail-fast, include/exclude globs
- Prints a detailed summary; optional JSON/Markdown reports

Usage
  python tools/validate_code.py
  python tools/validate_code.py --with-bash --timeout 90 \
      --report-json tools/code_report.json --report-md tools/code_report.md

Requirements
  Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess as sp
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class Result:
    path: str
    kind: str  # py or sh
    ok: bool
    duration: float
    returncode: int
    stdout: Optional[str] = None


def discover(patterns: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    for pat in patterns:
        paths.extend(sorted(Path().glob(pat)))
    # Default discovery if nothing matched
    if not paths and not patterns:
        paths = sorted(Path("code").glob("[0-9][0-9]_*.py"))
    # Filter to files
    return [p for p in paths if p.is_file()]


def run_py(path: Path, timeout: int) -> Result:
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    t0 = time.perf_counter()
    proc = sp.run([sys.executable, str(path)], env=env, text=True, capture_output=True, timeout=timeout)
    dur = time.perf_counter() - t0
    print(f"[py] {path} -> rc={proc.returncode} ({dur:.2f}s)")
    if proc.stdout:
        print(proc.stdout.strip()[:10_000])
    if proc.stderr and proc.returncode != 0:
        print(proc.stderr.strip()[:5_000])
    return Result(str(path), "py", proc.returncode == 0, dur, proc.returncode,
                  (proc.stdout or "")[-5_000:])


def run_sh(path: Path, timeout: int) -> Result:
    env = os.environ.copy()
    env.setdefault("PRIMER_DRY_RUN", "1")
    t0 = time.perf_counter()
    proc = sp.run(["bash", str(path)], env=env, text=True, capture_output=True, timeout=timeout)
    dur = time.perf_counter() - t0
    print(f"[sh] {path} -> rc={proc.returncode} ({dur:.2f}s)")
    if proc.stdout:
        print(proc.stdout.strip()[:10_000])
    if proc.stderr and proc.returncode != 0:
        print(proc.stderr.strip()[:5_000])
    return Result(str(path), "sh", proc.returncode == 0, dur, proc.returncode,
                  (proc.stdout or "")[-5_000:])


def print_summary(results: List[Result]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.ok)
    print("\nCode validation summary:")
    for r in results:
        status = "OK" if r.ok else f"FAIL({r.returncode})"
        print(f"  {Path(r.path).name:28} {r.kind:2} {status:10} {r.duration:6.2f}s")
    print(f"\nPassed {passed}/{total} scripts")


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--include", action="append", default=["code/[0-9][0-9]_*.py"],
                   help="glob(s) to include (default: code/[0-9][0-9]_*.py)")
    p.add_argument("--exclude", action="append", default=[],
                   help="globs to exclude (applied after include)")
    p.add_argument("--with-bash", action="store_true",
                   help="also include bash scripts (code/[0-9][0-9]_*.sh)")
    p.add_argument("--timeout", type=int, default=60,
                   help="per-script timeout in seconds (default: 60)")
    p.add_argument("--fail-fast", action="store_true",
                   help="stop at first failure")
    p.add_argument("--report-json", type=Path,
                   help="write a JSON report with detailed results")
    p.add_argument("--report-md", type=Path,
                   help="write a Markdown summary report")
    p.add_argument("--list", action="store_true",
                   help="list discovered scripts and exit")
    args = p.parse_args(list(argv) if argv is not None else None)

    inc = discover(args.include)
    # Optionally extend with bash discovery
    if args.with_bash:
        inc.extend(discover(["code/[0-9][0-9]_*.sh"]))
    # Apply excludes
    excludes: List[Path] = []
    for pat in args.exclude:
        excludes.extend(Path().glob(pat))
    excl_set = {p.resolve() for p in excludes}
    scripts = [p for p in inc if p.resolve() not in excl_set]
    if not scripts:
        print("No scripts found for patterns:", args.include)
        return 1

    if args.list:
        for s in scripts:
            kind = "sh" if s.suffix == ".sh" else "py"
            print(f"[{kind}] {s}")
        return 0

    results: List[Result] = []
    rc = 0
    for s in scripts:
        try:
            if s.suffix == ".sh":
                res = run_sh(s, args.timeout)
            else:
                res = run_py(s, args.timeout)
            results.append(res)
            if not res.ok:
                rc = 2
                if args.fail_fast:
                    break
        except sp.TimeoutExpired:
            print(f"[{('sh' if s.suffix == '.sh' else 'py')}] {s.name} timed out ({args.timeout}s)")
            results.append(Result(str(s), "sh" if s.suffix == ".sh" else "py", False, float(args.timeout), 124))
            rc = 2
            if args.fail_fast:
                break

    print_summary(results)

    # Reports
    if args.report_json:
        payload = [
            {
                "path": r.path,
                "kind": r.kind,
                "ok": r.ok,
                "duration": r.duration,
                "returncode": r.returncode,
            }
            for r in results
        ]
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(payload, indent=2))

    if args.report_md:
        lines = ["# Code Validation Report", ""]
        for r in results:
            status = "✅ OK" if r.ok else f"❌ FAIL ({r.returncode})"
            lines.append(f"- {status} `{Path(r.path).name}` — {r.duration:.2f}s")
        args.report_md.parent.mkdir(parents=True, exist_ok=True)
        args.report_md.write_text("\n".join(lines))

    return rc


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

