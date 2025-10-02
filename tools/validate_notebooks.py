#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Validate execution of all notebooks in notebooks/ locally.

Features
- Discovers notebooks (*.ipynb) under notebooks/ (configurable via --pattern)
- Executes each with nbclient (headless; MPLBACKEND=Agg)
- Per-notebook timeout, fail-fast, include/exclude globs
- Saves executed copies to tools/_executed/
- Prints a detailed summary; optional JSON/Markdown reports

Usage
  python tools/validate_notebooks.py
  python tools/validate_notebooks.py --timeout 300 --report-json tools/nb_report.json
  python tools/validate_notebooks.py --include 'notebooks/08_*.ipynb'

Requirements
  pip install nbclient nbformat
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from uuid import uuid4
from pathlib import Path
from typing import Iterable, List, Optional
import re


try:
    import nbformat  # type: ignore
    from nbclient import NotebookClient  # type: ignore
    from nbclient.exceptions import CellExecutionError  # type: ignore
except Exception as exc:  # pragma: no cover
    print("This tool requires nbformat and nbclient.\n"
          "Install with: python -m pip install nbclient nbformat",
          file=sys.stderr)
    raise


@dataclass
class Failure:
    notebook: str
    cell_index: int
    ename: str
    evalue: str
    traceback: List[str]
    snippet: str


@dataclass
class Result:
    notebook: str
    ok: bool
    duration: float
    failure: Optional[Failure] = None


