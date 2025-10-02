#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 6 — Lightweight classes and equality semantics."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "USD"

    def __post_init__(self) -> None:  # quick sanity
        if self.amount < 0:
            raise ValueError("amount must be >= 0")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)


def main() -> None:
    a = Money(10, "USD")
    b = Money(5, "USD")
    print("a + b =", a + b)
    print("equality:", Money(10, "USD") == Money(10, "USD"))


if __name__ == "__main__":
    main()

