#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 1 — Quickstart examples.

- Compute a simple NumPy statistic
- Create and save a tiny Matplotlib plot

Run: python code/01_intro_quickstart.py
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def hello_arrays() -> float:
    """Return the mean of a small array (1, 2, 3, 4)."""
    return np.mean([1, 2, 3, 4])


def hello_plot(path: Path) -> Path:
    """Save a simple sine plot to ``path`` and return the file path."""
    x = np.linspace(0.0, 2.0 * np.pi, 200)
    y = np.sin(x)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6.0, 4.0))
    plt.plot(x, y, label="sin(x)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Hello, line plot")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def main() -> None:
    print("Mean of [1,2,3,4] =", hello_arrays())
    out = Path("figures/hello_line.png")
    print("Saving plot to:", hello_plot(out))


if __name__ == "__main__":
    main()