def discover(patterns: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    for pat in patterns:
        paths.extend(sorted(Path().glob(pat)))
    # Default discovery if nothing matched
    if not paths and not patterns:
        paths = sorted(Path("notebooks").glob("*.ipynb"))
    return [p for p in paths if p.is_file()]


def _normalize_ids(nb):
    """Ensure every cell has an ``id`` and normalize structure.

    - Adds a UUID4-based ``id`` to any cell missing one (future-proof for
      nbformat >= 5.1.4 where missing IDs are a hard error).
    - If ``nbformat.validator.normalize`` exists, call it and return only the
      notebook object (some versions may return a tuple).
    """
    # Add missing ids
    try:
        for cell in getattr(nb, "cells", []) or []:
            if not isinstance(cell, dict):
                # NotebookNode behaves like dict; keep as-is
                if not getattr(cell, "id", None):
                    setattr(cell, "id", uuid4().hex)
            else:
                cell.setdefault("id", uuid4().hex)
    except Exception:
        pass
    # Normalize if available
    try:  # nbformat >= 5.1.4
        from nbformat.validator import normalize  # type: ignore

        maybe = normalize(nb)
        # Some versions normalize in-place and return None; some may return
        # (nb, changed). Critically, a few environments can return a boolean/int.
        # Always ensure we return a notebook-like object.
        if maybe is None:
            return nb
        # If it's a tuple, assume first element is the notebook
        if isinstance(maybe, tuple) and maybe:
            candidate = maybe[0]
        else:
            candidate = maybe
        # Verify candidate looks like a notebook
        if hasattr(candidate, "cells") and hasattr(candidate, "metadata"):
            return candidate
        # Fallback to original notebook if the return type is unexpected
        return nb
    except Exception:
        return nb


def _load_notebook(nb_path: Path):
    """Load a notebook robustly.

    Some notebooks might accidentally contain two concatenated JSON documents.
    We try a normal read first; on failure we trim to the last top‑level start
    marker and retry.
    """
    text = nb_path.read_text(encoding="utf-8")
    try:
        return nbformat.reads(text, as_version=4)
    except Exception:
        # Heuristics: notebooks might contain multiple concatenated JSON docs.
        # 1) Find the last occurrence of a top-level object starting before the
        #    last "cells" key.
        idx_cells = text.rfind('"cells"')
        if idx_cells != -1:
            start = text.rfind('{', 0, idx_cells)
            if start != -1:
                trimmed = text[start:]
            return nbformat.reads(trimmed.lstrip(), as_version=4)
        # 2) Fallback to last "\n{" marker
        pos = text.rfind('\n{')
        if pos != -1:
            return nbformat.reads(text[pos + 1 :].lstrip(), as_version=4)
        # 3) Fallback to last '{'
        pos = text.rfind('{')
        if pos != -1:
            return nbformat.reads(text[pos:].lstrip(), as_version=4)
        raise


def execute_notebook(nb_path: Path, timeout: int, kernel: str, exec_dir: Path,
                     normalize_inplace: bool = True) -> Result:
    os.environ.setdefault("MPLBACKEND", "Agg")
    t0 = time.perf_counter()
    nb = _load_notebook(nb_path)
    nb = _normalize_ids(nb)
    # Optionally write the normalized notebook back in place to silence future warnings
    if normalize_inplace:
        try:
            nbformat.write(nb, nb_path)
        except Exception:
            pass
    client = NotebookClient(nb, timeout=timeout, kernel_name=kernel)
    try:
        import asyncio
        try:
            # Prefer explicit async path to avoid event loop policy issues
            asyncio.run(client.async_execute())
        except RuntimeError:
            # If an event loop is already running, fall back to sync execute
            client.execute()
        ok = True
        failure = None
    except CellExecutionError as e:  # gather details
        ok = False
        # locate the errored cell
        cell_idx = getattr(e, "cell_index", -1)
        # find last error output
        ename = getattr(e, "ename", "ExecutionError")
        evalue = getattr(e, "evalue", str(e))
        tb: List[str] = []
        snippet = ""
        try:
            if 0 <= cell_idx < len(nb.cells):
                cell = nb.cells[cell_idx]
                src = cell.get("source", "")
                snippet = "\n".join(str(src).splitlines()[:20])
                for out in cell.get("outputs", []):
                    if out.get("output_type") == "error":
                        ename = out.get("ename", ename)
                        evalue = out.get("evalue", evalue)
                        tb = out.get("traceback", [])
        except Exception:
            pass
        failure = Failure(nb_path.name, cell_idx, ename, evalue, tb, snippet)
    # save executed notebook
    exec_dir.mkdir(parents=True, exist_ok=True)
    out_path = exec_dir / (nb_path.stem + ".executed.ipynb")
    try:
        nbformat.write(nb, out_path)
    except Exception:
        pass
    dur = time.perf_counter() - t0
    return Result(nb_path.name, ok, dur, failure)


def print_summary(results: List[Result]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.ok)
    print("\nNotebook validation summary:")
    for r in results:
        status = "OK" if r.ok else "FAIL"
        print(f"  {r.notebook:40} {status:6} {r.duration:6.2f}s")
    print(f"\nPassed {passed}/{total} notebooks")
    fails = [r for r in results if not r.ok]
    if fails:
        print("\nDetailed failures:")
        for r in fails:
            f = r.failure
            if not f:
                continue
            print(f"\n--- {f.notebook} (cell {f.cell_index}) ---")
            print(f"{f.ename}: {f.evalue}")
            if f.traceback:
                print("Traceback (most recent call last):")
                for line in f.traceback[-20:]:
                    print(line)
            if f.snippet:
                print("\nCell snippet:\n" + f.snippet)


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--include", action="append", default=["notebooks/*.ipynb"],
                   help="glob(s) of notebooks to include (default: notebooks/*.ipynb)")
    p.add_argument("--exclude", action="append", default=[],
                   help="globs to exclude (applied after include)")
    p.add_argument("--timeout", type=int, default=300,
                   help="per-notebook timeout in seconds (default: 300)")
    p.add_argument("--kernel", default="python3",
                   help="Jupyter kernel name (default: python3)")
    p.add_argument("--fail-fast", action="store_true",
                   help="stop at first failure")
    p.add_argument("--report-json", type=Path,
                   help="write a JSON report with detailed results")
    p.add_argument("--report-md", type=Path,
                   help="write a Markdown summary report")
    args = p.parse_args(list(argv) if argv is not None else None)

    # Discover notebooks
    inc = discover(args.include)
    # Exclude patterns
    excludes: List[Path] = []
    for pat in args.exclude:
        excludes.extend(Path().glob(pat))
    excl_set = {p.resolve() for p in excludes}
    nbs = [p for p in inc if p.resolve() not in excl_set]
    if not nbs:
        print("No notebooks found for patterns:", args.include)
        return 1

    results: List[Result] = []
    exec_dir = Path("tools/_executed")
    rc = 0
    for nb in nbs:
        print(f"[nb] executing {nb} ...")
        res = execute_notebook(nb, args.timeout, args.kernel, exec_dir,
                               normalize_inplace=True)
        results.append(res)
        if not res.ok:
            rc = 2
            if args.fail_fast:
                break

    print_summary(results)

    # JSON report
    if args.report_json:
        payload = [
            {
                "notebook": r.notebook,
                "ok": r.ok,
                "duration": r.duration,
                "failure": asdict(r.failure) if r.failure else None,
            }
            for r in results
        ]
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(payload, indent=2))

    # Markdown report
    if args.report_md:
        lines = ["# Notebook Validation Report", ""]
        for r in results:
            status = "✅ OK" if r.ok else "❌ FAIL"
            lines.append(f"- {status} `{r.notebook}` — {r.duration:.2f}s")
        fails = [r for r in results if not r.ok]
        if fails:
            lines.append("\n## Failures")
            for r in fails:
                f = r.failure
                if not f:
                    continue
                lines.append(f"\n### {f.notebook} (cell {f.cell_index})")
                lines.append(f"**{f.ename}:** {f.evalue}")
                if f.snippet:
                    lines.append("\n```python\n" + f.snippet + "\n```")
        args.report_md.parent.mkdir(parents=True, exist_ok=True)
        args.report_md.write_text("\n".join(lines))

    return rc


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
