#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 9 — Matplotlib: basic figures saved to figures/.

Run: python code/09_matplotlib.py
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def save_line(path: Path) -> None:
    x = np.linspace(0.0, 2.0 * np.pi, 400)
    y = np.sin(x)
    plt.figure(figsize=(6.4, 4.0))
    plt.plot(x, y, label="sin(x)")
    plt.legend(); plt.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(path, dpi=150); plt.close()


def save_scatter(path: Path) -> None:
    rng = np.random.default_rng(0)
    x = rng.normal(size=300)
    y = 0.5 * x + rng.normal(scale=0.6, size=300)
    c = np.hypot(x, y)
    plt.figure(figsize=(6.4, 4.0))
    sc = plt.scatter(x, y, c=c, s=20, cmap="viridis", alpha=0.8, edgecolor="none")
    plt.colorbar(sc, label="sqrt(x^2+y^2)")
    plt.tight_layout(); plt.savefig(path, dpi=150); plt.close()


def main() -> None:
    out = Path("figures"); out.mkdir(exist_ok=True)
    save_line(out / "fig_line_quick.png")
    save_scatter(out / "fig_scatter_quick.png")
    print("Saved figures to:", out.resolve())


if __name__ == "__main__":
    main()

