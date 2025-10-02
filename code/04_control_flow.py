#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 4 — Control flow: decisions, loops, and exceptions."""

from __future__ import annotations


def bucket(x: int) -> str:
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    else:
        return "positive"


def safe_div(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError:
        return None


def main() -> None:
    print([bucket(i) for i in (-1, 0, 1)])
    print("safe_div(4, 2)=", safe_div(4, 2))
    print("safe_div(1, 0)=", safe_div(1, 0))


if __name__ == "__main__":
    main()

