#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 7 — Idiomatic Python patterns."""

from __future__ import annotations


def eafp_get_price(record: dict) -> float | None:
    try:  # EAFP over LBYL
        return float(record["price"])  # may KeyError / ValueError
    except (KeyError, ValueError):
        return None


def main() -> None:
    xs = [x * x for x in range(6) if x % 2 == 0]
    print("even squares:", xs)
    print("safe price:", eafp_get_price({"price": "101.5"}))
    print("bad price:", eafp_get_price({"price": "n/a"}))


if __name__ == "__main__":
    main()

