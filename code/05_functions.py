#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 5 — Functions: signatures, defaults, closures."""

from __future__ import annotations
from math import pi
from functools import wraps


def vol_sphere(r: float) -> float:
    """Volume of a sphere with radius ``r``."""
    return 4.0 / 3.0 * pi * r ** 3


def memoize(fn):
    cache: dict[tuple, object] = {}

    @wraps(fn)
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]

    return wrapper


@memoize
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def main() -> None:
    print("vol_sphere(2.0)=", vol_sphere(2.0))
    print("fib(10)=", fib(10))


if __name__ == "__main__":
    main()

