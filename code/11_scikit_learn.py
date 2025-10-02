#!/usr/bin/env python3
# Python Primer for Data Science and Deep Learning
# (c) Dr. Yves J. Hilpisch
# AI-Powered by GPT-5

"""Chapter 11 — scikit-learn quick baselines.

Skips gracefully if scikit-learn is not installed.
"""

from __future__ import annotations

import sys


def main() -> None:
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        from sklearn.datasets import make_classification, make_regression
        from sklearn.linear_model import LogisticRegression, LinearRegression
        from sklearn.metrics import accuracy_score, r2_score
    except Exception as exc:  # pragma: no cover
        print("scikit-learn not available:", exc)
        sys.exit(0)

    X, y = make_classification(n_samples=600, n_features=6, n_informative=4,
                                random_state=0)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42,
                                          stratify=y)
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    clf.fit(Xtr, ytr)
    acc = accuracy_score(yte, clf.predict(Xte))
    print(f"logreg accuracy: {acc:.3f}")

    Xr, yr = make_regression(n_samples=500, n_features=4, noise=10.0,
                              random_state=1)
    Xtr, Xte, ytr, yte = train_test_split(Xr, yr, test_size=0.2,
                                          random_state=42)
    reg = make_pipeline(StandardScaler(), LinearRegression())
    reg.fit(Xtr, ytr)
    r2 = r2_score(yte, reg.predict(Xte))
    print(f"linear reg R^2: {r2:.3f}")


if __name__ == "__main__":
    main()

