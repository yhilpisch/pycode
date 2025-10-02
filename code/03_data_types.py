#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 3 — Data types and containers (tiny tour)."""


def main() -> None:
    # Scalars and strings
    price = 101.5
    name = "Ada"
    print(f"Hello, {name}! Price = {price}")

    # Lists, tuples, sets, dicts
    pages = [10, 15, 12]
    pages.append(20)
    avg = sum(pages) / len(pages)
    print("pages:", pages, "avg:", avg)

    trade = ("AAPL", 100, 190.5)
    sym, qty, px = trade
    print("trade value:", qty * px)

    attendees = {"Ada", "Alan", "Grace"}
    attendees.add("Ada")  # set keeps unique values
    print("attendees:", sorted(attendees))

    sizes = {"S": 1, "M": 2, "L": 3}
    print("sizes:", sizes)


if __name__ == "__main__":
    main()

