#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 10 — pandas basics quick tour.

Requires: pandas, numpy, matplotlib
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    idx = pd.date_range("2025-01-01", periods=5, freq="D")
    df = pd.DataFrame({
        "price": [100, 101.5, 99.8, 102.2, 103.0],
        "volume": [10, 12, 9, 15, 11],
    }, index=idx)
    # Avoid using the keyword 'return' as a column name via keyword-arg
    df = df.assign(ret=df["price"].pct_change())
    print(df.head())

    ts_idx = pd.date_range("2025-01-01", periods=120, freq="D")
    price = 100 + np.cumsum(np.random.default_rng(0).normal(0, 1.0, len(ts_idx)))
    vol = np.random.default_rng(1).integers(8, 20, len(ts_idx))
    ts = pd.DataFrame({"price": price, "volume": vol}, index=ts_idx)

    ax = ts["price"].plot(figsize=(6.8, 4.2), lw=1.6, color="#1f77b4")
    ts["price"].rolling(14, min_periods=1).mean().plot(
        ax=ax, lw=2.0, color="#ff7f0e"
    )
    ax.set(title="Price with Rolling Mean", xlabel="date", ylabel="price")
    Path("figures").mkdir(exist_ok=True)
    plt.tight_layout(); plt.savefig("figures/pandas_ts_quick.png", dpi=150)
    plt.close()
    print("Saved figures/pandas_ts_quick.png")


if __name__ == "__main__":
    main()
