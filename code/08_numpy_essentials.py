#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 8 — NumPy essentials quick tour."""

import numpy as np


def main() -> None:
    a = np.arange(12).reshape(3, 4)
    print("a shape, ndim:", a.shape, a.ndim)

    view = a[:, 1:3]
    view[:] = -1
    print("modified a[0]:", a[0])

    # Broadcast across the last axis (columns): need 4 elements to match
    b = np.arange(4)
    print("broadcast add:", (a + b)[0])

    v = np.array([3.0, 4.0])
    M = np.array([[1.0, 2.0], [3.0, 4.0]])
    print("norm(v)=", np.linalg.norm(v))
    print("M@v=", M @ v)

    S = np.array([[2.0, 1.0], [1.0, 2.0]])
    w, U = np.linalg.eigh(S)
    print("eigh w:", w)


if __name__ == "__main__":
    main()
